from django.utils import timezone


def generate_uniq_code():
    return str(timezone.now().timestamp()).replace('.', '')


def get_paths(path: str, depth: int, steplen: int, exclude_self=True):
    """
    Разбивает и собирает все связанные пути
    """
    if not exclude_self:
        depth += 1
    parent_paths = []
    for num in range(1, depth):
        parent_paths.append(path[:steplen * num])
    return parent_paths


class SerializeTree:
    """
    Сериализация объектов в дерево

    [
        {
            "data": {
                "name": "Категория 001",
                "create_dt": "2021-10-11T17:51:09.908453+03:00",
                "change_dt": "2021-10-11T17:51:09.908476+03:00"
            },
            "id": 10,
            "children": [
                {
                    "data": {
                        "name": "Категория 001-001",
                        "create_dt": "2021-10-11T17:51:09.927855+03:00",
                        "change_dt": "2021-10-11T17:51:09.927872+03:00"
                    },
                    "id": 14,
                    "children": []
                }
            ]
        }
    ]

    """
    def __init__(self, items) -> None:
        super().__init__()
        self.items = items
        self.min_depth = list(items)[0].depth if items else None

    def run(self):
        lnk = {}
        result = []
        for item in self.items:
            newobj = self.get_new_object(item)
            if item.depth == self.min_depth:
                result.append(newobj)
            else:
                parentpath = item._get_basepath(item.path, item.depth - 1)
                parentobj = lnk[parentpath]
                parentobj['children'].append(newobj)
            lnk[item.path] = newobj
        self.sort_children(result)
        return result

    def get_new_object(self, item):
        return {
            'id': item.id,
            'data': self.get_data(item),
            'children': [],
        }

    def get_data(self, item):
        return {
            "id": item.id,
            "name": item.name,
            "type": "category",
            "create_dt": item.create_dt,
            "change_dt": item.change_dt,
            "sort_order": item.sort_order,
        }

    def sort_children(self, result):
        for item in result:
            if item['children']:
                item['children'].sort(key=lambda x: x['data']['sort_order'])
                self.sort_children(item['children'])
