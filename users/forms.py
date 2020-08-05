from datetime import datetime
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUserProfile, CustomUser , Rank, Department

class LoginForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ('username','password')

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		department_choices = [(e.id, e.name) for e in Department.objects.all().order_by('name')]
		self.fields['department'] = forms.ChoiceField(
			label = 'Department',
			choices=department_choices,
			widget = forms.Select(attrs = {
				'class': 'form-control edited'})
		)

	username = forms.CharField(label = 'Username', widget = forms.TextInput(attrs = {
			'class': "form-control placeholder-no-fix"})
		)

	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs = {
			'class': "form-control placeholder-no-fix"})
		)


class CustomUserProfileForm(forms.ModelForm):
	class Meta:
		model = CustomUserProfile
		fields = ('firstname', 'lastname', 'personal_number', 'rank', 'ship_joining_date', 'section', 'remarks')

	def clean(self, *args, **kwargs):
		cleaned_data = super(CustomUserProfileForm, self).clean(*args, **kwargs)
		for key, val in zip(cleaned_data.keys(), cleaned_data.values()):
			try:
				cleaned_data[key] = val.upper()
			except AttributeError as e:
				continue
		cleaned_data['rank'] = Rank.objects.get(id=cleaned_data['rank'])
		cleaned_data['ship_joining_date'] = datetime.strftime(cleaned_data['ship_joining_date'], '%Y-%m-%d %H:%M:%M%z')
		return cleaned_data

	def __init__(self, *args, **kwargs):
		super(CustomUserProfileForm, self).__init__(*args, **kwargs)
		self.fields['rank'] = forms.ChoiceField(
			label = 'Rank',
			choices=[(e.id, e.name) for e in Rank.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control edited',
				})
			)

	firstname = forms.CharField(
		label = 'Firstname',
	 	widget = forms.TextInput(attrs = {
			'class': "form-control placeholder-no-fix",
			})
		)

	lastname = forms.CharField(
		label = 'Lastname', 
		widget = forms.TextInput(attrs = {
			'class': "form-control placeholder-no-fix",
			})
		)	

	personal_number = forms.CharField(label = 'Personal Number', widget = forms.TextInput(attrs = {
			'class': "form-control placeholder-no-fix",
			})
		)
	section = forms.CharField(label = 'Section', widget = forms.TextInput(attrs = {
			'class': "form-control placeholder-no-fix",
			})
		)
		
	ship_joining_date = forms.DateTimeField(
		label = 'Ship Joining Date',
		widget = forms.DateTimeInput(attrs = {
			'class': "form-control form-group"}),
		input_formats=[
			'%d %B %Y - %H:%M',
		]
	)

	remarks = forms.CharField(
		label = 'Remarks',
		required = False,
		widget = forms.Textarea(attrs = {
			'class': 'form-control form-group upper',			
			'rows': '4',
			})
		)


#To create usernames in CustomUser Model
class CustomUserCreationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		username_choices = [(e.personal_number, e.personal_number) for e in CustomUserProfile.objects.all().order_by('personal_number')]
		username_choices.insert(0, (u"", u"Choose Username"))
		self.fields['username'] = forms.ChoiceField(
			label = 'Username',
			choices=username_choices,
			widget = forms.Select(attrs = {
				'class': 'form-control edited',
				})
			)

	password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs = {
			'class': "form-control placeholder-no-fix",
			
			}))
			
	password2 = forms.CharField(label='Re-Confirm Password ', widget=forms.PasswordInput(attrs = {
			'class': "form-control placeholder-no-fix",
			}))

	class Meta:
		model = CustomUser
		fields = ('username','password')


	def check_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('Passwords do not match.')
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

	def clean(self, *args, **kwargs):
		cleaned_data = super(CustomUserCreationForm, self).clean(*args, **kwargs)
		cleaned_data['username'] = cleaned_data['username'].upper()
		return cleaned_data

class ManageUsersForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(ManageUsersForm, self).__init__(*args, **kwargs)
		username_choices = [(e.id, f"{e.rank.name} {e.firstname} {e.lastname}") for e in CustomUserProfile.objects.filter(user_active=True).order_by('personal_number')]
		self.fields['username'] = forms.ChoiceField(
			label = 'Username',
			choices=username_choices,
			widget = forms.Select(attrs = {
				'class': 'form-control edited',
				})
			)

		self.fields['access_level'] = forms.ChoiceField(
			label = 'Access Level',
			choices = CustomUserProfile.access_level_choices,
			widget = forms.Select(attrs = {
				'class': 'form-control',
				})
			)

	password = forms.CharField(
		label='Login Password',
		widget=forms.PasswordInput(attrs = {
			'class': "form-control placeholder-no-fix",
		})
	)


class CustomUserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()	
	class Meta:
		model = CustomUser	
		fields = ('username', 'password', 'is_active', 'is_admin',)

	def clean_password(self):
		return self.initial['password']


#To change password in edit profile.html
class CustomUserChangePasswordForm(forms.Form):
	def save(self, user, commit=True):
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

	old_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(attrs = {
			'class': "form-control placeholder-no-fix",
			
			}))	
	password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs = {
			'class': "form-control placeholder-no-fix",
			
			}))
	password2 = forms.CharField(label='Re-type New Password ', widget=forms.PasswordInput(attrs = {
			'class': "form-control placeholder-no-fix",
			}))

