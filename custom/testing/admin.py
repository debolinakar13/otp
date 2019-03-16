from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User
from .forms import UserCreationForm 

User = get_user_model()

#class UserAdmin(BaseUserAdmin):
#    
#    add_form = UserCreationForm
#
#    list_display = ['phone', 'is_admin']
#    list_filter = ('is_admin')
#
#    fieldsets = (
#            (None, {'fields':('phone', 'password')}),
#            ('Permissions', {'fields': ('is_admin',)})
#        )
#    
#    search_fields = ('phone')
#    ordering = ('phone')
#    filter_horizontal = ()

admin.site.register(User)
admin.site.unregister(Group)
