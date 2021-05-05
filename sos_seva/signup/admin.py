from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    # autocomplete_fields = ['community']
    can_delete = False
    verbose_name_plural = 'Additional Info'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'full_name', 'email', 'get_contact', 'get_community', 'is_staff', 'is_superuser', 'is_active')
    list_select_related = ('profile',)

    def full_name(self, obj):
        full_name = ' '.join([str(obj.first_name), str(obj.last_name)])
        return full_name

    full_name.short_description = 'Full Name'

    def get_contact(self, instance):
        return instance.profile.mobile_no

    get_contact.short_description = 'Contact Number'

    def get_community(self, instance):
        return instance.profile.community

    get_community.short_description = 'Community'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)