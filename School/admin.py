from django.contrib import admin
from School.models import School, Class, Session
from django_admin_relation_links import AdminChangeLinksMixin
# Register your models here.


admin.site.register(School)
admin.site.register(Class)
admin.site.register(Session)
