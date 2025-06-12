from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)  # High limit for large goals
    amount_pledged = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Matches target_amount
    
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name


class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Donation(models.Model):
    STATUS_CHOICES = [
        ('Pledged', 'Pledged'),
        ('Fulfilled', 'Fulfilled'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amount_pledged = models.DecimalField(max_digits=15, decimal_places=2)  # ✅ Increased to prevent overflow
    date_pledged = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pledged')

    def __str__(self):
        return f"{self.donor} - {self.campaign} - {self.amount_pledged}"
