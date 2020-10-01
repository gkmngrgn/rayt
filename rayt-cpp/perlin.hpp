#ifndef PERLIN_HPP
#define PERLIN_HPP

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

#include "utils.hpp"
#include "vec3.hpp"

class perlin {
public:
  perlin() {
    ranfloat = new double[point_count];
    for (int i = 0; i < point_count; ++i) {
      ranfloat[i] = random_double();
    }

    perm_x = perlin_generate_perm();
    perm_y = perlin_generate_perm();
    perm_z = perlin_generate_perm();
  }

  ~perlin() {
    delete[] ranfloat;
    delete[] perm_x;
    delete[] perm_y;
    delete[] perm_z;
  }

  double noise(const point3 &p) const {
    auto u = p.x() - floor(p.x());
    auto v = p.y() - floor(p.y());
    auto w = p.z() - floor(p.z());

    auto i = static_cast<int>(4 * p.x()) & 255;
    auto j = static_cast<int>(4 * p.y()) & 255;
    auto k = static_cast<int>(4 * p.z()) & 255;

    return ranfloat[perm_x[i] ^ perm_y[j] ^ perm_z[k]];
  }

private:
  static const int point_count = 256;
  double *ranfloat;
  int *perm_x;
  int *perm_y;
  int *perm_z;

  static int *perlin_generate_perm() {
    auto p = new int[point_count];

    for (int i = 0; i < perlin::point_count; i++) {
      p[i] = i;
    }

    permute(p, point_count);

    return p;
  }

  static void permute(int *p, int n) {
    for (int i = n - 1; i > 0; i--) {
      int target = random_int(0, i);
      int tmp = p[i];
      p[i] = p[target];
      p[target] = tmp;
    }
  }
};

#endif
