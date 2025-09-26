
"""
نماذج التقييمات الذكية - مشروع نائبك

This module defines the data models for the Naebak ratings service. It includes models for rating categories, smart ratings (which incorporate business logic for displaying ratings), user-submitted ratings, rating reports, system-wide rating settings, and cached rating statistics.
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class RatingCategory(models.Model):
    """Represents a category for rating users (e.g., deputies).

    Each category has a weight, icon, and color, allowing for a customizable rating system.
    This model defines the different aspects that users can be evaluated on.

    Attributes:
        name (str): The name of the category (e.g., "Transparency and Integrity").
        name_en (str): The English name of the category.
        description (str): A detailed description of the category and what it represents.
        icon (str): A FontAwesome icon to visually represent the category.
        color (str): A HEX color code to visually distinguish the category.
        weight (float): The weight of the category in the overall rating calculation.
        is_active (bool): Whether the category is active and can be used for ratings.
        display_order (int): The order in which the category is displayed in the user interface.
        show_in_summary (bool): Whether this category appears in the summary of ratings.
        show_comments (bool): Whether users can add comments for this category.
    """
    
    name = models.CharField("اسم الفئة", max_length=100, unique=True)
    name_en = models.CharField("الاسم بالإنجليزية", max_length=100, blank=True)
    description = models.TextField("الوصف", blank=True)
    icon = models.CharField("الأيقونة", max_length=50, default="fas fa-star")
    color = models.CharField("اللون", max_length=7, default="#FFD700")
    weight = models.FloatField("الوزن في الحساب", default=1.0)
    is_active = models.BooleanField("نشط", default=True)
    display_order = models.PositiveIntegerField("ترتيب العرض", default=0)
    
    # Display settings
    show_in_summary = models.BooleanField("إظهار في الملخص", default=True)
    show_comments = models.BooleanField("إظهار التعليقات", default=True)
    
    # System timestamps
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)
    updated_at = models.DateTimeField("تاريخ التحديث", auto_now=True)
    
    class Meta:
        db_table = "rating_categories"
        verbose_name = "فئة تقييم"
        verbose_name_plural = "فئات التقييم"
        ordering = ["display_order", "name"]
    
    def __str__(self):
        return self.name
    
    @property
    def total_ratings(self):
        """Returns the total number of ratings in this category."""
        return self.ratings.count()


class SmartRating(models.Model):
    """Represents a "smart" rating that can be administratively controlled.

    This model allows administrators to blend real user ratings with a "fake" or curated rating.
    This is useful for seeding new users with a baseline rating or for adjusting ratings for promotional purposes.
    The `display_mode` attribute determines how the final rating is calculated and displayed.

    Attributes:
        rated_user (User): The user being rated.
        category (RatingCategory): The rating category.
        real_rating (float): The actual average rating from real users.
        real_count (int): The number of real user ratings.
        fake_rating (float): The administratively set "fake" rating.
        fake_count (int): The virtual number of raters for the fake rating.
        display_mode (str): The mode for displaying the rating. Can be one of:
            - `real`: Show only the real rating.
            - `fake`: Show only the fake rating.
            - `mixed`: A weighted average of real and fake ratings.
            - `weighted`: A weighted average based on the counts of real and fake ratings.
        real_weight (float): The weight of the real rating in `mixed` mode.
        fake_weight (float): The weight of the fake rating in `mixed` mode.
        is_active (bool): Whether this smart rating is active.
        show_count (bool): Whether to display the total count of raters.
        allow_new_ratings (bool): Whether to allow new user ratings for this category.
    """
    
    # The user being rated (e.g., a deputy or candidate)
    rated_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="smart_ratings",
        verbose_name="المستخدم المُقيَّم"
    )
    
    category = models.ForeignKey(
        RatingCategory,
        on_delete=models.CASCADE,
        related_name="smart_ratings",
        verbose_name="فئة التقييم"
    )
    
    # Real ratings
    real_rating = models.FloatField(
        "التقييم الحقيقي",
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    real_count = models.PositiveIntegerField("عدد المقيمين الحقيقي", default=0)
    
    # Modified ratings (controlled by administration)
    fake_rating = models.FloatField(
        "التقييم المعدل",
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=4.5
    )
    fake_count = models.PositiveIntegerField("العدد الافتراضي للمقيمين", default=1000)
    
    # Display settings
    display_mode = models.CharField(
        "نمط العرض",
        max_length=20,
        choices=[
            ("real", "التقييم الحقيقي فقط"),
            ("fake", "التقييم المعدل فقط"),
            ("mixed", "خليط ذكي"),
            ("weighted", "متوسط مرجح")
        ],
        default="mixed"
    )
    
    # Mixing weights (for mixed mode)
    real_weight = models.FloatField("وزن التقييم الحقيقي", default=0.3)  # 30%
    fake_weight = models.FloatField("وزن التقييم المعدل", default=0.7)   # 70%
    
    # Control settings
    is_active = models.BooleanField("نشط", default=True)
    show_count = models.BooleanField("إظهار عدد المقيمين", default=True)
    allow_new_ratings = models.BooleanField("السماح بتقييمات جديدة", default=True)
    
    # System timestamps
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)
    updated_at = models.DateTimeField("تاريخ التحديث", auto_now=True)
    
    class Meta:
        db_table = "smart_ratings"
        verbose_name = "تقييم ذكي"
        verbose_name_plural = "التقييمات الذكية"
        unique_together = ["rated_user", "category"]
        indexes = [
            models.Index(fields=["rated_user", "category"]),
            models.Index(fields=["display_mode"]),
            models.Index(fields=["is_active"]),
        ]
    
    def __str__(self):
        return f"تقييم {self.rated_user.get_full_name()} - {self.category.name}"
    
    def get_display_rating(self):
        """Calculates the rating to be displayed based on the display mode."""
        if self.display_mode == "real":
            return self.real_rating
        elif self.display_mode == "fake":
            return self.fake_rating
        elif self.display_mode == "mixed":
            if self.real_count == 0:
                return self.fake_rating
            return (self.real_rating * self.real_weight) + (self.fake_rating * self.fake_weight)
        elif self.display_mode == "weighted":
            total_count = self.real_count + self.fake_count
            if total_count == 0:
                return self.fake_rating
            return ((self.real_rating * self.real_count) + (self.fake_rating * self.fake_count)) / total_count
        return self.fake_rating
    
    def get_display_count(self):
        """Calculates the number of raters to be displayed."""
        if self.display_mode == "real":
            return self.real_count
        elif self.display_mode == "fake":
            return self.fake_count
        else:
            return self.real_count + self.fake_count


class Rating(models.Model):
    """Represents a single, real rating submitted by a citizen.

    This model stores the core rating data, including the rater, the rated user, the category,
    the rating value, and an optional comment. It also includes metadata for moderation and tracking.

    Attributes:
        id (UUID): The primary key for the rating.
        rater (User): The user who submitted the rating.
        rated_user (User): The user who was rated.
        category (RatingCategory): The category of the rating.
        rating (int): The rating value (1-5).
        comment (str): An optional comment from the rater.
        ip_address (str): The IP address of the rater.
        user_agent (str): The user agent of the rater's browser.
        is_verified (bool): Whether the rating has been verified (e.g., by email).
        is_public (bool): Whether the rating is publicly visible.
        is_reported (bool): Whether the rating has been reported for abuse.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Rater and rated user
    rater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_ratings",
        verbose_name="المقيِّم"
    )
    rated_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_ratings",
        verbose_name="المُقيَّم"
    )
    
    category = models.ForeignKey(
        RatingCategory,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="فئة التقييم"
    )
    
    # The rating
    rating = models.PositiveIntegerField(
        "التقييم",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Optional comment
    comment = models.TextField("التعليق", max_length=500, blank=True)
    
    # Additional information
    ip_address = models.GenericIPAddressField("عنوان IP", blank=True, null=True)
    user_agent = models.TextField("معلومات المتصفح", blank=True)
    
    # Rating status
    is_verified = models.BooleanField("تم التحقق", default=False)
    is_public = models.BooleanField("عام", default=True)
    is_reported = models.BooleanField("تم الإبلاغ عنه", default=False)
    
    # System timestamps
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)
    updated_at = models.DateTimeField("تاريخ التحديث", auto_now=True)
    
    class Meta:
        db_table = "ratings"
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"
        unique_together = ["rater", "rated_user", "category"]
        indexes = [
            models.Index(fields=["rated_user", "category"]),
            models.Index(fields=["rater"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_verified", "is_public"]),
        ]
    
    def __str__(self):
        return f"{self.rater.get_full_name()} قيّم {self.rated_user.get_full_name()} - {self.rating}/5"


class RatingReport(models.Model):
    """Represents a report against an abusive or inappropriate rating.

    This model is used for content moderation. Users can report ratings they believe are spam,
    fake, offensive, or otherwise inappropriate. Administrators can then review these reports
    and take action.

    Attributes:
        rating (Rating): The rating that was reported.
        reporter (User): The user who filed the report.
        report_type (str): The type of report (e.g., 'spam', 'offensive').
        description (str): A detailed description of the reason for the report.
        status (str): The status of the report (e.g., 'pending', 'reviewed').
        admin_notes (str): Notes from the administrator who reviewed the report.
        reviewed_by (User): The administrator who reviewed the report.
        reviewed_at (datetime): When the report was reviewed.
    """
    
    REPORT_TYPES = [
        ("spam", "رسائل مزعجة"),
        ("fake", "تقييم وهمي"),
        ("offensive", "محتوى مسيء"),
        ("inappropriate", "غير مناسب"),
        ("misleading", "مضلل"),
        ("other", "أخرى")
    ]
    
    STATUS_CHOICES = [
        ("pending", "قيد المراجعة"),
        ("reviewed", "تمت المراجعة"),
        ("resolved", "تم الحل"),
        ("rejected", "مرفوض")
    ]
    
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="التقييم"
    )
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rating_reports",
        verbose_name="المبلغ"
    )
    
    report_type = models.CharField("نوع البلاغ", max_length=20, choices=REPORT_TYPES)
    description = models.TextField("وصف البلاغ", max_length=1000)
    
    # Review information
    status = models.CharField("الحالة", max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_notes = models.TextField("ملاحظات الإدارة", blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_rating_reports",
        verbose_name="راجعه"
    )
    reviewed_at = models.DateTimeField("تاريخ المراجعة", blank=True, null=True)
    
    # System timestamps
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)
    
    class Meta:
        db_table = "rating_reports"
        verbose_name = "بلاغ تقييم"
        verbose_name_plural = "بلاغات التقييمات"
        unique_together = ["rating", "reporter"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["report_type"]),
            models.Index(fields=["created_at"]),
        ]
    
    def __str__(self):
        return f"بلاغ على تقييم {self.rating.id}"


