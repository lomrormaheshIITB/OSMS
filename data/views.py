import json, os, re, sys
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Spares, SpareClass, EquipmentClass, Authority, Denomination, Issue, IssueList, Return
from .models import Survey, PostSurvey, Demand, PostDemand, Receive, PostReceive
from users.models import Rank

if ('makemigrations' not in sys.argv and 'migrate' not in sys.argv):
	from .forms import SearchForm, SpareForm, SpareClassForm, EquipmentClassForm, DenominationForm, AuthorityForm
	from .forms import IssueForm, ReturnForm, PostSurveyForm, PostDemandForm, PostReceiveForm, RankForm


# Store the search results as a list
SEARCH_RESULT = None

def resetSearch():
	global SEARCH_RESULT
	SEARCH_RESULT = None


# Remove extra spaces
def removeSpace(x):
	try:
		return re.sub(' +', ' ', x)
	except:
		return x




# Return all spare_class present in the database
def GetSpareClass(request):
	spare_class = list(map(lambda x: x.name, SpareClass.objects.all()))
	spare_class.sort()
	return JsonResponse({'spare_class': spare_class})


# Return equipment_class for the given spare_class
def GetEquipmentClass(request, spare_class=None):
	equipment_class = []
	if (spare_class == 'ALL'):
		equipment_class = EquipmentClass.objects.all()
	elif (spare_class):
		equipment_class = EquipmentClass.objects.filter(spare_class=spare_class)
		if (equipment_class.count()):
			equipment_class = list(set(list(map(lambda x: x.name, equipment_class))))
			equipment_class.sort()
			return JsonResponse({'equipment_class': equipment_class})
		else:
			return JsonResponse({'equipment_class': []})


# Home view
def HomeView(request):
	
	# Render home page
	template = 'data/home.html'
	context = {
		'title': 'OSMS | Home'
		
	}
	return render(request, template, context) 


# Search specific spare based on the search form
def SearchView(request):
	template = 'data/search.html'
	context = {
		'title': 'OSMS | Search',
		'user': request.user,
		'form': SearchForm(),
	}
	return render(request, template, context)


# Render the results from the search spare views
def SearchResultView(request):
	global SEARCH_RESULT
	if (request.method == 'POST'):
		form = SearchForm(request.POST)
		# Validate the form
		if (form.is_valid()):
			# Get the fields from the form
			spare_class = form.cleaned_data.get('spare_class')
			equipment_class = form.cleaned_data.get('equipment_class')
			pattern_number = form.cleaned_data.get('pattern_number')
			description = form.cleaned_data.get('description')
			
			# Filter the spares
			spares = Spares.objects.filter()
			if (spare_class != 'ALL'):
				spares = spares.filter(spare_class=spare_class)
			if (equipment_class != 'ALL'):
				spares = spares.filter(equipment_class=equipment_class)
			if (pattern_number):
				spares = spares.filter(pattern_number__icontains=pattern_number)
			if (description):
				spares = spares.filter(description__icontains=description)
			
			# No such spare found
			if (spares.count() == 0):
				resetSearch()
				messages.info(request, "No matching spare found!")
				return redirect('data:search')
			
			# Spares matching the description found
			else:
				SEARCH_RESULT = [e.pk for e in list(spares)]
				template = 'data/searchlist.html'
				context = {
					'title': 'OSMS | Search Result',
					'user': request.user,
					'spares': spares,
				}
				return render(request, template, context)
		# Form validation failed
		else:
			resetSearch()
			messages.error(request, "Form validation failed!")
			return redirect('data:search')

	# Handle get requests  - IF USING BACK BUTTON 
	elif (request.method == 'GET'):
		# If spares already exists
		if (SEARCH_RESULT):
			spares = Spares.objects.filter(pk__in=SEARCH_RESULT)
			template = 'data/searchlist.html'
			context = {
				'title': 'OSMS | Result',
				'user': request.user,
				'spares': spares,
			}
			return render(request, template, context)
		else:
			return redirect('data:search')
		

