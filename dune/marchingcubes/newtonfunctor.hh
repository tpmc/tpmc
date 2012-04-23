// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __NEWTONFUNCTOR_HH__
#define __NEWTONFUNCTOR_HH__

#include <dune/common/float_cmp.hh>

#include "trilinearfunction.hh"

namespace Dune {
  /*
   * stop Newton's method after a constant number of iterations
   */
  template <unsigned int maxIteration = 5>
  class IterationStopPolicy {
  public:
    template <typename ValueType>
    static bool stop(unsigned int iteration, ValueType residuum) {
      return iteration >= maxIteration;
    }
  };

  /*
   * stop Newton's method if the residuum is small enough
   */
  template <typename ValueType>
  class ResiduumStopPolicy {
  public:
    static bool stop(unsigned int iteration, ValueType residuum) {
      return std::abs(residuum) < MIN_RESIDUUM;
    }
  private:
    static const ValueType MIN_RESIDUUM;
  };
  template <typename ValueType>
  const ValueType ResiduumStopPolicy<ValueType>::MIN_RESIDUUM = 1e-8;

  /*
   * finds a root of a trilinear function along a line from a point a
   * to a point b using a combination of Newton's method and Bisection
   */
  template <typename ValueType, class StopPolicy = ResiduumStopPolicy<ValueType> >
  class NewtonFunctor {
    typedef double ctype;
  public:
    typedef FieldVector<ctype, 3> PointType;

    template <class VectorType>
    static void findRoot(const VectorType& vertex_values,
                         const PointType& a,
                         const PointType& b,
                         PointType& result);
  private:
    /* parameterization of a line from a to b; line(t=0)=a, line(t=1)=b */
    static void line(ValueType t, const PointType& a,
                     const PointType& b, PointType& result) {
      result = b;
      result -= a;
      result *= t;
      result += a;
    }
  };

  template <typename ValueType, class StopPolicy>
  template <class VectorType>
  void NewtonFunctor<ValueType, StopPolicy>::findRoot(const VectorType& vertex_values,
                                                      const PointType& a,
                                                      const PointType& b,
                                                      PointType& result) {
    typedef TrilinearFunction<ValueType> TF;
    ValueType fa = TF::evaluate(vertex_values, a);
    ValueType fb = TF::evaluate(vertex_values, b);
    ValueType l = 0.0, r = 1.0;
    // use linear interpolation as a starting value
    ValueType t = -fa/(fb-fa);
    line(t,a,b,result);
    ValueType residuum = TF::evaluate(vertex_values, result);
    unsigned int iteration = 0;

#ifndef NDEBUG
    std::cout << "starting Newton from " << a << " (" << fa << ") "
              << " to " << b << " (" << fb << ") with t = " << t << "\n";
#endif
    /* stop criteria provided by StopPolicy */
    while (!StopPolicy::stop(iteration, residuum)) {
      ++iteration;
      // compute gradient
      PointType gradient;
      TF::gradient(vertex_values, result, gradient);
      // update the current iteration using newton's method
      t -= residuum/((b-a)*gradient);
      // if it is out of range, use a bisection step
      if (FloatCmp::lt(t,l) || FloatCmp::lt(r,t)) {
#ifndef NDEBUG
        std::cout << "t using Newton's out of range: " << t
                  << " not in [" << l << "," << r << "] using "
                  << "bisection: t = " << 0.5*(l+r) << std::endl;
#endif
        t = 0.5*(l+r);
      }
      // update the coordinates and the residuum
      line(t, a, b, result);
      residuum = TF::evaluate(vertex_values, result);
      if (residuum*fa > 0)
        l = t;
      else
        r = t;

#ifndef NDEBUG
      std::cout << "Newton at iteration " << iteration
                << " residuum: " << residuum
                << " t: " << t << " (" << l <<"," << r <<") result: " << result << "\n";
#endif
    }
  }
}

#endif //__NEWTONFUNCTOR_HH__
