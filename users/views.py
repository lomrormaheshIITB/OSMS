from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from .models import CustomUser, CustomUserProfile, Rank, Department
from .forms import CustomUserCreationForm, CustomUserProfileForm , LoginForm ,CustomUserChangePasswordForm, ManageUsersForm


def LoginView(request):
	form = LoginForm()
	if (request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		department = request.POST['department']
		user_entry = CustomUser.objects.filter(username=username)
		if user_entry.count() != 0:
			user_entry = user_entry[0]
			user_department = user_entry.user_profile.department.id
			if (str(user_department) == str(department) and user_entry.profile.user_active == True):
				user = authenticate(username=username, password=password)
				if user is not None:
					login(request, user)
					# Redirect to home
					return redirect('data:home')
				else:
					# Return an 'invalid login' error message.
					messages.error(request, "Invalid login credentials!")
			else:
				messages.error(request, "Invalid login credentials!")
		else:
			messages.error(request, "No user found!")

	template = 'users/login.html'	
	context = {
		'title': 'OSMS | User Login',
		'form': form,		
	}
	return render(request, template, context)


@login_required
def LogoutView(request):
	logout(request)
	return redirect('users:login') 


@login_required
def CustomUserSignupView(request):
	form = CustomUserCreationForm()
	if (request.method == 'POST'):
		form = CustomUserCreationForm(request.POST)
		if (form.is_valid()):
			print(mahesh)			
			access_level = form.cleaned_data['access_level']
			print(access_level)
			department = form.cleaned_data['department']
					
			username = form.cleaned_data['username']
			customuser_entry = CustomUser.objects.filter(username=username)			
			customuserprofile_entry = CustomUserProfile.objects.filter(personal_number=username)
			if access_level == '1':
				if (customuser_entry.count() != 0 ):
					customuser_entry = customuser_entry[0]					
					messages.error(request, "Login Credentials corresponding to username " + username + " already exists!")
					return redirect('users:custom_user_signup')
				else: 
					if (customuserprofile_entry.count() != 0 ):
						customuserprofile_entry = customuserprofile_entry[0]
						
						print(department_entry.name)					
						# Modify the CustomUser Model					
						# Create a new  entry for username entered
						CustomUser.objects.create(username=username,access_level=access_level, department=department,user_profile=customuserprofile_entry)
						messages.success(request, "New Superuser in "+ department + " department with username " + username + " created!")
						return redirect('users:custom_user_signup')

			elif (access_level == "2"):		
				if (customuser_entry.count() != 0 ):
					messages.error(request, "Login Credentials corresponding to this username already exists!")
					return redirect('users:custom_user_signup')
				else: 
					if (customuserprofile_entry.count() != 0 ):
						customuserprofile_entry = customuserprofile_entry[0]	
										
						# Modify the CustomUser Model					
						# Create a new  entry for username entered
						CustomUser.objects.create(username=personal_number,access_level=access_level, department=department,user_profile=customuserprofile_entry)
						messages.success(request, "New Storekeeper in "+ department + " department with username " + username + " created!")
						return redirect('users:custom_user_signup')
			else:
				if (customuser_entry.count() != 0 ):
					customuser_entry = customuser_entry[0]
					messages.error(request, "Login Credentials corresponding to this username already exists!")
					return redirect('users:custom_user_signup')
				else: 
					if (customuserprofile_entry.count() != 0 ):
						customuserprofile_entry = customuserprofile_entry[0]
						messages.error(request, "Profile with the personal number " + personal_number + " cannot have Login Credentials as access level chosen is not appropriate")
						return redirect('users:custom_user_signup')				
		else:
			messages.error(request, "Form validation failed!")
	
	template = 'users/loginuser_creation.html'
	context = {
		'title': 'O-SMS | Login User Signup-Form',
		'form': form,
		'user': request.user,
	}
	return render(request, template, context)


def CustomUserProfileCreationView(request):
	form = CustomUserProfileForm()
	if (request.method == 'POST'):
		form = CustomUserProfileForm(request.POST)
		if (form.is_valid()):
			personal_number = form.cleaned_data['personal_number'].upper()
			customuserprofile_entry = CustomUserProfile.objects.filter(personal_number=personal_number)
			if (customuserprofile_entry.count() != 0 ):
				customuserprofile_entry = customuserprofile_entry[0]
				messages.error(request, "Profile with this personal number already exists!")
				return redirect('users:custom_user_profile')
			else: 
				form.save()
				messages.success(request, "New user profile having personal number " + personal_number + " created!")
				return redirect('users:custom_user_profile')
		else:
			messages.error(request, "Form validation failed!")
	
	template = 'users/userprofile.html'
	context = {
		'title': 'O-SMS | Profile Creation Form',
		'form': form,
		'user': request.user,
	}
	return render(request, template, context)	

@login_required
def EditProfileView(request):
	# Fetch the profile of the currently logged in user
	username = request.user.username
	profile = CustomUserProfile.objects.filter(personal_number=username)	
	if (profile.count() != 0):
		profile = profile[0]
		profile.ship_joining_date = datetime.strftime(profile.ship_joining_date, '%d %B %Y - %H:%M')
		if (request.method == 'POST'):
			form_id = request.POST.get('form_id')

			# Process based on the form_id received
			if (form_id == '1'):
				# Change profile details
				form1 = CustomUserProfileForm(request.POST, instance=profile)	
				if (form1.is_valid()):
					personal_number = form1.cleaned_data['personal_number']
					form1.save()
					# Change the username if personal number changes
					if (personal_number != username):
						user = CustomUser.objects.get(username=username)
						user.username = personal_number
						user.save()
					messages.success(request, "User profile updated!")
				else:
					messages.error(request, "Form validation failed!")
				
			elif (form_id == '2'):
				# Change password
				form2 = CustomUserChangePasswordForm(request.POST)
				if (form2.is_valid()):
					old_password = form2.cleaned_data['old_password']
					password1 = form2.cleaned_data['password1']
					password2 = form2.cleaned_data['password2']
					user = authenticate(username=username, password=old_password)
					if (user and password1 != '' and password1 == password2):
						form2.save(user)
						messages.success(request, "Password changed successfully!")
						return redirect('users:logout')
					else:
						messages.error(request, "Invalid credentials!")
				else:
					messages.error(request, "Form validation failed!")
			return redirect('users:editprofile')

		# Render the spare edit page
		template = 'users/edit_profile.html'
		context = {
			'title': 'OSMS | My Profile',
			'user': request.user,
			'form1': CustomUserProfileForm(instance=profile),
			'form2': CustomUserChangePasswordForm
		}
		return render(request, template, context)
	else:
		messages.info(request, 'No profile  details found!')
		return redirect('data:home')


@login_required
def LockScreenView(request):
	context = {
		'title': 'OSMS | Lock Screen',
	}
	template = 'users/lock-screen.html'
	return render(request, template, context)
	
@login_required
def ManageUserView(request):
	form = ManageUsersForm()
	if (request.method == 'POST'):
		form = ManageUsersForm(request.POST)
		if (form.is_valid()):
			password = form.cleaned_data['password']
			username = request.user.username
			user = authenticate(username=username, password=password)
			if (user is not None):
				form_id = request.POST.get('form_id')
				user_id = form.cleaned_data['username']
				userprofile = CustomUserProfile.objects.get(id=user_id)	
				if (form_id == '1'):
					userprofile.access_level = form.cleaned_data['access_level']
					userprofile.save()
					messages.success(request, 'User access level changed!')
				elif (form_id == '2'):
					userprofile.user_active = False
					userprofile.save()
					user = CustomUser.objects.filter(username=userprofile.personal_number)
					if (user.count() != 0):
						user[0].delete()
					messages.success(request, 'User deleted!')
			else:
				messages.error(request, 'Invalid credentials!')
		else:
			messages.error(request, "Form validation failed!")
	
	template = 'users/manage_users.html'
	context = {
		'title': 'O-SMS | Manage Users',
		'form': form,
		'user': request.user,
	}
	return render(request, template, context)	