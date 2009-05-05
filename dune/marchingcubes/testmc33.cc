// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#include <config.h>

#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <fstream>

#include <dune/common/fvector.hh>

#include "thresholdfunctor.hh"
#include "marchingcubes.hh"


typedef size_t sizeType;

class TestMarchingCubes33
{
public:
  static const int NO_KEY;
  bool verbose;
  bool write_vtk;
  bool testAny0d(int expect, double vertex_0, std::string name);
  bool testAny1d(int expect, double vertex_0, double vertex_1,
                 std::string name);
  bool testSimplex2d(int expect,
                     double vertex_0, double vertex_1, double vertex_2, std::string name);
  bool testCube2d(int expect,
                  double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                  std::string name);
  bool testSimplex3d(int expect,
                     double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                     std::string name);
  bool testCube3d(int expect,
                  double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                  double vertex_4, double vertex_5, double vertex_6, double vertex_7,
                  std::string name);
  template <int dim> bool assertEquals(int expect,
                                       sizeType vertex_count, double * vertices, std::string name);
  template <int dim> void writeVtkFile(
    const std::vector<std::vector<Dune::FieldVector <double, dim> > > & elements, int element_dim,
    std::string name);
};
const int TestMarchingCubes33::NO_KEY = -1;

bool TestMarchingCubes33::testAny0d(int expect,
                                    double vertex_0, std::string name)
{
  double vertices[] = {vertex_0};
  return this->assertEquals<0>(expect, 1, vertices, name);
}

bool TestMarchingCubes33::testAny1d(int expect,
                                    double vertex_0, double vertex_1, std::string name)
{
  double vertices[] = {vertex_0, vertex_1};
  return this->assertEquals<1>(expect, 2, vertices, name);
}

bool TestMarchingCubes33::testSimplex2d(int expect,
                                        double vertex_0, double vertex_1, double vertex_2, std::string name)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2};
  return this->assertEquals<2>(expect, 3, vertices, name);
}

bool TestMarchingCubes33::testCube2d(int expect,
                                     double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                                     std::string name)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2, vertex_3};
  return this->assertEquals<2>(expect, 4, vertices, name);
}

bool TestMarchingCubes33::testSimplex3d(int expect,
                                        double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                                        std::string name)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2, vertex_3};
  return this->assertEquals<3>(expect, 4, vertices, name);
}

bool TestMarchingCubes33::testCube3d(int expect,
                                     double vertex_0, double vertex_1, double vertex_2, double vertex_3,
                                     double vertex_4, double vertex_5, double vertex_6, double vertex_7,
                                     std::string name)
{
  double vertices[] = {vertex_0, vertex_1, vertex_2, vertex_3, vertex_4,
                       vertex_5, vertex_6, vertex_7};
  return this->assertEquals<3>(expect, 8, vertices, name);
}

