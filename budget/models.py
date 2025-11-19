from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid
from datetime import timedelta

class Family(models.Model):
    """家族グループ"""
    name = models.CharField(max_length=100, verbose_name=_("家族名")) # ⬅️ Translated verbose_name
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("家族") # ⬅️ Translated verbose_name
        verbose_name_plural = _("家族") # ⬅️ Translated verbose_name_plural

    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    """家族メンバー"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    nickname = models.CharField(max_length=50, verbose_name=_("ニックネーム")) # ⬅️ Translated verbose_name

    class Meta:
        verbose_name = _("家族メンバー") # ⬅️ Translated verbose_name
        verbose_name_plural = _("家族メンバー") # ⬅️ Translated verbose_name_plural

    def __str__(self):
        return f"{self.nickname} ({self.family.name})"

class FamilyInvite(models.Model):
    """家族への招待コード"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='invites')
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_by = models.ForeignKey('FamilyMember', on_delete=models.SET_NULL, null=True) # Use string reference if FamilyMember is defined later
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_invites')
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("招待") # ⬅️ Translated verbose_name
        verbose_name_plural = _("招待") # ⬅️ Translated verbose_name_plural

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.family.name} - {self.code}"

class Category(models.Model):
    """カテゴリー"""
    CATEGORY_TYPES = [
        ('expense', _('支出')), # ⬅️ Translated choice
        ('income', _('収入')), # ⬅️ Translated choice
    ]

    name = models.CharField(max_length=50, verbose_name=_("カテゴリー名")) # ⬅️ Translated verbose_name
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, verbose_name=_("種類")) # ⬅️ Translated verbose_name
    is_insurance_saving = models.BooleanField(
        default=False,
        verbose_name=_("保険（積立）"), # ⬅️ Translated verbose_name
        help_text=_("保険型の積立の場合はチェック") # ⬅️ Translated help_text
    )
    icon = models.CharField(max_length=50, blank=True, verbose_name=_("アイコン")) # ⬅️ Translated verbose_name
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name = _("カテゴリー") # ⬅️ Translated verbose_name
        verbose_name_plural = _("カテゴリー") # ⬅️ Translated verbose_name_plural
        unique_together = ['name', 'family']

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class PaymentMethod(models.Model):
    """支払方法"""
    METHOD_TYPES = [
        ('cash', _('現金')), # ⬅️ Translated choice
        ('credit', _('クレジットカード')), # ⬅️ Translated choice
        ('ic', _('ICカード')), # ⬅️ Translated choice
        ('qr', _('QR決済')), # ⬅️ Translated choice
        ('bank', _('銀行振込')), # ⬅️ Translated choice
        ('other', _('その他')), # ⬅️ Translated choice
    ]

    name = models.CharField(max_length=50, verbose_name=_("支払方法名")) # ⬅️ Translated verbose_name
    method_type = models.CharField(max_length=10, choices=METHOD_TYPES, verbose_name=_("種類")) # ⬅️ Translated verbose_name
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='payment_methods')

    class Meta:
        verbose_name = _("支払方法") # ⬅️ Translated verbose_name
        verbose_name_plural = _("支払方法") # ⬅️ Translated verbose_name_plural

    def __str__(self):
        return self.name

class Transaction(models.Model):
    """収支取引"""
    TRANSACTION_TYPES = [
        ('income', _('収入')), # ⬅️ Translated choice
        ('expense', _('支出')), # ⬅️ Translated choice
    ]

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='transactions')
    member = models.ForeignKey('FamilyMember', on_delete=models.SET_NULL, null=True, verbose_name=_("登録者")) # ⬅️ Translated verbose_name
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name=_("種類")) # ⬅️ Translated verbose_name
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_("カテゴリー")) # ⬅️ Translated verbose_name
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_("金額")) # ⬅️ Translated verbose_name
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("支払方法")) # ⬅️ Translated verbose_name
    date = models.DateField(default=timezone.now, verbose_name=_("日付")) # ⬅️ Translated verbose_name
    description = models.CharField(max_length=200, blank=True, verbose_name=_("メモ")) # ⬅️ Translated verbose_name
    receipt_image = models.ImageField(upload_to='receipts/%Y/%m/', blank=True, null=True, verbose_name=_("レシート")) # ⬅️ Translated verbose_name
    is_recurring = models.BooleanField(default=False, verbose_name=_("固定費")) # ⬅️ Translated verbose_name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("取引") # ⬅️ Translated verbose_name
        verbose_name_plural = _("取引") # ⬅️ Translated verbose_name_plural
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.category.name}: ¥{self.amount:,}"

    def is_insurance_saving(self):
        """保険型積立かどうか"""
        return self.transaction_type == 'expense' and self.category.is_insurance_saving

    def contributes_to_savings(self):
        """長期貯蓄に寄与するか（保険型積立の場合）"""
        return self.is_insurance_saving()

