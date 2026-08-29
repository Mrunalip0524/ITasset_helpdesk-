from django.urls import path
from . import views


urlpatterns = [

    # Dashboard
    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    # Authentication
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Hardware Assets
    path(
        'assets/',
        views.assets,
        name='assets'
    ),

    path(
        'assets/add/',
        views.add_asset,
        name='add_asset'
    ),

    # Software Licenses
    path(
        'licenses/',
        views.licenses,
        name='licenses'
    ),

    path(
        'licenses/add/',
        views.add_software_license,
        name='add_software_license'
    ),

    # Tickets
    path(
        'tickets/',
        views.tickets,
        name='tickets'
    ),

    path(
        'tickets/add/',
        views.create_ticket,
        name='create_ticket'
    ),

    path(
        'tickets/<int:ticket_id>/status/',
        views.update_ticket_status,
        name='update_ticket_status'
    ),
]