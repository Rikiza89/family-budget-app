from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal
from .models import (
    Family, FamilyMember, Transaction, CashSaving,
    Category, Budget, PaymentMethod,EmailNotificationSettings
)
import json
from django.utils.translation import gettext as _

@login_required
def dashboard(request):
    """ダッシュボード - 月次サマリー"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    # 現在の年月
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # 月の範囲
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date()
    else:
        end_date = datetime(year, month + 1, 1).date()

    # 今月の収入
    income_total = Transaction.objects.filter(
        family=family,
        transaction_type='income',
        date__gte=start_date,
        date__lt=end_date
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # 今月の支出（保険型積立を含む）
    expense_total = Transaction.objects.filter(
        family=family,
        transaction_type='expense',
        date__gte=start_date,
        date__lt=end_date
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # 今月の現金貯蓄
    cash_saving_total = CashSaving.objects.filter(
        family=family,
        date__gte=start_date,
        date__lt=end_date
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # 今月の保険型積立
    insurance_saving_total = Transaction.objects.filter(
        family=family,
        transaction_type='expense',
        category__is_insurance_saving=True,
        date__gte=start_date,
        date__lt=end_date
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # 月次収支
    balance = income_total - expense_total - cash_saving_total

    # 総貯蓄額（長期）
    total_savings = cash_saving_total + insurance_saving_total

    # カテゴリー別支出
    category_expenses = Transaction.objects.filter(
        family=family,
        transaction_type='expense',
        date__gte=start_date,
        date__lt=end_date
    ).values('category__name', 'category__is_insurance_saving').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # 予算対比
    budgets = Budget.objects.filter(
        family=family,
        year=year,
        month=month
    ).select_related('category')

    budget_data = []
    for budget in budgets:
        used = budget.get_used_amount()
        remaining = budget.get_remaining_amount()
        percentage = budget.get_usage_percentage()

        budget_data.append({
            'category': budget.category.name,
            'budget': budget.amount,
            'used': used,
            'remaining': remaining,
            'percentage': percentage,
            'is_over': remaining < 0
        })

    # 最近の取引
    recent_transactions = Transaction.objects.filter(
        family=family
    ).select_related('category', 'member', 'payment_method')[:10]

    # グラフ用データ（過去6ヶ月）
    chart_data = get_chart_data(family, year, month)

    # 前月・次月リンク
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        'family': family,
        'member': member,
        'year': year,
        'month': month,
        'income_total': income_total,
        'expense_total': expense_total,
        'cash_saving_total': cash_saving_total,
        'insurance_saving_total': insurance_saving_total,
        'balance': balance,
        'total_savings': total_savings,
        'category_expenses': category_expenses,
        'budget_data': budget_data,
        'recent_transactions': recent_transactions,
        'chart_data': json.dumps(chart_data),
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }

    return render(request, 'budget/dashboard.html', context)

def get_chart_data(family, current_year, current_month):
    """過去6ヶ月のグラフデータ生成"""
    months_data = []

    for i in range(5, -1, -1):
        month = current_month - i
        year = current_year

        while month < 1:
            month += 12
            year -= 1

        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()

        income = Transaction.objects.filter(
            family=family,
            transaction_type='income',
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        expense = Transaction.objects.filter(
            family=family,
            transaction_type='expense',
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        cash_saving = CashSaving.objects.filter(
            family=family,
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        insurance_saving = Transaction.objects.filter(
            family=family,
            transaction_type='expense',
            category__is_insurance_saving=True,
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        months_data.append({
            'label': f"{year}/{month}",
            'income': float(income),
            'expense': float(expense),
            'savings': float(cash_saving + insurance_saving)
        })

    return {
        'labels': [m['label'] for m in months_data],
        'income': [m['income'] for m in months_data],
        'expense': [m['expense'] for m in months_data],
        'savings': [m['savings'] for m in months_data]
    }

@login_required
def transaction_list(request):
    """取引一覧"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    transactions = Transaction.objects.filter(
        family=family
    ).select_related('category', 'member', 'payment_method')

    # フィルター
    trans_type = request.GET.get('type')
    category_id = request.GET.get('category')
    month = request.GET.get('month')

    if trans_type:
        transactions = transactions.filter(transaction_type=trans_type)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if month:
        year, m = month.split('-')
        transactions = transactions.filter(date__year=year, date__month=m)

    context = {
        'transactions': transactions[:100],
        'categories': Category.objects.filter(family=family),
    }

    return render(request, 'budget/transaction_list.html', context)

