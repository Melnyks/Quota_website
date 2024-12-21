from django.shortcuts import render,redirect
from quota.models import Subject,Student,registerSubject
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import transaction

# Create your views here.

def index(request):
    return render(request,'index.html')

def subject_list(request):
    all_subject = Subject.objects.all()
    return render(request, 'subject_list.html', {
        "all_subject": all_subject,
    })

def my_quota(request):
    mySubject = registerSubject.objects.filter(username=request.user.username)
    return render(request, 'my_quota.html', {
        "mySubject": mySubject,
    })

@transaction.atomic
def add_subject(request, id):
    subject = get_object_or_404(Subject, subjectCode=id)

    if subject.seatAvailable <= 0:
        messages.error(request, "No seats available for this subject.")
        return redirect('my_quota')  

    if registerSubject.objects.filter(username=request.user.username, subjectCode=id).exists():
        messages.error(request, "This subject has already been added to your quota.")
        return redirect('my_quota')  

    addSubject = registerSubject.objects.create(
        username=request.user.username,
        subjectCode=subject.subjectCode,
        subjectName=subject.subjectName,
        semester=subject.semester,
        year=subject.year,
    )
    subject.seatAvailable -= 1

    if subject.seatAvailable == 0:
        subject.status = 'Close'

    subject.save()
    messages.success(request, f"Subject {subject.subjectCode} has been added to your quota.")
    return redirect('my_quota')

@transaction.atomic
def del_subject(request, id):
    user_subject = get_object_or_404(registerSubject, username=request.user.username, subjectCode=id)
    subject = get_object_or_404(Subject, subjectCode=id)
    user_subject.delete()
    subject.seatAvailable += 1

    if subject.seatAvailable > 0:
        subject.status = 'Open'

    subject.save()  
    messages.success(request, f"Subject {subject.subjectCode} has been removed from your quota.")
    return redirect('my_quota')
