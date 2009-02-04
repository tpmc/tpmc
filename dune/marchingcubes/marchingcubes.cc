// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
namespace Dune {

  /*
   * \brief Test if the face center is covered by the surface.
   *
   * This test is needed to chose between ambiguous MC33 cases.
   */
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  bool MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  testFaceIsSurface(valueType cornerA, valueType cornerB,
                    valueType cornerC, valueType cornerD) const
  {
    // TODO: Ausprogrammieren
    return false;
  }


  /*
   * Calculate key to access cube2d_cases_offsets.
   * Return value indicates a mc33 case.
   * TODO: Allg. Mechnismus, um auf Eck- und Grenzwert zuzugreifen, um Interpolation auszurechnen (Templates)
   * TODO: Datentyp, Dimension und Referenzelement (Würfel, Dreieck usw) als Templates einführen
   *
   * \return True if the case is in the regular table, false if it's a MC33-only case.
   */
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  bool MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  getOffsets(const valueVector& vertexValues, const sizeType vertexCount,
             const bool useMc33)
  {
    // vector containing information if vertices are inside or not
    bool *vertexInside = new bool[vertexCount];
    int caseNumber = 0;
    for (sizeType i = 0; i < vertexCount; i++)
    {
      // Shift left
      caseNumber *= 2;
      //TODO: Mechanismus Datenwerte nutzen (siehe Methodenkommentar)
      vertexInside[i] = thresholdFunctor::isInside(vertexValues[i]);
      caseNumber += (int) vertexInside[i];
    }

    // Is it a marching cubes' 33 case?
    bool isAmbiguousMc33case =
      (cube2d_cases_offsets[caseNumber][4] == AMBIGUOUS_MC33_CASE);
    if (isAmbiguousMc33case)
    {
      // TODO: test face
      // TODO: evaluate face test
      // TODO: store result
    }
    else
    {
      // TODO: store result
    }

    return isAmbiguousMc33case;
  }

  /*
   * Marching cubes' algorithm.
   * vertex_values: pointer to an array containing vertices' values
   * vertex_count: count of vertices (array length)
   * threshold: value of the isosurface
   * smaller_inside: whether smaller values are inside the isosurface
   *
   * TODO: Allg. Mechnismus, um auf Eck- und Grenzwert zuzugreifen, um Interpolation auszurechnen (Templates)
   * TODO: Datentyp, Dimension und Referenzelement (Würfel, Dreieck usw) als Templates einführen
   * TODO: Template-Parameter für codim 0 und codim(const double * vertexValues,
                      const int vertexCount, char number,
                      double * coords) 1?
   */
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  getElements(const valueVector& vertexValues,
              const sizeType vertexCount, const char * offsets,
              const bool isMc33case,
              std::vector<std::vector<point> >& codim0)
  {
    // get elements for co-dimension 0

    const char * index;
    if (isMc33case)
    {         //TODO: nur eine Tabelle
      index = cube2d_mc33_cases_offsets[(int)offsets[INDEX_OFFSET_CODIM_0]];
    }
    else
    {
      index = cube2d_cases_offsets[(int)offsets[INDEX_OFFSET_CODIM_0]];
    }
    sizeType caseCountElements = offsets[INDEX_COUNT_CODIM_0];
    codim0.resize(caseCountElements);
    for (sizeType i = 0; i < caseCountElements; i++)
    {
      sizeType numberOfElements = (sizeType) index[0];
      // Vector for storing the element points
      codim0[i].resize(numberOfElements);

      // Read points from table and store them
      for (sizeType j = 0; j < numberOfElements; j++)
      {
        getCoordsFromNumber(vertexValues, vertexCount, index[j+1], codim0[i][j]);
      }
    }
  }

  /**
   * \brief Generates the coordinate for a point which is specified
   * by its vertex or edge number.
   *
   * Result will be stored to \param coords.
   *
   * TODO: dim wäre besser als Template-Parameter ausgeführt. Dim darf nur Dimension \in {1,2,3} sein
   * TODO: Code geht nur für Würfel, Quadrate und Linien, nicht aber für Dreiecke. Als Template implementieren
   * TODO: Allg. Mechnismus, um auf Eck- und Grenzwert zuzugreifen, um Interpolation auszurechnen (Templates)
   */
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  void MarchingCubesAlgorithm<valueType, dim, thresholdFunctor, baseElement>::
  getCoordsFromNumber(const valueVector& vertexValues,
                      const sizeType vertexCount, char number,
                      point& coords)
  {
    // it's a center point
    if (number == EV)
    {
      //TODO: Koordinaten für Mittelpunkt ausrechnen
    }
    // it's an edge
    else if ((number & NO_VERTEX) == NO_VERTEX)
    {
      // use first point
      getCoordsFromEdgeNumber(vertexValues,
                              vertexCount, number, coords);
      // extract both points vertices from number
      sizeType pointA = (number / FACTOR_FIRST_POINT)
                        & (VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP);
      sizeType pointB = (number / FACTOR_SECOND_POINT)
                        & (VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP);
      // figure out in which dimension the points differ
      sizeType dim_diff = pointA ^ pointB;
      // convert bit pattern to dimension number
      dim_diff = (dim_diff & VERTEX_GO_RIGHT)*VERTEX_GO_RIGHT
                 + (dim_diff & VERTEX_GO_DEPTH)*VERTEX_GO_DEPTH
                 + (dim_diff & VERTEX_GO_UP)*VERTEX_GO_UP;
      // calculate interpolation value and store it
      coords[dim_diff] -= thresholdFunctor::getDistance(vertexValues[pointA])
                          / (thresholdFunctor::getDistance(vertexValues[pointA])
                             - thresholdFunctor::getDistance(vertexValues[pointB]));

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
                          point& coord)
  {
    number /= FACTOR_FIRST_POINT;
    // Get coordinate for each dimension. It is either 0 or 1.
    for (sizeType d = 0; d < dim; d++)
    {
      coord[d] = (ctype) (number & 1<<d);
    }
  }


} // end namespace Dune
