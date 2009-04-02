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

void useMarchingCubes33(sizeType vertex_count, double * vertices, sizeType expected);

int main(int arg_count, char ** arg_array)
{
  std::cout << "Test MC 33 started." << std::endl;

  /*sizeType vertexCount = argCount - 1;
     double* vertices = new double[vertexCount];

     for (sizeType i = 0; i < vertexCount; i++)
     {
     vertices[i] = atof(argArray[i + 1]);
          std::cout << vertices[i] << std::endl;
     }*/
  sizeType vertex_count = 4;
  double* vertices = new double[vertex_count];
  vertices[0] = 0.1;       // basic case 16 = mc33 case 6.2
  vertices[1] = 0.8;
  vertices[2] = 0.9;
  vertices[3] = 0.2;
  useMarchingCubes33(vertex_count, vertices, 16);
  vertices[0] = 0.5;       //basic case 6
  vertices[1] = 0.8;
  vertices[2] = 0.7;
  vertices[3] = 0.4;
  useMarchingCubes33(vertex_count, vertices, 6);
  vertices[0] = 0.7;       // basic case 9
  vertices[1] = 0.5;
  vertices[2] = 0.4;
  vertices[3] = 0.8;
  useMarchingCubes33(vertex_count, vertices, 9);
  vertices[0] = 0.9;       // basic case 17 = mc33 case 9.2
  vertices[1] = 0.1;
  vertices[2] = 0.2;
  vertices[3] = 0.8;
  useMarchingCubes33(vertex_count, vertices, 17);

  vertices[0] = 0.8;       // 2D simplex basic case 7
  vertices[1] = 0.8;
  vertices[2] = 0.8;
  useMarchingCubes33(3, vertices, 7);
  vertices[0] = 0.8;       // 2D simplex basic case 6
  vertices[1] = 0.8;
  vertices[2] = 0.4;
  useMarchingCubes33(3, vertices, 6);
  vertices[0] = 0.8;       // 2D simplex basic case 5
  vertices[1] = 0.4;
  vertices[2] = 0.8;
  useMarchingCubes33(3, vertices, 5);
  vertices[0] = 0.4;       // 2D simplex basic case 3
  vertices[1] = 0.8;
  vertices[2] = 0.8;
  useMarchingCubes33(3, vertices, 3);

  std::cout << "Test MC 33 finished." << std::endl;
  return 0;
}

void useMarchingCubes33(sizeType vertex_count, double * vertices, sizeType expected)
{
  std::cout << " Test data: (size: " << vertex_count << ") ";
  for (sizeType i = 0; i < vertex_count; i++)
  {
    std::cout << vertices[i] << " ";
  }
  std::cout << std::endl;

  Dune::MarchingCubes33<double, 2, Dune::MarchingCubes::ThresholdFunctor> mc;
  std::vector<std::vector<Dune::FieldVector<double, 2> > > codim0;
  // Perform MC 33 algorithm
  size_t case_number = mc.getKey(vertices, vertex_count, true);
  mc.getElements(vertices, vertex_count, case_number, codim0, false);

  if (case_number != expected)
  {
    std::cout << "  ERROR: Case number not expected." << std::endl;
  }

  std::cout << "   Case number is: " << case_number
            << " Expected was: " << expected << std::endl;

  // Print result
  for(std::vector<std::vector<Dune::FieldVector<double, 2> > >::iterator i =
        codim0.begin(); i != codim0.end(); ++i)
  {
    std::cout << "    ";
    for(std::vector<Dune::FieldVector<double, 2> >::iterator j = i->begin(); j != i->end(); ++j)
    {
      std::cout << "(" << *j << ") ";
    }
    std::cout << std::endl;
  }
}
