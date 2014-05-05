// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __ORIGINCENTEREDCAMERA_HH__
#define __ORIGINCENTEREDCAMERA_HH__

#include <GL/glu.h>

class OriginCenteredCamera {
public:
  typedef Dune::FieldVector<double, 3> VectorType;

  OriginCenteredCamera();
  void rotateRight(double angle);
  void rotateUp(double angle);
  void zoom(double step);
  double getDist() const { return mDist; }
  void apply();
  void reset();
private:
  void update();
  double mTheta, mPhi, mDist;
  VectorType mEye, mUp;
};

OriginCenteredCamera::OriginCenteredCamera()
  : mTheta(0), mPhi(0), mDist(2.5), mEye(0), mUp(0) {
  update();
}

void OriginCenteredCamera::reset() {
  mTheta = mPhi = 0;
  mDist = 2;
  update();
}

// first rotate around x, then around y
void OriginCenteredCamera::update() {
  mEye[0] = std::sin(mTheta)*std::cos(mPhi);
  mEye[1] = std::sin(mPhi);
  mEye[2] = std::cos(mTheta)*std::cos(mPhi);
  mUp[0] = -std::sin(mTheta)*std::sin(mPhi);
  mUp[1] = std::cos(mPhi);
  mUp[2] = -std::cos(mTheta)*std::sin(mPhi);
  mEye *= mDist;
}

void OriginCenteredCamera::rotateRight(double angle) {
  mTheta += angle;
  while (mTheta < 0)
    mTheta += 2.f*M_PI;
  while (mTheta > 2.f*M_PI)
    mTheta -= 2.f*M_PI;
  update();
}

void OriginCenteredCamera::rotateUp(double angle) {
  mPhi += angle;
  while (mPhi < 0)
    mPhi += 2.f*M_PI;
  while (mPhi > 2.f*M_PI)
    mPhi -= 2.f*M_PI;
  update();
}

void OriginCenteredCamera::zoom(double step) {
  if (mDist >= 0) {
    mDist += step;
    update();
  }
}

void OriginCenteredCamera::apply() {
  gluLookAt(mEye[0], mEye[1], mEye[2],
            0.f, 0.f, 0.f,
            mUp[0], mUp[1], mUp[2]);
}

#endif //__ORIGINCENTEREDCAMERA_HH__
