from django.utils.html import format_html
from django.contrib import admin
from .models import Candidate, CandidateDocument, Interview, InterviewAssessment, Role,UserProfile
from django.contrib import admin
from .models import (
    ERPPBatch,
    Invoice,
    ERPPPayment,
    ERPPEnrollment,
    ERPPProgress,
    Agency,
    Employer,
    JobCategory,
    JobPosition,
    Contract,
    WorkPermit,
    ImmigrationProcess,
    VisaApplication,
    TravelAndSettlement,
)

from django.contrib import admin
from .models import (
    Candidate,
    ImmigrationProcess,
    VisaApplication,
    TravelAndSettlement,
)

# -------------------------
# Inlines
# -------------------------
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display=("name",)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=("user","role","created_at")
    list_filter=("user",)
    search_fields=("user__username","user__email")

class CandidateDocumentInline(admin.TabularInline):
    model = CandidateDocument
    extra = 1
    fields = ("doc_type", "number", "issue_date", "expiry_date", "file")
    show_change_link = True


class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 1
    show_change_link = True
    fields = ("scheduled_at", "location", "score", "result")


class InterviewAssessmentInline(admin.StackedInline):
    model = InterviewAssessment
    extra = 0
    can_delete = False
    max_num = 1
    readonly_fields = ("total_score", "final_classification")
    fields = (
        "parent_occupation",
        ("parents_deceased", "deceased_parent"),
        ("number_of_siblings", "birth_order"),
        ("has_work_experience", "work_experience_description"),
        ("has_volunteer_experience", "volunteer_description"),
        ("portuguese_rating", "english_rating"),
        ("interest_in_job", "attitude", "maturity"),
        ("motivation", "appearance", "confidence", "personality"),
        "total_score",
        "final_classification",
        ("martial_arts_member", "martial_arts_discipline"),
        "physically_fit",
    )

class ContractInline(admin.TabularInline):
    model=Contract
    extra=1
    can_delete=False
    max_num=1
    fields=("candidate", "employer", "contract_file", "issued_date","signed_date")

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("candidate", "employer", "contract_file", "issued_date","signed_date")



class ImmigrationProcessInline(admin.TabularInline):
    model = ImmigrationProcess
    extra = 1


class VisaApplicationInline(admin.TabularInline):
    model = VisaApplication
    extra = 1


class TravelAndSettlementInline(admin.StackedInline):
    model = TravelAndSettlement
    extra = 0
    max_num = 1  # because OneToOneField


# -------------------------
# Model Admins
# -------------------------

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("candidate", "scheduled_at", "location", "result", "score")
    list_filter = ("result", "location", "score")
    search_fields = ("candidate__first_name", "candidate__last_name", "candidate__candidate_id")
    inlines = [InterviewAssessmentInline]

from django.urls import reverse
from django.utils.html import format_html

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):

    list_display = (
        "candidate_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "district",
        "status",
        "report_link",
        "report_pdf_button",
    )

    def report_link(self, obj):
        url = reverse("api:candidate_report", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">View Report</a>',
            url
        )

    report_link.short_description = "Report"
    
    def report_pdf_button(self, obj):
        url = reverse("api:candidate_report_pdf", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">Download PDF</a>',
            url
        )
    report_pdf_button.short_description = "Download Report"

    search_fields = ("candidate_id", "first_name", "last_name", "email", "phone")
    list_filter = ("status", "gender", "district", "trades_courses", "english_level", "portuguese_level")

    readonly_fields = ("candidate_id",)
   fieldsets = (
    ("Basic Info", {
        "fields": (
            "candidate_id",
            ("first_name", "last_name"),
            ("date_of_birth","age", "gender", "height"),
            ("candidate_marital_status"),
            ("email", "phone"),
            ("district", "address"),
            ("father_full_name", "mother_full_name"),
            "total_siblings",
            "parent_marital_status",
        )
    }),
        ("Skills & Courses", {
            "fields": (
                "trades_courses",
                "lifeskilss_course",
                "health",
                ("english_level", "portuguese_level"),
            )
        }),
        ("Status", {"fields": ("status",)}),
    )

    # ✅ Both inlines here
    inlines = [CandidateDocumentInline, InterviewInline, ContractInline,ImmigrationProcessInline,
        VisaApplicationInline,
        TravelAndSettlementInline,]
    
   

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 1
    fields = ("invoice_number", "candidate", "amount", "due_date", "status")
    readonly_fields = ("invoice_number", "issue_date")
    show_change_link = True
class ERPPPaymentInline(admin.TabularInline):
    model = ERPPPayment
    extra = 1
    fields = ("candidate", "amount", "reference_number", "payment_date", "status")
    show_change_link = True

class ERPPEnrollmentInline(admin.TabularInline):
    model = ERPPEnrollment
    extra = 1
    fields = ("candidate", "payment", "status", "graduation_date")
    show_change_link = True

class ERPPProgressInline(admin.TabularInline):
    model = ERPPProgress
    extra = 1
    fields = ("module_name", "completed", "performance_score", "attendance", "notes")

@admin.register(ERPPBatch)
class ERPPBatchAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "max_participants")
    search_fields = ("name",)
    list_filter = ("start_date", "end_date")

    inlines = [
        InvoiceInline,
        ERPPPaymentInline,
        ERPPEnrollmentInline,
    ]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "candidate", "batch", "amount", "due_date", "status")
    search_fields = ("invoice_number", "candidate__first_name", "candidate__last_name")
    list_filter = ("status", "batch")

    readonly_fields = ("invoice_number", "issue_date")

    # inlines = [ERPPPaymentInline]

@admin.register(ERPPPayment)
class ERPPPaymentAdmin(admin.ModelAdmin):
    list_display = ("reference_number", "candidate", "batch", "amount", "payment_date", "status")
    search_fields = ("reference_number", "candidate__first_name", "candidate__last_name")
    list_filter = ("status", "batch")

@admin.register(ERPPEnrollment)
class ERPPEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("candidate", "batch", "status", "graduation_date")
    list_filter = ("status", "batch")
    search_fields = ("candidate__first_name", "candidate__last_name")

    # inlines = [ERPPProgressInline]

@admin.register(ERPPProgress)
class ERPPProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "module_name", "completed", "performance_score", "attendance")
    list_filter = ("completed", "attendance")



class AgencyInline(admin.TabularInline):
    model = Agency
    extra = 1
    fields = ("name", "type", "manager")
    readonly_fields = ( "type")
    show_change_link = True
@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "manager", "contact_email", "contact_phone")
    list_filter = ("name", "manager")
   

# -----------------------------
# INLINE DEFINITIONS
# -----------------------------

# -----------------------------
# CANDIDATE ADMIN
# -----------------------------

# @admin.register(Candidate)
# class CandidateAdmin(admin.ModelAdmin):
#     list_display = ("candidate_id", "first_name", "last_name", "status", "created_at")
#     search_fields = ("candidate_id", "first_name", "last_name", "email")
#     list_filter = ("status", "district", "gender")

#     inlines = [
#         ImmigrationProcessInline,
#         VisaApplicationInline,
#         TravelAndSettlementInline,
#     ]


from .custom_admin import CustomAdminSite
from .models import Candidate, Interview

admin_site = CustomAdminSite(name="custom_admin")

admin_site.register(Candidate)
admin_site.register(Interview)
