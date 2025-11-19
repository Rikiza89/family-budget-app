# admin.py
from django.contrib import admin
from .models import (
    Family, FamilyMember, Category, PaymentMethod,
    Transaction, CashSaving, Budget, RecurringTemplate, EmailNotificationSettings
)

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'member_count']
    search_fields = ['name']

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'メンバー数'

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'user', 'family']
    list_filter = ['family']
    search_fields = ['nickname', 'user__username']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_insurance_saving', 'family', 'icon']
    list_filter = ['category_type', 'is_insurance_saving', 'family']
    search_fields = ['name']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'method_type', 'family']
    list_filter = ['method_type', 'family']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'transaction_type', 'category', 'amount', 'member', 'family', 'is_recurring']
    list_filter = ['transaction_type', 'date', 'family', 'category', 'is_recurring']
    search_fields = ['description', 'category__name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('基本情報', {
            'fields': ('family', 'member', 'transaction_type', 'date')
        }),
        ('金額・カテゴリー', {
            'fields': ('amount', 'category', 'payment_method')
        }),
        ('詳細', {
            'fields': ('description', 'receipt_image', 'is_recurring')
        }),
        ('システム', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # 新規作成時
            if not obj.member:
                try:
                    obj.member = request.user.familymember
                except:
                    pass
        super().save_model(request, obj, form, change)

@admin.register(CashSaving)
class CashSavingAdmin(admin.ModelAdmin):
    list_display = ['date', 'amount', 'member', 'family', 'description']
    list_filter = ['date', 'family']
    search_fields = ['description']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'category', 'amount', 'family', 'usage_display']
    list_filter = ['year', 'month', 'family', 'category']
    search_fields = ['category__name']

    def usage_display(self, obj):
        used = obj.get_used_amount()
        percentage = obj.get_usage_percentage()
        return f"¥{used:,} / ¥{obj.amount:,} ({percentage:.1f}%)"
    usage_display.short_description = '使用状況'

@admin.register(RecurringTemplate)
class RecurringTemplateAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'frequency', 'start_date', 'last_generated', 'is_active', 'family']
    list_filter = ['frequency', 'is_active', 'family']
    search_fields = ['category__name', 'description']
    readonly_fields = ['last_generated', 'created_at']

@admin.register(EmailNotificationSettings)
class EmailNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ['family', 'enable_notifications', 'days_without_log', 'last_notification_sent']
    list_filter = ['enable_notifications']

# Django Admin カスタマイズ
admin.site.site_header = '家計簿アプリ 管理画面'
admin.site.site_title = '家計簿アプリ'
admin.site.index_title = 'データ管理'