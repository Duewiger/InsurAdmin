import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Insurance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True)
    line_of_business = models.CharField(null=True, blank=True, max_length=254, default="Other")
    policy_number = models.CharField(null=True, blank=True, max_length=100)
    insurer = models.CharField(null=True, blank=True, max_length=100)
    policy_holder = models.CharField(null=True, blank=True, max_length=254)
    commencement_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    policy_maturity = models.DateField(null=True, blank=True)
    payment_frequency = models.CharField(null=True, blank=True, max_length=100)
    premium = models.DecimalField(null=True, blank=True, max_digits=10,decimal_places=2)
    insurance_policy = models.FileField(upload_to="insurance_policies", blank=True)
    
    class Meta: 
        indexes = [
            models.Index(fields=["id"], name="id_index"),
        ]
        permissions = [
            ("special_status", "Can see own insurances"),
        ]
    
    def __str__(self):
        return f"{self.policy_number}"
    
    def get_absolute_url(self):
        return reverse("insurance_detail", args=[str(self.id)])