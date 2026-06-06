
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
import uuid
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    class Meta:
        abstract = True


class Candidate(TimeStampedModel):
    class Status(models.TextChoices):
                # Registration Phase
            REGISTERED = "REGISTERED"
            INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
            INTERVIEW_PASSED = "INTERVIEW_PASSED"
            INTERVIEW_FAILED = "INTERVIEW_FAILED"

            # Training Phase
            ERPP_ENROLLED = "ERPP_ENROLLED"
            ERPP_COMPLETED = "ERPP_COMPLETED"
            ERPP_DROPPED = "ERPP_DROPPED"

            # Placement Phase
            POOL_READY = "POOL_READY"
            MATCHED = "MATCHED"
            CONTRACT_SIGNED = "CONTRACT_SIGNED"

            # Government Phase
            WORK_PERMIT_SUBMITTED = "WORK_PERMIT_SUBMITTED"
            WORK_PERMIT_APPROVED = "WORK_PERMIT_APPROVED"
            WORK_PERMIT_REJECTED = "WORK_PERMIT_REJECTED"

            VISA_SUBMITTED = "VISA_SUBMITTED"
            VISA_APPROVED = "VISA_APPROVED"
            VISA_REJECTED = "VISA_REJECTED"

            # Travel & Settlement
            ARRIVED = "ARRIVED"
            SETTLED = "SETTLED"

            # Terminal
            WITHDRAWN = "WITHDRAWN"
    class MaritalStatus(models.TextChoices):
        SINGLE = "SINGLE", "Single"
        MARRIED = "MARRIED", "Married"
        WIDOW = "WIDOW", "Widow"
    

    class GenderChoices(models.TextChoices):
        MALE = "MALE","Male"
        FEMALE = "FEMALE","Female"
    class DistrictChoices(models.TextChoices):
        Aileu = "Aileu"
        AINARO = "Ainaro"
        BAUCAU = "Baucau"
        BOBONARO = "Bobonaro"
        DILI = "Dili"
        ERMERA="Ermera"
        LIQUICA = "Liquica"
        LAUTEM="Lautem"
        MANATUTO="Manatuto"
        SAME= "SAME"
        SUAI="Suai"
        OECUSSE="Oecussi"
        VIQUEQUE="Viqueque"

    class TradeChoices(models.TextChoices):
        Barista="Barista"
        Carpinter="Carpinter"
        Electrician="Electrician"
        Plumber="Plumber"
    class Languageschoices(models.TextChoices):
        A1="Basic"
        B1="Intermediate"
        C1="Advanced"
        
           
    candidate_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=30, choices=GenderChoices, default=GenderChoices.FEMALE)
    height=models.IntegerField(default=0, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    district=models.CharField(max_length=30, choices=DistrictChoices, default=DistrictChoices.Aileu)
    address = models.CharField(max_length=150, null=True, blank=True)

    # Extra profile fields
    trades_courses = models.CharField(max_length=50, choices=TradeChoices, default=TradeChoices.Barista)
    lifeskilss_course=models.CharField(max_length=100, blank=True, null=True)
    # health_status = models.CharField(max_length=255, blank=True)
    health=models.CharField(max_length=100, null=True, blank=True)

    # Language levels
    english_level = models.CharField(max_length=50, choices=Languageschoices, blank=True)
    portuguese_level = models.CharField(max_length=50, choices=Languageschoices, blank=True)
    
      # NEW FIELDS
    father_full_name = models.CharField(
    max_length=100,
    null=True,
    blank=True,
    verbose_name="Father's full name"
)
    mother_full_name = models.CharField(
    max_length=100,
    null=True,
    blank=True,
    verbose_name="Mother's full name"
)
    total_siblings = models.PositiveIntegerField(default=0)
     # Parent marital status
    parent_marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatus.choices,
        default=MaritalStatus.MARRIED
    )


    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.REGISTERED,
    )
    def save(self, *args, **kwargs):
        if not self.candidate_id:
            now = timezone.now()
            prefix = f"Tofta{now.year}{now.month:02d}"
            # Find the highest existing number
            last = Candidate.objects.filter(candidate_id__startswith=prefix).order_by('-candidate_id').first()
            if last:
                last_num = int(last.candidate_id[-3:])
                new_num = last_num + 1
            else:
                new_num = 1

            self.candidate_id = f"{prefix}{new_num:03d}"

        super().save(*args, **kwargs)
    def __str__(self):

        return f"{self.candidate_id} - {self.first_name} {self.last_name}"
    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"


