from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from models import *
from django.contrib import messages

def index(request):
	context = {
		"users" : User.objects.all()
	}
	return render(request, "pythonbelt2_app/index.html", context)

def register(request):
	errors = User.objects.regvalidator(request.POST, "create")
	if len(errors): 
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect("/") 
	else:
		newuser = User.objects.create(name=request.POST["name"], username=request.POST['username'], password=request.POST["password"])
		newuser.save()
		request.session["user_id"] = newuser.id
		messages.success(request, "Successfully registered!")
		return redirect("/travels")


def log(request):
	errors = User.objects.logvalidator(request.POST, "log")
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error, extra_tags="log")
		return redirect("/")
	else:
		request.session["user_id"] = User.objects.get(username=request.POST["username"]).id
		request.session["status"] = "logged in"
		return redirect("/travels")

def logout(request):

	del request.session['user_id']
	return redirect('/')

def travels(request):
	if 'user_id' not in request.session:
		return redirect('/')	
        user = User.objects.get(id=request.session["user_id"])
        othertrips = Trip.objects.exclude(user = user)
        mytrips = Trip.objects.filter(user = user)

        context = {
            "user":user,
            "othertrips": othertrips,
            "mytrips": mytrips,
        }

        return render(request, "pythonbelt2_app/dashboard.html", context)

def add(request):
	return render(request, "pythonbelt2_app/addtrip.html")

def addtrip(request):
	errors = Trip.objects.tripvalidator(request.POST, 'trip')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect("/add")
	newtrip=  Trip.objects.create(travelto=request.POST['to_x'], travelfrom=request.POST['from_x'], destination=request.POST['destination'], description= request.POST['desc'],user= User.objects.get(id=request.session['user_id']), )
	return redirect('/travels')

def show(request, id):
	user = User.objects.get(id=request.session["user_id"])
	context = {
		"user" : User.objects.get(id=request.session["user_id"]),
		'content': Trip.objects.filter(id=int(id) ),
		'count': Trip.objects.count(),
		'join': Trip.objects.filter(jointrip= user),
	}
	return render(request, "pythonbelt2_app/show.html", context)

def join(request, id):
	user = User.objects.get(id = request.session['user_id'])
	trip = Trip.objects.get(id = id)

	trip.jointrip.add(user)

	trip.save()
	return redirect('/travels')
