// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#if HAVE_CONFIG_H
#include "config.h"
#endif

#include <iostream>

#include <dune/marchingcubes/marchingcubesrefinement.hh>

using namespace Dune;

// Very primitive testing of the Dune wrapper for the marching cubes algorithm
int main(int argc, char* argv[])
{
  GeometryType quadrilateral;
  quadrilateral.makeQuadrilateral();

  std::vector<double> values(4);
  values[0] = values[1] = -1;
  values[2] = values[3] =  1;

  MarchingCubesRefinement<double,2> refinement(quadrilateral, values);

  std::cout << "Elements:" << std::endl;
  MarchingCubesRefinement<double,2>::const_iterator it = refinement.begin();

  for (; it!=refinement.end(); ++it) {

    std::cout << "element has " << it->corners() << " corners" << std::endl;
    for (int i=0; i<it->corners(); i++)
      std::cout << it->corner(i) << std::endl;

  }

}
