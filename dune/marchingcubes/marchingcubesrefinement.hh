// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_MARCHING_CUBES_REFINEMENT_HH
#define DUNE_MARCHING_CUBES_REFINEMENT_HH

/** \file
 * \brief A Dune wrapper for the marching cubes algorithm
 */

#include <vector>

#include <dune/grid/genericgeometry/geometry.hh>

#include <dune/marchingcubes/marchingcubes.hh>
#include <dune/marchingcubes/thresholdfunctor.hh>

namespace Dune {

  /** \brief A Dune wrapper for the marching cubes algorithm
   *
   * Use this by constructing an object of this type.  The constructor computes
   * the splitting.  Then you can access the elements of the splitting by an iterator.
   *
   * \tparam ctype Type used for coordinates
   * \tparam dim Element dimension
   */
  template <class ctype, int dim>
  class MarchingCubesRefinement
  {

  public:

    /** \brief Type of the geometries resulting from the splitting */
    typedef GenericGeometry::BasicGeometry<dim, GenericGeometry::DefaultGeometryTraits<ctype,dim,dim> > RefinementGeometryType;

    /** \brief Type of the iterator over all the geometries resulting from the splitting */
    typedef typename std::vector<RefinementGeometryType>::const_iterator const_iterator;

    /** \brief Constructor which sets up the refinement
     *
     * Once the element is constructed you can access the refinement elements with the begin()/end() methods
     * \param type Type of the element that we want to refine
     * \param values Values of the level set function at the element corners
     */
    MarchingCubesRefinement(const GeometryType& type,
                            std::vector<double> values);

    /** \brief Get iterator to the first element of the refinement */
    const_iterator begin() const {
      return geometries_.begin();
    }

    /** \brief Get iterator to one after the last element of the refinement */
    const_iterator end() const {
      return geometries_.end();
    }


  private:

    /** \brief Container for the geometries that we have created */
    std::vector<RefinementGeometryType> geometries_;

  };

}


template <class ctype, int dim>
Dune::MarchingCubesRefinement<ctype,dim>::
MarchingCubesRefinement(const GeometryType& type,std::vector<double> values)
{
  std::vector<std::vector<FieldVector<double,dim> > > elementCorners;

  // Call the actual marching cubes algorithm
  MarchingCubes33<double,dim,MarchingCubes::ThresholdFunctor> marchingcubes33;
  size_t key = marchingcubes33.getKey(values, values.size(), true);
  marchingcubes33.getElements(values, values.size(), key, false, false, elementCorners);

  // set up the list of BasicGeometries which is the output of this class
  geometries_.resize(elementCorners.size());

  // Construct the Dune GeometryType from the number of corners and the space dimension
  for (size_t i=0; i<elementCorners.size(); i++) {

    GeometryType type;
    if (dim==2) {

      switch (elementCorners[i].size()) {
      case 3 :
        type.makeSimplex(dim);
        break;
      case 4 :
        type.makeCube(dim);
        break;
      default :
        DUNE_THROW(NotImplemented, "2d elements with " << elementCorners[i].size() << " corners are not supported!");
      }

    } else if (dim==3) {

      switch (elementCorners[i].size()) {
      case 4 :
        type.makeSimplex(dim);
        break;
      case 5 :
        type.makePyramid();
        break;
      case 6 :
        type.makePrism();
        break;
      case 8 :
        type.makeCube(dim);
        break;
      default :
        DUNE_THROW(NotImplemented, "3d elements with " << elementCorners[i].size() << " corners are not supported!");
      }


    } else
      DUNE_THROW(NotImplemented, "MarchingCubesRefinement only implemented for 2d and 3d");

    // Make BasicGeometry from the element type and the corner positions
    geometries_[i] = RefinementGeometryType(type, elementCorners[i]);
  }

}

#endif
