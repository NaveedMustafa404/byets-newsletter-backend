from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # path('', views.content),
    path('send-mail', views.sendMail),
    
    
    # path('list', views.newsletter),
    # path('create', views.newsletterCreate),
    # path('edit/<int:pk>', views.newsletterEdit),
    # path('delete/<int:pk>', views.newsletterDelete),
    # path('toggle-status/<int:pk>', views.toggleNewsStatus),

    

]