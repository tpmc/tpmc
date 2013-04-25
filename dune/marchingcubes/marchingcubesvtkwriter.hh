// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_MARCHINGCUBESVTKWRITER_HH
#define DUNE_MARCHINGCUBESVTKWRITER_HH

#include <ostream>

#include <dune/geometry/type.hh>
#include <dune/common/indent.hh>
#include <dune/grid/io/file/vtk/vtkwriter.hh>
#include <dune/grid/io/file/vtk/vtuwriter.hh>
#include "marchingcubes.hh"
#include "thresholdfunctor.hh"

/** @file
    @author Christian Engwer
    @brief Provides subsampled file i/o for the visualization toolkit using the mc33 library
 */

namespace Dune
{
  /**
   * @brief Writer for the output of subsampled grid functions in the vtk format.
   * @ingroup VTK
   *
   * Writes arbitrary grid functions (living on cells or vertices of a grid)
   * to a file suitable for easy visualization with
   * <a href="http://public.kitware.com/VTK/">The Visualization Toolkit
   * (VTK)</a>.  In contrast to the regular VTKWriter, this Writer allows
   * subsampling of the elements via MC33.  The
   * MarchingCubesVTKWriter always writes nonconforming data.
   */
  template< class GridView >
  class MarchingCubesVTKWriter
    : public VTKWriter<GridView>
  {
    typedef VTKWriter<GridView> Base;
    enum { dim = GridView::dimension };
    enum { dimw = GridView::dimensionworld };
    typedef typename GridView::Grid::ctype ctype;

    typedef typename Base::CellIterator CellIterator;
    typedef typename Base::FunctionIterator FunctionIterator;
    using Base::cellBegin;
    using Base::cellEnd;
    using Base::celldata;
    using Base::ncells;
    using Base::ncorners;
    using Base::nvertices;
    using Base::outputtype;
    using Base::vertexBegin;
    using Base::vertexEnd;
    using Base::vertexdata;

  public:
    /**
     * @brief Construct a MarchingCubesVTKWriter working on a specific GridView.
     *
     * @param gridView         The gridView the grid functions live
     *                         on. (E. g. a LevelGridView.)
     *
     * The datamode is always nonconforming.
     */
    explicit MarchingCubesVTKWriter (const GridView &gridView, const VTKFunction<GridView> & levelset_, ctype interface, bool useMC33_ = true)
      : Base(gridView, VTK::nonconforming), levelset(levelset_), threshold(interface), mc33(threshold), useMC33(useMC33_)
    { }

  protected:
    //! count the vertices, cells and corners
    virtual void countEntities(int &nvertices, int &ncells, int &ncorners);

    //! write cell data
    virtual void writeCellData(VTK::VTUWriter& writer);

    //! write vertex data
    virtual void writeVertexData(VTK::VTUWriter& writer);

    //! write the positions of vertices
    virtual void writeGridPoints(VTK::VTUWriter& writer);

    //! write the connectivity array
    virtual void writeGridCells(VTK::VTUWriter& writer);

  public:
    using Base::addVertexData;

  private:
    // hide addVertexData -- adding vertex data directly without a VTKFunction
    // currently does not work since the P1VectorWrapper used for that uses a
    // nearest-neighbour search to find the value for the given point.  See
    // FS#676.
    template<class V>
    void addVertexData (const V& v, const std::string &name, int ncomps=1);

    template<class Entity>
    void getFaces(const Entity & e, std::vector< std::vector< FieldVector<ctype, dim> > > & elements) const
    {
      const GenericReferenceElement<ctype,dim> & refElem = GenericReferenceElements<ctype,dim>::general(e.type());
      std::vector<ctype> values(refElem.size(dim));
      for (unsigned int c = 0; c < refElem.size(dim); c++)
        values[c] = levelset.evaluate(0, e, refElem.position(c,dim));

      size_t key = mc33.getKey(values, values.size(), useMC33);
      mc33.getElements(values, values.size(), key, true, false, elements);
    }

    const VTKFunction<GridView> & levelset;
    MarchingCubes::ThresholdFunctor<ctype> threshold;
    MarchingCubes33<ctype, dim, MarchingCubes::ThresholdFunctor<ctype> > mc33;
    bool useMC33;
  };

