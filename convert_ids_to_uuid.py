import uuid
from accounts.models import CustomUser
from insurances.models import Insurance

def convert_ids_to_uuid():
    # Convert CustomUser IDs to UUIDs
    for user in CustomUser.objects.all():
        user.id = uuid.uuid4()
        user.save()

    # Convert Insurance IDs to UUIDs
    for insurance in Insurance.objects.all():
        insurance.id = uuid.uuid4()
        insurance.save()

# Führe die Konvertierung aus
convert_ids_to_uuid()
