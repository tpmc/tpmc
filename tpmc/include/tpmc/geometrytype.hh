#ifndef TPMC_GEOMETRYTYPE_HH
#define TPMC_GEOMETRYTYPE_HH

#include <exception>

namespace tpmc
{
  enum GeometryType
  {
    cube,
    simplex,
    prism,
    pyramid
  };

  int getCornerCount(int dim, GeometryType type)
  {
    switch (dim) {
      case 0:
        return 1;
      case 1:
        return 2;
      case 2:
        switch (type) {
          case GeometryType::simplex:
          case GeometryType::pyramid:
            return 3;
          case GeometryType::cube:
          case GeometryType::prism:
            return 4;
        }
        break;
      case 3:
        switch (type) {
          case GeometryType::simplex:
            return 4;
          case GeometryType::pyramid:
            return 5;
          case GeometryType::prism:
            return 6;
          case GeometryType::cube:
            return 8;
        }
        break;
    }
    throw std::invalid_argument("combination of dim and type not known");
  }

  GeometryType makeGeometryType(int dim, int corners)
  {
    if (dim == 0)
    {
      if (corners != 1)
        throw std::invalid_argument("geometry type unknown");
      return GeometryType::simplex;
    }
    else if (dim == 1)
    {
      if (corners != 2)
        throw std::invalid_argument("geometry type unknown");
      return GeometryType::simplex;
    }
    else if (dim == 2)
    {
      if (corners == 3)
        return GeometryType::simplex;
      else if (corners == 4)
        return GeometryType::cube;
      else
        throw std::invalid_argument("geometry type unknown");
    }
    else if (dim == 3)
    {
      if (corners == 4)
        return GeometryType::simplex;
      else if (corners == 5)
        return GeometryType::pyramid;
      else if (corners == 6)
        return GeometryType::prism;
      else if (corners == 8)
        return GeometryType::cube;
      else
        throw std::invalid_argument("geometry type unknown");
    }
    else
      throw std::invalid_argument("dimension not supported");
  }
}

#endif // TPMC_GEOMETRYTYPE_HH
