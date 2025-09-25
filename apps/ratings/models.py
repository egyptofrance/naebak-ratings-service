"""
نماذج التقييمات الذكية - مشروع نائبك
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class RatingCategory(models.Model):
    """فئات التقييم"""
    
    name = models.CharField('اسم الفئة', max_length=100, unique=True)
    name_en = models.CharField('الاسم بالإنجليزية', max_length=100, blank=True)
    description = models.TextField('الوصف', blank=True)
    icon = models.CharField('الأيقونة', max_length=50, default='fas fa-star')
    color = models.CharField('اللون', max_length=7, default='#FFD700')
    weight = models.FloatField('الوزن في الحساب', default=1.0)
    is_active = models.BooleanField('نشط', default=True)
    display_order = models.PositiveIntegerField('ترتيب العرض', default=0)
    
    # إعدادات العرض
    show_in_summary = models.BooleanField('إظهار في الملخص', default=True)
    show_comments = models.BooleanField('إظهار التعليقات', default=True)
    
    # تواريخ النظام
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        db_table = 'rating_categories'
        verbose_name = 'فئة تقييم'
        verbose_name_plural = 'فئات التقييم'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def total_ratings(self):
        """إجمالي التقييمات في هذه الفئة"""
        return self.ratings.count()


class SmartRating(models.Model):
    """التقييمات الذكية - التحكم الإداري"""
    
    # المستخدم المُقيَّم (نائب أو مرشح)
    rated_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='smart_ratings',
        verbose_name='المستخدم المُقيَّم'
    )
    
    category = models.ForeignKey(
        RatingCategory,
        on_delete=models.CASCADE,
        related_name='smart_ratings',
        verbose_name='فئة التقييم'
    )
    
    # التقييمات الحقيقية
    real_rating = models.FloatField(
        'التقييم الحقيقي',
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    real_count = models.PositiveIntegerField('عدد المقيمين الحقيقي', default=0)
    
    # التقييمات المعدلة (يتحكم بها الإدارة)
    fake_rating = models.FloatField(
        'التقييم المعدل',
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=4.5
    )
    fake_count = models.PositiveIntegerField('العدد الافتراضي للمقيمين', default=1000)
    
    # إعدادات العرض
    display_mode = models.CharField(
        'نمط العرض',
        max_length=20,
        choices=[
            ('real', 'التقييم الحقيقي فقط'),
            ('fake', 'التقييم المعدل فقط'),
            ('mixed', 'خليط ذكي'),
            ('weighted', 'متوسط مرجح')
        ],
        default='mixed'
    )
    
    # نسب الخلط (للنمط المختلط)
    real_weight = models.FloatField('وزن التقييم الحقيقي', default=0.3)  # 30%
    fake_weight = models.FloatField('وزن التقييم المعدل', default=0.7)   # 70%
    
    # إعدادات التحكم
    is_active = models.BooleanField('نشط', default=True)
    show_count = models.BooleanField('إظهار عدد المقيمين', default=True)
    allow_new_ratings = models.BooleanField('السماح بتقييمات جديدة', default=True)
    
    # تواريخ النظام
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        db_table = 'smart_ratings'
        verbose_name = 'تقييم ذكي'
        verbose_name_plural = 'التقييمات الذكية'
        unique_together = ['rated_user', 'category']
        indexes = [
            models.Index(fields=['rated_user', 'category']),
            models.Index(fields=['display_mode']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"تقييم {self.rated_user.get_full_name()} - {self.category.name}"
    
    def get_display_rating(self):
        """حساب التقييم المعروض حسب النمط"""
        if self.display_mode == 'real':
            return self.real_rating
        elif self.display_mode == 'fake':
            return self.fake_rating
        elif self.display_mode == 'mixed':
            if self.real_count == 0:
                return self.fake_rating
            return (self.real_rating * self.real_weight) + (self.fake_rating * self.fake_weight)
        elif self.display_mode == 'weighted':
            total_count = self.real_count + self.fake_count
            if total_count == 0:
                return self.fake_rating
            return ((self.real_rating * self.real_count) + (self.fake_rating * self.fake_count)) / total_count
        return self.fake_rating
    
    def get_display_count(self):
        """حساب عدد المقيمين المعروض"""
        if self.display_mode == 'real':
            return self.real_count
        elif self.display_mode == 'fake':
            return self.fake_count
        else:
            return self.real_count + self.fake_count


class Rating(models.Model):
    """التقييمات الحقيقية من المواطنين"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # المقيِّم والمُقيَّم
    rater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_ratings',
        verbose_name='المقيِّم'
    )
    rated_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_ratings',
        verbose_name='المُقيَّم'
    )
    
    category = models.ForeignKey(
        RatingCategory,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='فئة التقييم'
    )
    
    # التقييم
    rating = models.PositiveIntegerField(
        'التقييم',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # تعليق اختياري
    comment = models.TextField('التعليق', max_length=500, blank=True)
    
    # معلومات إضافية
    ip_address = models.GenericIPAddressField('عنوان IP', blank=True, null=True)
    user_agent = models.TextField('معلومات المتصفح', blank=True)
    
    # حالة التقييم
    is_verified = models.BooleanField('تم التحقق', default=False)
    is_public = models.BooleanField('عام', default=True)
    is_reported = models.BooleanField('تم الإبلاغ عنه', default=False)
    
    # تواريخ النظام
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        db_table = 'ratings'
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقييمات'
        unique_together = ['rater', 'rated_user', 'category']
        indexes = [
            models.Index(fields=['rated_user', 'category']),
            models.Index(fields=['rater']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_verified', 'is_public']),
        ]
    
    def __str__(self):
        return f"{self.rater.get_full_name()} قيّم {self.rated_user.get_full_name()} - {self.rating}/5"


class RatingReport(models.Model):
    """الإبلاغ عن التقييمات المسيئة"""
    
    REPORT_TYPES = [
        ('spam', 'رسائل مزعجة'),
        ('fake', 'تقييم وهمي'),
        ('offensive', 'محتوى مسيء'),
        ('inappropriate', 'غير مناسب'),
        ('misleading', 'مضلل'),
        ('other', 'أخرى')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('reviewed', 'تمت المراجعة'),
        ('resolved', 'تم الحل'),
        ('rejected', 'مرفوض')
    ]
    
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='التقييم'
    )
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rating_reports',
        verbose_name='المبلغ'
    )
    
    report_type = models.CharField('نوع البلاغ', max_length=20, choices=REPORT_TYPES)
    description = models.TextField('وصف البلاغ', max_length=1000)
    
    # معلومات المراجعة
    status = models.CharField('الحالة', max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField('ملاحظات الإدارة', blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_rating_reports',
        verbose_name='راجعه'
    )
    reviewed_at = models.DateTimeField('تاريخ المراجعة', blank=True, null=True)
    
    # تواريخ النظام
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    
    class Meta:
        db_table = 'rating_reports'
        verbose_name = 'بلاغ تقييم'
        verbose_name_plural = 'بلاغات التقييمات'
        unique_together = ['rating', 'reporter']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['report_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"بلاغ على تقييم {self.rating.id}"


class RatingSettings(models.Model):
    """إعدادات نظام التقييمات"""
    
    # إعدادات عامة
    enable_ratings = models.BooleanField('تفعيل التقييمات', default=True)
    enable_comments = models.BooleanField('تفعيل التعليقات', default=True)
    require_login = models.BooleanField('يتطلب تسجيل دخول', default=True)
    
    # حدود التقييم
    max_ratings_per_user_per_day = models.PositiveIntegerField('حد التقييمات اليومي', default=10)
    min_rating_interval_minutes = models.PositiveIntegerField('الحد الأدنى بين التقييمات (دقيقة)', default=5)
    
    # إعدادات التعليقات
    max_comment_length = models.PositiveIntegerField('حد أحرف التعليق', default=500)
    moderate_comments = models.BooleanField('مراجعة التعليقات', default=True)
    
    # إعدادات العرض الافتراضية
    default_display_mode = models.CharField(
        'نمط العرض الافتراضي',
        max_length=20,
        choices=[
            ('real', 'التقييم الحقيقي فقط'),
            ('fake', 'التقييم المعدل فقط'),
            ('mixed', 'خليط ذكي'),
            ('weighted', 'متوسط مرجح')
        ],
        default='mixed'
    )
    
    default_fake_rating = models.FloatField(
        'التقييم المعدل الافتراضي',
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=4.5
    )
    default_fake_count = models.PositiveIntegerField('العدد الافتراضي للمقيمين', default=1000)
    
    # أوزان النمط المختلط
    default_real_weight = models.FloatField('وزن التقييم الحقيقي الافتراضي', default=0.3)
    default_fake_weight = models.FloatField('وزن التقييم المعدل الافتراضي', default=0.7)
    
    # إعدادات الأمان
    enable_ip_tracking = models.BooleanField('تتبع عناوين IP', default=True)
    block_duplicate_ips = models.BooleanField('منع التقييمات المكررة من نفس IP', default=True)
    auto_verify_ratings = models.BooleanField('التحقق التلقائي من التقييمات', default=False)
    
    # إعدادات الإشعارات
    notify_on_new_rating = models.BooleanField('إشعار عند تقييم جديد', default=True)
    notify_on_report = models.BooleanField('إشعار عند بلاغ جديد', default=True)
    
    # تواريخ النظام
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='حدثه'
    )
    
    class Meta:
        db_table = 'rating_settings'
        verbose_name = 'إعدادات التقييمات'
        verbose_name_plural = 'إعدادات التقييمات'
    
    def __str__(self):
        return "إعدادات نظام التقييمات"
    
    def save(self, *args, **kwargs):
        # التأكد من وجود سجل واحد فقط
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """الحصول على الإعدادات الحالية"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class RatingStatistics(models.Model):
    """إحصائيات التقييمات (للتخزين المؤقت)"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='rating_stats',
        verbose_name='المستخدم'
    )
    
    # إحصائيات عامة
    total_ratings_received = models.PositiveIntegerField('إجمالي التقييمات المستلمة', default=0)
    average_rating = models.FloatField('متوسط التقييم', default=0.0)
    
    # توزيع التقييمات
    ratings_1_star = models.PositiveIntegerField('تقييمات نجمة واحدة', default=0)
    ratings_2_star = models.PositiveIntegerField('تقييمات نجمتان', default=0)
    ratings_3_star = models.PositiveIntegerField('تقييمات ثلاث نجوم', default=0)
    ratings_4_star = models.PositiveIntegerField('تقييمات أربع نجوم', default=0)
    ratings_5_star = models.PositiveIntegerField('تقييمات خمس نجوم', default=0)
    
    # إحصائيات زمنية
    ratings_this_month = models.PositiveIntegerField('تقييمات هذا الشهر', default=0)
    ratings_last_month = models.PositiveIntegerField('تقييمات الشهر الماضي', default=0)
    
    # تواريخ النظام
    last_updated = models.DateTimeField('آخر تحديث', auto_now=True)
    
    class Meta:
        db_table = 'rating_statistics'
        verbose_name = 'إحصائيات تقييم'
        verbose_name_plural = 'إحصائيات التقييمات'
    
    def __str__(self):
        return f"إحصائيات {self.user.get_full_name()}"
    
    def update_stats(self):
        """تحديث الإحصائيات"""
        ratings = Rating.objects.filter(
            rated_user=self.user,
            is_verified=True,
            is_public=True
        )
        
        self.total_ratings_received = ratings.count()
        if self.total_ratings_received > 0:
            self.average_rating = ratings.aggregate(avg=models.Avg('rating'))['avg'] or 0.0
            
            # توزيع التقييمات
            self.ratings_1_star = ratings.filter(rating=1).count()
            self.ratings_2_star = ratings.filter(rating=2).count()
            self.ratings_3_star = ratings.filter(rating=3).count()
            self.ratings_4_star = ratings.filter(rating=4).count()
            self.ratings_5_star = ratings.filter(rating=5).count()
            
            # إحصائيات زمنية
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
    """المحافظات المصرية"""
    
    name = models.CharField('اسم المحافظة', max_length=50, unique=True)
    name_en = models.CharField('الاسم بالإنجليزية', max_length=50, blank=True)
    code = models.CharField('الكود', max_length=10, unique=True)
    region = models.CharField(
        'المنطقة',
        max_length=20,
        choices=[
            ('cairo', 'القاهرة الكبرى'),
            ('delta', 'الدلتا'),
            ('canal', 'القناة'),
            ('sinai', 'سيناء'),
            ('upper', 'الصعيد'),
            ('red_sea', 'البحر الأحمر'),
            ('new_valley', 'الوادي الجديد')
        ]
    )
    
    # معلومات جغرافية
    capital = models.CharField('العاصمة', max_length=50, blank=True)
    area_km2 = models.PositiveIntegerField('المساحة (كم²)', blank=True, null=True)
    population = models.PositiveIntegerField('عدد السكان', blank=True, null=True)
    
    # إعدادات العرض
    is_active = models.BooleanField('نشط', default=True)
    display_order = models.PositiveIntegerField('ترتيب العرض', default=0)
    
    class Meta:
        db_table = 'governorates'
        verbose_name = 'محافظة'
        verbose_name_plural = 'المحافظات'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class Party(models.Model):
    """الأحزاب السياسية"""
    
    name = models.CharField('اسم الحزب', max_length=200, unique=True)
    name_en = models.CharField('الاسم بالإنجليزية', max_length=200, blank=True)
    abbreviation = models.CharField('الاختصار', max_length=10, blank=True)
    description = models.TextField('الوصف', blank=True)
    
    # معلومات إضافية
    founded_date = models.DateField('تاريخ التأسيس', blank=True, null=True)
    headquarters = models.CharField('المقر الرئيسي', max_length=200, blank=True)
    website = models.URLField('الموقع الإلكتروني', blank=True)
    
    # إعدادات العرض
    logo = models.ImageField('الشعار', upload_to='parties/logos/', blank=True, null=True)
    color = models.CharField('اللون المميز', max_length=7, default='#007BFF')
    is_active = models.BooleanField('نشط', default=True)
    display_order = models.PositiveIntegerField('ترتيب العرض', default=0)
    
    # تواريخ النظام
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        db_table = 'parties'
        verbose_name = 'حزب'
        verbose_name_plural = 'الأحزاب'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def members_count(self):
        """عدد أعضاء الحزب"""
        return User.objects.filter(party=self, user_type__in=['candidate', 'member']).count()
