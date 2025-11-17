from django import forms
from .models import Transaction, CashSaving, Category, PaymentMethod
from django.utils import timezone

class JoinFamilyForm(forms.Form):
    """家族参加フォーム"""
    nickname = forms.CharField(
        max_length=50,
        label="あなたのニックネーム",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': '例: パパ、ママ、太郎'
        })
    )
    
class QuickTransactionForm(forms.ModelForm):
    """クイック支出入力フォーム（モバイル最適化）"""
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'amount', 'payment_method', 'date', 'description']
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full p-4 text-2xl font-bold border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none'
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
                'placeholder': 'メモ（任意）'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', None)
        super().__init__(*args, **kwargs)
        
        if family:
            self.fields['category'].queryset = Category.objects.filter(family=family)
            self.fields['payment_method'].queryset = PaymentMethod.objects.filter(family=family)
        
        # デフォルト値設定
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
            self.fields['transaction_type'].initial = 'expense'

class CashSavingForm(forms.ModelForm):
    """現金貯蓄フォーム"""
    class Meta:
        model = CashSaving
        fields = ['amount', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full p-4 text-2xl font-bold border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none'
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
                'placeholder': 'メモ（例：給料から貯金）'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()