from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
# @login_required(login_url='/login/')

def landing_page(request):
    three_days_ago = timezone.now() - timedelta(days=3)
    newses = News.objects.filter(
        created_at__gte=three_days_ago,
        is_published=True
    ).order_by('-created_at')[:5] 
    
    context ={
        'newses':newses
    }
    return render(request, 'base/landing_page.html',context)

def explore(request):
    projects = Project.objects.all().order_by('-id')
    context ={
        'projects':projects
    }
    return render(request, 'base/explore.html',context)
    
@login_required(login_url='/login/')
def dashboard(request):
    projects = Project.objects.all().order_by('-id')

    if request.method == "GET":
        value = request.GET.get('value')
        if value:
            filtered_projects = Project.objects.filter(
                Q(title__icontains=value)
            )
            context ={
                'projects':filtered_projects
            }
            return render(request, 'base/home.html',context)
    context ={
        "projects":projects,
    }

    u= request.user
    if u.is_staff:
        try:
            teacher = Teacher.objects.get(user__id = u.id)
        except:
            teacher = None
        context.update({
                "teacher":teacher
            })
    else:
        try:
            student = Student.objects.get(user__id = u.id)   
        except:
            student= None
        context.update({
                "student":student
            })
    
    
   
    return render(request, 'base/home.html', context)

def create_project(request):
    
    students = Student.objects.filter(is_approved=True).order_by('-id')
    teachers = Teacher.objects.all()
    
    if request.method == 'POST':
        try:

            advisor = Teacher.objects.get(id=request.POST['advisor'])

        # Create the dataset first
            dataset = Dataset.objects.create(
                title=request.POST['title'] + " - dataset",
                dataset_link=request.POST.get('dataset_link', ''),
                file=request.FILES.get('dataset_file', ''),
                uploaded_by=advisor.user,
                is_private = request.POST.get('is_private','')
            )

            # Create the project
            project = Project.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                objectives=request.POST.get('objectives', ''),
                hypothesis=request.POST.get('hypothesis', ''),
                publication_link=request.POST.get('publication_link', ''),
                github_link=request.POST.get('github_link', ''),
                methodology=request.POST.get('methodology', ''),
                tools_used=request.POST.get('tools_used', ''),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('start_date',''),
                status=request.POST.get('status', ''),
                advisor=advisor,
                project_picture=request.FILES.get('project_picture', ''),
                project_file=request.FILES.get('project_file', ''),
                dataset_link=dataset,  # Associate the dataset with the project
            )
            
            
            for student_id in request.POST.getlist('students'):
                student = Student.objects.get(id=student_id)
                role = request.POST.get(f'roles_{student_id}')
                
                inst,created = project_studnet.objects.get_or_create(
                    project=project,
                    user=student,
                    role=role
                )
                project.students.add(student)

            messages.success(request, 'Project created successfully!')
            return redirect('project_detail', pk=project.id)

        except Teacher.DoesNotExist:
            messages.error(request, 'Selected advisor does not exist')
        except Student.DoesNotExist:
            messages.error(request, 'One or more selected students do not exist')
 
        except Exception as e:
            messages.error(request, f'Error creating project: {str(e)}')

        return redirect('create_project')
        
    
    # GET request
    context = {
        'teachers': teachers,
        'students': students
    }

    return render(request, 'base/create-project.html',context)

def project_detail(request, pk):
    # project = get_object_or_404(Project.objects.prefetch_related('students'), pk=pk)
    project = Project.objects.get(id = pk)
    print('objectives ',project.students_project.all())
    # print("Project Member: ", project.students.all())
    context = {
        'project': project,
        'tools':project.tools_used.split(","),
        'objectives':project.objectives.split("\n")
    }
    return render(request, 'base/project_details.html', context)

def update_project(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related('students'), pk=pk)
    
    
    context = {
        'project': project,
        'teachers': Teacher.objects.all(),
        'students': Student.objects.all(),
        'update_mode': True,
    }
    return render(request, 'base/update-project.html', context)

def view_student_profile(request, pk):
    student = Student.objects.get(user__id = pk)
    context={'student': student, 'skills':student.skills.split(',')}
       
    return render(request, 'base/profile.html', context)

def teacher(request,pk):
    teacher = Teacher.objects.get(user__id = pk)
    context={'teacher': teacher}
    return render(request, 'base/profile.html', context)
    
    
    
    
    
from django.contrib.auth import authenticate, login, logout
def student_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        profile_picture = request.FILES.get('profile_picture')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('student_register')

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create Student Profile
        Student.objects.create(
            user=user,
            phone=phone,
            profile_picture=profile_picture
        )

        messages.success(request, 'Registration successful! Please login.')
        return redirect('student_login')

    return render(request, 'base/register.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            student =None
            try:
                student =  Student.objects.get(user=user)
            except:
                student = None 
            if student:
                login(request, user)
                return redirect(next_url if next_url else 'home')
            else:
                messages.error(request, 'Unauthenticated Student!')
                return render(request, 'base/login.html')
        else:
            print('Invalid username or password!')
            messages.error(request, 'Invalid username or password!')
    next_url = request.GET.get('next', '')
    return render(request, 'base/login.html',{ 'next': next_url })

@csrf_exempt
def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username="faysalhassantorjo")
        print(user.is_active)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user:
            if Teacher.objects.filter(user=user).exists():
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Unauthenticated Teacher!')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'base/teacher_login.html')


    return render(request, 'base/teacher_login.html')

def student_logout(request):
    logout(request)
    return redirect('student_login')


from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def pending_approvals(request):
    pending_students = Student.objects.filter(is_approved=False).order_by('created_at')
    return render(request, 'base/pending_approvals.html', {'pending_students': pending_students})

