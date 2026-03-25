cmake_minimum_required(VERSION 3.16)

project(tpmc)

# Search for python intepreter
find_package(Python COMPONENTS Interpreter REQUIRED)

# Call python script to generate lookup table
add_custom_command(
   OUTPUT tpmc_lut.cc
   COMMAND ${Python_EXECUTABLE} generate_lut.py --output ${CMAKE_CURRENT_BINARY_DIR}/tpmc_lut.cc
   WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/tpmc/lut
)

# Build tpmc_tables library
add_library(tpmc_tables STATIC
  tpmc/src/aberthfunctor.cc
  tpmc/src/referenceelements.cc
  tpmc/src/marchingcubestables.cc
  tpmc/src/geometrytype.cc
  tpmc_lut.cc
)
target_include_directories(tpmc_tables PUBLIC tpmc/include/tpmc tpmc/include)

# Add interface library tpmc
add_library(tpmc INTERFACE)
target_link_libraries(tpmc INTERFACE tpmc_tables)
target_include_directories(tpmc INTERFACE tpmc)

# Export targets and generate CMake config file
export(TARGETS tpmc tpmc_tables FILE TpmcConfig.cmake)
