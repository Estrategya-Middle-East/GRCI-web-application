from django.urls import path
from . import views
from .views import PredictiveRiskAnalysisView

urlpatterns = [
    path("", views.dashboard, name="chat_dashboard"),  # Default dashboard for pioneer
    
    #chatbot
    path('chat/', views.chat_view, name='chat'),
    path('ajax/chat/', views.ajax_chat, name='ajax_chat'),
    path('clear/', views.clear_chat, name='clear_chat'),
    
    
    #Predictive Risk Analysis
    path('predictive-risk-analysis/', PredictiveRiskAnalysisView.as_view(), name='predictive_risk_analysis'),
]
