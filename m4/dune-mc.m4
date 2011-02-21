# Additional checks needed to build the module
AC_DEFUN([DUNE_MC_CHECKS], [
  AM_PATH_PYTHON(,,[AC_MSG_ERROR([Python required])])
  
  duneMCCheckPyModule ()
  {
    $PYTHON 2> /dev/null <<EOF
import $[]1
EOF
  return $?
  }

  for M in math pprint pyvtk; do
    AC_MSG_CHECKING([for python module [$M]])
    AS_IF([(duneMCCheckPyModule [$M])],
      [ AC_MSG_RESULT([yes])],
      [ AC_MSG_RESULT([no]) 
        AC_MSG_ERROR([Required python module [$M] not found])
      ])
  done
])
# Additional checks needed to find the module
AC_DEFUN([DUNE_MC_CHECK_MODULE], [
  DUNE_CHECK_MODULES([dune-mc], [marchingcubes/marchingcubes.hh], [table_any1d_cases_offsets])
])
