# accounts/migrations/0005_add_uuid_id_to_document.py

import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
