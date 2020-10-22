from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	return render(request, "index.html")

def register(request):
	if request.method == "POST":
		errors = User.objects.reg_validator(request.POST)
		if len(errors) > 0:
			for key,value in errors.items():
				messages.error(request, value)
			return redirect('/')

		user = User.objects.reg_validator(request.POST)
		if len(user) > 0:        # if there is something
			messages.error(request, "Email is already in use.")
			return redirect('/')

		pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

		User.objects.create(
			first_name=request.POST['first_name'],
			last_name=request.POST['last_name'],
			email=request.POST['email'],
			password=pw
		)
	
		request.session['user_id'] = User.objects.last().id 
		return redirect('/dashboard')

	else:
		return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.login_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request,value)
			return redirect('/')

		user = User.objects.filter(email=request.POST['login_email'])
		if len(user) == 0:
			messages.error(request, "Invalid Email/Password.")
			return redirect('/')
		if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
			messages.error(request,"Invalid Email/Password.")
			return redirect('/')

		request.session['user_id'] = user[0].id
		return redirect('/dashboard')
	else:
		return redirect('/')


def dashboard(request):
	if 'user_id' not in request.session:
		
		return redirect('/')
	else:
		context = {
			'user': User.objects.get(id=request.session['user_id'])
		}
		return render(request,'dashboard.html', context)


def logout(request):
	pass