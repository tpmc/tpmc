// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#if HAVE_CONFIG_H
#include "config.h"
#endif

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>
#include <cstdlib>
#include <sstream>
#include <dune/common/float_cmp.hh>
#include <dune/geometry/type.hh>
#include <dune/common/shared_ptr.hh>
#include <dune/geometry/genericgeometry/topologytypes.hh>
#include <dune/geometry/referenceelements.hh>
#include <dune/geometry/quadraturerules.hh>
#include <dune/marchingcubes/marchingcubesrefinement.hh>
#include <dune/marchingcubes/test/common/utilities.hh>

namespace MarchingCubesTest {
  template <typename S, typename V>
  void vectorToStream(S& s, const V& v, const std::string& sep) {
    for (std::size_t i = 0; i<v.size(); ++i)
      s << (i>0 ? sep : "") << v[i];
  }

  template <typename V>
  std::string valuesToCode(const V& v) {
    std::stringstream ss;
    for (std::size_t i = 0; i<v.size(); ++i)
      ss << (v[i]>0.0);
    return ss.str();
  }

  // runs tests and counts the successful ones
  class Test {
  public:
    Test(std::string name)
      : count_(0), success_(0), name_(name) {}

    template <typename G, typename T>
    void run();
    bool successful() const { return count_ == success_; }
    int count() const { return count_; }
    int success() const { return success_; }
    template <class S>
    void report(S& stream) {
      stream << "Result of test <" << name_ << ">: " << success_
             << "/" << count_ << " tests successful\n";
    }
  private:
    int count_;
    int success_;
    std::string name_;
  };

  template <typename G, typename T>
  void Test::run() {
    G generator;
    for (typename G::const_iterator it = generator.begin();
         it != generator.end(); ++it) {
      std::cout << "running test " << name_ << " on " << generator.name() << std::endl;
      std::cout << "case " << valuesToCode(*it) << std::endl;
      std::cout << "./dune_mc_gui ";
      vectorToStream(std::cout, *it, " ");
      std::cout << "\n";
      count_++;
      T test(*it);
      success_ += test.successful();
      if (!test.successful()) {
        std::cout << "[FAILED] test " << test.name() << " failed on " << generator.name() << std::endl;
        std::cout << "case " << valuesToCode(*it) << std::endl;
        std::cout << "./dune_mc_gui ";
        vectorToStream(std::cout, *it, " ");
        std::cout << "\n";
      }
    }
  }

