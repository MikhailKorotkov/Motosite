from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', ForumHome.as_view(), name='home'),
    path('archieve/<int:year>/', archieve),
    path('about/', AboutForum.as_view(), name='about'),
    path('addbike/', AddBike.as_view(), name='add_bike'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>/', cache_page(60)(ShowPost.as_view()), name='post'),
    path('category/<slug:cat_slug>/', cache_page(60)(MotoCategory.as_view()), name='category'),
]