@staff_member_required
def approve_student(request, student_id):
    if request.method == 'POST':
        student = Student.objects.get(id=student_id)
        student.is_approved = True
        student.save()
    return redirect('pending_approvals')


from .form import StudentProfileForm
from .models import Student

@login_required
def update_student_profile(request):
    student = Student.objects.get(user__id = request.user.id)
    teacher = Teacher.objects.all()
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student, user= request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile',pk=student.user.id)  # Redirect to the student's profile page
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'base/update_profile.html', {'form': form , 'teacher':teacher})

def team(request):
    facultyProfiles = FacultyProfile.objects.all()
    publications = Publication.objects.all()
    context={
        'facultyProfiles':facultyProfiles,
        'publications':publications,
    }
    return render(request, 'base/team.html',context)
def team_member_details(request,id):
    facultyProfile = FacultyProfile.objects.get(user_id = id)
    
    research_interest = ResearchInterest.objects.get(user_id = id)
    
    context ={
        'facultyProfile':facultyProfile,
        'research_interests':research_interest.interest.split(",")
    }
    return render(request, 'base/team-teacher-details.html', context)


def all_member(request):
    students = Student.objects.filter(is_approved=True)
    context ={
        'students':students
    }
    return render(request, 'base/members.html',context)


def dataset(request):
    datasets = Dataset.objects.all().order_by('-id')
    context={
        'datasets':datasets
    }
    return render(request, 'base/dataset.html',context)
from cloudinary.utils import cloudinary_url
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

def download_dataset(request, dataset_id):
    if request.method == 'POST':
        dataset = get_object_or_404(Dataset, id=dataset_id)
        
        # Save download history
        DatasetDownloadHistory.objects.create(
            username=request.POST['username'],
            gmail=request.POST['gmail'],
            university=request.POST.get('university', ''),
            dataset=dataset,
            downloaded_at=timezone.now()
        )
        
        dataset.downloaded_number += 1
        dataset.save()

        # Safety check: Ensure dataset.file exists
        if not dataset.file:
            # Optionally add an error message
            return redirect('project_detail', pk=dataset.project.id)

       
        download_url = dataset.file.url
        if not download_url:
            # Optionally add an error message
            messages.error(request, 'Download link is not available.')
            return redirect('project_detail', pk=dataset.project.id) 

       
        return redirect(download_url)  # Redirect to the file URL for download

    # If not POST, fallback
    return redirect('project_detail', pk=dataset.project.id)

from django.core.paginator import Paginator
import pandas as pd
def dataset_download_history(request, dataset_id):
    # Get the dataset
    dataset = get_object_or_404(Dataset, id=dataset_id)
    
    # Get the download history for this dataset
    download_history = DatasetDownloadHistory.objects.filter(dataset=dataset).order_by('-downloaded_at')
    
    # Get projects that use this dataset
    # projects = Project.objects.filter(dataset_link=dataset)
    projects = dataset.project_set.all()
    
    print('project dataset: ', projects)
    
    csv_data = []
    headers = []

    if dataset.file:
        try:
            # Read only the first 100 rows from the CSV file using pandas
            df = pd.read_csv(dataset.file.url, nrows=100)
            headers = df.columns.tolist()
            csv_data = df.values.tolist()
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    
    context = {
        'dataset': dataset,
        'download_history': download_history,
        'projects': projects,
         'csv_data': csv_data,
        'headers': headers,
    }
    return render(request, 'base/dataset_download_history.html', context)

from datetime import timedelta

def latest_news(request):
    two_days_ago = timezone.now() - timedelta(days=2)
    
    # Fetch news articles created in the last 2 days, ordered by creation date (newest first)
    news_articles = News.objects.filter(
        is_published=True,
        # created_at__gte=two_days_ago  # Filter articles created after `two_days_ago`
    ).order_by('-created_at')
    
    context = {
        'news_articles': news_articles,
    }
    return render(request, 'base/news_threads.html', context)

from .form import NewsForm

def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('latest_news')
    else:
        form = NewsForm()
    return render(request, 'base/create_news.html', {'form': form})

from functools import wraps
from urllib.parse import quote
def approved_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Use quote() to handle special characters in URLs safely
            next_url = quote(request.get_full_path())
            return redirect(f"/login/?next={next_url}")

        user = request.user
        try:
            if hasattr(user, 'student_profile'):
                if not user.student_profile.is_approved:
                    messages.error(request, 'Your account is not approved yet.')
                    return redirect('home')
            elif hasattr(user, 'teacher'):
                pass  # Teachers are allowed by default
            else:
                messages.error(request, 'Unauthorized user type.')
                return redirect('home')
        except Exception as e:
            messages.error(request, 'Something went wrong. Please contact support.')
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return _wrapped_view

# create_dataset
from .form import DatasetForm
from django_ckeditor_5.widgets import CKEditor5Widget

# @login_required(login_url="/login/")
@approved_user_required
def create_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.uploaded_by = request.user
            dataset.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                DatasetImage.objects.create(
                    dataset=dataset,
                    image=image
                )
            
            messages.success(request, 'Dataset uploaded successfully!')
            return redirect('dataset')
    else:
        form = DatasetForm()
    
    return render(request, 'base/create_dataset.html', {'form': form})








from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import RegisterForm
from .tokens import account_activation_token

def teacher_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username=username, email=email, password=password)

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('base/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return render(request, 'base/email_sent.html')
    else:
        form = RegisterForm()
    return render(request, 'base/teacher-register.html', {'form': form})



from django.http import HttpResponse

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Teacher.objects.create(user=user)
        return HttpResponse('Thank you for your email confirmation. Now you can log in.')
    else:
        return HttpResponse('Activation link is invalid!')
