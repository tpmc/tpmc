#ifndef TPMC_FIELDTRAITS_HH
#define TPMC_FIELDTRAITS_HH

#include <vector>

namespace tpmc {
  template <class T>
  struct FieldTraits;

  template <class T>
  struct FieldTraits<std::vector<T> > {
    typedef T field_type;
  };
}

#endif // TPMC_FIELDTRAITS_HH
