"""
Serializers لخدمة التقييمات الذكية - مشروع نائبك
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    RatingCategory, SmartRating, Rating, RatingReport, 
    RatingSettings, RatingStatistics, Governorate, Party
)


class UserBasicSerializer(serializers.ModelSerializer):
    """Serializer أساسي للمستخدم"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    display_name = serializers.CharField(source='get_display_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'display_name']


class GovernorateSerializer(serializers.ModelSerializer):
    """Serializer للمحافظات"""
    
    class Meta:
        model = Governorate
        fields = [
            'id', 'name', 'name_en', 'code', 'region', 'capital',
            'area_km2', 'population', 'is_active', 'display_order'
        ]


class PartySerializer(serializers.ModelSerializer):
    """Serializer للأحزاب"""
    members_count = serializers.IntegerField(source='members_count', read_only=True)
    
    class Meta:
        model = Party
        fields = [
            'id', 'name', 'name_en', 'abbreviation', 'description',
            'founded_date', 'headquarters', 'website', 'logo', 'color',
            'is_active', 'display_order', 'members_count', 'created_at'
        ]


class RatingCategorySerializer(serializers.ModelSerializer):
    """Serializer لفئات التقييم"""
    total_ratings = serializers.IntegerField(source='total_ratings', read_only=True)
    
    class Meta:
        model = RatingCategory
        fields = [
            'id', 'name', 'name_en', 'description', 'icon', 'color',
            'weight', 'is_active', 'display_order', 'show_in_summary',
            'show_comments', 'total_ratings', 'created_at'
        ]


class SmartRatingSerializer(serializers.ModelSerializer):
    """Serializer للتقييمات الذكية"""
    rated_user = UserBasicSerializer(read_only=True)
    category = RatingCategorySerializer(read_only=True)
    display_rating = serializers.FloatField(source='get_display_rating', read_only=True)
    display_count = serializers.IntegerField(source='get_display_count', read_only=True)
    
    class Meta:
        model = SmartRating
        fields = [
            'id', 'rated_user', 'category', 'real_rating', 'real_count',
            'fake_rating', 'fake_count', 'display_mode', 'real_weight',
            'fake_weight', 'display_rating', 'display_count', 'is_active',
            'show_count', 'allow_new_ratings', 'created_at', 'updated_at'
        ]


class SmartRatingUpdateSerializer(serializers.ModelSerializer):
    """Serializer لتحديث التقييمات الذكية (للإدارة)"""
    
    class Meta:
        model = SmartRating
        fields = [
            'fake_rating', 'fake_count', 'display_mode', 'real_weight',
            'fake_weight', 'is_active', 'show_count', 'allow_new_ratings'
        ]
    
    def validate_fake_rating(self, value):
        """التحقق من التقييم المعدل"""
        if not (0.0 <= value <= 5.0):
            raise serializers.ValidationError("التقييم يجب أن يكون بين 0 و 5")
        return value
    
    def validate_fake_count(self, value):
        """التحقق من العدد الافتراضي"""
        if value < 0:
            raise serializers.ValidationError("العدد يجب أن يكون موجباً")
        return value
    
    def validate(self, data):
        """التحقق من الأوزان"""
        real_weight = data.get('real_weight', 0.3)
        fake_weight = data.get('fake_weight', 0.7)
        
        if real_weight + fake_weight != 1.0:
            raise serializers.ValidationError("مجموع الأوزان يجب أن يساوي 1.0")
        
        return data


class RatingSerializer(serializers.ModelSerializer):
    """Serializer للتقييمات الحقيقية"""
    rater = UserBasicSerializer(read_only=True)
    rated_user = UserBasicSerializer(read_only=True)
    category = RatingCategorySerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = [
            'id', 'rater', 'rated_user', 'category', 'rating', 'comment',
            'is_verified', 'is_public', 'is_reported', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'rater', 'is_verified', 'is_public', 'is_reported', 'created_at', 'updated_at'
        ]


