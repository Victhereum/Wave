from uuid import uuid4

import auto_prefetch
from django.db import models
from django.db.models.query import QuerySet


class VisibleManager(auto_prefetch.Manager):
    def get_queryset(self) -> QuerySet:
        """filters queryset to return only visible items"""
        return super().get_queryset().filter(visible=True)


class TimeBasedModel(auto_prefetch.Model):
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

    objects = auto_prefetch.Manager()
    items = VisibleManager()


class TitleTimeBasedModel(TimeBasedModel):
    title = models.CharField(max_length=50, null=True, blank=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ["title", "created_at"]

    def __str__(self):
        return self.title


def default_uiid():
    return uuid4().hex


class UIDTimeBasedModel(TimeBasedModel):
    id = models.CharField(
        primary_key=True,
        default=default_uiid,
        max_length=120,
        editable=False,
        unique=True,
    )

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return self.id
