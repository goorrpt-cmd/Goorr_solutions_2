from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from .models import Candidate, Interview, AuditLog

# -----------------------------
# MAIN DASHBOARD VIEW
# -----------------------------
def dashboard(request):
    # High-level metrics
    total_candidates = Candidate.objects.count()
    active_recruiters = 12  # Replace with real logic later
    pending_interviews = Interview.objects.filter(result="PENDING").count()
    new_this_week = Candidate.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()

    context = {
        "total_candidates": total_candidates,
        "active_recruiters": active_recruiters,
        "pending_interviews": pending_interviews,
        "new_this_week": new_this_week,
    }

    return render(request, "dashboard.html", context)


# -----------------------------
# HTMX: Recent Candidates
# -----------------------------
def recent_candidates(request):
    candidates = Candidate.objects.order_by("-created_at")[:10]
    return render(request, "partials/recent_candidates.html", {"candidates": candidates})


# -----------------------------
# HTMX: Upcoming Interviews
# -----------------------------
def upcoming_interviews(request):
    interviews = Interview.objects.filter(
        scheduled_at__gte=timezone.now()
    ).order_by("scheduled_at")[:10]

    return render(request, "partials/upcoming_interviews.html", {"interviews": interviews})


# -----------------------------
# HTMX: Activity Feed (AuditLog)
# -----------------------------
def activity_feed(request):
    logs = AuditLog.objects.select_related("user").order_by("-created_at")[:15]
    return render(request, "partials/activity_feed.html", {"logs": logs})