  //! count the vertices, cells and corners
  template <class GridView>
  void MarchingCubesVTKWriter<GridView>::countEntities(int &nvertices, int &ncells, int &ncorners)
  {
    nvertices = 0;
    ncells = 0;
    ncorners = 0;
    for (CellIterator it=this->cellBegin(); it!=cellEnd(); ++it)
    {
      std::vector< std::vector< FieldVector<ctype, dim> > > elements;
      getFaces(*it, elements);

      ncells += elements.size();
      for (size_t e=0; e<elements.size(); e++)
      {
        nvertices += elements[e].size();
        ncorners +=  elements[e].size();
      }
    }
  }

  //! write cell data
  template <class GridView>
  void MarchingCubesVTKWriter<GridView>::writeCellData(VTK::VTUWriter& writer)
  {
    if(celldata.size() == 0)
      return;

    std::string scalars = "";
    for (FunctionIterator it=celldata.begin(); it!=celldata.end(); ++it)
      if ((*it)->ncomps()==1)
      {
        scalars = (*it)->name();
        break;
      }
    std::string vectors = "";
    for (FunctionIterator it=celldata.begin(); it!=celldata.end(); ++it)
      if ((*it)->ncomps()>1)
      {
        vectors = (*it)->name();
        break;
      }

    writer.beginCellData(scalars, vectors);
    for (FunctionIterator it=celldata.begin(); it!=celldata.end(); ++it)
    {
      // vtk file format: a vector data always should have 3 comps (with 3rd
      // comp = 0 in 2D case)
      unsigned writecomps = (*it)->ncomps();
      if(writecomps == 2) writecomps = 3;

      shared_ptr<VTK::DataArrayWriter<float> > p
        (writer.makeArrayWriter<float>((*it)->name(), writecomps, ncells));
      if(!p->writeIsNoop())
        for (CellIterator i=cellBegin(); i!=cellEnd(); ++i)
        {
          std::vector< std::vector< FieldVector<ctype, dim> > > elements;
          getFaces(*i, elements);

          for (size_t e=0; e<elements.size(); e++)
          {
            FieldVector<ctype,dim> center(0);
            for (size_t c=0; c<elements[e].size(); c++)
              center += elements[e][c];
            center /= elements[e].size();

            for (int j=0; j<(*it)->ncomps(); j++)
              p->write((*it)->evaluate(j,*i,center));
            // expand 2D-Vectors to 3D
            for(unsigned j = (*it)->ncomps(); j < writecomps; j++)
              p->write(0.0);
          }
        }
    }
    writer.endCellData();
  }

  //! write vertex data
  template <class GridView>
  void MarchingCubesVTKWriter<GridView>::writeVertexData(VTK::VTUWriter& writer)
  {
    if(vertexdata.size() == 0)
      return;

    std::string scalars = "";
    for (FunctionIterator it=vertexdata.begin(); it!=vertexdata.end(); ++it)
      if ((*it)->ncomps()==1)
      {
        scalars = (*it)->name();
        break;
      }
    std::string vectors = "";
    for (FunctionIterator it=vertexdata.begin(); it!=vertexdata.end(); ++it)
      if ((*it)->ncomps()>1)
      {
        vectors = (*it)->name();
        break;
      }

    writer.beginPointData(scalars, vectors);
    for (FunctionIterator it=vertexdata.begin(); it!=vertexdata.end(); ++it)
    {
      // vtk file format: a vector data always should have 3 comps (with 3rd
      // comp = 0 in 2D case)
      unsigned writecomps = (*it)->ncomps();
      if(writecomps == 2) writecomps = 3;

      shared_ptr<VTK::DataArrayWriter<float> > p
        (writer.makeArrayWriter<float>((*it)->name(), writecomps, nvertices));
      if(!p->writeIsNoop())
        for (CellIterator i=cellBegin(); i!=cellEnd(); ++i)
        {
          std::vector< std::vector< FieldVector<ctype, dim> > > elements;
          getFaces(*i, elements);

          for (size_t e=0; e<elements.size(); e++)
          {
            for (size_t c=0; c<elements[e].size(); c++)
            {
              for (int j=0; j<(*it)->ncomps(); j++)
                p->write((*it)->evaluate(j,*i,elements[e][c]));
              // vtk file format: a vector data always should have 3 comps (with
              // 3rd comp = 0 in 2D case)
              for(unsigned j = (*it)->ncomps(); j < writecomps; j++)
                p->write(0.0);
            }
          }
        }
    }
    writer.endPointData();
  }

