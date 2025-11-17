from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import uuid
from datetime import timedelta

class Family(models.Model):
    """家族グループ"""
    name = models.CharField(max_length=100, verbose_name="家族名")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "家族"
        verbose_name_plural = "家族"
    
    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    """家族メンバー"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    nickname = models.CharField(max_length=50, verbose_name="ニックネーム")
    
    class Meta:
        verbose_name = "家族メンバー"
        verbose_name_plural = "家族メンバー"
    
    def __str__(self):
        return f"{self.nickname} ({self.family.name})"

class FamilyInvite(models.Model):
    """家族への招待コード"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='invites')
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_by = models.ForeignKey(FamilyMember, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_invites')
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "招待"
        verbose_name_plural = "招待"
    
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
        ('expense', '支出'),
        ('income', '収入'),
    ]
    
    name = models.CharField(max_length=50, verbose_name="カテゴリー名")
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, verbose_name="種類")
    is_insurance_saving = models.BooleanField(
        default=False, 
        verbose_name="保険（積立）",
        help_text="保険型の積立の場合はチェック"
    )
    icon = models.CharField(max_length=50, blank=True, verbose_name="アイコン")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='categories')
    
    class Meta:
        verbose_name = "カテゴリー"
        verbose_name_plural = "カテゴリー"
        unique_together = ['name', 'family']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class PaymentMethod(models.Model):
    """支払方法"""
    METHOD_TYPES = [
        ('cash', '現金'),
        ('credit', 'クレジットカード'),
        ('ic', 'ICカード'),
        ('qr', 'QR決済'),
        ('bank', '銀行振込'),
        ('other', 'その他'),
    ]
    
    name = models.CharField(max_length=50, verbose_name="支払方法名")
    method_type = models.CharField(max_length=10, choices=METHOD_TYPES, verbose_name="種類")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='payment_methods')
    
    class Meta:
        verbose_name = "支払方法"
        verbose_name_plural = "支払方法"
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """収支取引"""
    TRANSACTION_TYPES = [
        ('income', '収入'),
        ('expense', '支出'),
    ]
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='transactions')
    member = models.ForeignKey(FamilyMember, on_delete=models.SET_NULL, null=True, verbose_name="登録者")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="種類")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="カテゴリー")
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="金額")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="支払方法")
    date = models.DateField(default=timezone.now, verbose_name="日付")
    description = models.CharField(max_length=200, blank=True, verbose_name="メモ")
    receipt_image = models.ImageField(upload_to='receipts/%Y/%m/', blank=True, null=True, verbose_name="レシート")
    is_recurring = models.BooleanField(default=False, verbose_name="固定費")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "取引"
        verbose_name_plural = "取引"
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
    member = models.ForeignKey(FamilyMember, on_delete=models.SET_NULL, null=True, verbose_name="登録者")
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="金額")
    date = models.DateField(default=timezone.now, verbose_name="日付")
    description = models.CharField(max_length=200, blank=True, verbose_name="メモ")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "現金貯蓄"
        verbose_name_plural = "現金貯蓄"
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.date} - 貯金: ¥{self.amount:,}"

class Budget(models.Model):
    """予算設定"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="カテゴリー")
    year = models.IntegerField(verbose_name="年")
    month = models.IntegerField(verbose_name="月")
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="予算額")
    
    class Meta:
        verbose_name = "予算"
        verbose_name_plural = "予算"
        unique_together = ['family', 'category', 'year', 'month']
    
    def __str__(self):
        return f"{self.year}/{self.month} - {self.category.name}: ¥{self.amount:,}"
    
    def get_used_amount(self):
        """使用済み金額を計算"""
        from django.db.models import Sum
        result = Transaction.objects.filter(
            family=self.family,
            category=self.category,
            date__year=self.year,
            date__month=self.month
        ).aggregate(total=Sum('amount'))
        return result['total'] or Decimal('0')
    
    def get_remaining_amount(self):
        """残額を計算"""
        return self.amount - self.get_used_amount()
    
    def get_usage_percentage(self):
        """使用率を計算"""
        if self.amount == 0:
            return 0
        return (self.get_used_amount() / self.amount * 100)