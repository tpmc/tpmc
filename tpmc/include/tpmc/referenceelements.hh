#ifndef TPMC_REFERENCEELEMENTS_HH
#define TPMC_REFERENCEELEMENTS_HH

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

    template <>
    int FaceVerticesTables<GeometryType::cube, 1>::indices[] = {0,1};
    template <>
    int FaceVerticesTables<GeometryType::cube, 1>::offsets[] = {0};

    template <>
    int FaceVerticesTables<GeometryType::cube, 2>::indices[] = {0,2,1,3,0,1,2,3};
    template <>
    int FaceVerticesTables<GeometryType::cube, 2>::offsets[] = {0,2,4,6};

    template <>
    int FaceVerticesTables<GeometryType::cube, 3>::indices[] = {0,2,4,6,1,3,5,7,0,1,4,5,2,3,6,7,0,1,2,3,4,5,6,7};
    template <>
    int FaceVerticesTables<GeometryType::cube, 3>::offsets[] = {0,4,8,12,16,20};

    template <>
    int FaceVerticesTables<GeometryType::simplex, 1>::indices[] = {0,1};
    template <>
    int FaceVerticesTables<GeometryType::simplex, 1>::offsets[] = {0};

    template <>
    int FaceVerticesTables<GeometryType::simplex, 2>::indices[] = {0,1,0,2,1,2};
    template <>
    int FaceVerticesTables<GeometryType::simplex, 2>::offsets[] = {0,2,4};

    template <>
    int FaceVerticesTables<GeometryType::simplex, 3>::indices[] = {0,1,2,0,1,3,0,2,3,1,2,3};
    template <>
    int FaceVerticesTables<GeometryType::simplex, 3>::offsets[] = {0,3,6,9};

    template <>
    int FaceVerticesTables<GeometryType::prism, 3>::indices[] = {0,1,3,4,0,2,3,5,1,2,4,5,0,1,2,3,4,5};
    template <>
    int FaceVerticesTables<GeometryType::prism, 3>::offsets[] = {0,4,8,12,15};

    template <>
    int FaceVerticesTables<GeometryType::pyramid, 3>::indices[] = {0,1,2,3,0,2,4,1,3,4,0,1,4,2,3,4};
    template <>
    int FaceVerticesTables<GeometryType::pyramid, 3>::offsets[] = {0,4,7,10,13};

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

  template <>
  int getVertexOfFace<1>(GeometryType type, int faceIndex, int localVertexIndex)
  {
    switch (type)
    {
    case cube:
      return faces::FaceVertices<GeometryType::cube, 1>::get(faceIndex, localVertexIndex);
    case simplex:
      return faces::FaceVertices<GeometryType::simplex, 1>::get(faceIndex, localVertexIndex);
    }
    throw std::invalid_argument("geometry not valid for 1d");
  }

  template <>
  int getVertexOfFace<2>(GeometryType type, int faceIndex, int localVertexIndex)
  {
    switch (type)
    {
    case cube:
      return faces::FaceVertices<GeometryType::cube, 2>::get(faceIndex, localVertexIndex);
    case simplex:
      return faces::FaceVertices<GeometryType::simplex, 2>::get(faceIndex, localVertexIndex);
    }
    throw std::invalid_argument("geometry not valid for 2d");
  }

  template <>
  int getVertexOfFace<3>(GeometryType type, int faceIndex, int localVertexIndex)
  {
    switch (type)
    {
    case cube:
      return faces::FaceVertices<GeometryType::cube, 3>::get(faceIndex, localVertexIndex);
    case simplex:
      return faces::FaceVertices<GeometryType::simplex, 3>::get(faceIndex, localVertexIndex);
    case prism:
      return faces::FaceVertices<GeometryType::prism, 3>::get(faceIndex, localVertexIndex);
    case pyramid:
      return faces::FaceVertices<GeometryType::pyramid, 3>::get(faceIndex, localVertexIndex);
    }
  }
}

#endif // TPMC_REFERENCEELEMENTS_HH
