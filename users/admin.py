from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# from guardian.admin import GuardedModelAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.

# class CustomUserAdmin(GuardedModelAdmin):
#     add_form = CustomUserCreationForm
#     readonly_fields = ('public_id',)

#     form = CustomUserChangeForm
#     model = CustomUser

#     list_display = ('public_id', 'username', 'email', 'team', 'role', 'first_name', 'last_name', 'is_active', 'is_staff')
#     list_filter = ('public_id', 'username', 'email', 'team', 'role', 'first_name', 'last_name', 'is_active', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name')}),
#         # (_('Team info'), {'fields': ('team', 'role')}),
#         (_('User Details'), {'fields': ('team', 'picture_url', 'role', 'offline_since',
#                                         'zen_mode_until', 'timezone_offset', 'status', 'location')}),
#         (_('Account Details'), {'fields': ('created_date', 'original_created_date', 'deleted_date')}),
#         (_('Admin Settings'), {'fields': ('teammate_joined_email', 'teammate_left_email')}),
#         (_('User Settings'), {'fields': ('current_team_show_app', 'current_team_show_status', 'other_team_show_app', 'other_team_show_status',
#                                          'auto_mute', 'notification_teammate_online', 'notification_receive_file', 'notification_system_text', 'notification_sound')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active'),
#         }),
#     )
#     search_fields = ('username', 'email', 'role', 'first_name', 'last_name')
#     ordering = ('email',)
#     # inlines = (AccountInline, )

#     def save_model(self, request, obj, form, change):
#         if not change and (not form.cleaned_data['password'] or not obj.has_usable_password()):
#             random_password = CustomUser.objects.make_random_password(
#                 length=16, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
#             obj.set_password(random_password)

#         super(CustomUserAdmin, self).save_model(request, obj, form, change)


# class GuestUserAdmin(GuardedModelAdmin):
#     model = GuestUser


# admin.site.unregister(CustomUser)
admin.site.register(CustomUser)
# admin.site.register(GuestUser, GuestUserAdmin)
