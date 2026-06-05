from django.shortcuts import render,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.models import Candidate, Interview
from django.http import JsonResponse
from django.db.models import Q
from .utils import get_user_role
from django.db.models import Count
from .models import (
    Candidate,
    Interview,
    Employer,
    ERPPBatch,
    WorkPermit,
    VisaApplication,
    AuditLog,
)

# ----------------------------------------------------
# ROLE-BASED DASHBOARD ROUTER
# ----------------------------------------------------

# views.py
from django.shortcuts import render
from django.utils import timezone
from .models import Candidate, Interview

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from .models import Candidate, Interview

def dashboard(request):
    today = timezone.localdate()

    kpi_candidates = Candidate.objects.count()

    kpi_interviews = Interview.objects.filter(
        scheduled_at__date=today
    ).count()

    kpi_erpp = Candidate.objects.filter(
        erpp_enrollments__isnull=False
    ).distinct().count()

    kpi_contracts = Candidate.objects.filter(
        contracts__is_active=True
    ).distinct().count()

    kpi_visas = Candidate.objects.filter(
        visa_applications__status="pending"
    ).distinct().count()

    context = {
        "kpi_candidates": kpi_candidates,
        "kpi_interviews": kpi_interviews,
        "kpi_erpp": kpi_erpp,
        "kpi_contracts": kpi_contracts,
        "kpi_visas": kpi_visas,
    }

    return render(request, "admin/index.html", context)


@login_required
def dashboard_router(request):
    role = get_user_role(request.user)

    if role == "ADMIN":
        return redirect("/admin/")   # ← send admins to Jazzmin

    if role == "RECRUITER":
        return recruiter_dashboard(request)

    if role == "AGENCY MANAGER":
        return agency_manager_dashboard(request)

    return render(request, "dashboards/no_role.html")

# @login_required
# def dashboard_router(request):
#     role = get_user_role(request.user)

#     if role == "ADMIN":
#         return admin_dashboard(request)

#     if role == "RECRUITER":
#         return recruiter_dashboard(request)

#     if role == "AGENCY MANAGER":
#         return agency_manager_dashboard(request)

#     return render(request, "dashboards/no_role.html")


# ----------------------------------------------------
# ADMIN DASHBOARD
# ----------------------------------------------------
@login_required
def admin_dashboard(request):
    context = {
        "total_candidates": Candidate.objects.count(),
        "total_interviews": Interview.objects.count(),
        "total_batches": ERPPBatch.objects.count(),
        "total_employers": Employer.objects.count(),
    }
    return render(request, "dashboards/admin_dashboard.html", context)
    #return render(request, "admin/custom_index.html", context)
    #return render(request, "dashboards/login.html")



@login_required
def recruiter_dashboard(request):
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    district = request.GET.get("district", "")
    gender = request.GET.get("gender", "")

    # ---------------------------
    # 1. Base queryset
    # ---------------------------
    candidates = Candidate.objects.all()

    # ---------------------------
    # 2. Apply search
    # ---------------------------
    if search:
        candidates = candidates.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(candidate_id__icontains=search)
        )

    # ---------------------------
    # 3. Apply filters
    # ---------------------------
    if status:
        candidates = candidates.filter(status=status)

    if district:
        candidates = candidates.filter(district=district)

    if gender:
        candidates = candidates.filter(gender=gender)

    # ---------------------------
    # 4. Dashboard sections
    # ---------------------------
    new_candidates = candidates.order_by("-created_at")[:10]

    upcoming_interviews = Interview.objects.filter(
        scheduled_at__gte=timezone.now()
    ).select_related("candidate").order_by("scheduled_at")[:10]

    pending_candidates = candidates.filter(
        status=Candidate.Status.REGISTERED
    ).order_by("created_at")[:10]

    context = {
        "new_candidates": new_candidates,
        "upcoming_interviews": upcoming_interviews,
        "pending_candidates": pending_candidates,
        "search": search,
        "status": status,
        "district": district,
        "gender": gender,
    }

    return render(request, "dashboards/recruiter_dashboard.html", context)
