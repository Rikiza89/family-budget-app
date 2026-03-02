from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=5)),
                ('exchange_rate', models.DecimalField(decimal_places=4, default=1.0, max_digits=10)),
            ],
            options={'verbose_name': '通貨', 'verbose_name_plural': '通貨'},
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='家族名')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('currency', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='budget.currency', verbose_name='通貨')),
            ],
            options={'verbose_name': '家族', 'verbose_name_plural': '家族'},
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50, verbose_name='ニックネーム')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='budget.family')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': '家族メンバー', 'verbose_name_plural': '家族メンバー'},
        ),
        migrations.CreateModel(
            name='FamilyInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to='budget.family')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.familymember')),
                ('used_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='used_invites', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': '招待', 'verbose_name_plural': '招待'},
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='カテゴリー名')),
                ('category_type', models.CharField(choices=[('expense', '支出'), ('income', '収入')], max_length=10, verbose_name='種類')),
                ('is_insurance_saving', models.BooleanField(default=False, help_text='保険型の積立の場合はチェック', verbose_name='保険（積立）')),
                ('icon', models.CharField(blank=True, max_length=50, verbose_name='アイコン')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='budget.family')),
            ],
            options={
                'verbose_name': 'カテゴリー',
                'verbose_name_plural': 'カテゴリー',
                'unique_together': {('name', 'family')},
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='支払方法名')),
                ('method_type', models.CharField(choices=[('cash', '現金'), ('credit', 'クレジットカード'), ('ic', 'ICカード'), ('qr', 'QR決済'), ('bank', '銀行振込'), ('other', 'その他')], max_length=10, verbose_name='種類')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to='budget.family')),
            ],
            options={'verbose_name': '支払方法', 'verbose_name_plural': '支払方法'},
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('income', '収入'), ('expense', '支出')], max_length=10, verbose_name='種類')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='金額')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='日付')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='メモ')),
                ('receipt_image', models.ImageField(blank=True, null=True, upload_to='receipts/%Y/%m/', verbose_name='レシート')),
                ('is_recurring', models.BooleanField(default=False, verbose_name='固定費')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='budget.category', verbose_name='カテゴリー')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='budget.family')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.familymember', verbose_name='登録者')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.paymentmethod', verbose_name='支払方法')),
            ],
            options={
                'verbose_name': '取引',
                'verbose_name_plural': '取引',
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CashSaving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='金額')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='日付')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='メモ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_savings', to='budget.family')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.familymember', verbose_name='登録者')),
            ],
            options={
                'verbose_name': '現金貯蓄',
                'verbose_name_plural': '現金貯蓄',
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='年')),
                ('month', models.IntegerField(verbose_name='月')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='予算額')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.category', verbose_name='カテゴリー')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='budget.family')),
            ],
            options={
                'verbose_name': '予算',
                'verbose_name_plural': '予算',
                'unique_together': {('family', 'category', 'year', 'month')},
            },
        ),
        migrations.CreateModel(
            name='RecurringTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('income', '収入'), ('expense', '支出')], max_length=10, verbose_name='種類')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='金額')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='メモ')),
                ('frequency', models.CharField(choices=[('daily', '毎日'), ('weekly', '毎週'), ('monthly', '毎月'), ('yearly', '毎年')], max_length=10, verbose_name='頻度')),
                ('start_date', models.DateField(verbose_name='開始日')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='終了日')),
                ('day_of_month', models.IntegerField(blank=True, help_text='月次の場合は1-31', null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='有効')),
                ('last_generated', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='budget.category', verbose_name='カテゴリー')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurring_templates', to='budget.family')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.familymember')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.paymentmethod', verbose_name='支払方法')),
            ],
            options={'verbose_name': '定期取引', 'verbose_name_plural': '定期取引'},
        ),
        migrations.CreateModel(
            name='EmailNotificationSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable_notifications', models.BooleanField(default=True, verbose_name='通知を有効にする')),
                ('days_without_log', models.IntegerField(default=3, help_text='何日間記録がない場合に通知', verbose_name='未記録日数')),
                ('notification_emails', models.TextField(help_text='1行1メールアドレス', verbose_name='通知先メールアドレス')),
                ('last_notification_sent', models.DateTimeField(blank=True, null=True)),
                ('family', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email_settings', to='budget.family')),
            ],
            options={'verbose_name': 'メール通知設定'},
        ),
    ]
