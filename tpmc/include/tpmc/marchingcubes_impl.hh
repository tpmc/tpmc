// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include <tpmc/marchinglut.hh>
#include <tpmc/referenceelements.hh>

#include <fstream>
#include <cmath>

#ifndef NDEBUG
#include <iostream> // FIXME TODO: Debug only, entferne mich!
#endif

namespace tpmc
{
  namespace {
    int vertexTableEntryToIndex(int entry)
    {
      return entry <= 0 ? -entry : (entry - 1) / 2 + VERTICES_ON_REFERENCE_COUNT;
    }
    int indexToVertexTableEntry(int index)
    {
      return index < VERTICES_ON_REFERENCE_COUNT? -index : 2*(index-VERTICES_ON_REFERENCE_COUNT) + 1;
    }
  }
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, class intersectionFunctor>
  template <typename InputIterator>
  typename MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                         intersectionFunctor>::size_type
  MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                intersectionFunctor>::getKey(InputIterator valuesBegin, InputIterator valuesEnd, bool use_mc_33) const
  {
    if ((dim < 0) || (dim > 3))
    {
      throw std::invalid_argument("Dimension must be 0, 1, 2 or 3");
    }
    else if (dim == 0)
    {
      return 0;
    }
    const size_type vertex_count = std::distance(valuesBegin, valuesEnd);
    const GeometryType geometry = makeGeometryType(dim, vertex_count);

    const unsigned short(*const table_case_offsets)[10]
        = Tables::all_case_offsets[vertex_count + dim];
    const short* const table_mc33_offsets = Tables::all_mc33_offsets[vertex_count + dim];
    const short* const table_mc33_face_test_order = Tables::all_face_tests[vertex_count + dim];

    // vector containing information if vertices are inside or not
    int case_number = 0;
    {
      int i = 0;
      for (InputIterator it = valuesBegin; it != valuesEnd; ++it, ++i)
      {
        case_number += (!threshFunctor.isInside(*it)) << i;
      }
    }
    // Is it a marching cubes' 33 case?
    bool ambiguous_case =
      (CASE_AMBIGUOUS_MC33 ==
       (CASE_AMBIGUOUS_MC33 & table_case_offsets[case_number][INDEX_UNIQUE_CASE]));
    // if it's not unique get the correct one
    if (use_mc_33 && ambiguous_case)
    {
      // find face tests for the case
      size_type test_index = (size_type) table_mc33_offsets[case_number];
      // offsets to have a binary tree like behavior
      size_type tree_offset = 1;
      // perform tests and find case number
      short test = table_mc33_face_test_order[test_index + tree_offset];

      valueType corner_a, corner_b, corner_c, corner_d;
#ifndef NDEBUG
      std::cout << "---- AMBIGUOUS:";
      {
        int count = 0;
        for (InputIterator it = valuesBegin; it != valuesEnd; ++it, ++count)
          std::cout << "v" << count << " = " << *it << "\n";
      }
      std::cout << std::endl;
#endif
      // tests are negative, non-negativ values are offsets
      while ((test < 0) && (test != -CASE_IS_REGULAR))
      {
        assert(test != TEST_INVALID);
#ifndef NDEBUG
        if (dim < 2 || dim > 3)
        {
          throw std::invalid_argument("MC 33 cases should occur with dimension 2 or 3");
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
          InputIterator ita = valuesBegin;
          std::advance(ita, getVertexOfFace<dim>(geometry, face, 0));
          corner_a = *ita;
          InputIterator itb = valuesBegin;
          std::advance(itb, getVertexOfFace<dim>(geometry, face, 1));
          corner_b = *itb;
          InputIterator itc = valuesBegin;
          std::advance(itc, getVertexOfFace<dim>(geometry, face, 2));
          corner_c = *itc;
          InputIterator itd = valuesBegin;
          std::advance(itd, getVertexOfFace<dim>(geometry, face, 3));
          corner_d = *itd;
#ifndef NDEBUG
          std::cout << "vertices " << corner_a << " "  << corner_b << " "  << corner_c << " "  << corner_d << "\n";
#endif
          bool inverse = (-test - TEST_FACE) & TEST_FACE_FLIP;
          test_result = testAmbiguousFace(corner_a, corner_b, corner_c, corner_d, inverse);
        }
        else if ((-test) & TEST_INTERIOR)
        {
          size_t refCorner = (-test - TEST_INTERIOR) >> 3;
          size_t refFace = (-test - TEST_INTERIOR) & 7;
          test_result = testAmbiguousCenter(valuesBegin, valuesEnd, refCorner, refFace);
        }
        else
        {
          throw std::invalid_argument("mc test must be either TEST_FACE or TEST_INTERIOR.");
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


  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  int MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                     IntersectionFunctor>::getMaximalVertexCount(GeometryType geometry) const
  {
    return Tables::all_complex_vertex_count[getCornerCount(dim,geometry) + dim];
  }

  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  template <typename InputIterator, typename OutputIterator>
  void MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                     IntersectionFunctor>::getVertices(InputIterator valuesBegin,
                                                       InputIterator valuesEnd, size_type key,
                                                       std::vector<int>& vertexToIndex,
                                                       OutputIterator out) const
  {
    const int NOTCOMPUTED = -1;

    const unsigned int vertex_count = std::distance(valuesBegin, valuesEnd);
    const unsigned int vertexArraySize = Tables::all_complex_vertex_count[vertex_count + dim]
                                         + VERTICES_ON_REFERENCE_COUNT;
    vertexToIndex.resize(vertexArraySize);
    std::fill(vertexToIndex.begin(), vertexToIndex.end(), NOTCOMPUTED);

    unsigned int nextOutIndex = 0;

    const int extint_and_codim[][2] = { { 0, 0 }, { 1, 0 }, { 0, 1 } };

    size_type element_count;
    const short* codim_index;

    // loop over exterior, interior and interface and collect vertices
    for (int ecIndex = 0; ecIndex < 3; ++ecIndex)
    {
      const int exterior_not_interior = extint_and_codim[ecIndex][0];
      const int codim_1_not_0 = extint_and_codim[ecIndex][1];

      // get pointer into codim table and element count
      if (codim_1_not_0)
      {
        element_count = Tables::all_case_offsets[vertex_count + dim][key][INDEX_COUNT_CODIM_1];
        codim_index = Tables::all_codim_1[vertex_count + dim]
                      + Tables::all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_1];
      }
      else
      {
        element_count
            = Tables::all_case_offsets[vertex_count
                                       + dim][key][INDEX_COUNT_CODIM_0[int(exterior_not_interior)]];
        codim_index = Tables::all_codim_0[vertex_count + dim][int(exterior_not_interior)]
                      + Tables::all_case_offsets[vertex_count + dim][key]
                                                [INDEX_OFFSET_CODIM_0[int(exterior_not_interior)]];
      }
      for (int elementIndex = 0; elementIndex < element_count; ++elementIndex)
      {
        const short currentVertexCount = *codim_index++;
        for (int j = 0; j < currentVertexCount; ++j)
        {
          const short current = *codim_index++;
          // check if it is not already computed
          const int vertex = vertexTableEntryToIndex(current);
          if (vertexToIndex[vertex] == NOTCOMPUTED)
          {
            // compute vertex and store result
            *out++ = getCoordsFromNumber(valuesBegin, valuesEnd, current);
            // remember index
            vertexToIndex[vertex] = nextOutIndex++;
          }
        }
      }
    }
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  template <typename OutputIterator>
  void MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                     IntersectionFunctor>::getElements(GeometryType geometry, size_type key,
                                                       TriangulationType type,
                                                       OutputIterator out) const
  {
    const unsigned int vertex_count = getCornerCount(dim, geometry);
    const bool exterior_not_interior = (type == TriangulationType::Exterior);
    const bool codim_1_not_0 = (type == TriangulationType::Interface);

    size_type element_count
        = Tables::all_case_offsets[vertex_count
                                   + dim][key][INDEX_COUNT_CODIM_0[int(exterior_not_interior)]];
    const short(*codim_index)
        = Tables::all_codim_0[vertex_count + dim][int(exterior_not_interior)]
          + Tables::all_case_offsets[vertex_count
                                     + dim][key][INDEX_OFFSET_CODIM_0[int(exterior_not_interior)]];
    if (codim_1_not_0)
    {
      element_count = Tables::all_case_offsets[vertex_count + dim][key][INDEX_COUNT_CODIM_1];
      codim_index = Tables::all_codim_1[vertex_count + dim]
                    + Tables::all_case_offsets[vertex_count + dim][key][INDEX_OFFSET_CODIM_1];
    }

    for (size_type i = 0; i < element_count; i++)
    {
      size_type point_count = *codim_index++;
      // Vector for storing the element points
      std::vector<int> element;
      element.reserve(point_count);
      for (size_type j = 0; j < point_count; j++)
      {
        const int current = *codim_index++;
        const int vertex = vertexTableEntryToIndex(current);
        // check if its a reference vertex or not
        element.push_back(vertex);
      }
      *out++ = element;
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  template <typename OutputIterator>
  void MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                     IntersectionFunctor>::getVertexGroups(GeometryType geometry, size_type key,
                                                           OutputIterator out) const
  {
    const unsigned int vertex_count = getCornerCount(dim,geometry);

    const short* vg_index
        = Tables::all_vertex_groups[vertex_count + dim]
          + Tables::all_case_offsets[vertex_count + dim][key][INDEX_VERTEX_GROUPS];

    std::copy(vg_index, vg_index + vertex_count, out);
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  template <typename OutputIterator>
  void MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                     IntersectionFunctor>::getElementGroups(GeometryType geometry, size_type key,
                                                            TriangulationType type,
                                                            OutputIterator out) const
  {
    const bool exterior_not_interior = (type == TriangulationType::Exterior);
    const unsigned int vertex_count = getCornerCount(dim,geometry);

    const short* eg_index
        = Tables::all_element_groups[vertex_count + dim][int(exterior_not_interior)]
          + Tables::all_case_offsets[vertex_count + dim][key]
                                    [INDEX_OFFSET_ELEMENT_GROUPS[int(exterior_not_interior)]];
    size_type element_count
        = Tables::all_case_offsets[vertex_count
                                   + dim][key][INDEX_COUNT_CODIM_0[int(exterior_not_interior)]];

    std::copy(eg_index, eg_index + element_count, out);
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  template <typename InputIterator>
  Coordinate MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                           IntersectionFunctor>::getCoordsFromNumber(InputIterator valuesBegin,
                                                                     InputIterator valuesEnd,
                                                                     short number_) const
  {
    short number = number_;
    // get position in the vertex table
    // std::cout << "getting coords for number " << number << "\n";
    if (number <= 0)
    { // we have a single point
      number *= -1;

      if (number >= FA && number <= FF) {
        short faceid = number - FA;
        return getCoordsFromFaceId(valuesBegin, valuesEnd, faceid);
      } else if (number >= CA && number <= CF) {
        short faceid = number - CA;
        return getCoordsFromCenterId(valuesBegin, valuesEnd, faceid);
      } else if (number >= RA && number <= RF) {
        short faceid = number - RA;
        return getCoordsFromRootId(valuesBegin, valuesEnd, faceid);
      }
      else {
        return getCoordsFromEdgeNumber(valuesBegin, valuesEnd, number);
      }
    } else {     // we have an egde
      const unsigned int vertex_count = std::distance(valuesBegin, valuesEnd);
      const short(*vertex_index) = Tables::all_case_vertices[vertex_count + dim] + number;
      Coordinate point_a = getCoordsFromNumber(valuesBegin, valuesEnd, vertex_index[0]);
      Coordinate point_b = getCoordsFromNumber(valuesBegin, valuesEnd, vertex_index[1]);
      if (vertex_index[0] <= 0 && vertex_index[1] <= 0 && -vertex_index[0] >= VA
          && -vertex_index[0] <= VH && -vertex_index[1] >= VA && -vertex_index[1] <= VH)
      { // we have a simple edge
        size_type index_a = Tables::all_vertex_to_index[vertex_count + dim][-vertex_index[0]];
        size_type index_b = Tables::all_vertex_to_index[vertex_count + dim][-vertex_index[1]];
        InputIterator value_a = valuesBegin;
        std::advance(value_a, index_a);
        InputIterator value_b = valuesBegin;
        std::advance(value_b, index_b);
        // if theres no intersection along the edge, we use the middle as a
        // helper vertex. otherwise, use linear interpolation
        valueType interpol_factor = -0.5;
        if (threshFunctor.isInside(*value_a) != threshFunctor.isInside(*value_b))
        {
          // factor for interpolation
          interpol_factor = threshFunctor.interpolationFactor(point_a, point_b, *value_a, *value_b);
        }
        // calculate interpolation point
        Coordinate result;
        for (size_type i = 0; i < dim; i++)
        {
          result[i] = point_a[i] - interpol_factor * (point_b[i] - point_a[i]);
        }
        return result;
      } else {
#ifndef NDEBUG
        std::cout << "#####!!non-simple edge " << number << " = "
                  << " (" << vertex_index[0] << ", " << vertex_index[1] << ")\n";
#endif
        return IntersectionFunctor::template findRoot<dim>(valuesBegin, valuesEnd, point_a,
                                                           point_b);
      }
    }
    // an invalid number has been provided since we are still in the method
    // indicates an error in the lut
    assert(false);
  }

  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  template <typename InputIterator>
  Coordinate MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                           IntersectionFunctor>::getCoordsFromCenterId(InputIterator valuesBegin,
                                                                       InputIterator valuesEnd,
                                                                       short centerid) const
  {
    const unsigned int vertex_count = std::distance(valuesBegin, valuesEnd);
    // CenterPoints only supported in 3d cubes
    assert(dim == 3 && vertex_count == 8);
    static unsigned short permutations[][8] = {{0,4,1,5,2,6,3,7}, {0,1,4,5,2,3,6,7}, {0,1,2,3,4,5,6,7}};
    // x dir, y dir, z dir
    static unsigned short coordPerm[][3] = {{1,2,0}, {0,2,1}, {0,1,2}};
    unsigned short * currentPermutation = permutations[centerid/2];
    unsigned short * currentCoordPerm = coordPerm[centerid/2];
    double v[vertex_count];
    for (; valuesBegin != valuesEnd; ++valuesBegin)
    {
      v[*currentPermutation++] = *valuesBegin;
    }
    double edges[] = {v[4]-v[0], v[5]-v[1], v[6]-v[2], v[7]-v[3]};
    double A = edges[3]*v[0]+edges[0]*v[3]-edges[2]*v[1]-edges[1]*v[2];
    double B = edges[1]*v[6]+edges[2]*v[5]-edges[0]*v[7]-edges[3]*v[4];
    double denom = (v[0]-v[1]-v[2]+v[3])*B+(v[4]-v[5]-v[6]+v[7])*A;
    Coordinate result;
    result[currentCoordPerm[0]] = (B * (v[0] - v[2]) + A * (v[4] - v[6])) / denom;
    result[currentCoordPerm[1]] = (B * (v[0] - v[1]) + A * (v[4] - v[5])) / denom;
    result[currentCoordPerm[2]] = A / (A + B);
    return result;
  }

  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, typename IntersectionFunctor>
  template <typename InputIterator>
  Coordinate MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                           IntersectionFunctor>::getCoordsFromRootId(InputIterator valuesBegin,
                                                                     InputIterator valuesEnd,
                                                                     short faceid) const
  {
    const unsigned int vertex_count = std::distance(valuesBegin, valuesEnd);
    assert(dim == 3 && vertex_count == 8);
    static unsigned short permutations[][8] = {{0,4,1,5,2,6,3,7}, {4,0,5,1,6,2,7,3}, {0,1,4,5,2,3,6,7},
                                               {4,5,0,1,6,7,2,3}, {0,1,2,3,4,5,6,7}, {4,5,6,7,0,1,2,3}};
    // x dir, y dir, z dir
    static unsigned short coordPerm[][3] = {{1,2,0}, {0,2,1}, {0,1,2}};
    unsigned short * currentPermutation = permutations[faceid];
    unsigned short * currentCoordPerm = coordPerm[faceid/2];
    double v[vertex_count];
    for (; valuesBegin != valuesEnd; ++valuesBegin)
    {
      v[*currentPermutation++] = *valuesBegin;
    }
    double edges[] = {v[4]-v[0], v[5]-v[1], v[6]-v[2], v[7]-v[3]};
    double A = edges[0]*edges[3]-edges[1]*edges[2];
    double B = edges[3]*v[0]+edges[0]*v[3]-edges[2]*v[1]-edges[1]*v[2];
    double C = edges[1]*v[6]+edges[2]*v[5]-edges[0]*v[7]-edges[3]*v[4];
    double D = v[0]*v[3]-v[1]*v[2];
    double E = -std::sqrt(-4*A*D+B*B);
    Coordinate result;
    if (FloatCmp::eq(A,0.0)) {
      double root = -D/B;
      double denom = -(edges[0]-edges[1]-edges[2]+edges[3])*D+(v[0]-v[1]-v[2]+v[3])*B;
      result[currentCoordPerm[0]] = ((edges[2] - edges[0]) * D + (v[0] - v[2]) * B) / denom;
      result[currentCoordPerm[1]] = ((edges[1] - edges[0]) * D + (v[0] - v[1]) * B) / denom;
      result[currentCoordPerm[2]] = faceid % 2 == 0 ? root : 1.0 - root;
    } else {
      double root0 = 0.5*(-E-B)/A;
      double root1 = 0.5*(E-B)/A;
      const bool root0_invalid = FloatCmp::lt(root0,0.0) || FloatCmp::gt(root0,1.0);
      const bool root1_invalid = FloatCmp::lt(root1,0.0) || FloatCmp::gt(root1,1.0);
      if (root0_invalid || (!root1_invalid && root1 < root0)) {
        E *= -1;
        result[currentCoordPerm[2]] = faceid%2==0 ? root1 : 1.0-root1;
      } else {
        result[currentCoordPerm[2]] = faceid%2==0 ? root0 : 1.0-root0;
      }
      const double denom = -(edges[0]-edges[1]-edges[2]+edges[3])*E-(v[4]-v[5]-v[6]+v[7])*B-(v[0]-v[1]-v[2]+v[3])*C;
      result[currentCoordPerm[0]] = (-(edges[0]-edges[2])*E-(v[4]-v[6])*B-(v[0]-v[2])*C)/denom;
      result[currentCoordPerm[1]] = (-(edges[0]-edges[1])*E-(v[4]-v[5])*B-(v[0]-v[1])*C)/denom;
    }
    return result;
  }

  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, class IntersectionFunctor>
  template <typename InputIterator>
  Coordinate MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                           IntersectionFunctor>::getCoordsFromFaceId(InputIterator valuesBegin,
                                                                     InputIterator valuesEnd,
                                                                     short faceid) const
  {
    // FacePoints only supported in 3d
    assert(dim == 3);
    const int vertex_count = std::distance(valuesBegin, valuesEnd);
    static short cube_faceoffsets[] = {0,4,8,12,16,20,24};
    static short cube_faces[] = {0,2,4,6,1,3,5,7,0,1,4,5,2,3,6,7,0,1,2,3,4,
                                 5,6,7};
    static short pyramid_faceoffsets[] = {0,4,7,10,13,16};
    static short pyramid_faces[] = {0,1,2,3,0,2,4,1,3,4,0,1,4,2,3,4};
    static short prism_faceoffsets[] = {0,4,8,12,15,18};
    static short prism_faces[] = {0,1,3,4,0,2,3,5,1,2,4,5,0,1,2,3,4,5};
    static short simplex_faceoffsets[] = {0,3,6,9,12};
    static short simplex_faces[] = {0,1,2,0,1,3,0,2,3,1,2,3};
    static short* all_faceoffsets[] = {NULL, NULL, NULL, NULL,
                                       simplex_faceoffsets,
                                       pyramid_faceoffsets,
                                       prism_faceoffsets, NULL,
                                       cube_faceoffsets};
    static short* all_faces[] = {NULL, NULL, NULL, NULL, simplex_faces,
                                 pyramid_faces, prism_faces, NULL,
                                 cube_faces};
    short* faceoffsets = all_faceoffsets[vertex_count];
    short* faces = all_faces[vertex_count];
    if (faceoffsets == NULL || faces == NULL) {
      throw std::invalid_argument("Face Center only supported for cubes, prisms, pyramids or simplices");
    }
    short count = faceoffsets[faceid+1]-faceoffsets[faceid];
    if (count == 3) {
      short a = faces[faceoffsets[faceid]];
      short b = faces[faceoffsets[faceid]+1];
      short c = faces[faceoffsets[faceid]+2];
      return getCoordsFromTriangularFace(valuesBegin, valuesEnd, a, b, c, faceid);
    } else if (count == 4) {
      short a = faces[faceoffsets[faceid]];
      short b = faces[faceoffsets[faceid]+1];
      short c = faces[faceoffsets[faceid]+2];
      short d = faces[faceoffsets[faceid]+3];
      return getCoordsFromRectangularFace(valuesBegin, valuesEnd, a, b, c, d, faceid);
    } else {
      throw std::invalid_argument("Face Center only supported for triangular or rectangular faces");
    }
  }

  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, class IntersectionFunctor>
  template <typename InputIterator>
  Coordinate
  MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                IntersectionFunctor>::getCoordsFromRectangularFace(InputIterator valuesBegin,
                                                                   InputIterator valuesEnd, short a,
                                                                   short b, short c, short d,
                                                                   short faceid) const
  {
    const int vertex_count = std::distance(valuesBegin, valuesEnd);
    // map prism and simplex indices to cube (i.e. skip vertex 3)
    if (vertex_count == 4 || vertex_count == 6) {
      if (a > 2) ++a;
      if (b > 2) ++b;
      if (c > 2) ++c;
      if (d > 2) ++d;
    }
    Coordinate pa = getCoordsFromEdgeNumber(valuesBegin, valuesEnd, a);
    Coordinate pb = getCoordsFromEdgeNumber(valuesBegin, valuesEnd, b);
    Coordinate pc = getCoordsFromEdgeNumber(valuesBegin, valuesEnd, c);
    Coordinate pd = getCoordsFromEdgeNumber(valuesBegin, valuesEnd, d);

    InputIterator ia = valuesBegin;
    std::advance(ia, a);
    valueType va = *ia;
    InputIterator ib = valuesBegin;
    std::advance(ib, b);
    valueType vb = *ib;
    InputIterator ic = valuesBegin;
    std::advance(ic, c);
    valueType vc = *ic;
    InputIterator id = valuesBegin;
    std::advance(id, d);
    valueType vd = *id;
#ifndef NDEBUG
    std::cout << "getting coords for rectangular face:\n";
    std::cout << "pa = " << pa << " va = " << va << "\n";
    std::cout << "pb = " << pb << " vb = " << vb << "\n";
    std::cout << "pc = " << pc << " vc = " << vc << "\n";
    std::cout << "pd = " << pd << " vd = " << vd << "\n";
#endif
    valueType cx = 0.5, cy = 0.5;
    if (FloatCmp::ge(va*vd,0.0) && FloatCmp::ge(vb*vc,0.0) && FloatCmp::lt(va*vb,0.0)) {
      valueType factor = 1.0/(va-vb-vc+vd);
      cx = factor*(va-vc);
      cy = factor*(va-vb);
    } else if (FloatCmp::ge(va*vb,0.0) && FloatCmp::ge(vc*vd,0.0) && FloatCmp::lt(va*vc,0.0)) {
      cy = (va+vb)/(va+vb-vc-vd);
    } else if (FloatCmp::ge(va*vc,0.0) && FloatCmp::ge(vb*vd,0.0) && FloatCmp::lt(va*vb,0.0)) {
      cx = (va+vc)/(va-vb+vc-vd);
    }
#ifndef NDEBUG
    std::cout << "local coordinates of center: " << cx << ", " << cy << "\n";
#endif
    pa *= (1-cx)*(1-cy);
    pb *= cx*(1-cy);
    pc *= (1-cx)*cy;
    pd *= cx*cy;
    pa += pb;
    pa += pc;
    pa += pd;
#ifndef NDEBUG
    std::cout << "result = " << pa << "\n";
    std::cout << "value at center : " << (1-cx)*(1-cy)*va+cx*(1-cy)*vb+(1-cx)*cy*vc+cx*cy*vd << "\n";
#endif
    return pa;
  }

  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, class IntersectionFunctor>
  template <typename InputIterator>
  Coordinate
  MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                IntersectionFunctor>::getCoordsFromTriangularFace(InputIterator valuesBegin,
                                                                  InputIterator valuesEnd, short a,
                                                                  short b, short c, short faceid)
      const
  {
    short ind[] = {a,b,c};
    InputIterator ita = valuesBegin;
    std::advance(ita, a);
    valueType va = *ita;
    InputIterator itb = valuesBegin;
    std::advance(itb, b);
    valueType vb = *itb;
    InputIterator itc = valuesBegin;
    std::advance(itc, c);
    valueType vc = *itc;
    bool ia = threshFunctor.isInside(va);
    bool ib = threshFunctor.isInside(vb);
    bool ic = threshFunctor.isInside(vc);
    int key = ia+2*ib+4*ic;
    if (key == 0 || key == 7) {
      throw std::invalid_argument("Face Center on triangular face not supported for plain faces");
    }
    // permute vertices so that (sign(v0) != sign(v1)) && (sign(v1) == sign(v2))
    static short perm[][3] = {{0,1,2},{1,2,0},{2,0,1},{2,0,1},{1,2,0},{0,1,2}};
    short* lperm = perm[key-1];
    short nind[] = {ind[lperm[0]], ind[lperm[1]], ind[lperm[2]]};
    short k01 = std::min(nind[0],nind[1])*FACTOR_FIRST_POINT+std::max(nind[0],nind[1])*FACTOR_SECOND_POINT;
    short k02 = std::min(nind[0],nind[2])*FACTOR_FIRST_POINT+std::max(nind[0],nind[2])*FACTOR_SECOND_POINT;
    Coordinate result = getCoordsFromNumber(valuesBegin, valuesEnd, k01);
    result += getCoordsFromNumber(valuesBegin, valuesEnd, k02);
    result += getCoordsFromNumber(valuesBegin, valuesEnd, nind[1]);
    result += getCoordsFromNumber(valuesBegin, valuesEnd, nind[2]);
    result *= 0.25;
    return result;
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, class intersectionFunctor>
  template <typename InputIterator>
  Coordinate MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                           intersectionFunctor>::getCoordsFromEdgeNumber(InputIterator valuesBegin,
                                                                         InputIterator valuesEnd,
                                                                         char number) const
  {
    number /= FACTOR_FIRST_POINT;
    Coordinate result;
    // Get coordinate for each dimension. It is either 0 or 1.
    for (size_type d = 0; d < dim; d++)
    {
      result[d] = number & (1 << d) ? ctype(1.0) : ctype(0.0);
    }
    return result;
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, class intersectionFunctor>
  bool MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                     intersectionFunctor>::testAmbiguousFace(const valueType corner_a,
                                                             const valueType corner_b,
                                                             const valueType corner_c,
                                                             const valueType corner_d, bool inverse)
      const
  {
    // Change naming scheme to jgt-paper ones
    ctype a = threshFunctor.getDistance(corner_a);
    ctype b = threshFunctor.getDistance(corner_b);
    ctype c = threshFunctor.getDistance(corner_d);
    ctype d = threshFunctor.getDistance(corner_c);

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

    bool result = !threshFunctor.isLower(f*(a*c-b*d));
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
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType, class intersectionFunctor>
  template <typename InputIterator>
  bool MarchingCubes<valueType, dim, Coordinate, thresholdFunctor, symmetryType,
                     intersectionFunctor>::testAmbiguousCenter(InputIterator valuesBegin,
                                                               InputIterator valuesEnd,
                                                               size_t refCorner, size_t refFace)
      const
  {
    assert(dim==3);
#ifndef NDEBUG
    std::cout << "---------------------------\ntestAmbiguousCenter " << refCorner << "_" << refFace << std::endl;
#endif
    // \TODO need to find proper axis and rotate accordingly

    // permute vertices according to refCorner
    // rotate arounf z-axis such that refCorner is a0
    assert (refCorner < 4);
    assert (refFace == 0 || refFace == 2 || refFace == 4);
    refFace /= 2;
    static size_t permutation[4][8] = {
      {0, 1, 2, 3, 4, 5, 6, 7},
      {2, 0, 3, 1, 6, 4, 7, 5},
      {1, 3, 0, 2, 5, 7, 4, 6},
      {3, 2, 1, 0, 7, 6, 5, 4}
    };
    static size_t face_permutation[3][8] = {
      {0, 4, 2, 6, 1, 5, 3, 7},
      {0, 1, 4, 5, 2, 3, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7}
    };
    static size_t face_ref_perm[3][4] = {
      {0, 3, 2, 1},
      {0, 1, 3, 2},
      {0, 1, 2, 3}
    };
    // permute reference Corner
    refCorner = face_ref_perm[refFace][refCorner];
    size_t *p = permutation[refCorner];
    size_t *fp = face_permutation[refFace];

#ifndef NDEBUG
    for (InputIterator it = valuesBegin; it != valuesEnd; ++it)
      std::cout << (it == valuesBegin ? "" : " ::: ") << *it;
    std::cout << std::endl;
#endif

    const int vertex_count = std::distance(valuesBegin, valuesEnd);
    double v[vertex_count];
    const ctype sign = threshFunctor.isInside(*valuesBegin) ? -1.0 : 1.0;
    for (; valuesBegin != valuesEnd; ++valuesBegin, ++fp)
    {
      v[p[*fp]] = sign * threshFunctor.getDistance(*valuesBegin);
    }

#ifndef NDEBUG
    for (int i = 0; i < vertex_count; ++i)
      std::cout << (i == 0 ? "" : " ::: ") << v[i];
    std::cout << std::endl;
#endif

    // check that there is maximum
    const ctype a = (v[4] - v[0]) * (v[7] - v[3]) - (v[6] - v[2]) * (v[5] - v[1]);
#ifndef NDEBUG
    std::cout << "a = " << a << "\n";
#endif
    if (a >= 0.0)
    {
#ifndef NDEBUG
      std::cout << "a >= 0 (" << a << ")\nresult: false" << std::endl;
#endif
      return false;
    }
    // check that the maximum-plane is inside the cube
    const ctype b = v[3] * (v[4] - v[0]) + v[0] * (v[7] - v[3]) - v[1] * (v[6] - v[2])
                    - v[2] * (v[5] - v[1]);
#ifndef NDEBUG
    std::cout << "b = " << b << "\n";
#endif
    const ctype t_max = -0.5 * b / a;
#ifndef NDEBUG
    std::cout << "t_max = " << t_max << "\n";
#endif
    if ((0.0 >= t_max) || (1.0 <= t_max))
    {
#ifndef NDEBUG
      std::cout << "t_max not in [0,1]\nresult: false" << std::endl;
#endif
      return false;
    }
    // check that the
    const ctype at = v[0] + (v[4] - v[0]) * t_max;
    const ctype bt = v[2] + (v[6] - v[2]) * t_max;
    const ctype ct = v[3] + (v[7] - v[3]) * t_max;
    const ctype dt = v[1] + (v[5] - v[1]) * t_max;
    const bool inequation_4 = !threshFunctor.isLower(at*ct - bt*dt);
    // check sign(v[0]) = sign(at) = sign(ct) = sign(v[7])
#ifndef NDEBUG
    const bool corner_signs_x = (at*ct >= 0)
                                && (bt*dt >= 0) && (at*bt >= 0);
#endif
    const bool corner_signs = (v[0] * at >= 0) && (at * ct >= 0) && (ct * v[7] >= 0);
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

} // end namespace tpmc