# Display the spare with given pk
def SpareView(request, pk=None):
	if (pk):
		# Search for the spare that matches the given pk
		spare = Spares.objects.filter(pk=pk)
		if (spare.count() != 0):
			spare = spare[0]
			
			# Figure out the next and previous spares using SEARCH_RESULT
			next_spare = previous_spare = -1
			if (SEARCH_RESULT):
				if (pk in SEARCH_RESULT):
					length = len(SEARCH_RESULT)
					index = SEARCH_RESULT.index(pk)
					
					# Figure out the next spare
					if (index + 1 < length):
						next_spare = SEARCH_RESULT[index + 1]
					else:
						next_spare = SEARCH_RESULT[0]
					
					# Figure out the previous spare
					if (index > 0):
						previous_spare = SEARCH_RESULT[index - 1]
					else:
						previous_spare = SEARCH_RESULT[length - 1]

			# Found the spare, redirect to spare view page
			template = 'data/searchdetails.html'
			context = {
				'title': 'OSMS | View',
				'user': request.user,
				'spare': spare,
				'form': SpareForm(),
				'next': next_spare,
				'previous': previous_spare,
			}
			return render(request, template, context)
		else:
			messages.info(request, 'No matching spare found!')
			return redirect('data:search')
	
	# No pk value specified
	else:
		return redirect('data:search')


# Add a new spare
def AddSpareView(request, force=False):
	global SEARCH_RESULT
	if (request.method == 'POST'):
		form = SpareForm(request.POST, request.FILES)
		# Check if the form is valid
		if (form.is_valid()):
			# Filter the spares
			spare_class = form.cleaned_data.get('spare_class')
			equipment_class = form.cleaned_data.get('equipment_class')
			pattern_number = form.cleaned_data.get('pattern_number')
			spares = Spares.objects.filter(spare_class=spare_class, equipment_class=equipment_class)
			
			# Check if the pattern number matches exactly
			spare = spares.filter(pattern_number=pattern_number)
			if (spare.count() != 0):
				messages.info(request, "Spare already exists!")
				return redirect('data:edit_pk', pk=spare[0].pk)
			else:
				form.save()
				messages.success(request, "Spare added successfully!")
		# Form validation failed
		else:
			messages.error(request, "Form validation failed!")
			return redirect('data:add')
	
	template = 'data/add.html'
	context = {
		'title': 'OSMS | Add',
		'user': request.user,
		'form': SpareForm(),
	}
	return render(request, template, context)


# Edit an existing spare
def EditSpareView(request, pk=None):
	if (pk):
		# Search for the spare that matches the given pk
		spare = Spares.objects.filter(pk=pk)
		if (spare.count() != 0):
			spare = spare[0]
			if (request.method == 'POST'):
				form = SpareForm(request.POST, request.FILES, instance=spare)
				if (form.is_valid()):
					# Save the edited details
					form.save()
					messages.success(request, "Spare details updated!")
					return redirect('data:view_pk', pk=pk)
				else:
					messages.error(request, "Form validation failed!")
					return redirect('data:edit_pk', pk=pk)

			# Render the spare edit page
			template = 'data/edit.html'
			context = {
				'title': 'OSMS | Edit',
				'spare': spare,
				'form': SpareForm(instance=spare),
			}
			return render(request, template, context)
		else:
			messages.info(request, 'No matching spare found!')
			return redirect('data:search')
	# No pk value specified
	else:
		return redirect('data:home')


# List of the spares issued
def IssueListView(request):
	entries = IssueList.objects.all()
	template = 'data/issuelist.html'
	context = {
		'title': 'OSMS | Issue List',
		'entries': entries, 
	}
	return render(request, template, context)


