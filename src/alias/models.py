from datetime import datetime
import pytz

from django.db import models
from django.db.models import Q


"""
CREATE TABLE "alias_alias" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"alias" varchar(64) NOT NULL,
"target" varchar(24) NOT NULL,
"start" datetime NOT NULL,
"end" datetime NULL);
CREATE INDEX "alias_alias_target_05020389" ON "alias_alias" ("target");
"""


class Alias(models.Model):
    alias = models.CharField(max_length=64)

    # target --- a "soft foreign key" to slugs of other models/apps of the existing project
    target = models.SlugField(max_length=24, allow_unicode=True)

    start = models.DateTimeField(default=datetime.today)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Alias'
        verbose_name_plural = 'Aliases'

    def __str__(self):
        return f'{self.alias}, {self.target}, {self.start}, {self.end}'

    def such_object_in_db(self):
        qs = Alias.objects.filter(alias=self.alias, target=self.target, start=self.start, end=self.end)
        return qs

    def overlap_objects_in_db(self):

        MAXIMUM_DATE = datetime(2099, 12, 31, 23, 59, 36, 123456, tzinfo=pytz.UTC)

        if self.end is None:
            self.end = MAXIMUM_DATE

        qs = Alias.objects.filter(alias=self.alias, target=self.target).exclude(pk=self.pk)

        for qs_item in qs:
            if qs_item.end is None:
                qs_item.end = MAXIMUM_DATE

        qs = qs.filter(
            ~(Q(start__lt=self.start, end__lte=self.start) | Q(
                start__gte=self.end, end__gt=self.end)
              )
        )

        if self.end == MAXIMUM_DATE:
            self.end = None
        # print(qs)
        return qs

    def save(self, *args, **kwargs):
        if self.such_object_in_db():
            raise Exception('Such an Object already exists !!!')

        if self.overlap_objects_in_db():
            raise Exception('OVERLAPPING Date Range of Objects !')

        super().save(*args, **kwargs)


def get_aliases(target, point_1, point_2):
    qs = Alias.objects.filter(
        Q(target=target, start__lte=point_1, end=None) | Q(
            target=target, start__lte=point_1, end__gte=point_2))
    set_of_aliases = {i['alias'] for i in qs.values('alias')}
    return set_of_aliases


def alias_replace(existing_alias, replace_at, new_alias_value):
    existing_alias.end = replace_at
    existing_alias.save()
    target = existing_alias.target
    Alias.objects.create(alias=new_alias_value, target=target, start=replace_at, end=None)
