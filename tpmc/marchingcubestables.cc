// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include "lut/marchinglut.hh"

namespace Dune {
  /* table specialization for non symmetric tables */

  /*
   * Case offset tables (e.g. table_cube2d_cases offsets) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      typename intersectionFunctor>
  typename MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::nonsymmetric,
      intersectionFunctor>::offsetRow *
  MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::nonsymmetric,intersectionFunctor>::
  all_case_offsets[] = {NULL, NULL, NULL, table_any1d_cases_offsets,
                        NULL, table_simplex2d_cases_offsets,
                        table_cube2d_cases_offsets,
                        table_simplex3d_cases_offsets,
                        table_pyramid3d_cases_offsets,
                        table_prism3d_cases_offsets,
                        NULL, table_cube3d_cases_offsets};

  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::nonsymmetric,intersectionFunctor>::
  all_case_vertices[] = {NULL, NULL, NULL, table_any1d_vertices,
                         NULL, table_simplex2d_vertices,
                         table_cube2d_vertices, table_simplex3d_vertices,
                         table_pyramid3d_vertices, table_prism3d_vertices,
                         NULL, table_cube3d_vertices};

  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::nonsymmetric, intersectionFunctor>::
  all_vertex_to_index[] = {NULL, NULL, NULL, table_any1d_vertex_to_index,
                           NULL, table_simplex2d_vertex_to_index,
                           table_cube2d_vertex_to_index,
                           table_simplex3d_vertex_to_index,
                           table_pyramid3d_vertex_to_index,
                           table_prism3d_vertex_to_index,
                           NULL, table_cube3d_vertex_to_index};

  /*
   * vertex_groups tables (e.g. table_cube2d_vertex_groups) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::nonsymmetric, intersectionFunctor>::
  all_vertex_groups[] = {NULL, NULL, NULL, table_any1d_vertex_groups,
                         NULL, table_simplex2d_vertex_groups,
                         table_cube2d_vertex_groups,
                         table_simplex3d_vertex_groups,
                         table_pyramid3d_vertex_groups,
                         table_prism3d_vertex_groups,
                         NULL, table_cube3d_vertex_groups};

  /*
   * Codimension 0 element tables (e.g. table_cube2d_codim_0) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::nonsymmetric, intersectionFunctor>::
  all_codim_0[][2] = {{NULL, NULL}, {NULL, NULL}, {NULL, NULL},
                      {table_any1d_codim_0_interior,
                       table_any1d_codim_0_exterior}, {NULL, NULL},
                      {table_simplex2d_codim_0_interior,
                       table_simplex2d_codim_0_exterior},
                      {table_cube2d_codim_0_interior,
                       table_cube2d_codim_0_exterior},
                      {table_simplex3d_codim_0_interior,
                       table_simplex3d_codim_0_exterior},
                      {table_pyramid3d_codim_0_interior,
                       table_pyramid3d_codim_0_exterior},
                      {table_prism3d_codim_0_interior,
                       table_prism3d_codim_0_exterior}, {NULL, NULL},
                      {table_cube3d_codim_0_interior,
                       table_cube3d_codim_0_exterior}};

  /*
   * element group tables (e.g. table_cube2d_codim_0_exterior_groups)
   * for different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::nonsymmetric, intersectionFunctor>::
  all_element_groups[][2] = {{NULL, NULL}, {NULL, NULL}, {NULL, NULL},
                             {table_any1d_interior_groups,
                              table_any1d_exterior_groups}, {NULL, NULL},
                             {table_simplex2d_interior_groups,
                              table_simplex2d_exterior_groups},
                             {table_cube2d_interior_groups,
                              table_cube2d_exterior_groups},
                             {table_simplex3d_interior_groups,
                              table_simplex3d_exterior_groups},
                             {table_pyramid3d_interior_groups,
                              table_pyramid3d_exterior_groups},
                             {table_prism3d_interior_groups,
                              table_prism3d_exterior_groups}, {NULL, NULL},
                             {table_cube3d_interior_groups,
                              table_cube3d_exterior_groups}};

  /*
   * Codimension 1 element tables (e.g. table_cube2d_codim_1) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::nonsymmetric, intersectionFunctor>::
  all_codim_1[] = {NULL, NULL, NULL, table_any1d_codim_1,
                   NULL, table_simplex2d_codim_1,
                   table_cube2d_codim_1, table_simplex3d_codim_1,
                   table_pyramid3d_codim_1, table_prism3d_codim_1, NULL,
                   table_cube3d_codim_1};

  /*
   * MC33 offset tables (e.g. table_cube2d_mc33_offsets) for
   * different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::nonsymmetric, intersectionFunctor>::
  all_mc33_offsets[] = {NULL, NULL, NULL, NULL, NULL, NULL,
                        table_cube2d_mc33_offsets, NULL,
                        table_pyramid3d_mc33_offsets,
                        table_prism3d_mc33_offsets, NULL,
                        table_cube3d_mc33_offsets};

  /*
   * Test face tables (e.g. table_cube2d_mc33_face_test_order) for
   * different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::nonsymmetric, intersectionFunctor>::
  all_face_tests[] = {NULL, NULL, NULL, NULL, NULL, NULL,
                      table_cube2d_mc33_face_test_order, NULL,
                      table_pyramid3d_mc33_face_test_order,
                      table_prism3d_mc33_face_test_order, NULL,
                      table_cube3d_mc33_face_test_order};


  /** table secialization for symmetric cases */

