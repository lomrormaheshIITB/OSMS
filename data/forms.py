from django import forms
from users.models import CustomUser, CustomUserProfile, Rank, Department 
from .models import Spares, SpareClass, EquipmentClass, Denomination, Authority, Issue, Return, PostSurvey, PostDemand, PostReceive

class SpareClassForm(forms.ModelForm):
	class Meta:
		model = SpareClass
		fields = '__all__'

	name = forms.CharField(
		label = 'Spare',
		widget = forms.TextInput(attrs = {
			'class': 'form-control',
			})
		)

class EquipmentClassForm(forms.ModelForm):
	class Meta:
		model = EquipmentClass
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(EquipmentClassForm, self).__init__(*args, **kwargs)
		self.fields['spare_class'] = forms.ChoiceField(
			label = 'Class of Spares',
			choices=[(e.name, e.name) for e in SpareClass.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control edited',
				})
			)

	name = forms.CharField(
		label = 'Class of Equipment /Fittings/ Valves/ PLL',
		widget = forms.TextInput(attrs = {
			'class': 'form-control',
			})
		)

class DenominationForm(forms.ModelForm):
	class Meta:
		model = Denomination
		fields = '__all__'

	name = forms.CharField(
		label = 'Denomination',
		widget = forms.TextInput(attrs = {
			'class': 'form-control',
			})
		)

class AuthorityForm(forms.ModelForm):
	class Meta:
		model = Authority
		fields = '__all__'

	name = forms.CharField(
		label = 'Authority',
		widget = forms.TextInput(attrs = {
			'class': 'form-control',
			})
		)

class RankForm(forms.ModelForm):
	class Meta:
		model = Rank
		fields = '__all__'

	name = forms.CharField(
		label = 'Rank',
		widget = forms.TextInput(attrs = {
			'class': 'form-control',
			})
		)


class SearchForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
	
		self.fields['spare_class'] = forms.ChoiceField(
			label = 'Class of Spares',
			choices =  [('ALL', 'ALL')] + [(e.name, e.name) for e in SpareClass.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control edited select2',
				})
			)

		self.fields['equipment_class'] = forms.ChoiceField(
			label = 'Class of Equipment/ Valve/ Fitting',
			choices = [('ALL', 'ALL')] + [(e.name, e.name) for e in EquipmentClass.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control edited select2',
				})
			)

	pattern_number = forms.CharField(
		label = 'Pattern Number',
		required = False,
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	description = forms.CharField(
		label = 'Spare Description',
		required = False,
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)



class SpareForm(forms.ModelForm):
	class Meta:
		model = Spares
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(SpareForm, self).__init__(*args, **kwargs)
	
		self.fields['spare_class'] = forms.ChoiceField(
			label = 'Class of Spares',
			choices = [(e.name, e.name) for e in SpareClass.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control edited',
				})
			)

		self.fields['equipment_class'] = forms.ChoiceField(
			label = 'Name of Equipment/ Fitting/ Valves',
			choices = [(e.name, e.name) for e in EquipmentClass.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control edited',
				})
			)

		self.fields['denomination'] = forms.ChoiceField(
			label = 'Denomination',
			choices = [(e.name, e.name) for e in Denomination.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control',
				})
			)

		self.fields['category'] = forms.ChoiceField(
			label = 'Category',
			choices = Spares.category_choices,
			widget = forms.Select(attrs = {
				'class': 'form-control',
				})
			)

		self.fields['critical'] = forms.ChoiceField(
			label = 'Critical',
			choices = [(True, 'YES'), (False, 'NO')],
			widget = forms.Select(attrs = {
				'class': 'form-control',
				})
			)

		self.fields['authority'] = forms.ChoiceField(
			label = 'Authority',
			choices = [(e.name, e.name) for e in Authority.objects.all().order_by('name')],
			widget = forms.Select(attrs = {
				'class': 'form-control',
				})
			)

	pattern_number = forms.CharField(
		label = 'Pattern Number',
		required = False,
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	compartment = forms.CharField(
		label = 'Onboard Location',
		required = False,
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	location = forms.CharField(
		label = 'Box No.',
		required = False,
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	quantity_authorised = forms.DecimalField(
		min_value = 0,
		label = 'Quantity Authorised',
		required = False,
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': '0',
			})
		)

	quantity_available = forms.DecimalField(
		min_value = 0,
		label = 'Quantity Held',
		required = False,
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': '0',
			})
		)

	image = forms.ImageField(
		label = 'Spare Image',
		required = False,
		widget = forms.FileInput(attrs = {
			'class': 'form-control-file btn btn-outline-secondary',
			})
		)

	page = forms.CharField(
		label = 'D787J Page No.',
		required = False,
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	line = forms.DecimalField(
		min_value = 0,	
		label = 'D787J Line No.',
		required = False,
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': 0,
			})
		)
	description = forms.CharField(
		label = 'Spare Description',
		required = False,
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)
	remarks = forms.CharField(
		label = 'Remarks',
		required = False,
		widget = forms.Textarea(attrs = {
			'class': 'form-control upper',
			'rows': '4',
			})
		)

   

