# ⭐ LEADER - دليل خدمة التقييمات البسيط

**اسم الخدمة:** naebak-ratings-service  
**المنفذ:** 8005  
**الإطار:** Django 4.2 + Django REST Framework  
**قاعدة البيانات:** PostgreSQL (للتقييمات والإحصائيات)  
**التخزين المؤقت:** Redis (للحسابات السريعة)  

---

## 📋 **نظرة عامة على الخدمة**

### **🎯 الغرض البسيط:**
خدمة التقييمات هي **نظام تقييم بسيط** يمكن المواطنين من تقييم النواب بنجوم من 1 إلى 5، مع إمكانية الأدمن في تحديد نقطة البداية للتقييمات (عدد المقيمين الأولي أو متوسط التقييم الأولي).

### **📝 كيف يعمل التطبيق بالضبط:**

**للمواطن:**
1. المواطن يدخل على **صفحة النائب الرئيسية** أو **كارت النائب في صفحة تصفح المرشحين والنواب**
2. يجد قسم التقييم مع 5 نجوم فارغة
3. يضغط على النجوم لاختيار تقييمه (1 إلى 5 نجوم)
4. يضغط زر "تقييم" لحفظ التقييم
5. **فوراً:** يزيد عدد المقيمين بـ +1 ويتم حساب المتوسط الجديد
6. **لا يستطيع تقييم نفس النائب مرة أخرى** من نفس الحساب

**للأدمن:**
1. الأدمن يدخل على لوحة إدارة التقييمات
2. يختار أي نائب من القائمة
3. يحدد **نقطة البداية** للنائب:
   - **عدد المقيمين الأولي:** مثلاً 500 مقيم
   - **متوسط التقييم الأولي:** مثلاً 4.2 نجوم
4. **النتيجة النهائية:** (التقييمات الحقيقية + التقييم الأولي) ÷ (عدد المقيمين الحقيقي + العدد الأولي)

**مثال عملي:**
- النائب أحمد محمد: الأدمن حدد له 500 مقيم أولي بمتوسط 4.2
- 100 مواطن حقيقي قيموه بمتوسط 4.8
- **النتيجة المعروضة:** (500×4.2 + 100×4.8) ÷ (500+100) = 4.3 نجوم من 600 مقيم

### **🔄 آلية العمل البسيطة:**
```
1. المواطن يدخل على صفحة النائب أو كارته في متصفح المرشحين
                                    ↓
2. المواطن يختار تقييم من 1 إلى 5 نجوم
                                    ↓
3. يتم حفظ التقييم وتحديث المتوسط تلقائياً
                                    ↓
4. الأدمن يمكنه تعديل نقطة البداية (عدد المقيمين أو المتوسط الأولي)
                                    ↓
5. التقييم النهائي = (التقييمات الحقيقية + التقييم الأولي) / (عدد المقيمين الحقيقي + العدد الأولي)
```

### **🏛️ أهمية الخدمة في منصة نائبك:**
- **مقياس شعبية النواب** من خلال تقييمات المواطنين
- **أداة للمواطنين** للتعبير عن رأيهم في أداء النواب
- **مؤشر للنواب** لمعرفة مستوى رضا المواطنين عنهم
- **أداة للأدمن** لإدارة التقييمات وضبط نقاط البداية

---

## 👥 **أدوار المستخدمين والصلاحيات**

### **🏠 المواطن (Citizen):**
**الصلاحيات من المخزن:**
```json
{
  "role": "citizen",
  "permissions": [
    "rate_representatives",
    "view_ratings",
    "update_own_rating",
    "view_rating_statistics"
  ],
  "rating_limits": {
    "min_rating": 1,
    "max_rating": 5,
    "one_rating_per_representative": true,
    "can_update_rating": false,
    "no_cooldown": true
  }
}
```

**الوظائف:**
- تقييم أي نائب من 1 إلى 5 نجوم (مرة واحدة فقط)
- مشاهدة متوسط تقييمات النواب
- مشاهدة عدد المقيمين لكل نائب
- زيادة عداد المقيمين تلقائياً عند التقييم

### **⚙️ الإدارة (Admin):**
**الصلاحيات من المخزن:**
```json
{
  "role": "admin",
  "permissions": [
    "manage_all_ratings",
    "set_initial_ratings",
    "set_initial_voter_count",
    "moderate_ratings",
    "view_detailed_statistics",
    "reset_ratings",
    "manage_featured_representatives"
  ],
  "access_level": "full_system_access"
}
```

