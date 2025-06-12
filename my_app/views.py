from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Campaign, Donor, Donation


def home(request):
    campaigns = Campaign.objects.all()
    return render(request, 'home.html', {'campaigns': campaigns})


def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST' and request.user.is_authenticated:
        try:
            amount = Decimal(request.POST.get('amount', '0'))

            if amount <= 0:
                messages.error(request, 'Pledge amount must be greater than zero!')
            elif amount > Decimal('999999999999.99'):
                messages.error(request, 'Donation amount is too large!')
            elif campaign.amount_pledged + amount > campaign.target_amount:
                messages.error(request, 'Donation exceeds campaign target!')
            else:
                donor = Donor.objects.get(user=request.user)

                Donation.objects.create(
                    donor=donor,
                    campaign=campaign,
                    amount_pledged=amount,
                    status='Pledged'
                )

                campaign.amount_pledged += amount
                campaign.save()

                messages.success(request, 'Your pledge has been recorded!')
                return redirect('campaign_detail', pk=campaign.pk)

        except (InvalidOperation, ValueError):
            messages.error(request, 'Invalid pledge amount!')
        except ObjectDoesNotExist:
            messages.error(request, 'Donor profile not found!')

    # Calculate remaining amount
    remaining = campaign.target_amount - campaign.amount_pledged

    return render(request, 'campaign.html', {'campaign': campaign, 'remaining': remaining})


@login_required
def donor_dashboard(request):
    try:
        donor = Donor.objects.get(user=request.user)
        donations = Donation.objects.filter(donor=donor)
        return render(request, 'donor.html', {'donor': donor, 'donations': donations})
    except ObjectDoesNotExist:
        messages.error(request, 'Donor profile not found! Please contact support.')
        return redirect('home')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            if not all([username, email, phone_number, password1, password2]):
                messages.error(request, 'All fields are required!')
            elif password1 != password2:
                messages.error(request, 'Passwords do not match!')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already in use!')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                Donor.objects.create(user=user, phone_number=phone_number)
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('donor_dashboard')
        except ValueError:
            messages.error(request, 'Invalid input! Please check your details.')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required!')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('donor_dashboard')
            else:
                messages.error(request, 'Invalid credentials!')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')
