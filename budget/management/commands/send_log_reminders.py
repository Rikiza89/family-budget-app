# 3. Create management/commands/send_log_reminders.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from budget.models import Family, Transaction, EmailNotificationSettings

class Command(BaseCommand):
    help = 'Send email reminders for families without recent logs'
    
    def handle(self, *args, **options):
        today = timezone.now().date()
        
        for settings in EmailNotificationSettings.objects.filter(enable_notifications=True):
            family = settings.family
            
            # Check last transaction date
            last_transaction = Transaction.objects.filter(
                family=family
            ).order_by('-date').first()
            
            if last_transaction:
                days_since = (today - last_transaction.date).days
            else:
                days_since = 999  # No transactions ever
            
            # Send reminder if needed
            if days_since >= settings.days_without_log:
                # Check if already sent recently (avoid spam)
                if settings.last_notification_sent:
                    hours_since = (timezone.now() - settings.last_notification_sent).total_seconds() / 3600
                    if hours_since < 24:
                        continue
                
                # Send email
                subject = f'家計簿記録のリマインダー - {family.name}'
                message = f'''
こんにちは、{family.name}の皆様

最後の記録から{days_since}日が経過しています。
家計簿の記録をお忘れなく！

今すぐ記録: https://yourdomain.com/quick-add/

- 家計簿アプリ
                '''
                
                try:
                    send_mail(
                        subject,
                        message,
                        None,  # Use DEFAULT_FROM_EMAIL
                        settings.get_email_list(),
                        fail_silently=False,
                    )
                    
                    settings.last_notification_sent = timezone.now()
                    settings.save()
                    
                    self.stdout.write(f'✓ Sent reminder to {family.name}')
                except Exception as e:
                    self.stdout.write(f'✗ Failed for {family.name}: {str(e)}')
