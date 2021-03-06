// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
/*
 * This file contains the lookup tables for marching cubes' algorithms
 * for the 1D, 2D and 3D cases along with their marching cubes' 33 tables for
 * ambiguous cases.
 *
 * == Names for vertices and edges ==
 * For every vertex exists a constant begining with V and followed
 * by second big letter according to its name. Edges are named with
 * a G and a following big letter, too.
 * Here is the naming scheme for a square and a cube. Lines,
 * triangles and tetrahedrons follow this scheme. They always
 * contain vertex A and edge I.
 *
 * Square:
 *
 * C--J--D
 * |     |
 * K     L
 * |     |
 * A--I--B
 *
 * Cube:
 *         G ________ H           _____R__
 *         /|       /|          /|       /|
 *       /  |     /  |       S/  |     /T |
 *   E /_______ /    |    E /__Q____ /    P
 *    |     |  |F    |     |     O  |     |
 *    |    C|__|_____|D    |     |__|__J__|
 *    |    /   |    /      M   K/   N    /
 *    |  /     |  /        |  /     |  /L
 *    |/_______|/          |/___I___|/    Cube center: Z
 *   A          B         A          B
 *
 * Simplex:
 * Vertices: [A,B,C,E]
 *
 * Pyramid:
 * Vertices: [A,B,C,D,E], (A,B,C,D) form the bottom square-face
 *
 * Prism:
 * Vertices: [A,B,C,E,F,G], (A,B,C) and (E,F,G) form the two triangular faces
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
static const short NO_VERTEX = 1<<8;
static const short VERTEX_GO_RIGHT = 1;     // x1 = 1
static const short VERTEX_GO_DEPTH = 2;     // x2 = 1
static const short VERTEX_GO_UP = 4;     // x3 = 1
static const short FACTOR_FIRST_POINT = 1;
static const short FACTOR_SECOND_POINT = 16;
// vertices start with V
static const short VA = 0;
static const short VB = VERTEX_GO_RIGHT;
static const short VC = VERTEX_GO_DEPTH;
static const short VD = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH;
static const short VE = VERTEX_GO_UP;
static const short VF = VERTEX_GO_RIGHT + VERTEX_GO_UP;
static const short VG = VERTEX_GO_DEPTH + VERTEX_GO_UP;
static const short VH = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP;
// faces
static const short FA = VH + 1;
static const short FB = VH + 2;
static const short FC = VH + 3;
static const short FD = VH + 4;
static const short FE = VH + 5;
static const short FF = VH + 6;
// center
static const short CA = FF + 1;
static const short CB = FF + 2;
static const short CC = FF + 3;
static const short CD = FF + 4;
static const short CE = FF + 5;
static const short CF = FF + 6;
// root
static const short RA = CF + 1;
static const short RB = CF + 2;
static const short RC = CF + 3;
static const short RD = CF + 4;
static const short RE = CF + 5;
static const short RF = CF + 6;

// the number of different vertices defined above (assuming ascending continuous order)
static const short VERTICES_ON_REFERENCE_COUNT = RF+1;

/* Constants indicating whether case special treatment when marching cubes' 33 is used. */
static const short CASE_UNIQUE_MC33 = 0;
static const short CASE_AMBIGUOUS_MC33 = 1;
/* Face tests */
/* \todo could lead to problems if index is a valid index of the offset table */
static const short CASE_IS_REGULAR = (1<<8);
static const short TEST_FACE = (1<<9);
static const short TEST_INTERIOR = (1<<10);
static const short TEST_INVALID = (1<<11);
static const short TEST_FACE_FLIP = 8;
static const short TEST_FACE_0_0 = -(TEST_FACE | 0);
static const short TEST_FACE_1_0 = -(TEST_FACE | 1);
static const short TEST_FACE_2_0 = -(TEST_FACE | 2);
static const short TEST_FACE_3_0 = -(TEST_FACE | 3);
static const short TEST_FACE_4_0 = -(TEST_FACE | 4);
static const short TEST_FACE_5_0 = -(TEST_FACE | 5);
static const short TEST_FACE_0_1 = -(TEST_FACE | TEST_FACE_FLIP | 0);
static const short TEST_FACE_1_1 = -(TEST_FACE | TEST_FACE_FLIP | 1);
static const short TEST_FACE_2_1 = -(TEST_FACE | TEST_FACE_FLIP | 2);
static const short TEST_FACE_3_1 = -(TEST_FACE | TEST_FACE_FLIP | 3);
static const short TEST_FACE_4_1 = -(TEST_FACE | TEST_FACE_FLIP | 4);
static const short TEST_FACE_5_1 = -(TEST_FACE | TEST_FACE_FLIP | 5);
static const short TEST_INTERIOR_0_0 = -(TEST_INTERIOR | (0 << 3) | 0);
static const short TEST_INTERIOR_1_0 = -(TEST_INTERIOR | (1 << 3) | 0);
static const short TEST_INTERIOR_2_0 = -(TEST_INTERIOR | (2 << 3) | 0);
static const short TEST_INTERIOR_3_0 = -(TEST_INTERIOR | (3 << 3) | 0);
static const short TEST_INTERIOR_0_2 = -(TEST_INTERIOR | (0 << 3) | 2);
static const short TEST_INTERIOR_1_2 = -(TEST_INTERIOR | (1 << 3) | 2);
static const short TEST_INTERIOR_2_2 = -(TEST_INTERIOR | (2 << 3) | 2);
static const short TEST_INTERIOR_3_2 = -(TEST_INTERIOR | (3 << 3) | 2);
static const short TEST_INTERIOR_0_4 = -(TEST_INTERIOR | (0 << 3) | 4);
static const short TEST_INTERIOR_1_4 = -(TEST_INTERIOR | (1 << 3) | 4);
static const short TEST_INTERIOR_2_4 = -(TEST_INTERIOR | (2 << 3) | 4);
static const short TEST_INTERIOR_3_4 = -(TEST_INTERIOR | (3 << 3) | 4);

