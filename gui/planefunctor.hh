// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __PLANEFUNCTOR_HH__
#define __PLANEFUNCTOR_HH__

template <class FunctorType>
class PlaneFunctor {
public:
  typedef typename FunctorType::CoordType CoordType;
  typedef typename FunctorType::ValueType ValueType;
  typedef Dune::FieldVector<CoordType, 3> VolumeVectorType;
  typedef Dune::FieldVector<CoordType, 2> PlaneVectorType;

  PlaneFunctor(const FunctorType& functor = FunctorType(),
               const VolumeVectorType& position = VolumeVectorType(0),
               const VolumeVectorType& first = VolumeVectorType(0),
               const VolumeVectorType& second = VolumeVectorType(0));
  ValueType operator()(const PlaneVectorType& x) const;
  PlaneVectorType gradient(const PlaneVectorType& x) const;
private:
  FunctorType mFunctor;
  VolumeVectorType mPosition, mFirst, mSecond;
};

template <class FunctorType>
PlaneFunctor<FunctorType>::PlaneFunctor(const FunctorType& functor,
                                        const VolumeVectorType& position,
                                        const VolumeVectorType& first,
                                        const VolumeVectorType& second)
  : mFunctor(functor), mPosition(position), mFirst(first), mSecond(second) {
  // nothing to do here
}

template <class FunctorType>
typename PlaneFunctor<FunctorType>::ValueType PlaneFunctor<FunctorType>::
operator() (const PlaneVectorType& x) const {
  VolumeVectorType u(mPosition), v(mFirst), w(mSecond);
  v *= x[0];
  w *= x[1];
  u += v;
  u += w;
  return mFunctor(u);
}

template <class FunctorType>
typename PlaneFunctor<FunctorType>::PlaneVectorType PlaneFunctor<FunctorType>::
gradient(const PlaneVectorType& x) const {
  VolumeVectorType u(mPosition), v(mFirst), w(mSecond);
  v *= x[0];
  w *= x[1];
  u += v;
  u += w;
  VolumeVectorType g = mFunctor.gradient(u);
  PlaneVectorType result;
  result[0] = mFirst * g;
  result[1] = mSecond * g;
  return result;
}

#endif //__PLANEFUNCTOR_HH__
