from django.contrib import admin
from .models import Researcher
from .models import ResearchItem

# admin.site.register(ResearchItem)
# # Simple registrations

# # Custom admin for Researcher
# class ResearcherAdmin(admin.ModelAdmin):
#     list_display = ('last_name', 'first_name', 'affiliation_institution', 'get_email')
    
#     def get_email(self, obj):
#         return obj.user.email
#     get_email.short_description = 'Email'  # Optional: Sets a column header

#     search_fields = ('user__email', 'last_name', 'first_name', 'user__email')  # Assuming you want to include email in search

# admin.site.register(Researcher, ResearcherAdmin)

class ResearchItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'subject')
    list_filter = ('published_date', 'author', 'subject')
    search_fields = ('title', 'description', 'subject')
    
    def get_queryset(self, request):
        """
        Limit objects displayed in the admin list to those created by the user,
        unless the user is a superuser.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(uploaded_by=request.user) 

    def save_model(self, request, obj, form, change):
        """
        Automatically set the author of the object to the current user
        for new objects.
        """
        if not obj.pk:
            # For new objects, set the author to the current user
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        """
        Return True if the current user is the author of the object or a superuser.
        """
        if not obj:
            # In the list view, so defer to the standard behaviour
            return super().has_change_permission(request, obj)
        return obj.uploaded_by == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return super().has_delete_permission(request, obj)
        return obj.uploaded_by == request.user or request.user.is_superuser
    
from django.contrib.admin.sites import AlreadyRegistered    
# Attempt to register ResearchItem with its admin class
try:
    admin.site.register(ResearchItem, ResearchItemAdmin)
except AlreadyRegistered:
    pass  # Model is already registered, do nothing
# @admin.register(Researcher)
# class ResearcherAdmin(admin.ModelAdmin):
#     list_display = ('user', 'affiliation_institution', 'position_title')
#     list_filter = ('affiliation_institution',)
#     search_fields = ('user__username', 'user__email', 'affiliation_institution', 'position_title')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Researcher

# Define an inline admin descriptor for the Researcher model
# which acts a bit like a singleton
class ResearcherInline(admin.StackedInline):
    model = Researcher
    can_delete = False
    verbose_name_plural = 'researcher'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ResearcherInline, )
    # Assuming you're customizing the admin form for the User model
    # Here's an example of how you might want to customize fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    def get_inline_instances(self, request, obj=None):
            if not obj:
                return list()
            return super(UserAdmin, self).get_inline_instances(request, obj)

    # Adding 'is_active' to list_display if not already included
    list_display = list(BaseUserAdmin.list_display) + ['is_active'] if 'is_active' not in BaseUserAdmin.list_display else BaseUserAdmin.list_display
    
    # Making 'is_active' editable from the list view
    list_editable = list(BaseUserAdmin.list_editable) + ['is_active'] if 'is_active' not in BaseUserAdmin.list_editable else list(BaseUserAdmin.list_editable)


# Attempt to registe with its admin class
try:
    admin.site.register(User, UserAdmin)
except AlreadyRegistered:
    pass  # Model is already registered, do nothing