from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

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

    path(
        'assets/',
        views.assets,
        name='assets'
    ),

    path(
        'licenses/',
        views.licenses,
        name='licenses'
    ),

    path(
        'assets/add/',
        views.add_asset,
        name='add_asset'
    ),

    path(
        'licenses/add/',
        views.add_software_license,
        name='add_software_license'
    ),

]