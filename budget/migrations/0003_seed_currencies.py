from django.db import migrations


def seed_currencies(apps, schema_editor):
    Currency = apps.get_model('budget', 'Currency')
    db_alias = schema_editor.connection.alias
    currencies = [
        {'code': 'JPY', 'name': 'Japanese Yen',  'symbol': '¥', 'exchange_rate': 1.0},
        {'code': 'USD', 'name': 'US Dollar',      'symbol': '$', 'exchange_rate': 0.0065},
        {'code': 'EUR', 'name': 'Euro',            'symbol': '€', 'exchange_rate': 0.0060},
        {'code': 'GBP', 'name': 'British Pound',  'symbol': '£', 'exchange_rate': 0.0053},
        {'code': 'CNY', 'name': 'Chinese Yuan',   'symbol': '¥', 'exchange_rate': 0.048},
        {'code': 'KRW', 'name': 'Korean Won',     'symbol': '₩', 'exchange_rate': 9.0},
        {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': 'S$', 'exchange_rate': 0.0088},
        {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$', 'exchange_rate': 0.010},
    ]
    for c in currencies:
        Currency.objects.using(db_alias).get_or_create(code=c['code'], defaults=c)


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_familymember_gemini_api_key'),
    ]

    operations = [
        migrations.RunPython(seed_currencies, migrations.RunPython.noop),
    ]
