from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import HardwareAsset, SoftwareLicense
from .forms import HardwareAssetForm, SoftwareLicenseForm 


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'helpdesk/login.html')


@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def dashboard(request):

    if request.user.is_staff:

        hardware_count = HardwareAsset.objects.count()

        software_count = SoftwareLicense.objects.count()

        assigned_count = HardwareAsset.objects.filter(
            assigned_to__isnull=False
        ).count()

        available_count = HardwareAsset.objects.filter(
            assigned_to__isnull=True
        ).count()

        recent_assets = HardwareAsset.objects.order_by(
            '-id'
        )[:5]

    else:

        hardware_count = HardwareAsset.objects.filter(
            assigned_to=request.user
        ).count()

        software_count = SoftwareLicense.objects.filter(
            assigned_to=request.user
        ).count()

        assigned_count = hardware_count

        available_count = 0

        recent_assets = HardwareAsset.objects.filter(
            assigned_to=request.user
        ).order_by('-id')[:5]

    context = {
        'hardware_count': hardware_count,
        'software_count': software_count,
        'assigned_count': assigned_count,
        'available_count': available_count,
        'recent_assets': recent_assets,
    }

    return render(
        request,
        'helpdesk/dashboard.html',
        context
    )


@login_required
def assets(request):

    if request.user.is_staff:
        asset_list = HardwareAsset.objects.all()
    else:
        asset_list = HardwareAsset.objects.filter(
            assigned_to=request.user
        )

    return render(
        request,
        'helpdesk/assets.html',
        {
            'assets': asset_list
        }
    )


@login_required
def licenses(request):

    if request.user.is_staff:
        license_list = SoftwareLicense.objects.all()
    else:
        license_list = SoftwareLicense.objects.filter(
            assigned_to=request.user
        )

    return render(
        request,
        'helpdesk/licenses.html',
        {
            'licenses': license_list
        }
    )


@login_required
def add_asset(request):

    if not request.user.is_staff:
        messages.error(
            request,
            'Only IT Support can add assets.'
        )
        return redirect('dashboard')

    if request.method == 'POST':

        form = HardwareAssetForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Hardware asset added successfully!'
            )

            return redirect('assets')

    else:

        form = HardwareAssetForm()

    return render(
        request,
        'helpdesk/asset_form.html',
        {
            'form': form
        }
    )
@login_required
def add_software_license(request):

    if not request.user.is_staff:
        messages.error(
            request,
            'Only IT Support can add software licenses.'
        )
        return redirect('dashboard')

    if request.method == 'POST':

        form = SoftwareLicenseForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Software license added successfully!'
            )

            return redirect('licenses')

    else:

        form = SoftwareLicenseForm()

    return render(
        request,
        'helpdesk/software_license_form.html',
        {
            'form': form
        }
    )