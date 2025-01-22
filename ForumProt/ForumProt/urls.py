"""
URL configuration for ForumProt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Imp
    ort the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from forum import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration', views.registration_regular_user),
    path('login', views.login_regular_user),
    path('logout', views.logout_user),
    path('create_publication', views.create_publication),
    path('publication', views.publication_view),
    path('edit_publication', views.edit_publication),
    path('delete_publication', views.delete_publication),
    path('staff_registration', views.registration_staff),
    path('publ_upvote', views.publ_upvote),
    path('', views.home_page),

]
handler404 = 'forum.views.error_404_view'
