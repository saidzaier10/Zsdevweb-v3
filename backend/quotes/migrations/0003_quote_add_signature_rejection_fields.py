# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_quote_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='signer_name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nom du signataire'),
        ),
        migrations.AddField(
            model_name='quote',
            name='rejection_reason',
            field=models.TextField(blank=True, verbose_name='Raison du refus'),
        ),
    ]
