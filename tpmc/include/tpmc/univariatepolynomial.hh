// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef TPMC_UNIVARIATEPOLYNOMIAL_HH
#define TPMC_UNIVARIATEPOLYNOMIAL_HH

namespace tpmc {
  template <int po, class X>
  class UnivariatePolynomial {
  public:
    enum {
      order = po
    };
    typedef X Domain;

    template <class I>
    UnivariatePolynomial(I f, I e);

    /** \brief evaluates the polynomial using horners method
     */
    Domain operator()(const Domain& x) const;
    /** \brief evaluates the derivative of the polynomial
     */
    Domain derivative(const Domain& x) const;
    const Domain& coeff(std::size_t i) const { return coefficients_[i]; }


    template <int p, class Y>
    friend
    std::ostream& operator<<(std::ostream& s, const UnivariatePolynomial<p, Y>& poly);
  private:
    Domain coefficients_[order+1];
  };

  template <int po, class X>
  template <class I>
  UnivariatePolynomial<po,X>::UnivariatePolynomial(I f, I e) {
    std::copy(f,e,coefficients_);
  }

  template <int po, class X>
  typename UnivariatePolynomial<po,X>::Domain
  UnivariatePolynomial<po, X>::operator()(const Domain& x) const {
    Domain result(0);
    for (std::size_t i = 0; i<=order; ++i) {
      result *= x;
      result += coefficients_[order-i];
    }
    return result;
  }

  template <int po, class X>
  typename UnivariatePolynomial<po,X>::Domain
  UnivariatePolynomial<po, X>::derivative(const Domain& x) const {
    Domain result(0);
    for (std::size_t i = order; i>=1; --i) {
      result *= x;
      Domain t = i;
      t *= coefficients_[i];
      result += t;
    }
    return result;
  }


  template <int po, class X>
  std::ostream& operator<<(std::ostream& s, const UnivariatePolynomial<po, X>& p) {
    for (std::size_t i = 0; i<=po; ++i) {
      if (i<po)
        s << p.coefficients_[po-i] << "x^" << (po-i) << " + ";
      else
        s << p.coefficients_[0];
    }
    return s;
  }
}

#endif // TPMC_UNIVARIATEPOLYNOMIAL_HH
