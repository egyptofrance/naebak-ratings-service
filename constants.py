# -*- coding: utf-8 -*-
"""ثوابت وبيانات أساسية لخدمة التقييمات"""

# قيم التقييمات
RATING_VALUES = [
    {"value": 1, "name": "ضعيف جداً", "name_en": "Very Poor", "emoji": "😞"},
    {"value": 2, "name": "ضعيف", "name_en": "Poor", "emoji": "😕"},
    {"value": 3, "name": "متوسط", "name_en": "Average", "emoji": "😐"},
    {"value": 4, "name": "جيد", "name_en": "Good", "emoji": "😊"},
    {"value": 5, "name": "ممتاز", "name_en": "Excellent", "emoji": "😍"}
]

# أنواع التقييمات
RATING_TYPES = [
    {
        "type": "candidate_performance",
        "name": "أداء المرشح",
        "name_en": "Candidate Performance",
        "description": "تقييم أداء المرشح في الحملة الانتخابية"
    },
    {
        "type": "member_performance", 
        "name": "أداء العضو",
        "name_en": "Member Performance",
        "description": "تقييم أداء عضو المجلس في فترة العضوية"
    },
    {
        "type": "service_quality",
        "name": "جودة الخدمة",
        "name_en": "Service Quality", 
        "description": "تقييم جودة الخدمات المقدمة"
    },
    {
        "type": "response_time",
        "name": "سرعة الاستجابة",
        "name_en": "Response Time",
        "description": "تقييم سرعة الاستجابة للشكاوى والطلبات"
    },
    {
        "type": "communication",
        "name": "التواصل",
        "name_en": "Communication",
        "description": "تقييم جودة التواصل مع المواطنين"
    }
]

# معايير التقييم
RATING_CRITERIA = [
    {
        "criteria": "transparency",
        "name": "الشفافية",
        "name_en": "Transparency",
        "weight": 0.25
    },
    {
        "criteria": "effectiveness",
        "name": "الفعالية",
        "name_en": "Effectiveness", 
        "weight": 0.30
    },
    {
        "criteria": "responsiveness",
        "name": "الاستجابة",
        "name_en": "Responsiveness",
        "weight": 0.25
    },
    {
        "criteria": "integrity",
        "name": "النزاهة",
        "name_en": "Integrity",
        "weight": 0.20
    }
]

# حالات التقييم
RATING_STATUS = [
    {"status": "pending", "name": "في الانتظار", "name_en": "Pending"},
    {"status": "approved", "name": "معتمد", "name_en": "Approved"},
    {"status": "rejected", "name": "مرفوض", "name_en": "Rejected"},
    {"status": "flagged", "name": "مبلغ عنه", "name_en": "Flagged"}
]

# المحافظات المصرية (27 محافظة)
GOVERNORATES = [
    {"name": "القاهرة", "name_en": "Cairo", "code": "CAI"},
    {"name": "الجيزة", "name_en": "Giza", "code": "GIZ"},
    {"name": "الإسكندرية", "name_en": "Alexandria", "code": "ALX"},
    {"name": "الدقهلية", "name_en": "Dakahlia", "code": "DAK"},
    {"name": "البحر الأحمر", "name_en": "Red Sea", "code": "RSS"},
    {"name": "البحيرة", "name_en": "Beheira", "code": "BEH"},
    {"name": "الفيوم", "name_en": "Fayoum", "code": "FAY"},
    {"name": "الغربية", "name_en": "Gharbia", "code": "GHR"},
    {"name": "الإسماعيلية", "name_en": "Ismailia", "code": "ISM"},
    {"name": "المنوفية", "name_en": "Monufia", "code": "MNF"},
    {"name": "المنيا", "name_en": "Minya", "code": "MNY"},
    {"name": "القليوبية", "name_en": "Qalyubia", "code": "QLY"},
    {"name": "الوادي الجديد", "name_en": "New Valley", "code": "WAD"},
    {"name": "شمال سيناء", "name_en": "North Sinai", "code": "NSI"},
    {"name": "جنوب سيناء", "name_en": "South Sinai", "code": "SSI"},
    {"name": "الشرقية", "name_en": "Sharqia", "code": "SHR"},
    {"name": "سوهاج", "name_en": "Sohag", "code": "SOH"},
    {"name": "السويس", "name_en": "Suez", "code": "SUZ"},
    {"name": "أسوان", "name_en": "Aswan", "code": "ASW"},
    {"name": "أسيوط", "name_en": "Asyut", "code": "ASY"},
    {"name": "بني سويف", "name_en": "Beni Suef", "code": "BNS"},
    {"name": "بورسعيد", "name_en": "Port Said", "code": "PTS"},
    {"name": "دمياط", "name_en": "Damietta", "code": "DAM"},
    {"name": "كفر الشيخ", "name_en": "Kafr El Sheikh", "code": "KFS"},
    {"name": "مطروح", "name_en": "Matrouh", "code": "MAT"},
    {"name": "الأقصر", "name_en": "Luxor", "code": "LUX"},
    {"name": "قنا", "name_en": "Qena", "code": "QEN"}
]