  /*
   * Case offset tables (e.g. table_cube2d_cases offsets) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      typename intersectionFunctor>
  typename MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::symmetric,
      intersectionFunctor>::offsetRow *
  MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::symmetric,intersectionFunctor>::
  all_case_offsets[] = {NULL, NULL, NULL, table_any1d_cases_offsets,
                        NULL, table_simplex2d_cases_offsets,
                        table_cube2d_cases_offsets,
                        table_simplex3d_cases_offsets,
                        table_pyramid3d_cases_offsets,
                        table_prism3d_cases_offsets,
                        NULL, table_cube3dsym_cases_offsets};

  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::symmetric,intersectionFunctor>::
  all_case_vertices[] = {NULL, NULL, NULL, table_any1d_vertices,
                         NULL, table_simplex2d_vertices,
                         table_cube2d_vertices, table_simplex3d_vertices,
                         table_pyramid3d_vertices, table_prism3d_vertices,
                         NULL, table_cube3dsym_vertices};

  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::symmetric, intersectionFunctor>::
  all_vertex_to_index[] = {NULL, NULL, NULL, table_any1d_vertex_to_index,
                           NULL, table_simplex2d_vertex_to_index,
                           table_cube2d_vertex_to_index,
                           table_simplex3d_vertex_to_index,
                           table_pyramid3d_vertex_to_index,
                           table_prism3d_vertex_to_index,
                           NULL, table_cube3d_vertex_to_index};

  /*
   * vertex_groups tables (e.g. table_cube2d_vertex_groups) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::symmetric, intersectionFunctor>::
  all_vertex_groups[] = {NULL, NULL, NULL, table_any1d_vertex_groups,
                         NULL, table_simplex2d_vertex_groups,
                         table_cube2d_vertex_groups,
                         table_simplex3d_vertex_groups,
                         table_pyramid3d_vertex_groups,
                         table_prism3d_vertex_groups,
                         NULL, table_cube3dsym_vertex_groups};

  /*
   * Codimension 0 element tables (e.g. table_cube2d_codim_0) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::symmetric, intersectionFunctor>::
  all_codim_0[][2] = {{NULL, NULL}, {NULL, NULL}, {NULL, NULL},
                      {table_any1d_codim_0_interior,
                       table_any1d_codim_0_exterior}, {NULL, NULL},
                      {table_simplex2d_codim_0_interior,
                       table_simplex2d_codim_0_exterior},
                      {table_cube2d_codim_0_interior,
                       table_cube2d_codim_0_exterior},
                      {table_simplex3d_codim_0_interior,
                       table_simplex3d_codim_0_exterior},
                      {table_pyramid3d_codim_0_interior,
                       table_pyramid3d_codim_0_exterior},
                      {table_prism3d_codim_0_interior,
                       table_prism3d_codim_0_exterior}, {NULL, NULL},
                      {table_cube3dsym_codim_0_interior,
                       table_cube3dsym_codim_0_exterior}};

  /*
   * element group tables (e.g. table_cube2d_codim_0_exterior_groups)
   * for different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::symmetric, intersectionFunctor>::
  all_element_groups[][2] = {{NULL, NULL}, {NULL, NULL}, {NULL, NULL},
                             {table_any1d_interior_groups,
                              table_any1d_exterior_groups}, {NULL, NULL},
                             {table_simplex2d_interior_groups,
                              table_simplex2d_exterior_groups},
                             {table_cube2d_interior_groups,
                              table_cube2d_exterior_groups},
                             {table_simplex3d_interior_groups,
                              table_simplex3d_exterior_groups},
                             {table_pyramid3d_interior_groups,
                              table_pyramid3d_exterior_groups},
                             {table_prism3d_interior_groups,
                              table_prism3d_exterior_groups}, {NULL, NULL},
                             {table_cube3dsym_interior_groups,
                              table_cube3dsym_exterior_groups}};

  /*
   * Codimension 1 element tables (e.g. table_cube2d_codim_1) for different
   * types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::symmetric, intersectionFunctor>::
  all_codim_1[] = {NULL, NULL, NULL, table_any1d_codim_1,
                   NULL, table_simplex2d_codim_1,
                   table_cube2d_codim_1, table_simplex3d_codim_1,
                   table_pyramid3d_codim_1, table_prism3d_codim_1, NULL,
                   table_cube3dsym_codim_1};

  /*
   * MC33 offset tables (e.g. table_cube2d_mc33_offsets) for
   * different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::symmetric, intersectionFunctor>::
  all_mc33_offsets[] = {NULL, NULL, NULL, NULL, NULL, NULL,
                        table_cube2d_mc33_offsets, NULL,
                        table_pyramid3d_mc33_offsets,
                        table_prism3d_mc33_offsets, NULL,
                        table_cube3dsym_mc33_offsets};

  /*
   * Test face tables (e.g. table_cube2d_mc33_face_test_order) for
   * different types of elements and dimensions.
   */
  template <typename valueType, int dim, typename thresholdFunctor,
      class intersectionFunctor>
  const short * const
  MarchingCubes33Tables<valueType, dim, thresholdFunctor,
      SymmetryType::symmetric, intersectionFunctor>::
  all_face_tests[] = {NULL, NULL, NULL, NULL, NULL, NULL,
                      table_cube2d_mc33_face_test_order, NULL,
                      table_pyramid3d_mc33_face_test_order,
                      table_prism3d_mc33_face_test_order, NULL,
                      table_cube3dsym_mc33_face_test_order};
}