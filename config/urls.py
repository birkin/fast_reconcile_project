# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from fast_reconcile_app import views


admin.autodiscover()


urlpatterns = [

    # url( r'^admin/login/', RedirectView.as_view(pattern_name='login_url') ),

    url( r'^admin/', admin.site.urls ),  # eg host/project_x/admin/

    url( r'^info/$', views.info, name='info_url' ),

    url( r'^v1/reconcile/$', views.reconcile_v1, name='reconcile_v1_url' ),  ## the worker

    # url( r'^login/$', views.login, name='login_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='info_url') ),

    ]
