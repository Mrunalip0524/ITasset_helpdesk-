from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import HardwareAsset, SoftwareLicense, Ticket
from .forms import HardwareAssetForm, SoftwareLicenseForm, TicketForm


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
@login_required
def create_ticket(request):

    if request.user.is_staff:
        messages.error(
            request,
            'IT Support does not raise employee tickets.'
        )
        return redirect('dashboard')

    if request.method == 'POST':

        form = TicketForm(request.POST)

        form.fields['asset'].queryset = HardwareAsset.objects.filter(
            assigned_to=request.user
        )

        if form.is_valid():

            ticket = form.save(commit=False)

            ticket.created_by = request.user

            ticket.status = 'OPEN'

            ticket.save()

            messages.success(
                request,
                'Ticket raised successfully!'
            )

            return redirect('tickets')

    else:

        form = TicketForm()

        form.fields['asset'].queryset = HardwareAsset.objects.filter(
            assigned_to=request.user
        )

    return render(
        request,
        'helpdesk/ticket_form.html',
        {
            'form': form
        }
    )

@login_required
def tickets(request):

    if request.user.is_staff:
        ticket_list = Ticket.objects.all().order_by('-id')
    else:
        ticket_list = Ticket.objects.filter(
            created_by=request.user
        ).order_by('-id')

    return render(
        request,
        'helpdesk/tickets.html',
        {
            'tickets': ticket_list
        }
    )

@login_required
def update_ticket_status(request, ticket_id):

    if not request.user.is_staff:
        messages.error(
            request,
            'Only IT Support can update ticket status.'
        )
        return redirect('tickets')

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        allowed_transitions = {
            'OPEN': ['IN_PROGRESS'],
            'IN_PROGRESS': ['RESOLVED'],
            'RESOLVED': ['CLOSED'],
            'CLOSED': [],
        }

        if new_status in allowed_transitions[ticket.status]:

            ticket.status = new_status
            ticket.save()

            messages.success(
                request,
                'Ticket status updated successfully.'
            )

        else:

            messages.error(
                request,
                'Invalid ticket status transition.'
            )

    return redirect('tickets')