@login_required
def savings_summary(request):
    """貯蓄サマリー"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    # 総現金貯蓄
    total_cash_savings = CashSaving.objects.filter(
        family=family
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # 総保険型積立
    total_insurance_savings = Transaction.objects.filter(
        family=family,
        transaction_type='expense',
        category__is_insurance_saving=True
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # 合計貯蓄
    grand_total = total_cash_savings + total_insurance_savings

    # 最近の貯蓄記録
    recent_cash_savings = CashSaving.objects.filter(
        family=family
    ).order_by('-date')[:10]

    recent_insurance_savings = Transaction.objects.filter(
        family=family,
        category__is_insurance_saving=True
    ).select_related('category').order_by('-date')[:10]

    context = {
        'total_cash_savings': total_cash_savings,
        'total_insurance_savings': total_insurance_savings,
        'grand_total': grand_total,
        'recent_cash_savings': recent_cash_savings,
        'recent_insurance_savings': recent_insurance_savings,
    }

    return render(request, 'budget/savings_summary.html', context)

from django.contrib import messages
from .forms import QuickTransactionForm, CashSavingForm

@login_required
def quick_add_transaction(request):
    """クイック取引追加（モバイル最適化）"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    if request.method == 'POST':
        form = QuickTransactionForm(request.POST, request.FILES, family=family)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.family = family
            transaction.member = member
            transaction.save()

            messages.success(request, _('✓ 登録しました'))

            # モバイルの場合はダッシュボードへ、それ以外は同じページ
            if request.POST.get('stay'):
                return redirect('quick_add_transaction')
            return redirect('dashboard')
    else:
        # クエリパラメータから初期値設定
        initial = {}
        if request.GET.get('type'):
            initial['transaction_type'] = request.GET.get('type')
        if request.GET.get('category'):
            initial['category'] = request.GET.get('category')

        form = QuickTransactionForm(family=family, initial=initial)

    # よく使うカテゴリー（最近の取引から）
    frequent_categories = Transaction.objects.filter(
        family=family
    ).values('category__id', 'category__name').annotate(
        count=models.Count('id')
    ).order_by('-count')[:6]

    context = {
        'form': form,
        'frequent_categories': frequent_categories,
    }

    return render(request, 'budget/quick_add.html', context)

@login_required
def quick_add_saving(request):
    """クイック貯蓄追加"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    if request.method == 'POST':
        form = CashSavingForm(request.POST)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.family = family
            saving.member = member
            saving.save()

            messages.success(request, _('✓ 貯金を登録しました'))
            return redirect('savings_summary')
    else:
        form = CashSavingForm()

    context = {
        'form': form,
    }

    return render(request, 'budget/quick_add_saving.html', context)

@login_required
def preset_transaction(request, category_id):
    """プリセット取引（2タップ入力）"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    category = get_object_or_404(Category, id=category_id, family=family)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method_id = request.POST.get('payment_method')

        if amount:
            transaction = Transaction.objects.create(
                family=family,
                member=member,
                transaction_type=category.category_type,
                category=category,
                amount=amount,
                payment_method_id=payment_method_id if payment_method_id else None,
                date=timezone.now().date()
            )
            messages.success(request, _('✓ %(category_name)s を登録しました') % {'category_name': category.name}) # ⬅️ Translated (using placeholder for safety)
            return redirect('dashboard')
