// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __TRILINEARFUNCTOR_HH__
#define __TRILINEARFUNCTOR_HH__

template <typename ctype, typename vtype>
class TrilinearFunctor {
public:
  typedef vtype ValueType;
  typedef ctype CoordType;

  template <class V>
  TrilinearFunctor(V values);
  ValueType operator()(const Dune::FieldVector<ctype, 3>& x) const;
  Dune::FieldVector<ctype, 3> gradient(const Dune::FieldVector<ctype, 3>& x) const;
private:
  ValueType mVertexValues[8];
};

template <typename ctype, typename vtype>
template <class V>
TrilinearFunctor<ctype, vtype>::TrilinearFunctor(V values) {
  std::copy(values.begin(), values.end(), mVertexValues);
}

template <typename ctype, typename vtype>
typename TrilinearFunctor<ctype, vtype>::ValueType TrilinearFunctor<ctype, vtype>::operator()(const Dune::FieldVector<ctype, 3>& x) const {
  return x[0]*(x[1]*(x[2]*mVertexValues[7]+(1-x[2])*mVertexValues[3]) +
               (1-x[1])*(x[2]*mVertexValues[5]+(1-x[2])*mVertexValues[1])) +
         (1-x[0])*(x[1]*(x[2]*mVertexValues[6]+(1-x[2])*mVertexValues[2])+
                   (1-x[1])*(x[2]*mVertexValues[4]+(1-x[2])*mVertexValues[0]));
}

template <typename ctype, typename vtype>
Dune::FieldVector<ctype, 3> TrilinearFunctor<ctype, vtype>::gradient(const Dune::FieldVector<ctype, 3>& x) const {
  Dune::FieldVector<vtype, 3> v;
  v[0] = x[1]*(x[2]*(mVertexValues[7]-mVertexValues[6])+(1-x[2])*(mVertexValues[3]-mVertexValues[2]))
         + (1-x[1])*(x[2]*(mVertexValues[5]-mVertexValues[4])+(1-x[2])*(mVertexValues[1]-mVertexValues[0]));
  v[1] = x[0]*(x[2]*(mVertexValues[7]-mVertexValues[5])+(1-x[2])*(mVertexValues[3]-mVertexValues[1]))
         + (1-x[0])*(x[2]*(mVertexValues[6]-mVertexValues[4])+(1-x[2])*(mVertexValues[2]-mVertexValues[0]));
  v[2] = x[0]*(x[1]*(mVertexValues[7]-mVertexValues[3])+(1-x[1])*(mVertexValues[5]-mVertexValues[1]))
         + (1-x[0])*(x[1]*(mVertexValues[6]-mVertexValues[2])+(1-x[1])*(mVertexValues[4]-mVertexValues[0]));
  return v;
}


#endif //__TRILINEARFUNCTOR_HH__
