from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

#from .custom_admin import CustomAdminSite
from .custom_admin import custom_admin_site

# -------------------------
# MODELS
# -------------------------
from .models import (
    Candidate,
    CandidateDocument,
    Interview,
    InterviewAssessment,
    Role,
    UserProfile,
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

# -------------------------
# INLINE DEFINITIONS
# -------------------------

class CandidateDocumentInline(admin.TabularInline):
    model = CandidateDocument
    extra = 1
    fields = ("doc_type", "number", "issue_date", "expiry_date", "file")
    show_change_link = True


class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 1
    fields = ("scheduled_at", "location", "score", "result")
    show_change_link = True


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
    model = Contract
    extra = 1
    can_delete = False
    max_num = 1
    fields = ("candidate", "employer", "contract_file", "issued_date", "signed_date")


class ImmigrationProcessInline(admin.TabularInline):
    model = ImmigrationProcess
    extra = 1


class VisaApplicationInline(admin.TabularInline):
    model = VisaApplication
    extra = 1


class TravelAndSettlementInline(admin.StackedInline):
    model = TravelAndSettlement
    extra = 0
    max_num = 1


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


# -------------------------
# MODEL ADMINS
# -------------------------

class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "created_at")
    list_filter = ("user",)
    search_fields = ("user__username", "user__email")


class InterviewAdmin(admin.ModelAdmin):
    list_display = ("candidate", "scheduled_at", "location", "result", "score")
    list_filter = ("result", "location", "score")
    search_fields = ("candidate__first_name", "candidate__last_name", "candidate__candidate_id")
    inlines = [InterviewAssessmentInline]


class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "candidate_id",
        "first_name",
        "last_name",
        "age",
        "email",
        "phone",
        "district",
        "status",
        "report_link",
        "report_pdf_button",
    )

    search_fields = ("candidate_id", "first_name", "last_name", "email", "phone")
    list_filter = ("status", "gender", "district", "trades_courses", "english_level", "portuguese_level")
    readonly_fields = ("candidate_id","age",)

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

    inlines = [
        CandidateDocumentInline,
        InterviewInline,
        ContractInline,
        ImmigrationProcessInline,
        VisaApplicationInline,
        TravelAndSettlementInline,
    ]

    def report_link(self, obj):
        url = reverse("api:candidate_report", args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">View Report</a>', url)

    def report_pdf_button(self, obj):
        url = reverse("api:candidate_report_pdf", args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">Download PDF</a>', url)


class ContractAdmin(admin.ModelAdmin):
    list_display = ("candidate", "employer", "contract_file", "issued_date", "signed_date")


class ERPPBatchAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "max_participants")
    search_fields = ("name",)
    list_filter = ("start_date", "end_date")
    inlines = [InvoiceInline, ERPPPaymentInline, ERPPEnrollmentInline]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "candidate", "batch", "amount", "due_date", "status")
    search_fields = ("invoice_number", "candidate__first_name", "candidate__last_name")
    list_filter = ("status", "batch")
    readonly_fields = ("invoice_number", "issue_date")


class ERPPPaymentAdmin(admin.ModelAdmin):
    list_display = ("reference_number", "candidate", "batch", "amount", "payment_date", "status")
    search_fields = ("reference_number", "candidate__first_name", "candidate__last_name")
    list_filter = ("status", "batch")


class ERPPEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("candidate", "batch", "status", "graduation_date")
    list_filter = ("status", "batch")
    search_fields = ("candidate__first_name", "candidate__last_name")


class ERPPProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "module_name", "completed", "performance_score", "attendance")
    list_filter = ("completed", "attendance")


class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "manager", "contact_email", "contact_phone")
    list_filter = ("name", "manager")


# -------------------------
# REGISTER MODELS ON CUSTOM ADMIN SITE ONLY
# -------------------------

custom_admin_site.register(Role, RoleAdmin)
custom_admin_site.register(UserProfile, UserProfileAdmin)
custom_admin_site.register(Candidate, CandidateAdmin)
custom_admin_site.register(Interview, InterviewAdmin)
custom_admin_site.register(Contract, ContractAdmin)
custom_admin_site.register(ERPPBatch, ERPPBatchAdmin)
custom_admin_site.register(Invoice, InvoiceAdmin)
custom_admin_site.register(ERPPPayment, ERPPPaymentAdmin)
custom_admin_site.register(ERPPEnrollment, ERPPEnrollmentAdmin)
custom_admin_site.register(ERPPProgress, ERPPProgressAdmin)
custom_admin_site.register(Agency, AgencyAdmin)
