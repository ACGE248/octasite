from django.contrib import admin

# Register your models here.
from octapply.models import University, Professor,Program

admin.site.register(Program)
admin.site.register(University)
admin.site.register(Professor)