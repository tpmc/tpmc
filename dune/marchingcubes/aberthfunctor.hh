// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef ABERTHFUNCTOR_HH
#define ABERTHFUNCTOR_HH

#include <algorithm>
#include <dune/common/fvector.hh>
#include <dune/common/array.hh>
#include "univariatepolynomial.hh"
#include "newtonfunctor.hh"

namespace Dune {

  /** \brief class wrapping the aberth method
   *
   * see for example: http://en.wikipedia.org/wiki/Aberth_method
   */
  template <class StopPolicy>
  class AberthMethod {
    struct AbsCmp {
      template <class X, class Y>
      bool operator()(const X& x, const Y& y) const {
        return std::abs(x) < std::abs(y);
      }
    };
  public:
    typedef std::size_t SizeType;

    template <int po, class X, class R>
    static void apply(const UnivariatePolynomial<po,X>& p, R& result) {
      typedef typename UnivariatePolynomial<po,X>::Domain Domain;
      Domain bound(0);
      for (SizeType i = 0; i<po; ++i)
        if (FloatCmp::ne(std::abs(p.coeff(i+1)), 0.0))
          bound += std::abs(p.coeff(i))/std::abs(p.coeff(i+1));
#ifndef NDEBUG
      std::cout << "bound = " << bound << "\n";
#endif
      array<Domain, po> roots;
      for (SizeType i = 0; i<po; ++i) {
        roots[i] = 2*static_cast<int>(i)-po+1;
        roots[i] /= std::max(po-1,1);
        roots[i] *= bound;
      }
      array<Domain, po> value, derivative, weight;
      Domain residuum;
      update<po,X>(p, roots, value, derivative, weight, residuum);
      SizeType iteration = 0;
      while (!StopPolicy::stop(iteration, std::abs(residuum))) {
#ifndef NDEBUG
        std::cout << "aberth method at iterator " << iteration
                  << " roots: ";
        for (SizeType i = 0; i<po; ++i)
          std::cout << " " << roots[i] << " [" << value[i] << "] ";
        std::cout << "\n";
#endif
        for (SizeType i = 0; i<po; ++i) {
          Domain t = value[i] / derivative[i];
          roots[i] -= t / (1.0-t*weight[i]);
        }
        update<po, X>(p, roots, value, derivative, weight, residuum);
        ++iteration;
      }
      for (SizeType i = 0; i<po; ++i)
        result[i] = roots[i];
    }

    template <int po, class X>
    static void update(const UnivariatePolynomial<po, X>& p,
                       const array<X, po>& roots, array<X, po>& value,
                       array<X, po>& derivative, array<X, po>& weight,
                       X& residuum) {
      for (SizeType i = 0; i<po; ++i) {
        value[i] = p(roots[i]);
        if (i == 0 || std::abs(value[i]) > std::abs(residuum))
          residuum = value[i];
        derivative[i] = p.derivative(roots[i]);
        weight[i] = 0;
        for (SizeType j = 0; j<po; ++j) {
          if (i == j)
            continue;
          weight[i] += 1.0/(roots[i]-roots[j]);
        }
      }
    }
  };

  /** \brief functor to be used in the mc algorithm
   */
  template <typename ctype,
      class StopPolicy = OrCombinedStopPolicy<ctype,
          ResiduumStopPolicy,
          IterationStopPolicy> >
  class AberthFunctor {
  public:
    typedef typename AberthMethod<StopPolicy>::SizeType SizeType;
    typedef FieldVector<ctype, 3> PointType;

    template <class VectorType>
    static void findRoot(const VectorType& vertex_values,
                         const PointType& a,
                         const PointType& b,
                         PointType& result);

    template <class VectorType>
    static void findRoot(const VectorType& vertex_values,
                         const Dune::FieldVector<ctype, 2>& a,
                         const Dune::FieldVector<ctype, 2>& b,
                         Dune::FieldVector<ctype, 2>& result);
  private:
    template <int po, class I>
    static void apply(const I& begin, const I& end, ctype& result);
  };


  template <typename ctype, class StopPolicy>
  template <class VectorType>
  void AberthFunctor<ctype, StopPolicy>::findRoot(const VectorType& vertex_values,
                                                  const Dune::FieldVector<ctype, 2>& a,
                                                  const Dune::FieldVector<ctype, 2>& b,
                                                  Dune::FieldVector<ctype, 2>& result) {
    DUNE_THROW(Dune::NotImplemented, "aberth method not supported for 2d vector");
  }

  template <typename ctype, class StopPolicy>
  template <int po, class I>
  void AberthFunctor<ctype, StopPolicy>::apply(const I& begin, const I& end, ctype& result) {
    UnivariatePolynomial<po, ctype > p(begin, end);
    ctype roots[po];
    AberthMethod<StopPolicy>::apply(p,roots);
#ifndef NDEBUG
    std::cout << "found roots at: ";
    for (SizeType i = 0; i<po; ++i)
      std::cout << " " << roots[i];
    std::cout << "\n";
#endif
    result = 0;
    int id = -1;
    ctype v = 0.0;
    for (SizeType i = 0; i<po; ++i) {
      if (FloatCmp::ge(std::min(roots[i], 1.0-roots[i]),v)) {
        id = i;
        v = roots[i];
      }
    }
    if (id >= 0)
      result = roots[id];
#ifndef NDEBUG
    std::cout << "choosing root " << id << " at: " << result << "\n";
#endif
  }


  template <typename ctype, class StopPolicy>
  template <class VectorType>
  void AberthFunctor<ctype, StopPolicy>::findRoot(const VectorType& v,
                                                  const PointType& a,
                                                  const PointType& b,
                                                  PointType& result) {
    PointType x(b);
    x -= a;
    // compute coefficients
    ctype A = v[7]-v[6]-v[5]+v[4]-v[3]+v[2]+v[1]-v[0],
          B = v[6]-v[4]-v[2]+v[0], C = v[5]-v[4]-v[1]+v[0],
          D = v[3]-v[2]-v[1]+v[0], E = v[4]-v[0], F = v[2]-v[0],
          G = v[1]-v[0], H = v[0];
    ctype coefficients[] = {
      A*a[0]*a[1]*a[2] + B*a[1]*a[2] + C*a[0]*a[2] + D*a[0]*a[1]
      + E*a[2] + F*a[1] + G*a[0] + H,
      A*(x[0]*a[1]*a[2]+a[0]*x[1]*a[2]+a[0]*a[1]*x[2])
      + B*(x[1]*a[2]+a[1]*x[2]) + C*(x[0]*a[2]+a[0]*x[2])
      + D*(x[0]*a[1]+a[0]*x[1]) + E*x[2] + F*x[1] + G*x[0],
      A*(x[0]*x[1]*a[2]+x[0]*a[1]*x[2]+a[0]*x[1]*x[2])
      + B*x[1]*x[2] + C*x[0]*x[2] + D*x[0]*x[1],
      A*x[0]*x[1]*x[2]
    };
    // create polynomial
    ctype root = 0.0;
    if (Dune::FloatCmp::ne(coefficients[3], 0.0)) {
      apply<3, ctype*>(coefficients, coefficients+4, root);
    } else if (Dune::FloatCmp::ne(coefficients[2], 0.0)) {
      apply<2, ctype*>(coefficients, coefficients+3, root);
    } else {
      apply<1, ctype*>(coefficients, coefficients+2, root);
    }
    result = x;
    result *= root;
    result += a;
  }
}

#endif //ABERTHFUNCTOR_HH
