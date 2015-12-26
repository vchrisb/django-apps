from django.contrib import admin

# Register your models here.
from .models import Tweet
from .forms import TweetAdminForm
class TweetAdmin(admin.ModelAdmin):
    list_display = ["user","text", "created_at"]
    form = TweetAdminForm


admin.site.register(Tweet, TweetAdmin)
