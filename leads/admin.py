from django.contrib import admin

# Register your models here.

from leads.models import Category, User, Lead, Agent, UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Category)
admin.site.register(Agent)

