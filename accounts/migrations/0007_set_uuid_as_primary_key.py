# accounts/migrations/0007_set_uuid_as_primary_key.py

import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_copy_id_to_uuid_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='id',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='uuid_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
