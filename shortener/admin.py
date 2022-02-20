from django.contrib import admin

from shortener.models import ShortUrl
from shortener.utils import shortit


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    readonly_fields = ("url_hash", "creator", "redirect_count")
    search_fields = ("url_hash", "full_url")

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creator = request.user
        if "full_url" in form.changed_data:
            obj.url_hash = shortit(form.cleaned_data["full_url"])

        super().save_model(request, obj, form, change)