class CashSaving(models.Model):
    """現金貯蓄（貯金）"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='cash_savings')
    member = models.ForeignKey('FamilyMember', on_delete=models.SET_NULL, null=True, verbose_name=_("登録者")) # ⬅️ Translated verbose_name
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_("金額")) # ⬅️ Translated verbose_name
    date = models.DateField(default=timezone.now, verbose_name=_("日付")) # ⬅️ Translated verbose_name
    description = models.CharField(max_length=200, blank=True, verbose_name=_("メモ")) # ⬅️ Translated verbose_name
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("現金貯蓄") # ⬅️ Translated verbose_name
        verbose_name_plural = _("現金貯蓄") # ⬅️ Translated verbose_name_plural
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - 貯金: ¥{self.amount:,}"

class Budget(models.Model):
    """予算設定"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("カテゴリー")) # ⬅️ Translated verbose_name
    year = models.IntegerField(verbose_name=_("年")) # ⬅️ Translated verbose_name
    month = models.IntegerField(verbose_name=_("月")) # ⬅️ Translated verbose_name
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_("予算額")) # ⬅️ Translated verbose_name

    class Meta:
        verbose_name = _("予算") # ⬅️ Translated verbose_name
        verbose_name_plural = _("予算") # ⬅️ Translated verbose_name_plural
        unique_together = ['family', 'category', 'year', 'month']

    def __str__(self):
        return f"{self.year}/{self.month} - {self.category.name}: ¥{self.amount:,}"

    # ... (methods omitted for brevity)
    def get_used_amount(self):
        from django.db.models import Sum
        result = Transaction.objects.filter(
            family=self.family,
            category=self.category,
            date__year=self.year,
            date__month=self.month
        ).aggregate(total=Sum('amount'))
        return result['total'] or Decimal('0')

    def get_remaining_amount(self):
        return self.amount - self.get_used_amount()

    def get_usage_percentage(self):
        if self.amount == 0:
            return 0
        return (self.get_used_amount() / self.amount * 100)



        # Add to models.py

from dateutil.relativedelta import relativedelta

class RecurringTemplate(models.Model):
    """定期取引テンプレート"""
    FREQUENCY_CHOICES = [
        ('daily', _('毎日')), # ⬅️ Translated choice
        ('weekly', _('毎週')), # ⬅️ Translated choice
        ('monthly', _('毎月')), # ⬅️ Translated choice
        ('yearly', _('毎年')), # ⬅️ Translated choice
    ]

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='recurring_templates')
    member = models.ForeignKey('FamilyMember', on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=10, choices=Transaction.TRANSACTION_TYPES, verbose_name=_("種類")) # ⬅️ Translated verbose_name
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_("カテゴリー")) # ⬅️ Translated verbose_name
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_("金額")) # ⬅️ Translated verbose_name
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("支払方法")) # ⬅️ Translated verbose_name
    description = models.CharField(max_length=200, blank=True, verbose_name=_("メモ")) # ⬅️ Translated verbose_name

    # Recurring settings
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name=_("頻度")) # ⬅️ Translated verbose_name
    start_date = models.DateField(verbose_name=_("開始日")) # ⬅️ Translated verbose_name
    end_date = models.DateField(null=True, blank=True, verbose_name=_("終了日")) # ⬅️ Translated verbose_name
    day_of_month = models.IntegerField(null=True, blank=True, help_text=_("月次の場合は1-31")) # ⬅️ Translated help_text
    is_active = models.BooleanField(default=True, verbose_name=_("有効")) # ⬅️ Translated verbose_name
    last_generated = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("定期取引") # ⬅️ Translated verbose_name
        verbose_name_plural = _("定期取引") # ⬅️ Translated verbose_name_plural

    def __str__(self):
        return f"{self.category.name} - {self.get_frequency_display()}"

    def get_next_date(self, from_date=None):
        """Calculate next occurrence date"""
        if from_date is None:
            from_date = self.last_generated or self.start_date

        if self.frequency == 'daily':
            return from_date + timedelta(days=1)
        elif self.frequency == 'weekly':
            return from_date + timedelta(weeks=1)
        elif self.frequency == 'monthly':
            next_date = from_date + relativedelta(months=1)
            if self.day_of_month:
                try:
                    next_date = next_date.replace(day=self.day_of_month)
                except ValueError:
                    # Handle months with fewer days
                    next_date = next_date.replace(day=28)
            return next_date
        elif self.frequency == 'yearly':
            return from_date + relativedelta(years=1)

        return from_date

    def should_generate(self):
        """Check if transaction should be generated today"""
        if not self.is_active:
            return False

        today = timezone.now().date()

        if today < self.start_date:
            return False

        if self.end_date and today > self.end_date:
            return False

        if self.last_generated and self.last_generated >= today:
            return False

        next_date = self.get_next_date()
        return today >= next_date

    def generate_transaction(self):
        """Create actual transaction from template"""
        today = timezone.now().date()

        transaction = Transaction.objects.create(
            family=self.family,
            member=self.member,
            transaction_type=self.transaction_type,
            category=self.category,
            amount=self.amount,
            payment_method=self.payment_method,
            date=today,
            description=f"{self.description} (定期)",
            is_recurring=True
        )

        self.last_generated = today
        self.save()

        return transaction


class EmailNotificationSettings(models.Model):
    """メール通知設定"""
    family = models.OneToOneField(Family, on_delete=models.CASCADE, related_name='email_settings')

    # Notification preferences
    enable_notifications = models.BooleanField(default=True, verbose_name=_("通知を有効にする")) # ⬅️ Translated verbose_name
    days_without_log = models.IntegerField(default=3, verbose_name=_("未記録日数"), help_text=_("何日間記録がない場合に通知")) # ⬅️ Translated verbose_name/help_text

    # Email addresses
    notification_emails = models.TextField(verbose_name=_("通知先メールアドレス"), help_text=_("1行1メールアドレス")) # ⬅️ Translated verbose_name/help_text

    last_notification_sent = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("メール通知設定") # ⬅️ Translated verbose_name

    def get_email_list(self):
        return [email.strip() for email in self.notification_emails.split('\n') if email.strip()]
