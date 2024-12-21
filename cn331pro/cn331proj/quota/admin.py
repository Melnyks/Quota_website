from django.contrib import admin
from quota.models import Subject, registerSubject, Student

# Register your models here.
admin.site.register(Subject)
admin.site.register(registerSubject)
admin.site.register(Student)