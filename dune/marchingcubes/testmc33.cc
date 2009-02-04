// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#include <config.h>

#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>

#include "thresholdfunctor.hh"
#include "marchingcubes.hh"

int main(int argCount, char ** argArray)
{
  std::cout << "Test MC 33 started." << std::endl;

  int vertexCount = argCount - 1;
  double * vertices = new double[vertexCount];

  for (int i = 0; i < vertexCount; i++)
  {
    vertices[i] = atof(argArray[i + 1]);
  }
  Dune::MarchingCubesAlgorithm<double, 2, Dune::MarchingCubes::ThresholdFunctor, std::string> mc;

  std::vector<std::vector<double> > * codim0 = new std::vector<std::vector<double> >();

  char * offsets = new char[5];

  bool isMc33case = mc.getOffsets(vertices, vertexCount, true);
  mc.getElements(vertices, vertexCount, offsets, isMc33case, codim0);

  // Ausgabe der Ergebnisse
  for(std::vector<std::vector<double> >::iterator i = codim0->begin(); i != codim0->end(); ++i)
  {
    for(std::vector<double>::iterator j = i->begin(); j != i->end(); ++j)
    {
      std::cout << *j << "  ";
    }
    std::cout << std::endl;
  }

  std::cout << "Test MC 33 finished." << std::endl;

  return 0;
}
