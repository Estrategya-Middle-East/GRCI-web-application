from django.urls import path
from django.urls import get_resolver
from . import views
from .views import PredictiveRiskAnalysisView, PredictiveRiskOptionsAPI, PredictiveRiskAnalysisAPI

urlpatterns = [
    path("", views.dashboard, name="chat_dashboard"),  # Default dashboard for pioneer
    
    #chatbot
    path('chat/', views.chat_view, name='chat'),
    path('ajax/chat/', views.ajax_chat, name='ajax_chat'),
    path('clear/', views.clear_chat, name='clear_chat'),
    path('mismatched-subtotals-response/', PredictiveRiskAnalysisView.as_view(), name='mismatched_subtotals_response'),
    
    #Predictive Risk Analysis
    path('predictive-risk-analysis/', PredictiveRiskAnalysisView.as_view(), name='predictive_risk_analysis'),
    path('load_chart_1/', PredictiveRiskAnalysisView.as_view(), name='load-chart-1'),
    path('load_chart_2/', PredictiveRiskAnalysisView.as_view(), name='load-chart-2'),
    path('load_chart_3/', PredictiveRiskAnalysisView.as_view(), name='load-chart-3'),
    path('load_ai_insights/', PredictiveRiskAnalysisView.as_view(), name='load-ai-insights'),
     
    #api
    path('api/predictive-risk/options/', PredictiveRiskOptionsAPI.as_view(), name='predictive-risk-options'),
    path('api/risk-analysis/', PredictiveRiskAnalysisAPI.as_view(), name='risk-analysis-api'),
]