# Issue the spare to a user
def IssueSpareView(request, pk=None):
	if (pk):
		form = IssueForm()
		# Get the spare with the given pk
		spare = Spares.objects.filter(pk=pk)		
		if (spare.count() != 0):
			spare = spare[0]	
			
			if (request.method == 'POST'):
				form = IssueForm(request.POST)
				if (form.is_valid()):
					quantity_issued = form.cleaned_data['quantity_issued']
					username = form.cleaned_data['username']
					if (quantity_issued == 0):
						messages.error(request, "Issued quantity must be greater than 0!")
					elif (quantity_issued > spare.quantity_available):
						messages.error(request, "Issued quantity more than available quantity!")
					else:
						form = form.save(commit=False)
						form.spare = spare
						form.save()   #this saves Issue model instance						
						spare.quantity_available -= quantity_issued
						spare.save()
						# Modify the issue list table ie creating temprory entry
						issue = Issue.objects.filter(spare=pk)
						issue = issue[0]
						spare_toreturn = IssueList.objects.filter(issue_entry=issue)
						
						if (spare_toreturn.count() == 0):
							IssueList.objects.create(issue_entry=form, quantity_toreturn=quantity_issued)
						else:
							spare_toreturn = spare_toreturn[0]
							spare_toreturn.quantity_toreturn += quantity_issued
							spare_toreturn.save()

						# Add to survey / demand based on spare category
						if (spare.category == 'CONSUMABLE'):
							# Check if the spare exists in the demand table
							demand_entry = Demand.objects.filter(spare=spare)
							if (demand_entry.count() == 0):
								# Create a new demand entry
								Demand.objects.create(spare=spare, quantity_todemand=quantity_issued)
							else:
								demand_entry = demand_entry[0]
								demand_entry.quantity_todemand += quantity_issued
								demand_entry.save()
						else:
							# Check if the spare exists in the survey table
							survey_entry = Survey.objects.filter(spare=spare)
							if (survey_entry.count() == 0):
								# Create a new survey entry
								Survey.objects.create(spare=spare, quantity_tosurvey=quantity_issued)
							else:
								survey_entry = survey_entry[0]
								survey_entry.quantity_tosurvey += quantity_issued
								survey_entry.save()

						messages.success(request, "Spare issued!")
						return redirect('data:view_pk', pk=pk)
				else:
					messages.error(request, "Form validation failed!")

			# Redirect to the issue spare page
			template = 'data/issue.html'
			context = {
				'title': 'OSMS | Issue',
				'spare': spare,
				'form': form,
			}
			return render(request, template, context)
		# Spare not found
		else:
			messages.info(request, "No matching spare found!")
			return redirect('data:home')
	# No pk value specified
	else:
		return redirect('data:home')


# Return spares
def ReturnSpareView(request, pk=None):
	if (pk):
		# Fetch the spare
		spare = Spares.objects.filter(pk=pk)
		issue = Issue.objects.filter(spare=pk)
		# Check if spare exists
		if (spare.count() != 0):
			spare = spare[0]
			issue = issue[0]
			issue_entry = IssueList.objects.filter(issue_entry=issue)
			# Check if there is an issue entry
			if (issue_entry.count() == 0):
				messages.error(request, "Spare currently not issued!")
			else: 
				issue_entry = issue_entry[0]
				username = issue.username
			form = ReturnForm()			
			if (request.method == 'POST'):
				form = ReturnForm(request.POST)
				# Check if form is valid
				if (form.is_valid()):					
					quantity_returned = form.cleaned_data['quantity_returned']
					# Check if the quantity being returned is valid
					if (quantity_returned == 0):
						messages.error(request, "Returned quantity must be greater than 0!")
					elif (quantity_returned > issue_entry.quantity_toreturn):
						messages.error(request, "Returned quantity must be less than or equal to quantity issued!")
					else:
						# Save the form to the return table
						form.username = username
						form = form.save(commit=False)
						form.spare = spare
						form.save()
						# Update the spare quantity
						spare.quantity_available += quantity_returned
						spare.save()
						# Update the issue list table
						issue_entry.quantity_toreturn -= quantity_returned
						if (issue_entry.quantity_toreturn <= 0):
							issue_entry.delete()
						else:
							issue_entry.save()
						# Remove the spare from demand table 
						if (spare.category == 'CONSUMABLE'):
							# Check if the spare exists in the demand table
							demand_entry = Demand.objects.filter(spare=spare)
							if (demand_entry.count() != 0):
								# Spare entry still exists in the to be demanded table
								demand_entry = demand_entry[0]
								demand_entry.quantity_todemand -= quantity_returned
								if (demand_entry.quantity_todemand <= 0):
									demand_entry.delete()
								else:
									demand_entry.save()
						else:
							# Check if the spare exists in the survey table
							survey_entry = Survey.objects.filter(spare=spare)
							if (survey_entry.count() != 0):
								# Spare entry still exists in the to be surveyed table
								survey_entry = survey_entry[0]
								survey_entry.quantity_tosurvey -= quantity_returned
								if (survey_entry.quantity_tosurvey <= 0):
									survey_entry.delete()
								else:
									survey_entry.save()

						messages.success(request, "Spare returned!")
						return redirect('data:view_pk', pk=pk)
				else:
					messages.error(request, "Form validation failed!")
			
			
			# Render the spare return page
			template = 'data/return.html'
			context = {
				'title': 'OSMS | Return',
				'spare': spare,
				'form': form,				
				'entry':issue_entry,
			}
			return render(request, template, context)
		else:
			messages.info(request, 'No matching spare found!')
			return redirect('data:search')
	# No pk value specified
	else:
		return redirect('data:search')