class CandidateDocument(TimeStampedModel):
    class DocType(models.TextChoices):
        PASSPORT = "PASSPORT", "Passport"
        BI = "BI", "BI"
        NIF = "NIF", "NIF"
        NISS = "NISS", "NISS"
        UTENTE= "UTENTE", "UTENTE"
        TdR="TdR","TdR"
        CC="CC","CC"
        CRIMINAL_RECORD = "CRIMINAL_RECORD", "Criminal Record"
        BIRTH_CERT = "BIRTH_CERT", "Birth Certificate"
        DRIVERS_LICENSE = "DRIVERS_LICENSE", "Driver License"

        OTHER = "OTHER", "Other"


    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=50, choices=DocType.choices)
    number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to="candidate_documents/", blank=True, null=True)

class Interview(TimeStampedModel):

    class Result(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PASS = "PASS", "Pass"
        FAIL = "FAIL", "Fail"
        NO_SHOW = "NO_SHOW", "No Show"

    class Location(models.TextChoices):
        REMOTE = "Online"
        OFFICE = "Offline"

    # ✅ Add ScoreLevel here — inside the model, alongside other enums
    class ScoreLevel(models.IntegerChoices):
        POOR = 1, "Poor"
        BELOW_AVERAGE = 2, "Below Average"
        AVERAGE = 3, "Average"
        GOOD = 4, "Good"
        EXCELLENT = 5, "Excellent"

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="interviews",
        null=True,
        blank=True
    )

    scheduled_at = models.DateTimeField(null=True, blank=True)

    location = models.CharField(
        max_length=20,
        choices=Location.choices,
        null=True,
        blank=True
    )

    # ✅ Add the score field here
    score = models.IntegerField(
        choices=ScoreLevel.choices,
        null=True,
        blank=True
    )

    result = models.CharField(
        max_length=20,
        choices=Result.choices,
        default=Result.PENDING
    )

    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.candidate and self.candidate.email:
            try:
                self.send_invitation_email()
            except Exception as e:
                print("Email sending failed:", e)

    def send_invitation_email(self):
        send_mail(
            subject="Your Interview Schedule",
            message=(
                f"Dear {self.candidate.first_name},\n\n"
                f"You have been scheduled for an interview on {self.scheduled_at}.\n"
                f"Location: {self.location}\n\n"
                "Best regards,\nRecruitment Team"
            ),
            from_email="no-reply@yourcompany.com",
            recipient_list=[self.candidate.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"Interview for {self.candidate} on {self.scheduled_at}"



class ERPPBatch(TimeStampedModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    max_participants = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "ERPPBatch"
        verbose_name_plural = "ERPPBatches"

class Invoice(TimeStampedModel):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ISSUED = "ISSUED", "Issued"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"

    invoice_number = models.CharField(max_length=50, unique=True, editable=False)

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    batch = models.ForeignKey(
        ERPPBatch,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    issue_date = models.DateField(auto_now_add=True)

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    pdf = models.FileField(upload_to="invoices/", blank=True, null=True)

    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class ERPPPayment(TimeStampedModel):
    
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="payments",
        blank=True,
        null=True
    )
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="erpp_payments"
    )

    batch = models.ForeignKey(
        ERPPBatch,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    reference_number = models.CharField(max_length=120, unique=True)

    payment_date = models.DateTimeField(null=True, blank=True)

    receipt = models.FileField(upload_to="erpp_receipts/", blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )


class ERPPEnrollment(TimeStampedModel):

    class Status(models.TextChoices):
        ENROLLED = "ENROLLED", "Enrolled"
        COMPLETED = "COMPLETED", "Completed"
        DROPPED = "DROPPED", "Dropped"

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="erpp_enrollments"
    )

    batch = models.ForeignKey(
        ERPPBatch,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    payment = models.OneToOneField(
        ERPPPayment,
        on_delete=models.PROTECT,
        related_name="enrollment",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ENROLLED
    )

    completion_certificate = models.FileField(
        upload_to="erpp_certificates/",
        null=True,
        blank=True
    )

    graduation_date = models.DateField(null=True, blank=True)


class ERPPProgress(TimeStampedModel):
    enrollment = models.ForeignKey(ERPPEnrollment, on_delete=models.CASCADE, related_name="progress_records")
    module_name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    performance_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    attendance = models.BooleanField(default=True)
    notes = models.TextField(blank=True)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Admin, Job Matching Officer, Agency Manager

    def __str__(self):
        return self.name


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.role}"


class Agency(TimeStampedModel):
    class Type(models.TextChoices):
        TEMPORARY = "TEMPORARY", "Temporary Work Permit"
        PERMANENT = "PERMANENT", "Permanent Work Permit"

    name = models.CharField(max_length=255)
    agency_type = models.CharField(max_length=20, choices=Type.choices)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_agencies"
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Agency"
        verbose_name_plural = "Agencies"


class Employer(TimeStampedModel):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class JobCategory(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "JobCategory"
        verbose_name_plural = "JobCategories"


class JobPosition(TimeStampedModel):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="positions")
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    required_skills = models.TextField(blank=True)
    available_positions = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} - {self.employer.name}"


class JobMatching(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="assignments")
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="assignments")
    job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_date = models.DateField()
    notes = models.TextField(blank=True)


