"""
URL configuration for Test project.

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from testapp.views import HomePage,login,logout,perosonIndex,open1,\
    homeDelete,homeEdit,homeIndex,HomePost,\
    signView,signPost,signEdit,signallIndex,Detail,\
    meetingallIndex,meetingView,meetingPost,meetingEdit,meetinginnerView,\
    meetinginnerEdit,meetinginnerPost,meetinginnerIndex,meetinginnerDelete,\
    contactallIndex,contactView,contactPost,contactEdit,\
    contractallIndex,contractPost,contractEdit,contractView,\
    contractinnerDelete,contractinnerIndex,contractinnerEdit,contractinnerPost,contractinnerView,\
    changeallIndex,changeView,changeEdit,changePost

urlpatterns = [
    path('',HomePage),
    path('HomePage/',HomePage),
    path('login/', login),
    path('logout/', logout),
    path('perosonIndex/<str:cUsername>/',perosonIndex),
    path('open1/<int:id>/<str:mode>',open1),

    path('homeIndex/',homeIndex),
    path('homePost/',HomePost),
    path('homeEdit/<int:id>/<str:mode>',homeEdit),
    path('homeDelete/<int:id>/',homeDelete),

    path('signallIndex/',signallIndex),
    path('signView/<str:cNumber>/',signView),
    path('signPost/<str:cNumber>/',signPost),
    path('signEdit/<str:cNumber>/<int:id>/<str:mode>',signEdit),
    path('Detail/<str:cNumber>/',Detail),

    path('meetingallIndex/',meetingallIndex),
    path('meetingView/<str:cNumber>/',meetingView),
    path('meetingPost/<str:cNumber>/',meetingPost),
    path('meetingEdit/<str:cNumber>/<int:id>/<str:mode>',meetingEdit),

    path('meetinginnerDelete/<str:cNumber>/<int:id>/',meetinginnerDelete),
    path('meetinginnerIndex/<str:cNumber>/',meetinginnerIndex),
    path('meetinginnerEdit/<str:cNumber>/<int:id>/<str:mode>',meetinginnerEdit),
    path('meetinginnerPost/<str:cNumber>/',meetinginnerPost),
    path('meetinginnerView/<str:cNumber>/<int:id>/',meetinginnerView),

    path('contactallIndex/',contactallIndex),
    path('contactView/<str:cNumber>/',contactView),
    path('contactPost/<str:cNumber>/',contactPost),
    path('contactEdit/<str:cNumber>/<int:id>/<str:mode>',contactEdit),

    path('contractallIndex/',contractallIndex),
    path('contractPost/<str:cNumber>/',contractPost),
    path('contractEdit/<str:cNumber>/<int:id>/<str:mode>',contractEdit),
    path("contractView/<str:cNumber>/",contractView),

    path('contractinnerDelete/<str:cNumber>/<int:id>/',contractinnerDelete),
    path('contractinnerIndex/<str:cNumber>/',contractinnerIndex),
    path('contractinnerEdit/<str:cNumber>/<int:id>/<str:mode>',contractinnerEdit),
    path('contractinnerPost/<str:cNumber>/',contractinnerPost),
    path('contractinnerView/<str:cNumber>/<int:id>/',contractinnerView),

    path('changeallIndex/',changeallIndex),
    path('changeView/<str:cNumber>/',changeView),
    path('changeEdit/<str:cNumber>/<int:id>/<str:mode>',changeEdit),
    path('changePost/<str:cNumber>/',changePost),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
