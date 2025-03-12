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

            # Create project with all fields
            project = Project.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                objectives=request.POST.get('objectives', ''),
                hypothesis=request.POST.get('hypothesis', ''),
                publication_link=request.POST.get('publication_link', ''),
                dataset_link=request.POST.get('dataset_link', ''),
                github_link=request.POST.get('github_link', ''),
                methodology=request.POST.get('methodology', ''),
                tools_used=request.POST.get('tools_used', ''),
                created_at=request.POST['start_date'],
                advisor=Teacher.objects.get(id=request.POST['advisor']),
                project_picture=request.FILES.get('project_picture',''),
                project_file=request.FILES.get('project_file',''),
            )

            # Add team members
            print('assigned_student',request.POST.getlist('students'))
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