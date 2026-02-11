from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile

# 1. Define the Inline class first
# This allows the Profile fields to appear directly inside the User edit page
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'KYC Documents & Profile'
    fields = ('phone_number', 'license_front', 'license_back', 'next_of_kin_name', 'next_of_kin_phone', 'is_verified')

# 2. Define the ProfileAdmin for the standalone Profile list view
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Columns shown in the main list
    list_display = ('user', 'phone_number', 'display_license_front', 'is_verified', 'next_of_kin_name')
    
    # Filtering and searching capabilities
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'phone_number', 'next_of_kin_name')
    
    # Helper method to render the license image thumbnail
    def display_license_front(self, obj):
        if obj.license_front:
            return format_html('<img src="{}" style="width: 80px; height: auto; border-radius: 4px;" />', obj.license_front.url)
        return "No Image"
    
    display_license_front.short_description = 'License Preview'

    # Custom Admin Action for bulk verification
    actions = ['verify_profiles']

    @admin.action(description="Mark selected users as Verified")
    def verify_profiles(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} profiles were successfully verified.")

# 3. Unregister the default User admin and re-register with the Inline
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    # Adding 'is_verified' visibility to the User list is also helpful
    list_display = BaseUserAdmin.list_display + ('get_is_verified',)

    def get_is_verified(self, obj):
        return obj.profile.is_verified
    get_is_verified.boolean = True
    get_is_verified.short_description = 'Verified'