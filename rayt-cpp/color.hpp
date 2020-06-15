#ifndef COLOR_HPP
#define COLOR_HPP

#include "utils.hpp"

#include <iostream>

void write_color(std::ostream &out, color pixel_color, int samples_per_pixel) {
  auto r = pixel_color.x();
  auto g = pixel_color.y();
  auto b = pixel_color.z();

  // Divide the color total by the number of samples.
  auto scale = 1.0 / samples_per_pixel;
  r *= scale;
  g *= scale;
  b *= scale;

  // Write the translated [0, 255] value of each color component.
  out << static_cast<int>(255.999 * clamp(r, 0.0, 0.999)) << ' '
      << static_cast<int>(255.999 * clamp(g, 0.0, 0.999)) << ' '
      << static_cast<int>(255.999 * clamp(b, 0.0, 0.999)) << '\n';
}

#endif
