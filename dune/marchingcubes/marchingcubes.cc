// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include <iostream> // FIXME TODO: Debug only, entferne mich!

namespace Dune {
  /*
   * TODO: Comment
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  typename MarchingCubes33<valueType, dim, thresholdFunctor>::
  offsetRow *
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_case_offsets[] = {
    NULL, NULL, NULL, NULL, table_simplex2d_cases_offsets,
    table_cube2d_cases_offsets, table_simplex3d_cases_offsets,
    NULL, NULL, NULL, table_cube3d_cases_offsets
  };

  /*
   * TODO: Comment
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_codim_0[] = {
    NULL, NULL, NULL, NULL, table_simplex2d_codim_0,
    table_cube2d_codim_0, table_simplex3d_codim_0,
    NULL, NULL, NULL, table_cube3d_codim_0
  };

  /*
   * TODO: Comment
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_codim_1[] = {
    NULL, NULL, NULL, NULL, table_simplex2d_codim_1,
    table_cube2d_codim_1, table_simplex3d_codim_1,
    NULL, NULL, NULL, table_cube3d_codim_1
  };

  /*
   * TODO: Comment
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_mc33_offsets[] = {
    NULL, NULL, NULL, NULL, NULL,
    table_cube2d_mc33_offsets, NULL,
    NULL, NULL, NULL, table_cube3d_mc33_offsets
  };

  /*
   * TODO: Comment
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_face_tests[] = {
    NULL, NULL, NULL, NULL, NULL,
    table_cube2d_mc33_face_test_order, NULL,
    NULL, NULL, NULL, table_cube3d_mc33_face_test_order
  };

  /*
   * Calculate key to access cube2d_cases_offsets.
   * Return value indicates a mc33 case.
   *
   * \return True if the case is in the regular table, false if it's a MC33-only case.
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
    else if ((dim == 0) || (dim == 1))
    {
      DUNE_THROW(IllegalArgumentException,
                 "For dimension 0 or 1 getKey() is not needed.");
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
    for (sizeType i = 0; i < vertex_count; i++)
    {
      case_number *= 2;
      // Set bit to 0 if vertex is inside
      vertex_inside[i] = 1 - thresholdFunctor::isInside(vertex_values[i]);
      case_number += (int) vertex_inside[i];
    }

    // Is it a marching cubes' 33 case?
    bool ambiguous_case = (CASE_AMBIGUOUS_MC33 ==
                           table_case_offsets[case_number][4] & CASE_AMBIGUOUS_MC33);
    // if it's not unique get the correct one
    if (use_mc_33 && ambiguous_case)
    {
      // find face tests for the case
      sizeType test_index = (sizeType) table_mc33_offsets[case_number];
      // offsets to have a binary tree like behavior
      sizeType tree_offset = 1;
      // perform tests and find case number
      short face = table_mc33_face_test_order[test_index + tree_offset];
      bool not_inverted = (CASE_INVERTED == CASE_INVERTED &
                           table_case_offsets[case_number][(sizeType) INDEX_UNIQUE_CASE]);

      GeometryType geo_type;
      geo_type.makeQuadrilateral();
      ReferenceElementContainer<ctype, dim> rec;
      const ReferenceElement<ctype, dim> & ref_element = rec(geo_type);
      valueType corner_a, corner_b, corner_c, corner_d;
      // tests are non-positive, positive values are offsets
      while ((face <= 0) && (face != CASE_IS_REGULAR))
      {
        if (dim == 3)
        {
          corner_a = vertex_values[ref_element.subEntity(face, 1, 0, dim)];
          corner_b = vertex_values[ref_element.subEntity(face, 1, 2, dim)];
          corner_c = vertex_values[ref_element.subEntity(face, 1, 3, dim)];
          corner_d = vertex_values[ref_element.subEntity(face, 1, 4, dim)];
        }
        else if (dim == 2)
        {
          corner_a = vertex_values[0];
          corner_b = vertex_values[1];
          corner_c = vertex_values[2];
          corner_d = vertex_values[3];
        }
        // calculate index position (if test is true: 2*index, otherwise: 2*index+1)
        tree_offset *= 2;
        tree_offset += (1 - testAmbiguousFace(
                          corner_a, corner_b, corner_c, corner_d, not_inverted));
        face = table_mc33_face_test_order[test_index + tree_offset];
      }
      if (face != CASE_IS_REGULAR)
      {
        case_number = face;
      }
    }
    return case_number;
  }

  /*
   * Marching cubes' algorithm.
   * vertex_values: pointer to an array containing vertices' values
   * vertex_count: count of vertices (array length)
   * threshold: value of the isosurface
   * smaller_inside: whether smaller values are inside the isosurface
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getElements(const valueVector& vertex_values,
              const sizeType vertex_count, const sizeType key,
              std::vector<std::vector<point> >& elements,
              const bool codim_1_not_0)
  {
    sizeType element_count = all_case_offsets
                             [vertex_count + dim][key][INDEX_COUNT_CODIM_0];
    const short (* codim_index) = all_codim_0[vertex_count + dim]
                                  + all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_1];
    if (codim_1_not_0)
    {
      element_count = all_case_offsets
                      [vertex_count + dim][key][INDEX_COUNT_CODIM_1];
      codim_index = all_codim_1[vertex_count + dim]
                    + all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_0];
    }
    elements.resize(element_count);
    // printf("Anzahl Elemente: %d \n", (int)caseCountElements);
    for (sizeType i = 0; i < element_count; i++)
    {
      sizeType point_count = (sizeType) codim_index[0];
      // Vector for storing the element points
      elements[i].resize(point_count);
      //printf(" Debug vectorsize: %d %d\n", (int)numberOfPoints, (int)offsets[INDEX_OFFSET_CODIM_1]);
      // Read points from table and store them
      for (sizeType j = 0; j < point_count; j++)
      {
        getCoordsFromNumber(vertex_values, vertex_count, codim_index[j+1], elements[i][j]);
        //printf("   Loop debug output: j %d / vertex number %d / results: %1.1f %1.1f\n", (int)j, (int)index[j+1], elements[i][j][0], elements[i][j][1]);
      }
      // increase index for pointing to the next element
      codim_index += point_count + 1;
    }
  }

  /*
   * TODO: Kommentar schreiben
   */
  /*TODO: folgende nutzlose(?) Methode entfernen*/
  template <typename valueType, int dim, typename thresholdFunctor>
  typename MarchingCubes33<valueType, dim, thresholdFunctor>::sizeType
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  getMc33case(const valueVector& vertex_values,
              const sizeType vertex_count, char number) const
  {
    return (sizeType) 0;
  }

