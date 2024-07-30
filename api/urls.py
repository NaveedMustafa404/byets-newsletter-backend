from django.urls import path, include

urlpatterns = [

    path('auth/', include('authentication.urls')),
    path('content/', include('content.urls')),
    path('newsletter/', include('newsletter.urls')),
   


]
