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

class TestMarchingCubes33
{
public:
  bool testAny0d(sizeType expect, bool verbose,
                 double vertex_0);
  bool testAny1d(sizeType expect, bool verbose,
                 double vertex_0, double vertex_1);
  bool testSimplex2d(sizeType expect, bool verbose,
                     double vertex_0, double vertex_1, double vertex_2);
  bool testCube2d(sizeType expect, bool verbose,
                  double vertex_0, double vertex_1, double vertex_2, double vertex_3);
  bool testSimplex3d(sizeType expect, bool verbose,
                     double vertex_0, double vertex_1, double vertex_2, double vertex_3);
  bool testCube3d(sizeType expect, bool verbose,
                  double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                  double vertex_4, double vertex_5, double vertex_6, double vertex_7);
  template <int dim> bool assertEquals(sizeType expect,
                                       sizeType vertex_count, double * vertices, bool verbose);
};

bool TestMarchingCubes33::testAny0d(sizeType expect, bool verbose,
                                    double vertex_0)
{
  double vertices[] = {vertex_0};
  return this->assertEquals<0>(expect, 1, vertices, verbose);
}

bool TestMarchingCubes33::testAny1d(sizeType expect, bool verbose,
                                    double vertex_0, double vertex_1)
{
  double vertices[] = {vertex_0, vertex_1};
  return this->assertEquals<1>(expect, 2, vertices, verbose);
}

bool TestMarchingCubes33::testSimplex2d(sizeType expect, bool verbose,
                                        double vertex_0, double vertex_1, double vertex_2)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2};
  return this->assertEquals<2>(expect, 3, vertices, verbose);
}

bool TestMarchingCubes33::testCube2d(sizeType expect, bool verbose,
                                     double vertex_0, double vertex_1, double vertex_2, double vertex_3)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2, vertex_3};
  return this->assertEquals<2>(expect, 4, vertices, verbose);
}

bool TestMarchingCubes33::testSimplex3d(sizeType expect, bool verbose,
                                        double vertex_0, double vertex_1, double vertex_2, double vertex_3)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2, vertex_3};
  return this->assertEquals<3>(expect, 4, vertices, verbose);
}

bool TestMarchingCubes33::testCube3d(sizeType expect, bool verbose,
                                     double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                                     double vertex_4, double vertex_5, double vertex_6, double vertex_7)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2, vertex_3, vertex_4,
                       vertex_5, vertex_6, vertex_7};
  return this->assertEquals<3>(expect, 8, vertices, verbose);
}

template <int dim> bool TestMarchingCubes33::assertEquals(sizeType expect,
                                                          sizeType vertex_count, double * vertices, bool verbose)
{
  if (verbose)
  {
    std::cout << " Test data (dim: " << dim << ", vertices: " <<
    vertex_count << "): ";
    for (sizeType i = 0; i < vertex_count; i++)
    {
      std::cout << vertices[i] << " ";
    }
    std::cout << std::endl;
  }
  // Perform first part of MC 33 algorithm
  Dune::MarchingCubes33<double, dim, Dune::MarchingCubes::ThresholdFunctor> mc;
  size_t key = mc.getKey(vertices, vertex_count, true);
  // Print failed test cases
  if (key != expect)
  {
    std::cout << "  FAILED: Expected key " << expect <<
    " but " << key << " found. (Dimension: " << dim <<
    " Number of vertices: " << vertex_count << ")." << std::endl;
  }
  // Print result
  else if (verbose)
  {
    std::cout << "   Key: " << key << std::endl;
    // Perform second part of MC 33 algorithm
    typedef Dune::FieldVector<double, dim> dim_point;
    std::vector<std::vector<dim_point> > codim0;
    mc.getElements(vertices, vertex_count, key, false, codim0);
    std::cout << "   Codim 0 elements: ";
    for(typename std::vector<std::vector<dim_point> >::iterator i =
          codim0.begin(); i != codim0.end(); ++i)
    {
      std::cout << "[";
      for(typename std::vector<dim_point>::iterator j = i->begin();
          j != i->end(); ++j)
      {
        std::cout << "(" << *j << ") ";
      }
      std::cout << "]";
    }
    std::cout << std::endl;
    // Perform second part of MC 33 algorithm for codim 1 elements
    std::vector<std::vector<dim_point> > codim1;
    mc.getElements(vertices, vertex_count, key, true, codim1);
    std::cout << "   Codim 1 elements: ";
    for(typename std::vector<std::vector<dim_point> >::iterator i =
          codim1.begin(); i != codim1.end(); ++i)
    {
      std::cout << "[";
      for(typename std::vector<dim_point>::iterator j = i->begin();
          j != i->end(); ++j)
      {
        std::cout << "(" << *j << ") ";
      }
      std::cout << "]";
    }
    std::cout << std::endl;
  }
  return (key == expect);
}

