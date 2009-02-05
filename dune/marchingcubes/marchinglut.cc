// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
//#define _MARCHING_LUT_CC_
#include "marchinglut.hh"

extern "C" {

  const char table_cube2d_cases_offsets[][5] = {
    /* vv: vertex values D, C, B, A with 0=in, 1=out
     * cn: case number
     * bc: basic case, if negative it's inverted
     * c1: element count of co-dimension 1 elements
     * o1: table offset for co-dimension 1
     * c0: element count of co-dimension 0 elements
     * o0: table offset for co-dimension 0
     * uniq: whether the case is ambiguous for MC33 */
    /* vv      / cn / bc  /   c1 o1  c0 o0  uniq or  */
    /* 0 0 0 0 /  0 /  0 */ {0,  0, 1,  0, UNIQUE_MC33_CASE},
    /* 0 0 0 1 /  1 /  1 */ {1,  0, 3,  0, UNIQUE_MC33_CASE},
    /* 0 0 1 0 /  2 /  1 */ {1,  3, 3,  0, UNIQUE_MC33_CASE},
    /* 0 0 1 1 /  3 /  2 */ {1,  6, 1,  0, UNIQUE_MC33_CASE},
    /* 0 1 0 0 /  4 /  1 */ {1,  9, 3,  0, UNIQUE_MC33_CASE},
    /* 0 1 0 1 /  5 /  2 */ {1, 12, 1,  0, UNIQUE_MC33_CASE},
    /* 0 1 1 0 /  6 /  3 */ {2, 15, 2,  0, 0},
    /* 0 1 1 1 /  7 / -1 */ {1, 21, 1,  0, UNIQUE_MC33_CASE},
    /* 1 0 0 0 /  8 /  1 */ {1, 21, 3,  0, UNIQUE_MC33_CASE},
    /* 1 0 0 1 /  9 /  3 */ {2, 15, 0,  0, 1},
    /* 1 0 1 0 / 10 /  2 */ {1, 12, 1,  0, UNIQUE_MC33_CASE},
    /* 1 0 1 1 / 11 / -1 */ {1,  9, 1,  0, UNIQUE_MC33_CASE},
    /* 1 1 0 0 / 12 /  2 */ {1,  6, 1,  0, UNIQUE_MC33_CASE},
    /* 1 1 0 1 / 13 / -1 */ {1,  3, 1,  0, UNIQUE_MC33_CASE},
    /* 1 1 1 0 / 14 / -1 */ {1,  0, 1,  0, UNIQUE_MC33_CASE},
    /* 1 1 1 1 / 15 / -0 */ {0,  0, 0,  0, UNIQUE_MC33_CASE},    //TODO: 4. Spalte fertigmachen / übertragen
    /* All cases below this line are ambiguous mc 33 cases */
    /* vv      / cn / bc  /   c1 o1  c0 o0 noUse  / row count*/
    /* 0 1 1 0 /  6 /  3.2 */ {2, 30, 2,  0, 1},    /*  16 */
    /* 1 0 0 1 /  9 /  3.2 */ {2, 36, 0,  0, 2}     /*  17 */
  };

  /*
   * Contains all lines for Cube 2D.
   * The first entry indicates the number of points that belongs
   * to the coming type. In this case only lines are possible.
   *
   * In the middle of square edges are pseudo vertices 5 to 9
   * introduced. Be beware, that these numbers are only valid
   * in this part of the code and doesn't follow any of DUNE's
   * conventions! The square looks like this:
   *  2-6-3
   *  |   |
   *  7   8
   *  |   |
   *  0-5-1
   */
  const char table_cube2d_codim_1[] = {
    /* cn: case numbers
     * bc: basis case
     * co: current offset */
    /* cn     / bc  / types / co  / element count and points */
    /*  0, 15 /   0 /  -    /  0 */ /* no entries for these cases */
    /*  1, 14 /   1 /  2    /  0 */ 2, EJ, EL,
    /*  2, 13 /   1 /  2    /  3 */ 2, EJ, EM,
    /*  3, 12 /   2 /  2    /  6 */ 2, EL, EM,
    /*  4, 11 /   1 /  2    /  9 */ 2, EK, EL,
    /*  5, 10 /   2 /  2    / 12 */ 2, EJ, EK,
    /*  6     / 3.1 /  2, 2 / 15 */ 2, EJ, EM, 2, EK, EL,
    /*  7,  8 /   1 /  2    / 21 */ 2, EK, EM,
    /*  9     / 3.1 /  2, 2 / 24 */ 2, EJ, EL, 2, EK, EM,
    /* All cases below this line are ambiguous mc 33 cases */
    /*  6     / 3.2 / 2, 2 / 30 */ 2, EJ, EL, 2, EK, EM,
    /*  9     / 3.2 / 2, 2 / 36 */ 2, EJ, EM, 2, EK, EL
  };

  /*
   * Contains all lines for Cube 2D.
   * The first entry indicates the number of points that belongs
   * to the coming type. In this case only lines are possible.
   *
   * In the middle of square edges are pseudo vertices 5 to 9
   * introduced. Be beware, that these numbers are only valid
   * in this part of the code and doesn't follow any of DUNE's
   * conventions! The square looks like this:
   *  2-6-3
   *  |   |
   *  7   8
   *  |   |
   *  0-5-1char
   */
  const char table_cube2d_codim_0[] = {
    /* case number / types / entry count */
    /*  0 / 4       /  0 */ 4, 0, 1, 2, 3,
    /*  1 / 3, 3, 3 /  1 */ 3, 1, 3, 2, 3, 1, 2, 7, 3, 1, 7, 5,
    /*  2 / 3, 3, 3 /  1 */ 3, 0, 3, 2, 3, 0, 8, 3, 3, 0, 5, 8,
    /*  3 / 4       /  1 */ 4,   /* usw usf TODO: fertigstellen*/
    /*  4 / 3, 3, 3 /  1 */ 3,
    /*  5 / 4       /  1 */ 4,
    /*  6 / 3, 3, 4 /  1 */ 3, 0, 5, 7, 3, 3, 6, 8, 4, 5, 8, 7, 6,
    /*  7 / 3       /  1 */ 3,
    /*  8 / 3, 3, 3 /  1 */ 3,
    /*  9 / 3, 3, 4 /  1 */ 3, 1, 8, 5, 3, 2, 7, 6, 4, 5, 8, 7, 6,
    /* 10 / 4       /  1 */ 4,
    /* 11 / 3       /  1 */ 3,
    /* 12 / 4       /  1 */ 4,
    /* 13 / 3       /  1 */ 3,
    /* 14 / 3       /  1 */ 3,
    /* 15 / -       /  1 */ /* no entries for this case */

    // below this line are only MC 33 cases TODO: anpassen
    /* case number / basic case / types / entry count */
    /* 6 / 3.2 / 3, 3 / 0 */ 3, VA, EJ, EL, 3, VD, EK, EM,
    /* 9 / 3.2 / 3, 3 / 8 */ 3, VB, EM, EJ, 3, VC, EL, EK
  };

  /*
   * TODO: Kommentar (diese Tabelle gibt den Index an, an der in table_cube2d_mc33_face_test_order
   * weitergemacht werden muss)
   */
  const char table_cube2d_mc33_offsets[] = {
    /* case number / basic case / row / offset / notInverted */
    /* 6 / 3 / 0 */ 1, 1,
    /* 9 / 3 / 1 */ 4, 0
  };

  /*
   * TODO: Kommentar (diese Tabelle gibt an, welche Faces getestet werden müssen. Negative
   * Zahlen sind Face-Tests (Nummerierung Dune-typisch), 0 ist Test Zentrum, positive Zahlen
   * sind Zeilennummern in table_cube2d_cases_offsets)
   */
  const short table_cube2d_mc33_face_test_order[] = {
    /* dummy entry, not used, but the index should start with 1*/
    1,
    /* case number 6, basis case 3.1 or 3.2, offset 1 */
    -1, 6, 16,
    /* case number 9, basis case 3.1 or 3.2, offset 4 */
    -1, 9, 17
  };
}
