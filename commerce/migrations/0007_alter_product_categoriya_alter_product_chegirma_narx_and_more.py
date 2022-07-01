# Generated by Django 4.0.3 on 2022-06-29 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0006_alter_product_kilogramm_alter_product_litri_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categoriya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mahsulot', to='commerce.categoriya'),
        ),
        migrations.AlterField(
            model_name='product',
            name='chegirma_narx',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.CreateModel(
            name='Rasmi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_field', models.FileField(blank=True, null=True, upload_to='')),
                ('title', models.CharField(max_length=2500, null=True)),
                ('rasmlar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rasmlari', to='commerce.product')),
            ],
        ),
    ]