# أنواع المجالس
COUNCIL_TYPES = [
    {
        "type": "parliament", 
        "name": "مجلس النواب", 
        "name_en": "Parliament",
        "total_seats": 596
    },
    {
        "type": "senate", 
        "name": "مجلس الشيوخ", 
        "name_en": "Senate",
        "total_seats": 300
    }
]

# إعدادات التقييم
RATING_SETTINGS = {
    'MIN_RATING': 1,
    'MAX_RATING': 5,
    'DEFAULT_RATING': 3,
    'ALLOW_ANONYMOUS': False,
    'REQUIRE_COMMENT': False,
    'MAX_COMMENT_LENGTH': 500,
    'MIN_COMMENT_LENGTH': 10,
    'COOLDOWN_PERIOD': 24 * 60 * 60,  # 24 ساعة بالثواني
    'MAX_RATINGS_PER_USER_PER_DAY': 5
}

# رسائل التحقق
VALIDATION_MESSAGES = {
    'RATING_REQUIRED': 'التقييم مطلوب',
    'INVALID_RATING_VALUE': 'قيمة التقييم غير صحيحة (1-5)',
    'COMMENT_TOO_SHORT': 'التعليق قصير جداً',
    'COMMENT_TOO_LONG': 'التعليق طويل جداً',
    'DUPLICATE_RATING': 'لقد قمت بتقييم هذا العنصر مسبقاً',
    'COOLDOWN_ACTIVE': 'يجب الانتظار قبل إضافة تقييم جديد',
    'UNAUTHORIZED': 'غير مخول لإضافة تقييم',
    'INVALID_TARGET': 'الهدف المراد تقييمه غير صحيح'
}

# للاستخدام في Django choices
RATING_VALUE_CHOICES = [(rating['value'], rating['name']) for rating in RATING_VALUES]
RATING_TYPE_CHOICES = [(rating['type'], rating['name']) for rating in RATING_TYPES]
STATUS_CHOICES = [(status['status'], status['name']) for status in RATING_STATUS]
CRITERIA_CHOICES = [(criteria['criteria'], criteria['name']) for criteria in RATING_CRITERIA]

# وظائف مساعدة
def get_rating_name(value):
    """الحصول على اسم التقييم بالعربية"""
    for rating in RATING_VALUES:
        if rating['value'] == value:
            return rating['name']
    return 'غير محدد'

def get_rating_emoji(value):
    """الحصول على رمز التقييم"""
    for rating in RATING_VALUES:
        if rating['value'] == value:
            return rating['emoji']
    return '❓'

def calculate_weighted_average(ratings_by_criteria):
    """حساب المتوسط المرجح للتقييمات"""
    total_weight = 0
    weighted_sum = 0
    
    for criteria_data in RATING_CRITERIA:
        criteria = criteria_data['criteria']
        weight = criteria_data['weight']
        
        if criteria in ratings_by_criteria:
            rating_value = ratings_by_criteria[criteria]
            weighted_sum += rating_value * weight
            total_weight += weight
    
    return weighted_sum / total_weight if total_weight > 0 else 0
