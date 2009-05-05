// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
/*
 * This file contains the lookup tables for marching cubes' algorithms
 * for the 1D and 2D cases. The 2D case has additional tables for the
 * Marching Cubes' 33 algorithm.
 *
 * == Names for vertices and edges ==
 * For every vertex exists a constant begining with V and followed
 * by second big letter according to its name. Edges are named with
 * a G and a following big letter, too.
 * Here is the naming scheme for a square and a cube. Lines,
 * triangles and tetrahedrons follow this scheme. They always
 * contain vertex A and edge J.
 *
 * Square:
 *
 * C--K--D
 * |     |
 * L     M
 * |     |
 * A--J--B
 *
 * Cube:
 *         G ________ H           _____S__
 *         /|       /|          /|       /|
 *       /  |     /  |       T/  |     /U |
 *   E /_______ /    |    E /__R____ /    Q
 *    |     |  |F    |     |     P  |     |
 *    |    C|__|_____|D    |     |__|__K__|
 *    |    /   |    /      N   L/   O    /
 *    |  /     |  /        |  /     |  /M
 *    |/_______|/          |/___J___|/    Cube center: V
 *   A          B         A          B
 *
 *
 * To describe vertices and edges of lines, triangles, squares,
 * terahedrons and cubes every element has its own number.
 * - The number is even if it is a vertex.
 * - The number is uneven otherwise (edge, center of element).
 * - One vertex number is stored in the three bits 2, 3, 4. The
 *   three bits are enough to distinguish 8 vertices, sufficient
 *   for all elements including cubes.
 * - For edges the second vertex is stored in the next three bits
 *   5, 6, and 7.
 * - If the two stored vertices are on diametral vertices the center
 *   of the element is stored. It needs more than two vertices.
 * NB: the bit counting used here is the least value bit is 1.
 */

#ifndef MARCHING_LUT
#define MARCHING_LUT

// constants for vertex and edge numbering
static const short NO_VERTEX = 1<<6;
static const short VERTEX_GO_RIGHT = 1;     // x1 = 1
static const short VERTEX_GO_DEPTH = 2;     // x2 = 1
static const short VERTEX_GO_UP = 4;     // x3 = 1
static const short FACTOR_FIRST_POINT = 1;
static const short FACTOR_SECOND_POINT = 8;
// vertices start with V
static const short VA = 0;
static const short VB = VERTEX_GO_RIGHT;
static const short VC = VERTEX_GO_DEPTH;
static const short VD = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH;
static const short VE = VERTEX_GO_UP;
static const short VF = VERTEX_GO_RIGHT + VERTEX_GO_UP;
static const short VG = VERTEX_GO_DEPTH + VERTEX_GO_UP;
static const short VH = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP;
// edges start with E
static const short EJ = VA * FACTOR_FIRST_POINT + VB * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EK = VC * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EL = VA * FACTOR_FIRST_POINT + VC * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EM = VB * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EN = VA * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EO = VB * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EP = VC * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EQ = VD * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;
static const short ER = VE * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX;
static const short ES = VG * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;
static const short ET = VE * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EU = VF * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EV = VB * FACTOR_FIRST_POINT + VC * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EW = VB * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX;
static const short EX = VC * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX;
// Center point is in the center of a cube or tetrahedron
static const short EY = VA * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;

/* Constants indicating whether case special treatment when marching cubes' 33 is used. */
static const short CASE_UNIQUE_MC33 = 0;
static const short CASE_AMBIGUOUS_MC33 = 1;
/* Face tests */
static const short CASE_IS_REGULAR = (1<<8);
static const short TEST_FACE = (1<<9);
static const short TEST_INTERIOR = (1<<10);
static const short TEST_INVALID = (1<<11);
static const short TEST_FACE_0 = -(TEST_FACE | 0);
static const short TEST_FACE_1 = -(TEST_FACE | 1);
static const short TEST_FACE_2 = -(TEST_FACE | 2);
static const short TEST_FACE_3 = -(TEST_FACE | 3);
static const short TEST_FACE_4 = -(TEST_FACE | 4);
static const short TEST_FACE_5 = -(TEST_FACE | 5);
static const short TEST_CENTER = -(TEST_INTERIOR | 0); // DEPRECATED
static const short TEST_INTERIOR_0 = -(TEST_INTERIOR | 0);
static const short TEST_INTERIOR_1 = -(TEST_INTERIOR | 1);
static const short TEST_INTERIOR_2 = -(TEST_INTERIOR | 2);
static const short TEST_INTERIOR_3 = -(TEST_INTERIOR | 3);

/* Indices for access to cube2d_case_offsets */
static const int INDEX_OFFSET_CODIM_0 = 0;
static const int INDEX_COUNT_CODIM_0 = 1;
static const int INDEX_OFFSET_CODIM_1 = 2;
static const int INDEX_COUNT_CODIM_1 = 3;
static const int INDEX_UNIQUE_CASE = 4;

#ifndef _MARCHING_LUT_CC_

extern "C"
{
  /*
   * Lookup table for 2D cases. The first entry is the offset
   * for
   * The number of the marching cubes' case is calculated by
   * case = 0;
   * for (i=0; i<4; i++) {
   *   case += vertex * 2^vertex-number
   * }
   * with vertex is 1 if it's value is inside and 0 otherwise.
   *
   * There are four basic cases: (vertices D, C, B, A)
   * Basic case 0: 0 0 0 0
   * Basic case 1: 0 0 0 1
   * Basic case 2: 0 0 1 1
   * Basic case 3: 0 1 0 1
   */
  extern const short table_cube2d_cases_offsets[][5];

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
  extern const short table_cube2d_codim_1[];

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
  extern const short table_cube2d_codim_0[];

  /*
   * TODO: Comment
   */
  extern const short table_cube2d_mc33_offsets[];

  /*
   * TODO: Comment
   */
  extern const short table_cube2d_mc33_face_test_order[];

  /*
   * TODO: Comment 3D cube
   */
  extern const short table_cube3d_cases_offsets[][5];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_codim_0[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_codim_1[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_mc33_offsets[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_mc33_face_test_order[];

  /*
   * TODO: Comment 2D simplex
   */
  extern const short table_simplex2d_cases_offsets[][5];

  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_codim_0[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_codim_1[];

  /*
   * TODO: Comment 3D simplex
   */
  extern const short table_simplex3d_cases_offsets[][5];

  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_codim_0[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_codim_1[];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_cases_offsets[][5];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_codim_0[];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_codim_1[];

} // extern "C"

#endif // _MARCHING_LUT_CC_

#endif // MARCHING_LUT
