from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal
from .models import (
    Family, FamilyMember, Transaction, CashSaving, 
    Category, Budget, PaymentMethod
)
import json

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
            
            messages.success(request, '✓ 登録しました')
            
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
            
            messages.success(request, '✓ 貯金を登録しました')
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
            messages.success(request, f'✓ {category.name} を登録しました')
            return redirect('dashboard')
    
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
        messages.success(request, '✓ 削除しました')
        return redirect('transaction_list')
    
    context = {
        'transaction': transaction,
    }
    
    return render(request, 'budget/confirm_delete.html', context)