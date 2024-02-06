from django.contrib import admin

from todos.models import TodoItem


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ("title", "completed_on")
    search_fields = ("title",)
