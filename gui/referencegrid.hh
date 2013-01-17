// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_MCGUI_REFERENCEGRID_HH
#define DUNE_MCGUI_REFERENCEGRID_HH

#include <dune/grid/alugrid.hh>

namespace MCGui {
  namespace {
    template <Dune::GeometryType::BasicType bt, class ctype, int dim>
    struct SelectionTraits;

    template <class ctype, int dim>
    struct SelectionTraits<Dune::GeometryType::simplex, ctype, dim> {
      typedef Dune::ALUGrid<dim,dim,Dune::simplex,Dune::conforming> GridType;
    };

    template <class ctype, int dim>
    struct SelectionTraits<Dune::GeometryType::cube, ctype, dim> {
      typedef Dune::ALUGrid<dim,dim,Dune::cube,Dune::conforming> GridType;
    };
  }

  template <Dune::GeometryType::BasicType bt, class ctype, int dim>
  class ReferenceGrid {
  public:
    typedef typename SelectionTraits<bt,ctype,dim>::GridType GridType;
    typedef typename GridType::LeafGridView GridViewType;

    ReferenceGrid()
      : reference_(Dune::GenericReferenceElements<ctype,dim>::general(Dune::GeometryType(bt,dim))) {
      reset();
    }

    GridViewType gridView() const {
      return grid_->leafView();
    }

    void refine(unsigned int n) {
      grid_->globalRefine(n);
    }

    void reset() {
      Dune::GridFactory<GridType> factory;
      std::vector<unsigned int> vertices;
      for (int i = 0; i<reference_.size(dim); ++i) {
        vertices.push_back(i);
        factory.insertVertex(reference_.position(i,dim));
      }
      factory.insertElement(reference_.type(), vertices);
      grid_.reset(factory.createGrid());
    }
  private:
    const Dune::GenericReferenceElement<ctype,dim>& reference_;
    Dune::shared_ptr<GridType> grid_;
  };
}

#endif //DUNE_MCGUI_REFERENCEGRID_HH
