from typing import Any

from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, View
from django_htmx.http import retarget
from render_block import render_block_to_string

from todos.forms import TodoItemForm
from todos.models import TodoItem


class HtmxResponseClass(TemplateResponse):
    def __init__(self, htmx_template_block: str | None = None, *args, **kwargs):
        self.htmx_template_block = htmx_template_block
        super().__init__(*args, **kwargs)

    @property
    def rendered_content(self):
        context = self.resolve_context(self.context_data)
        if self._request.htmx and self.htmx_template_block:
            return render_block_to_string(
                self.template_name,
                block_name=self.htmx_template_block,
                context=self.context_data,
                request=self._request,
            )
        template = self.resolve_template(self.template_name)
        return template.render(context, self._request)


class HtmxTemplateResponseMixin:
    response_class = HtmxResponseClass
    htmx_template_block = None

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            htmx_template_block=self.htmx_template_block,
            **response_kwargs,
        )


class TodoItemListView(HtmxTemplateResponseMixin, ListView):
    model = TodoItem
    template_name = "todos/todoitem_list.html"
    context_object_name = "todoitems"
    ordering = ["-id"]
    htmx_template_block = "object_list_block"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = TodoItemForm()
        return context


class TodoItemCreateView(HtmxTemplateResponseMixin, CreateView):
    form_class = TodoItemForm
    template_name = "todos/todoitem_list.html"
    htmx_template_block = "form_block"
    http_method_names = ["post"]
    success_url = reverse_lazy("todos:todoitem-list")

    def form_invalid(self, form: forms.ModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        return retarget(response, "this")


class TodoItemDeleteView(DeleteView):
    model = TodoItem
    success_url = reverse_lazy("todos:todoitem-list")
    http_method_names = ["post"]


class TodoMarkComplete(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        todoitem = TodoItem.objects.get(pk=kwargs["pk"])
        todoitem.completed_on = timezone.now()
        todoitem.save()
        return redirect("todos:todoitem-list")
