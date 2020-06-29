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

    def hit(self, r: Ray, t_min: float, t_max: float) -> typing.Union[HitRecord, None]:
        closest_so_far = t_max
        rec = None

        for h_table in self.h_tables:
            temp_rec = h_table.hit(r, t_min, closest_so_far)
            if temp_rec is not None:
                closest_so_far = temp_rec.t
                rec = temp_rec

        return rec
