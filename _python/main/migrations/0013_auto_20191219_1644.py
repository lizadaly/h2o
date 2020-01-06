# Generated by Django 2.2.9 on 2019-12-19 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20191219_1629'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='user',
            name='users_login_eda8f4_idx',
        ),
        migrations.RemoveIndex(
            model_name='user',
            name='users_oauth_t_1a9921_idx',
        ),
        migrations.RemoveIndex(
            model_name='user',
            name='users_persist_f5cd85_idx',
        ),
        migrations.RemoveIndex(
            model_name='user',
            name='users_tz_name_4599bd_idx',
        ),
        migrations.RemoveField(
            model_name='case',
            name='annotations_count',
        ),
        migrations.RemoveField(
            model_name='contentnode',
            name='is_alias',
        ),
        migrations.RemoveField(
            model_name='contentnode',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='textblock',
            name='annotations_count',
        ),
        migrations.RemoveField(
            model_name='textblock',
            name='enable_discussions',
        ),
        migrations.RemoveField(
            model_name='textblock',
            name='enable_feedback',
        ),
        migrations.RemoveField(
            model_name='textblock',
            name='enable_responses',
        ),
        migrations.RemoveField(
            model_name='textblock',
            name='version',
        ),
        migrations.RemoveField(
            model_name='user',
            name='canvas_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_font',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_font_size',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_show_comments',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_show_paragraph_numbers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='description',
        ),
        migrations.RemoveField(
            model_name='user',
            name='hidden_text_display',
        ),
        migrations.RemoveField(
            model_name='user',
            name='image_content_type',
        ),
        migrations.RemoveField(
            model_name='user',
            name='image_file_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='image_file_size',
        ),
        migrations.RemoveField(
            model_name='user',
            name='image_updated_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='oauth_secret',
        ),
        migrations.RemoveField(
            model_name='user',
            name='oauth_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='perishable_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='persistence_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_annotations',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_dates_details',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_export_format',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_font_face',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_font_size',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_highlights',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_links',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_paragraph_numbers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='print_titles',
        ),
        migrations.RemoveField(
            model_name='user',
            name='toc_levels',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tz_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='url',
        ),
    ]
