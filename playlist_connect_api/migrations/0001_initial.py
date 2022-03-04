# Generated by Django 2.2 on 2022-03-04 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistPairs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apple_token_1', models.CharField(max_length=128)),
                ('apple_token_2', models.CharField(max_length=128)),
                ('apple_token_3', models.CharField(max_length=128)),
                ('spotify_token_1', models.CharField(max_length=128)),
                ('spotify_token_2', models.CharField(max_length=128)),
                ('spotify_token_3', models.CharField(max_length=128)),
                ('spotify_refresh_1', models.CharField(max_length=128)),
                ('spotify_refresh_2', models.CharField(max_length=128)),
                ('apple_playlist_id', models.CharField(max_length=255)),
                ('spotify_playlist_id', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
