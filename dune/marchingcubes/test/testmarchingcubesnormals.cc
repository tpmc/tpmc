// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#if HAVE_CONFIG_H
    #include "config.h"
#endif
#include <iostream>
#include <ctime>
#include <dune/marchingcubes/marchingcubes.hh>
#include <dune/marchingcubes/thresholdfunctor.hh>
#include <dune/common/fvector.hh>
#include <dune/common/fassign.hh>

/** \brief number of random tests to be run */
const int RANDOM_TESTS = 200;


template <class ctype, int dim>
struct MultilinearFunctor {
  typedef Dune::FieldVector<int, dim> MultiIndex;

  template <class I>
  MultilinearFunctor(I begin, I end)
    : coefficients_(begin, end) {}

  /** \brief compute next multi index (count binary) */
  void next(MultiIndex& mi) {
    int i = 0;
    for (; i<dim && mi[i] == 1; mi[i] = 0, ++i) ;
    if (i<dim) mi[i] = 1;
  }

  /** \brief map a multi index to its associated value */
  int linear(const MultiIndex& mi) {
    int result = 0;
    for (int i = 0; i<dim; ++i) {
      result += (1 << i)*mi[i];
    }
    return result;
  }

  /** \brief evaluate functor at x */
  ctype operator()(const Dune::FieldVector<ctype,dim>& x) {
    ctype res = 0;
    MultiIndex mi;
    mi = 0;
    // loop through all coefficients
    for (int i = 0; i<(1<<dim); ++i, next(mi)) {
      int l = linear(mi);
      ctype c = coefficients_[l];
      for (int j = 0; j<dim; ++j) {
        c *= (mi[j] == 0 ? 1.0-x[j] : x[j]);
      }
      res += c;
    }
    return res;
  }

  /** \brief compute gradient at x */
  Dune::FieldVector<ctype,dim> gradient(const Dune::FieldVector<ctype,dim>& x) {
    Dune::FieldVector<ctype,dim> result;
    result = 0.0;
    // loop through all dimension and compute derivate
    for (int i = 0; i<dim; ++i) {
      MultiIndex mi;
      mi = 0;
      // now check all coefficients
      for (int k = 0; k<(1<<dim); ++k, next(mi)) {
        ctype c = coefficients_[linear(mi)];
        // consider coordinates
        for (int j = 0; j<dim; ++j) {
          if (j != i) {
            c *= (mi[j] == 0 ? 1.0-x[j] : x[j]);
          }
        }
        c *= 2*mi[i]-1;
        result[i] += c;
      }
    }
    return result;
  }

  std::vector<ctype> coefficients_;
};

/** \brief compares the normal given by the mc33 with a normal interpolated from
 * the gradient at element corners. check if both point in the same direction */
template <class ctype, int dim, class V>
bool testNormal(const V& values,
                std::size_t size,
                bool useMc33) {
  // create interface refinement
  MultilinearFunctor<ctype,dim> functor(values.begin(), values.end());
  Dune::MarchingCubes33<ctype,dim, Dune::MarchingCubes::ThresholdFunctor<ctype> > mc;
  std::size_t key = mc.getKey(values, size, useMc33);
  std::vector<std::vector<Dune::FieldVector<ctype, dim> > > elements;
  mc.getElements(values, size, key, true, false, elements);
  // loop through all elements and retrieve normal
  typename std::vector<std::vector<Dune::FieldVector<ctype,dim> > >::const_iterator it = elements.begin();
  for (; it != elements.end(); ++it) {
    // first retrieve normal from mc
    Dune::FieldVector<ctype,dim> normal;
    mc.getNormal(*it, normal);
    // and now from the multi linear functor by taking the mean of the gradient at the element corners
    // \TODO note: linear interpolation of gradient in general not applicable!!
    Dune::FieldVector<ctype,dim> centerNormal(0.0);
    typename std::vector<Dune::FieldVector<ctype,dim> >::const_iterator eit = it->begin();
    for (; eit != it->end(); ++eit) {
      Dune::FieldVector<ctype,dim> g = functor.gradient(*eit);
      centerNormal += g;
    }
    centerNormal /= centerNormal.two_norm();
    // check if test is successfull and normals match
    ctype dot = normal*centerNormal;
    if (dot < 1e-5) {
      std::cout << "TEST FAILED:\n";
      std::cout << "values:";
      for (std::size_t i = 0; i<size; ++i) {
        std::cout << " " << values[i];
      }
      std::cout << "\n";
      std::cout << "element corners:\n";
      typename std::vector<Dune::FieldVector<ctype,dim> >::const_iterator eit = it->begin();
      for (; eit != it->end(); ++eit) {
        Dune::FieldVector<ctype,dim> g = functor.gradient(*eit);
        std::cout << *eit << " value: " << functor(*eit) << " gradient: " << g << "\n";
      }
      std::cout << "normal: " << normal << "\tcalculated: " << centerNormal << "\n";
      std::cout << "dot: " << dot << "\n";
      return false;
    }
  }
  return true;
}

template <class ctype>
struct RandGen {
  ctype range;
  explicit RandGen(ctype range) : range(range) {}
  ctype operator()() {
    return (1.0-2.0*(std::rand()/(double)RAND_MAX))*range;
  }
};

/** \brief generate random values between -1.0 and 1.0 and run testNormal */
template <class ctype, int dim>
bool testRandomNormal(bool useMc33) {
  int count = 1<<dim;
  std::vector<ctype> values;
  values.reserve(count);
  std::generate_n(std::back_inserter(values), count, RandGen<ctype>(1.0));
  return testNormal<ctype,dim>(values, count, useMc33);
}

int main(int argc, const char *argv[]) {
  try {
    std::srand(time(NULL));
    int passed = 0, total = 0;
    Dune::FieldVector<double,8> values;
    values <<= -1,-1,-1,-1,1,1,1,1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= 1,1,1,1,-1,-1,-1,-1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= -1,-1,1,1,-1,-1,1,1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= 1,1,-1,-1,1,1,-1,-1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= -1,1,-1,1,-1,1,-1,1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= 1,-1,1,-1,1,-1,1,-1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= -1,1,1,1,1,1,1,1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= 1,-1,-1,-1,-1,-1,-1,-1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= -2,-2,1,1,1,1,1,1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    values <<= 2,2,-1,-1,-1,-1,-1,-1;
    ++total;
    passed += testNormal<double,3>(values, values.size(), true);
    for (int i = 0; i<RANDOM_TESTS; ++i) {
      ++total;
      passed += testRandomNormal<double,3>(true);
    }
    std::cout << "Result of normal tests: " << passed << " of " << total << " tests passed\n";
  } catch (Dune::Exception& ex) {
    std::cout << "Dune::Exception: " << ex.what() << "\n";
  }
}
