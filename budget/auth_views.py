from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError
from .models import FamilyInvite, FamilyMember
from .forms import JoinFamilyForm
from django.utils import timezone
# Import translation utilities
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext # Alias for gettext, used for messages.

class SignUpForm(forms.Form):
    """新規登録フォーム"""
    username = forms.CharField(
        max_length=150,
        label=_("ユーザー名"), # ⬅️ Translated
        widget=forms.TextInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': _('ユーザー名（英数字）') # ⬅️ Translated
        })
    )
    email = forms.EmailField(
        label=_("メールアドレス"), # ⬅️ Translated
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': _('メールアドレス（任意）') # ⬅️ Translated
        })
    )
    password1 = forms.CharField(
        label=_("パスワード"), # ⬅️ Translated
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': _('パスワード（8文字以上）') # ⬅️ Translated
        })
    )
    password2 = forms.CharField(
        label=_("パスワード（確認）"), # ⬅️ Translated
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': _('パスワードを再入力') # ⬅️ Translated
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            # Use gettext for immediate error messages
            raise ValidationError(gettext('このユーザー名は既に使用されています')) # ⬅️ Translated
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(gettext('パスワードが一致しません')) # ⬅️ Translated

        if password1 and len(password1) < 8:
            raise ValidationError(gettext('パスワードは8文字以上にしてください')) # ⬅️ Translated

        return cleaned_data

class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    username = forms.CharField(
        max_length=150,
        label=_("ユーザー名"), # ⬅️ Translated
        widget=forms.TextInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': _('ユーザー名'), # ⬅️ Translated
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label=_("パスワード"), # ⬅️ Translated
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': _('パスワード'), # ⬅️ Translated
            'autocomplete': 'current-password'
        })
    )

def signup_view(request):
    """新規登録"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    # 招待コードチェック
    invite_code = request.GET.get('invite')
    invite = None

    if invite_code:  # Only check if invite code exists
        try:
            invite = FamilyInvite.objects.get(code=invite_code)
            if not invite.is_valid():
                messages.warning(request, gettext('この招待リンクは有効期限切れです')) # ⬅️ Translated
                invite = None
        except FamilyInvite.DoesNotExist:
            messages.warning(request, gettext('招待コードが見つかりません')) # ⬅️ Translated
        except Exception:
            pass  # Silently fail for invalid formats

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data.get('email', '')
            password = form.cleaned_data['password1']

            # ユーザー作成
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # 自動ログイン
            login(request, user)

            # 招待経由の場合
            if invite and invite.is_valid():
                return redirect('join_family_confirm', code=invite.code)

            messages.success(request, gettext('✓ アカウントを作成しました')) # ⬅️ Translated
            return redirect('setup_profile')
    else:
        form = SignUpForm()

    context = {
        'form': form,
        'invite': invite
    }
    return render(request, 'budget/signup.html', context)

@login_required
def join_family_confirm(request, code):
    """家族参加確認"""
    try:
        invite = FamilyInvite.objects.get(code=code)
    except FamilyInvite.DoesNotExist:
        messages.error(request, gettext('⚠️ 招待コードが見つかりません')) # ⬅️ Translated
        return redirect('setup_profile')

    if not invite.is_valid():
        messages.error(request, gettext('⚠️ この招待リンクは無効です')) # ⬅️ Translated
        return redirect('setup_profile')

    # すでに家族に所属している場合
    try:
        existing_member = request.user.familymember
        messages.info(request, gettext('すでに家族に所属しています')) # ⬅️ Translated
        return redirect('dashboard')
    except FamilyMember.DoesNotExist:
        pass

    if request.method == 'POST':
        form = JoinFamilyForm(request.POST)
        if form.is_valid():
            # 家族メンバー作成
            FamilyMember.objects.create(
                user=request.user,
                family=invite.family,
                nickname=form.cleaned_data['nickname']
            )

            # 招待を使用済みに
            invite.is_used = True
            invite.used_by = request.user
            invite.used_at = timezone.now()
            invite.save()
            
            # Note: f-string needs explicit translation function, use gettext for dynamic messages
            messages.success(request, gettext('✓ %(family_name)sに参加しました！') % {'family_name': invite.family.name}) # ⬅️ Translated and dynamic
            return redirect('dashboard')
    else:
        form = JoinFamilyForm()

    context = {
        'form': form,
        'invite': invite
    }
    return render(request, 'budget/join_family_confirm.html', context)

def login_view(request):
    """ログイン"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                
                # Note: f-string needs explicit translation function, use gettext for dynamic messages
                messages.success(request, gettext('✓ おかえりなさい、%(username)sさん') % {'username': user.username}) # ⬅️ Translated and dynamic

                # 次のページへ
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
        else:
            messages.error(request, gettext('ユーザー名またはパスワードが正しくありません')) # ⬅️ Translated
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'budget/login.html', context)

def logout_view(request):
    """ログアウト"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, gettext('✓ ログアウトしました')) # ⬅️ Translated
        return redirect('login')

    return render(request, 'budget/logout_confirm.html')

def landing_page(request):
    """ランディングページ"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'budget/landing.html')