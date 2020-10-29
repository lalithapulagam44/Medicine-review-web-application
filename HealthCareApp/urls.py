from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('MedicineDetails.html', views.MedicineDetails, name="MedicineDetails"),
	       path('SetReminder.html', views.SetReminder, name="SetReminder"),
	       path('ViewPatientRequest.html', views.ViewPatientRequest, name="ViewPatientRequest"),
	       path('ViewMedicineDetails.html', views.ViewMedicineDetails, name="ViewMedicineDetails"),
	       path('ViewReminder.html', views.ViewReminder, name="ViewReminder"),
	       path('ViewPrescription.html', views.ViewPrescription, name="ViewPrescription"),
	       path('SendQuery.html', views.SendQuery, name="SendQuery"),
	       path('SendQueryRequest.html', views.SendQueryRequest, name="SendQueryRequest"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('AddMedicineDetails', views.AddMedicineDetails, name="AddMedicineDetails"),
	       path('SetReminderAction', views.SetReminderAction, name="SetReminderAction"),
	       path('PrescriptionAction', views.PrescriptionAction, name="PrescriptionAction"),
	       path('ViewMap', views.ViewMap, name="ViewMap"),
	       path('SendPrescription', views.SendPrescription, name="SendPrescription"),
	       path('ViewMedicineDetailsAction', views.ViewMedicineDetailsAction, name="ViewMedicineDetailsAction"),
]