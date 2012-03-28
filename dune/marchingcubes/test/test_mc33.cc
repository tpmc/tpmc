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
  template <typename Geometry, int count>
  class RandomDataGenerator {
    std::vector<typename Geometry::VectorType> testData_;
  public:
    typedef typename std::vector<typename Geometry::VectorType>::const_iterator const_iterator;

    RandomDataGenerator();
    const_iterator begin() const { return testData_.begin(); }
    const_iterator end() const { return testData_.end(); }
    std::string name() const {
      std::stringstream name_stream;
      name_stream << "RandomDataGenerator[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  };

  template <typename Geometry, int count>
  RandomDataGenerator<Geometry, count>::RandomDataGenerator()
    : testData_(count) {
    for (int i = 0; i<count; ++i) {
      testData_[i].resize(Geometry::vertexCount);
      std::generate(testData_[i].begin(), testData_[i].end(),
                    my_rand<typename Geometry::ValueType>);
    }
  }

  // generates vertex values in {-1,1} for all interior/exterior combinations
  template <typename Geometry>
  class AllCombinationGenerator {
    std::vector<typename Geometry::VectorType> testData_;
  public:
    typedef typename std::vector<typename Geometry::VectorType>::const_iterator const_iterator;
    static const int count = 1<<Geometry::vertexCount;

    AllCombinationGenerator();
    const_iterator begin() const { return testData_.begin(); }
    const_iterator end() const { return testData_.end(); }
    std::string name() const {
      std::stringstream name_stream;
      name_stream << "AllCombinationGenerator[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  };

  template <typename Geometry>
  AllCombinationGenerator<Geometry>::AllCombinationGenerator()
    : testData_(count) {
    for (int i = 0; i< count; ++i) {
      testData_[i].resize(Geometry::vertexCount);
      for (int j = 0; j<Geometry::vertexCount; ++j)
        testData_[i][j] = ((i>>j)&1)*2 - 1;
    }
  }

  // tests if the volume of interior and exterior match the volume of the reference element
  template <typename Geometry>
  class VolumeTest {
    const typename Geometry::VectorType& values_;
    bool result_;
  public:
    VolumeTest(const typename Geometry::VectorType& values);
    bool successful() const { return result_; }
    static std::string name() {
      std::stringstream name_stream;
      name_stream << "VolumeTest[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  private:
    template <typename I>
    bool match(I ibegin, I iend, I ebegin, I eend,
               typename Geometry::ValueType referenceVolume) const;
  };

  template <typename Geometry>
  VolumeTest<Geometry>::VolumeTest(const typename Geometry::VectorType& values)
    : values_(values) {
    typedef typename Geometry::ValueType ctype;
    const int dim = Geometry::dimension;
    Dune::GeometryType geometryType(Geometry::basicType, Geometry::dimension);

    const Dune::GenericReferenceElement<ctype, dim>& referenceElement =
      Dune::GenericReferenceElements<ctype, dim>::general(geometryType);
    Dune::MarchingCubesRefinement<ctype, dim> refInterior(geometryType, values_, false);
    Dune::MarchingCubesRefinement<ctype, dim> refExterior(geometryType, values_, true);
    result_ = match(refInterior.begin(), refInterior.end(),
                    refExterior.begin(), refExterior.end(),
                    referenceElement.volume());
  }

  template <typename Geometry>
  template <typename I>
  bool VolumeTest<Geometry>::match(I ibegin, I iend, I ebegin, I eend,
                                   typename Geometry::ValueType referenceVolume) const {
    typename Geometry::ValueType volumeInterior = 0.0,
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

  template <typename Geometry>
  struct TransformationTraits {};

  template <typename Geometry>
  class TransformationTest {
    bool result_;
  public:
    TransformationTest(const typename Geometry::VectorType& values);
    bool successful() const { return result_; }
    static std::string name() {
      std::stringstream name_stream;
      name_stream << "TransformationTest[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  private:
    template <typename I>
    typename Geometry::ValueType sumVolume(I begin, I end);
  };
  template <typename Geometry>
  TransformationTest<Geometry>::TransformationTest(const typename Geometry::VectorType& values)
    : result_(true) {
    typedef typename Geometry::ValueType ctype;
    const int dim = Geometry::dimension;
    for (int i = 0; i<TransformationTraits<Geometry>::transformationCount; ++i) {
      // rotate values
      typename Geometry::VectorType rotatedValues(Geometry::vertexCount);
      for (int j = 0; j<Geometry::vertexCount; ++j)
        rotatedValues[j] = values[TransformationTraits<Geometry>::transformations[i][j]];

      Dune::GeometryType geometryType(Geometry::basicType, Geometry::dimension);
      Dune::MarchingCubesRefinement<ctype, dim> refInterior(geometryType, values, false);
      Dune::MarchingCubesRefinement<ctype, dim> refExterior(geometryType, values, true);
      Dune::MarchingCubesRefinement<ctype, dim> refInteriorRotated(geometryType, rotatedValues, false);
      Dune::MarchingCubesRefinement<ctype, dim> refExteriorRotated(geometryType, rotatedValues, true);
      ctype vi = sumVolume(refInterior.begin(), refInterior.end());
      ctype ve = sumVolume(refExterior.begin(), refExterior.end());
      ctype vir = sumVolume(refInteriorRotated.begin(), refInteriorRotated.end());
      ctype ver = sumVolume(refExteriorRotated.begin(), refExteriorRotated.end());
      if (!Dune::FloatCmp::eq(vi, vir)) {
        result_ = false;
        std::cout << "TransformationTest: i: " << vi << " ir: " << vir << std::endl;
        std::cout << "    rotated values: (";
        vectorToStream(std::cout, rotatedValues);
        std::cout << ")" << std::endl;
      }
      if (!Dune::FloatCmp::eq(ve, ver)) {
        result_ = false;
        std::cout << "TransformationTest: e: " << ve << " er: " << ver << std::endl;
        std::cout << "    rotated values: (";
        vectorToStream(std::cout, rotatedValues);
        std::cout << ")" << std::endl;
      }
      if (!result_) {
        break;
      }
    }
  }

  template <typename Geometry>
  template <typename I>
  typename Geometry::ValueType TransformationTest<Geometry>::sumVolume(I begin, I end) {
    typename Geometry::ValueType v = 0.0;
    while (begin != end) {
      v += begin->volume();
      ++begin;
    }
    return v;
  }

  template <int dim>
  struct CubeGeometry {
    typedef double ValueType;
    typedef std::vector<ValueType> VectorType;
    static const int dimension = dim;
    static const int vertexCount = 1 << dim;
    static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::cube;
    static const std::string name;
  };
  template <int dim>
  const std::string CubeGeometry<dim>::name = "Cube";
  template <>
  struct TransformationTraits<CubeGeometry<2> > {
    static const int transformationCount = 1;
    static const int transformations[][4];
  };
  const int TransformationTraits<CubeGeometry<2> >::transformations[][4] = {{2,0,3,1}};
  template <>
  struct TransformationTraits<CubeGeometry<3> > {
    static const int transformationCount = 3;
    static const int transformations[][8];
  };
  const int TransformationTraits<CubeGeometry<3> >::transformations[][8] =
  {
    {2,0,3,1,6,4,7,5},
    {4,5,0,1,6,7,2,3},
    {1,3,0,2,5,7,4,6}
  };

  template <int dim>
  struct SimplexGeometry {
    typedef double ValueType;
    typedef std::vector<ValueType> VectorType;
    static const int dimension = dim;
    static const int vertexCount = 1 + dim;
    static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::simplex;
    static const std::string name;
  };
  template <int dim>
  const std::string SimplexGeometry<dim>::name = "Simplex";
  template <>
  struct TransformationTraits<SimplexGeometry<2> > {
    static const int transformationCount = 1;
    static const int transformations[][3];
  };
  const int TransformationTraits<SimplexGeometry<2> >::transformations[][3] = {{2,0,1}};
  template <>
  struct TransformationTraits<SimplexGeometry<3> > {
    static const int transformationCount = 1;
    static const int transformations[][4];
  };
  const int TransformationTraits<SimplexGeometry<3> >::transformations[][4] = {{2,0,1,3}};

  struct PrismGeometry {
    typedef double ValueType;
    typedef std::vector<ValueType> VectorType;
    static const int dimension = 3;
    static const int vertexCount = 6;
    static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::prism;
    static const std::string name;
  };
  const std::string PrismGeometry::name = "Prism";
  template <>
  struct TransformationTraits<PrismGeometry> {
    static const int transformationCount = 2;
    static const int transformations[][6];
  };
  const int TransformationTraits<PrismGeometry>::transformations[][6] =
  {
    {2,0,1,5,3,4},
    {3,4,5,0,1,2}
  };

  struct PyramidGeometry {
    typedef double ValueType;
    typedef std::vector<ValueType> VectorType;
    static const int dimension = 3;
    static const int vertexCount = 5;
    static const Dune::GeometryType::BasicType basicType = Dune::GeometryType::pyramid;
    static const std::string name;
  };
  const std::string PyramidGeometry::name = "Pyramid";
  template <>
  struct TransformationTraits<PyramidGeometry> {
    static const int transformationCount = 1;
    static const int transformations[][5];
  };
  const int TransformationTraits<PyramidGeometry>::transformations[][5] = {{2,0,3,1,4}};
}

int main(int argc, char* argv[]) {
  using namespace MarchingCubesTest;
  const int N = 100;
  std::srand(std::time(0));
  Test volumetest;
  volumetest.run<AllCombinationGenerator<CubeGeometry<3> >, VolumeTest<CubeGeometry<3> > >();
  volumetest.run<AllCombinationGenerator<CubeGeometry<2> >, VolumeTest<CubeGeometry<2> > >();
  volumetest.run<AllCombinationGenerator<SimplexGeometry<3> >, VolumeTest<SimplexGeometry<3> > >();
  volumetest.run<AllCombinationGenerator<SimplexGeometry<2> >, VolumeTest<SimplexGeometry<2> > >();
  volumetest.run<AllCombinationGenerator<PrismGeometry>, VolumeTest<PrismGeometry> >();
  volumetest.run<AllCombinationGenerator<PyramidGeometry>, VolumeTest<PyramidGeometry> >();
  volumetest.run<RandomDataGenerator<CubeGeometry<3>, N>, VolumeTest<CubeGeometry<3> > >();
  volumetest.run<RandomDataGenerator<CubeGeometry<2>, N>, VolumeTest<CubeGeometry<2> > >();
  volumetest.run<RandomDataGenerator<SimplexGeometry<3>, N>, VolumeTest<SimplexGeometry<3> > >();
  volumetest.run<RandomDataGenerator<SimplexGeometry<2>, N>, VolumeTest<SimplexGeometry<2> > >();
  volumetest.run<RandomDataGenerator<PrismGeometry, N>, VolumeTest<PrismGeometry> >();
  volumetest.run<RandomDataGenerator<PyramidGeometry, N>, VolumeTest<PyramidGeometry> >();
  Test transformationtest;
  transformationtest.run<AllCombinationGenerator<CubeGeometry<3> >, TransformationTest<CubeGeometry<3> > >();
  transformationtest.run<AllCombinationGenerator<CubeGeometry<2> >, TransformationTest<CubeGeometry<2> > >();
  transformationtest.run<AllCombinationGenerator<SimplexGeometry<3> >, TransformationTest<SimplexGeometry<3> > >();
  transformationtest.run<AllCombinationGenerator<SimplexGeometry<2> >, TransformationTest<SimplexGeometry<2> > >();
  transformationtest.run<AllCombinationGenerator<PrismGeometry>, TransformationTest<PrismGeometry> >();
  transformationtest.run<AllCombinationGenerator<PyramidGeometry>, TransformationTest<PyramidGeometry> >();
  transformationtest.run<RandomDataGenerator<CubeGeometry<3>, N>, TransformationTest<CubeGeometry<3> > >();
  transformationtest.run<RandomDataGenerator<CubeGeometry<2>, N>, TransformationTest<CubeGeometry<2> > >();
  transformationtest.run<RandomDataGenerator<SimplexGeometry<3>, N>, TransformationTest<SimplexGeometry<3> > >();
  transformationtest.run<RandomDataGenerator<SimplexGeometry<2>, N>, TransformationTest<SimplexGeometry<2> > >();
  transformationtest.run<RandomDataGenerator<PrismGeometry, N>, TransformationTest<PrismGeometry> >();
  transformationtest.run<RandomDataGenerator<PyramidGeometry, N>, TransformationTest<PyramidGeometry> >();
  std::cout << volumetest.success() << "/" << volumetest.count() << " volume tests successful" << std::endl;
  std::cout << transformationtest.success() << "/" << transformationtest.count() << " transformation tests successful" << std::endl;
  return !(volumetest.successful() && transformationtest.successful());
}
