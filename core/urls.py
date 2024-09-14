from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', homePage_view, name='home'),
    path('events/', eventsPage_view, name='all-events'),
    path('blogs/', blogsPage_view, name='all-blogs'),
    path('new_blog/', addBlogPost_view, name='new-blog'),
    path('new_event/', addEventPost_view, name='new-event'),
    path("upload_image/", upload_image_view, name="upload-image"),
    path('blog/<slug:slug>/', blogDetailPage_view, name='blog-detail'),
    path('event/<slug:slug>/', eventDetailPage_view, name='event-detail'),
    path('post/<slug:slug>/delete', deletePost_view, name='delete-post'),
    path('post/<slug:slug>/edit', editPost_view, name='edit-post'),
] 