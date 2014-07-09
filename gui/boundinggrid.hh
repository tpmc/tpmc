// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_MCGUI_BOUNDINGGRID_HH
#define DUNE_MCGUI_BOUNDINGGRID_HH

#include <dune/common/version.hh>

namespace MCGui {
  template <Dune::GeometryType::BasicType bt, class ctype, int dim>
  class BoundingGrid {
  public:
    typedef Dune::FieldVector<ctype,dim> VectorType;
    typedef std::pair<VectorType, VectorType> EdgeType;
    typedef typename std::vector<VectorType>::const_iterator ConstVertexIterator;
    typedef typename std::vector<EdgeType>::const_iterator ConstEdgeIterator;
    BoundingGrid() {
#if DUNE_VERSION_NEWER(DUNE_COMMON,2,3)
      const Dune::ReferenceElement<ctype, dim>& ref = Dune::ReferenceElements<ctype,dim>::general(Dune::GeometryType(bt,dim));
#else
      const Dune::GenericReferenceElement<ctype, dim>& ref = Dune::GenericReferenceElements<ctype,dim>::general(Dune::GeometryType(bt,dim));
#endif
      for (int i = 0; i<ref.size(dim-1); ++i) {
        int a = ref.subEntity(i,dim-1,0,dim);
        int b = ref.subEntity(i,dim-1,1,dim);
        edges_.push_back(std::make_pair(ref.position(a,dim), ref.position(b,dim)));
      }
      for (int i = 0; i<ref.size(dim); ++i)
        vertices_.push_back(ref.position(i,dim));
    }
    ConstVertexIterator beginVertices() const { return vertices_.begin(); }
    ConstVertexIterator endVertices() const { return vertices_.end(); }
    ConstEdgeIterator beginEdges() const { return edges_.begin(); }
    ConstEdgeIterator endEdges() const { return edges_.end(); }
    std::size_t vertexCount() const { return vertices_.size(); }
  private:
    std::vector<VectorType> vertices_;
    std::vector<EdgeType> edges_;
  };
}

#endif //DUNE_MCGUI_BOUNDINGGRID_HH
