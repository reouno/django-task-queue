from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api_server.demoapp import views

urlpatterns = format_suffix_patterns([
    path('call-debug-task/', views.CallDebugTask.as_view(), name='call-debug-task'),
    path('call-sleep-task/', views.CallSleepTask.as_view(), name='call-sleep-task'),
])
