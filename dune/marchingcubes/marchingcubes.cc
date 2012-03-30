// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#if HAVE_CONFIG
#include <config.h>
#endif

#include "lut/marchinglut.hh"
#include "isdegenerated.hh"

#include <dune/geometry/type.hh>
#include <dune/geometry/referenceelements.hh>

#include <fstream>
#include <cmath>

#ifndef NDEBUG
#include <iostream> // FIXME TODO: Debug only, entferne mich!
#endif

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
    table_pyramid3d_cases_offsets, table_prism3d_cases_offsets,
    NULL, table_cube3d_cases_offsets
  };

  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_vertex_to_index[] = {
    NULL, NULL, NULL, table_any1d_vertex_to_index,
    NULL, table_simplex2d_vertex_to_index,
    table_cube2d_vertex_to_index, table_simplex3d_vertex_to_index,
    table_pyramid3d_vertex_to_index, table_prism3d_vertex_to_index,
    NULL, table_cube3d_vertex_to_index
  };

  /*
   * vertex_groups tables (e.g. table_cube2d_vertex_groups) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_vertex_groups[] = {
    NULL, NULL, NULL, table_any1d_vertex_groups,
    NULL, table_simplex2d_vertex_groups,
    table_cube2d_vertex_groups, table_simplex3d_vertex_groups,
    table_pyramid3d_vertex_groups, table_prism3d_vertex_groups,
    NULL, table_cube3d_vertex_groups
  };

  /*
   * Codimension 0 element tables (e.g. table_cube2d_codim_0) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_codim_0[][2] = {
    {NULL, NULL}, {NULL, NULL}, {NULL, NULL},
    {table_any1d_codim_0_interior, table_any1d_codim_0_exterior},
    {NULL, NULL}, {table_simplex2d_codim_0_interior,
                   table_simplex2d_codim_0_exterior},
    {table_cube2d_codim_0_interior, table_cube2d_codim_0_exterior},
    {table_simplex3d_codim_0_interior, table_simplex3d_codim_0_exterior},
    {table_pyramid3d_codim_0_interior, table_pyramid3d_codim_0_exterior},
    {table_prism3d_codim_0_interior, table_prism3d_codim_0_exterior},
    {NULL, NULL},
    {table_cube3d_codim_0_interior, table_cube3d_codim_0_exterior}
  };

  /*
   * element group tables (e.g. table_cube2d_codim_0_exterior_groups)
   * for different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_element_groups[][2] = {
    {NULL, NULL}, {NULL, NULL}, {NULL, NULL},
    {table_any1d_interior_groups, table_any1d_exterior_groups},
    {NULL, NULL}, {table_simplex2d_interior_groups,
                   table_simplex2d_exterior_groups},
    {table_cube2d_interior_groups, table_cube2d_exterior_groups},
    {table_simplex3d_interior_groups, table_simplex3d_exterior_groups},
    {table_pyramid3d_interior_groups, table_pyramid3d_exterior_groups},
    {table_prism3d_interior_groups, table_prism3d_exterior_groups},
    {NULL, NULL},
    {table_cube3d_interior_groups, table_cube3d_exterior_groups}
  };

  /*
   * Codimension 1 element tables (e.g. table_cube2d_codim_1) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  const short * const
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  all_codim_1[] = {
    NULL, NULL, NULL, table_any1d_codim_1,
    NULL, table_simplex2d_codim_1,
    table_cube2d_codim_1, table_simplex3d_codim_1,
    table_pyramid3d_codim_1, table_pyramid3d_codim_1, NULL,
    table_cube3d_codim_1
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
    table_pyramid3d_mc33_offsets, table_prism3d_mc33_offsets, NULL,
    table_cube3d_mc33_offsets
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
    table_pyramid3d_mc33_face_test_order,
    table_prism3d_mc33_face_test_order, NULL,
    table_cube3d_mc33_face_test_order
  };

  /** \brief Calculates the key in the marching cubes' case table
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
  template <typename valueVector>
  typename MarchingCubes33<valueType, dim, thresholdFunctor>::sizeType
  MarchingCubes33<valueType, dim, thresholdFunctor>::
  getKey(const valueVector& vertex_values, const sizeType vertex_count,
         const bool use_mc_33) const
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
    const short (* const table_case_offsets)[10] =
      all_case_offsets[vertex_count + dim];
    const short * const table_mc33_offsets =
      all_mc33_offsets[vertex_count + dim];
    const short * const table_mc33_face_test_order =
      all_face_tests[vertex_count + dim];

    // vector containing information if vertices are inside or not
    int case_number = 0;
    for (sizeType i = vertex_count; i > 0; i--)
    {
      case_number *= 2;
      // Set bit to 0 if vertex is inside
      case_number |= !thresholdFunctor::isInside(vertex_values[i-1]);
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

      GeometryType geo_type;
      switch (vertex_count) {
      case 5 : geo_type.makePyramid(); break;
      case 6 : geo_type.makePrism(); break;
      default : geo_type.makeCube(dim);
      }
      const GenericReferenceElement<ctype, dim> & ref_element =
        GenericReferenceElements<ctype, dim>::general(geo_type);
      valueType corner_a, corner_b, corner_c, corner_d;
#ifndef NDEBUG
      std::cout << "---- AMBIGUOUS:";
      for (sizeType i = 0; i<vertex_count; ++i)
        std::cout << "v" << i << " = " << vertex_values[i] << "\n";
      std::cout << std::endl;
#endif
      // tests are negative, non-negativ values are offsets
      while ((test < 0) && (test != -CASE_IS_REGULAR))
      {
        assert(test != TEST_INVALID);
#ifndef NDEBUG
        if (dim < 2 || dim > 3)
        {
          DUNE_THROW(IllegalArgumentException, "MC 33 cases should"
                     << " occur with dimension 2 or 3, not " << dim << ".");
        }
#endif

        bool test_result = false;
#ifndef NDEBUG
        std::cout << "++++ case-nr: " << case_number << ", test: "
                  << test << ", test-index: " << test_index
                  << std::endl;
#endif
        if ((-test) & TEST_FACE)
        {
          size_t face = (-test - TEST_FACE) & ~TEST_FACE_FLIP;
#ifndef NDEBUG
          std::cout << "++++ testing face " << face << std::endl;
#endif
          corner_a = vertex_values[ref_element.subEntity(face, dim-2, 0, dim)];
          corner_b = vertex_values[ref_element.subEntity(face, dim-2, 1, dim)];
          corner_c = vertex_values[ref_element.subEntity(face, dim-2, 2, dim)];
          corner_d = vertex_values[ref_element.subEntity(face, dim-2, 3, dim)];
#ifndef NDEBUG
          std::cout << "vertices " << corner_a << " "  << corner_b << " "  << corner_c << " "  << corner_d << "\n";
#endif
          bool inverse = (-test - TEST_FACE) & TEST_FACE_FLIP;
          test_result = testAmbiguousFace(corner_a, corner_b, corner_c, corner_d, inverse);
        }
        else if ((-test) & TEST_INTERIOR)
        {
          size_t refCorner = -test - TEST_INTERIOR;
          test_result = testAmbiguousCenter(vertex_values, vertex_count, refCorner);
        }
        else
        {
          DUNE_THROW(IllegalArgumentException, "MC 33 test must be either"
                     "TEST_FACE or TEST_INTERIOR.");
        }
        // calculate next index position (if test is true: 2*index, otherwise: 2*index+1)
        tree_offset *= 2;
        tree_offset |= !test_result;
        test = table_mc33_face_test_order[test_index + tree_offset];
#ifndef NDEBUG
        std::cout << "test_result: " << test_result << std::endl;
        std::cout << "next test: " << test << std::endl;
        std::cout << "regular is: " << CASE_IS_REGULAR << std::endl;
#endif
      }
      if (test != CASE_IS_REGULAR)
      {
        case_number = test;
      }
#ifndef NDEBUG
      std::cout << "mc33: case is: " << case_number << std::endl;
#endif
    }
    return case_number;
  }

  /** \brief Calculates partition with marching cubes' algorithm for
   * the given key which specifies base case and transformation.
   *
   * Result will be stored in <code>elements</code> which is a vector
   * with an entry for every element; an element is represented by
   * a vector of its points. The key specifies the offset for in
   * the case table and must be generated from <code>getKey</code>.
   * The key is necessary to calculate the offset only once, even if
   * co-dimension 0 and co-dimension 1 will be requested. Co-dimension
   * 1 is the isosurface, co-dimension 0 is the volume inside the
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
   * \param exterior_not_interior defines whether elements of the
   *                              interior or exterior are generated.
   *                              only affects codim0.
   * \param elements where the resulting coordinates will be stored.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  template <typename valueVector>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getElements(const valueVector& vertex_values,
              const sizeType vertex_count, const sizeType key,
              const bool codim_1_not_0,
              const bool exterior_not_interior,
              std::vector<std::vector<point> >& elements) const
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
                               [vertex_count + dim][key][INDEX_COUNT_CODIM_0[int(exterior_not_interior)]];
      const short (* codim_index) = all_codim_0[vertex_count + dim][int(exterior_not_interior)]
                                    + all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_0[int(exterior_not_interior)]];
      if (codim_1_not_0)
      {
        element_count = all_case_offsets
                        [vertex_count + dim][key][INDEX_COUNT_CODIM_1];
        codim_index = all_codim_1[vertex_count + dim]
                      + all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_1];
      }
      elements.reserve(element_count);
      for (sizeType i = 0; i < element_count; i++)
      {
        sizeType point_count = (sizeType) codim_index[0];
        // Vector for storing the element points
        std::vector<point> element;
        element.resize(point_count);
        for (sizeType j = 0; j < point_count; j++)
        {
          getCoordsFromNumber(vertex_values, vertex_count, codim_index[j+1], element[j]);
        }
        if (codim_1_not_0)
        {
          if (! IsDegenerated<ctype,dim-1>::check(element))
            elements.push_back(element);
        }
        else
        {
          if (! IsDegenerated<ctype,dim>::check(element))
            elements.push_back(element);
        }
        // increase index for pointing to the next element
        codim_index += point_count + 1;
      }
    }
  }

  /**
   * \brief returns connectivity information of the reference vertices
   * for a partition obtained by <code>getElements</code>
   *
   * Result will be stored in <code>vertex_groups</code>. Returns a group id
   * for each vertex of the reference element. Vertices with the same id are
   * connected in the partition obtained by <code>getElements</code>. The
   * ids correspond to the ids generated by <code>getElementGroups</code>.
   *
   * \param vertex_count Number of vertices, same as length of <code>
   *                     vertex_values</code>.
   * \param key specifies the offset for the case table and must be
   *            generated from <code>getKey</code>.
   * \param vertex_groups where the resulting group indices are stored
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getVertexGroups(const sizeType vertex_count, const sizeType key,
                  std::vector<short>& vertex_groups) const {
    const short *vg_index = all_vertex_groups[vertex_count + dim]
                            + all_case_offsets[vertex_count+dim][key][INDEX_VERTEX_GROUPS];
    for (sizeType i = 0; i<vertex_count; ++i) {
      vertex_groups.push_back(*(vg_index++));
    }
  }

  /**
   * \brief returns connectivity information of the elements obtained by
   * <code>getElements</code>
   *
   * Result will be stored in <code>vertex_groups</code>. Returns a group id
   * for each element of the partition obtained by <code>getElements</code>.
   * Elements with the same id are connected. The ids correspond to the ids
   * generated by <code>getVertexGroups</code>.
   *
   * \param key specifies the offset for the case table and must be
   *            generated from <code>getKey</code>.
   * \param exterior_not_interior defines whether groups for interior or
   *                              exterior elements are generated
   * \param element_groups where the resulting group indices are stored
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getElementGroups(const sizeType vertex_count, const sizeType key,
                   const bool exterior_not_interior,
                   std::vector<short>& element_groups) const {
    const short * eg_index = all_element_groups[vertex_count + dim][int(exterior_not_interior)]
                             + all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_ELEMENT_GROUPS[int(exterior_not_interior)]];
    sizeType element_count = all_case_offsets
                             [vertex_count + dim][key][INDEX_COUNT_CODIM_0[int(exterior_not_interior)]];
    for (sizeType i = 0; i<element_count; ++i) {
      element_groups.push_back(*(eg_index++));
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
  template <typename valueVector>
  void MarchingCubes33<valueType, dim, thresholdFunctor>::
  getCoordsFromNumber(const valueVector& vertex_values,
                      const sizeType vertex_count, const short number,
                      point& coord) const
  {
    // it's a center point and we are in the cube case
    if (number == EZ && dim == 3 && vertex_count == 8)
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
      static short edges[] = {EI, EJ, EK, EL, EM, EN, EO, EP, EQ, ER, ES, ET};

      for (short e_index = 0; e_index<12; ++e_index)
      {
        int i = edges[e_index];
        vertex_1 = (i / FACTOR_FIRST_POINT) &
                   (VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP);
        vertex_2 = (i / FACTOR_SECOND_POINT) &
                   (VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP);
        if (thresholdFunctor::isInside(vertex_values[vertex_1]) !=
            thresholdFunctor::isInside(vertex_values[vertex_2]))
        {
          point edge_point;
          getCoordsFromNumber(vertex_values, vertex_count, i,
                              edge_point);
          for (sizeType j = 0; j < dim; j++)
          {
            coord[j] += edge_point[j];
          }
          count++;
        }
      }
      assert(count > 0);
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

      /* \TODO wrong indices for Simplex
       * Simplex is numbered (0, 1, 2, 4) to get the right reference
       * corners, ie to match the numbering of the cube. This leads to
       * wrong indices in vertex_values.
       */

      sizeType index_a = 0;
      sizeType index_b = 0;
      for (sizeType i = 0; i < dim; i++)
      {
        index_a += (sizeType) point_a[i] * (1<<i);
        index_b += (sizeType) point_b[i] * (1<<i);
      }
      index_a = all_vertex_to_index[vertex_count+dim][index_a];
      index_b = all_vertex_to_index[vertex_count+dim][index_b];
      // factor for interpolation
      valueType interpol_factor =
        thresholdFunctor::getDistance(vertex_values[index_a])
        / (thresholdFunctor::getDistance(vertex_values[index_b])
           - thresholdFunctor::getDistance(vertex_values[index_a]));
      // if we are at an egde with no intersecting, just take the
      // edge-center (occurs in codim 0 triangulation)
      if (thresholdFunctor::isInside(vertex_values[index_a]) ==
          thresholdFunctor::isInside(vertex_values[index_b]))
        interpol_factor = -0.5;
      // calculate interpolation point
      for (sizeType i = 0; i < dim; i++)
      {
        coord[i] = point_a[i] - interpol_factor * (point_b[i] - point_a[i]);
      }
    }
    // it's a vertex
    else
    {
      getCoordsFromEdgeNumber(vertex_values, vertex_count,
                              number, coord);
    }
    if (! std::isfinite(coord[0]))
      assert(false);
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
  template <typename valueVector>
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

  /** \brief Tests whether vertices are connected by the middle of the face.
   *
   * This test is needed to chose between ambiguous MC33 cases. It checks
   * whether two vertices are connected by the middle of the face or whether
   * they are separated. This method is implemented according to the paper
   * from Lewiner et al. It should be only applied on squares like 2D-cube
   * (rectangles) or faces of 3D-cubes.
   * parameter numbering is according to the dune-numbering scheme
   *
   * \param corner_a Value of the first face vertex.
   * \param corner_b Value of the second face vertex.
   * \param corner_c Value of the third face vertex.
   * \param corner_d Value of the forth face vertex.
   *
   * \return <code>True</code> if face center is not inside
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  bool MarchingCubes33<valueType, dim, thresholdFunctor>::
  testAmbiguousFace(const valueType corner_a, const valueType corner_b,
                    const valueType corner_c, const valueType corner_d, bool inverse) const
  {
    // Change naming scheme to jgt-paper ones
    ctype a = thresholdFunctor::getDistance(corner_a);
    ctype b = thresholdFunctor::getDistance(corner_b);
    ctype c = thresholdFunctor::getDistance(corner_d);
    ctype d = thresholdFunctor::getDistance(corner_c);

    // check if its really an amiguous face
    assert(a*c >= 0);
    assert(b*d >= 0);

    // should use 'a' according to lewiner paper (inverse is true if reference
    // vertex is not equal to zero
    //ctype f = inverse ? a : b;
    ctype f = a;

#ifndef NDEBUG
    std::cout << "testFace " << inverse << " => " << f*(a*c-b*d) << std::endl;
#endif

    bool result = !thresholdFunctor::isLower(f*(a*c-b*d));
    return result;
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
   *
   * \return <code>True</true> if cell center is connected to refCorner and the opposite corner.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  template <typename valueVector>
  bool MarchingCubes33<valueType, dim, thresholdFunctor>::
  testAmbiguousCenter(const valueVector& vertex_values,
                      const sizeType vertex_count, size_t refCorner) const
  {
    assert(dim==3);
#ifndef NDEBUG
    std::cout << "---------------------------\ntestAmbiguousCenter " << refCorner << std::endl;
#endif
    // permute vertices according to refCorner
    // rotate arounf z-axis such that refCorner is a0
    assert (refCorner < 4);
    static size_t permutation[4][8] = {
      {0, 1, 2, 3, 4, 5, 6, 7},
      {1, 3, 0, 2, 5, 7, 4, 6},
      {2, 0, 3, 1, 6, 4, 7, 5},
      {3, 2, 1, 0, 7, 6, 5, 4}
    };
    const ctype sign = thresholdFunctor::getDistance(vertex_values[permutation[refCorner][0]]) < 0 ? -1.0 : 1.0;
    // get vertex values
    const ctype a0 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][0]]);
    const ctype b0 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][2]]);
    const ctype c0 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][3]]);
    const ctype d0 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][1]]);
    const ctype a1 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][4]]);
    const ctype b1 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][6]]);
    const ctype c1 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][7]]);
    const ctype d1 = sign*thresholdFunctor::getDistance(vertex_values[permutation[refCorner][5]]);

#ifndef NDEBUG
    std::cout << vertex_values[0] << " ::: " << vertex_values[1] << " ::: "
              << vertex_values[2] << " ::: " << vertex_values[3] << " ::: "
              << vertex_values[4] << " ::: " << vertex_values[5] << " ::: "
              << vertex_values[6] << " ::: " << vertex_values[7] <<std::endl;
    std::cout << a0 << " ::: " << d0 << " ::: " << b0 << " ::: " << c0 << " ::: "
              << a1 << " ::: " << d1 << " ::: " << b1 << " ::: " << c1 << std::endl;
#endif

    // check that there is maximum
    const ctype a =  (a1 - a0) * (c1 - c0) - (b1 - b0) * (d1 - d0);
    if (a >= 0.0)
    {
#ifndef NDEBUG
      std::cout << "a >= 0 (" << a << ")\nresult: false" << std::endl;
#endif
      return false;
    }
    // check that the maximum-plane is inside the cube
    const ctype b =  c0*(a1 - a0) + a0*(c1 - c0) - d0*(b1 - b0) - b0*(d1 - d0);
    const ctype t_max = -0.5 * b / a;
    if ((0.0 >= t_max) || (1.0 <= t_max))
    {
#ifndef NDEBUG
      std::cout << "t_max not in [0,1]\nresult: false" << std::endl;
#endif
      return false;
    }
    // check that the
    const ctype at = a0 + (a1 - a0) * t_max;
    const ctype bt = b0 + (b1 - b0) * t_max;
    const ctype ct = c0 + (c1 - c0) * t_max;
    const ctype dt = d0 + (d1 - d0) * t_max;
    const bool inequation_4 = !thresholdFunctor::isLower(at*ct - bt*dt);
    // check sign(a0) = sign(at) = sign(ct) = sign(c1)
#ifndef NDEBUG
    const bool corner_signs_x = (at*ct >= 0)
                                && (bt*dt >= 0) && (at*bt >= 0);
#endif
    const bool corner_signs = (a0*ct >= 0) && (at*ct >= 0) && (ct*c1 >= 0);
    bool result = (inequation_4 && corner_signs);
#ifndef NDEBUG
    std::cout << "ineq " << inequation_4 << " ::: corner " << corner_signs
              << " ::: cornerX " << corner_signs_x << std::endl;
    std::cout << "result: " << (result ? "true" : "false") << std::endl;
    std::cout << "corners: " << at << " " << bt << " " << ct << " " << dt
              << std::endl;
#endif
    return result;
  }

} // end namespace Dune
