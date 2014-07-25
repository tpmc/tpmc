add_custom_command(OUTPUT ${CMAKE_SOURCE_DIR}/dune/marchingcubes/lut/marchinglut.cc
  COMMAND ./generate_lut.py
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/dune/marchingcubes/lut
  DEPENDS ${CMAKE_SOURCE_DIR}/dune/marchingcubes/lut/generate_lut.py)
add_custom_target(generate_lut_target DEPENDS ${CMAKE_SOURCE_DIR}/dune/marchingcubes/lut/marchinglut.cc)

dune_add_library(mclut OBJECT marchinglut.cc)

install(FILES marchinglut.hh DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/marchingcubes/lut/)
