# Generated by Django 4.2.10 on 2024-07-20 06:39

from django.db import migrations, models
import django.db.models.deletion
import django_spanner


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(default=django_spanner.gen_rand_int64, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('Buyer', 'Buyer'), ('Realtor', 'Realtor')], max_length=10)),
                ('profile_picture', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchFilter',
            fields=[
                ('filter_id', models.AutoField(default=django_spanner.gen_rand_int64, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=150)),
                ('price_min', models.FloatField()),
                ('price_max', models.FloatField()),
                ('property_type', models.CharField(max_length=50)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('area_min', models.FloatField()),
                ('area_max', models.FloatField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.user')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('property_id', models.AutoField(default=django_spanner.gen_rand_int64, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('location', models.CharField(max_length=255)),
                ('property_type', models.CharField(max_length=100)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('area', models.FloatField()),
                ('listed_at', models.DateField(auto_now_add=True)),
                ('realtor', models.ForeignKey(limit_choices_to={'user_type': 'Realtor'}, on_delete=django.db.models.deletion.CASCADE, to='property.user')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(default=django_spanner.gen_rand_int64, primary_key=True, serialize=False)),
                ('bio', models.TextField()),
                ('address', models.CharField(max_length=255)),
                ('preferences', models.TextField()),
                ('updated_at', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='property.user')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('photo_id', models.AutoField(default=django_spanner.gen_rand_int64, primary_key=True, serialize=False)),
                ('url', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(default=django_spanner.gen_rand_int64, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('sent_at', models.DateField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='property.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='property.user')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(default=django_spanner.gen_rand_int64, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.user')),
            ],
        ),
    ]
