from django.contrib.admin import AdminSite
from django.utils import timezone
from django.shortcuts import render
from .models import Candidate, Interview
from django.contrib.admin import AdminSite
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Count
from api.models import Candidate, Interview

class CustomAdminSite(AdminSite):
    site_header = "Recruitment Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
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

        if extra_context:
            context.update(extra_context)

        return render(request, "admin/index.html", context)
