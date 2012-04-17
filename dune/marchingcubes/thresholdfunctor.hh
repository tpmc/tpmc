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
      bool isInside(vtype testValue) const
      {
        return (testValue < threshold);
      }

      //! distance to iso surface
      vtype getDistance(vtype value) const
      {
        return value - threshold;
      }

      //! minimum length for an edge below which it will be considered
      //! to be degenerated
      vtype degenerationDistance() const
      {
        return 1e-8;
      }

      //! distance to iso surface
      template<typename point>
      vtype interpolationFactor
        (const point &, const point& , const vtype va, const vtype vb) const
      {
        const vtype dist = getDistance(vb)-getDistance(va);
        return getDistance(va) / dist;
      }

      //! isInside for distance value
      bool isLower(vtype distance) const
      {
        return distance < 0;
      }

    private:
      //! Defines the isosurface.
      constexpr static vtype threshold = 0.0;
    };


    template <class vtype, class Geometry>
    class NonDegeneratingThresholdFunctor
      : public ThresholdFunctor<vtype>
    {
    public:

      //! constructor
      NonDegeneratingThresholdFunctor(const Geometry & _embedding, const vtype _minLength)
        : embedding(_embedding), minLength(_minLength)
      {}

      //! minimum length for an edge below which it will be considered
      //! to be degenerated
      vtype degenerationDistance() const
      {
        return 0;
      }

      //! distance to iso surface
      template<typename point>
      vtype interpolationFactor
        (const point &a, const point& b, const vtype va, const vtype vb) const
      {
        const vtype length = (embedding.global(a)-embedding.global(b)).two_norm();
        const vtype factor = getDistance(va) / (getDistance(vb)-getDistance(va));
        const vtype sign   = factor / std::abs(factor);
        if(length*std::abs(factor)<minLength)
          return sign*minLength/length;
        else if(length-length*std::abs(factor)<minLength)
          return sign*(1.0-minLength/length);
        else
          return factor;
      }

    private:
      const Geometry embedding;
      const vtype minLength;
    };


  } // end namespace MarchingCubes
} // end namespace Dune

#endif /* THRESHOLD_FUNCTOR_HH_ */
