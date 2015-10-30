#ifndef TPMC_REFERENCEELEMENTS_HH
#define TPMC_REFERENCEELEMENTS_HH

#include <exception>
#include "geometrytype.hh"

namespace tpmc
{
  namespace faces
  {
    template <GeometryType type, int dim>
    struct FaceVerticesTables
    {
      static int indices[];
      static int offsets[];
    };

    template <GeometryType type, int dim>
    struct FaceVertices
    {
      typedef FaceVerticesTables<type,dim> Tables;
      static int get(int faceIndex, int localVertexIndex)
      {
        return Tables::indices[Tables::offsets[faceIndex]+localVertexIndex];
      }
    };

  }
  // returns the index of a vertex in the reference element
  template <int dim>
  int getVertexOfFace(GeometryType type, int faceIndex, int localVertexIndex);
}

#endif // TPMC_REFERENCEELEMENTS_HH
