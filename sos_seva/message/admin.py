from django.contrib import admin
from .models import WhatsAppUsers, CoordinatingBodies, RankMaster
import datetime
from django.db.models import Q
from import_export import resources
from import_export.formats import base_formats
from import_export.admin import ExportMixin, ExportActionMixin
from django.utils.html import mark_safe



class WhatsAppUsersResource(resources.ModelResource):

    class Meta:
        model = WhatsAppUsers

class WhatsAppUsersAdmin(ExportActionMixin,admin.ModelAdmin):
    change_list_template = 'admin/message/WhatsAppUsers/change_list.html'
    resource_class = WhatsAppUsersResource
    list_display = ('ticket_id', 'ticket_status', 'username', 'contact_number', 'address', 'pincode', 'purpose', 'other_details', 'assigned_to', 'created')
    exclude = ('assigned_to','status', 'rank', 'opened_time', 'resolved_time', 'responded_time', 'closed_time', 'released_time')
    list_per_page = 20
    list_filter = ['ticket_status']
    search_fields = ('username', 'contact_number', 'address', 'pincode', 'purpose', 'other_details', 'created', 'assigned_to', 'ticket_status', 'assigned_to',)

    def ticket_id(self, obj):
        tick_text = '#'.join(['Ticket', str(obj.id)])
        return tick_text

    ticket_id.short_description = 'Ticket ID'

    # def ticket_id(self, obj):
    #     tick_text = '#'.join(['Ticket', str(obj.id)])
    #     return tick_text
    #
    # ticket_id.short_description = 'Ticket ID'

    # def other_details_new(self, obj):
    #     others_text = '<span>{}</span><span id="hidden_text" style="display:none">{}</span><a href="javascript:void(' \
    #                   '0)" id="show_text" onclick="show_text()">more</a><a href="javascript:void(0)" id="hide_text" ' \
    #                   'onclick="hide_text()" style="display:none">less</a>'.format(obj.other_details[0:15],
    #                                                                                obj.other_details[15:])
    #     return mark_safe(others_text)

    # ticket_id.short_description = 'Ticket ID'

    def get_queryset(self, request):
        qs = super(WhatsAppUsersAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='sos_whatsapp_view').exists() and request.user.is_staff:
            return qs
        elif request.user.is_staff:
            return qs.filter(Q(assigned_to=request.user.username) | Q(assigned_to='') | Q(assigned_to='-'))
        else:
            return qs.filter(assigned_to=request.user.username)

    def save_model(self, request, instance, form, change):
        user = request.user.username
        print(user)
        if instance.ticket_status == 'Opened':
            instance.opened_time = datetime.datetime.now()
        elif instance.ticket_status == 'Responded':
            instance.responded_time = datetime.datetime.now()
        elif instance.ticket_status == 'Resolved':
            instance.resolved_time = datetime.datetime.now()
        elif instance.ticket_status == 'Closed':
            instance.closed_time = datetime.datetime.now()
        elif instance.ticket_status == 'Submitted':
            instance.assigned_to = '-'
            instance.save()
            return instance
        if instance.remarks:
            instance.remarks = ' - By Admin: '.join([instance.remarks, user])
        if instance.assigned_to == '-' or instance.assigned_to == '':
            instance.assigned_to = user
        if instance.ticket_status == 'Released':
            instance.ticket_status = 'Submitted'
            instance.released_time = datetime.datetime.now()
            instance.assigned_to = '-'
        instance.save()
        return instance

    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,

        )
        return [f for f in formats if f().can_export()]

    class Media:
        js = ('/static/js/show_text.js',)


class CoordinatingBodiesAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'address', 'pincode', 'status', 'created']

class RankMasterAdmin(admin.ModelAdmin):
    list_display = ('rank_name', 'keywords')


admin.site.register(WhatsAppUsers, WhatsAppUsersAdmin)
admin.site.register(CoordinatingBodies, CoordinatingBodiesAdmin)
admin.site.register(RankMaster, RankMasterAdmin)




# Register your models here.
'''
from django.contrib.admin import AdminSite, ModelAdmin
class EventAdminSite(AdminSite):
    site_header = "UMSRA Events Admin"
    site_title = "UMSRA Events Admin Portal"
    index_title = "Welcome to UMSRA Researcher Events Portal"

event_admin_site = EventAdminSite(name='event_admin')

from .models import WhatsAppUsers, CoordinatingBodies, RankMaster


class WhatsAppUsersAdmin(ModelAdmin):
    list_display = ('username', 'contact_number', 'address', 'pincode', 'purpose', 'other_details', 'rank', 'created')

class CoordinatingBodiesAdmin(ModelAdmin):
    list_display = ['name', 'contact_number', 'address', 'pincode', 'status', 'created']

class RankMasterAdmin(ModelAdmin):
    list_display = ('rank_name', 'keywords')


event_admin_site.register(WhatsAppUsers, WhatsAppUsersAdmin)
event_admin_site.register(CoordinatingBodies, CoordinatingBodiesAdmin)
event_admin_site.register(RankMaster, RankMasterAdmin)
'''
