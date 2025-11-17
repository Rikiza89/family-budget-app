from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Family, FamilyMember, Category, PaymentMethod, Budget, Transaction, FamilyInvite
from django import forms
import uuid
from django.utils import timezone

class CategoryForm(forms.ModelForm):
    """カテゴリーフォーム"""
    class Meta:
        model = Category
        fields = ['name', 'category_type', 'is_insurance_saving', 'icon']
        labels = {
            'name': 'カテゴリー名',
            'category_type': '種類',
            'is_insurance_saving': '保険積立',
            'icon': 'アイコン'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg',
                'placeholder': '例: 食費'
            }),
            'category_type': forms.Select(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg',
                'placeholder': '🍚'
            }),
            'is_insurance_saving': forms.CheckboxInput(attrs={
                'class': 'w-6 h-6'
            })
        }

class PaymentMethodForm(forms.ModelForm):
    """支払方法フォーム"""
    class Meta:
        model = PaymentMethod
        fields = ['name', 'method_type']
        labels = {
            'name': '支払方法名',
            'method_type': '種類'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg',
                'placeholder': '例: メインカード'
            }),
            'method_type': forms.Select(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg'
            })
        }

@login_required
def family_members(request):
    """家族メンバー管理"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    members = FamilyMember.objects.filter(family=family)
    active_invites = FamilyInvite.objects.filter(
        family=family,
        is_used=False,
        expires_at__gt=timezone.now()
    )
    
    context = {
        'family': family,
        'members': members,
        'active_invites': active_invites,
    }
    return render(request, 'budget/family_members.html', context)

@login_required
def create_invite(request):
    """招待コード作成"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    if request.method == 'POST':
        invite = FamilyInvite.objects.create(
            family=family,
            created_by=member
        )
        messages.success(request, '✓ 招待リンクを作成しました')
        return redirect('family_members')
    
    return render(request, 'budget/create_invite.html')

@login_required
def delete_invite(request, invite_id):
    """招待削除"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    invite = get_object_or_404(FamilyInvite, id=invite_id, family=family)
    
    if request.method == 'POST':
        invite.delete()
        messages.success(request, '✓ 招待を削除しました')
        return redirect('family_members')
    
    context = {'invite': invite}
    return render(request, 'budget/delete_invite.html', context)



@login_required
def manage_categories(request):
    """カテゴリー管理"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    categories = Category.objects.filter(family=family).order_by('category_type', 'name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'budget/manage_categories.html', context)

@login_required
def add_category(request):
    """カテゴリー追加"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.family = family
            category.save()
            messages.success(request, '✓ カテゴリーを追加しました')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    
    context = {'form': form}
    return render(request, 'budget/add_category.html', context)

@login_required
def edit_category(request, category_id):
    """カテゴリー編集"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    category = get_object_or_404(Category, id=category_id, family=family)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, '✓ カテゴリーを更新しました')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'budget/edit_category.html', context)

@login_required
def delete_category(request, category_id):
    """カテゴリー削除"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    category = get_object_or_404(Category, id=category_id, family=family)
    
    # 使用中かチェック
    transaction_count = Transaction.objects.filter(category=category).count()
    
    if request.method == 'POST':
        if transaction_count > 0:
            messages.error(request, '⚠️ このカテゴリーは取引で使用されているため削除できません')
        else:
            category.delete()
            messages.success(request, '✓ カテゴリーを削除しました')
        return redirect('manage_categories')
    
    context = {
        'category': category,
        'transaction_count': transaction_count
    }
    return render(request, 'budget/delete_category.html', context)

@login_required
def manage_payment_methods(request):
    """支払方法管理"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    payment_methods = PaymentMethod.objects.filter(family=family).order_by('method_type', 'name')
    
    context = {
        'payment_methods': payment_methods,
    }
    return render(request, 'budget/manage_payment_methods.html', context)

