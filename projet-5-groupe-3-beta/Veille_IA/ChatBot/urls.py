from django.urls import path
from django.conf.urls import include
from . import views
from utils.tfidf_pipeline import pipeline_tfidf
from django.core.cache import cache

urlpatterns = [
    path('chatbot', views.chatbot, name='chatbot'),
    path('get_bot_response', views.get_bot_response, name='get_bot_response'),
]


