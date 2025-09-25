"""
أمر Django لتحميل البيانات الأساسية لخدمة التقييمات الذكية
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.ratings.models import (
    RatingCategory, RatingSettings, Governorate, Party
)


class Command(BaseCommand):
    help = 'تحميل البيانات الأساسية لخدمة التقييمات الذكية'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='إعادة تحميل البيانات حتى لو كانت موجودة',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        with transaction.atomic():
            # تحميل فئات التقييم
            self.load_rating_categories(force)
            
            # تحميل المحافظات
            self.load_governorates(force)
            
            # تحميل الأحزاب
            self.load_parties(force)
            
            # تحميل إعدادات النظام
            self.load_system_settings(force)
        
        self.stdout.write(
            self.style.SUCCESS('تم تحميل البيانات الأساسية لخدمة التقييمات بنجاح!')
        )

    def load_rating_categories(self, force=False):
        """تحميل فئات التقييم"""
        categories_data = [
            {
                "name": "الأداء العام",
                "name_en": "Overall Performance",
                "description": "تقييم الأداء العام للنائب أو المرشح في عمله",
                "icon": "fas fa-chart-line",
                "color": "#007BFF",
                "weight": 1.5,
                "display_order": 1,
                "show_in_summary": True,
                "show_comments": True
            },
            {
                "name": "التواصل مع المواطنين",
                "name_en": "Citizen Communication",
                "description": "مدى تفاعل النائب مع المواطنين والرد على استفساراتهم",
                "icon": "fas fa-comments",
                "color": "#28A745",
                "weight": 1.3,
                "display_order": 2,
                "show_in_summary": True,
                "show_comments": True
            },
            {
                "name": "سرعة الاستجابة",
                "name_en": "Response Speed",
                "description": "سرعة الرد على الرسائل والشكاوى المقدمة",
                "icon": "fas fa-tachometer-alt",
                "color": "#FFC107",
                "weight": 1.2,
                "display_order": 3,
                "show_in_summary": True,
                "show_comments": True
            },
            {
                "name": "الشفافية",
                "name_en": "Transparency",
                "description": "مدى وضوح وشفافية النائب في تعاملاته وقراراته",
                "icon": "fas fa-eye",
                "color": "#17A2B8",
                "weight": 1.4,
                "display_order": 4,
                "show_in_summary": True,
                "show_comments": True
            },
            {
                "name": "حل المشاكل",
                "name_en": "Problem Solving",
                "description": "قدرة النائب على حل المشاكل والقضايا المطروحة",
                "icon": "fas fa-tools",
                "color": "#DC3545",
                "weight": 1.6,
                "display_order": 5,
                "show_in_summary": True,
                "show_comments": True
            },
            {
                "name": "المصداقية",
                "name_en": "Credibility",
                "description": "مدى مصداقية النائب في وعوده والتزامه بها",
                "icon": "fas fa-handshake",
                "color": "#6F42C1",
                "weight": 1.5,
                "display_order": 6,
                "show_in_summary": True,
                "show_comments": True
            },
            {
                "name": "الخبرة والكفاءة",
                "name_en": "Experience & Competence",
                "description": "مستوى خبرة وكفاءة النائب في المجال السياسي",
                "icon": "fas fa-graduation-cap",
                "color": "#E83E8C",
                "weight": 1.3,
                "display_order": 7,
                "show_in_summary": False,
                "show_comments": True
            },
            {
                "name": "التمثيل البرلماني",
                "name_en": "Parliamentary Representation",
                "description": "جودة تمثيل النائب لدائرته في البرلمان",
                "icon": "fas fa-university",
                "color": "#FD7E14",
                "weight": 1.4,
                "display_order": 8,
                "show_in_summary": False,
                "show_comments": True
            }
        ]
        
        created_count = 0
        for category_data in categories_data:
            category, created = RatingCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            if created or force:
                if force and not created:
                    for key, value in category_data.items():
                        setattr(category, key, value)
                    category.save()
                created_count += 1
        
        self.stdout.write(f'تم تحميل {created_count} فئة تقييم')

    def load_governorates(self, force=False):
        """تحميل المحافظات المصرية"""
        governorates_data = [
            {"name": "القاهرة", "name_en": "Cairo", "code": "CAI", "region": "cairo", "capital": "القاهرة", "display_order": 1},
            {"name": "الجيزة", "name_en": "Giza", "code": "GIZ", "region": "cairo", "capital": "الجيزة", "display_order": 2},
            {"name": "القليوبية", "name_en": "Qalyubia", "code": "QAL", "region": "cairo", "capital": "بنها", "display_order": 3},
            {"name": "الإسكندرية", "name_en": "Alexandria", "code": "ALX", "region": "delta", "capital": "الإسكندرية", "display_order": 4},
            {"name": "البحيرة", "name_en": "Beheira", "code": "BEH", "region": "delta", "capital": "دمنهور", "display_order": 5},
            {"name": "كفر الشيخ", "name_en": "Kafr El Sheikh", "code": "KFS", "region": "delta", "capital": "كفر الشيخ", "display_order": 6},
            {"name": "الدقهلية", "name_en": "Dakahlia", "code": "DAK", "region": "delta", "capital": "المنصورة", "display_order": 7},
            {"name": "دمياط", "name_en": "Damietta", "code": "DAM", "region": "delta", "capital": "دمياط", "display_order": 8},
            {"name": "الشرقية", "name_en": "Sharqia", "code": "SHA", "region": "delta", "capital": "الزقازيق", "display_order": 9},
            {"name": "المنوفية", "name_en": "Monufia", "code": "MON", "region": "delta", "capital": "شبين الكوم", "display_order": 10},
            {"name": "الغربية", "name_en": "Gharbia", "code": "GHA", "region": "delta", "capital": "طنطا", "display_order": 11},
            {"name": "بورسعيد", "name_en": "Port Said", "code": "POR", "region": "canal", "capital": "بورسعيد", "display_order": 12},
            {"name": "الإسماعيلية", "name_en": "Ismailia", "code": "ISM", "region": "canal", "capital": "الإسماعيلية", "display_order": 13},
            {"name": "السويس", "name_en": "Suez", "code": "SUE", "region": "canal", "capital": "السويس", "display_order": 14},
            {"name": "شمال سيناء", "name_en": "North Sinai", "code": "NSI", "region": "sinai", "capital": "العريش", "display_order": 15},
            {"name": "جنوب سيناء", "name_en": "South Sinai", "code": "SSI", "region": "sinai", "capital": "الطور", "display_order": 16},
            {"name": "المنيا", "name_en": "Minya", "code": "MIN", "region": "upper", "capital": "المنيا", "display_order": 17},
            {"name": "بني سويف", "name_en": "Beni Suef", "code": "BNS", "region": "upper", "capital": "بني سويف", "display_order": 18},
            {"name": "الفيوم", "name_en": "Fayoum", "code": "FAY", "region": "upper", "capital": "الفيوم", "display_order": 19},
            {"name": "أسيوط", "name_en": "Asyut", "code": "ASY", "region": "upper", "capital": "أسيوط", "display_order": 20},
            {"name": "سوهاج", "name_en": "Sohag", "code": "SOH", "region": "upper", "capital": "سوهاج", "display_order": 21},
            {"name": "قنا", "name_en": "Qena", "code": "QEN", "region": "upper", "capital": "قنا", "display_order": 22},
            {"name": "الأقصر", "name_en": "Luxor", "code": "LUX", "region": "upper", "capital": "الأقصر", "display_order": 23},
            {"name": "أسوان", "name_en": "Aswan", "code": "ASW", "region": "upper", "capital": "أسوان", "display_order": 24},
            {"name": "البحر الأحمر", "name_en": "Red Sea", "code": "RED", "region": "red_sea", "capital": "الغردقة", "display_order": 25},
            {"name": "الوادي الجديد", "name_en": "New Valley", "code": "NEW", "region": "new_valley", "capital": "الخارجة", "display_order": 26},
            {"name": "مطروح", "name_en": "Matrouh", "code": "MAT", "region": "red_sea", "capital": "مرسى مطروح", "display_order": 27}
        ]
        
        created_count = 0
        for gov_data in governorates_data:
            gov, created = Governorate.objects.get_or_create(
                name=gov_data['name'],
                defaults=gov_data
            )
            if created or force:
                if force and not created:
                    for key, value in gov_data.items():
                        setattr(gov, key, value)
                    gov.save()
                created_count += 1
        
        self.stdout.write(f'تم تحميل {created_count} محافظة')

    def load_parties(self, force=False):
        """تحميل الأحزاب السياسية"""
        parties_data = [
            {
                "name": "حزب مستقبل وطن",
                "name_en": "Future of a Nation Party",
                "abbreviation": "مستقبل",
                "description": "حزب سياسي مصري تأسس في 2014",
                "color": "#1E3A8A",
                "display_order": 1
            },
            {
                "name": "الحزب الجمهوري الشعبي",
                "name_en": "Republican People's Party",
                "abbreviation": "جمهوري",
                "description": "حزب سياسي مصري",
                "color": "#DC2626",
                "display_order": 2
            },
            {
                "name": "حزب الوفد",
                "name_en": "Wafd Party",
                "abbreviation": "الوفد",
                "description": "أحد أقدم الأحزاب السياسية في مصر",
                "color": "#059669",
                "display_order": 3
            },
            {
                "name": "حزب المؤتمر",
                "name_en": "Conference Party",
                "abbreviation": "المؤتمر",
                "description": "حزب سياسي مصري",
                "color": "#7C3AED",
                "display_order": 4
            },
            {
                "name": "الحزب المصري الديمقراطي الاجتماعي",
                "name_en": "Egyptian Social Democratic Party",
                "abbreviation": "الديمقراطي",
                "description": "حزب سياسي مصري ليبرالي اجتماعي",
                "color": "#EA580C",
                "display_order": 5
            },
            {
                "name": "حزب التجمع الوطني التقدمي الوحدوي",
                "name_en": "National Progressive Unionist Party",
                "abbreviation": "التجمع",
                "description": "حزب يساري مصري",
                "color": "#BE185D",
                "display_order": 6
            },
            {
                "name": "حزب الشعب الجمهوري",
                "name_en": "Republican People's Party",
                "abbreviation": "الشعب",
                "description": "حزب سياسي مصري",
                "color": "#0891B2",
                "display_order": 7
            },
            {
                "name": "حزب الحرية المصري",
                "name_en": "Egyptian Freedom Party",
                "abbreviation": "الحرية",
                "description": "حزب سياسي مصري",
                "color": "#65A30D",
                "display_order": 8
            },
            {
                "name": "حزب الإصلاح والتنمية",
                "name_en": "Reform and Development Party",
                "abbreviation": "الإصلاح",
                "description": "حزب سياسي مصري",
                "color": "#C2410C",
                "display_order": 9
            },
            {
                "name": "حزب المحافظين",
                "name_en": "Conservative Party",
                "abbreviation": "المحافظين",
                "description": "حزب سياسي مصري محافظ",
                "color": "#7E22CE",
                "display_order": 10
            },
            {
                "name": "حزب الأحرار الاشتراكيين",
                "name_en": "Free Socialists Party",
                "abbreviation": "الأحرار",
                "description": "حزب سياسي مصري",
                "color": "#0D9488",
                "display_order": 11
            },
            {
                "name": "مستقل",
                "name_en": "Independent",
                "abbreviation": "مستقل",
                "description": "غير منتمي لأي حزب سياسي",
                "color": "#6B7280",
                "display_order": 12
            }
        ]
        
        created_count = 0
        for party_data in parties_data:
            party, created = Party.objects.get_or_create(
                name=party_data['name'],
                defaults=party_data
            )
            if created or force:
                if force and not created:
                    for key, value in party_data.items():
                        setattr(party, key, value)
                    party.save()
                created_count += 1
        
        self.stdout.write(f'تم تحميل {created_count} حزب سياسي')

    def load_system_settings(self, force=False):
        """تحميل إعدادات النظام الافتراضية"""
        settings_data = {
            "enable_ratings": True,
            "enable_comments": True,
            "require_login": True,
            "max_ratings_per_user_per_day": 10,
            "min_rating_interval_minutes": 5,
            "max_comment_length": 500,
            "moderate_comments": True,
            "default_display_mode": "mixed",
            "default_fake_rating": 4.5,
            "default_fake_count": 1000,
            "default_real_weight": 0.3,
            "default_fake_weight": 0.7,
            "enable_ip_tracking": True,
            "block_duplicate_ips": True,
            "auto_verify_ratings": False,
            "notify_on_new_rating": True,
            "notify_on_report": True
        }
        
        settings = RatingSettings.get_settings()
        
        if force:
            for key, value in settings_data.items():
                setattr(settings, key, value)
            settings.save()
            self.stdout.write('تم تحديث إعدادات النظام')
        else:
            self.stdout.write('إعدادات النظام موجودة مسبقاً')
