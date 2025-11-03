from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_quote_rejection_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='signer_name',
            field=models.CharField(max_length=200, blank=True, null=True),
        ),
    ]
