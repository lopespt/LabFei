from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.utils.importlib import import_module


admin.autodiscover()

urlpatterns = patterns('',
    ##url(r'^admin/', include(admin.site.urls)),
)


#PUT ALL VIEWS FILES HERE
import_module('LabFeiApplication.views')
import_module('LabFeiApplication.views_user')
import_module('LabFeiApplication.views_labs')
import_module('LabFeiApplication.views_admin')
