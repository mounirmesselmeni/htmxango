from typing import Any

from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, View
from django_htmx.http import retarget
from render_block import render_block_to_string

from todos.forms import TodoItemForm
from todos.models import TodoItem


class TodoItemListView(ListView):
    model = TodoItem
    template_name = "todos/todoitem_list.html"
    context_object_name = "todoitems"
    ordering = ["-id"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = TodoItemForm()
        return context

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        if self.request.htmx:
            return HttpResponse(
                render_block_to_string(
                    self.template_name,
                    block_name="object_list_block",
                    context=context,
                    request=self.request,
                )
            )
        return super().render_to_response(context, **response_kwargs)


class TodoItemCreateView(CreateView):
    form_class = TodoItemForm
    template_name = "todos/todoitem_form.html"
    success_url = reverse_lazy("todos:todoitem-list")

    def form_invalid(self, form: forms.ModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        return retarget(response, "this")


class TodoItemDeleteView(DeleteView):
    model = TodoItem
    template_name = "todos/todoitem_confirm_delete.html"
    success_url = reverse_lazy("todos:todoitem-list")


class TodoMarkComplete(View):
    def post(self, request, *args, **kwargs):
        todoitem = TodoItem.objects.get(pk=kwargs["pk"])
        todoitem.completed_on = timezone.now()
        todoitem.save()
        return redirect("todos:todoitem-list")
