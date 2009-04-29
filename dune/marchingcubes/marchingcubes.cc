// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include "lut/marchinglut.hh"
#include <fstream>
#include <iostream> // FIXME TODO: Debug only, entferne mich!

#define DEBUG printf

namespace Dune {
  /*
   * Case offset tables (e.g. table_cube2d_cases offsets) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  typename MarchingCubes33<valueType, dim, thresholdFunctor>::
  offsetRow *
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_case_offsets[] = {
    NULL, NULL, NULL, table_any1d_cases_offsets,
    NULL, table_simplex2d_cases_offsets,
    table_cube2d_cases_offsets, table_simplex3d_cases_offsets,
    NULL, NULL, NULL, table_cube3d_cases_offsets
  };

  /*
   * Codimension 0 element tables (e.g. table_cube2d_codim_0) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_codim_0[] = {
    NULL, NULL, NULL, table_any1d_codim_0,
    NULL, table_simplex2d_codim_0,
    table_cube2d_codim_0, table_simplex3d_codim_0,
    NULL, NULL, NULL, table_cube3d_codim_0
  };

  /*
   * Codimension 1 elment tables (e.g. table_cube2d_codim_1) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_codim_1[] = {
    NULL, NULL, NULL, table_any1d_codim_1,
    NULL, table_simplex2d_codim_1,
    table_cube2d_codim_1, table_simplex3d_codim_1,
    NULL, NULL, NULL, table_cube3d_codim_1
  };

  /*
   * MC33 offset tables (e.g. table_cube2d_mc33_offsets) for
   * different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_mc33_offsets[] = {
    NULL, NULL, NULL, NULL, NULL, NULL,
    table_cube2d_mc33_offsets, NULL,
    NULL, NULL, NULL, table_cube3d_mc33_offsets
  };

  /*
   * Test face tables (e.g. table_cube2d_mc33_face_test_order) for
   * different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_face_tests[] = {
    NULL, NULL, NULL, NULL, NULL, NULL,
    table_cube2d_mc33_face_test_order, NULL,
    NULL, NULL, NULL, table_cube3d_mc33_face_test_order
  };

  /*
   * \brief Calculates the key in the marching cubes' case table
   * for the given element.
   *
   * The key is necessary to calculate the offset only once, even if
   * co-dimension 0 and co-dimension 1 will be requested.
   *
   * \param vertex_values Element's vertex values.
   * \param vertex_count Number of vertices, same as length of <code>
   *                     vertex_values</code>.
   * \param use_mc_33 specifies whether marching cubes' 33 case table
   *                  should be used. Marching cubes' 33 leads to more
   *                  elements but they are topological correct.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  typename MarchingCubes33<valueType, dim, thresholdFunctor>::sizeType
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  getKey(const valueVector& vertex_values, const sizeType vertex_count,
         const bool use_mc_33)
  {
    if ((dim < 0) || (dim > 3))
    {
      DUNE_THROW(IllegalArgumentException,
                 "Dimension must be 0, 1, 2 or 3, not " << dim << ".");
    }
    else if (dim == 0)
    {
      return 0;
    }
    const short (* const table_case_offsets)[5] =
      all_case_offsets[vertex_count + dim];
    const short * const table_mc33_offsets =
      all_mc33_offsets[vertex_count + dim];
    const short * const table_mc33_face_test_order =
      all_face_tests[vertex_count + dim];

    // vector containing information if vertices are inside or not
    bool * vertex_inside = new bool[vertex_count];
    int case_number = 0;
    for (sizeType i = vertex_count; i > 0; i--)
    {
      case_number *= 2;
      // Set bit to 0 if vertex is inside
      vertex_inside[i-1] = 1 - thresholdFunctor::isInside(vertex_values[i-1]);
      case_number += (int) vertex_inside[i-1];
    }

    // Is it a marching cubes' 33 case?
    bool ambiguous_case =
      (CASE_AMBIGUOUS_MC33 ==
       (CASE_AMBIGUOUS_MC33 & table_case_offsets[case_number][INDEX_UNIQUE_CASE]));
    // if it's not unique get the correct one
    if (use_mc_33 && ambiguous_case)
    {
      // find face tests for the case
      sizeType test_index = (sizeType) table_mc33_offsets[case_number];
      // offsets to have a binary tree like behavior
      sizeType tree_offset = 1;
      // perform tests and find case number
      short test = table_mc33_face_test_order[test_index + tree_offset];
      bool not_inverted =
        (CASE_INVERTED !=
         (CASE_INVERTED & table_case_offsets[case_number][(sizeType) INDEX_UNIQUE_CASE]));

      GeometryType geo_type;
      geo_type.makeQuadrilateral();
      ReferenceElementContainer<ctype, dim> rec;
      const ReferenceElement<ctype, dim> & ref_element = rec(geo_type);
      valueType corner_a, corner_b, corner_c, corner_d;
      DEBUG("---- AMBIGUOUS\n");
      // tests are negative, non-negativ values are offsets
      while ((test < 0) && (test != CASE_IS_REGULAR))
      {
        DEBUG("++++ test: %d\n", test);
        if (dim == 3)
        {
          // face tests are stored inverted and face 0 is stored as -6
          int face = (-1 * test) % 6;
          DEBUG("test face: %i\n", face);
          corner_a = vertex_values[ref_element.subEntity(face, 1, 0, dim)];
          corner_b = vertex_values[ref_element.subEntity(face, 1, 1, dim)];
          corner_c = vertex_values[ref_element.subEntity(face, 1, 2, dim)];
          corner_d = vertex_values[ref_element.subEntity(face, 1, 3, dim)];
        }
        else if (dim == 2)
        {
          corner_a = vertex_values[0];
          corner_b = vertex_values[1];
          corner_c = vertex_values[2];
          corner_d = vertex_values[3];
        }
        else
        {
          DUNE_THROW(IllegalArgumentException, "MC 33 cases should"
                     << " occur with dimension 2 or 3, not " << dim << ".");
        }
        // calculate index position (if test is true: 2*index, otherwise: 2*index+1)
        tree_offset *= 2;
        bool test_result = (test == TEST_CENTER) ?
                           testAmbiguousCenter(vertex_values, vertex_count, not_inverted) :
                           testAmbiguousFace(corner_a, corner_b, corner_c, corner_d, not_inverted);
        //DEBUG("test_result: %d\n", test_result);
        tree_offset += (1 - test_result);
        DEBUG("test result: %d\n", test_result);
        test = table_mc33_face_test_order[test_index + tree_offset];
        DEBUG("next test: %d\n", test);
        DEBUG("regular is: %d\n", CASE_IS_REGULAR);
      }
      if (test != CASE_IS_REGULAR)
      {
        case_number = test;
      }
    }
    return case_number;
  }

  /*
   * \brief Calculates partition with marching cubes' algorithm for
   * the given key which specifies base case and transformation.
   *
   * Result will be stored in <code>elements</code> which is a vector
   * with an entry for every element; an element is represented by
   * a vector of its points. The key specifies the offset for in
   * the case table and must be generated from <code>getKey</code>.
   * The key is necessary to calculate the offset only once, even if
   * co-dimension 0 and co-dimension 1 will be requested. Co-dimension
   * 1 is the isosurface, co-dimension 0 is the volumen inside the
   * isosurface.
   *
   * \param vertex_values Element's vertex values.
   * \param vertex_count Number of vertices, same as length of <code>
   *                     vertex_values</code>.
   * \param key specifies the offset for the case table and must be
   *            generated from <code>getKey</code>.
   * \param codim_1_not_0 defines whether elements of co-dimension 1
   *                      (e.g. faces in 3D) will returned or of
   *                      co-dimension 0 (e.g. volumes in 3D).
   * \param elements where the resulting coordinates will be stored.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getElements(const valueVector& vertex_values,
              const sizeType vertex_count, const sizeType key,
              const bool codim_1_not_0,
              std::vector<std::vector<point> >& elements)
  {
    if (dim == 0)
    {
      if (thresholdFunctor::isInside(vertex_values[0]))
      {
        elements.resize(1);
        elements[1].resize(0);
      }
      else
      {
        elements.resize(0);
      }
    }
    else
    {
      sizeType element_count = all_case_offsets
                               [vertex_count + dim][key][INDEX_COUNT_CODIM_0];
      const short (* codim_index) = all_codim_0[vertex_count + dim]
                                    + all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_0];
      if (codim_1_not_0)
      {
        element_count = all_case_offsets
                        [vertex_count + dim][key][INDEX_COUNT_CODIM_1];
        codim_index = all_codim_1[vertex_count + dim]
                      + all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_1];
      }
      /*DEBUG(">>> %i Daten: %p\n %p %p\n %p %p\n %p %p\n", (int)key,
              (codim_index - all_case_offsets[vertex_count + dim][key][codim_1_not_0?INDEX_OFFSET_CODIM_1:INDEX_OFFSET_CODIM_0]),
              table_any1d_codim_0, table_any1d_codim_1,
              table_simplex2d_codim_0, table_simplex2d_codim_1,
              table_cube2d_codim_0, table_cube2d_codim_1);*/
      elements.resize(element_count);
      // DEBUG("Anzahl Elemente: %d \n", (int)caseCountElements);
      for (sizeType i = 0; i < element_count; i++)
      {
        sizeType point_count = (sizeType) codim_index[0];
        // Vector for storing the element points
        elements[i].resize(point_count);
        //DEBUG(" Debug vectorsize: %d %d\n", (int)numberOfPoints, (int)offsets[INDEX_OFFSET_CODIM_1]);
        // Read points from table and store them
        for (sizeType j = 0; j < point_count; j++)
        {
          getCoordsFromNumber(vertex_values, vertex_count, codim_index[j+1], elements[i][j]);
          //DEBUG("   Loop debug output: j %d / vertex number %d / results: %1.1f %1.1f\n", (int)j, (int)index[j+1], elements[i][j][0], elements[i][j][1]);
        }
        // increase index for pointing to the next element
        codim_index += point_count + 1;
      }
    }
  }

  /**
   * \brief Generates the coordinate for a point which is specified
   * by its vertex or edge number.
   *
   * Result will be stored in <code>coords</code>. The coordinate for in
   * the middle of an edge is interpolated with respect to both vertex
   * values; the one for center point with respect to all eight vertex
   * values. The center point must be used only for 3D-cubes.
   *
   * \param vertex_values Element's vertex values.
   * \param vertex_count Number of vertices, same as length of <code>
   *                     vertex_values</code>.
   * \param number specifies the point of which the coordinates should
   *               be generated; should be a <code>const</code> from
   *               \ref marchinglut.hh .
   * \param coord where the resulting coordinates will be stored.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getCoordsFromNumber(const valueVector& vertex_values,
                      const sizeType vertex_count, const short number,
                      point& coord) const
  {
    // it's a center point
    if (number == EY)
    {
      //TODO: Testen

      // Initialize point
      for (sizeType i = 0; i < dim; i++)
      {
        coord[i] = 0.0;
      }
      // Mean from each threshold value on an edge
      short vertex_1, vertex_2;
      sizeType count = 0;
      for (short i = EJ; i <= EU; i++)
      {
        vertex_1 = (i / FACTOR_FIRST_POINT) &
                   (VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP);
        vertex_2 = (i / FACTOR_SECOND_POINT) &
                   (VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP);
        if (thresholdFunctor::isInside(vertex_1) !=
            thresholdFunctor::isInside(vertex_2))
        {
          point edge_point;
          getCoordsFromEdgeNumber(vertex_values, vertex_count, i,
                                  edge_point);
          for (sizeType j = 0; j < dim; j++)
          {
            coord[j] += edge_point[j];
          }
          count++;
        }
      }
      for (sizeType i = 0; i < dim; i++)
      {
        coord[i] /= count;
      }
    }
    // it's an edge
    else if ((number & NO_VERTEX) == NO_VERTEX)
    {
      // get both vertices
      point point_a, point_b;
      getCoordsFromEdgeNumber(vertex_values, vertex_count,
                              number, point_a);
      getCoordsFromEdgeNumber(vertex_values, vertex_count,
                              (number / FACTOR_SECOND_POINT * FACTOR_FIRST_POINT), point_b);
      // get indices for point in valueVector
      sizeType index_a = 0;
      sizeType index_b = 0;
      for (sizeType i = 0; i < dim; i++)
      {
        index_a += (sizeType) point_a[i] * (1<<i);
        index_b += (sizeType) point_b[i] * (1<<i);
      }
      // factor for interpolation
      valueType interpol_factor =
        thresholdFunctor::getDistance(vertex_values[index_a])
        / (thresholdFunctor::getDistance(vertex_values[index_b])
           - thresholdFunctor::getDistance(vertex_values[index_a]));
      //DEBUG("     Kante: coords %1.3f %1.3f davor indexA %d  indexB %d // %d %d\n", coords[0], coords[1], indexA, indexB, NO_VERTEX^number, number);
      // calculate interpolation point
      for (sizeType i = 0; i < dim; i++)
      {
        coord[i] = point_a[i] - interpol_factor * (point_b[i] - point_a[i]);
      }
      //   DEBUG("     Kante: coords %1.3f %1.3f / A` %1.3f B` %1.3f \n", coords[0], coords[1], thresholdFunctor::getDistance(vertexValues[indexA]), thresholdFunctor::getDistance(vertexValues[indexB]));

    }
    // it's a vertex
    else
    {
      getCoordsFromEdgeNumber(vertex_values, vertex_count,
                              number, coord);
    }
  }

  /**
   * \brief Generates the coordinate for a vertex which is specified
   * by its vertex number.
   *
   * Result will be stored to <code>coord</code>. <code>number</code>
   * must be an valid vertex number, otherwise the result of the method
   * will be unspecified.
   *
   * \param vertex_values Element's vertex values.
   * \param vertex_count Number of vertices, same as length of <code>
   *                     vertex_values</code>.
   * \param number specifies the point of which the coordinates should
   *               be generated; should be a <code>const</code> from
   *               \ref marchinglut.hh .
   * \param coord where the resulting coordinates will be stored.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getCoordsFromEdgeNumber(const valueVector& vertex_values,
                          const sizeType vertex_count, char number,
                          point& coord) const
  {
    number /= FACTOR_FIRST_POINT;
    // Get coordinate for each dimension. It is either 0 or 1.
    for (sizeType d = 0; d < dim; d++)
    {
      coord[d] = (ctype) ((number & 1<<d) != 0);
    }
  }

  /*
   * \brief Tests whether vertices are connected by the middle of the face.
   *
   * This test is needed to chose between ambiguous MC33 cases. It checks
   * whether two vertices are connected by the middle of the face or whether
   * they are separated. This method is implemented according to the paper
   * from Lewiner et al. It should be only applied on squares like 2D-cube
   * (rectangles) or faces of 3D-cubes.
   *
   * \param corner_a Value of the first face vertex.
   * \param corner_b Value of the second face vertex.
   * \param corner_c Value of the third face vertex.
   * \param corner_d Value of the forth face vertex.
   * \param not_inverted Whether basic case is not inverted.
   *
   * \return <code>True</true> if vertices are connected.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  bool MarchingCubes33<valueType, dim, thresholdFunctor>::
  testAmbiguousFace(const valueType corner_a, const valueType corner_b,
                    const valueType corner_c, const valueType corner_d,
                    const bool not_inverted) const
  {
        #warning DEBUGCODE
    assert(not_inverted == true);
    // Change naming scheme to jgt-paper ones
    double a = thresholdFunctor::getDistance(corner_a);
    double b = thresholdFunctor::getDistance(corner_c);
    double c = thresholdFunctor::getDistance(corner_d);
    double d = thresholdFunctor::getDistance(corner_b);

    bool result_orig = false;
    // Check A*C == B*D
        #warning WARUM?
    if ((a*c - b*d) == 0.0)
    {
      result_orig = not_inverted;
    }
    else
    {
      // not_inverted and a may invert the sign
      result_orig = ((not_inverted*2 - 1) * a * (a*c - b*d) >= 0.0);
    }
    // Cb Dc
    // Aa Bd
    bool result_other = ((a*c-b*d)/(c+a-d-b) >= 0.0);
    if (result_other != result_orig)
    {
      std::cout << "not_inverted " << not_inverted << "\n";
      std::cout << "WARNING: unexpected result " << (a*c - b*d) << " FACETEST "
                << a << " "
                << d << " "
                << b << " "
                << c << " "
                << " : " << result_orig << " != " << result_other << "\n";
    }
    return result_other;
    return result_orig;
  }

  /*
   * \brief Tests whether vertices are connected by the middle of the cube.
   *
   * This test is needed to chose between ambiguous MC33 cases. It checks
   * whether two vertices are connected by the center of the cube or whether
   * they are separated. This method is implemented according to the paper
   * from Lewiner et al. It should be only applied on 3D-cubes.
   *
   * \param vertex_values Cube's vertex values.
   * \param vertex_count Number of vertices, should be eight.
   * \param not_inverted Whether basic case is not inverted.
   *
   * \return <code>True</true> if vertices are connected.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  bool MarchingCubes33<valueType, dim, thresholdFunctor>::
  testAmbiguousCenter(const valueVector& vertex_values,
                      const sizeType vertex_count, const bool not_inverted) const
  {
    DEBUG("testCenter\n");
    assert(dim==3);
    // TODO: mit Lewiner vergleichen. Testen!
    const double a0 = thresholdFunctor::getDistance(vertex_values[0]);
    const double b0 = thresholdFunctor::getDistance(vertex_values[2]);
    const double c0 = thresholdFunctor::getDistance(vertex_values[3]);
    const double d0 = thresholdFunctor::getDistance(vertex_values[1]);
    const double a1 = thresholdFunctor::getDistance(vertex_values[5]);
    const double b1 = thresholdFunctor::getDistance(vertex_values[7]);
    const double c1 = thresholdFunctor::getDistance(vertex_values[8]);
    const double d1 = thresholdFunctor::getDistance(vertex_values[6]);

    const double a =  (a1 - a0) * (c1 - c0) - (b1 - b0) * (d1 - d0);
    if (a >= 0.0)
    {
      return not_inverted;
    }
    const double b =  c0*(a1 - a0) + a0*(c1 - c0) - d0*(b1 - b0) - b0*(d1 - d0);
    const double t_max = -0.5 * b / a;
    if ((0.0 >= t_max) || (1.0 <= t_max))
    {
      return not_inverted;
    }
    //const double c =  (a0 * c0) - (b0 * d0);
    const double at = a0 + (a1 - a0) * t_max;
    const double bt = b0 + (b1 - b0) * t_max;
    const double ct = c0 + (c1 - c0) * t_max;
    const double dt = d0 + (d1 - d0) * t_max;
    const bool inequation_4 = (at*ct - bt*dt > 0.0);
    const bool corner_signs = (at*ct > 0.0) && (bt*dt > 0.0)
                              && (at*bt < 0.0);
    return (inequation_4 && corner_signs) != not_inverted;
  }

} // end namespace Dune