@login_required
def add_payment_method(request):
    """支払方法追加"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            method = form.save(commit=False)
            method.family = family
            method.save()
            messages.success(request, '✓ 支払方法を追加しました')
            return redirect('manage_payment_methods')
    else:
        form = PaymentMethodForm()
    
    context = {'form': form}
    return render(request, 'budget/add_payment_method.html', context)

@login_required
def edit_payment_method(request, method_id):
    """支払方法編集"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    method = get_object_or_404(PaymentMethod, id=method_id, family=family)
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=method)
        if form.is_valid():
            form.save()
            messages.success(request, '✓ 支払方法を更新しました')
            return redirect('manage_payment_methods')
    else:
        form = PaymentMethodForm(instance=method)
    
    context = {
        'form': form,
        'method': method
    }
    return render(request, 'budget/edit_payment_method.html', context)

@login_required
def delete_payment_method(request, method_id):
    """支払方法削除"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    method = get_object_or_404(PaymentMethod, id=method_id, family=family)
    
    # 使用中かチェック
    transaction_count = Transaction.objects.filter(payment_method=method).count()
    
    if request.method == 'POST':
        if transaction_count > 0:
            messages.error(request, '⚠️ この支払方法は取引で使用されているため削除できません')
        else:
            method.delete()
            messages.success(request, '✓ 支払方法を削除しました')
        return redirect('manage_payment_methods')
    
    context = {
        'method': method,
        'transaction_count': transaction_count
    }
    return render(request, 'budget/delete_payment_method.html', context)

class FamilySetupForm(forms.ModelForm):
    """家族登録フォーム"""
    nickname = forms.CharField(
        max_length=50,
        label="あなたのニックネーム",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border-2 border-gray-300 rounded-lg',
            'placeholder': '例: パパ、ママ'
        })
    )
    
    class Meta:
        model = Family
        fields = ['name']
        labels = {'name': '家族名'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg',
                'placeholder': '例: 田中家'
            })
        }

class CategorySetupForm(forms.Form):
    """カテゴリー一括設定フォーム"""
    use_default = forms.BooleanField(
        required=False,
        initial=True,
        label="デフォルトカテゴリーを使用",
        widget=forms.CheckboxInput(attrs={
            'class': 'w-6 h-6'
        })
    )

class BudgetSetupForm(forms.ModelForm):
    """予算設定フォーム"""
    class Meta:
        model = Budget
        fields = ['category', 'amount']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full p-3 border-2 border-gray-300 rounded-lg',
                'placeholder': '月額予算',
                'inputmode': 'numeric'
            })
        }

@login_required
def setup_profile(request):
    """初期プロフィール設定"""
    # すでに設定済みならダッシュボードへ
    try:
        member = request.user.familymember
        return redirect('dashboard')
    except FamilyMember.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = FamilySetupForm(request.POST)
        if form.is_valid():
            # 家族作成
            family = form.save()
            
            # メンバー作成
            FamilyMember.objects.create(
                user=request.user,
                family=family,
                nickname=form.cleaned_data['nickname']
            )
            
            messages.success(request, '✓ プロフィールを作成しました')
            return redirect('setup_categories')
    else:
        form = FamilySetupForm()
    
    context = {'form': form}
    return render(request, 'budget/setup_profile.html', context)

@login_required
def setup_categories(request):
    """カテゴリー初期設定"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    # すでにカテゴリーがある場合はスキップ
    if Category.objects.filter(family=family).exists():
        return redirect('setup_payment_methods')
    
    if request.method == 'POST':
        form = CategorySetupForm(request.POST)
        if form.is_valid() and form.cleaned_data['use_default']:
            # デフォルトカテゴリー作成
            create_default_categories(family)
            messages.success(request, '✓ カテゴリーを設定しました')
            return redirect('setup_payment_methods')
    else:
        form = CategorySetupForm()
    
    context = {'form': form}
    return render(request, 'budget/setup_categories.html', context)

