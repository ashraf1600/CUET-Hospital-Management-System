from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from userauths import models

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'user_type', 'account_status', 'is_active', 'date_joined']
    list_filter = ['user_type', 'account_status', 'is_active', 'date_joined']
    search_fields = ['email', 'username']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Account Type', {'fields': ('user_type',)}),
        ('Verification Status', {'fields': ('account_status', 'rejection_reason')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'user_type', 'password1', 'password2'),
        }),
    )
    
    actions = ['verify_accounts', 'reject_accounts']
    
    def verify_accounts(self, request, queryset):
        updated = queryset.update(account_status='Verified')
        self.message_user(request, f'{updated} accounts verified successfully.')
    verify_accounts.short_description = "Verify selected accounts"
    
    def reject_accounts(self, request, queryset):
        for user in queryset:
            user.account_status = 'Rejected'
            user.rejection_reason = 'Rejected by admin'
            user.save()
        self.message_user(request, f'{queryset.count()} accounts rejected.')
    reject_accounts.short_description = "Reject selected accounts"

admin.site.register(models.User, CustomUserAdmin)