from django.db import models


class University(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    website = models.URLField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    ranking = models.IntegerField(null=True,blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(null=True,blank = True)
    slug = models.SlugField()
    featured = models.BooleanField()

    def __str__(self):
        return self.title

class Program(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    requirements = models.TextField()
    university = models.ForeignKey(University,on_delete=models.CASCADE,related_name="uni")
    fall_deadline = models.DateField(null=True,blank = True)
    winter_deadline = models.DateField(null=True,blank = True)
    spring_deadline = models.DateField(null=True,blank = True)
    summer_deadline = models.DateField(null=True,blank = True)
    link = models.URLField()
    course = models.BooleanField()
    project = models.BooleanField()
    thesis = models.BooleanField()
    fee = models.IntegerField()
    lang = models.CharField(max_length=100,null=True,blank = True)
    period = models.CharField(max_length=100,null=True,blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(null=True,blank = True)
    slug = models.SlugField()
    featured = models.BooleanField()
    class Program_lvl(models.IntegerChoices):
        Bachelor =1, 'Bachelor'
        Master =2, 'Master'
        Doctoral =3, 'Doctoral'
    lvl = models.PositiveSmallIntegerField(choices=Program_lvl.choices)
    def __str__(self):
        return self.title
    
class Professor(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=150)
    major = models.CharField(max_length=150,null=True,blank = True)
    interest_field = models.CharField(max_length=200)
    website = models.URLField(null=True,blank = True)
    faculty_page = models.URLField(null=True,blank = True)
    email = models.EmailField()
    phone = models.CharField(max_length=30,null=True,blank = True)
    description = models.TextField(null=True,blank = True)
    google_scholar = models.URLField(null=True,blank = True)
    research_gate = models.URLField(null=True,blank = True)
    linkedin = models.URLField(null=True,blank = True)
    twitter = models.URLField(null=True,blank = True)
    github = models.URLField(null=True,blank = True)
    facebook = models.URLField(null=True,blank = True)
    rate = models.URLField(null=True,blank = True)
    university = models.ForeignKey(University,on_delete=models.CASCADE,related_name="uniprof")
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(null=True,blank = True)
    slug = models.SlugField()
    featured = models.BooleanField()

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    thumbnail = models.ImageField()
    university = models.ManyToManyField(University)
    slug = models.SlugField()
    featured = models.BooleanField()

    def __str__(self):
        return self.title
