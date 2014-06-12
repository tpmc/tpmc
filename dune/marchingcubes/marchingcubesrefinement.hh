// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_MARCHING_CUBES_REFINEMENT_HH
#define DUNE_MARCHING_CUBES_REFINEMENT_HH

/** \file
 * \brief A Dune wrapper for the marching cubes algorithm
 */

#include <vector>

#include <dune/geometry/genericgeometry/geometry.hh>

#include <dune/marchingcubes/marchingcubes.hh>
#include <dune/marchingcubes/thresholdfunctor.hh>

namespace Dune {

  /** \brief A Dune wrapper for the marching cubes algorithm
   *
   * Use this by constructing an object of this type.  The constructor computes
   * the splitting.  Then you can access the elements of the splitting or the interface by an iterator.
   *
   * \tparam ctype Type used for coordinates
   * \tparam dim Element dimension
   */
  template <class ctype, int dim, class thresholdFunctor = MarchingCubes::ThresholdFunctor<double> >
  class MarchingCubesRefinement
  {

  public:

    /** \brief Type of the volume geometries resulting from the splitting */
    typedef GenericGeometry::BasicGeometry<dim, GenericGeometry::DefaultGeometryTraits<ctype,dim,dim> > VolumeGeometryType;

    /** \brief Type of the interface geometries resulting from the splitting */
    typedef GenericGeometry::BasicGeometry<dim-1, GenericGeometry::DefaultGeometryTraits<ctype,dim-1,dim> > InterfaceGeometryType;

    /** \brief Container type for the volume geometries */
    typedef std::vector<VolumeGeometryType> VolumeGeometries;

    /** \brief Container type for the interface geometries */
    typedef std::vector<InterfaceGeometryType> InterfaceGeoemtries;

    /** \brief Type of the iterator over all the volume geometries resulting from the splitting */
    typedef typename std::vector<VolumeGeometryType>::const_iterator const_volume_iterator;

    /** \brief Type of the iterator over all the interface geometries resulting from the splitting */
    typedef typename std::vector<InterfaceGeometryType>::const_iterator const_interface_iterator;

    /** \brief Constructor which sets up the refinement and the interface
     *
     * Once the element is constructed you can access the refinement elements and the interface with the begin()/end() methods
     * \param values Values of the level set function at the element corners
     * \param exterior_not_interior Defines whether elements of the interior or exterior are generated
     */
    MarchingCubesRefinement(const GeometryType& type,
                            std::vector<double> values,
                            bool exterior_not_interior = false,
                            const thresholdFunctor & threshFunctor = thresholdFunctor() );

    /** \brief Get iterator to the first element of the interior volume refinement */
    const_volume_iterator interiorBegin() const {
      return interiorGeometries_.begin();
    }

    /** \brief Get iterator to one after the last element of the interior volume refinement */
    const_volume_iterator interiorEnd() const {
      return interiorGeometries_.end();
    }

    /** \brief Get iterator to the first element of the interface */
    const_interface_iterator interfaceBegin() const {
      return interfaceGeometries_.begin();
    }

    /** \brief Get iterator to one after the last element of the interface */
    const_interface_iterator interfaceEnd() const {
      return interfaceGeometries_.end();
    }

    /** \brief Access to the refinement geometries container */
    VolumeGeometries & volumeGeometries()
    { return interiorGeometries_; }

    /** \brief Access to the refinement geometries container */
    InterfaceGeoemtries & interfaceGeometries()
    { return interfaceGeometries_; }

  private:

    /** \brief Container for the geometries that we have created for the interior volume */
    VolumeGeometries interiorGeometries_;

    /** \brief Container for the geometries that we have created for the interior volume */
    InterfaceGeoemtries interfaceGeometries_;

  };

}


template <class ctype, int dim, class thresholdFunctor>
Dune::MarchingCubesRefinement<ctype,dim,thresholdFunctor>::
MarchingCubesRefinement(const GeometryType& type,
                        std::vector<double> values,
                        bool exterior_not_interior,
                        const thresholdFunctor & threshFunctor)
{
  std::vector<std::vector<FieldVector<double,dim> > > elementCorners;

  // Call the actual marching cubes algorithm
  MarchingCubes33<double,dim,thresholdFunctor> marchingcubes33(threshFunctor);
  size_t key = marchingcubes33.getKey(values, values.size(), true);

  /////////////////////////////////////////////////////////////////////////////////////////////
  //  Extract the interior volume elements
  /////////////////////////////////////////////////////////////////////////////////////////////
  marchingcubes33.getElements(values, values.size(), key, false, exterior_not_interior, elementCorners);

  // set up the list of BasicGeometries which is the output of this class
  interiorGeometries_.resize(elementCorners.size());

  // Construct the Dune GeometryType from the number of corners and the space dimension
  for (size_t i=0; i<elementCorners.size(); i++) {
    // Make BasicGeometry from the element type and the corner positions
    interiorGeometries_[i] = VolumeGeometryType(elementCorners[i]);
  }

  elementCorners.clear();

  /////////////////////////////////////////////////////////////////////////////////////////////
  //  Extract the interface elements
  /////////////////////////////////////////////////////////////////////////////////////////////

  marchingcubes33.getElements(values, values.size(), key, true,  exterior_not_interior, elementCorners);

  // set up the list of BasicGeometries which is the output of this class
  interfaceGeometries_.resize(elementCorners.size());

  // Construct the Dune GeometryType from the number of corners and the space dimension

  for (size_t i=0; i<elementCorners.size(); i++) {
    interfaceGeometries_[i] = InterfaceGeometryType(elementCorners[i]);
  }

}

#endif