# ----------------------------------------------------
# AGENCY MANAGER DASHBOARD
# ----------------------------------------------------
@login_required
def agency_manager_dashboard(request):
    user = request.user

    # Agencies managed by this user
    agencies = getattr(user, "managed_agencies", None)
    if not agencies:
        agencies = []

    candidates = Candidate.objects.filter(
        assignments__employer__in=[a.id for a in agencies]
    ).distinct()

    context = {
        "agencies": agencies,
        "candidates": candidates[:10],
        "work_permits": WorkPermit.objects.filter(
            employer__in=[a.id for a in agencies]
        )[:10],
        "visa_apps": VisaApplication.objects.filter(
            candidate__in=candidates
        )[:10],
    }

    return render(request, "dashboards/agency_manager_dashboard.html", context)


# ----------------------------------------------------
# HTMX PARTIALS
# ----------------------------------------------------
#@login_required
def recent_candidates(request):
    candidates = Candidate.objects.order_by("-created_at")[:10]
    return render(request, "partials/recent_candidates.html", {"candidates": candidates})


#@login_required
def upcoming_interviews(request):
    interviews = Interview.objects.filter(
        scheduled_at__gte=timezone.now()
    ).order_by("scheduled_at")[:10]
    return render(request, "partials/upcoming_interviews.html", {"interviews": interviews})


#@login_required
def activity_feed(request):
    logs = AuditLog.objects.select_related("user").order_by("-created_at")[:15]
    return render(request, "partials/activity_feed.html", {"logs": logs})


# ----------------------------------------------------
# ROLE-RESTRICTED VIEWS
# ----------------------------------------------------
@login_required
def admin_only_view(request):
    if get_user_role(request.user) != "ADMIN":
        return HttpResponseForbidden("You do not have permission to access this page.")
    return render(request, "admin_only.html")


@login_required
def recruiter_only_view(request):
    if get_user_role(request.user) != "RECRUITER":
        return HttpResponseForbidden("Access denied.")
    return render(request, "recruiter_page.html")




# views.py
from django.shortcuts import render, get_object_or_404
from .models import (
    Candidate, CandidateDocument, Interview, InterviewAssessment,
    ERPPEnrollment, ERPPBatch, Contract, VisaApplication, WorkPermit
)

@login_required
def candidate_report(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)

    documents = candidate.documents.all()
    interviews = Interview.objects.filter(candidate=candidate)
    assessments = InterviewAssessment.objects.filter(interview__candidate=candidate)
    erpp = ERPPEnrollment.objects.filter(candidate=candidate).select_related("batch")
    contracts = Contract.objects.filter(candidate=candidate)
    visa_apps = VisaApplication.objects.filter(candidate=candidate)
    work_permits = WorkPermit.objects.filter(candidate=candidate)

    context = {
        "candidate": candidate,
        "documents": documents,
        "interviews": interviews,
        "assessments": assessments,
        "erpp": erpp,
        "contracts": contracts,
        "visa_apps": visa_apps,
        "work_permits": work_permits,
    }

    return render(request, "reports/candidate_report.html", context)


from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

@login_required
def candidate_report_pdf(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)

    documents = candidate.documents.all()
    interviews = Interview.objects.filter(candidate=candidate)
    assessments = InterviewAssessment.objects.filter(interview__candidate=candidate)
    erpp = ERPPEnrollment.objects.filter(candidate=candidate).select_related("batch")
    contracts = Contract.objects.filter(candidate=candidate)
    visa_apps = VisaApplication.objects.filter(candidate=candidate)
    work_permits = WorkPermit.objects.filter(candidate=candidate)

    context = {
        "candidate": candidate,
        "documents": documents,
        "interviews": interviews,
        "assessments": assessments,
        "erpp": erpp,
        "contracts": contracts,
        "visa_apps": visa_apps,
        "work_permits": work_permits,
    }

    html_string = render_to_string("reports/candidate_report_pdf.html", context)
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=candidate_{candidate_id}_report.pdf"
    return response
