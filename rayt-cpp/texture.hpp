#ifndef TEXTURE_HPP
#define TEXTURE_HPP

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

#include "color.hpp"
#include "perlin.hpp"

class texture {
public:
  virtual color value(double u, double v, const point3 &p) const = 0;
};

class solid_color : public texture {
public:
  solid_color() {}

  solid_color(color c) : color_value(c) {}

  solid_color(double red, double green, double blue)
      : solid_color(color(red, green, blue)) {}

  virtual color value(double u, double v, const vec3 &p) const override {
    return color_value;
  }

private:
  color color_value;
};

class checker_texture : public texture {
public:
  checker_texture() {}

  checker_texture(shared_ptr<texture> t0, shared_ptr<texture> t1)
      : even(t0), odd(t1) {}

  checker_texture(color c1, color c2)
      : even(make_shared<solid_color>(c1)), odd(make_shared<solid_color>(c2)) {}

  virtual color value(double u, double v, const point3 &p) const override {
    auto sines = sin(10 * p.x()) * sin(10 * p.y()) * sin(10 * p.z());
    if (sines < 0) {
      return odd->value(u, v, p);
    } else {
      return even->value(u, v, p);
    }
  }

private:
  shared_ptr<texture> odd;
  shared_ptr<texture> even;
};

class noise_texture : public texture {
public:
  noise_texture() {}

  virtual color value(double u, double v, const point3 &p) const override {
    return color(1.0, 1.0, 1.0) * noise.noise(p);
  }

public:
  perlin noise;
};

#endif
