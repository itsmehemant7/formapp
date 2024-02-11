from django.urls import path
from . import views

urlpatterns = [ 
    path("submit",views.submit,name='submit'),
    path("client/<int:id>",views.get_client_info,name="get_client_info")
   
] 