template <int dim> bool TestMarchingCubes33::assertEquals(int expect,
                                                          sizeType vertex_count, double * vertices, std::string name)
{
  if (verbose)
  {
    std::cout << "======================================\n";
    std::cout << " Test data for \"" << name << "\" (dim: " << dim <<
    ", vertices: " << vertex_count << "): ";
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
  if ((int)key != expect && expect != NO_KEY)
  {
    std::cout << "  FAILED: \""  << name << "\" Expected key " <<
    expect << " but " << key << " found. (Dimension: " << dim <<
    " Number of vertices: " << vertex_count << ")." << std::endl;
  }
  // Print result
  else
  {
    if (verbose)
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
    // write vtk file
    if(write_vtk)
    {
      // Perform second part of MC 33 algorithm
      typedef Dune::FieldVector<double, dim> dim_point;
      std::vector<std::vector<dim_point> > codim0;
      mc.getElements(vertices, vertex_count, key, false, codim0);
      writeVtkFile<dim>(codim0, dim, name);
      // Perform second part of MC 33 algorithm for codim 1 elements
      std::vector<std::vector<dim_point> > codim1;
      mc.getElements(vertices, vertex_count, key, true, codim1);
      writeVtkFile<dim>(codim1, dim - 1, name);
    }
  }
  return (((int)key == expect) || ((int)expect == NO_KEY));
}

/*
 * Write Vtk file containing the given elements.
 */
template <int dim> void TestMarchingCubes33::writeVtkFile(
  const std::vector<std::vector<Dune::FieldVector <double, dim> > > & elements,
  int element_dim, std::string name)
{
  typedef Dune::FieldVector<double, dim> dim_point;
  std::string file_name = "vtk/" + name + "_" +
                          (dim == element_dim ? "cells" : "faces") + ".vtk";
  std::ofstream vtk_file(file_name.c_str(), std::ios::out);
  // Write vtk header
  vtk_file << "# vtk DataFile Version 3.0" << std::endl <<
  "test case " << name <<
  (dim == element_dim ? " cells" : " faces") << std::endl <<
  "ASCII" << std::endl <<
  "DATASET UNSTRUCTURED_GRID" << std::endl;
  // Write occuring points
  int number_points = 0;
  for(typename std::vector<std::vector<dim_point> >::const_iterator
      i = elements.begin(); i != elements.end(); ++i)
  {
    number_points += i->size();
  }
  vtk_file << "POINTS " << number_points << " float" << std::endl;
  for(typename std::vector<std::vector<dim_point> >::const_iterator
      i = elements.begin(); i != elements.end(); ++i)
  {
    for(typename std::vector<dim_point>::const_iterator j = i->begin();
        j != i->end(); ++j)
    {
      for (typename dim_point::const_iterator k = j->begin();
           k != j->end(); ++k)
      {
        vtk_file << *k << " ";
      }
      // fill with zero until three coordinates are given
      for (sizeType n = dim; n < 3; n++)
      {
        vtk_file << "0 ";
      }
      vtk_file << std::endl;
    }
    vtk_file << std::endl;
  }
  // Write cells
  vtk_file << "CELLS " << elements.size() << " " <<
  (elements.size() + number_points) << std::endl;
  int point_index = 0;
  for(typename std::vector<std::vector<dim_point> >::const_iterator
      i = elements.begin(); i != elements.end(); ++i)
  {
    vtk_file << i->size();
    // Change numbering scheme for squares (VTK_QUAD = 9)
    if (element_dim == 2 && i->size() == 4)
    {
      vtk_file << " " << point_index;
      vtk_file << " " << (point_index + 1);
      vtk_file << " " << (point_index + 3);
      vtk_file << " " << (point_index + 2);
      point_index += 4;
    }
    // Change numbering scheme for cubes (VTK_HEXAHEDRON = 12)
    else if (element_dim == 3 && i->size() == 8)
    {
      vtk_file << " " << point_index;
      vtk_file << " " << (point_index + 1);
      vtk_file << " " << (point_index + 3);
      vtk_file << " " << (point_index + 2);
      vtk_file << " " << (point_index + 4);
      vtk_file << " " << (point_index + 5);
      vtk_file << " " << (point_index + 7);
      vtk_file << " " << (point_index + 6);
      point_index += 8;
    }
    // Change numbering scheme for pyramids (VTK_PYRAMID = 14)
    else if (element_dim == 3 && i->size() == 5)
    {
      vtk_file << " " << point_index;
      vtk_file << " " << (point_index + 1);
      vtk_file << " " << (point_index + 3);
      vtk_file << " " << (point_index + 2);
      vtk_file << " " << (point_index + 4);
      point_index += 5;
    }
    else
    {
      for (sizeType j = 0; j < i->size(); j++)
      {
        vtk_file << " " << point_index;
        point_index++;
      }
    }
    vtk_file << std::endl;
  }
  vtk_file << std::endl;
  // Write cell types
  vtk_file << "CELL_TYPES " << elements.size() << std::endl;
  for(typename std::vector<std::vector<dim_point> >::const_iterator
      i = elements.begin(); i != elements.end(); ++i)
  {
    int cell_type = 0;
    switch (element_dim)
    {
    case 0 :
      cell_type = 1;
      break;
    case 1 :
      cell_type = 3;
      break;
    case 2 :
      if (i->size() == 3)
      {
        cell_type = 5;
      }
      else
      {
        cell_type = 9;
      }
      break;
    case 3 :
      if (i->size() == 4)
      {
        cell_type = 10;
      }
      else if (i->size() == 8)
      {
        cell_type = 12;
      }
      else if (i->size() == 6)
      {
        cell_type = 13;
      }
      else
      {
        cell_type = 14;
      }
      break;
    }
    vtk_file << cell_type << std::endl;
  }
  vtk_file << std::endl;
  // Write point data
  vtk_file << "POINT_DATA " << number_points << std::endl <<
  "SCALARS ElementID int 1" << std::endl <<
  "LOOKUP_TABLE default" << std::endl;
  int point_id = 0;
  for(typename std::vector<std::vector<dim_point> >::const_iterator
      i = elements.begin(); i != elements.end(); ++i)
  {
    for(typename std::vector<dim_point>::const_iterator j = i->begin();
        j != i->end(); ++j)
    {
      vtk_file << point_id << " ";
    }
    point_id++;
    vtk_file << std::endl;
  }
  vtk_file.close();
  if (verbose)
  {
    std::cout << "File written: " << file_name << std::endl;
  }
}

/*
 * Main method containing all test cases.
 */
int main(int argc, char ** argv)
{
  TestMarchingCubes33 testmc33;
  int passed = 0;
  int count = 0;
  testmc33.verbose = false;
  testmc33.write_vtk = true;

  if (argc > 1)
    testmc33.verbose = (std::string("-verbose") == argv[1] || std::string("-v") == argv[1]);
  // Test any 0d (point)
  // count++;
  // passed += testmc33.testAny0d(0, 0.4, "any0d_0");
  // count++;
  // passed += testmc33.testAny0d(0, 0.8, "any0d_1");
  // Test any 1d (line)
  count++;
  passed += testmc33.testAny1d(0, 0.4, 0.2, "any1d_0");
  count++;
  passed += testmc33.testAny1d(1, 0.7, 0.1, "any1d_1");
  count++;
  passed += testmc33.testAny1d(2, 0.3, 0.7, "any1d_2");
  count++;
  passed += testmc33.testAny1d(3, 0.8, 0.7, "any1d_3");
  // Test simplex 2d
  count++;
  passed += testmc33.testSimplex2d(0, 0.2, 0.3, 0.4, "simplex2d_0");
  count++;
  passed += testmc33.testSimplex2d(1, 0.8, 0.2, 0.4, "simplex2d_1");
  count++;
  passed += testmc33.testSimplex2d(2, 0.1, 0.7, 0.5, "simplex2d_2");
  count++;
  passed += testmc33.testSimplex2d(3, 0.8, 0.8, 0.4, "simplex2d_3");
  count++;
  passed += testmc33.testSimplex2d(6, 0.3, 0.7, 0.8, "simplex2d_4");
  // Test simplex 3d
  count++;
  passed += testmc33.testSimplex3d(0, 0.2, 0.3, 0.4, 0.5, "simplex3d_0");
  count++;
  passed += testmc33.testSimplex3d(1, 0.8, 0.3, 0.4, 0.5, "simplex3d_1");
  count++;
  passed += testmc33.testSimplex3d(2, 0.2, 1.0, 0.4, 0.5, "simplex3d_2");
  count++;
  passed += testmc33.testSimplex3d(3, 0.9, 0.7, 0.4, 0.5, "simplex3d_3");
  count++;
  passed += testmc33.testSimplex3d(4, 0.2, 0.3, 0.8, 0.4, "simplex3d_4");
  count++;
  passed += testmc33.testSimplex3d(5, 0.7, 0.3, 0.8, 0.4, "simplex3d_5");
  count++;
  passed += testmc33.testSimplex3d(6, 0.2, 0.9, 0.8, 0.4, "simplex3d_6");
  count++;
  passed += testmc33.testSimplex3d(7, 0.8, 0.7, 0.9, 0.2, "simplex3d_7");
  count++;
  passed += testmc33.testSimplex3d(8, 0.2, 0.3, 0.4, 0.8, "simplex3d_8");
  count++;
  passed += testmc33.testSimplex3d(9, 0.8, 0.3, 0.4, 0.8, "simplex3d_9");
  count++;
  passed += testmc33.testSimplex3d(10, 0.2, 1.0, 0.4, 0.8, "simplex3d_10");
  count++;
  passed += testmc33.testSimplex3d(11, 0.9, 0.7, 0.4, 0.8, "simplex3d_11");
  count++;
  passed += testmc33.testSimplex3d(12, 0.2, 0.3, 0.8, 0.8, "simplex3d_12");
  count++;
  passed += testmc33.testSimplex3d(13, 0.7, 0.3, 0.8, 0.8, "simplex3d_13");
  count++;
  passed += testmc33.testSimplex3d(14, 0.2, 0.9, 0.8, 0.8, "simplex3d_14");
  count++;
  passed += testmc33.testSimplex3d(15, 0.8, 0.7, 0.9, 0.8, "simplex3d_15");
  // Test cube 2d
  count++;
  passed += testmc33.testCube2d(0, 0.1, 0.4, 0.5, 0.3, "cube2d_0");
  count++;
  passed += testmc33.testCube2d(1, 0.7, 0.4, 0.5, 0.3, "cube2d_1");
  count++;
  passed += testmc33.testCube2d(2, 0.2, 0.8, 0.5, 0.3, "cube2d_2");
  count++;
  passed += testmc33.testCube2d(3, 0.7, 0.8, 0.5, 0.3, "cube2d_3");
  count++;
  passed += testmc33.testCube2d(4, 0.1, 0.4, 0.9, 0.3, "cube2d_4");
  count++;
  passed += testmc33.testCube2d(5, 0.7, 0.4, 0.9, 0.3, "cube2d_5");
  count++;
  passed += testmc33.testCube2d(6, 0.5, 0.8, 0.7, 0.4, "cube2d_6");
  count++;
  passed += testmc33.testCube2d(7, 0.9, 0.8, 0.7, 0.3, "cube2d_7");
  count++;
  passed += testmc33.testCube2d(8, 0.1, 0.4, 0.5, 0.8, "cube2d_8");
  count++;
  passed += testmc33.testCube2d(9, 0.7, 0.5, 0.4, 0.8, "cube2d_9");
  count++;
  passed += testmc33.testCube2d(10, 0.1, 0.8, 0.4, 0.8, "cube2d_10");
  count++;
  passed += testmc33.testCube2d(11, 0.7, 0.8, 0.5, 0.8, "cube2d_11");
  count++;
  passed += testmc33.testCube2d(12, 0.1, 0.4, 0.9, 0.8, "cube2d_12");
  count++;
  passed += testmc33.testCube2d(13, 0.7, 0.4, 0.9, 0.8, "cube2d_13");
  count++;
  passed += testmc33.testCube2d(14, 0.5, 0.8, 0.7, 0.8, "cube2d_14");
  count++;
  passed += testmc33.testCube2d(15, 0.9, 0.8, 0.7, 0.8, "cube2d_15");
  count++;
  passed += testmc33.testCube2d(16, 0.1, 0.8, 0.9, 0.2, "cube2d_16");
  count++;
  passed += testmc33.testCube2d(17, 0.9, 0.1, 0.2, 0.8, "cube2d_17");
  // Test cube 3d
  // Test all transformations of a basic case
  count++;
  passed += testmc33.testCube3d(255-1, 0.4, 0.8, 0.8, 0.8,
                                0.8, 0.8, 0.8, 0.8, "cube3d_transf_0");
  count++;
  passed += testmc33.testCube3d(255-2, 0.8, 0.4, 0.8, 0.8,
                                0.8, 0.8, 0.8, 0.8, "cube3d_transf_1");
  count++;
  passed += testmc33.testCube3d(255-4, 0.8, 0.8, 0.4, 0.8,
                                0.8, 0.8, 0.8, 0.8, "cube3d_transf_2");
  count++;
  passed += testmc33.testCube3d(255-8, 0.8, 0.8, 0.8, 0.4,
                                0.8, 0.8, 0.8, 0.8, "cube3d_transf_3");
  count++;
  passed += testmc33.testCube3d(255-16, 0.8, 0.8, 0.8, 0.8,
                                0.4, 0.8, 0.8, 0.8, "cube3d_transf_4");
  count++;
  passed += testmc33.testCube3d(255-32, 0.8, 0.8, 0.8, 0.8,
                                0.8, 0.4, 0.8, 0.8, "cube3d_transf_5");
  count++;
  passed += testmc33.testCube3d(255-64, 0.8, 0.8, 0.8, 0.8,
                                0.8, 0.8, 0.4, 0.8, "cube3d_transf_6");
  count++;
  passed += testmc33.testCube3d(255-128, 0.8, 0.8, 0.8, 0.8,
                                0.8, 0.8, 0.8, 0.4, "cube3d_transf_7");
  // Test every non MC 33 basic case
  count++;
  passed += testmc33.testCube3d(0, 0.5, 0.5, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.5, "cube3d_basic_0"); // Basic case 0
  count++;
  passed += testmc33.testCube3d(1, 0.9, 0.5, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.5, "cube3d_basic_1"); // Basic case 1
  count++;
  passed += testmc33.testCube3d(3, 0.9, 0.9, 0.5, 0.5,
                                0.5, 0.5, 0.5, 0.5, "cube3d_basic_2"); // Basic case 2
  count++;
  passed += testmc33.testCube3d(33, 0.9, 0.5, 0.5, 0.5,
                                0.5, 0.9, 0.5, 0.5, "cube3d_basic_3"); // Basic case 3
  count++;
  passed += testmc33.testCube3d(129, 0.7, 0.2, 0.2, 0.2,
                                0.2, 0.2, 0.2, 0.7, "cube3d_basic_4"); // Basic case 4
  count++;
  passed += testmc33.testCube3d(14, 0.5, 0.9, 0.9, 0.9,
                                0.5, 0.5, 0.5, 0.5, "cube3d_basic_5"); // Basic case 5
  count++;
  passed += testmc33.testCube3d(131, 0.7, 0.7, 0.2, 0.2,
                                0.2, 0.2, 0.2, 0.7, "cube3d_basic_6"); // Basic case 6
  count++;
  passed += testmc33.testCube3d(67, 0.7, 0.7, 0.2, 0.2,
                                0.2, 0.2, 0.7, 0.2, "cube3d_basic_6_mirror"); // Basic case 6, key 01000011
  count++;
  passed += testmc33.testCube3d(146, 0.5, 0.9, 0.5, 0.5,
                                0.9, 0.5, 0.5, 0.9, "cube3d_basic_7"); // Basic case 7
  count++;
  passed += testmc33.testCube3d(240, 0.5, 0.5, 0.5, 0.5,
                                0.9, 0.9, 0.9, 0.9, "cube3d_basic_8"); // Basic case 8
  count++;
  passed += testmc33.testCube3d(77, 0.9, 0.5, 0.9, 0.9,
                                0.5, 0.5, 0.9, 0.5, "cube3d_basic_9"); // Basic case 9
  count++;
  passed += testmc33.testCube3d(153, 0.9, 0.5, 0.5, 0.9,
                                0.9, 0.5, 0.5, 0.9, "cube3d_basic_10"); // Basic case 10
  count++;
  passed += testmc33.testCube3d(141, 0.9, 0.5, 0.9, 0.9,
                                0.5, 0.5, 0.5, 0.9, "cube3d_basic_11"); // Basic case 11
  count++;
  passed += testmc33.testCube3d(30, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.5, 0.5, 0.5, "cube3d_basic_12"); // Basic case 12
  count++;
  passed += testmc33.testCube3d(105, 0.9, 0.5, 0.5, 0.9,
                                0.5, 0.9, 0.9, 0.5, "cube3d_basic_13"); // Basic case 13
  count++;
  passed += testmc33.testCube3d(78, 0.5, 0.9, 0.9, 0.9,
                                0.5, 0.5, 0.9, 0.5, "cube3d_basic_14"); // Basic case 14
  count++;
  passed += testmc33.testCube3d(255, 0.9, 0.9, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.9, "cube3d_basic_0_inv"); // Inverted basic case 0
  count++;
  passed += testmc33.testCube3d(255-1, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.9, "cube3d_basic_1_inv"); // Inverted basic case 1
  count++;
  passed += testmc33.testCube3d(255-3, 0.5, 0.5, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.9, "cube3d_basic_2_inv"); // Inverted basic case 2
  count++;
  passed += testmc33.testCube3d(255-33, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.5, 0.9, 0.9, "cube3d_basic_3inv"); // Inverted basic case 3
  count++;
  passed += testmc33.testCube3d(255-129, 0.5, 0.9, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.5, "cube3d_basic_4_inv"); // Inverted basic case 4
  count++;
  passed += testmc33.testCube3d(255-14, 0.9, 0.5, 0.5, 0.5,
                                0.9, 0.9, 0.9, 0.9, "cube3d_basic_5_inv"); // Inverted basic case 5
  count++;
  passed += testmc33.testCube3d(255-131, 0.5, 0.5, 0.9, 0.9,
                                0.9, 0.9, 0.9, 0.5, "cube3d_basic_6_inv"); // Inverted basic case 6
  count++;
  passed += testmc33.testCube3d(255-67, 0.5, 0.5, 0.9, 0.9,
                                0.9, 0.9, 0.5, 0.9, "cube3d_basic_6_mirror_inv"); // Inverted basic case 6
  count++;
  passed += testmc33.testCube3d(255-146, 0.9, 0.5, 0.9, 0.9,
                                0.5, 0.9, 0.9, 0.5, "cube3d_basic_7_inv"); // Inverted basic case 7
  // Test Marching cubes' 33 cases
  count++;
  passed += testmc33.testCube3d(testmc33.NO_KEY, 0.7, 0.2, 0.2, 0.2,
                                0.2, 0.7, 0.2, 0.2, "cube3d_mc33_3.2"); // MC33 case 3.2
  count++;
  passed += testmc33.testCube3d(testmc33.NO_KEY, 1.7, 0.5, 0.5, 0.5,
                                0.5, 0.5, 0.5, 1.7, "cube3d_mc33_4.2"); // MC33 case 3.2
  count++;
  passed += testmc33.testCube3d(testmc33.NO_KEY, 1.6, 1.6, -0.3, -0.3,
                                -0.3, -0.3, -0.3, 1.6, "cube3d_mc33_6.2"); // MC33 case 6.2
  count++;
  passed += testmc33.testCube3d(testmc33.NO_KEY, 1.5, .7, .2, .2, .2, .2, .2, 1.5,
                                "cube3d_mc33_6.1.2"); // MC33 case 6.1.2
  count++;
  passed += testmc33.testCube3d(testmc33.NO_KEY, .2, .2, 1.5, .7, .2, 1.5, .2, .2,
                                "cube3d_mc33_6.1.2_mirror"); // MC33 case 6.1.2 other mirror
  count++; passed += testmc33.testCube3d(testmc33.NO_KEY, 0.5, 0.9, 0.5, 0.5,
                                         0.9, 0.5, 0.5, 0.9, "cube3d_mc33_7.2"); // MC33 case 7
  count++;
  passed += testmc33.testCube3d(testmc33.NO_KEY, 0.7, 0.2, 0.2, 0.7,
                                0.7, 0.2, 0.2, 0.7, "cube3d_mc33_10.1.2"); // MC case 10.1.2
  count++;
  passed += testmc33.testCube3d(testmc33.NO_KEY, 0.7, 0.2, 0.2, 0.7,
                                0.9, 0.5, 0.5, 0.9, "cube3d_mc33_10.2"); // MC case 10.2

  if (passed < count)
  {
    std::cout << "* * * " << (count-passed) << " of " << count << " marching cubes 33 tests FAILED. * * *"
              << std::endl << "Rerun program with option -verbose for details"
              << std::endl;
    return 1;
  }
  std::cout << "All " << count << " marching cubes 33 tests passed. Congratulations."
            << std::endl;
  return 0;
}
