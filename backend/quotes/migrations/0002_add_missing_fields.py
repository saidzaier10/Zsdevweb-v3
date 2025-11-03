from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='signer_name',
            field=models.CharField(max_length=200, blank=True, null=True, verbose_name="Nom du signataire"),
        ),
        migrations.AddField(
            model_name='quote',
            name='rejection_reason',
            field=models.TextField(blank=True, verbose_name="Raison du refus"),
        ),
        migrations.AddField(
            model_name='quote',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='created_quotes',
                to=settings.AUTH_USER_MODEL,
                verbose_name="Créé par"
            ),
        ),
    ]
