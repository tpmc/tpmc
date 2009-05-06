# Additional checks needed to build the module
AC_DEFUN([DUNE_MC_CHECKS])
# Additional checks needed to find the module
AC_DEFUN([DUNE_MC_CHECK_MODULE], [
  DUNE_CHECK_MODULES([dune-mc], [marchingcubes/marchingcubes.hh], [table_any1d_cases_offsets])
])