# Spares to be surveyed
def SurveyListView(request):
	# Render the page with the spares to be surveyed
	entries = Survey.objects.all()
	template = 'data/surveylist.html'
	context = {
		'title': 'OSMS | To Be Surveyed',
		'entries': entries,
	}
	return render(request, template, context)


# Survey details for the spare selected
def SurveyDetailsView(request, pk=None):
	if (pk):
		# Get the survey entry
		survey_entry = Survey.objects.filter(pk=pk)
		# Form to enter post survey details
		form = PostSurveyForm()
		if (survey_entry.count() != 0):
			survey_entry = survey_entry[0]
			spare = survey_entry.spare
			# Find the quantity that was supposed to be surveyed
			quantity_tosurvey = survey_entry.quantity_tosurvey
			
			if (request.method == 'POST'):
				form = PostSurveyForm(request.POST)
				# Vaidate the form
				if (form.is_valid()):
					survey_number = form.cleaned_data['survey_number'].upper()
					remarks = form.cleaned_data['remarks'].upper()
					quantity_surveyed = form.cleaned_data['quantity_surveyed']				
					quantity_tosurvey -= quantity_surveyed			

					# Check if the survey number exists for another spare in the PostSurvey table
					postsurvey_entry = PostSurvey.objects.filter(survey_number=survey_number)
					if (postsurvey_entry.count() != 0 and postsurvey_entry[0].spare != spare):					
						messages.error(request, "Survey number already exists for a different spare!")
						return redirect('data:surveydetails_pk', pk=pk)
						
					#  Modify the survey table details
					elif (quantity_tosurvey == 0):
						survey_entry.delete()
					else:
						survey_entry.quantity_tosurvey = quantity_tosurvey
						survey_entry.save()
					# Save the form
					surveydetails = form.save(commit=False)
					surveydetails.spare = spare  #since this is a foreign key its specified separately
					surveydetails.save()

					# Add the spare to demand table
					demand_entry = Demand.objects.filter(spare=spare)
					# Modify the demand table details
					if (demand_entry.count() == 0):
						# Create a new demand entry for permanent/returnable items only
						Demand.objects.create(spare=spare,survey_entry=surveydetails, quantity_todemand=quantity_surveyed)
					else:
						# Update the existing demand details in Demand model
						entry_created = False
						for entry in demand_entry:
							if (entry.survey_entry.survey_number == survey_number) and (entry.survey_entry.remarks == remarks):
								entry.quantity_todemand += quantity_surveyed
								entry.save()
								entry_created = True
								break
						# Spare has a new survey number or remards then create a new entry
						if (not entry_created):
							Demand.objects.create(spare=spare,survey_entry=surveydetails, quantity_todemand=quantity_surveyed)
					messages.success(request, "Survey details updated!")
					return redirect('data:surveylist')
				else:
					messages.error(request, "Form validation failed!")

			# Render the page to enter suvey details
			template = 'data/surveydetails.html'
			context = {
				'title': 'OSMS | Survey Details',
				'entry': survey_entry,
				'form': form,
			}
			return render(request, template, context)
		else:
			messages.error(request, "No matching spare found!")
			return redirect('data:surveylist')
	else:
		# No pk value specified
		return redirect('data:surveylist')

