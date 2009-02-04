// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
/*
 * MarchingThresholdFunctor.hh
 * TODO: Templateisierung des Datentyps
 */

#ifndef THRESHOLD_FUNCTOR_HH_
#define THRESHOLD_FUNCTOR_HH_

namespace Dune {
  namespace MarchingCubes {

    class ThresholdFunctor {
    public:
      /*
       * Function to test whether a point is inside the isosurface.
       */
      static bool isInside(double testValue);

      static double getDistance(double value);

    private:
      /*
       * Defines the isosurface.
       */
      const static double threshold;
    };

  } // end namespace MarchingCubes
} // end namespace Dune

#endif /* THRESHOLD_FUNCTOR_HH_ */