  // ####### RandomDataGenerator #######

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
      std::generate(testData_[i].begin(), testData_[i].end(), IntervalRandom<double>(-1,1));
    }
  }

  // ####### AllInsideGenerator #######

  // generates vertex values of -1 for all vertices
  template <typename Geometry>
  class AllInsideGenerator {
    std::vector<typename Geometry::VectorType> testData_;
  public:
    typedef typename std::vector<typename Geometry::VectorType>::const_iterator const_iterator;

    AllInsideGenerator();
    const_iterator begin() const { return testData_.begin(); }
    const_iterator end() const { return testData_.end(); }
    std::string name() const {
      std::stringstream name_stream;
      name_stream << "AllInsideGenerator[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  };
  template <typename Geometry>
  AllInsideGenerator<Geometry>::AllInsideGenerator()
    : testData_(1,typename Geometry::VectorType(Geometry::vertexCount,-1.0)) {}

  // ####### AllCombinationGenerator #######

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
    IntervalRandom<double> random(-0.3,0.3);
    for (int i = 0; i< count; ++i) {
      testData_[i].resize(Geometry::vertexCount);
      for (int j = 0; j<Geometry::vertexCount; ++j)
        testData_[i][j] = ((i>>j)&1)*2 - 1+random();
    }
  }

  template <class Geo>
  typename Geo::ctype integrate(const Geo& geo, int intorder = 3) {
    typename Geo::ctype result = 0.0;
    const Dune::QuadratureRule<typename Geo::ctype, Geo::mydimension>& rule = Dune::QuadratureRules<typename Geo::ctype, Geo::mydimension>::rule(geo.type(), intorder);
    for (typename Dune::QuadratureRule<typename Geo::ctype, Geo::mydimension>::const_iterator it = rule.begin();
         it != rule.end(); ++it) {
      result += it->weight()*geo.integrationElement(it->position());
    }
    return result;
  }

  // tests if the volume of interior and exterior match the volume of the reference element
  template <typename Geometry>
  class InterfaceTest {
    bool result_;
  public:
    typedef Geometry GeometryType;

    InterfaceTest(const typename Geometry::VectorType& values);
    bool successful() const { return result_; }
    static std::string name() {
      std::stringstream name_stream;
      name_stream << "InterfaceTest[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  };

  template <typename Geometry>
  InterfaceTest<Geometry>::InterfaceTest(const typename Geometry::VectorType& values)
    : result_(true) {
    typedef typename Geometry::ValueType ctype;
    const int dim = Geometry::dimension;
    Dune::GeometryType geometryType(Geometry::basicType, Geometry::dimension);

    Dune::MarchingCubesRefinement<ctype, dim> refInterior(geometryType, values, false);
    Dune::MarchingCubesRefinement<ctype, dim> refExterior(geometryType, values, true);
    // find all exterior vertices which are not in interface
    typedef FieldVectorLexicographicComparator Compare;
    typedef Dune::FieldVector<ctype,dim> Coordinate;
    typedef std::vector<Coordinate> CoordinateVector;
    CoordinateVector exNotInIntf;
    findNotInSecondFlat<Compare>(refExterior.interiorBegin(),
                                 refExterior.interiorEnd(),
                                 refExterior.interfaceBegin(),
                                 refExterior.interfaceEnd(),
                                 std::back_inserter(exNotInIntf));
    typedef typename CoordinateVector::const_iterator It;
    // make sure that every such vertex is a reference corner
    It exNoRefCorner = std::find_if(exNotInIntf.begin(), exNotInIntf.end(), isNotReferenceCorner<Coordinate>);
    if (exNoRefCorner != exNotInIntf.end()) {
      std::cout << "InterfaceTest failing: exterior coordinate " << *exNoRefCorner << " not in interface and not a reference corner\n";
      result_ = false;
    }
    // find all interior vertices which are not in the interface
    CoordinateVector inNotInIntf;
    findNotInSecondFlat<Compare>(refInterior.interiorBegin(),
                                 refInterior.interiorEnd(),
                                 refInterior.interfaceBegin(),
                                 refInterior.interfaceEnd(),
                                 std::back_inserter(inNotInIntf));
    // make sure that every such vertex is a reference corner
    It inNoRefCorner = std::find_if(inNotInIntf.begin(), inNotInIntf.end(), isNotReferenceCorner<Coordinate>);
    if (inNoRefCorner != inNotInIntf.end()) {
      std::cout << "InterfaceTest failing: interior coordinate " << *inNoRefCorner << " not in interface and not a reference corner\n";
      result_ = false;
    }
  }

  // tests if the volume of interior and exterior match the volume of the reference element
  template <typename Geometry>
  class VolumeTest {
    const typename Geometry::VectorType& values_;
    bool result_;
  public:
    typedef Geometry GeometryType;

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

#if DUNE_VERSION_NEWER(DUNE_COMMON,2,3)
    const Dune::ReferenceElement<ctype, dim>& referenceElement =
      Dune::ReferenceElements<ctype, dim>::general(geometryType);
#else
    const Dune::GenericReferenceElement<ctype, dim>& referenceElement =
      Dune::GenericReferenceElements<ctype, dim>::general(geometryType);
#endif
    Dune::MarchingCubesRefinement<ctype, dim> refInterior(geometryType, values_, false);
    Dune::MarchingCubesRefinement<ctype, dim> refExterior(geometryType, values_, true);
    result_ = match(refInterior.interiorBegin(), refInterior.interiorEnd(),
                    refExterior.interiorBegin(), refExterior.interiorEnd(),
                    referenceElement.volume());
  }

  template <typename Geometry>
  template <typename I>
  bool VolumeTest<Geometry>::match(I ibegin, I iend, I ebegin, I eend,
                                   typename Geometry::ValueType referenceVolume) const {
    const int dim = Geometry::dimension;
    typename Geometry::ValueType volumeInterior = 0.0,
    volumeExterior = 0.0;
    int countInterior = 0, countExterior = 0;
    for (I it = ibegin; it != iend; ++it) {
      volumeInterior += integrate(*it);
      ++countInterior;
    }
    for (I it = ebegin; it != eend; ++it) {
      volumeExterior += integrate(*it);
      ++countExterior;
    }
    bool result = Dune::FloatCmp::eq(volumeInterior+volumeExterior, referenceVolume);
    if (!result) {
      std::cout << "VolumeTest failing: i: " << volumeInterior << " (" << countInterior << ") "
                << " e: " << volumeExterior << " (" << countExterior << ") "
                << " diff: " << std::abs(volumeInterior+volumeExterior-referenceVolume) << std::endl;
      std::cout << "Interior:\n";
      printVolumeStatistics<dim>(ibegin, iend);
      std::cout << "Exterior:\n";
      printVolumeStatistics<dim>(ebegin, eend);
    }
    return result;
  }

  template <typename Geometry>
  class ValidCoordinatesTest {
    bool result_;
  public:
    typedef Geometry GeometryType;

    ValidCoordinatesTest(const typename Geometry::VectorType& values);
    bool successful() const { return result_; }
    static std::string name() {
      std::stringstream name_stream;
      name_stream << "ValidCoordinatesTest[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  private:
    template <class I>
    bool check(I begin, I end) const;
  };
  template <typename Geometry>
  ValidCoordinatesTest<Geometry>::ValidCoordinatesTest(const typename Geometry::VectorType& values)
    : result_(true) {
    typedef typename Geometry::ValueType ctype;
    const int dim = Geometry::dimension;
    Dune::GeometryType geometryType(Geometry::basicType, Geometry::dimension);
    Dune::MarchingCubesRefinement<ctype, dim> refInterior(geometryType, values, false);
    Dune::MarchingCubesRefinement<ctype, dim> refExterior(geometryType, values, true);
    result_ = check(refInterior.interiorBegin(), refInterior.interiorEnd())
      && check(refExterior.interiorBegin(), refExterior.interiorEnd());
  }
  template <typename Geometry>
  template <class I>
  bool ValidCoordinatesTest<Geometry>::check(I begin, I end) const {
    typedef typename Geometry::ValueType ctype;
    const int dim = Geometry::dimension;
    Dune::GeometryType geometryType(Geometry::basicType, Geometry::dimension);
#if DUNE_VERSION_NEWER(DUNE_COMMON,2,3)
    const Dune::ReferenceElement<ctype, dim>& referenceElement =
      Dune::ReferenceElements<ctype, dim>::general(geometryType);
#else
    const Dune::GenericReferenceElement<ctype, dim>& referenceElement =
      Dune::GenericReferenceElements<ctype, dim>::general(geometryType);
#endif
    for (; begin != end; ++begin) {
      for (int i = 0; i<begin->corners(); ++i) {
        if (!referenceElement.checkInside(begin->corner(i))) {
          return false;
        }
      }
    }
    return true;
  }

  template <typename Geometry>
  class InversionTest {
    bool result_;
  public:
    typedef Geometry GeometryType;

    InversionTest(const typename Geometry::VectorType& values);
    bool successful() const { return result_; }
    static std::string name() {
      std::stringstream name_stream;
      name_stream << "InversionTest[" << Geometry::name << Geometry::dimension << "d]";
      return name_stream.str();
    }
  private:
    template <typename I>
    typename Geometry::ValueType sumVolume(I begin, I end);
  };
  template <typename Geometry>
  InversionTest<Geometry>::InversionTest(const typename Geometry::VectorType& values)
    : result_(true) {
    typedef typename Geometry::ValueType ctype;
    const int dim = Geometry::dimension;
    Dune::GeometryType geometryType(Geometry::basicType, Geometry::dimension);
    typename Geometry::VectorType invertedValues(values);
    for (int i = 0; i<invertedValues.size(); ++i) {
      invertedValues[i] *= -1.0;
    }
    Dune::MarchingCubesRefinement<ctype, dim> refInterior(geometryType, values, false);
    Dune::MarchingCubesRefinement<ctype, dim> refExteriorInverted(geometryType, invertedValues, true);
    typedef typename Dune::MarchingCubesRefinement<ctype, dim>::const_volume_iterator It;
    typedef FieldVectorLexicographicComparator Compare;
    std::vector<Dune::FieldVector<ctype,dim> > inNotInInvEx;
    // find all coordinates of an interior element which are not part
    // of an inverted exterior element
    findNotInSecondFlat<Compare>(refInterior.interiorBegin(),
                                 refInterior.interiorEnd(),
                                 refExteriorInverted.interiorBegin(),
                                 refExteriorInverted.interiorEnd(),
                                 std::back_inserter(inNotInInvEx));
    if (inNotInInvEx.size() > 0) {
      // such coordinates are only valid in the interior
      for (std::size_t i = 0; i<inNotInInvEx.size(); ++i) {
        if (!isInReferenceInterior(inNotInInvEx[i])) {
          std::cout << "InversionTest: coordinate " << inNotInInvEx[i] << " not in invertedExterior and not an interior coordinate\n";
          result_ = false;
        }
      }
    }
  }
  template <typename Geometry>
  template <typename I>
  typename Geometry::ValueType InversionTest<Geometry>::sumVolume(I begin, I end) {
    typename Geometry::ValueType v = 0.0;
    while (begin != end) {
      v += integrate(*begin);
      ++begin;
    }
    return v;
  }

  template <typename Geometry>
  struct TransformationTraits {};

  template <typename Geometry>
  class TransformationTest {
    bool result_;
  public:
    typedef Geometry GeometryType;

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
      ctype vi = sumVolume(refInterior.interiorBegin(), refInterior.interiorEnd());
      ctype ve = sumVolume(refExterior.interiorBegin(), refExterior.interiorEnd());
      ctype vir = sumVolume(refInteriorRotated.interiorBegin(), refInteriorRotated.interiorEnd());
      ctype ver = sumVolume(refExteriorRotated.interiorBegin(), refExteriorRotated.interiorEnd());
      if (Dune::FloatCmp::ne(vi, vir) || Dune::FloatCmp::ne(ve, ver)) {
        result_ = false;
        std::cout << "TransformationTest: i: " << vi << " ir: " << vir
                  << " e: " << ve << " er: " << ver << std::endl;
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
      v += integrate(*begin);
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
  try {
    const int N = 1500;
    std::srand(std::time(0));
    Test allinside("allinside");
    allinside.run<AllInsideGenerator<CubeGeometry<3> >, VolumeTest<CubeGeometry<3> > >();
    allinside.run<AllInsideGenerator<CubeGeometry<2> >, VolumeTest<CubeGeometry<2> > >();
    allinside.run<AllInsideGenerator<SimplexGeometry<3> >, VolumeTest<SimplexGeometry<3> > >();
    allinside.run<AllInsideGenerator<SimplexGeometry<2> >, VolumeTest<SimplexGeometry<2> > >();
    allinside.run<AllInsideGenerator<PrismGeometry >, VolumeTest<PrismGeometry> >();
    allinside.run<AllInsideGenerator<PyramidGeometry >, VolumeTest<PyramidGeometry> >();
    Test volumetest("volume");
    volumetest.run<AllCombinationGenerator<CubeGeometry<3> >, VolumeTest<CubeGeometry<3> > >();
    volumetest.run<AllCombinationGenerator<CubeGeometry<2> >, VolumeTest<CubeGeometry<2> > >();
    volumetest.run<AllCombinationGenerator<SimplexGeometry<3> >, VolumeTest<SimplexGeometry<3> > >();
    volumetest.run<AllCombinationGenerator<SimplexGeometry<2> >, VolumeTest<SimplexGeometry<2> > >();
    volumetest.run<AllCombinationGenerator<PrismGeometry>, VolumeTest<PrismGeometry> >();
    //volumetest.run<AllCombinationGenerator<PyramidGeometry>, VolumeTest<PyramidGeometry> >();
    volumetest.run<RandomDataGenerator<CubeGeometry<3>, N>, VolumeTest<CubeGeometry<3> > >();
    volumetest.run<RandomDataGenerator<CubeGeometry<2>, N>, VolumeTest<CubeGeometry<2> > >();
    volumetest.run<RandomDataGenerator<SimplexGeometry<3>, N>, VolumeTest<SimplexGeometry<3> > >();
    volumetest.run<RandomDataGenerator<SimplexGeometry<2>, N>, VolumeTest<SimplexGeometry<2> > >();
    volumetest.run<RandomDataGenerator<PrismGeometry, N>, VolumeTest<PrismGeometry> >();
    //volumetest.run<RandomDataGenerator<PyramidGeometry, N>, VolumeTest<PyramidGeometry> >();

    //Test transformationtest("transformation");
    //transformationtest.run<AllCombinationGenerator<CubeGeometry<3> >, TransformationTest<CubeGeometry<3> > >();
    //transformationtest.run<AllCombinationGenerator<CubeGeometry<2> >, TransformationTest<CubeGeometry<2> > >();
    //transformationtest.run<AllCombinationGenerator<SimplexGeometry<3> >, TransformationTest<SimplexGeometry<3> > >();
    //transformationtest.run<AllCombinationGenerator<SimplexGeometry<2> >, TransformationTest<SimplexGeometry<2> > >();
    //transformationtest.run<AllCombinationGenerator<PrismGeometry>, TransformationTest<PrismGeometry> >();
    ////transformationtest.run<AllCombinationGenerator<PyramidGeometry>, TransformationTest<PyramidGeometry> >();
    //transformationtest.run<RandomDataGenerator<CubeGeometry<3>, N>, TransformationTest<CubeGeometry<3> > >();
    //transformationtest.run<RandomDataGenerator<CubeGeometry<2>, N>, TransformationTest<CubeGeometry<2> > >();
    //transformationtest.run<RandomDataGenerator<SimplexGeometry<3>, N>, TransformationTest<SimplexGeometry<3> > >();
    //transformationtest.run<RandomDataGenerator<SimplexGeometry<2>, N>, TransformationTest<SimplexGeometry<2> > >();
    //transformationtest.run<RandomDataGenerator<PrismGeometry, N>, TransformationTest<PrismGeometry> >();
    ////transformationtest.run<RandomDataGenerator<PyramidGeometry, N>, TransformationTest<PyramidGeometry> >();
    Test validcoordinatestest("validcoordinates");
    validcoordinatestest.run<AllCombinationGenerator<CubeGeometry<3> >, ValidCoordinatesTest<CubeGeometry<3> > >();
    validcoordinatestest.run<AllCombinationGenerator<CubeGeometry<2> >, ValidCoordinatesTest<CubeGeometry<2> > >();
    validcoordinatestest.run<AllCombinationGenerator<SimplexGeometry<3> >, ValidCoordinatesTest<SimplexGeometry<3> > >();
    validcoordinatestest.run<AllCombinationGenerator<SimplexGeometry<2> >, ValidCoordinatesTest<SimplexGeometry<2> > >();
    validcoordinatestest.run<AllCombinationGenerator<PrismGeometry>, ValidCoordinatesTest<PrismGeometry> >();
    validcoordinatestest.run<AllCombinationGenerator<PyramidGeometry>, ValidCoordinatesTest<PyramidGeometry> >();
    validcoordinatestest.run<RandomDataGenerator<CubeGeometry<3>, N>, ValidCoordinatesTest<CubeGeometry<3> > >();
    validcoordinatestest.run<RandomDataGenerator<CubeGeometry<2>, N>, ValidCoordinatesTest<CubeGeometry<2> > >();
    validcoordinatestest.run<RandomDataGenerator<SimplexGeometry<3>, N>, ValidCoordinatesTest<SimplexGeometry<3> > >();
    validcoordinatestest.run<RandomDataGenerator<SimplexGeometry<2>, N>, ValidCoordinatesTest<SimplexGeometry<2> > >();
    validcoordinatestest.run<RandomDataGenerator<PrismGeometry, N>, ValidCoordinatesTest<PrismGeometry> >();
    validcoordinatestest.run<RandomDataGenerator<PyramidGeometry, N>, ValidCoordinatesTest<PyramidGeometry> >();
    Test inversiontest("inversion");
    inversiontest.run<AllCombinationGenerator<CubeGeometry<3> >, InversionTest<CubeGeometry<3> > >();
    inversiontest.run<AllCombinationGenerator<CubeGeometry<2> >, InversionTest<CubeGeometry<2> > >();
    inversiontest.run<AllCombinationGenerator<SimplexGeometry<3> >, InversionTest<SimplexGeometry<3> > >();
    inversiontest.run<AllCombinationGenerator<SimplexGeometry<2> >, InversionTest<SimplexGeometry<2> > >();
    inversiontest.run<AllCombinationGenerator<PrismGeometry>, InversionTest<PrismGeometry> >();
    inversiontest.run<AllCombinationGenerator<PyramidGeometry>, InversionTest<PyramidGeometry> >();
    inversiontest.run<RandomDataGenerator<CubeGeometry<3>, N>, InversionTest<CubeGeometry<3> > >();
    inversiontest.run<RandomDataGenerator<CubeGeometry<2>, N>, InversionTest<CubeGeometry<2> > >();
    inversiontest.run<RandomDataGenerator<SimplexGeometry<3>, N>, InversionTest<SimplexGeometry<3> > >();
    inversiontest.run<RandomDataGenerator<SimplexGeometry<2>, N>, InversionTest<SimplexGeometry<2> > >();
    inversiontest.run<RandomDataGenerator<PrismGeometry, N>, InversionTest<PrismGeometry> >();
    inversiontest.run<RandomDataGenerator<PyramidGeometry, N>, InversionTest<PyramidGeometry> >();
    Test interfacetest("interface");
    interfacetest.run<AllCombinationGenerator<CubeGeometry<3> >, InterfaceTest<CubeGeometry<3> > >();
    interfacetest.run<AllCombinationGenerator<CubeGeometry<2> >, InterfaceTest<CubeGeometry<2> > >();
    interfacetest.run<AllCombinationGenerator<SimplexGeometry<3> >, InterfaceTest<SimplexGeometry<3> > >();
    interfacetest.run<AllCombinationGenerator<SimplexGeometry<2> >, InterfaceTest<SimplexGeometry<2> > >();
    interfacetest.run<AllCombinationGenerator<PrismGeometry>, InterfaceTest<PrismGeometry> >();
    interfacetest.run<AllCombinationGenerator<PyramidGeometry>, InterfaceTest<PyramidGeometry> >();
    interfacetest.run<RandomDataGenerator<CubeGeometry<3>, N>, InterfaceTest<CubeGeometry<3> > >();
    interfacetest.run<RandomDataGenerator<CubeGeometry<2>, N>, InterfaceTest<CubeGeometry<2> > >();
    interfacetest.run<RandomDataGenerator<SimplexGeometry<3>, N>, InterfaceTest<SimplexGeometry<3> > >();
    interfacetest.run<RandomDataGenerator<SimplexGeometry<2>, N>, InterfaceTest<SimplexGeometry<2> > >();
    interfacetest.run<RandomDataGenerator<PrismGeometry, N>, InterfaceTest<PrismGeometry> >();
    interfacetest.run<RandomDataGenerator<PyramidGeometry, N>, InterfaceTest<PyramidGeometry> >();
    allinside.report(std::cout);
    volumetest.report(std::cout);
    //transformationtest.report(std::cout);
    validcoordinatestest.report(std::cout);
    inversiontest.report(std::cout);
    interfacetest.report(std::cout);
    return !(allinside.successful() && validcoordinatestest.successful() && inversiontest.successful() && interfacetest.successful() && volumetest.successful());// && transformationtest.successful());
  } catch (Dune::Exception& ex) {
    std::cout << ex.what();
  }
}