@login_required
def setup_payment_methods(request):
    """支払方法初期設定"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    # すでに支払方法がある場合はスキップ
    if PaymentMethod.objects.filter(family=family).exists():
        return redirect('dashboard')
    
    if request.method == 'POST':
        # デフォルト支払方法作成
        create_default_payment_methods(family)
        messages.success(request, '✓ セットアップ完了！')
        return redirect('dashboard')
    
    return render(request, 'budget/setup_payment_methods.html')

def create_default_categories(family):
    """デフォルトカテゴリー作成"""
    expense_categories = [
        ('食費', False, '🍚'),
        ('外食', False, '🍽️'),
        ('日用品', False, '🧴'),
        ('交通費', False, '🚃'),
        ('光熱費', False, '💡'),
        ('通信費', False, '📱'),
        ('医療費', False, '🏥'),
        ('娯楽', False, '🎮'),
        ('衣服', False, '👕'),
        ('保険（積立）', True, '📋'),  # 保険型積立
        ('その他', False, '📦'),
    ]
    
    for name, is_insurance, icon in expense_categories:
        Category.objects.create(
            family=family,
            name=name,
            category_type='expense',
            is_insurance_saving=is_insurance,
            icon=icon
        )
    
    income_categories = [
        ('給料', False, '💰'),
        ('賞与', False, '🎁'),
        ('副収入', False, '💵'),
        ('その他収入', False, '📈'),
    ]
    
    for name, _, icon in income_categories:
        Category.objects.create(
            family=family,
            name=name,
            category_type='income',
            icon=icon
        )

def create_default_payment_methods(family):
    """デフォルト支払方法作成"""
    methods = [
        ('現金', 'cash'),
        ('クレジットカード', 'credit'),
        ('交通系ICカード', 'ic'),
        ('PayPay', 'qr'),
        ('銀行振込', 'bank'),
    ]
    
    for name, method_type in methods:
        PaymentMethod.objects.create(
            family=family,
            name=name,
            method_type=method_type
        )

@login_required
def settings(request):
    """設定画面"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    categories = Category.objects.filter(family=family).order_by('category_type', 'name')
    payment_methods = PaymentMethod.objects.filter(family=family)
    family_members = FamilyMember.objects.filter(family=family)
    
    context = {
        'family': family,
        'categories': categories,
        'payment_methods': payment_methods,
        'family_members': family_members,
    }
    
    return render(request, 'budget/settings.html', context)

@login_required
def manage_budgets(request):
    """予算管理"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    from django.utils import timezone
    today = timezone.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        
        if category_id and amount:
            Budget.objects.update_or_create(
                family=family,
                category_id=category_id,
                year=year,
                month=month,
                defaults={'amount': amount}
            )
            messages.success(request, '✓ 予算を設定しました')
            return redirect('manage_budgets')
    
    budgets = Budget.objects.filter(
        family=family,
        year=year,
        month=month
    ).select_related('category')
    
    # 未設定のカテゴリー
    expense_categories = Category.objects.filter(
        family=family,
        category_type='expense'
    ).exclude(
        id__in=budgets.values_list('category_id', flat=True)
    )
    
    context = {
        'budgets': budgets,
        'expense_categories': expense_categories,
        'year': year,
        'month': month,
    }
    
    return render(request, 'budget/manage_budgets.html', context)

@login_required
def export_data(request):
    """データエクスポート"""
    try:
        member = request.user.familymember
        family = member.family
    except FamilyMember.DoesNotExist:
        return redirect('setup_profile')
    
    if request.method == 'POST':
        export_type = request.POST.get('type', 'csv')
        year = request.POST.get('year')
        month = request.POST.get('month')
        
        # CSV/Excel エクスポート処理
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="transactions_{year}_{month}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['日付', '種類', 'カテゴリー', '金額', '支払方法', 'メモ', '登録者'])
        
        transactions = Transaction.objects.filter(
            family=family,
            date__year=year,
            date__month=month
        ).select_related('category', 'payment_method', 'member')
        
        for t in transactions:
            writer.writerow([
                t.date,
                t.get_transaction_type_display(),
                t.category.name,
                t.amount,
                t.payment_method.name if t.payment_method else '',
                t.description,
                t.member.nickname if t.member else ''
            ])
        
        return response
    
    return render(request, 'budget/export_data.html')