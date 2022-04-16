# Generated by Django 4.0.4 on 2022-04-15 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0006_remove_product_p_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-p_time_create',)},
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]