# Bypass Survey details view
def SurveyBypassView(request, pk):
	if (pk):
		# Get the survey entry
		survey_entry = Survey.objects.filter(pk=pk)
		if (survey_entry.count() != 0):
			survey_entry = survey_entry[0]
			Demand.objects.create(spare=survey_entry.spare, survey_entry=None, quantity_todemand=survey_entry.quantity_tosurvey)
			survey_entry.delete()
			messages.error(request, "Survey details not taken view item can be demanded directly using authority!")
			return redirect('data:surveylist')
		else:
			# No survey entry found
			messages.error(request, "No matching entry found!")
			return redirect('data:surveylist')
	else:
		# No pk value specified
		return redirect('data:surveylist')



# Spares to be demanded
def DemandListView(request):
	# Render the page with the spares to be demanded
	entries = Demand.objects.all()
	
	template = 'data/demandlist.html'
	context = {
		'title': 'OSMS | To Be Demanded',
		'entries': entries,
		
	}
	return render(request, template, context)


# Demand details for the spare selected
def DemandDetailsView(request, pk=None):
	if (pk):
		# Get the demand entry
		demand_entry = Demand.objects.filter(pk=pk)		
		# Form to enter post demand details
		form = PostDemandForm()
		if (demand_entry.count() != 0):
			demand_entry = demand_entry[0]
			#get the spare
			spare = demand_entry.spare
			# Find the quantity that was supposed to be demanded
			quantity_todemand = demand_entry.quantity_todemand			
			if (request.method == 'POST'):
				form = PostDemandForm(request.POST)
				# Vaidate the form
				if (form.is_valid()):
					demand_number= form.cleaned_data['demand_number'].upper()
					remarks = form.cleaned_data['remarks'].upper()
					quantity_demanded = form.cleaned_data['quantity_demanded']
					quantity_todemand -= quantity_demanded
					# Check if the demand number exists for another spare in the PostDemand table
					postdemand_entry = PostDemand.objects.filter(demand_number=demand_number)
					if (postdemand_entry.count() != 0 and postdemand_entry[0].spare != spare):					
						messages.error(request, "Demand number already exists for a different spare!")
						return redirect('data:demanddetails_pk', pk=pk)
					# Modify the demand table details
					elif (quantity_todemand == 0):					
						demand_entry.delete()
					else:
						demand_entry.quantity_todemand = quantity_todemand
						demand_entry.save()
					# Save the form
					demanddetails = form.save(commit=False)
					demanddetails.spare = spare
					demanddetails.save()
					# Add the spare to receive table
					receive_entry = Receive.objects.filter(spare=spare)
					if (receive_entry.count() == 0):
						# Create a new receive entry
						Receive.objects.create(spare=spare,demand_entry=demanddetails, quantity_toreceive=quantity_demanded)
					else:
						# Update the existing receive details
						entry_created = False
						for entry in receive_entry:
							if (entry.demand_entry.demand_number == demand_number) and (entry.demand_entry.remarks == remarks):
								entry.quantity_toreceive += quantity_demanded
								entry.save()
								entry_created = True
								break
						# Spare has a new survey number or remards then create a new entry
						if (not entry_created):
							Receive.objects.create(spare=spare,demand_entry=demanddetails, quantity_toreceive=quantity_demanded)						
					messages.success(request, "Demand details updated!")
					return redirect('data:demandlist')
				else:
					messages.error(request, "Form validation failed!")

			# Render the page to enter suvey details
			template = 'data/demanddetails.html'
			context = {
				'title': 'OSMS | Demand Details',
				'entry': demand_entry,
				'form': form,
			}
			return render(request, template, context)
		else:
			messages.error(request, "No matching demand entry found!")
			return redirect('data:demandlist')
	else:
		# No pk value specified
		return redirect('data:demandlist')


# Spares to be received
def ReceiveListView(request):
	# Render the page with the spares to be received
	entries = Receive.objects.all()	
	template = 'data/receivelist.html'
	context = {
		'title': 'OSMS | To Be Received',
		'entries': entries,
	}
	return render(request, template, context)


