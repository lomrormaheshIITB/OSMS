from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, CustomUserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
	form = CustomUserChangeForm
	add_form = CustomUserCreationForm

	list_display = ('username', 'is_admin',)
	list_filter = ('is_admin',)
	
	fieldssets = (
		(None, {
			'fields': ('username', 'password',),
			}),
		('Personal info', {
			'fields': (),
			}),
		('Permissions', {
			'fields': ('is_admin',)
			}),
		)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username','password1', 'password2',)
			}),
		)

	search_fields = ('username',)
	ordering = ('username',)
	filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUserProfile)
