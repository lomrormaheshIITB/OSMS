from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'data'
urlpatterns = [
	path('', views.HomeView, name='home'),

	path('search/', views.SearchView, name='search'),
	path('search_result/', views.SearchResultView, name='search_result'),	

	path('view/', views.SpareView, name='view'),
	path('view/<int:pk>/', views.SpareView, name='view_pk'),

	path('add/', views.AddSpareView, name='add'),
	path('add/<int:force>/', views.AddSpareView, name='add_force'),

	path('miscellaneous/', views.AddMiscellaneous, name='miscellaneous'),

	path('edit/', views.EditSpareView, name='edit'),
	path('edit/<int:pk>/', views.EditSpareView, name='edit_pk'),

	path('issue_list/', views.IssueListView, name='issuelist'),
	path('issue/', views.IssueSpareView, name='issue'),
	path('issue/<int:pk>/', views.IssueSpareView, name='issue_pk'),

	path('return/', views.ReturnSpareView, name='return'),
	path('return/<int:pk>/', views.ReturnSpareView, name='return_pk'),

	path('survey_list/', views.SurveyListView, name='surveylist'),
	path('survey_details/', views.SurveyDetailsView, name='surveydetails'),
	path('survey_details/<int:pk>/', views.SurveyDetailsView, name='surveydetails_pk'),

	path('survey_bypass/', views.SurveyBypassView, name='surveybypass'),
	path('survey_bypass/<int:pk>/', views.SurveyBypassView, name='surveybypass_pk'),

	path('demand_list/', views.DemandListView, name='demandlist'),
	path('demand_details/', views.DemandDetailsView, name='demanddetails'),
	path('demand_details/<int:pk>/', views.DemandDetailsView, name='demanddetails_pk'),


	path('receive_list/', views.ReceiveListView, name='receivelist'),
	path('receive_details/', views.ReceiveDetailsView, name='receivedetails'),
	path('receive_details/<int:pk>/', views.ReceiveDetailsView, name='receivedetails_pk'),

	path('history/', views.HistoryView, name='history'),
	# path('history/issue/', views.IssueHistoryView, name='history_issue'),

	path('spare_class/', views.GetSpareClass, name='spare_class'),

	path('equipment_class/', views.GetEquipmentClass, name='equipment_class'),
	re_path(r'equipment_class/(?P<spare_class>[\w ]+)/', views.GetEquipmentClass, name='equipment_class_slug'),



	path('about_us/', views.AboutUsView, name='about_us'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

