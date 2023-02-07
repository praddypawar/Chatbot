from django.urls import path,include
from . import views
app_name = "appclient"
urlpatterns =[
    path("",views.index,name="index"),
    path('bot-builder/',views.bot_builder,name="bot_builder"),
    path('advance-bot-builder/',views.advance_bot_builder,name="advance_bot_builder"),
    path("chat-bot-<str:c_id>-<ch_id>/",views.clientchatboturl,name="clientchatboturl"),
    path("client-chatbot-list/",views.clientchatbotlist,name="clientchatbotlist"),
    path("clientdeletechatbot/<int:pk>/",views.clientdeletechatbot,name="clientdeletechatbot"),
]