class RatingCreateSerializer(serializers.ModelSerializer):
    """Serializer لإنشاء تقييم جديد"""
    rated_user_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Rating
        fields = ['rated_user_id', 'category_id', 'rating', 'comment']
    
    def validate_rating(self, value):
        """التحقق من التقييم"""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("التقييم يجب أن يكون بين 1 و 5")
        return value
    
    def validate_rated_user_id(self, value):
        """التحقق من المستخدم المُقيَّم"""
        try:
            user = User.objects.get(id=value, is_active=True)
            
            # التحقق من كون المستخدم نائب أو مرشح
            if not hasattr(user, 'user_type') or user.user_type not in ['candidate', 'member']:
                raise serializers.ValidationError("يمكن تقييم النواب والمرشحين فقط")
            
            # التحقق من عدم تقييم النفس
            request = self.context.get('request')
            if request and request.user.id == value:
                raise serializers.ValidationError("لا يمكن تقييم نفسك")
            
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("المستخدم غير موجود")
    
    def validate_category_id(self, value):
        """التحقق من فئة التقييم"""
        try:
            category = RatingCategory.objects.get(id=value, is_active=True)
            return value
        except RatingCategory.DoesNotExist:
            raise serializers.ValidationError("فئة التقييم غير موجودة أو غير نشطة")
    
    def validate_comment(self, value):
        """التحقق من التعليق"""
        if value and len(value) > 500:
            raise serializers.ValidationError("التعليق يجب ألا يتجاوز 500 حرف")
        return value
    
    def validate(self, data):
        """التحقق من عدم وجود تقييم مسبق"""
        request = self.context.get('request')
        if request and request.user:
            existing_rating = Rating.objects.filter(
                rater=request.user,
                rated_user_id=data['rated_user_id'],
                category_id=data['category_id']
            ).exists()
            
            if existing_rating:
                raise serializers.ValidationError("لقد قمت بتقييم هذا المستخدم في هذه الفئة مسبقاً")
        
        return data


class RatingReportSerializer(serializers.ModelSerializer):
    """Serializer للإبلاغ عن التقييمات"""
    reporter = UserBasicSerializer(read_only=True)
    rating = RatingSerializer(read_only=True)
    rating_id = serializers.UUIDField(write_only=True)
    reviewed_by = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = RatingReport
        fields = [
            'id', 'rating', 'rating_id', 'reporter', 'report_type', 'description',
            'status', 'admin_notes', 'reviewed_by', 'reviewed_at', 'created_at'
        ]
        read_only_fields = [
            'reporter', 'status', 'admin_notes', 'reviewed_by', 'reviewed_at', 'created_at'
        ]
    
    def validate_rating_id(self, value):
        """التحقق من التقييم"""
        try:
            rating = Rating.objects.get(id=value, is_public=True)
            
            # التحقق من عدم الإبلاغ عن تقييم خاص بالمستخدم
            request = self.context.get('request')
            if request and rating.rater == request.user:
                raise serializers.ValidationError("لا يمكن الإبلاغ عن تقييمك الخاص")
            
            return value
        except Rating.DoesNotExist:
            raise serializers.ValidationError("التقييم غير موجود")
    
    def validate_description(self, value):
        """التحقق من وصف البلاغ"""
        if not value or not value.strip():
            raise serializers.ValidationError("وصف البلاغ مطلوب")
        
        if len(value) < 10:
            raise serializers.ValidationError("وصف البلاغ يجب أن يكون 10 أحرف على الأقل")
        
        return value.strip()


class RatingSettingsSerializer(serializers.ModelSerializer):
    """Serializer لإعدادات التقييمات"""
    
    class Meta:
        model = RatingSettings
        fields = [
            'enable_ratings', 'enable_comments', 'require_login',
            'max_ratings_per_user_per_day', 'min_rating_interval_minutes',
            'max_comment_length', 'moderate_comments', 'default_display_mode',
            'default_fake_rating', 'default_fake_count', 'default_real_weight',
            'default_fake_weight', 'enable_ip_tracking', 'block_duplicate_ips',
            'auto_verify_ratings', 'notify_on_new_rating', 'notify_on_report',
            'updated_at'
        ]
        read_only_fields = ['updated_at']