  /**
   * \brief Generates the coordinate for a point which is specified
   * by its vertex or edge number.
   *
   * Result will be stored to <code>coords</code>.
   * \param vertex_values array with all vertex values in it.
   * \param vertex_count number of vertices in <code>vertex_values</code>.
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
      //TODO: Koordinaten für Mittelpunkt ausrechnen

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
      //printf("     Kante: coords %1.3f %1.3f davor indexA %d  indexB %d // %d %d\n", coords[0], coords[1], indexA, indexB, NO_VERTEX^number, number);
      // calculate interpolation point
      for (sizeType i = 0; i < dim; i++)
      {
        coord[i] = point_a[i] - interpol_factor * (point_b[i] - point_a[i]);
      }
      //   printf("     Kante: coords %1.3f %1.3f / A` %1.3f B` %1.3f \n", coords[0], coords[1], thresholdFunctor::getDistance(vertexValues[indexA]), thresholdFunctor::getDistance(vertexValues[indexB]));

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
   * Result will be stored to \param coords.
   *
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
   * \brief Test if the face center is covered by the surface.
   *
   * This test is needed to chose between ambiguous MC33 cases.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  bool MarchingCubes33<valueType, dim, thresholdFunctor>::
  testAmbiguousFace(const valueType corner_a, const valueType cornerB,
                    const valueType cornerC, const valueType cornerD,
                    const bool notInverted) const
  {
    // Change naming scheme to jgt-paper ones
    double a = thresholdFunctor::getDistance(corner_a);
    double b = thresholdFunctor::getDistance(cornerC);
    double c = thresholdFunctor::getDistance(cornerD);
    double d = thresholdFunctor::getDistance(cornerB);

    // Check A*C == B*D
    if (FloatCmp::eq((a*c - b*d), 0.0))
    {
      return notInverted;
    }
    // notInverted and a may invert the sign
    return ((notInverted*2 - 1) * a * (a*c - b*d) >= 0.0);
  }

  /*
   * \brief Test if the face center is inside the isosurface.
   *
   * This test is needed to chose between ambiguous MC33 cases.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  bool MarchingCubes33<valueType, dim, thresholdFunctor>::
  testAmbiguousCenter(const valueVector& vertex_values,
                      const sizeType vertex_count, const bool not_inverted) const
  {
    const double a0 = vertex_values[0];
    const double b0 = vertex_values[2];
    const double c0 = vertex_values[3];
    const double d0 = vertex_values[1];
    const double a1 = vertex_values[5];
    const double b1 = vertex_values[7];
    const double c1 = vertex_values[8];
    const double d1 = vertex_values[6];

    const double a =  (a1 - a0) * (c1 - c0) - (b1 - b0) * (d1 - d0);
    if (a >= 0.0)
    {
      return !not_inverted;
    }
    const double b =  c0*(a1 - a0) + a0*(c1 - c0) - d0*(b1 - b0) - b0*(d1 - d0);
    const double t_max = -0.5 * b / a;
    if ((0.0 >= t_max) || (1.0 <= t_max))
    {
      return !not_inverted;
    }
    //const double c =  (a0 * c0) - (b0 * d0);
    const double at = a0 + (a1 - a0) * t_max;
    const double bt = b0 + (b1 - b0) * t_max;
    const double ct = c0 + (c1 - c0) * t_max;
    const double dt = d0 + (d1 - d0) * t_max;
    const bool inequation_4 = (at*ct - bt*dt > 0.0);
    const bool corner_signs = (at*ct > 0.0) && (bt*dt > 0.0)
                              && (at*bt < 0.0);
    return (inequation_4 && corner_signs) == not_inverted;
  }

} // end namespace Dune
