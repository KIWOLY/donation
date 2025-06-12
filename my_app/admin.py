from django.contrib import admin
from .models import Campaign, Donor, Donation

admin.site.register(Campaign)
admin.site.register(Donor)
admin.site.register(Donation)