import typing

from rayt_python.hittable import HitRecord, Hittable
from rayt_python.ray import Ray


class HittableList:
    def __init__(self, h_tables: typing.List[Hittable] = []):
        self.h_tables = h_tables

    def add(self, h_table: Hittable) -> None:
        self.h_tables.append(h_table)

    def clear(self):
        self.h_tables.clear()

    def hit(self, ray: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max

        for h_table in self.h_tables:
            if h_table.hit(ray, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.update(temp_rec)

        return hit_anything
