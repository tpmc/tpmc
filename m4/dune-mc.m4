# Additional checks needed to build the module
AC_DEFUN([DUNE_MC_CHECKS])
# Additional checks needed to find the module
AC_DEFUN([DUNE_MC_CHECK_MODULE], [
  DUNE_CHECK_MODULES([dune-mc], [dune/marchingcube/marchingcube.hh])
])