# ...

    # よく使う支払方法
    common_methods = PaymentMethod.objects.filter(family=family)[:4]

    # 最近の同カテゴリー金額
    recent_amounts = Transaction.objects.filter(
        family=family,
        category=category
    ).values_list('amount', flat=True).distinct()[:3]

    context = {
        'category': category,
        'common_methods': common_methods,
        'recent_amounts': recent_amounts,
    }

    return render(request, 'budget/preset_transaction.html', context)

@login_required
def delete_transaction(request, transaction_id):
    """取引削除"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    transaction = get_object_or_404(Transaction, id=transaction_id, family=family)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, _('✓ 削除しました'))
        return redirect('transaction_list')

    context = {
        'transaction': transaction,
    }

    return render(request, 'budget/confirm_delete.html', context)



    # Add to views.py or create recurring_views.py

from django.contrib.auth.decorators import login_required
from .models import RecurringTemplate
from django import forms

class RecurringTemplateForm(forms.ModelForm):
    class Meta:
        model = RecurringTemplate
        fields = ['transaction_type', 'category', 'amount', 'payment_method',
                  'description', 'frequency', 'start_date', 'end_date', 'day_of_month']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'w-full p-3 border-2 rounded-lg'}),
            'category': forms.Select(attrs={'class': 'w-full p-3 border-2 rounded-lg'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full p-3 border-2 rounded-lg'}),
            'payment_method': forms.Select(attrs={'class': 'w-full p-3 border-2 rounded-lg'}),
            'description': forms.TextInput(attrs={'class': 'w-full p-3 border-2 rounded-lg'}),
            'frequency': forms.Select(attrs={'class': 'w-full p-3 border-2 rounded-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-3 border-2 rounded-lg'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-3 border-2 rounded-lg'}),
            'day_of_month': forms.NumberInput(attrs={'class': 'w-full p-3 border-2 rounded-lg', 'min': 1, 'max': 31}),
        }

@login_required
def manage_recurring(request):
    """定期取引管理"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    templates = RecurringTemplate.objects.filter(family=family, is_active=True)

    context = {
        'templates': templates,
    }
    return render(request, 'budget/manage_recurring.html', context)

@login_required
def add_recurring(request):
    """定期取引追加"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    if request.method == 'POST':
        form = RecurringTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.family = family
            template.member = member
            template.save()
            messages.success(request, _('✓ 定期取引を追加しました'))
            return redirect('manage_recurring')
    else:
        form = RecurringTemplateForm()
        form.fields['category'].queryset = Category.objects.filter(family=family)
        form.fields['payment_method'].queryset = PaymentMethod.objects.filter(family=family)

    context = {'form': form}
    return render(request, 'budget/add_recurring.html', context)

@login_required
def generate_all_recurring(request):
    """一括定期取引生成"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    if request.method == 'POST':
        templates = RecurringTemplate.objects.filter(family=family, is_active=True)
        generated_count = 0

        for template in templates:
            if template.should_generate():
                template.generate_transaction()
                generated_count += 1

        if generated_count > 0:
            # Use string formatting for translation
            messages.success(request, _('✓ %(count)s件の定期取引を記録しました') % {'count': generated_count}) # ⬅️ Translated
        else:
            messages.info(request, _('記録すべき定期取引はありません')) # ⬅️ Translated

        return redirect('manage_recurring')

    # Show confirmation page
    templates = RecurringTemplate.objects.filter(family=family, is_active=True)
    pending = [t for t in templates if t.should_generate()]

    context = {
        'pending_templates': pending,
    }
    return render(request, 'budget/confirm_generate_recurring.html', context)

