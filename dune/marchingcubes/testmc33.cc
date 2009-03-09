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
  /*vertices[0] = 0.1; // basic case 16 = mc33 case 6.2
     vertices[1] = 0.8;
     vertices[2] = 0.9;
     vertices[3] = 0.2;*/
  /*vertices[0] = 0.5; //basic case 6
     vertices[1] = 0.8;
     vertices[2] = 0.7;
     vertices[3] = 0.4;*/
  vertices[0] = 0.7;       // basic case 9
  vertices[1] = 0.5;
  vertices[2] = 0.4;
  vertices[3] = 0.8;
  /*vertices[0] = 0.9; // basic case 17 = mc33 case 9.2
     vertices[1] = 0.1;
     vertices[2] = 0.2;
     vertices[3] = 0.8;*/

  std::cout << "Test data: " << vertices[0] << " " << vertices[1] << " "
            << vertices[2] << " " << vertices[3] << " " << std::endl;

  Dune::MarchingCubesAlgorithm<double, 2, Dune::MarchingCubes::ThresholdFunctor> mc;
  std::vector<std::vector<Dune::FieldVector<double, 2> > > codim0;
  // Perform mc 33 algorithm
  size_t caseNumber = mc.getKey(vertices, vertexCount, true);
  mc.getElements(vertices, vertexCount, caseNumber, codim0, false);

  std::cout << "Case number is: " << caseNumber << std::endl;

  // Print result
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
