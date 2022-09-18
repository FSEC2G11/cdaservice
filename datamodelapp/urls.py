from django.urls import path
from .views import DataModelList, DataModelView

urlpatterns = [
    path('models/', DataModelList.as_view()),
    path('model/<slug:pk>', DataModelView.as_view()),
]