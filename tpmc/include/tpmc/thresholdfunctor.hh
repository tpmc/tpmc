// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
/*
 * MarchingThresholdFunctor.hh
 * TODO: Templateisierung des Datentyps
 */
#ifndef TPMC_THRESHOLDFUNCTOR_HH
#define TPMC_THRESHOLDFUNCTOR_HH

namespace tpmc {

    /**
     * \brief basic threshold functor
     *
     * - $u < t$   : inside
     * - $u \ge t$ : outside
     *
     * the threshold $t$ is a runtime parameter of the constructor
     *
     * \param vtype data type of the threshold value, e.g. the data type of the marching cubes class
     */
    template <class vtype>
    class ThresholdFunctor {
    public:

      //! setup the ThresholdFunctor with a given threshold value
      ThresholdFunctor(vtype v = 0.0) : threshold(v) {}

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
      vtype threshold;
    };

    /**
     * \brief wraps a static constant of type double.
     *
     * the number is encode in the form A.B*10^(Exp)
     * \tparam A   the pre-comma part
     * \tparam B   the post-comma part
     * \tparam Exp the exponent
     *
     * \code
     * double_constant<17,3> // == 17.3
     * \endcode
     * or
     * \code
     * double_constant<1,3,-4> // == 1.3e-4
     * \endcode
     */
    template<int A, unsigned int B = 0, int Exp = 1>
    struct double_constant
    {
    static constexpr double value =
      (A + // the pre comma values
        (B>0 ?
          (A>0?1.0:-1.0) // the sign
          * B            // the post comma values
          * std::pow(10,-std::ceil(std::log10(B))):0.0) // the B exponent
        )
      * std::pow(10,Exp); // the overall exponent
    };

    /**
     * \brief basic threshold functor
     *
     * - $u < t$   : inside
     * - $u \ge t$ : outside
     *
     * the threshold $t$ and the data type are obtained statically from the ValueTraits
     *
     * ValueTraits are an implementation of the following type:
     * \code
     * struct ValueTraits {
     *   static constexpr double value = 17.3;
     * };
     * \endcode
     * for convinience you can just use the double_constant class, for example
     * \code
     * double_constant<17,3> // == 17.3
     * \endcode
     */
    template <typename ValueTraits>
    class StaticThresholdFunctor {
    public:

      typedef typename ValueTraits::ValueType vtype;

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
      constexpr static vtype threshold = ValueTraits::value;
    };
}

#endif // TPMC_THRESHOLDFUNCTOR_HH
