from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import dashboard_router, candidate_report, candidate_report_pdf,recent_candidates,upcoming_interviews,activity_feed
app_name = "api"


urlpatterns = [
    path("dashboard/", dashboard_router, name="dashboard"),

    # HTMX endpoints (clean)
    path("recent-candidates/", views.recent_candidates, name="recent_candidates"),
    #path("upcoming-interviews/", views.upcoming_interviews, name="upcoming_interviews"),
    path("upcoming-interviews/", views.upcoming_interviews,name="upcoming_interviews"),
    path("activity/", views.activity_feed, name="activity_feed"),
    # Candidate report
     path("/dashboard/candidate/<int:candidate_id>/report/", candidate_report, name="candidate_report"),
     path("candidate/<int:candidate_id>/report/pdf/", candidate_report_pdf, name="candidate_report_pdf"),
]