@login_required
def toggle_recurring(request, template_id):
    """定期取引の有効/無効切り替え"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    template = get_object_or_404(RecurringTemplate, id=template_id, family=family)
    template.is_active = not template.is_active
    template.save()

    status = _('有効') if template.is_active else _('無効')
    messages.success(request, _('✓ 定期取引を%(status)sにしました') % {'status': status}) # ⬅️ Translated
    return redirect('manage_recurring')



from django.contrib.auth.decorators import login_required

@login_required
def email_notification_settings(request):
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    settings, created = EmailNotificationSettings.objects.get_or_create(family=family)

    if request.method == 'POST':
        settings.enable_notifications = request.POST.get('enable_notifications') == 'on'
        settings.days_without_log = int(request.POST.get('days_without_log', 3))
        settings.notification_emails = request.POST.get('notification_emails', '')
        settings.save()

        messages.success(request, _('✓ メール通知設定を更新しました'))
        return redirect('settings')

    context = {'settings': settings}
    return render(request, 'budget/email_settings.html', context)

# Feature 3: Future Forecast Charts


@login_required
def forecast_view(request):
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    # Get years parameter (default 5, max 60)
    forecast_years = min(int(request.GET.get('years', 5)), 60)
    year_options = list(range(1, 61))
    # Historical data (last 12 months)
    today = timezone.now().date()
    twelve_months_ago = today - timedelta(days=365)

    # Initialize sums and counters
    sum_income = Decimal('0')
    sum_expense = Decimal('0')
    sum_cash_saving = Decimal('0')
    sum_insurance = Decimal('0')

    months_with_income = 0
    months_with_expense = 0
    months_with_cash_saving = 0
    months_with_insurance = 0

    monthly_data = []

    for i in range(12):
        month_start = twelve_months_ago + timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)

        income = Transaction.objects.filter(
            family=family, transaction_type='income',
            date__gte=month_start, date__lt=month_end
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        expense = Transaction.objects.filter(
            family=family, transaction_type='expense',
            date__gte=month_start, date__lt=month_end
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        cash_saving = CashSaving.objects.filter(
            family=family, date__gte=month_start, date__lt=month_end
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        insurance = Transaction.objects.filter(
            family=family, category__is_insurance_saving=True,
            date__gte=month_start, date__lt=month_end
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        # Add to sums and increment counters if > 0
        if income > 0:
            sum_income += income
            months_with_income += 1
        if expense > 0:
            sum_expense += expense
            months_with_expense += 1
        if cash_saving > 0:
            sum_cash_saving += cash_saving
            months_with_cash_saving += 1
        if insurance > 0:
            sum_insurance += insurance
            months_with_insurance += 1

        monthly_data.append({
            'month': month_start.strftime('%Y/%m'),
            'income': float(income),
            'expense': float(expense),
            'cash_saving': float(cash_saving),
            'insurance': float(insurance)
        })

    # Calculate averages based on months with data
    avg_income = float(sum_income / months_with_income) if months_with_income else 0
    avg_expense = float(sum_expense / months_with_expense) if months_with_expense else 0
    avg_cash_saving = float(sum_cash_saving / 12)
    avg_insurance = float(sum_insurance / months_with_insurance) if months_with_insurance else 0

    # Current totals
    total_cash_savings = CashSaving.objects.filter(family=family).aggregate(
        total=models.Sum('amount'))['total'] or Decimal('0')

    total_insurance = Transaction.objects.filter(
        family=family, category__is_insurance_saving=True
    ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

    # Generate forecast
    forecast_data = []

    cumulative_cash = float(total_cash_savings)
    cumulative_insurance = float(total_insurance)

    for i in range(1, forecast_years * 12 + 1):  # Monthly for N years
        future_month = today + timedelta(days=30*i)
        cumulative_cash = cumulative_cash + avg_cash_saving + avg_income - avg_expense
        cumulative_insurance = cumulative_insurance + avg_insurance

        if i % 12 == 0:  # Store yearly data
            forecast_data.append({
                'year': future_month.year,
                'cash_savings': cumulative_cash,
                'insurance_savings': cumulative_insurance,
                'total_savings': cumulative_cash + cumulative_insurance
            })

    context = {
        'forecast_data': json.dumps(forecast_data),
        'avg_cash_saving': avg_cash_saving,
        'avg_insurance': avg_insurance * 12,
        'total_cash_savings': float(total_cash_savings),
        'total_insurance': float(total_insurance),
        'forecast_years': forecast_years,
        'year_options': year_options,  # ← ADD THIS
    }

    return render(request, 'budget/forecast.html', context)


from django.http import JsonResponse
from django.conf import settings

def manifest(request):
    """PWA Manifest"""
    manifest_data = {
        "name": "家計簿アプリ",
        "short_name": "家計簿",
        "description": "家族で使える家計簿管理アプリ",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#2563eb",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/static/images/icons/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }
    return JsonResponse(manifest_data)

# Add to views.py or create ai_analysis.py

import google.generativeai as genai
from django.conf import settings
from datetime import timedelta

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# @login_required
# def ai_spending_analysis(request):
#     try:
#         member = request.user.familymember
#         family = member.family
#     except FamilyMember.DoesNotExist:
#         return redirect('setup_profile')

#     # Get last 3 months data
#     today = timezone.now().date()
#     three_months_ago = today - timedelta(days=90)

#     transactions = Transaction.objects.filter(
#         family=family,
#         date__gte=three_months_ago
#     ).select_related('category')

#     # Prepare data for AI
#     category_totals = {}
#     for trans in transactions:
#         cat_name = trans.category.name
#         if cat_name not in category_totals:
#             category_totals[cat_name] = {
#                 'total': 0,
#                 'count': 0,
#                 'type': trans.transaction_type
#             }
#         category_totals[cat_name]['total'] += float(trans.amount)
#         category_totals[cat_name]['count'] += 1

#     # Calculate totals
#     total_income = sum(v['total'] for k, v in category_totals.items() if v['type'] == 'income')
#     total_expense = sum(v['total'] for k, v in category_totals.items() if v['type'] == 'expense')

#     # Build prompt
#     currency_symbol = family.get_currency_symbol()
#     prompt = f"""
# あなたは家計アドバイザーです。以下のデータを分析し、日本語で改善提案をしてください。

