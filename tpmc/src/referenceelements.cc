#include <stdexcept>
#include <tpmc/referenceelements.hh>
#include <tpmc/geometrytype.hh>

namespace tpmc
{
  namespace faces
  {

    template <>
    int FaceVerticesTables<cube, 1>::indices[] = {0,1};
    template <>
    int FaceVerticesTables<cube, 1>::offsets[] = {0};

    template <>
    int FaceVerticesTables<cube, 2>::indices[] = {0,2,1,3,0,1,2,3};
    template <>
    int FaceVerticesTables<cube, 2>::offsets[] = {0,2,4,6};

    template <>
    int FaceVerticesTables<cube, 3>::indices[] = {0,2,4,6,1,3,5,7,0,1,4,5,2,3,6,7,0,1,2,3,4,5,6,7};
    template <>
    int FaceVerticesTables<cube, 3>::offsets[] = {0,4,8,12,16,20};

    template <>
    int FaceVerticesTables<simplex, 1>::indices[] = {0,1};
    template <>
    int FaceVerticesTables<simplex, 1>::offsets[] = {0};

    template <>
    int FaceVerticesTables<simplex, 2>::indices[] = {0,1,0,2,1,2};
    template <>
    int FaceVerticesTables<simplex, 2>::offsets[] = {0,2,4};

    template <>
    int FaceVerticesTables<simplex, 3>::indices[] = {0,1,2,0,1,3,0,2,3,1,2,3};
    template <>
    int FaceVerticesTables<simplex, 3>::offsets[] = {0,3,6,9};

    template <>
    int FaceVerticesTables<prism, 3>::indices[] = {0,1,3,4,0,2,3,5,1,2,4,5,0,1,2,3,4,5};
    template <>
    int FaceVerticesTables<prism, 3>::offsets[] = {0,4,8,12,15};

    template <>
    int FaceVerticesTables<pyramid, 3>::indices[] = {0,1,2,3,0,2,4,1,3,4,0,1,4,2,3,4};
    template <>
    int FaceVerticesTables<pyramid, 3>::offsets[] = {0,4,7,10,13};
  }
  template <>
  int getVertexOfFace<1>(GeometryType type, int faceIndex, int localVertexIndex)
  {
    switch (type)
    {
    case cube:
      return faces::FaceVertices<cube, 1>::get(faceIndex, localVertexIndex);
    case simplex:
      return faces::FaceVertices<simplex, 1>::get(faceIndex, localVertexIndex);
    default:
      throw std::invalid_argument("geometry not valid for 1d");
    }
  }

  template <>
  int getVertexOfFace<2>(GeometryType type, int faceIndex, int localVertexIndex)
  {
    switch (type)
    {
    case cube:
      return faces::FaceVertices<cube, 2>::get(faceIndex, localVertexIndex);
    case simplex:
      return faces::FaceVertices<simplex, 2>::get(faceIndex, localVertexIndex);
    default:
      throw std::invalid_argument("geometry not valid for 2d");
    }
  }

  template <>
  int getVertexOfFace<3>(GeometryType type, int faceIndex, int localVertexIndex)
  {
    switch (type)
    {
    case cube:
      return faces::FaceVertices<cube, 3>::get(faceIndex, localVertexIndex);
    case simplex:
      return faces::FaceVertices<simplex, 3>::get(faceIndex, localVertexIndex);
    case prism:
      return faces::FaceVertices<prism, 3>::get(faceIndex, localVertexIndex);
    case pyramid:
      return faces::FaceVertices<pyramid, 3>::get(faceIndex, localVertexIndex);
    }
    throw std::invalid_argument("unknown geometry type provided");
  }
}
