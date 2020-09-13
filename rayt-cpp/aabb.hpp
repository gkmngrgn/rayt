#ifndef AABB_HPP
#define AABB_HPP

//==============================================================================
// Originally written in 2016 by Peter Shirley <ptrshrl@gmail.com>
//
// To the extent possible under law, the author(s) have dedicated all copyright
// and related and neighboring rights to this software to the public domain
// worldwide. This software is distributed without any warranty.
//
// You should have received a copy (see file COPYING.txt) of the CC0 Public
// Domain Dedication along with this software. If not, see
// <http://creativecommons.org/publicdomain/zero/1.0/>.
//==============================================================================

#include "ray.hpp"
#include "vec3.hpp"

class aabb {
public:
  aabb() {}
  aabb(const point3 &a, const point3 &b) {
    _min = a;
    _max = b;
  }

  point3 min() const { return _min; }
  point3 max() const { return _max; }

  bool hit(const ray &r, double t_min, double t_max) const {
    for (int a = 0; a < 3; a++) {
      auto t0 = fmin((_min[a] - r.origin()[a]) / r.direction()[a],
                     (_max[a] - r.origin()[a]) / r.direction()[a]);
      auto t1 = fmax((_min[a] - r.origin()[a]) / r.direction()[a],
                     (_max[a] - r.origin()[a]) / r.direction()[a]);
      t_min = fmax(t0, t_min);
      t_max = fmin(t1, t_max);
      if (t_max <= t_min) {
        return false;
      }
    }
    return true;
  }

  point3 _min;
  point3 _max;
};

inline bool aabb::hit(const ray &r, double t_min, double t_max) const {
  for (int a = 0; a < 3; a++) {
    auto invD = 1.0f / r.direction()[a];
    auto t0 = (min()[a] - r.origin()[a]) * invD;
    auto t1 = (max()[a] - r.origin()[a]) * invD;
    if (invD < 0.0f) {
      std::swap(t0, t1);
    }
    t_min = t0 > t_min ? t0 : t_min;
    t_max = t1 < t_max ? t1 : t_max;
    if (t_max <= t_min) {
      return false;
    }
  }
  return true;
}

aabb surrounding_box(aabb box0, aabb box1) {
  point3 small(fmin(box0.min().x(), box1.min().x()),
               fmin(box0.min().y(), box1.min().y()),
               fmin(box0.min().z(), box1.min().z()));
  point3 big(fmin(box0.max().x(), box1.max().x()),
             fmin(box0.max().y(), box1.max().y()),
             fmin(box0.max().z(), box1.max().z()));
  return aabb(small, big);
}

#endif