class RatingSettings(models.Model):
    """A singleton model to store global settings for the rating system.

    This model ensures that there is only one set of rating settings for the entire application.
    The `get_settings` class method should be used to access the settings object.

    Attributes:
        enable_ratings (bool): Globally enable or disable the rating system.
        enable_comments (bool): Globally enable or disable comments on ratings.
        require_login (bool): Whether users must be logged in to submit a rating.
        max_ratings_per_user_per_day (int): The maximum number of ratings a user can submit per day.
        min_rating_interval_minutes (int): The minimum time a user must wait between ratings.
        max_comment_length (int): The maximum length of a comment.
        moderate_comments (bool): Whether new comments require administrative approval.
        default_display_mode (str): The default display mode for new smart ratings.
        default_fake_rating (float): The default fake rating for new smart ratings.
        default_fake_count (int): The default fake count for new smart ratings.
        default_real_weight (float): The default real weight for new smart ratings.
        default_fake_weight (float): The default fake weight for new smart ratings.
        enable_ip_tracking (bool): Whether to store the IP address of raters.
        block_duplicate_ips (bool): Whether to prevent multiple ratings from the same IP address.
        auto_verify_ratings (bool): Whether to automatically verify new ratings.
        notify_on_new_rating (bool): Whether to send a notification when a new rating is submitted.
        notify_on_report (bool): Whether to send a notification when a rating is reported.
    """
    
    # General settings
    enable_ratings = models.BooleanField("تفعيل التقييمات", default=True)
    enable_comments = models.BooleanField("تفعيل التعليقات", default=True)
    require_login = models.BooleanField("يتطلب تسجيل دخول", default=True)
    
    # Rating limits
    max_ratings_per_user_per_day = models.PositiveIntegerField("حد التقييمات اليومي", default=10)
    min_rating_interval_minutes = models.PositiveIntegerField("الحد الأدنى بين التقييمات (دقيقة)", default=5)
    
    # Comment settings
    max_comment_length = models.PositiveIntegerField("حد أحرف التعليق", default=500)
    moderate_comments = models.BooleanField("مراجعة التعليقات", default=True)
    
    # Default display settings
    default_display_mode = models.CharField(
        "نمط العرض الافتراضي",
        max_length=20,
        choices=[
            ("real", "التقييم الحقيقي فقط"),
            ("fake", "التقييم المعدل فقط"),
            ("mixed", "خليط ذكي"),
            ("weighted", "متوسط مرجح")
        ],
        default="mixed"
    )
    
    default_fake_rating = models.FloatField(
        "التقييم المعدل الافتراضي",
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=4.5
    )
    default_fake_count = models.PositiveIntegerField("العدد الافتراضي للمقيمين", default=1000)
    
    # Default weights for mixed mode
    default_real_weight = models.FloatField("وزن التقييم الحقيقي الافتراضي", default=0.3)
    default_fake_weight = models.FloatField("وزن التقييم المعدل الافتراضي", default=0.7)
    
    # Security settings
    enable_ip_tracking = models.BooleanField("تتبع عناوين IP", default=True)
    block_duplicate_ips = models.BooleanField("منع التقييمات المكررة من نفس IP", default=True)
    auto_verify_ratings = models.BooleanField("التحقق التلقائي من التقييمات", default=False)
    
    # Notification settings
    notify_on_new_rating = models.BooleanField("إشعار عند تقييم جديد", default=True)
    notify_on_report = models.BooleanField("إشعار عند بلاغ جديد", default=True)
    
    # System timestamps
    updated_at = models.DateTimeField("تاريخ التحديث", auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="حدثه"
    )
    
    class Meta:
        db_table = "rating_settings"
        verbose_name = "إعدادات التقييمات"
        verbose_name_plural = "إعدادات التقييمات"
    
    def __str__(self):
        return "إعدادات نظام التقييمات"
    
    def save(self, *args, **kwargs):
        # Ensure there is only one record
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Returns the current rating settings."""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class RatingStatistics(models.Model):
    """Caches and stores aggregated rating statistics for a user.

    This model is used to improve performance by avoiding expensive database queries
    to calculate statistics on the fly. The `update_stats` method should be called
    periodically to keep the statistics up-to-date.

    Attributes:
        user (User): The user for whom the statistics are being calculated.
        total_ratings_received (int): The total number of verified, public ratings received.
        average_rating (float): The average rating.
        ratings_1_star (int): The number of 1-star ratings.
        ratings_2_star (int): The number of 2-star ratings.
        ratings_3_star (int): The number of 3-star ratings.
        ratings_4_star (int): The number of 4-star ratings.
        ratings_5_star (int): The number of 5-star ratings.
        ratings_this_month (int): The number of ratings received in the current month.
        ratings_last_month (int): The number of ratings received in the previous month.
        last_updated (datetime): When the statistics were last updated.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="rating_stats",
        verbose_name="المستخدم"
    )
    
    # General statistics
    total_ratings_received = models.PositiveIntegerField("إجمالي التقييمات المستلمة", default=0)
    average_rating = models.FloatField("متوسط التقييم", default=0.0)
    
    # Rating distribution
    ratings_1_star = models.PositiveIntegerField("تقييمات نجمة واحدة", default=0)
    ratings_2_star = models.PositiveIntegerField("تقييمات نجمتان", default=0)
    ratings_3_star = models.PositiveIntegerField("تقييمات ثلاث نجوم", default=0)
    ratings_4_star = models.PositiveIntegerField("تقييمات أربع نجوم", default=0)
    ratings_5_star = models.PositiveIntegerField("تقييمات خمس نجوم", default=0)
    
    # Time-based statistics
    ratings_this_month = models.PositiveIntegerField("تقييمات هذا الشهر", default=0)
    ratings_last_month = models.PositiveIntegerField("تقييمات الشهر الماضي", default=0)
    
    # System timestamps
    last_updated = models.DateTimeField("آخر تحديث", auto_now=True)
    
    class Meta:
        db_table = "rating_statistics"
        verbose_name = "إحصائيات تقييم"
        verbose_name_plural = "إحصائيات التقييمات"
    
    def __str__(self):
        return f"إحصائيات {self.user.get_full_name()}"
    
    def update_stats(self):
        """Updates the rating statistics for the user."""
        ratings = Rating.objects.filter(
            rated_user=self.user,
            is_verified=True,
            is_public=True
        )
        
        self.total_ratings_received = ratings.count()
        if self.total_ratings_received > 0:
            self.average_rating = ratings.aggregate(avg=models.Avg("rating"))["avg"] or 0.0
            
            # Rating distribution
            self.ratings_1_star = ratings.filter(rating=1).count()
            self.ratings_2_star = ratings.filter(rating=2).count()
            self.ratings_3_star = ratings.filter(rating=3).count()
            self.ratings_4_star = ratings.filter(rating=4).count()
            self.ratings_5_star = ratings.filter(rating=5).count()
            
            # Time-based statistics
            from datetime import datetime, timedelta
            now = timezone.now()
            this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
            
            self.ratings_this_month = ratings.filter(created_at__gte=this_month_start).count()
            self.ratings_last_month = ratings.filter(
                created_at__gte=last_month_start,
                created_at__lt=this_month_start
            ).count()
        
        self.save()


