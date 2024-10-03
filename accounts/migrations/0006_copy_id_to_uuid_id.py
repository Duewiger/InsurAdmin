# accounts/migrations/0006_copy_id_to_uuid_id.py

import uuid
from django.db import migrations

def copy_id_to_uuid_id(apps, schema_editor):
    Document = apps.get_model('accounts', 'Document')
    for document in Document.objects.all():
        document.uuid_id = uuid.UUID(int=document.id)
        document.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_add_uuid_id_to_document'),
    ]

    operations = [
        migrations.RunPython(copy_id_to_uuid_id),
    ]