/* Indices for access to cube2d_case_offsets */
static const int INDEX_OFFSET_CODIM_0[] = {3, 0};
static const int INDEX_OFFSET_ELEMENT_GROUPS[] = {4, 1};
static const int INDEX_COUNT_CODIM_0[] = {5, 2};
static const int INDEX_OFFSET_CODIM_1 = 6;
static const int INDEX_COUNT_CODIM_1 = 7;
static const int INDEX_VERTEX_GROUPS = 8;
static const int INDEX_COMPLEX_VERTICES = 9;
static const int INDEX_UNIQUE_CASE = 10;

/* Mappings for vertex number to linear index in value array */
static const short table_any0d_vertex_to_index[] = {0};
static const short table_any1d_vertex_to_index[] = {0,1};
static const short table_simplex2d_vertex_to_index[] = {0,1,2};
static const short table_cube2d_vertex_to_index[] = {0,1,2,3};
static const short table_simplex3d_vertex_to_index[] = {0,1,2,0,3};
static const short table_pyramid3d_vertex_to_index[] = {0,1,2,3,4};
static const short table_prism3d_vertex_to_index[] = {0,1,2,0,3,4,5};
static const short table_cube3d_vertex_to_index[] = {0,1,2,3,4,5,6,7};

#ifndef _MARCHING_LUT_CC_

extern "C"
{

  extern const int table_cube2d_max_complex_vertex_count;

  extern const short table_cube2d_vertices[];
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
  extern const unsigned short table_cube2d_cases_offsets[][11];
  extern const short table_cube2d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_cube2d_vertex_groups[];

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
  extern const short table_cube2d_codim_0_exterior[];
  /*
   * TODO: Comment
   */
  extern const short table_cube2d_codim_0_interior[];
  /*
   * TODO: Comment
   */
  extern const short table_cube2d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_cube2d_interior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_cube2d_mc33_offsets[];
  extern const short table_cube2d_mc33_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_cube2d_mc33_face_test_order[];

  extern const int table_cube3d_max_complex_vertex_count;

  extern const short table_cube3d_vertices[];
  /*
   * TODO: Comment 3D cube
   */
  extern const unsigned short table_cube3d_cases_offsets[][11];
  extern const short table_cube3d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_cube3d_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_codim_1[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_mc33_offsets[];
  extern const short table_cube3d_mc33_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3d_mc33_face_test_order[];

  extern const int table_cube3dsym_max_complex_vertex_count;

  extern const short table_cube3dsym_vertices[];
  /*
   * TODO: Comment 3D cube
   */
  extern const unsigned short table_cube3dsym_cases_offsets[][11];
  extern const short table_cube3dsym_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_codim_1[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_mc33_offsets[];
  extern const short table_cube3dsym_mc33_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_cube3dsym_mc33_face_test_order[];

  extern const int table_simplex2d_max_complex_vertex_count;

  extern const short table_simplex2d_vertices[];
  /*
   * TODO: Comment 2D simplex
   */
  extern const unsigned short table_simplex2d_cases_offsets[][11];
  extern const short table_simplex2d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex2d_codim_1[];

  extern const int table_simplex3d_max_complex_vertex_count;

  extern const short table_simplex3d_vertices[];
  /*
   * TODO: Comment 3D simplex
   */
  extern const unsigned short table_simplex3d_cases_offsets[][11];
  extern const short table_simplex3d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_simplex3d_codim_1[];

  extern const int table_pyramid3d_max_complex_vertex_count;

  extern const short table_pyramid3d_vertices[];
  /*
   * TODO: Comment 3D pyramid
   */
  extern const unsigned short table_pyramid3d_cases_offsets[][11];
  extern const short table_pyramid3d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_codim_1[];

  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_mc33_offsets[];
  extern const short table_pyramid3d_mc33_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_pyramid3d_mc33_face_test_order[];

  extern const int table_prism3d_max_complex_vertex_count;

  extern const short table_prism3d_vertices[];
  /*
   * TODO: Comment 3D prism
   */
  extern const unsigned short table_prism3d_cases_offsets[][11];
  extern const short table_prism3d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_prism3d_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_prism3d_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_prism3d_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_prism3d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_prism3d_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_prism3d_codim_1[];

  /*
   * TODO: Comment
   */
  extern const short table_prism3d_mc33_offsets[];
  extern const short table_prism3d_mc33_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_prism3d_mc33_face_test_order[];

  extern const int table_any0d_max_complex_vertex_count;

  extern const short table_any0d_vertices[];
  /*
   * TODO: Comment
   */
  extern const unsigned short table_any0d_cases_offsets[][11];
  extern const short table_any0d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_any0d_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_any0d_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_any0d_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_any0d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_any0d_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_any0d_codim_1[];

  extern const int table_any1d_max_complex_vertex_count;

  extern const short table_any1d_vertices[];
  /*
   * TODO: Comment
   */
  extern const unsigned short table_any1d_cases_offsets[][11];
  extern const short table_any1d_complex_vertices[];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_vertex_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_codim_0_exterior[];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_codim_0_interior[];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_exterior_groups[];
  /*
   * TODO: Comment
   */
  extern const short table_any1d_interior_groups[];

  /*
   * TODO: Comment
   */
  extern const short table_any1d_codim_1[];

} // extern "C"

#endif // _MARCHING_LUT_CC_

#endif // MARCHING_LUT
