set(NORMALTESTS)

list(APPEND NORMALTESTS test_mc33)
add_executable(test_mc33 test_mc33.cc)
target_link_libraries(test_mc33 ${DUNE_LIBS})

list(APPEND NORMALTESTS testmc33)
add_executable(testmc33 testmc33.cc)
target_link_libraries(testmc33 ${DUNE_LIBS})

list(APPEND NORMALTESTS testmarchingcubesnormals)
add_executable(testmarchingcubesnormals testmarchingcubesnormals.cc)
target_link_libraries(testmarchingcubesnormals ${DUNE_LIBS})

list(APPEND NORMALTESTS testmarchingcubesrefinement)
add_executable(testmarchingcubesrefinement testmarchingcubesrefinement.cc)
target_link_libraries(testmarchingcubesrefinement ${DUNE_LIBS})

foreach(i ${NORMALTESTS})
  add_test(${i} ${i})
  add_dune_alugrid_flags(${i})
  add_dune_ug_flags(${i})
  if(SUPERLU_FOUND)
    add_dune_superlu_flags(${i})
  endif(SUPERLU_FOUND)
endforeach(i ${NORMALTESTS})

add_directory_test_target(_test_target)
add_dependencies(${_test_target} ${NORMALTESTS})
