from django import forms
from .models import HardwareAsset, SoftwareLicense


class HardwareAssetForm(forms.ModelForm):

    class Meta:
        model = HardwareAsset
        fields = [
            'asset_name',
            'asset_type',
            'serial_number',
            'assigned_to',
            'purchase_date',
            'is_active',
        ]

        widgets = {
            'asset_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Dell Latitude 5420'
            }),

            'asset_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. DELL-LAP-001'
            }),

            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            }),

            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'checkbox'
            }),
        }


class SoftwareLicenseForm(forms.ModelForm):

    class Meta:
        model = SoftwareLicense

        fields = [
            'software_name',
            'license_key',
            'assigned_to',
            'expiry_date',
            'is_active',
        ]

        widgets = {
            'software_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Microsoft Office'
            }),

            'license_key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter license key'
            }),

            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            }),

            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'checkbox'
            }),
        }