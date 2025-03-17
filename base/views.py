from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='/login/')

def landing_page(request):
    return render(request, 'base/landing_page.html')

def explore(request):
    projects = Project.objects.all().order_by('-id')
    context ={
        'projects':projects
    }
    return render(request, 'base/explore.html',context)
    
@login_required(login_url='/login/')
def dashboard(request):
    projects = Project.objects.all().order_by('-id')
    
    # User.objects.create(username = "nami" , password="1234")
    # User.objects.create(username = "zoro" , password="1234")
    # User.objects.create(username = "sanji" , password="1234")
    # User.objects.create(username = "robin" , password="1234")
    
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
                created_at=request.POST['start_date'],
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
        print(username)
        print(password)
        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            student =None
            try:
                student =  Student.objects.get(user=user)
            except:
                student = None 
            if student:
                login(request, user)
                return redirect('home')  # Redirect to dashboard or home page
            else:
                messages.error(request, 'Unauthenticated Student!')
                return render(request, 'base/login.html')
        else:
            print('Invalid username or password!')
            messages.error(request, 'Invalid username or password!')

    return render(request, 'base/login.html')

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
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('view_profile',pk=student.user.id)  # Redirect to the student's profile page
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'base/update_profile.html', {'form': form , 'teacher':teacher})

def team(request):
    return render(request, 'base/team.html')
def all_member(request):
    students = Student.objects.all()
    context ={
        'students':students
    }
    return render(request, 'base/members.html',context)


def dataset(request):
    datasets = Dataset.objects.all()
    context={
        'datasets':datasets
    }
    return render(request, 'base/dataset.html',context)

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
        dataset.downloaded_number +=1 
        dataset.save()
        # Redirect to the dataset file download
        return redirect(dataset.file.url)
    
    return redirect('project_detail', pk=dataset.project.id)
from django.core.paginator import Paginator
import pandas as pd
def dataset_download_history(request, dataset_id):
    # Get the dataset
    dataset = get_object_or_404(Dataset, id=dataset_id)
    
    # Get the download history for this dataset
    download_history = DatasetDownloadHistory.objects.filter(dataset=dataset).order_by('-downloaded_at')
    
    # Get projects that use this dataset
    projects = Project.objects.filter(dataset_link=dataset)
    
    csv_data = []
    headers = []

    if dataset.file:
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(dataset.file.path)
            headers = df.columns.tolist()

            # Paginate the data
            paginator = Paginator(df.values.tolist(), 100)  # 20 rows per page
            page = request.GET.get('page', 1)
            csv_data = paginator.get_page(page)
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
        created_at__gte=two_days_ago  # Filter articles created after `two_days_ago`
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

# create_dataset
from .form import DatasetForm
@login_required(login_url="/login/")
def create_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.uploaded_by = request.user  # Assuming the user is a Teacher
            dataset.save()
            return redirect('dataset')  # Redirect to a success page
    else:
        form = DatasetForm()
    
    return render(request, 'base/create_dataset.html', {'form': form})