from django.db import models
from django.db.models import Q, OuterRef, Subquery


class CreateModelMixin(models.Model):
    create_dt = models.DateTimeField('Создание записи', auto_now_add=True)

    class Meta:
        abstract = True


class DateModelMixin(CreateModelMixin, models.Model):

    change_dt = models.DateTimeField('Изменение записи', auto_now=True)

    class Meta:
        abstract = True


class SubqueryAggregate:
    """
    Класс для агрегаций в подзапросах
    """
    def __init__(self, sub_model, aggregate, name, filters=None) -> None:
        self.sub_model = sub_model
        self.aggregate = aggregate
        self.name = name
        self.filters = filters or Q()
        super().__init__()

    def subquery(self):
        query = self.sub_model.objects.filter(
            self.filters,
            **{self.name: OuterRef('pk')},
        ).values(self.name).annotate(annotate_value=self.aggregate('pk')).values('annotate_value')
        return Subquery(query)