class RatingStatisticsSerializer(serializers.ModelSerializer):
    """Serializer لإحصائيات التقييمات"""
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = RatingStatistics
        fields = [
            'user', 'total_ratings_received', 'average_rating',
            'ratings_1_star', 'ratings_2_star', 'ratings_3_star',
            'ratings_4_star', 'ratings_5_star', 'ratings_this_month',
            'ratings_last_month', 'last_updated'
        ]


class UserRatingSummarySerializer(serializers.Serializer):
    """Serializer لملخص تقييمات المستخدم"""
    user = UserBasicSerializer()
    overall_rating = serializers.FloatField()
    total_ratings = serializers.IntegerField()
    categories = serializers.ListField(child=serializers.DictField())
    recent_comments = serializers.ListField(child=serializers.DictField())
    
    # إحصائيات التوزيع
    rating_distribution = serializers.DictField()
    
    # معلومات إضافية
    last_rating_date = serializers.DateTimeField()
    is_highly_rated = serializers.BooleanField()
    rating_trend = serializers.CharField()  # 'up', 'down', 'stable'


class RatingAnalyticsSerializer(serializers.Serializer):
    """Serializer لتحليلات التقييمات"""
    
    # إحصائيات عامة
    total_ratings = serializers.IntegerField()
    total_users_rated = serializers.IntegerField()
    average_rating_system_wide = serializers.FloatField()
    
    # إحصائيات زمنية
    ratings_today = serializers.IntegerField()
    ratings_this_week = serializers.IntegerField()
    ratings_this_month = serializers.IntegerField()
    
    # توزيع التقييمات
    rating_distribution = serializers.DictField()
    
    # أفضل المقيمين
    top_rated_users = serializers.ListField(child=UserRatingSummarySerializer())
    
    # إحصائيات الفئات
    category_stats = serializers.ListField(child=serializers.DictField())
    
    # إحصائيات التقييمات الذكية
    smart_ratings_stats = serializers.DictField()
    
    # معدلات النشاط
    activity_rates = serializers.DictField()


class BulkSmartRatingUpdateSerializer(serializers.Serializer):
    """Serializer لتحديث التقييمات الذكية بالجملة"""
    user_ids = serializers.ListField(child=serializers.IntegerField())
    category_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    # البيانات المراد تحديثها
    fake_rating = serializers.FloatField(required=False, min_value=0.0, max_value=5.0)
    fake_count = serializers.IntegerField(required=False, min_value=0)
    display_mode = serializers.ChoiceField(
        choices=['real', 'fake', 'mixed', 'weighted'],
        required=False
    )
    real_weight = serializers.FloatField(required=False, min_value=0.0, max_value=1.0)
    fake_weight = serializers.FloatField(required=False, min_value=0.0, max_value=1.0)
    is_active = serializers.BooleanField(required=False)
    
    def validate_user_ids(self, value):
        """التحقق من معرفات المستخدمين"""
        if not value:
            raise serializers.ValidationError("يجب تحديد مستخدم واحد على الأقل")
        
        # التحقق من وجود المستخدمين
        existing_users = User.objects.filter(
            id__in=value,
            is_active=True,
            user_type__in=['candidate', 'member']
        ).count()
        
        if existing_users != len(value):
            raise serializers.ValidationError("بعض المستخدمين غير موجودين أو غير صالحين للتقييم")
        
        return value
    
    def validate_category_ids(self, value):
        """التحقق من معرفات الفئات"""
        if value:
            existing_categories = RatingCategory.objects.filter(
                id__in=value,
                is_active=True
            ).count()
            
            if existing_categories != len(value):
                raise serializers.ValidationError("بعض فئات التقييم غير موجودة أو غير نشطة")
        
        return value
    
    def validate(self, data):
        """التحقق من الأوزان"""
        real_weight = data.get('real_weight')
        fake_weight = data.get('fake_weight')
        
        if real_weight is not None and fake_weight is not None:
            if abs((real_weight + fake_weight) - 1.0) > 0.01:  # السماح بخطأ صغير
                raise serializers.ValidationError("مجموع الأوزان يجب أن يساوي 1.0")
        
        return data
