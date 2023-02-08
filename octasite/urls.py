"""octasite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path

from octapply import views
urlpatterns = [
    path('', views.home, name='home'),
    path('university/<slug>/', views.university, name='university'),
    #path('universities/<slug>/', views.university, name='university'),
    path('program_list/', views.ProgramList.as_view()),
    path('program/<slug>/', views.program, name='program'),
    path('professor_list/', views.professor_list, name='professor_list'),
    path('professor/<slug>', views.professor, name='professor'),
    path('<slug>/programs/', views.programs, name='programs'),
    path('<slug>/professors/', views.professors, name='professors'),
    #path('university/', views.UniversityList.as_view()),
    path("universities/", views.uni_list_view, name="uni_list"),
    path("universities/search/", views.uni_list_search_view, name="search"),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^wagtail-admin/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^blog/', include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