class Governorate(models.Model):
    """Represents an Egyptian governorate.

    This model stores information about the governorates of Egypt, which can be used to
    associate users or other data with a specific geographical region.

    Attributes:
        name (str): The name of the governorate.
        name_en (str): The English name of the governorate.
        code (str): A unique code for the governorate.
        region (str): The region of Egypt where the governorate is located.
        capital (str): The capital city of the governorate.
        area_km2 (int): The area of the governorate in square kilometers.
    """
    
    name = models.CharField("اسم المحافظة", max_length=50, unique=True)
    name_en = models.CharField("الاسم بالإنجليزية", max_length=50, blank=True)
    code = models.CharField("الكود", max_length=10, unique=True)
    region = models.CharField(
        "المنطقة",
        max_length=20,
        choices=[
            ("cairo", "القاهرة الكبرى"),
            ("delta", "الدلتا"),
            ("canal", "القناة"),
            ("sinai", "سيناء"),
            ("upper", "الصعيد"),
            ("red_sea", "البحر الأحمر"),
            ("new_valley", "الوادي الجديد")
        ]
    )
    
    # Geographical information
    capital = models.CharField("العاصمة", max_length=50, blank=True)
    area_km2 = models.PositiveIntegerField("المساحة (كم²)", blank=True, null=True)
    
    class Meta:
        db_table = "governorates"
        verbose_name = "محافظة"
        verbose_name_plural = "المحافظات"
        ordering = ["name"]
        
    def __str__(self):
        return self.name

