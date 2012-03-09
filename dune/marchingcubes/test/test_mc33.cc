// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>
#include <cstdlib>
#include <sstream>
#include "dune/common/float_cmp.hh"
#include "dune/common/geometrytype.hh"
#include "dune/common/shared_ptr.hh"
#include "dune/grid/genericgeometry/topologytypes.hh"
#include "dune/grid/common/genericreferenceelements.hh"
#include "dune/marchingcubes/marchingcubesrefinement.hh"

namespace MarchingCubesTest {
  template <typename S, typename V>
  void vectorToStream(S& s, const V& v) {
    for (std::size_t i = 0; i<v.size(); ++i)
      s << (i>0 ? ", " : "") << v[i];
  }

  // runs tests and counts the successful ones
  class Test {
    int count_;
    int success_;
  public:
    Test()
      : count_(0), success_(0) {}

    template <typename G, typename T>
    void run();
    bool successful() const { return count_ == success_; }
    int count() const { return count_; }
    int success() const { return success_; }
  };

  template <typename G, typename T>
  void Test::run() {
    G generator;
    for (typename G::const_iterator it = generator.begin();
         it != generator.end(); ++it) {
      T test(*it);
      count_++;
      success_ += test.successful();
      if (!test.successful()) {
        std::cout << "[FAILED] test " << test.name() << " failed on " << generator.name() << std::endl;
        std::cout << "         vertex values: (";
        vectorToStream(std::cout, *it);
        std::cout << ")" << std::endl;
      }
    }
  }

  // generates a random number in [-1,1]
  template <typename T>
  T my_rand() {
    return (static_cast<T>(rand())/RAND_MAX)*2.0-1.0;
  }

  // generates random vertex values for count test runs
  template <typename Traits, int count>
  class RandomDataGenerator {
    std::vector<typename Traits::VectorType> testData_;
  public:
    typedef typename std::vector<typename Traits::VectorType>::const_iterator const_iterator;

    RandomDataGenerator();
    const_iterator begin() const { return testData_.begin(); }
    const_iterator end() const { return testData_.end(); }
    std::string name() const {
      std::stringstream name_stream;
      name_stream << "RandomDataGenerator[" << Traits::name << Traits::dimension << "d]";
      return name_stream.str();
    }
  };

  template <typename Traits, int count>
  RandomDataGenerator<Traits, count>::RandomDataGenerator()
    : testData_(count) {
    for (int i = 0; i<count; ++i) {
      testData_[i].resize(Traits::vertexCount);
      std::generate(testData_[i].begin(), testData_[i].end(),
                    my_rand<typename Traits::ValueType>);
    }
  }

  // generates vertex values in {-1,1} for all interior/exterior combinations
  template <typename Traits>
  class AllCombinationGenerator {
    std::vector<typename Traits::VectorType> testData_;
  public:
    typedef typename std::vector<typename Traits::VectorType>::const_iterator const_iterator;
    static const int count = 1<<Traits::vertexCount;

    AllCombinationGenerator();
    const_iterator begin() const { return testData_.begin(); }
    const_iterator end() const { return testData_.end(); }
    std::string name() const {
      std::stringstream name_stream;
      name_stream << "AllCombinationGenerator[" << Traits::name << Traits::dimension << "d]";
      return name_stream.str();
    }
  };

  template <typename Traits>
  AllCombinationGenerator<Traits>::AllCombinationGenerator()
    : testData_(count) {
    for (int i = 0; i< count; ++i) {
      testData_[i].resize(Traits::vertexCount);
      for (int j = 0; j<Traits::vertexCount; ++j)
        testData_[i][j] = ((i>>j)&1)*2 - 1;
    }
  }

  // tests if the volume of interior and exterior match the volume of the reference element
  template <typename Traits>
  class VolumeTest {
    const typename Traits::VectorType& values_;
    bool result_;
  public:
    VolumeTest(const typename Traits::VectorType& values);
    bool successful() const { return result_; }
    std::string name() const {
      std::stringstream name_stream;
      name_stream << "VolumeTest[" << Traits::name << Traits::dimension << "d]";
      return name_stream.str();
    }
  private:
    template <typename I>
    bool match(I ibegin, I iend, I ebegin, I eend,
               typename Traits::ValueType referenceVolume) const;
  };

