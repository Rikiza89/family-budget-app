from django import forms
from .models import Transaction, CashSaving, Category, PaymentMethod
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ # ⬅️ Import translation utility
import json
from django.forms.widgets import Select

class JoinFamilyForm(forms.Form):
    """家族参加フォーム"""
    # 1. Translate the label
    nickname = forms.CharField(
        max_length=50,
        label=_("あなたのニックネーム"), # ⬅️ Translated label
        widget=forms.TextInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            # 2. Translate the placeholder
            'placeholder': _('例: パパ、ママ、太郎') # ⬅️ Translated placeholder
        })
    )

class CategorySelect(Select):
    # This class handles rendering the Category choices and doesn't need changes here, 
    # but ensure Category names in the database are handled for translation if needed.
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

        if value:
            try:
                category = Category.objects.get(pk=value)
                option['attrs']['data-type'] = category.category_type
            except Category.DoesNotExist:
                pass

        return option

class QuickTransactionForm(forms.ModelForm):
    # 3. Translate field labels using the 'labels' attribute in Meta
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'amount', 'payment_method', 'date', 'description']
        labels = {
            'transaction_type': _("種類"),
            'category': _("カテゴリー"),
            'amount': _("金額"),
            'payment_method': _("支払方法"),
            'date': _("日付"),
            'description': _("メモ"),
        }
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none'
            }),
            'category': CategorySelect(attrs={
                'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
                'id': 'categorySelect'
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
                # 4. Translate the placeholder
                'placeholder': _('メモ（任意）') # ⬅️ Translated placeholder
            }),
        }

    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', None)
        super().__init__(*args, **kwargs)

        if family:
            categories = Category.objects.filter(family=family)

            # 5. Translate the default/empty choice text
            self.fields['category'].choices = [('', _('選択してください'))] + [ # ⬅️ Translated choice
                (c.id, c.name) for c in categories
            ]

            # Store categories as JSON for the template (No translation needed here as it's just data)
            self.fields['category'].widget.attrs['data-categories'] = json.dumps([
                {'id': c.id, 'name': c.name, 'type': c.category_type}
                for c in categories
            ])

            self.fields['payment_method'].queryset = PaymentMethod.objects.filter(family=family)

        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
            self.fields['transaction_type'].initial = 'expense'


class CashSavingForm(forms.ModelForm):
    """現金貯蓄フォーム"""
    # 6. Translate field labels using the 'labels' attribute in Meta
    class Meta:
        model = CashSaving
        fields = ['amount', 'date', 'description']
        labels = {
            'amount': _("金額"),
            'date': _("日付"),
            'description': _("メモ"),
        }
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
                # 7. Translate the placeholder
                'placeholder': _('メモ（例：給料から貯金）') # ⬅️ Translated placeholder
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()