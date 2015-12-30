from django.contrib import admin

# Register your models here.
from .models import Tweet, TweetPic
from .forms import TweetAdminForm

class TweetPicInLine(admin.TabularInline):
    model = TweetPic
    extra = 0

class TweetAdmin(admin.ModelAdmin):
    list_display = ["id", "twitter_id", "user", "text", "created_at"]
    ordering = ['-created_at']
    form = TweetAdminForm
    inlines = [TweetPicInLine]

class TweetPicAdmin(admin.ModelAdmin):
    list_display = ["id", "picture"]

admin.site.register(Tweet, TweetAdmin)
admin.site.register(TweetPic, TweetPicAdmin)