  template <typename Traits>
  VolumeTest<Traits>::VolumeTest(const typename Traits::VectorType& values)
    : values_(values) {
    typedef typename Traits::ValueType ctype;
    const int dim = Traits::dimension;
    Dune::GeometryType geometryType(Traits::basicType, Traits::dimension);

    const Dune::GenericReferenceElement<ctype, dim>& referenceElement =
      Dune::GenericReferenceElements<ctype, dim>::general(geometryType);
    Dune::MarchingCubesRefinement<ctype, dim> refInterior(geometryType, values_, false);
    Dune::MarchingCubesRefinement<ctype, dim> refExterior(geometryType, values_, true);
    result_ = match(refInterior.begin(), refInterior.end(),
                    refExterior.begin(), refExterior.end(),
                    referenceElement.volume());
  }

  template <typename Traits>
  template <typename I>
  bool VolumeTest<Traits>::match(I ibegin, I iend, I ebegin, I eend,
                                 typename Traits::ValueType referenceVolume) const {
    typename Traits::ValueType volumeInterior = 0.0,
    volumeExterior = 0.0;
    int countInterior = 0, countExterior = 0;
    for (I it = ibegin; it != iend; ++it) {
      volumeInterior += it->volume();
      ++countInterior;
    }
    for (I it = ebegin; it != eend; ++it) {
      volumeExterior += it->volume();
      ++countExterior;
    }
    bool result = Dune::FloatCmp::eq(volumeInterior+volumeExterior, referenceVolume);
    if (!result) {
      std::cout << "VolumeTest: i: " << volumeInterior << " (" << countInterior << ") "
                << " e: " << volumeExterior << " (" << countExterior << ") "
                << " sum: " << volumeInterior+volumeExterior << " != "
                << referenceVolume << std::endl;
    }
    return result;
  }
}

template <int dim>
struct CubeTraits {
  typedef double ValueType;
  typedef std::vector<ValueType> VectorType;
  static const int dimension = dim;
  static const int vertexCount = 1 << dim;
  static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::cube;
  static const std::string name;
};
template <int dim>
const std::string CubeTraits<dim>::name = "Cube";

template <int dim>
struct SimplexTraits {
  typedef double ValueType;
  typedef std::vector<ValueType> VectorType;
  static const int dimension = dim;
  static const int vertexCount = 1 + dim;
  static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::simplex;
  static const std::string name;
};
template <int dim>
const std::string SimplexTraits<dim>::name = "Simplex";

struct PrismTraits {
  typedef double ValueType;
  typedef std::vector<ValueType> VectorType;
  static const int dimension = 3;
  static const int vertexCount = 6;
  static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::prism;
  static const std::string name;
};
const std::string PrismTraits::name = "Prism";

struct PyramidTraits {
  typedef double ValueType;
  typedef std::vector<ValueType> VectorType;
  static const int dimension = 3;
  static const int vertexCount = 5;
  static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::pyramid;
  static const std::string name;
};
const std::string PyramidTraits::name = "Pyramid";

int main(int argc, char* argv[]) {
  using namespace MarchingCubesTest;
  const int N = 100;
  std::srand(std::time(0));
  Test test;
  test.run<AllCombinationGenerator<CubeTraits<3> >, VolumeTest<CubeTraits<3> > >();
  test.run<AllCombinationGenerator<CubeTraits<2> >, VolumeTest<CubeTraits<2> > >();
  test.run<AllCombinationGenerator<SimplexTraits<3> >, VolumeTest<SimplexTraits<3> > >();
  test.run<AllCombinationGenerator<SimplexTraits<2> >, VolumeTest<SimplexTraits<2> > >();
  test.run<AllCombinationGenerator<PrismTraits>, VolumeTest<PrismTraits> >();
  test.run<AllCombinationGenerator<PyramidTraits>, VolumeTest<PyramidTraits> >();
  test.run<RandomDataGenerator<CubeTraits<3>, N>, VolumeTest<CubeTraits<3> > >();
  test.run<RandomDataGenerator<CubeTraits<2>, N>, VolumeTest<CubeTraits<2> > >();
  test.run<RandomDataGenerator<SimplexTraits<3>, N>, VolumeTest<SimplexTraits<3> > >();
  test.run<RandomDataGenerator<SimplexTraits<2>, N>, VolumeTest<SimplexTraits<2> > >();
  test.run<RandomDataGenerator<PrismTraits, N>, VolumeTest<PrismTraits> >();
  test.run<RandomDataGenerator<PyramidTraits, N>, VolumeTest<PyramidTraits> >();
  std::cout << test.success() << "/" << test.count() << " tests successful" << std::endl;
  return !test.successful();
}