# Receive details for the spare selected
def ReceiveDetailsView(request, pk=None):
	if (pk):
		# Get the receive entry
		receive_entry = Receive.objects.filter(pk=pk)		
		# Form to enter post demand details
		form = PostReceiveForm()
		if (receive_entry.count() != 0):
			receive_entry = receive_entry[0]
			spare = receive_entry.spare
			# Find the quantity that was supposed to be demanded
			quantity_toreceive = receive_entry.quantity_toreceive			
			if (request.method == 'POST'):
				form = PostReceiveForm(request.POST)
				# Vaidate the form
				if (form.is_valid()):
					quantity_received = form.cleaned_data['quantity_received']
					remarks = form.cleaned_data['remarks'].upper()
					if (quantity_received == 0):
						messages.error(request, "Quantity received must be greater than 0!")
					elif (quantity_received > quantity_toreceive):
						messages.error(request, "Quantity received must be less than or equal to quantity to be received!")
					else:
						quantity_toreceive -= quantity_received
						# Modify the receive table details
						if (quantity_toreceive == 0):
							receive_entry.delete()
						else:
							receive_entry.quantity_toreceive = quantity_toreceive
							receive_entry.save()
						# Save the form
						receivedetails = form.save(commit=False)
						receivedetails.spare = spare
						receivedetails.save()
						# Modify the spare details in the spares table
						spare.quantity_available += quantity_received
						spare.save()
						
						# Modify the issue list table after receiving the spare
						issue = Issue.objects.filter(spare=spare)
						issue = issue[0]
						issue_entry = IssueList.objects.filter(issue_entry=issue)
						if (issue_entry.count() != 0):
							delta = quantity_received
							# issue_entry = issue_entry[0]
							for entry in issue_entry:
								if (delta >= entry.quantity_toreturn):
									delta -= entry.quantity_toreturn
									entry.delete()
								else:
									entry.quantity_toreturn -= delta
									entry.save()
									break
						messages.success(request, "Receive details updated!")
						return redirect('data:receivelist')
				else:
					messages.error(request, "Form validation failed!")

			# Render the page to enter suvey details
			template = 'data/receivedetails.html'
			context = {
				'title': 'OSMS | Receive Details',
				'entry': receive_entry,
				'form': form,
			}
			return render(request, template, context)
		else:
			messages.error(request, "No matching spare found!")
			return redirect('data:receivelist')
	else:
		# No pk value specified
		return redirect('data:receivelist')


# History tracking - issue, return, survey, demand, receive
def HistoryView(request):
	history_issue = [
		{
		'pattern_number': e.spare.pattern_number, 
		'equipment_class': e.spare.equipment_class, 
		'description': e.spare.description, 
		'username': e.username,		
		'quantity': str(e.quantity_issued),
		'date': e.issue_time,
		'remarks': e.remarks,
		}
		for e in Issue.objects.all()
	]
	history_return = [
		{
		'pattern_number': e.spare.pattern_number, 
		'equipment_class': e.spare.equipment_class, 
		'description': e.spare.description, 
		'username': e.username,
		'quantity': e.quantity_returned,
		'date': e.return_time,
		'remarks': e.remarks,
		}
		for e in Return.objects.all()
	]
	history_survey = [
		{
		'pattern_number': e.spare.pattern_number, 
		'equipment_class': e.spare.equipment_class, 
		'description': e.spare.description, 
		'quantity': e.quantity_surveyed,
		'survey_number': e.survey_number,
		'date': e.survey_report_date,
		'remarks': e.remarks,
		}
		for e in PostSurvey.objects.all()
	]
	history_demand = [
		{
		'pattern_number': e.spare.pattern_number, 
		'equipment_class': e.spare.equipment_class, 
		'description': e.spare.description, 
		'quantity': e.quantity_demanded,
		'demand_number': e.demand_number,
		'date': e.demand_date,
		'remarks': e.remarks,
		}
		for e in PostDemand.objects.all()
	]
	history_receive = [
		{
		'pattern_number': e.spare.pattern_number, 
		'equipment_class': e.spare.equipment_class, 
		'description': e.spare.description, 
		'quantity': e.quantity_received,
		'receipt_number': e.receipt_number,		
		'date': e.receive_date,
		'remarks': e.remarks,
		}
		for e in PostReceive.objects.all()
	]
	data = {
		'history_issue': history_issue,
		'history_return': history_return,
		'history_survey': history_survey,
		'history_demand': history_demand,
		'history_receive': history_receive
	}
	data = json.dumps(data, cls=DjangoJSONEncoder)
	template = 'data/history.html'
	context = {
		'title': 'OSMS | History',
		'data': data, 
	}
	return render(request, template, context)


