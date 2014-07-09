// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#if HAVE_CONFIG_H
#include "config.h"
#endif

#include <iostream>

#include <dune/geometry/quadraturerules.hh>

#include <dune/marchingcubes/marchingcubesrefinement.hh>

using namespace Dune;

/* We integrate over both inside and outside and check whether the two volumes
 * sum up to 1.0.
 */
template <int dim>
void integralTest(GeometryType type,
                  const std::vector<double> values)
{
  double volume = 0;

  ///////////////////////////
  // Sum over inside
  ///////////////////////////
  MarchingCubesRefinement<double,dim> interiorRefinement(type,values);

  typename MarchingCubesRefinement<double,dim>::const_volume_iterator it = interiorRefinement.interiorBegin();

  for (; it!=interiorRefinement.interiorEnd(); ++it)
  {
    // Get zero-order quadrature rule
    const QuadratureRule<double,dim>& quad = QuadratureRules<double,dim>::rule(it->type(),0);

    for (size_t i=0; i<quad.size(); i++)
      volume += quad[i].weight() * it->integrationElement(quad[i].position());

  }

  ///////////////////////////
  // Sum over outside
  ///////////////////////////
  MarchingCubesRefinement<double,dim> exteriorRefinement(type,values,true);

  for (it = exteriorRefinement.interiorBegin(); it!=exteriorRefinement.interiorEnd(); ++it)
  {
    // Get zero-order quadrature rule
    const QuadratureRule<double,dim>& quad = QuadratureRules<double,dim>::rule(it->type(),0);

    for (size_t i=0; i<quad.size(); i++)
      volume += quad[i].weight() * it->integrationElement(quad[i].position());

  }

  if ( std::fabs(volume -
#if DUNE_VERSION_NEWER(DUNE_COMMON,2,3)
      ReferenceElements<double,dim>::general(type).volume()) > 1e-5
#else
      GenericReferenceElements<double,dim>::general(type).volume()) > 1e-5
#endif
    )
  {
    std::cout << "Integration over the entire refinement does not yield the correct element volume!" << std::endl;
  }
}

template <int dim>
void cornerTest(GeometryType type,
                const std::vector<double> values)
{
  MarchingCubesRefinement<double,dim> refinement(type,values);

  ////////////////////////////////////////////////////////////////////////////////
  //  Test the interior volume
  ////////////////////////////////////////////////////////////////////////////////

  std::cout << "Elements:" << std::endl;
  typename MarchingCubesRefinement<double,dim>::const_volume_iterator it = refinement.interiorBegin();

  for (; it!=refinement.interiorEnd(); ++it) {

    std::cout << "element has " << it->corners() << " corners" << std::endl;
    for (int i=0; i<it->corners(); i++)
      std::cout << it->corner(i) << std::endl;

  }

  ////////////////////////////////////////////////////////////////////////////////
  //  Test the interface
  ////////////////////////////////////////////////////////////////////////////////

  std::cout << "Interface:" << std::endl;
  typename MarchingCubesRefinement<double,dim>::const_interface_iterator iIt = refinement.interfaceBegin();

  for (; iIt!=refinement.interfaceEnd(); ++iIt) {

    std::cout << "interface element has " << iIt->corners() << " corners" << std::endl;
    for (int i=0; i<iIt->corners(); i++) {
      std::cout << iIt->corner(i) << std::endl;
    }

  }

}

// Very primitive testing of the Dune wrapper for the marching cubes algorithm
int main(int argc, char* argv[]) try
{
  //////////////////////////////////////////////////////
  //   Test subdividing a triangle
  //////////////////////////////////////////////////////
  GeometryType triangle;
  triangle.makeTriangle();

  std::vector<double> values = {-1, 1, 1};

  integralTest<2>(triangle, values);
  cornerTest<2>(triangle, values);

  //////////////////////////////////////////////////////
  //   Test subdividing a quadrilateral
  //////////////////////////////////////////////////////
  GeometryType quadrilateral;
  quadrilateral.makeQuadrilateral();

  values = {-1, -1, 1, 1};

  integralTest<2>(quadrilateral, values);
  cornerTest<2>(quadrilateral, values);

  //////////////////////////////////////////////////////
  //   Test subdividing a tetrahedron
  //////////////////////////////////////////////////////
  GeometryType tetrahedron;
  tetrahedron.makeTetrahedron();

  values = {-1, -1, 1, 1};

  integralTest<3>(tetrahedron, values);
  cornerTest<3>(tetrahedron, values);

  //////////////////////////////////////////////////////
  //   Test subdividing a hexahedron
  //////////////////////////////////////////////////////
  GeometryType hexahedron;
  hexahedron.makeHexahedron();

  values = {-1, 1, 1, -1, 2, 2, -2, 2};

  integralTest<3>(hexahedron, values);
  cornerTest<3>(hexahedron, values);

}
catch (Exception e) {
  std::cout << e << std::endl;
}
