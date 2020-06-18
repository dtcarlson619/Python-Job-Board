from django.shortcuts import render, redirect
from .models import UserManager, User, JobManager, Job
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def dashboard(request):
    context = {
        "all_jobs": Job.objects.all(),
        "user": User.objects.get(id=request.session['userid']),
    }
    return render(request, "dashboard.html", context)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if request.method == 'POST':
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
            request.session["userid"] = user.id
            return redirect("/dashboard")

def login(request):
    if request.method == "POST":
        errors = User.objects.loginCheck(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            login = User.objects.get(email=request.POST["email"])
            context = {
                "user": login
            }
            # CREATE a key in the session dictionary called "userid" with
            # a value of the ID of the user from the database
            request.session["userid"] = login.id
            return redirect("/dashboard")

def logout(request):
    try:
        del request.session["userid"]
        return redirect("/")
    except:
        return redirect("/")

def newJobPage(request):
    context = {
        "user": User.objects.get(id=request.session['userid']),
    }
    return render(request, "jobs_new.html", context)

def createJob(request):
    errors = Job.objects.basic_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/jobs/new")
        else:
            title = request.POST["title"]
            userid = User.objects.get(id=request.session['userid'])
            description = request.POST["description"]
            location = request.POST["location"]
            newJob = Job.objects.create(title=title, user=userid, description=description, location=location)
            return redirect("/dashboard")

def viewJobPage(request, job_id):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "job": Job.objects.get(id=job_id),
    }
    return render(request, "jobs_view.html", context)

def editJobPage(request, job_id):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "job": Job.objects.get(id=job_id),
    }
    return render(request, "jobs_edit.html", context)

def updateJob(request, job_id):
    errors = Job.objects.basic_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/jobs/{job_id}/edit")
        else:
            job = Job.objects.get(id=job_id)
            job.title = request.POST["title"]
            job.description = request.POST["description"]
            job.location = request.POST["location"]
            job.save()
            return redirect("/dashboard")

def removeJob(request, job_id):
    thisJob = Job.objects.get(id=job_id)
    thisJob.delete()
    return redirect("/dashboard")