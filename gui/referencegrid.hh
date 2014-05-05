// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_MCGUI_REFERENCEGRID_HH
#define DUNE_MCGUI_REFERENCEGRID_HH

#include <dune/grid/alugrid.hh>
#include <dune/grid/yaspgrid.hh>

namespace MCGui {
  namespace {
    template <Dune::GeometryType::BasicType bt, class ctype, int dim>
    struct SelectionTraits;

    template <class ctype, int dim>
    struct SelectionTraits<Dune::GeometryType::simplex, ctype, dim> {
      typedef Dune::ALUGrid<dim,dim,Dune::simplex,Dune::conforming> GridType;
      template <class Ref>
      static Dune::shared_ptr<GridType> construct(const Ref& reference) {
        Dune::GridFactory<GridType> factory;
        std::vector<unsigned int> vertices;
        for (int i = 0; i<reference.size(dim); ++i) {
          vertices.push_back(i);
          factory.insertVertex(reference.position(i,dim));
        }
        factory.insertElement(reference.type(), vertices);
        return Dune::shared_ptr<GridType>(factory.createGrid());
      }
    };

    template <class ctype, int dim>
    struct SelectionTraits<Dune::GeometryType::cube, ctype, dim> {
      typedef Dune::YaspGrid<dim> GridType;

      template <class Ref>
      static Dune::shared_ptr<GridType> construct(const Ref& reference) {
        Dune::FieldVector< ctype, dim > L(1.0);
        Dune::FieldVector< int, dim > s(1);
        Dune::FieldVector< bool, dim > periodic(false);
        return Dune::shared_ptr<GridType>(new GridType(L,s,periodic,1));
      }
    };
  }

  template <Dune::GeometryType::BasicType bt, class ctype, int dim>
  class ReferenceGrid {
  public:
    typedef typename SelectionTraits<bt,ctype,dim>::GridType GridType;
    typedef typename GridType::LeafGridView GridViewType;

    ReferenceGrid()
      : reference_(Dune::ReferenceElements<ctype,dim>::general(Dune::GeometryType(bt,dim))) {
      reset();
    }

    GridViewType gridView() const {
      return grid_->leafView();
    }

    void refine(unsigned int n) {
      grid_->globalRefine(n);
    }

    void reset() {
      grid_ = SelectionTraits<bt,ctype,dim>::construct(reference_);
    }
  private:
    const Dune::ReferenceElement<ctype,dim>& reference_;
    Dune::shared_ptr<GridType> grid_;
  };
}

#endif //DUNE_MCGUI_REFERENCEGRID_HH
