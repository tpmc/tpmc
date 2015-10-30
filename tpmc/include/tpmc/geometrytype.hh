#ifndef TPMC_GEOMETRYTYPE_HH
#define TPMC_GEOMETRYTYPE_HH

namespace tpmc
{
  enum GeometryType
  {
    cube,
    simplex,
    prism,
    pyramid
  };

  int getCornerCount(int dim, GeometryType type);
  GeometryType makeGeometryType(int dim, int corners);
}

#endif // TPMC_GEOMETRYTYPE_HH
