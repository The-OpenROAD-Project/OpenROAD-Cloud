from django.contrib import admin

from .models import Design, Flow

admin.site.register(Design)
admin.site.register(Flow)

admin.site.site_header = 'OpenROAD Flow'
admin.site.site_title = 'OpenROAD Admin'
admin.site.index_title = 'OpenROAD Admin'