int main(int arg_count, char ** arg_array)
{
  TestMarchingCubes33 testmc33;
  bool passed = true;
  bool verbose = false;

  /*sizeType vertexCount = argCount - 1;
     double* vertices = new double[vertexCount];

     for (sizeType i = 0; i < vertexCount; i++)
     {
      vertices[i] = atof(argArray[i + 1]);
      std::cout << vertices[i] << std::endl;
     }*/

  // Test any 0d (point)
  passed &= testmc33.testAny0d(0, verbose, 0.4);
  passed &= testmc33.testAny0d(0, verbose, 0.8);
  // Test any 1d (line)
  passed &= testmc33.testAny1d(0, verbose, 0.4, 0.2);
  passed &= testmc33.testAny1d(1, verbose, 0.7, 0.1);
  passed &= testmc33.testAny1d(2, verbose, 0.3, 0.7);
  passed &= testmc33.testAny1d(3, verbose, 0.8, 0.7);
  // Test simplex 2d
  passed &= testmc33.testSimplex2d(0, verbose, 0.2, 0.3, 0.4);
  passed &= testmc33.testSimplex2d(1, verbose, 0.8, 0.2, 0.4);
  passed &= testmc33.testSimplex2d(2, verbose, 0.1, 0.7, 0.5);
  passed &= testmc33.testSimplex2d(3, verbose, 0.8, 0.8, 0.4);
  passed &= testmc33.testSimplex2d(4, verbose, 0.0, 0.2, 0.8);
  passed &= testmc33.testSimplex2d(5, verbose, 0.8, 0.2, 0.9);
  passed &= testmc33.testSimplex2d(6, verbose, 0.3, 0.7, 0.8);
  passed &= testmc33.testSimplex2d(7, verbose, 0.9, 0.7, 0.8);
  // Test simplex 3d
  passed &= testmc33.testSimplex3d(0, verbose, 0.2, 0.3, 0.4, 0.5);
  passed &= testmc33.testSimplex3d(1, verbose, 0.8, 0.3, 0.4, 0.5);
  passed &= testmc33.testSimplex3d(2, verbose, 0.2, 1.0, 0.4, 0.5);
  passed &= testmc33.testSimplex3d(3, verbose, 0.9, 0.7, 0.4, 0.5);
  passed &= testmc33.testSimplex3d(4, verbose, 0.2, 0.3, 0.8, 0.4);
  passed &= testmc33.testSimplex3d(5, verbose, 0.7, 0.3, 0.8, 0.4);
  passed &= testmc33.testSimplex3d(6, verbose, 0.2, 0.9, 0.8, 0.4);
  passed &= testmc33.testSimplex3d(7, verbose, 0.8, 0.7, 0.9, 0.2);
  passed &= testmc33.testSimplex3d(8, verbose, 0.2, 0.3, 0.4, 0.8);
  passed &= testmc33.testSimplex3d(9, verbose, 0.8, 0.3, 0.4, 0.8);
  passed &= testmc33.testSimplex3d(10, verbose, 0.2, 1.0, 0.4, 0.8);
  passed &= testmc33.testSimplex3d(11, verbose, 0.9, 0.7, 0.4, 0.8);
  passed &= testmc33.testSimplex3d(12, verbose, 0.2, 0.3, 0.8, 0.8);
  passed &= testmc33.testSimplex3d(13, verbose, 0.7, 0.3, 0.8, 0.8);
  passed &= testmc33.testSimplex3d(14, verbose, 0.2, 0.9, 0.8, 0.8);
  passed &= testmc33.testSimplex3d(15, verbose, 0.8, 0.7, 0.9, 0.8);
  // Test cube 2d
  passed &= testmc33.testCube2d(0, verbose, 0.1, 0.4, 0.5, 0.3);
  passed &= testmc33.testCube2d(1, verbose, 0.7, 0.4, 0.5, 0.3);
  passed &= testmc33.testCube2d(2, verbose, 0.2, 0.8, 0.5, 0.3);
  passed &= testmc33.testCube2d(3, verbose, 0.7, 0.8, 0.5, 0.3);
  passed &= testmc33.testCube2d(4, verbose, 0.1, 0.4, 0.9, 0.3);
  passed &= testmc33.testCube2d(5, verbose, 0.7, 0.4, 0.9, 0.3);
  passed &= testmc33.testCube2d(6, verbose, 0.5, 0.8, 0.7, 0.4);
  passed &= testmc33.testCube2d(7, verbose, 0.9, 0.8, 0.7, 0.3);
  passed &= testmc33.testCube2d(8, verbose, 0.1, 0.4, 0.5, 0.8);
  passed &= testmc33.testCube2d(9, verbose, 0.7, 0.5, 0.4, 0.8);
  passed &= testmc33.testCube2d(10, verbose, 0.1, 0.8, 0.4, 0.8);
  passed &= testmc33.testCube2d(11, verbose, 0.7, 0.8, 0.5, 0.8);
  passed &= testmc33.testCube2d(12, verbose, 0.1, 0.4, 0.9, 0.8);
  passed &= testmc33.testCube2d(13, verbose, 0.7, 0.4, 0.9, 0.8);
  passed &= testmc33.testCube2d(14, verbose, 0.5, 0.8, 0.7, 0.8);
  passed &= testmc33.testCube2d(15, verbose, 0.9, 0.8, 0.7, 0.8);
  passed &= testmc33.testCube2d(16, verbose, 0.1, 0.8, 0.9, 0.2);
  passed &= testmc33.testCube2d(17, verbose, 0.9, 0.1, 0.2, 0.8);
  // Test cube 3d
  // Test all transformations of a basic case
  passed &= testmc33.testCube3d(255-1, verbose, 0.4, 0.8, 0.8, 0.8,
                                0.8, 0.8, 0.8, 0.8);
  passed &= testmc33.testCube3d(255-2, verbose, 0.8, 0.4, 0.8, 0.8,
                                0.8, 0.8, 0.8, 0.8);
  passed &= testmc33.testCube3d(255-4, verbose, 0.8, 0.8, 0.4, 0.8,
                                0.8, 0.8, 0.8, 0.8);
  passed &= testmc33.testCube3d(255-8, verbose, 0.8, 0.8, 0.8, 0.4,
                                0.8, 0.8, 0.8, 0.8);
  passed &= testmc33.testCube3d(255-16, verbose, 0.8, 0.8, 0.8, 0.8,
                                0.4, 0.8, 0.8, 0.8);
  passed &= testmc33.testCube3d(255-32, verbose, 0.8, 0.8, 0.8, 0.8,
                                0.8, 0.4, 0.8, 0.8);
  passed &= testmc33.testCube3d(255-64, verbose, 0.8, 0.8, 0.8, 0.8,
                                0.8, 0.8, 0.4, 0.8);
  passed &= testmc33.testCube3d(255-128, verbose, 0.8, 0.8, 0.8, 0.8,
                                0.8, 0.8, 0.8, 0.4);
  // Test every non MC 33 basic case
  passed &= testmc33.testCube3d(0, verbose, 0.5, 0.5, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.5); // Basic case 0
  passed &= testmc33.testCube3d(1, verbose, 0.9, 0.5, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.5); // Basic case 1
  passed &= testmc33.testCube3d(3, verbose, 0.9, 0.9, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.5); // Basic case 2
  passed &= testmc33.testCube3d(33, verbose, 0.9, 0.5, 0.5, 0.5,
                                0.5, 0.9, 0.5, 0.5); // Basic case 3
  passed &= testmc33.testCube3d(129, verbose, 0.9, 0.5, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.9); // Basic case 4
  passed &= testmc33.testCube3d(14, verbose, 0.5, 0.9, 0.9, 0.9,
                                0.5, 0.5, 0.5, 0.5); // Basic case 5
  passed &= testmc33.testCube3d(131, verbose, 0.9, 0.9, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.9); // Basic case 6
  passed &= testmc33.testCube3d(162, verbose, 0.5, 0.9, 0.5, 0.5,
                                0.5, 0.9, 0.5, 0.9); // Basic case 7
  passed &= testmc33.testCube3d(240, verbose, 0.5, 0.5, 0.5, 0.5,
                                0.9, 0.9, 0.9, 0.9); // Basic case 8
  passed &= testmc33.testCube3d(77, verbose, 0.9, 0.5, 0.9, 0.9,
                                0.5, 0.5, 0.9, 0.5); // Basic case 9
  passed &= testmc33.testCube3d(153, verbose, 0.9, 0.5, 0.5, 0.9,
                                0.9, 0.5, 0.5, 0.9); // Basic case 10
  passed &= testmc33.testCube3d(141, verbose, 0.9, 0.5, 0.9, 0.9,
                                0.5, 0.5, 0.5, 0.9); // Basic case 11
  passed &= testmc33.testCube3d(30, verbose, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.5, 0.5, 0.5); // Basic case 12
  passed &= testmc33.testCube3d(105, verbose, 0.9, 0.5, 0.5, 0.9,
                                0.5, 0.9, 0.9, 0.5); // Basic case 13
  passed &= testmc33.testCube3d(78, verbose, 0.5, 0.9, 0.9, 0.9,
                                0.5, 0.5, 0.9, 0.5); // Basic case 14
  passed &= testmc33.testCube3d(255, verbose, 0.9, 0.9, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.9); // Inverted basic case 0
  passed &= testmc33.testCube3d(255-1, verbose, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.9); // Inverted basic case 1
  passed &= testmc33.testCube3d(255-3, verbose, 0.5, 0.5, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.9); // Inverted basic case 2
  passed &= testmc33.testCube3d(255-33, verbose, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.5, 0.9, 0.9); // Inverted basic case 3
  passed &= testmc33.testCube3d(255-129, verbose, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.5); // Inverted basic case 4
  passed &= testmc33.testCube3d(255-14, verbose, 0.9, 0.5, 0.5, 0.5,
                                0.9, 0.9, 0.9, 0.9); // Inverted basic case 5
  passed &= testmc33.testCube3d(255-131, verbose, 0.5, 0.5, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.5); // Inverted basic case 6
  passed &= testmc33.testCube3d(255-162, verbose, 0.9, 0.5, 0.9, 0.9,
                                0.9, 0.5, 0.9, 0.5); // Inverted basic case 7
  // Test Marching cubes' 33 cases
  /*passed &= testmc33.testCube3d(33, verbose, 0.9, 0.5, 0.5, 0.5,
      0.5, 0.9, 0.5, 0.5); // Basic case 3 / MC33 case 3.1
     passed &= testmc33.testCube3d(260, verbose, 0.7, 0.2, 0.2, 0.2,
      0.2, 0.7, 0.2, 0.2); // MC33 case 3.2
     verbose = true;
     passed &= testmc33.testCube3d(255-129, verbose, 0.9, 0.9, 0.9, 0.9,
      0.5, 0.9, 0.9, 0.5); // Inverse of Basic case 3 / Inv. MC33 case 3.1
     passed &= testmc33.testCube3d(260, verbose, 0.7, 0.7, 0.7, 0.7,
      0.2, 0.7, 0.7, 0.2); // Inverse of MC33 case 3.2
   */


  if (!passed)
  {
    std::cout << "* * * Some marching cubes 33 tests FAILED. * * *"
              << std::endl << "Rerun program with option -verbose for details"
              << std::endl;
    return 1;
  }
  std::cout << "All marching cubes 33 tests passed. Congratulations."
            << std::endl;
  return 0;
}