# 【期間】過去3ヶ月
# 【通貨】{family.currency.code}
# 【総収入】{currency_symbol}{total_income:,.0f}
# 【総支出】{currency_symbol}{total_expense:,.0f}

# 【カテゴリー別支出】
# """
#     for cat_name, data in category_totals.items():
#         if data['type'] == 'expense':
#             prompt += f"- {cat_name}: {currency_symbol}{data['total']:,.0f} ({data['count']}回)\n"

#     prompt += """

# 以下の形式で分析してください：
# 1. 支出の特徴（3つ）
# 2. 改善提案（3つ）
# 3. 節約できそうな項目（具体的な金額目標付き）
# 4. 良い点（1つ）

# 簡潔に、箇条書きで回答してください。
# """

#     try:
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = model.generate_content(prompt)
#         ai_analysis = response.text
#     except Exception as e:
#         ai_analysis = f"AI分析エラー: {str(e)}"

#     context = {
#         'ai_analysis': ai_analysis,
#         'total_income': total_income,
#         'total_expense': total_expense,
#         'category_totals': category_totals,
#         'currency_symbol': currency_symbol
#     }

#     return render(request, 'budget/ai_analysis.html', context)

import markdown
from django.utils.safestring import mark_safe

@login_required
def ai_spending_analysis(request):
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')

    # Get last 3 months data
    today = timezone.now().date()
    three_months_ago = today - timedelta(days=90)

    transactions = Transaction.objects.filter(
        family=family,
        date__gte=three_months_ago
    ).select_related('category')

    # Prepare data for AI
    category_totals = {}
    for trans in transactions:
        cat_name = trans.category.name
        if cat_name not in category_totals:
            category_totals[cat_name] = {
                'total': 0,
                'count': 0,
                'type': trans.transaction_type
            }
        category_totals[cat_name]['total'] += float(trans.amount)
        category_totals[cat_name]['count'] += 1

    # --- Improved Calculation Logic ---
    total_income = sum(v['total'] for k, v in category_totals.items() if v['type'] == 'income')
    total_expense = sum(v['total'] for k, v in category_totals.items() if v['type'] == 'expense')

    # Calculate averages and rates for better context
    balance = total_income - total_expense
    savings_rate = (balance / total_income * 100) if total_income > 0 else 0

    # Convert 3-month totals to monthly averages for the prompt
    monthly_income = total_income / 3
    monthly_expense = total_expense / 3

    currency_symbol = family.get_currency_symbol()

    # --- Improved Prompt ---
    prompt = f"""
あなたは経験豊富なファイナンシャルプランナー（FP）です。
以下の家計データ（過去3ヶ月の実績）に基づき、具体的で実行可能な家計改善のアドバイスを日本語で作成してください。

## 📊 家計概要（3ヶ月合計）
- **期間:** 90日間
- **通貨:** {family.currency.code}
- **総収入:** {currency_symbol}{total_income:,.0f}
- **総支出:** {currency_symbol}{total_expense:,.0f}
- **収支バランス:** {currency_symbol}{balance:,.0f}
- **貯蓄率:** {savings_rate:.1f}%

## 📅 月平均換算（目安）
- **月収:** 約 {currency_symbol}{monthly_income:,.0f}
- **月支出:** 約 {currency_symbol}{monthly_expense:,.0f}

## 📂 カテゴリー別支出詳細（金額順）
"""
    # Sort categories by amount (highest first) so AI focuses on big spenders
    sorted_expenses = sorted(
        [(k, v) for k, v in category_totals.items() if v['type'] == 'expense'],
        key=lambda x: x[1]['total'],
        reverse=True
    )

    for cat_name, data in sorted_expenses:
        monthly_avg = data['total'] / 3
        percent_of_total = (data['total'] / total_expense * 100) if total_expense > 0 else 0
        prompt += f"- **{cat_name}**: 総額 {currency_symbol}{data['total']:,.0f} (月平均 {currency_symbol}{monthly_avg:,.0f}) | 支出全体の{percent_of_total:.1f}% | {data['count']}回\n"

    prompt += """

## 📝 分析依頼内容
以下のフォーマットに従って、Markdown形式で出力してください。
トーンは「親身で、かつ論理的」にお願いします。

### 1. 🔍 現状分析（3つのポイント）
数字に基づいた客観的な分析を3点挙げてください。
（例：「食費が支出全体のXX%を占めており、理想的な比率を超えています」など）

### 2. 💡 具体的な改善提案（3つのステップ）
「少し頑張れば実行できる」レベルの具体的なアクションを3つ提案してください。
抽象的なアドバイスではなく、具体的な行動（例：「コンビニ利用を週1回減らす」）を提示してください。

### 3. 💰 今すぐ見直すべき項目（節約ターゲット）
最も削減効果が高いカテゴリーを1つ選び、翌月の具体的な削減目標金額（数値）とその理由を提示してください。

### 4. 🌟 素晴らしい点（Goodポイント）
家計管理の中で評価できる点、健全な数字、または努力が見られる点を1つ褒めてください。

"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        ai_raw = extract_text(response)

        if not ai_raw:
            ai_raw = "⚠️ AIが有効なテキストを返しませんでした。（safety / 空の応答）"

        ai_analysis = mark_safe(markdown.markdown(ai_raw))

    except Exception as e:
        ai_analysis = f"AI分析エラー: {str(e)}"


    context = {
        'ai_analysis': ai_analysis,
        'total_income': total_income,
        'total_expense': total_expense,
        'category_totals': category_totals,
        'currency_symbol': currency_symbol
    }

    return render(request, 'budget/ai_analysis.html', context)

# --- Safe extraction of Gemini response ---
def extract_text(resp):
    if not resp:
        return ""
    if hasattr(resp, "text") and resp.text:
        return resp.text
    # Fallback: extract from candidates manually
    if resp.candidates:
        for c in resp.candidates:
            if c.content and c.content.parts:
                return "".join(
                    p.text for p in c.content.parts if hasattr(p, "text") and p.text
                )
    return ""