**الوظائف:**
- تحديد نقطة البداية لتقييم أي نائب
- تحديد عدد المقيمين الأولي لأي نائب
- تحديد متوسط التقييم الأولي لأي نائب
- مراقبة التقييمات ومنع التلاعب
- إعادة تعيين تقييمات النواب عند الحاجة
- إدارة قائمة النواب المميزين (تقييم عالي)

### **🏛️ النائب (Representative):**
**الصلاحيات من المخزن:**
```json
{
  "role": "representative",
  "permissions": [
    "view_own_ratings",
    "view_rating_breakdown",
    "view_rating_trends",
    "respond_to_ratings"
  ],
  "rating_display": {
    "show_in_profile": true,
    "show_in_card": true,
    "show_in_search": true,
    "show_trend_analysis": true
  }
}
```

**الوظائف:**
- مشاهدة تقييمه الحالي ومتوسط النجوم
- مشاهدة عدد المواطنين الذين قيموه
- مشاهدة تطور تقييمه عبر الوقت
- مشاهدة توزيع التقييمات (كم مواطن أعطى 5 نجوم، كم أعطى 4، إلخ)

---

## 📦 **البيانات الكاملة من المستودع المخزن**

### **⭐ مستويات التقييم (5 مستويات):**
```python
RATING_LEVELS = [
    {
        "stars": 1,
        "name": "ضعيف جداً",
        "name_en": "Very Poor",
        "color": "#DC3545",
        "icon": "⭐",
        "description": "أداء ضعيف جداً وغير مرضي"
    },
    {
        "stars": 2,
        "name": "ضعيف",
        "name_en": "Poor",
        "color": "#FD7E14",
        "icon": "⭐⭐",
        "description": "أداء ضعيف ويحتاج تحسين كبير"
    },
    {
        "stars": 3,
        "name": "متوسط",
        "name_en": "Average",
        "color": "#FFC107",
        "icon": "⭐⭐⭐",
        "description": "أداء متوسط ومقبول"
    },
    {
        "stars": 4,
        "name": "جيد",
        "name_en": "Good",
        "color": "#28A745",
        "icon": "⭐⭐⭐⭐",
        "description": "أداء جيد ومرضي"
    },
    {
        "stars": 5,
        "name": "ممتاز",
        "name_en": "Excellent",
        "color": "#007BFF",
        "icon": "⭐⭐⭐⭐⭐",
        "description": "أداء ممتاز ومتميز"
    }
]
```
**الاستخدام:** واجهة التقييم، عرض النتائج، الألوان والأيقونات

### **🗺️ المحافظات المصرية (27 محافظة):**
```python
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
```
**الاستخدام:** إحصائيات التقييمات حسب المحافظة، تصنيف النواب

### **🎉 الأحزاب السياسية المصرية (16 حزب):**
```python
POLITICAL_PARTIES = [
    {"name": "حزب الوفد", "name_en": "Al-Wafd Party", "abbreviation": "الوفد"},
    {"name": "الحزب الوطني الديمقراطي", "name_en": "National Democratic Party", "abbreviation": "الوطني"},
    {"name": "حزب الغد", "name_en": "Al-Ghad Party", "abbreviation": "الغد"},
    {"name": "حزب التجمع الوطني التقدمي الوحدوي", "name_en": "National Progressive Unionist Party", "abbreviation": "التجمع"},
    {"name": "حزب الناصري", "name_en": "Nasserist Party", "abbreviation": "الناصري"},
    {"name": "حزب الكرامة", "name_en": "Al-Karama Party", "abbreviation": "الكرامة"},
    {"name": "حزب الوسط الجديد", "name_en": "New Wasat Party", "abbreviation": "الوسط"},
    {"name": "حزب الحرية المصري", "name_en": "Egyptian Freedom Party", "abbreviation": "الحرية"},
    {"name": "حزب المصريين الأحرار", "name_en": "Free Egyptians Party", "abbreviation": "المصريين الأحرار"},
    {"name": "حزب النور", "name_en": "Al-Nour Party", "abbreviation": "النور"},
    {"name": "حزب البناء والتنمية", "name_en": "Building and Development Party", "abbreviation": "البناء والتنمية"},
    {"name": "حزب الإصلاح والتنمية", "name_en": "Reform and Development Party", "abbreviation": "الإصلاح والتنمية"},
    {"name": "حزب مستقبل وطن", "name_en": "Future of a Nation Party", "abbreviation": "مستقبل وطن"},
    {"name": "حزب المؤتمر", "name_en": "Conference Party", "abbreviation": "المؤتمر"},
    {"name": "حزب الشعب الجمهوري", "name_en": "Republican People's Party", "abbreviation": "الشعب الجمهوري"},
    {"name": "مستقل", "name_en": "Independent", "abbreviation": "مستقل"}
]
```
**الاستخدام:** إحصائيات التقييمات حسب الحزب، مقارنة أداء الأحزاب

