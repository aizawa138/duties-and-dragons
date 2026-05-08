from django.contrib import admin
from .models import Users, Bosses, CurrentFight, Duties
# Register your models here.

admin.site.register(Users)
admin.site.register(Bosses)
admin.site.register(CurrentFight)
admin.site.register(Duties)
