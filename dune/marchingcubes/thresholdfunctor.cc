// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include "thresholdfunctor.hh"


// TODO: Template-Parameter valueType

namespace Dune {
  namespace MarchingCubes {
    /*
     * Function to test whether a point is inside the isosurface.
     */
    bool ThresholdFunctor::isInside(double testValue)
    {
      return (testValue < threshold);
    }

    double ThresholdFunctor::getDistance(double value)
    {
      return value - threshold;
    }

    const double ThresholdFunctor::threshold = 0.6;

  } // end namespace MarchingCubes
} // end namespace Dune
