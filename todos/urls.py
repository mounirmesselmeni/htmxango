from django.urls import path

from todos import views

urlpatterns = [
    path("", views.TodoItemListView.as_view(), name="todoitem-list"),
    path("create/", views.TodoItemCreateView.as_view(), name="todoitem-create"),
    path(
        "<int:pk>/mark-complete/",
        views.TodoMarkComplete.as_view(),
        name="todoitem-mark-complete",
    ),
    path(
        "<int:pk>/delete/", views.TodoItemDeleteView.as_view(), name="todoitem-delete"
    ),
]

app_name = "todos"
