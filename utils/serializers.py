from rest_framework import serializers


def get_write_only_extra(fields, exclude_fields: list = None):
    """
    При создании/редактировании будет возвращаться только id (по умолчанию)
    """
    if exclude_fields is None:
        exclude_fields = ['id']
    return {
        field: {'write_only': True}
        for field in fields
        if field not in exclude_fields
    }


class RecursiveField(serializers.Serializer):
    """
    Поле для рекурсивного вывода дерева
    """

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return self.parent.parent.__class__(value, context=self.context).data
