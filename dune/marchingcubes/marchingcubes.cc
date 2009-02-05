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
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  bool MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  getOffsets(const valueVector& vertexValues, const sizeType vertexCount,
             const bool useMc33, char * offsets)
  {
    // vector containing information if vertices are inside or not
    bool *vertexInside = new bool[vertexCount];
    int caseNumber = 0;
    for (sizeType i = 0; i < vertexCount; i++)
    {
      // Shift left
      caseNumber *= 2;
      // Set bit to 0 if vertex is inside
      vertexInside[i] = 1 - thresholdFunctor::isInside(vertexValues[i]);
      caseNumber += (int) vertexInside[i];
    }

    // Is it a marching cubes' 33 case?
    bool isUniqueMc33case =
      (table_cube2d_cases_offsets[caseNumber][4] == UNIQUE_MC33_CASE);
    // if it's not unique get the rigth one
    if ( !isUniqueMc33case)
    {
      // find face tests for the case
      sizeType testIndex = table_cube2d_mc33_offsets[
        (sizeType) table_cube2d_cases_offsets[caseNumber][(sizeType) INDEX_UNIQUE_CASE]] - 1;
      // offsets to have a binary tree like behavour
      sizeType treeOffset = 1;

      // perform tests and find case number
      int faceNumber = table_cube2d_mc33_face_test_order[testIndex + treeOffset];
      bool notInverted = (table_cube2d_mc33_offsets[
                            (sizeType) table_cube2d_cases_offsets[caseNumber][(sizeType) INDEX_UNIQUE_CASE] + 1] == 1);

      /*GeometryType geometryType;
         geometryType.makeQuadrilateral();
         ReferenceElementContainer<ctype, dim> container;
         const ReferenceElement<ctype, dim> & re = container(geometryType);*/
      // test are never positiv, positiv values are offsets
      while (faceNumber <= 0)
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
        treeOffset += (1 -faceIsSurface);
        faceNumber = table_cube2d_mc33_face_test_order[testIndex + treeOffset];
      }
      caseNumber = faceNumber;
    }

    // store result
    offsets[0] = table_cube2d_cases_offsets[caseNumber][0];
    offsets[1] = table_cube2d_cases_offsets[caseNumber][1];
    offsets[2] = table_cube2d_cases_offsets[caseNumber][2];
    offsets[3] = table_cube2d_cases_offsets[caseNumber][3];

    printf("<Debug output> case number %d (row index if mc 33 case) \n", caseNumber);
    return isUniqueMc33case;
  }

  /*
   * Marching cubes' algorithm.
   * vertex_values: pointer to an array containing vertices' values
   * vertex_count: count of vertices (array length)
   * threshold: value of the isosurface
   * smaller_inside: whether smaller values are inside the isosurface
   *
   * TODO: Datentyp, Dimension und Referenzelement (Würfel, Dreieck usw) als Templates einführen
   * TODO: Template-Parameter für codim 0 und codim1?
   */
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  getElements(const valueVector& vertexValues,
              const sizeType vertexCount, const char * offsets,
              std::vector<std::vector<point> >& codim0)
  {
    // get elements for co-dimension 0

    // Pointer to first element
    const char * index = table_cube2d_codim_1 + (int) offsets[INDEX_OFFSET_CODIM_1];
    // Element count
    sizeType caseCountElements = offsets[INDEX_COUNT_CODIM_1];
    codim0.resize(caseCountElements);
    for (sizeType i = 0; i < caseCountElements; i++)
    {
      sizeType numberOfPoints = (sizeType) index[0];
      // Vector for storing the element points
      codim0[i].resize(numberOfPoints);
      //printf(" Debug vectorsize: %d\n", numberOfPoints);
      // Read points from table and store them
      for (sizeType j = 0; j < numberOfPoints; j++)
      {
        getCoordsFromNumber(vertexValues, vertexCount, index[j+1], codim0[i][j]);
        //              printf("   Loop debug output: j %d / index %p / vertex number %d / results: %1.1f %1.1f\n", j, index, index[j+1], codim0[i][j][0], codim0[i][j][1]);
      }
      // increase index for pointing to the next element
      index += numberOfPoints + 1;
    }
  }

  /*
   * TODO: Kommentar schreiben
   */
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  typename MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::sizeType
  MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
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
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  getCoordsFromNumber(const valueVector& vertexValues,
                      const sizeType vertexCount, char number,
                      point& coords) const
  {
    // it's a center point
    if (number == EV)
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
      sizeType indexA, indexB;
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
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
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
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  bool MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  testFaceIsSurface(const valueType cornerA, const valueType cornerB,
                    const valueType cornerC, const valueType cornerD, const bool notInverted) const
  {
    // Check A*C == B*D
    if (FloatCmp::eq((cornerA*cornerC - cornerB*cornerD), 0.0))
    {
      return notInverted;
    }
    // notInverted and cornerA may invert the sign
    return ((notInverted*2 -1) * cornerA * (cornerA*cornerC - cornerB*cornerD) >= 0.0);
  }
} // end namespace Dune
