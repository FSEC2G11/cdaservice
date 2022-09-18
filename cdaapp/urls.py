from django.urls import path
from .views import AnalysisRunView, AnalysisRunList, AnalyzerView

urlpatterns = [
    path('runs/', AnalysisRunList.as_view()),
    path('run/<slug:pk>', AnalysisRunView.as_view()),
    path('analyze/<slug:pk>', AnalyzerView.as_view())
]