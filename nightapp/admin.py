from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(login_tbl)
admin.site.register(Users)
admin.site.register(Clubs)
admin.site.register(Club_Highlights)
admin.site.register(Events)
admin.site.register(Booking)

