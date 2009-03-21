// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include <iostream> // FIXME: Debug only, enferne mich!

namespace Dune {

  /*
   * Calculate key to access cube2d_cases_offsets.
   * Return value indicates a mc33 case.
   *
   * \return True if the case is in the regular table, false if it's a MC33-only case.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  typename MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::sizeType
  MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::
  getKey(const valueVector& vertexValues, const sizeType vertex_count,
         const bool useMc33)
  {
    short (* table_cases_offsets)[5] = NULL;
    short * table_mc33_offsets = NULL;
    short * table_mc33_face_test_order = NULL;
    // 2D shapes
    if (dim == 2)
    {
      // simplex 2D
      if (vertex_count == 3)
      {
        table_cases_offsets = table_simplex2d_cases_offsets;
      }
      // cube 2D
      else if (vertex_count == 4)
      {
        table_cases_offsets = table_cube2d_cases_offsets;
        table_mc33_offsets = table_cube2d_mc33_offsets;
        table_mc33_face_test_order = table_cube2d_mc33_face_test_order;
      }
    }
    // 3D
    else if (dim == 3)
    {
      // simplex 3D
      if (vertex_count == 4)
      {
        table_cases_offsets = table_simplex3d_cases_offsets;
      }
      // cube 3D
      else if (vertex_count == 8)
      {
        table_cases_offsets = table_cube3d_cases_offsets;
        table_mc33_offsets = table_cube3d_mc33_offsets;
        table_mc33_face_test_order = table_cube3d_mc33_face_test_order;
      }
    }

    // vector containing information if vertices are inside or not
    bool *vertexInside = new bool[vertex_count];
    int caseNumber = 0;
    for (sizeType i = 0; i < vertex_count; i++)
    {
      // Shift left
      caseNumber *= 2;
      // Set bit to 0 if vertex is inside
      vertexInside[i] = 1 - thresholdFunctor::isInside(vertexValues[i]);
      caseNumber += (int) vertexInside[i];
    }

    // Is it a marching cubes' 33 case?
    bool isAmiguousMc33case = (CASE_AMIGUOUS_MC33 ==
                               table_cases_offsets[caseNumber][4] & CASE_AMIGUOUS_MC33);
    // if it's not unique get the right one
    if (useMc33 && isAmiguousMc33case)
    {
      // find face tests for the case
      sizeType testIndex = (sizeType) table_mc33_offsets[caseNumber];
      // offsets to have a binary tree like behavior
      sizeType treeOffset = 1;

      // perform tests and find case number
      short faceNumber = table_mc33_face_test_order[testIndex + treeOffset];
      bool notInverted = (CASE_INVERTED == CASE_INVERTED &
                          table_cases_offsets[caseNumber][(sizeType) INDEX_UNIQUE_CASE]);

      /*GeometryType geometryType;
         geometryType.makeQuadrilateral();
         ReferenceElementContainer<ctype, dim> container;
         const ReferenceElement<ctype, dim> & re = container(geometryType);*/
      // test are never positive, positive values are offsets
      while ((faceNumber <= 0) && (faceNumber != CASE_IS_REGULAR))
      {
        /* TODO: verallgemeinerten Code benutzen für Würfel
           valueType cornerA = vertexValues[re.subEntity(faceNumber, 1, 0, dim)];
           valueType cornerB = vertexValues[re.subEntity(faceNumber, 1, 2, dim)];
           valueType cornerC = vertexValues[re.subEntity(faceNumber, 1, 3, dim)];
           valueType cornerD = vertexValues[re.subEntity(faceNumber, 1, 4, dim)];
         */
        valueType cornerA = vertexValues[0];
        valueType cornerB = vertexValues[1];
        valueType cornerC = vertexValues[2];
        valueType cornerD = vertexValues[3];
        // test face
        bool faceIsSurface = testFaceIsSurface(cornerA, cornerB, cornerC, cornerD, notInverted);
        // calculate index position (if test is true: 2*index, otherwise: 2*index+1)
        treeOffset *= 2;
        treeOffset += (1 - faceIsSurface);
        faceNumber = table_mc33_face_test_order[testIndex + treeOffset];
      }
      if (faceNumber != CASE_IS_REGULAR)
      {
        caseNumber = faceNumber;
      }
    }
    return caseNumber;
  }

  /*
   * Marching cubes' algorithm.
   * vertex_values: pointer to an array containing vertices' values
   * vertex_count: count of vertices (array length)
   * threshold: value of the isosurface
   * smaller_inside: whether smaller values are inside the isosurface
   *
   * TODO: Datentyp, Dimension und Referenzelement (Würfel, Dreieck usw) als Templates einführen
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::
  getElements(const valueVector& vertexValues,
              const sizeType vertexCount, const sizeType key,
              std::vector<std::vector<point> >& elements,
              const bool codim1InstedCodim0)
  {
    const short * offsets = table_cube2d_cases_offsets[key];
    // Pointer to first element
    const short * index = table_cube2d_codim_0 + (int) offsets[INDEX_OFFSET_CODIM_0];
    // Element count
    sizeType caseCountElements = offsets[INDEX_COUNT_CODIM_0];

    if (codim1InstedCodim0)
    {
      index = table_cube2d_codim_1 + (int) offsets[INDEX_OFFSET_CODIM_1];
      caseCountElements = offsets[INDEX_COUNT_CODIM_1];
    }
    elements.resize(caseCountElements);
    // printf("Anzahl Elemente: %d \n", (int)caseCountElements);
    for (sizeType i = 0; i < caseCountElements; i++)
    {
      sizeType numberOfPoints = (sizeType) index[0];
      // Vector for storing the element points
      elements[i].resize(numberOfPoints);
      //printf(" Debug vectorsize: %d %d\n", (int)numberOfPoints, (int)offsets[INDEX_OFFSET_CODIM_1]);
      // Read points from table and store them
      for (sizeType j = 0; j < numberOfPoints; j++)
      {
        getCoordsFromNumber(vertexValues, vertexCount, index[j+1], elements[i][j]);
        //printf("   Loop debug output: j %d / vertex number %d / results: %1.1f %1.1f\n", (int)j, (int)index[j+1], elements[i][j][0], elements[i][j][1]);
      }
      // increase index for pointing to the next element
      index += numberOfPoints + 1;
    }
  }

  /*
   * TODO: Kommentar schreiben
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  typename MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::sizeType
  MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::
  getMc33case(const valueVector& vertexValues,
              const sizeType vertexCount, char number) const
  {
    return (sizeType) 0;
  }

  /**
   * \brief Generates the coordinate for a point which is specified
   * by its vertex or edge number.
   *
   * Result will be stored to \param coords.
   *
   * TODO: Code geht nur für Würfel, Quadrate und Linien, nicht aber für Dreiecke. Als Template implementieren
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::
  getCoordsFromNumber(const valueVector& vertexValues,
                      const sizeType vertexCount, char number,
                      point& coords) const
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
      point pointA, pointB;
      getCoordsFromEdgeNumber(vertexValues,
                              vertexCount, number, pointA);
      getCoordsFromEdgeNumber(vertexValues,
                              vertexCount, (number / FACTOR_SECOND_POINT * FACTOR_FIRST_POINT), pointB);
      // get indices for point in valueVector
      sizeType indexA = 0;
      sizeType indexB = 0;
      for (sizeType i = 0; i < dim; i++)
      {
        indexA += (sizeType) pointA[i] * (1<<i);
        indexB += (sizeType) pointB[i] * (1<<i);
      }
      // factor for interpolation
      valueType interpolFactor = thresholdFunctor::getDistance(vertexValues[indexA])
                                 / (thresholdFunctor::getDistance(vertexValues[indexB])
                                    - thresholdFunctor::getDistance(vertexValues[indexA]));
      //printf("     Kante: coords %1.3f %1.3f davor indexA %d  indexB %d // %d %d\n", coords[0], coords[1], indexA, indexB, NO_VERTEX^number, number);
      // calculate interpolation point
      for (sizeType i = 0; i < dim; i++)
      {
        coords[i] = pointA[i] - interpolFactor * (pointB[i] - pointA[i]);
      }
      //   printf("     Kante: coords %1.3f %1.3f / A` %1.3f B` %1.3f \n", coords[0], coords[1], thresholdFunctor::getDistance(vertexValues[indexA]), thresholdFunctor::getDistance(vertexValues[indexB]));

    }
    // it's a vertex
    else
    {
      getCoordsFromEdgeNumber(vertexValues,
                              vertexCount, number, coords);
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
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::
  getCoordsFromEdgeNumber(const valueVector& vertexValues,
                          const sizeType vertexCount, char number,
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
  bool MarchingCubesAlgorithm<valueType, dim, thresholdFunctor>::
  testFaceIsSurface(const valueType cornerA, const valueType cornerB,
                    const valueType cornerC, const valueType cornerD,
                    const bool notInverted) const
  {
    // Change naming scheme to jgt-paper ones
    double a = thresholdFunctor::getDistance(cornerA);
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
} // end namespace Dune
