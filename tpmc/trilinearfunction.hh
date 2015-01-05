// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __TRILINEARFUNCTION_HH__
#define __TRILINEARFUNCTION_HH__

#include <dune/common/fvector.hh>

namespace Dune {
  template <typename ValueType>
  class TrilinearFunction {
    typedef double ctype;
    typedef std::size_t SizeType;
  public:
    typedef Dune::FieldVector<ctype, 3> PointType;

    template <class ValueVector>
    static ValueType evaluate(const ValueVector& vertex_values,
                              const PointType& x);

    template <class ValueVector>
    static void gradient(const ValueVector& vertex_values,
                         const PointType& x,
                         PointType& result);
  };

  template <typename ValueType>
  template <class ValueVector>
  ValueType TrilinearFunction<ValueType>::evaluate(const ValueVector& vertex_values,
                                                   const PointType& x) {
    return (1-x[0])*(1-x[1])*(1-x[2])*vertex_values[0]
           + x[0]*(1-x[1])*(1-x[2])*vertex_values[1]
           + (1-x[0])*x[1]*(1-x[2])*vertex_values[2]
           + x[0]*x[1]*(1-x[2])*vertex_values[3]
           + (1-x[0])*(1-x[1])*x[2]*vertex_values[4]
           + x[0]*(1-x[1])*x[2]*vertex_values[5]
           + (1-x[0])*x[1]*x[2]*vertex_values[6]
           + x[0]*x[1]*x[2]*vertex_values[7];
  }

  template <typename ValueType>
  template <class ValueVector>
  void TrilinearFunction<ValueType>::gradient(const ValueVector& vertex_values,
                                              const PointType& x,
                                              PointType& result) {
    result[0] = (1-x[1])*(1-x[2])*(vertex_values[1]-vertex_values[0])
                + x[1]*(1-x[2])*(vertex_values[3]-vertex_values[2])
                + (1-x[1])*x[2]*(vertex_values[5]-vertex_values[4])
                + x[1]*x[2]*(vertex_values[7]-vertex_values[6]);
    result[1] = (1-x[0])*(1-x[2])*(vertex_values[2]-vertex_values[0])
                + x[0]*(1-x[2])*(vertex_values[3]-vertex_values[1])
                + (1-x[0])*x[2]*(vertex_values[6]-vertex_values[4])
                + x[0]*x[2]*(vertex_values[7]-vertex_values[5]);
    result[2] = (1-x[0])*(1-x[1])*(vertex_values[4]-vertex_values[0])
                + x[0]*(1-x[1])*(vertex_values[5]-vertex_values[1])
                + (1-x[0])*x[1]*(vertex_values[6]-vertex_values[2])
                + x[0]*x[1]*(vertex_values[7]-vertex_values[3]);
  }
}

#endif //__TRILINEARFUNCTION_HH__
