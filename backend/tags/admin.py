from django.contrib import admin

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'color',
    )
    list_editable = ('color',)


admin.site.register(Tag, TagAdmin)