class IssueForm(forms.ModelForm):
	required_css_class = 'required'
	class Meta:
		model = Issue
		fields = ('username', 'quantity_issued', 'remarks')
	
	def __init__(self, *args, **kwargs):
		super(IssueForm, self).__init__(*args, **kwargs)
	
		users = list(CustomUser.objects.all())
		choices = [(e.username, e.username) for e in users]
		choices.sort()
		self.fields['username'] = forms.ChoiceField(			
			label = 'Issue to',			
			choices = choices,
			widget = forms.Select(attrs = {
				'class': 'form-control'
				})
			)

	quantity_issued = forms.DecimalField(		
		min_value = 0,		
		label = 'Quantity Issued',		
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': '0',
			})
		)

	remarks = forms.CharField(		
		label = 'Reason of Issue',
		
		widget = forms.Textarea(attrs = {			
			'class': 'form-control upper',
			'rows': '2',
			})
		)


class ReturnForm(forms.ModelForm):
	class Meta:
		model = Return
		fields = ('username', 'quantity_returned', 'remarks')
	
	def __init__(self, *args, **kwargs):
		super(ReturnForm, self).__init__(*args, **kwargs)
	
		users = list(CustomUser.objects.all())   #+ list(BasicUser.objects.all()
		choices = [(e.username, e.username) for e in users]
		choices.sort()
		self.fields['username'] = forms.ChoiceField(
			label = 'User',
			choices = choices,
			widget = forms.Select(attrs = {
				'class': 'form-control'
				})
			)

	quantity_returned = forms.DecimalField(
		min_value = 0,
		label = 'Quantity Returned',
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': '0',
			})
		)

	remarks = forms.CharField(
		label = 'Remarks',
		required = False,
		widget = forms.Textarea(attrs = {
			'class': 'form-control upper',
			'rows': '6',
			})
		)


class PostSurveyForm(forms.ModelForm):
	class Meta:
		model = PostSurvey
		fields = ('quantity_surveyed', 'survey_number', 'survey_number_date', 'survey_report_date', 'remarks')

	quantity_surveyed = forms.DecimalField(
		min_value = 0,
		label = 'Quantity Surveyed',
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': '0',
			})
		)

	survey_number = forms.CharField(
		label = 'Survey Number',
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	survey_number_date = forms.DateTimeField(
		input_formats=[
			'%d %B %Y - %H:%M',
		])

	survey_report_date = forms.DateTimeField(
		input_formats=[
			'%d %B %Y - %H:%M',
		])

	remarks = forms.CharField(
		label = 'Remarks',		
		widget = forms.Textarea(attrs = {
			'class': 'form-control upper',
			'rows': '5',
			})
		)


class PostDemandForm(forms.ModelForm):
	class Meta:
		model = PostDemand
		fields = ('quantity_demanded', 'demand_number', 'demand_date', 'remarks')

	quantity_demanded = forms.DecimalField(
		min_value = 0,
		label = 'Quantity Demanded',
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': '0',
			})
		)

	demand_number = forms.CharField(
		label = 'Demand Number',
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	demand_date = forms.DateTimeField(
		input_formats = [
			'%d %B %Y - %H:%M',
		])

	remarks = forms.CharField(
		label = 'Remarks',		
		widget = forms.Textarea(attrs = {
			'class': 'form-control upper',
			'rows': '5',
			})
		)


class PostReceiveForm(forms.ModelForm):
	class Meta:
		model = PostReceive
		fields = ('quantity_received', 'receipt_number', 'receive_date', 'remarks')

	quantity_received = forms.DecimalField(
		min_value = 0,
		label = 'Quantity Received',
		widget = forms.NumberInput(attrs = {
			'class': 'form-control',
			'value': '0',
			})
		)
	
	receipt_number = forms.CharField(
		label = 'Receipt Number',
		widget = forms.TextInput(attrs = {
			'class': 'form-control upper',
			})
		)

	receive_date = forms.DateTimeField(
		label = 'Receive Date',
		input_formats = [
			'%d %B %Y - %H:%M',
		])

	remarks = forms.CharField(
		label = 'Remarks',
		widget = forms.Textarea(attrs = {
			'class': 'form-control upper',
			'rows': '5',
			})
		)
