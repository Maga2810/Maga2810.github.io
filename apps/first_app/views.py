from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	return render(request, 'first_app/main.html')

def registration(request):
	errors = []
	if len(request.POST['alias']) < 2:
		errors.append("Name must be at least 2 characters")
	if len(request.POST['license']) < 2:
		errors.append("License number must be at least 2 characters")
	if len(request.POST['phone']) < 2:
		errors.append("Phone number must be at least 2 characters")
	if len(request.POST['password']) < 2:
		errors.append("Password must be at least 2 characters")
	if request.POST['password'] != request.POST['confirm_password']:
		errors.append("Password and password confirmation don't match. Try again!")
	if not EMAIL_REGEX.match(request.POST['email']):
		messages.error(request,"Invalid Email")
            
	if errors:
		for err in errors:
			messages.error(request, err)
			print(errors)
		return redirect('/')
	
	else:	
		try:
			User.objects.get(email=request.POST['email'])
			messages.error(request, "User with that email already exists.")
			return redirect('/')
		except User.DoesNotExist:
			hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(
									password = hashpw,\
									email = request.POST['email'],
									username = request.POST['email']
									)

			user.save()
			print user
			partner = Partner.objects.create(
									alias=request.POST['alias'],\
									license=request.POST['license'],\
									phone=request.POST['phone'],\
									user = user
									)
			partner.save()

			request.session['message'] = "You are registered"
			request.session['user_id'] = user.id
			return redirect('/dashboard')
			
def user_login(request):
	if not request.POST['email']:
		messages.error(request, "Please enter your email")
		return redirect('/')

	if not request.POST['password']:
		messages.error(request, "Please enter your password")
		return redirect('/')
	try:
		user = authenticate(username = request.POST['email'], password = request.POST['password'])
		if user: 
			login(request, user)
			request.session['user_id'] = user.id
			request.session['message'] = "You are logged in"
			if user.is_staff: 
				return redirect('/admin_account')
			return redirect('/dashboard')
		else:
			messages.error(request, 'Email or password are incorrect')
			return redirect('/')
	except User.DoesNotExist:
		messages.error(request, "Email doesn't exist.")
		return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

@login_required(login_url='/')
def dashboard(request):
	current_user = User.objects.get(id = request.session['user_id'])
	context = {
		'user': current_user,
		'my_orders': Order.objects.filter(partner=current_user.partner)
	}    
	return render(request, 'first_app/dashboard.html', context)

def make_order(request):
	current_user = User.objects.get(id = request.session['user_id'])
	order = Order.objects.create(title=request.POST['title'],\
								category=request.POST['category'],\
								quantity=request.POST['quantity'],\
								year=request.POST['year'],\
								brand=request.POST['brand'],\
								model=request.POST['model'],\
								serial=request.POST['serial'],\
								link=request.POST['link'],\
								location=request.POST['location'],\
								notes=request.POST['notes'],\
								partner=current_user.partner)
	htmly = get_template('first_app/order-create.html')
	d = Context({ 'title': order.title,\
	 							'category': order.category,\
	  						'quantity': order.quantity,\
	   						'year': order.year,\
	    					'brand': order.brand,\
	     					'model': order.model,\
	     					'serial': order.serial,\
	     					'link': order.link,\
	     					'location': order.location,\
	     					'notes': order.notes})

	subject, from_email, to = '{0} created new order'.format(current_user.partner.alias), 'oscarxportservice@gmail.com', 'razor_sb@mail.ru'
	# text_content = plaintext.render(d)
	html_content = htmly.render(d)
	msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	return redirect('/dashboard')

def delete_order(request, id):
	order = Order.objects.get(id=id)
	order.delete()
	return redirect('/dashboard')

@login_required(login_url='/')
def admin_account(request):
	context = {
		"all_orders": Order.objects.all().order_by('-created_at')
	}
	return render(request, 'first_app/admin.html', context)

def delete_order_by_superuser(request, id):
	order = Order.objects.get(id=id)
	order.delete()
	return redirect('/admin_account')

def partner(request, id):
	par = User.objects.get(id=id)
	context = {
		'par': User.objects.get(id=id),
		'par_orders': Order.objects.filter(partner=par.partner).order_by('-created_at')
	}
	return render(request, 'first_app/partner.html', context)