from django.core.management.base import BaseCommand
from budget.models import Currency

class Command(BaseCommand):
    help = "Create default currencies (JPY, USD, EUR) if they do not exist."

    def handle(self, *args, **kwargs):
        defaults = [
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥", "exchange_rate": 1.0},
            {"code": "USD", "name": "US Dollar", "symbol": "$", "exchange_rate": 0.0065},
            {"code": "EUR", "name": "Euro", "symbol": "€", "exchange_rate": 0.0060},
            {'code': 'GBP', 'name': 'British Pound',  'symbol': '£', 'exchange_rate': 0.0053},
            {'code': 'CNY', 'name': 'Chinese Yuan',   'symbol': '¥', 'exchange_rate': 0.048},
            {'code': 'KRW', 'name': 'Korean Won',     'symbol': '₩', 'exchange_rate': 9.0},
            {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': 'S$', 'exchange_rate': 0.0088},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$', 'exchange_rate': 0.010},
        ]

        for data in defaults:
            obj, created = Currency.objects.get_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                    "symbol": data["symbol"],
                    "exchange_rate": data["exchange_rate"],
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.code}"))
            else:
                self.stdout.write(self.style.WARNING(f"Exists already: {obj.code}"))

