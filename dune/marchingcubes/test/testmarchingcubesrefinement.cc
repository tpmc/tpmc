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
    const Dune::QuadratureRule<double,dim>& quad = Dune::QuadratureRules<double,dim>::rule(it->type(),0);

    for (size_t i=0; i<quad.size(); i++)
      volume += quad[i].weight() * it->integrationElement(quad[i].position());

  }

  ///////////////////////////
  // Sum over outside
  ///////////////////////////
  MarchingCubesRefinement<double,2> exteriorRefinement(type,values,true);

  for (it = exteriorRefinement.interiorBegin(); it!=exteriorRefinement.interiorEnd(); ++it)
  {
    // Get zero-order quadrature rule
    const QuadratureRule<double,dim>& quad = Dune::QuadratureRules<double,dim>::rule(it->type(),0);

    for (size_t i=0; i<quad.size(); i++)
      volume += quad[i].weight() * it->integrationElement(quad[i].position());

  }

  if ( std::fabs(volume - ReferenceElements<double,dim>::general(type).volume()) > 1e-5 )
  {
    std::cout << "Integration over the entire refinement does not yield the correct element volume!" << std::endl;
  }
}

// Very primitive testing of the Dune wrapper for the marching cubes algorithm
int main(int argc, char* argv[]) try
{
  GeometryType quadrilateral;
  quadrilateral.makeQuadrilateral();

  std::vector<double> values(4);
  values[0] = values[1] = -1;
  values[2] = values[3] =  1;

  integralTest<2>(quadrilateral, values);

  MarchingCubesRefinement<double,2> refinement(quadrilateral,values);

  ////////////////////////////////////////////////////////////////////////////////
  //  Test the interior volume
  ////////////////////////////////////////////////////////////////////////////////

  std::cout << "Elements:" << std::endl;
  MarchingCubesRefinement<double,2>::const_volume_iterator it = refinement.interiorBegin();

  for (; it!=refinement.interiorEnd(); ++it) {

    std::cout << "element has " << it->corners() << " corners" << std::endl;
    for (int i=0; i<it->corners(); i++)
      std::cout << it->corner(i) << std::endl;

  }

  ////////////////////////////////////////////////////////////////////////////////
  //  Test the interface
  ////////////////////////////////////////////////////////////////////////////////

  std::cout << "Interface:" << std::endl;
  MarchingCubesRefinement<double,2>::const_interface_iterator iIt = refinement.interfaceBegin();

  for (; iIt!=refinement.interfaceEnd(); ++iIt) {

    std::cout << "interface element has " << iIt->corners() << " corners" << std::endl;
    for (int i=0; i<iIt->corners(); i++) {
      std::cout << iIt->corner(i) << std::endl;
    }

  }

}
catch (Exception e) {
  std::cout << e << std::endl;
}
