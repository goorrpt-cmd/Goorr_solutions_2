#from django.urls import path
#from .views import candidate_list, hello

#urlpatterns = [
#    path("", candidate_list, name="home"),
#    path("hello/", hello, name="hello"),
#]




from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # HTMX endpoints
    path("dashboard/recent-candidates/", views.recent_candidates, name="recent_candidates"),
    path("dashboard/upcoming-interviews/", views.upcoming_interviews, name="upcoming_interviews"),
    path("dashboard/activity/", views.activity_feed, name="activity_feed"),
]
