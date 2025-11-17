# urls.py - Updated URL patterns
from django.urls import path
from . import views, setup_views, auth_views

urlpatterns = [
    # 認証
    path('', auth_views.landing_page, name='landing'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # 初期設定
    path('setup/profile/', setup_views.setup_profile, name='setup_profile'),
    path('setup/categories/', setup_views.setup_categories, name='setup_categories'),
    path('setup/payment-methods/', setup_views.setup_payment_methods, name='setup_payment_methods'),
    
    # ダッシュボード
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('savings/', views.savings_summary, name='savings_summary'),
    
    # クイック入力
    path('quick-add/', views.quick_add_transaction, name='quick_add_transaction'),
    path('quick-add/saving/', views.quick_add_saving, name='quick_add_saving'),
    path('preset/<int:category_id>/', views.preset_transaction, name='preset_transaction'),
    
    # 設定
    path('settings/', setup_views.settings, name='settings'),
    
    # 家族メンバー管理
    path('family/members/', setup_views.family_members, name='family_members'),
    path('family/invite/create/', setup_views.create_invite, name='create_invite'),
    path('family/invite/<int:invite_id>/delete/', setup_views.delete_invite, name='delete_invite'),
    path('family/join/<uuid:code>/', auth_views.join_family_confirm, name='join_family_confirm'),
    
    # カテゴリー管理
    path('categories/', setup_views.manage_categories, name='manage_categories'),
    path('categories/add/', setup_views.add_category, name='add_category'),
    path('categories/<int:category_id>/edit/', setup_views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', setup_views.delete_category, name='delete_category'),
    
    # 支払方法管理
    path('payment-methods/', setup_views.manage_payment_methods, name='manage_payment_methods'),
    path('payment-methods/add/', setup_views.add_payment_method, name='add_payment_method'),
    path('payment-methods/<int:method_id>/edit/', setup_views.edit_payment_method, name='edit_payment_method'),
    path('payment-methods/<int:method_id>/delete/', setup_views.delete_payment_method, name='delete_payment_method'),
    
    # 予算・エクスポート
    path('budgets/', setup_views.manage_budgets, name='manage_budgets'),
    path('export/', setup_views.export_data, name='export_data'),
    
    # 削除
    path('transaction/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
]