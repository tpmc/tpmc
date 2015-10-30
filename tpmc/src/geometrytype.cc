#include <stdexcept>

#include <tpmc/geometrytype.hh>

namespace tpmc
{
  int getCornerCount(int dim, GeometryType type)
  {
    switch (dim) {
      case 0:
        return 1;
      case 1:
        return 2;
      case 2:
        switch (type) {
          case simplex:
          case pyramid:
            return 3;
          case cube:
          case prism:
            return 4;
        }
        break;
      case 3:
        switch (type) {
          case simplex:
            return 4;
          case pyramid:
            return 5;
          case prism:
            return 6;
          case cube:
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
      return simplex;
    }
    else if (dim == 1)
    {
      if (corners != 2)
        throw std::invalid_argument("geometry type unknown");
      return simplex;
    }
    else if (dim == 2)
    {
      if (corners == 3)
        return simplex;
      else if (corners == 4)
        return cube;
      else
        throw std::invalid_argument("geometry type unknown");
    }
    else if (dim == 3)
    {
      if (corners == 4)
        return simplex;
      else if (corners == 5)
        return pyramid;
      else if (corners == 6)
        return prism;
      else if (corners == 8)
        return cube;
      else
        throw std::invalid_argument("geometry type unknown");
    }
    else
      throw std::invalid_argument("dimension not supported");
  }
}
