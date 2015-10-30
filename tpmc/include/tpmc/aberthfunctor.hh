// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef TPMC_ABERTHFUNCTOR_HH
#define TPMC_ABERTHFUNCTOR_HH

#include <algorithm>
#include <array>
#include <cassert>
#include <type_traits>
#include <tpmc/univariatepolynomial.hh>
#include <tpmc/floatcmp.hh>
#include <tpmc/fieldtraits.hh>

namespace tpmc {
  class NoRootException : public std::exception {};

  /** \brief class wrapping the aberth method
   *
   * see for example: http://en.wikipedia.org/wiki/Aberth_method
   */
  class AberthMethod {
    struct AbsCmp {
      template <class X, class Y>
      bool operator()(const X& x, const Y& y) const {
        return std::abs(x) < std::abs(y);
      }
    };
    static const unsigned int MAX_ITERATION;
    static const double MIN_RESIDUUM;
  public:
    typedef std::size_t SizeType;

    template <int po, class X, class R>
    static void apply(const UnivariatePolynomial<po,X>& p, R& result) {
      typedef typename UnivariatePolynomial<po,X>::Domain Domain;
      /*Domain bound(0);
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
      */
      std::array<Domain, po> roots;
      for (SizeType i = 0; i<po; ++i) {
        roots[i] = static_cast<Domain>(i)/std::max(po-1,1);
      }
      std::array<Domain, po> value, derivative, weight;
      Domain residuum;
      update<po,X>(p, roots, value, derivative, weight, residuum);
      SizeType iteration = 0;
      while (iteration < MAX_ITERATION && std::abs(residuum) > MIN_RESIDUUM) {
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
                       const std::array<X, po>& roots, std::array<X, po>& value,
                       std::array<X, po>& derivative, std::array<X, po>& weight,
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
  template <typename Coordinate>
  class AberthFunctor
  {
  public:
    typedef typename AberthMethod::SizeType SizeType;
    typedef typename FieldTraits<Coordinate>::field_type ctype;

    template <int dim, typename InputIterator>
    static Coordinate findRoot(InputIterator valuesBegin, InputIterator valuesEnd,
                               const Coordinate& a, const Coordinate& b)
    {
      return findRootImpl(valuesBegin, valuesEnd, a, b, std::integral_constant<int,dim>());
    }
  private:

    template <int dim, typename InputIterator>
    static Coordinate findRootImpl(InputIterator valuesBegin, InputIterator valuesEnd,
                                   const Coordinate& a, const Coordinate& b, std::integral_constant<int,dim>);
    template <typename InputIterator>
    static Coordinate findRootImpl(InputIterator valuesBegin, InputIterator valuesEnd,
                                   const Coordinate& a, const Coordinate& b, std::integral_constant<int,3>);

    template <int po, class I>
    static ctype apply(const I& begin, const I& end);

    template <typename InputIterator, typename OutputIterator>
    static void insertPrismCoefficients(InputIterator valuesBegin, InputIterator valuesEnd,
                                        const Coordinate& a, const Coordinate& b,
                                        OutputIterator out);

    template <typename InputIterator, typename OutputIterator>
    static void insertCubeCoefficients(InputIterator valuesBegin, InputIterator valuesEnd,
                                       const Coordinate& a, const Coordinate& b,
                                       OutputIterator out);
  };

  template <typename Coordinate>
  template <int dim, typename InputIterator>
  Coordinate AberthFunctor<Coordinate>::findRootImpl(InputIterator valuesBegin,
                                                     InputIterator valuesEnd,
                                                     const Coordinate& a, const Coordinate& b,
                                                     std::integral_constant<int, dim>)
  {
    throw std::invalid_argument("aberth method not valid for this dimension");
  }

  template <typename Coordinate>
  template <int po, class I>
  typename FieldTraits<Coordinate>::field_type AberthFunctor<Coordinate>::apply(const I& begin, const I& end) {
    UnivariatePolynomial<po, ctype > p(begin, end);
    ctype roots[po];
    AberthMethod::apply(p,roots);
#ifndef NDEBUG
    std::cout << "found roots at: ";
    for (SizeType i = 0; i<po; ++i)
      std::cout << " " << roots[i];
    std::cout << "\n";
#endif
    ctype result = 0;
    int id = -1;
    ctype v = 0.0;
    for (SizeType i = 0; i<po; ++i) {
      ctype value = p(roots[i]);
      if (std::abs(value) < 1e-4 && FloatCmp::ge(std::min(roots[i], 1.0-roots[i]),v)) {
        id = i;
        v = roots[i];
      }
    }
    if (id >= 0)
      result = roots[id];
    else {
      throw NoRootException();
    }
#ifndef NDEBUG
    std::cout << "choosing root " << id << " at: " << result << "\n";
#endif
    return result;
  }

  template <typename Coordinate>
  template <typename InputIterator, typename OutputIterator>
  void AberthFunctor<Coordinate>::insertCubeCoefficients(InputIterator valuesBegin,
                                                         InputIterator valuesEnd,
                                                         const Coordinate& a,
                                                         const Coordinate& b,
                                                         OutputIterator out)
  {
    Coordinate x;
    for (int i = 0; i < 3; ++i)
      x[i] = b[i] - a[i];
    std::array<ctype,8> v;
    std::copy(valuesBegin, valuesEnd, v.begin());
    ctype A = v[7]-v[6]-v[5]+v[4]-v[3]+v[2]+v[1]-v[0],
          B = v[6]-v[4]-v[2]+v[0], C = v[5]-v[4]-v[1]+v[0],
          D = v[3]-v[2]-v[1]+v[0], E = v[4]-v[0], F = v[2]-v[0],
          G = v[1]-v[0], H = v[0];
    // zero coefficient
    *out++ = A*a[0]*a[1]*a[2] + B*a[1]*a[2] + C*a[0]*a[2] + D*a[0]*a[1] + E*a[2] + F*a[1] + G*a[0] + H;
    // first coefficient
    *out++ = A*(x[0]*a[1]*a[2]+a[0]*x[1]*a[2]+a[0]*a[1]*x[2]) + B*(x[1]*a[2]+a[1]*x[2]) + C*(x[0]*a[2]+a[0]*x[2]) + D*(x[0]*a[1]+a[0]*x[1]) + E*x[2] + F*x[1] + G*x[0];
    // second coefficient
    *out++ = A*(x[0]*x[1]*a[2]+x[0]*a[1]*x[2]+a[0]*x[1]*x[2]) + B*x[1]*x[2] + C*x[0]*x[2] + D*x[0]*x[1];
    // third coefficient
    *out++ = A*x[0]*x[1]*x[2];
  }

  template <typename Coordinate>
  template <typename InputIterator, typename OutputIterator>
  void AberthFunctor<Coordinate>::insertPrismCoefficients(InputIterator valuesBegin,
                                                          InputIterator valuesEnd,
                                                          const Coordinate& a,
                                                          const Coordinate& b,
                                                          OutputIterator out)
  {
    Coordinate d;
    for (int i = 0; i < 3; ++i)
      d[i] = b[i] - a[i];
    std::array<ctype, 6> v;
    std::copy(valuesBegin, valuesEnd, v.begin());
    ctype A = v[0]-v[1]-v[3]+v[4],
          B = v[0]-v[2]-v[3]+v[5],
          C = v[1]-v[0],
          D = v[2]-v[0],
          E = v[3]-v[0];
    // zero coefficient
    *out++ = a[0]*a[2]*A + a[1]*a[2]*B + a[0]*C + a[1]*D + a[2]*E + v[0];
    // first coefficient
    *out++ = (d[0]*a[2]+d[2]*a[0])*A + (d[1]*a[2]+d[2]*a[1])*B
             + d[0]*C + d[1]*D + d[2]*E;
    // second coefficient
    *out++ = d[0]*d[2]*A + d[1]*d[2]*B;
  }

  template <typename Coordinate>
  template <typename InputIterator>
  Coordinate AberthFunctor<Coordinate>::findRootImpl(InputIterator valuesBegin,
                                                     InputIterator valuesEnd,
                                                     const Coordinate& a,
                                                     const Coordinate& b,
                                                     std::integral_constant<int, 3>)
  {
    // method only supported for cube or prism
    unsigned int valueCount = std::distance(valuesBegin, valuesEnd);
    assert(valueCount == 6 || valueCount == 8);
#ifndef NDEBUG
    std::cout << "finding root between";
    for (int i = 0; i < 3; ++i)
      std::cout << " " << a[i];
    std::cout << " and ";
    for (int i = 0; i < 3; ++i)
      std::cout << " " << b[i];
    std::cout << "\n";
#endif
    ctype coefficients[4] = {0.,0.,0.,0.};
    if (valueCount == 6) {
      insertPrismCoefficients(valuesBegin, valuesEnd, a, b, coefficients);
    } else if (valueCount == 8) {
      insertCubeCoefficients(valuesBegin, valuesEnd, a, b, coefficients);
    }
#ifndef NDEBUG
    std::cout << "polynomial coefficients: "
      << coefficients[0] << " " << coefficients[1] << " "
      << coefficients[2] << " " << coefficients[3] << "\n";
#endif
    // create polynomial
    ctype root = 0.0;
    if (FloatCmp::ne(coefficients[3], 0.0)) {
      root = apply<3, ctype*>(coefficients, coefficients+4);
    } else if (FloatCmp::ne(coefficients[2], 0.0)) {
      root = apply<2, ctype*>(coefficients, coefficients+3);
    } else {
      root = apply<1, ctype*>(coefficients, coefficients+2);
    }
    Coordinate result;
    for (int i = 0; i < 3; ++i)
      result[i] = a[i] + root * (b[i] - a[i]);
    return result;
  }
}

#endif // TPMC_ABERTHFUNCTOR_HH
