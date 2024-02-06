from django.db import models


class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title
