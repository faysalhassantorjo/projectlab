from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary.models import CloudinaryField

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    about = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=11)
    # profile_picture = models.ImageField(upload_to="student-images/", blank=True)
    profile_picture = CloudinaryField("student-profile", folder="student_profile", blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    skills = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of skills")
    
    cv =CloudinaryField("students-cv", folder="student_cv", blank=True, null=True, resource_type='raw',)
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
    profile_picture = CloudinaryField("teacher-profile", folder ="teacher_profile", blank=True, null=True)
    
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
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Description', config_name='default', null=True, blank=True)  #     dataset_link  = models.URLField(blank=True)
    dataset_link = models.URLField(null=True, blank=True)
    file = CloudinaryField("dataset-file", folder="datasets", blank=True, null=True,resource_type='raw')
    is_private = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="uploaded_dataset")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloaded_number = models.PositiveIntegerField(default=0)

class DatasetImage(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='preview_images')
    image = CloudinaryField("dataset-preview",folder="dataset-preview-image", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    
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
    project_picture = CloudinaryField("project-picture", folder="project-banner", blank=True, null=True)
    objectives = models.TextField(blank=True)
    hypothesis = models.TextField(blank=True)
    publication_link = models.URLField(blank=True)
    dataset_link = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    github_link = models.URLField(blank=True)
    methodology = models.CharField(max_length=200, blank=True)
    tools_used = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    project_file = CloudinaryField("project-file", folder="project-file",blank=True, null=True)
    
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
    PRIORITY_CHOICES = (
    ('urgent', 'Urgent'),
    ('important', 'Important'),
    ('general', 'General'),)

    title = models.CharField(max_length=200)
    content = CKEditor5Field(config_name='default', null=True, blank=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="news_articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = CloudinaryField("news-image", folder="news-banner", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    priority = models.CharField(choices=PRIORITY_CHOICES, null=True, blank=True, max_length=20)

    def __str__(self):
        return self.title

    def imageURL(self):
        if self.image:
            return self.image.url
        return ""
    
class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    currently_studying = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['-end_year']
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    profile_image = CloudinaryField("faculty-profile",folder="faculty-profile", blank=True, null=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100)
    office_hours = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    biography = models.TextField()
    
    # Social links
    linkedin_url = models.URLField(blank=True, null=True)
    google_scholar_url = models.URLField(blank=True, null=True)
    researchgate_url = models.URLField(blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)
    
    #education
    educations = models.ManyToManyField(Education,related_name='educations')
    
    
    class Meta:
        verbose_name = "Faculty Profile"
        verbose_name_plural = "Faculty Profiles"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"



class ResearchInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='research_interests')
    interest = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Research Interest"
        verbose_name_plural = "Research Interests"
    
    def __str__(self):
        return self.interest

class Publication(models.Model):
    PUBLICATION_TYPES = (
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book'),
        ('chapter', 'Book Chapter'),
        ('thesis', 'Thesis'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=500)
    publication_type = models.CharField(max_length=20, choices=PUBLICATION_TYPES)
    journal_or_conference = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    doi = models.CharField(max_length=100, blank=True, null=True)
    pdf_file = CloudinaryField("publications-pdf",folder="publication-pdf", blank=True, null=True)
    code_url = models.URLField(blank=True, null=True)
    is_selected = models.BooleanField(default=False, help_text="Mark as selected publication to display on profile")
    
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-year']
    
    def __str__(self):
        return self.title