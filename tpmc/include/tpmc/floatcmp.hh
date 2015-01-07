#ifndef TPMC_FLOATCMP_HH
#define TPMC_FLOATCMP_HH

#include <limits>

namespace tpmc
{
  namespace FloatCmp
  {
    template <class T>
    struct DefaultEpsilon
    {
      static T value;
    };
    template <class T>
    T DefaultEpsilon<T>::value = std::numeric_limits<T>::epsilon() * 8;

    template <class T>
    static bool eq(T a, T b) {
      return std::abs(a-b) <= DefaultEpsilon<T>::value * std::max(std::abs(a), std::abs(b));
    }

    template <class T>
    static bool ne(T a, T b) {
      return ! eq(a,b);
    }

    template <class T>
    static bool lt(T a, T b) {
      return a < b && ne(a,b);
    }

    template <class T>
    static bool gt(T a, T b) {
      return a > b && ne(a,b);
    }

    template <class T>
    static bool le(T a, T b) {
      return a<b || eq(a,b);
    }

    template <class T>
    static bool ge(T a, T b) {
      return a>b || eq(a,b);
    }
  };
}

#endif // TPMC_FLOATCMP_HH