# Add new spare class, equipment class, denomination
def AddMiscellaneous(request):
	if (request.method == 'POST'):
		form_id = request.POST.get('form_id')
		if (form_id == '1'):
			form = SpareClassForm(request.POST)
			if (form.is_valid()):
				name = form.cleaned_data.get('name').upper()
				name = removeSpace(name)
				spare_class = SpareClass.objects.filter(name=name)
				if (spare_class.count() != 0):
					return JsonResponse({'message': 'Entry already exists!'})
				else:
					form = form.save(commit=False)
					form.name = name
					form.save()
					return JsonResponse({'message': 'New entry created!'})
			else:
				return JsonResponse({'message': 'Form validation failed!'})
		elif (form_id == '2'):
			form = DenominationForm(request.POST)
			if (form.is_valid()):
				name = form.cleaned_data.get('name').upper()
				name = removeSpace(name)
				denomination = Denomination.objects.filter(name=name)
				if (denomination.count() != 0):
					return JsonResponse({'message': 'Entry already exists!'})
				else:
					form = form.save(commit=False)
					form.name = name
					form.save()
					return JsonResponse({'message': 'New entry created!'})
			else:
				return JsonResponse({'message': 'Form validation failed!'})
		elif (form_id == '3'):
			form = EquipmentClassForm(request.POST)
			if (form.is_valid()):
				name = form.cleaned_data.get('name').upper()
				name = removeSpace(name)
				spare_class = form.cleaned_data.get('spare_class').upper()
				equipment_class = EquipmentClass.objects.filter(name=name, spare_class=spare_class)
				if (equipment_class.count() != 0):
					return JsonResponse({'message': 'Entry already exists!'})
				else:
					form = form.save(commit=False)
					form.name = name
					form.save()
					return JsonResponse({'message': 'New entry created!'})
			else:
				return JsonResponse({'message': 'Form validation failed!'})
		elif (form_id == '4'):
			form = AuthorityForm(request.POST)
			if (form.is_valid()):
				name = form.cleaned_data.get('name').upper()
				name = removeSpace(name)
				authority = Authority.objects.filter(name=name)
				if (authority.count() != 0):
					return JsonResponse({'message': 'Entry already exists!'})
				else:
					form = form.save(commit=False)
					form.name = name
					form.save()
					return JsonResponse({'message': 'New entry created!'})
			else:
				return JsonResponse({'message': 'Form validation failed!'})
		elif (form_id == '5'):
			form = RankForm(request.POST)
			if (form.is_valid()):
				name = form.cleaned_data.get('name').upper()
				name = removeSpace(name)
				rank = Rank.objects.filter(name=name)
				if (rank.count() != 0):
					return JsonResponse({'message': 'Entry already exists!'})
				else:
					form = form.save(commit=False)
					form.name = name
					form.save()
					return JsonResponse({'message': 'New entry created!'})
			else:
				return JsonResponse({'message': 'Form validation failed!'})
	template = 'data/miscellaneous.html'
	context = {
		'title': 'Add Miscellaneous',
		'form1': SpareClassForm(),
		'form2': DenominationForm(),
		'form3': EquipmentClassForm(),
		'form4': AuthorityForm(),
		'form5': RankForm(),
	}
	return render(request, template, context)


def AboutUsView(request):
	template = 'data/about_us.html'
	context = {
		'title': 'O-SMS | About O-SMS',
		 
	}
	return render(request, template, context)

