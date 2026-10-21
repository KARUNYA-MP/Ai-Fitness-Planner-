from django.contrib import admin
from django.urls import path
from planner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('assessment/', views.assessment, name='assessment'),
    path('goals/', views.goals, name='goals'),
    path('bmi-result/', views.bmi_result, name='bmi_result'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workout/', views.workout, name='workout'),
    path('diet/', views.diet, name='diet'),
    path('plan-30days/', views.plan_30days, name='plan_30days'),
    path('progress/', views.progress, name='progress'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('profile/', views.profile, name='profile'),
]