### **🏛️ أنواع المجالس (2 نوع):**
```python
COUNCIL_TYPES = [
    {
        "type": "parliament", 
        "name": "مجلس النواب", 
        "name_en": "Parliament",
        "description": "المجلس الأساسي للتشريع",
        "total_seats": 596,
        "rating_weight": 1.0
    },
    {
        "type": "senate", 
        "name": "مجلس الشيوخ", 
        "name_en": "Senate",
        "description": "المجلس الاستشاري العلوي", 
        "total_seats": 300,
        "rating_weight": 1.0
    }
]
```
**الاستخدام:** تصنيف التقييمات حسب نوع المجلس، إحصائيات منفصلة

### **📊 فئات التقييم (5 فئات):**
```python
RATING_CATEGORIES = [
    {
        "category": "overall",
        "name": "التقييم العام",
        "name_en": "Overall Rating",
        "description": "التقييم الشامل لأداء النائب",
        "weight": 1.0,
        "is_primary": True
    },
    {
        "category": "responsiveness",
        "name": "سرعة الاستجابة",
        "name_en": "Responsiveness",
        "description": "مدى سرعة رد النائب على الشكاوى والاستفسارات",
        "weight": 0.8,
        "is_primary": False
    },
    {
        "category": "effectiveness",
        "name": "فعالية الحلول",
        "name_en": "Effectiveness",
        "description": "مدى فعالية الحلول المقدمة من النائب",
        "weight": 0.9,
        "is_primary": False
    },
    {
        "category": "communication",
        "name": "التواصل",
        "name_en": "Communication",
        "description": "جودة التواصل مع المواطنين",
        "weight": 0.7,
        "is_primary": False
    },
    {
        "category": "transparency",
        "name": "الشفافية",
        "name_en": "Transparency",
        "description": "مدى شفافية النائب في أعماله وقراراته",
        "weight": 0.6,
        "is_primary": False
    }
]
```
**الاستخدام:** تقييمات مفصلة، تحليل نقاط القوة والضعف

### **🎯 معايير النواب المميزين:**
```python
FEATURED_CRITERIA = {
    "min_ratings_count": 100,
    "min_average_rating": 4.5,
    "min_months_active": 6,
    "max_featured_count": 10,
    "update_frequency": "weekly",
    "criteria": [
        {
            "name": "عدد التقييمات",
            "requirement": "100+ تقييم",
            "weight": 0.3
        },
        {
            "name": "متوسط التقييم",
            "requirement": "4.5+ نجوم",
            "weight": 0.4
        },
        {
            "name": "الاستمرارية",
            "requirement": "6+ أشهر نشاط",
            "weight": 0.2
        },
        {
            "name": "التفاعل",
            "requirement": "تفاعل منتظم مع المواطنين",
            "weight": 0.1
        }
    ]
}
```
**الاستخدام:** تحديد النواب المميزين، عرضهم في الصفحة الرئيسية

### **🔒 قواعد التقييم البسيطة:**
```python
SIMPLE_RATING_RULES = {
    "one_rating_per_user_per_representative": True,
    "can_update_existing_rating": False,
    "increment_counter_on_new_rating": True,
    "admin_control_only": True,
    "no_complex_validation": True
}
```
**الاستخدام:** قواعد بسيطة، تحكم الأدمن فقط

### **📱 أماكن عرض التقييمات:**
```python
RATING_DISPLAY_LOCATIONS = [
    {
        "location": "representative_profile",
        "name": "صفحة النائب الرئيسية",
        "format": "نجوم + رقم + عدد المقيمين",
        "example": "⭐⭐⭐⭐⭐ 4.7 (1,234 تقييم)"
    },
    {
        "location": "representative_card",
        "name": "كارت النائب في المتصفح",
        "format": "نجوم + رقم",
        "example": "⭐⭐⭐⭐⭐ 4.7"
    },
    {
        "location": "search_results",
        "name": "نتائج البحث",
        "format": "نجوم + رقم",
        "example": "⭐⭐⭐⭐⭐ 4.7"
    },
    {
        "location": "leaderboard",
        "name": "قائمة الأعلى تقييماً",
        "format": "ترتيب + نجوم + رقم + عدد المقيمين",
        "example": "#1 ⭐⭐⭐⭐⭐ 4.9 (2,156 تقييم)"
    },
    {
        "location": "statistics_dashboard",
        "name": "لوحة الإحصائيات",
        "format": "تفصيلي مع رسوم بيانية",
        "example": "متوسط شامل + توزيع النجوم + اتجاهات"
    }
]
```
**الاستخدام:** تحديد كيفية عرض التقييمات في كل مكان

