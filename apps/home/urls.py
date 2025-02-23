# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    
    # API endpoint for saving DQ check
    path('save_dq_check/', views.save_dq_check, name='save_dq_check'),
    
    # Matches any html file - MUST BE LAST
    re_path(r'^.*\.html', views.pages, name='pages'),
]

 