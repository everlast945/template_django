# from typing import List
#
# import pandas as pd
# import numpy as np
# import time
#
#
# class ColumnImport:
#     """
#     Колонки для импорта
#     """
#
#     def __init__(self, name, method=None, model_name=None) -> None:
#         self.name = name
#         self.method = method
#         self.model_name = model_name or name
#
#     def get_row_value(self, row):
#         value = row[self.name]
#         if self.method:
#             return self.method(value)
#         return value
#
#     @classmethod
#     def get_json_data(cls, value):
#         if value == 'null' or value is None:
#             return None
#         elif isinstance(value, str):
#             return value.replace('"', '')
#         return value
#
#     @classmethod
#     def get_value_replace(cls, value):
#         if value is None:
#             return value
#         return value.replace('"', '')
#
#
# class PandasImportBase:
#     """
#     Импорт через пандас
#     """
#
#     uniq_csv_name = None
#     uniq_field_name = None
#     save_count = 100
#     model = None
#     DTYPE = None
#     COLUMNS: List[ColumnImport] = []
#
#     def __init__(self, file) -> None:
#         self.parsing_time = None
#         self.save_time = None
#         self._parse_document(file)
#
#     def save(self):
#         start_time = time.time()
#         self.exists_uniq_codes = list(self.model.objects.values_list(self.uniq_field_name, flat=True))
#         self._save_objects()
#         self.save_time = time.time() - start_time
#
#     def get_result(self):
#         return {
#             'parsing_time': f'Парисинг файла: {self.parsing_time}',
#             'save_time': f'Обновление БД: {self.save_time}',
#         }
#
#     def _parse_document(self, file):
#         """
#         Парсин
#         """
#         start_time = time.time()
#         self.df = pd.read_csv(file, skiprows=0, dtype=self.DTYPE)
#         self.df = self.df.replace({np.nan: None})
#         self.parsing_time = time.time() - start_time
#
#     def _save_objects(self):
#         objects_to_save = []
#         iterator_rows = self.df.iterrows()
#         for index, row in iterator_rows:
#             if not self._is_valid_uniq_code(row):
#                 continue
#             objects_to_save.append(
#                 self.model(**{column.model_name: column.get_row_value(row) for column in self.COLUMNS})
#             )
#         if objects_to_save:
#             self.model.objects.bulk_create(objects_to_save, batch_size=self.save_count, ignore_conflicts=True)
#
#     def _is_valid_uniq_code(self, row):
#         """
#         Извлечение, проверка и фиксация уникального кода
#         """
#         uniq_code = str(row[self.uniq_csv_name])
#         if uniq_code == self.uniq_csv_name or uniq_code in self.exists_uniq_codes:
#             return False
#         self.exists_uniq_codes.append(uniq_code)
#         return True
