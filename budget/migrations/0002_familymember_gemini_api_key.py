from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='familymember',
            name='gemini_api_key',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Gemini API Key'),
        ),
    ]
