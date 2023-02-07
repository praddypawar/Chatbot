from django.urls import path,include
from . import views
app_name = "appadmins"
urlpatterns =[
    path("",views.index,name="index"),
    path("client-view/",views.clientview,name="clientview"),
    path("client-add/",views.clientadd,name="clientadd"),
    path("client-update/<int:pk>/",views.clientadd,name="clientupdate"),
    path("client-delete/<int:pk>/",views.clientdelete,name="clientdelete"),
    path('bot-builder/',views.bot_builder,name="bot_builder"),
]