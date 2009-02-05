// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#include <config.h>

#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>

#include <dune/common/fvector.hh>

#include "thresholdfunctor.hh"
#include "marchingcubes.hh"


typedef size_t sizeType;

int main(int argCount, char ** argArray)
{
  std::cout << "Test MC 33 started." << std::endl;

  /*sizeType vertexCount = argCount - 1;
     double* vertices = new double[vertexCount];

     for (sizeType i = 0; i < vertexCount; i++)
     {
     vertices[i] = atof(argArray[i + 1]);
          std::cout << vertices[i] << std::endl;
     }*/
  sizeType vertexCount = 4;
  double* vertices = new double[vertexCount];
  vertices[0] = 0.5;
  vertices[1] = 1.8;
  vertices[2] = 1.9;
  vertices[3] = 0.55;

  Dune::MarchingCubesAlgorithm<double, 2, Dune::MarchingCubes::ThresholdFunctor, std::string> mc;

  std::vector<std::vector<Dune::FieldVector<double, 2> > > codim0;

  char * offsets = new char[5];
  mc.getOffsets(vertices, vertexCount, true, offsets);
  mc.getElements(vertices, vertexCount, offsets, codim0);

  // Ausgabe der Ergebnisse
  for(std::vector<std::vector<Dune::FieldVector<double, 2> > >::iterator i = codim0.begin(); i != codim0.end(); ++i)
  {
    for(std::vector<Dune::FieldVector<double, 2> >::iterator j = i->begin(); j != i->end(); ++j)
    {
      std::cout << "(" << *j << ") ";
    }
    std::cout << std::endl;
  }

  std::cout << "Test MC 33 finished." << std::endl;

  return 0;
}
