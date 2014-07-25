dune_add_library(dunemc
  _DUNE_TARGET_OBJECTS:mclut_
  ADD_LIBS ${DUNE_LIBS})
set_source_files_properties(${CMAKE_SOURCE_DIR}/dune/marchingcubes/lut/marchinglut.cc
  PROPERTIES GENERATED TRUE)
add_dependencies(dunemc generate_lut_target)
