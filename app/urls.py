import app.views

from django.urls import path

urlpatterns = [
    path('<str:module>/', app.views.SysView.as_view()),
    path('colleges/<str:module>/', app.views.CollegesView.as_view()),
    path('majors/<str:module>/', app.views.MajorsView.as_view()),
    path('companies/<str:module>/', app.views.CompaniesView.as_view()),
    path('jobs/<str:module>/', app.views.JobsView.as_view()),
    path('users/<str:module>/', app.views.UsersView.as_view()),
    path('students/<str:module>/', app.views.StudentsView.as_view()),
    path('educationLogs/<str:module>/', app.views.EducationLogsView.as_view()),
    path('projectLogs/<str:module>/', app.views.ProjectLogsView.as_view()),
    path('sendLogs/<str:module>/', app.views.SendLogs.as_view()),
]