class Contract(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="contracts")
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="contracts")
    contract_file = models.FileField(upload_to="contracts/", null=True, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    signed_date = models.DateField(null=True, blank=True)


class WorkPermit(TimeStampedModel):
    class Status(models.TextChoices):
        INITIATED = "INITIATED", "Initiated"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="work_permits")
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="work_permits")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIATED)
    application_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)


class ImmigrationProcess(TimeStampedModel):
    class FundingType(models.TextChoices):
        SELF_FUNDED = "SELF_FUNDED", "Self-funded"
        BANK_LOAN = "BANK_LOAN", "Bank-loan funded"
        

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="immigration_processes")
    visa_application_initiated = models.BooleanField(default=False)
    funding_type = models.CharField(max_length=20, choices=FundingType.choices, blank=True)
    lodge_application = models.BooleanField(default=False)
    passed = models.BooleanField(null=True, blank=True)
    notes = models.TextField(blank=True)


class VisaApplication(TimeStampedModel):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved"
        FAILED = "FAILED", "Failed"

    class VisaType(models.TextChoices):
        CPLP = "CPLP", "CPLP"
        OTHER = "OTHER", "Other"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="visa_applications")
    visa_type = models.CharField(max_length=20, choices=VisaType.choices, default=VisaType.CPLP)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    visa_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    country_of_issuance = models.CharField(max_length=100, blank=True)
    documents = models.FileField(upload_to="visa_documents/", null=True, blank=True)


class TravelAndSettlement(TimeStampedModel):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name="settlement")
    ticket_purchased = models.BooleanField(default=False)
    ticket_details = models.TextField(blank=True)
    nif_appointment_date = models.DateField(null=True, blank=True)
    transport_scheduled = models.BooleanField(default=False)
    accommodation_identified = models.BooleanField(default=False)
    accommodation_details = models.TextField(blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    flight_details = models.TextField(blank=True)
    nif_obtained = models.BooleanField(default=False)
    niss_obtained = models.BooleanField(default=False)
    employment_contract_signed = models.BooleanField(default=False)
    docs_ready_for_aima = models.BooleanField(default=False)


class AuditLog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    object_id = models.CharField(max_length=100)
    changes = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

class InterviewAssessment(models.Model):

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE,
        related_name="assessments",
        null=True,
        blank=True,
    )
    interview = models.OneToOneField(
    "Interview",
    on_delete=models.CASCADE,
    related_name="assessment",
    null=True,
    blank=True,
)
    # 2. Parental Information
    parent_occupation = models.CharField(max_length=255, blank=True)

    PARENT_CHOICES = [
        ("mother", "Mother"),
        ("father", "Father"),
        ("both", "Both"),
    ]

    parents_deceased = models.BooleanField(default=False)
    deceased_parent = models.CharField(
        max_length=10,
        choices=PARENT_CHOICES,
        blank=True,
        null=True
    )

    # 3. Siblings
    number_of_siblings = models.PositiveIntegerField(default=0)
    birth_order = models.PositiveIntegerField(null=True, blank=True)

    # 4. Work Experience
    has_work_experience = models.BooleanField(default=False)
    work_experience_description = models.TextField(blank=True)

    # 5. Volunteer Experience
    has_volunteer_experience = models.BooleanField(default=False)
    volunteer_description = models.TextField(blank=True)

    # 6. Language Ratings
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    portuguese_rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    english_rating = models.IntegerField(choices=RATING_CHOICES, default=1)

    # 7. General Assessment
    interest_in_job = models.IntegerField(choices=RATING_CHOICES, default=1)
    attitude = models.IntegerField(choices=RATING_CHOICES, default=1)
    maturity = models.IntegerField(choices=RATING_CHOICES, default=1)
    motivation = models.IntegerField(choices=RATING_CHOICES, default=1)
    appearance = models.IntegerField(choices=RATING_CHOICES, default=1)
    confidence = models.IntegerField(choices=RATING_CHOICES, default=1)
    personality = models.IntegerField(choices=RATING_CHOICES, default=1)

    total_score = models.IntegerField(default=0)
    final_classification = models.CharField(max_length=150, blank=True)

    # 8. Martial Arts
    martial_arts_member = models.BooleanField(default=False)
    martial_arts_discipline = models.CharField(max_length=100, blank=True)

    # 9. Fitness
    physically_fit = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.total_score = (
            self.interest_in_job +
            self.attitude +
            self.maturity +
            self.motivation +
            self.appearance +
            self.confidence +
            self.personality
        )

        if self.total_score <= 15:
            self.final_classification = "Not a good fit"
        elif 16 <= self.total_score <= 25:
            self.final_classification = "Potential candidate"
        else:
            self.final_classification = "Strong candidate"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Assessment - {self.interview.candidate}"

    def get_absolute_url(self):
        return reverse("api:assessment_detail", kwargs={"pk": self.pk})
    