---

## 🌐 **العلاقات مع الخدمات الأخرى**

### **🔗 الخدمات المتفاعلة:**

#### **📨 الخدمات المرسلة إليها:**
1. **خدمة المصادقة (8001):**
   - التحقق من هوية المقيم
   - التحقق من صلاحيات الأدمن
   - الحصول على بيانات المستخدم

2. **خدمة عداد الزوار (8006):**
   - تتبع زيارات صفحات التقييم
   - إحصائيات استخدام النظام

#### **📤 الخدمات المستقبلة منها:**
1. **خدمة الإحصائيات (8012):**
   - إرسال بيانات التقييمات الجديدة
   - إحصائيات متوسط التقييمات
   - تحليلات أداء النواب

2. **خدمة الإشعارات (8008):**
   - إشعار النائب بالتقييمات الجديدة
   - تنبيهات الأدمن للتقييمات المشبوهة

3. **خدمة المحتوى (8010):**
   - عرض التقييمات في صفحات النواب
   - عرض التقييمات في كروت المتصفح

### **📊 تدفق البيانات:**
```
المواطن → تقييم النائب → خدمة التقييمات (8005)
                              ↓
خدمة المصادقة (8001) ← التحقق من الهوية
                              ↓
خدمة الإحصائيات (8012) ← تحديث إحصائيات النائب
                              ↓
خدمة الإشعارات (8008) ← إشعار النائب (اختياري)
                              ↓
خدمة المحتوى (8010) ← تحديث عرض التقييم في الصفحات
```

---

## ⚙️ **إعدادات Google Cloud Run**

### **🛠️ بيئة التطوير:**
```yaml
service_name: naebak-ratings-service-dev
resources:
  cpu: 0.3
  memory: 256Mi
scaling:
  min_instances: 0
  max_instances: 2

environment_variables:
  - DJANGO_SETTINGS_MODULE=app.settings.development
  - DEBUG=true
  - DATABASE_URL=postgresql://localhost:5432/naebak_ratings_dev
  - REDIS_URL=redis://localhost:6379/4
  - MIN_RATINGS_FOR_FEATURED=10
  - FEATURED_THRESHOLD=4.0
  - ONE_RATING_PER_USER=true
```

### **🏭 بيئة الإنتاج:**
```yaml
service_name: naebak-ratings-service
resources:
  cpu: 0.4
  memory: 256Mi
scaling:
  min_instances: 1
  max_instances: 5

environment_variables:
  - DJANGO_SETTINGS_MODULE=app.settings.production
  - DEBUG=false
  - DATABASE_URL=${DATABASE_URL_PROD}
  - REDIS_URL=${REDIS_URL_PROD}
  - MIN_RATINGS_FOR_FEATURED=100
  - FEATURED_THRESHOLD=4.5
  - ONE_RATING_PER_USER=true
  - ALLOWED_HOSTS=naebak.com,*.naebak.com
```

---

## 🔗 **واجهات برمجة التطبيقات البسيطة**

### **📡 نقاط النهاية الأساسية (7 APIs):**
```
# Rating Management
POST /api/ratings/rate/                         - تقييم نائب (مواطن - مرة واحدة فقط)
GET  /api/ratings/representative/{id}/          - تقييمات نائب محدد

# Admin Management  
PUT  /api/ratings/set-initial/{rep_id}/         - تحديد نقطة البداية (أدمن)
GET  /api/ratings/statistics/                   - إحصائيات شاملة (أدمن)

# Public Data
GET  /api/ratings/featured/                     - النواب الأعلى تقييماً
GET  /api/ratings/governorates/                 - المحافظات للتصفية
GET  /health                                    - فحص صحة الخدمة
```