  //! write the positions of vertices
  template <class GridView>
  void MarchingCubesVTKWriter<GridView>::writeGridPoints(VTK::VTUWriter& writer)
  {
    writer.beginPoints();

    shared_ptr<VTK::DataArrayWriter<float> > p
      (writer.makeArrayWriter<float>("Coordinates", 3, nvertices));
    if(!p->writeIsNoop())
      for (CellIterator i=cellBegin(); i!=cellEnd(); ++i)
      {
        std::vector< std::vector< FieldVector<ctype, dim> > > elements;
        getFaces(*i, elements);

        for (size_t e=0; e<elements.size(); e++)
        {
          for (size_t c=0; c<elements[e].size(); c++)
          {
            FieldVector<ctype, dimw> coords = i->geometry().global(elements[e][c]);
            for (int j=0; j<std::min(int(dimw),3); j++)
              p->write(coords[j]);
            for (int j=std::min(int(dimw),3); j<3; j++)
              p->write(0.0);
          }
        }
      }
    // free the VTK::DataArrayWriter before touching the stream
    p.reset();

    writer.endPoints();
  }

  //! write the connectivity array
  template <class GridView>
  void MarchingCubesVTKWriter<GridView>::writeGridCells(VTK::VTUWriter& writer)
  {
    writer.beginCells();

    // connectivity
    {
      GeometryType type;
      shared_ptr<VTK::DataArrayWriter<int> > p1
        (writer.makeArrayWriter<int>("connectivity", 1, ncorners));
      // The offset within the index numbering
      if(!p1->writeIsNoop()) {
        int offset = 0;
        for (CellIterator i=cellBegin(); i!=cellEnd(); ++i)
        {
          std::vector< std::vector< FieldVector<ctype, dim> > > elements;
          getFaces(*i, elements);

          for (size_t e=0; e<elements.size(); e++)
          {
            for (size_t c=0; c<elements[e].size(); c++)
            {
              type.makeFromVertices(dim-1,elements[e].size());
              p1->write(offset+VTK::renumber(type,c));
            }
            offset += elements[e].size();
          }
        }
      }
    }

    // offsets
    {
      shared_ptr<VTK::DataArrayWriter<int> > p2
        (writer.makeArrayWriter<int>("offsets", 1, ncells));
      if(!p2->writeIsNoop()) {
        // The offset into the connectivity array
        int offset = 0;
        for (CellIterator i=cellBegin(); i!=cellEnd(); ++i)
        {
          std::vector< std::vector< FieldVector<ctype, dim> > > elements;
          getFaces(*i, elements);

          for (size_t e=0; e<elements.size(); e++)
          {
            offset += elements[e].size();
            p2->write(offset);
          }
        }
      }
    }

    // types
    if (dim>1)
    {
      GeometryType type;
      shared_ptr<VTK::DataArrayWriter<unsigned char> > p3
        (writer.makeArrayWriter<unsigned char>("types", 1, ncells));
      if(!p3->writeIsNoop())
        for (CellIterator it=cellBegin(); it!=cellEnd(); ++it)
        {
          std::vector< std::vector< FieldVector<ctype, dim> > > elements;
          getFaces(*it, elements);

          for (size_t e=0; e<elements.size(); e++)
          {
            type.makeFromVertices(dim-1,elements[e].size());
            int vtktype = VTK::geometryType(type);
            p3->write(vtktype);
          }
        }
    }

    writer.endCells();
  }
}

#endif // DUNE_MARCHINGCUBESVTKWRITER_HH
