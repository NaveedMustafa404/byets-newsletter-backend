from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.content), #need pagination
    path('list', views.contentPaginated), #need pagination
    path('detail/<str:slug>', views.contentDetails),
    path('create', views.contentCreate),
    path('update/<int:pk>', views.contentEdit),
    path('delete/<int:pk>', views.contentDelete),
    
    path('draft', views.contentDraft),
    path('draft/create', views.contentDraftEdit),
    path('draft/delete/<int:pk>', views.contentDraftDelete),

    path('settings', views.getEmailSettings),
    path('settings/edit', views.settingsEdit),
    
    path('layout/list', views.layout),
    path('layout/list/by-published/<str:pub_st>', views.layoutFiltered),
    path('layout/detail/<int:pk>', views.layoutDetails),
    path('layout/update/<int:pk>', views.layoutEdit),
    path('layout/create', views.layoutCreate),
    path('layout/delete/<int:pk>', views.layoutDelete),
    path('layout/toggle-status/<int:pk>', views.toggleLayoutStatus),
    
    path('blog', views.getBlogs), # need pagination
    path('blog/list', views.getBlogsPaginated), # need pagination
    path('blog/create', views.createBlog),
    path('blog/delete/<int:pk>', views.deleteBlog),
    
    
    

    

]