# Generated by Django 5.2.4 on 2025-07-04 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FamilyMember', '0001_initial'),
        ('Question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='FamilyMember.familymember')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='Question.question')),
            ],
            options={
                'unique_together': {('question', 'member')},
            },
        ),
    ]