### **📥 مثال تقييم نائب:**
```json
POST /api/ratings/rate/
Content-Type: application/json
Authorization: Bearer {jwt_token}

{
  "representative_id": 15,
  "rating": 5,
  "category": "overall",
  "comment": "نائب ممتاز ومتجاوب مع الشكاوى" // اختياري
}

Response:
{
  "status": "success",
  "data": {
    "rating_id": 1234,
    "representative_id": 15,
    "rating": 5,
    "category": "overall",
    "submitted_at": "2025-01-01T10:30:00Z",
    "is_final": true,
    "representative_new_average": 4.7,
    "representative_total_ratings": 1235
  },
  "message": "تم تسجيل تقييمك بنجاح"
}
```

### **📥 مثال تحديد نقطة البداية (أدمن):**
```json
PUT /api/ratings/set-initial/15/
Content-Type: application/json
Authorization: Bearer {admin_jwt_token}

{
  "initial_rating": 4.2,
  "initial_count": 500,
  "reason": "تعديل نقطة البداية بناءً على التقييمات السابقة"
}

Response:
{
  "status": "success",
  "data": {
    "representative_id": 15,
    "initial_rating": 4.2,
    "initial_count": 500,
    "current_real_ratings": 235,
    "current_real_average": 4.8,
    "final_displayed_average": 4.4,
    "final_displayed_count": 735
  },
  "message": "تم تحديث نقطة البداية بنجاح"
}
```

---

## 🔄 **الفروق بين البيئات**

### **🛠️ بيئة التطوير:**
- **الحد الأدنى للتميز:** 10 تقييمات (بدلاً من 100)
- **متوسط التميز:** 4.0 نجوم (بدلاً من 4.5)
- **قاعدة البيانات:** PostgreSQL محلي
- **قاعدة بسيطة:** تقييم واحد لكل مواطن لكل نائب

### **🏭 بيئة الإنتاج:**
- **الحد الأدنى للتميز:** 100 تقييم
- **متوسط التميز:** 4.5 نجوم
- **قاعدة البيانات:** Cloud SQL PostgreSQL
- **قاعدة بسيطة:** تقييم واحد لكل مواطن لكل نائب

---

## 📈 **المراقبة والتحليلات**

### **📊 المقاييس الأساسية:**
- **معدل التقييمات اليومي** - عدد التقييمات الجديدة
- **متوسط التقييمات العام** - متوسط جميع النواب
- **توزيع التقييمات** - كم نائب في كل فئة نجوم
- **النواب الأعلى تقييماً** - القائمة المحدثة أسبوعياً
- **معدل التحديث** - كم مواطن يغير تقييمه

### **🚨 التنبيهات:**
- **انخفاض مفاجئ** - تراجع تقييم نائب بسرعة
- **نشاط عالي** - زيادة غير طبيعية في التقييمات
- **أخطاء النظام** - مشاكل تقنية في الخدمة

---

## 🎯 **خطة التطوير البسيطة**

### **المرحلة الأولى (2 أسبوع):**
- إعداد Django + نماذج البيانات البسيطة
- تطبيق تقييم النواب (1-5 نجوم)
- حساب المتوسطات تلقائياً

### **المرحلة الثانية (1 أسبوع):**
- لوحة الأدمن لتحديد نقاط البداية
- عرض التقييمات في صفحات النواب
- ربط مع خدمة المصادقة

### **المرحلة الثالثة (1 أسبوع):**
- ربط مع خدمة الإحصائيات
- اختبارات ونشر
- مراقبة الأداء

---

## 📚 **الموارد والمراجع**

### **🔧 التبعيات:**
```python
DEPENDENCIES = [
    "Django==4.2.0",
    "djangorestframework==3.14.0", 
    "psycopg2-binary==2.9.7",
    "redis==4.6.0"  # للتخزين المؤقت البسيط
]
```

---

## 🎯 **الخلاصة**

خدمة التقييمات هي **نظام بسيط وفعال** يمكن المواطنين من تقييم النواب بنجوم من 1 إلى 5، مع إمكانية الأدمن في ضبط نقاط البداية. الخدمة تركز على **البساطة والوضوح** مع حماية من التلاعب وتكامل سلس مع باقي خدمات المنصة.

**النقاط الرئيسية:**
- ✅ تقييم بسيط بالنجوم (1-5)
- ✅ تقييم واحد فقط لكل مواطن لكل نائب
- ✅ زيادة العداد تلقائياً (+1) عند كل تقييم
- ✅ إمكانية تحديد نقطة البداية للأدمن  
- ✅ عرض في صفحات النواب وكروتهم
- ✅ تكامل مع الخدمات الأخرى

الخدمة الآن **جاهزة للتطوير** مع جميع المتطلبات والإعدادات محددة بوضوح.
