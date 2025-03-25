from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    about = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=11)
    profile_picture = models.ImageField(upload_to="student-images/", blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    skills = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of skills")
    
    cv = models.FileField(upload_to='students-cv', null=True, blank=True)
    google_scholar_profile = models.URLField(blank=True, null=True)
    linkin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)

    
    def imageURL(self):
        url = ''
        try:
            url = self.profile_picture.url
        except:
            url =''
        return url
    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    profile_picture = models.ImageField(upload_to="teacher-profile/", blank=True)
    about = models.TextField(null=True)
    
    def imageURL(self):
        url = ''
        try:
            url = self.profile_picture.url
        except:
            url =''
        return url
    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title



class Dataset(models.Model):
    title = models.TextField(max_length=200)
    dataset_link  = models.URLField(blank=True)
    file = models.FileField(upload_to='dataset-file')
    is_private = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="uploaded_dataset")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloaded_number = models.PositiveIntegerField(default=0)
    
class DatasetDownloadHistory(models.Model):
    username = models.TextField(max_length=100)
    gmail = models.EmailField(max_length=100)
    university = models.TextField(max_length=20, blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="dataset_download",blank=True, null=True)
    downloaded_at = models.DateTimeField(default=timezone.now)
    
    
class project_studnet(models.Model):
    LEADER = 'leader'
    DEVELOPER = 'developer'
    TESTER = 'tester'

    ROLE_CHOICES = [
        (LEADER, 'Leader'),
        (DEVELOPER, 'Developer'),
        (TESTER, 'Tester'),
    ]
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True,null=True, related_name='students_project')
    def __str__(self):
        return self.user.user.username

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    students = models.ManyToManyField(Student, through=project_studnet, related_name="assigned_students")
    advisor = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='project_advisor')
    project_picture = models.ImageField(upload_to="project-images/", blank=True)
    objectives = models.TextField(blank=True)
    hypothesis = models.TextField(blank=True)
    publication_link = models.URLField(blank=True)
    dataset_link = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    github_link = models.URLField(blank=True)
    methodology = models.CharField(max_length=200, blank=True)
    tools_used = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    project_file = models.FileField(upload_to='project-file/', null=True, blank=True)
    
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    
    def imageURL(self):
        url = ''
        try:
            url = self.project_picture.url
        except:
            url =''
        return url
    def __str__(self):
        return self.title
    
    
    
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="news_articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="news-images/", blank=True, null=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def imageURL(self):
        if self.image:
            return self.image.url
        return ""
    
    