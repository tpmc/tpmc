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

    template <class vtype>
    class ThresholdFunctor {
    public:
      //! Function to test whether a point is inside the isosurface.
      static bool isInside(vtype testValue)
      {
        return (testValue < threshold);
      }

      //! distance to iso surface
      static vtype getDistance(vtype value)
      {
        return value - threshold;
      }

      //! isInside for distance value
      static bool isLower(vtype distance)
      {
        return distance < 0;
      }

    private:
      //! Defines the isosurface.
      constexpr static vtype threshold = 0.0;
    };

  } // end namespace MarchingCubes
} // end namespace Dune

#endif /* THRESHOLD_FUNCTOR_HH_ */
