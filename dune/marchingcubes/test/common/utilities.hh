#ifndef MARCHINGCUBESTEST_UTILITIES_HH
#define MARCHINGCUBESTEST_UTILITIES_HH

#include <set>
#include <dune/grid/io/file/vtk/vtkwriter.hh>
#include <dune/grid/uggrid.hh>

namespace MarchingCubesTest
{
  // print the number of different geometry types
  // in the range of [begin,end)
  template <int dim, class I>
  void printVolumeStatistics(I begin, I end)
  {
    std::map<unsigned int, unsigned int> counts;
    for (; begin != end; ++begin) {
      ++counts[begin->corners()];
    }
    for (std::map<unsigned int,unsigned int>::const_iterator it = counts.begin();
         it != counts.end(); ++it) {
      if (dim == 2) {
        switch (it->first) {
        case 3 : std::cout << "Triangles: ";
          break;
        case 4 : std::cout << "Quads: ";
          break;
        default : std::cout << "Unknown: ";
        }
      } else if (dim == 3) {
        switch (it->first) {
        case 4 : std::cout << "Simplices: ";
          break;
        case 5 : std::cout << "Pyramids: ";
          break;
        case 6 : std::cout << "Prisms: ";
          break;
        case 8 : std::cout << "Cubes: ";
          break;
        default : std::cout << "Unknown: ";
        }
      }
      std::cout << it->second << "\n";
    }
  }

  // generates a random number in a given interval
  template <typename T>
  struct IntervalRandom {
    IntervalRandom(T low_, T high_)
      : low(low_), high(high_)
    {}
    T operator()() const {
      return low+(static_cast<T>(rand())/RAND_MAX)*(high-low);
    }
    T low;
    T high;
  };

  template <typename T>
  struct RingRandom {
    RingRandom(T low_, T high_)
      : low(low_), high(high_)
    {}
    T operator()() const {
      // generate random between -(high-low) and (high-low)
      T r = (high-low)*(2.0*static_cast<T>(rand())/RAND_MAX-1.0);
      if (Dune::FloatCmp::lt(r,0.0)) {
        return r-low;
      } else {
        return r+low;
      }
    }
    T low;
    T high;
  };

#if HAVE_UGGRID
  template <typename ctype, int dim>
  void toVTK(const std::string& name, const Dune::GenericReferenceElement<ctype,dim>& ref) {
    typedef Dune::UGGrid<dim> Grid;
    Dune::GridFactory<Grid> factory;
    std::vector<unsigned int> element;
    for (int i = 0; i<ref.size(dim); ++i) {
      factory.insertVertex(ref.position(i,dim));
      element.push_back(i);
    }
    factory.insertElement(ref.type(), element);
    Dune::shared_ptr<Grid> grid(factory.createGrid());
    typedef typename Grid::LeafGridView GV;
    GV gv = grid->leafView();
    Dune::VTKWriter<GV> vtkwriter(gv);
    vtkwriter.write(name);
  }

  template <typename G>
  void toVTK(const std::string& name, const G& geometry) {
    typedef typename G::ctype ctype;
    const int dim = G::mydimension;
    typedef Dune::UGGrid<dim> Grid;
    Dune::GridFactory<Grid> factory;
    std::vector<unsigned int> element;
    for (int i = 0; i<geometry.corners(); ++i) {
      factory.insertVertex(geometry.corner(i));
      element.push_back(i);
    }
    factory.insertElement(geometry.type(), element);
    Dune::shared_ptr<Grid> grid(factory.createGrid());
    typedef typename Grid::LeafGridView GV;
    GV gv = grid->leafView();
    Dune::VTKWriter<GV> vtkwriter(gv);
    vtkwriter.write(name);
  }
#endif

  struct FieldVectorLexicographicComparator {
    template <typename ctype,int dim>
    bool operator()(const Dune::FieldVector<ctype,dim>& a, const Dune::FieldVector<ctype,dim>& b) const {
      for (int i = 0; i<dim; ++i) {
        if (Dune::FloatCmp::lt(a[i],b[i]))
          return true;
        if (Dune::FloatCmp::gt(a[i],b[i]))
          return false;
      }
      return false;
    }
  };

  template <class I, class C>
  void flatInsert(I begin, I end, C& container) {
    for (; begin != end; ++begin) {
      for (std::size_t i = 0; i<begin->corners(); ++i) {
        container.insert(begin->corner(i));
      }
    }
  }

  template <class Compare, class In1, class In2, class Out>
  void findNotInSecondFlat(In1 beginFirst, In1 endFirst,
                           In2 beginSecond, In2 endSecond,
                           Out out) {
    typedef typename In1::value_type NestedType;
    typedef typename NestedType::GlobalCoordinate NestedData;
    std::set<NestedData,Compare> firstFlat;
    flatInsert(beginFirst, endFirst, firstFlat);
    std::set<NestedData,Compare> secondFlat;
    flatInsert(beginSecond, endSecond, secondFlat);
    typedef typename std::set<NestedData,Compare>::iterator It;
    for (It it = firstFlat.begin(); it != firstFlat.end(); ++it) {
      typename std::set<NestedData,Compare>::iterator itInSecond =
        secondFlat.find(*it);
      if (itInSecond == secondFlat.end()) {
        *out++ = *it;
      }
    }
  }

  template <class Vector>
  bool isInReferenceInterior(const Vector& v) {
    // no coordinate is 0 or 1
    const int dim = Vector::dimension;
    for (int d = 0; d<dim; ++d) {
      if (Dune::FloatCmp::eq(v[d],0.0) || Dune::FloatCmp::eq(v[d],1.0)) {
        return false;
      }
    }
    return true;
  }

  template <class Vector>
  bool isReferenceCorner(const Vector& v) {
    // all coordinates are either 0 or 1
    const int dim = Vector::dimension;
    for (int d = 0; d<dim; ++d) {
      if (Dune::FloatCmp::ne(v[d],0.0) && Dune::FloatCmp::ne(v[d],1.0)) {
        return false;
      }
    }
    return true;
  }

  template <class Vector>
  bool isOnReferenceEdge(const Vector& v) {
  }

  template <class Vector>
  bool isNotReferenceCorner(const Vector& v) {
    return !isReferenceCorner(v);
  }
}

#endif // MARCHINGCUBESTEST_UTILITIES_HH
