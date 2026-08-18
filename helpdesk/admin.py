from django.contrib import admin
from .models import HardwareAsset, SoftwareLicense



@admin.register(HardwareAsset)
class HardwareAssetAdmin(admin.ModelAdmin):
    list_display = (
        'asset_name',
        'asset_type',
        'serial_number',
        'assigned_to',
        'purchase_date',
        'is_active',
    )

    list_filter = (
        'asset_type',
        'is_active',
    )

    search_fields = (
        'asset_name',
        'serial_number',
        'assigned_to__username',
    )


@admin.register(SoftwareLicense)
class SoftwareLicenseAdmin(admin.ModelAdmin):
    list_display = (
        'software_name',
        'license_key',
        'assigned_to',
        'expiry_date',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'software_name',
        'license_key',
        'assigned_to__username',
    )
admin.site.site_header = "Ticketing"
admin.site.site_title = "Ticketing Portal"
admin.site.index_title = "IT Asset & Helpdesk Management"