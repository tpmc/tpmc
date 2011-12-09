from generator import *
from permutation import *

# this file contains the triangulations for the marching-cubes base cases generated
# by the LookupGenerators init-method.
# geometries: (3,"cube"), (3,"simplex"), (2,"cube"), (2,"simplex"), (1,"any"), (0,"any")

# test are according to:
# test_faces: TEST | OUTSIDE | INSIDE
# test_inter: TEST | ref connected | ref not connected
# where test | true | false

# Constants for permutate mc 33 cases
MIRROR_FACES_0_TO_1 = Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6))
MIRROR_FACES_0_TO_2 = Permutation(-1, (0, 2, 1, 3, 4, 6, 5, 7))
MIRROR_FACES_0_TO_4 = Permutation(-1, (0, 4, 2, 6, 1, 5, 3, 7))
ROTATE_FACES_0_2_4 = Permutation(1, (0, 2, 4, 6, 1, 3, 5, 7))
ROTATE_FACES_0_2_5 = Permutation(1, (5, 7, 1, 3, 4, 6, 0, 2))
ROTATE_FACES_0_3_5 = Permutation(1, (5, 1, 4, 0, 7, 3, 6, 2))
ROTATE_FACES_1_2_5 = Permutation(1, (6, 4, 2, 0, 7, 5, 3, 1))
ROTATE_FACES_0_1 = Permutation(1, (4, 5, 0, 1, 6, 7, 2, 3))

################################################################################
## 3D Cube                                                                    ##
################################################################################
BCTcube3d = LookupGenerator(3,"cube")
BCTcube3d.print_info()
# base cases cube 3D:
# 0,0,0,0,0,0,0,0 -> 00000000 # Basic Case 0
BCTcube3d.base_cases[0].name = "MC33 Case 0"
BCTcube3d.base_cases[0].faces = []
BCTcube3d.base_cases[0].exterior = []
BCTcube3d.base_cases[0].interior = [[0, 1, 2, 3, 4, 5, 6, 7]]
# 1,0,0,0,0,0,0,0 -> 00000001 # Basic Case 1
BCTcube3d.base_cases[1].name = "MC33 Case 1"
BCTcube3d.base_cases[1].faces = [[(0, 4), (0, 1), (0, 2)]]
BCTcube3d.base_cases[1].exterior = [[0, (0, 4), (0, 1), (0, 2)]]
BCTcube3d.base_cases[1].interior = [[(0, 4), (0, 1), (0, 2), 4, 1, 2], [1, 4, 5, (0, 7)], [1, 2, 4, (0, 7)], [2, 6, 4, (0, 7)], [1, 2, 3, (0, 7)], [4, 5, 6, 7, (0, 7)], [1, 3, 5, 7, (0, 7)], [2, 3, 6, 7, (0, 7)]]
# 1,1,0,0,0,0,0,0 -> 00000011 # Basic Case 2
BCTcube3d.base_cases[2].name = "MC33 Case 2"
BCTcube3d.base_cases[2].faces = [[(0, 2), (1, 3), (0, 4), (1, 5)]]
BCTcube3d.base_cases[2].exterior = [[0, (0, 2), (0, 4), 1, (1, 3), (1, 5)]]
BCTcube3d.base_cases[2].interior = [[(0, 2), (1, 3), (0, 4), (1, 5), 2, 3, 4, 5], [2, 4, 6, 3, 5, 7]]
# 0,1,1,0,0,0,0,0 -> 00000110 # Basic Case 3
BCTcube3d.base_cases[3].name = "MC33 Case 3.1"
BCTcube3d.base_cases[3].faces = [[(1, 5), (0, 1), (1, 3)], [(2, 3), (0, 2), (2, 6)]]
BCTcube3d.base_cases[3].exterior = [[1, (1, 5), (0, 1), (1, 3)], [2, (2, 3), (0, 2), (2, 6)]]
BCTcube3d.base_cases[3].interior = [[(1, 5), (0, 1), (1, 3), 5, 0, 3], [(2, 3), (0, 2), (2, 6), 3, 0, 6], [5, 6, 7, 3], [0, 3, 5, 6], [0, 4, 5, 6]]
# 1,1,1,0,0,0,0,0 -> 00000111 # Basic Case 4
BCTcube3d.base_cases[4].name = "MC33 Case 5"
BCTcube3d.base_cases[4].faces = [[(0, 4), (1, 5), (2, 6)], [(1, 5), (2, 6), (1, 3), (2, 3)]]
BCTcube3d.base_cases[4].exterior = [[0, 1, 2, (0, 4), (1, 5) , (2, 6)], [1, (1, 3), (1, 5), 2, (2, 3), (2, 6)]]
BCTcube3d.base_cases[4].interior = [[(0, 4), (1, 5), (2, 6), 4, 5, 6], [(1, 5), 3, (2, 6), 5, 7, 6], [(1, 3), (1, 5), (2, 3), (2, 6), 3]]
# 1,1,1,1,0,0,0,0 -> 00001111 # Basic Case 5 and its inverse
BCTcube3d.base_cases[5].name = "MC33 Case 8"
BCTcube3d.base_cases[5].faces = [[(0, 4), (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[5].exterior = [[0, 1, 2, 3, (0, 4), (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[5].interior = [[(0, 4), (1, 5), (2, 6), (3, 7), 4, 5, 6, 7]]
# 0,1,1,0,1,0,0,0 -> 00010110 # Basic Case 6
BCTcube3d.base_cases[6].name = "MC33 Case 7.1"
BCTcube3d.base_cases[6].faces = [[(0, 1), (1, 3), (1, 5)], [(0, 2), (2, 6), (2, 3)], [(0, 4), (4, 5), (4, 6)]]
BCTcube3d.base_cases[6].exterior = [[1, (0, 1), (1, 3), (1, 5)], [2, (0, 2), (2, 6), (2, 3)], [4, (0, 4), (4, 5), (4, 6)]]
BCTcube3d.base_cases[6].interior = [[(0, 1), (1, 3), (1, 5), (0, 2), (2, 3), (2, 6)], [(1, 5), 5, (4, 5), (2, 6), 6, (4,6)], [0, (0, 1), (0, 2), (0, 4), (4, 5), (4, 6)], [(0, 1), (1, 5), (4, 5), (0, 2), (2, 6), (4, 6)], [(1, 5), 3, (2,6), 5, 7, 6], [(1, 3), (1, 5), (2, 3), (2, 6), 3]]
# 1,1,1,0,1,0,0,0 -> 00010111 # Basic Case 9 and its inverse
BCTcube3d.base_cases[7].name = "MC33 Case 9"
BCTcube3d.base_cases[7].faces = [[(2, 3), (1, 3), (2, 6), (1, 5)], [(2, 6), (1, 5), (4, 6), (4, 5)]]
BCTcube3d.base_cases[7].exterior = [[(2, 3), (2, 6), 2, (1, 3), (1, 5), 1], [0, 1, 2, (0, 4), (1, 5), (2, 6)], [(0, 4), (1, 5), (2, 6), 4, (4, 5), (4, 6)]]
BCTcube3d.base_cases[7].interior = [[(2, 3), (1, 3), 3, 6, 5, 7], [6, (2, 6), (2, 3), 5, (1, 5), (1, 3)], [(4, 6), (2, 6), 6, (4, 5), (1, 5), 5]]
# 0,0,0,1,1,0,0,0 -> 00011000 # Basic Case 4
BCTcube3d.base_cases[8].name = "MC33 Case 4.1"
BCTcube3d.base_cases[8].faces = [[(0, 4), (4, 6), (4, 5)], [(1, 3), (2, 3), (3, 7)]]
BCTcube3d.base_cases[8].exterior = [[4, (0, 4), (4, 6), (4, 5)], [3, (1, 3), (2, 3), (3, 7)]]
BCTcube3d.base_cases[8].interior = [[(0, 4), (4, 6), (4, 5), 0, 2, 1], [(4, 6), 6, 2, (4, 5), 5, 1], [(1, 3), 1, 5, (2, 3), 2, 6], [(1, 3), (2, 3), (3, 7), 5, 6, 7]]
# 1,0,0,1,1,0,0,0 -> 00011001 # Basic Case 6
BCTcube3d.base_cases[9].name = "MC33 Case 6.1.1"
BCTcube3d.base_cases[9].faces = [[(4, 5), (4, 6), (0, 1), (0, 2)], [(2, 3), (3, 7), (1, 3)]]
BCTcube3d.base_cases[9].exterior = [[0, (0, 1), (0, 2), 4, (4, 5), (4, 6)], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[9].interior = [[(4, 5), (4, 6), (0, 1), (0, 2), 5, 6, 1, 2], [5, 6, 1, 2, (5, 7), (6, 7), (1, 3), (2, 3)], [(1, 3), (2, 3), (3, 7), (5, 7), (6, 7), 7]]
# 1,1,0,1,1,0,0,0 -> 00011011 # Basic Case 11 and its inverse
BCTcube3d.base_cases[10].name = "MC33 Case 11"
BCTcube3d.base_cases[10].faces = [[(0, 2), (4, 5), (4, 6)], [(0, 2), (2, 3), (4, 5), (3, 7)], [(4, 5), (3, 7), (1, 5)]]
BCTcube3d.base_cases[10].exterior = [[(0, 2), (2, 3), (4, 5), (3, 7), (1, 5)], [(0, 2), (2, 3), 1, (1, 5)], [1, (1, 5), (2, 3), 3], [(1, 5), (2, 3), 3, (3, 7)], [(0, 2), 1, (1, 5), 0], [0, (0, 2), (1, 5), (4, 5)], [0, (0, 2), 4, (4, 6), (4, 5)]]
BCTcube3d.base_cases[10].interior = [[(0, 2), (2, 3), (4, 5), (3, 7), (4, 6)], [(0, 2), (2, 3), 2, (4, 6)], [2, (2, 3), 6, (4, 6)], [(4, 6), 6, (2, 3), (3, 7)], [(4, 6), 6, (3, 7), 7], [(4, 5), (4, 6), (3, 7), 7], [(1, 5), (4, 5), (3, 7), 7], [(1, 5), (4, 5), 5, 7]]
# 0,1,1,1,1,0,0,0 -> 00011110 # Basic Case 12 and its inverse
BCTcube3d.base_cases[11].name = "MC33 Case 12.1.1"
BCTcube3d.base_cases[11].faces = [[(0, 4), (4, 5), (4, 6)], [(0, 1), (0, 2), (1, 5), (2, 6)], [(1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].exterior = [[(0, 4), (4, 5), (4, 6), 4], [(0, 1), 1, (1, 5), (0, 2), 2, (2, 6)], [1, 2, 3, (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].interior = [[0, (0, 1), (0, 2), (0, 4), (4, 5), (4, 6)], [(0, 1), (1, 5), (4, 5), (0, 2), (2, 6), (4, 6)], [(1, 5), (4, 5), 5, (2, 6), (4, 6), 6], [(1, 5), (2, 6), (3, 7), 5, 6, 7]]
# 0,0,1,1,1,1,0,0 -> 00111100 # Basic Case 10 and its inverse
BCTcube3d.base_cases[12].name = "MC33 Case 10.1.1"
BCTcube3d.base_cases[12].faces = [[(0, 4), (1, 5), (4, 6), (5, 7)], [(0, 2), (1, 3), (2, 6), (3, 7)]]
BCTcube3d.base_cases[12].exterior = [[(0, 4), 4, (4, 6), (1, 5), 5, (5, 7)], [(0, 2), 2, (2, 6), (1, 3), 3, (3, 7)]]
BCTcube3d.base_cases[12].interior = [[0, (0, 4), 6, (4, 6), 1, (1, 5), 7, (5, 7)], [0, (0, 2), 6, (2, 6), 1, (1, 3), 7, (3, 7)]]
# 1,0,0,1,0,1,1,0 -> 01101001 # Basic Case 13 and its inverse
BCTcube3d.base_cases[13].name = "MC33 Case 13.1"
BCTcube3d.base_cases[13].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 3), (2, 3), (3, 7)], [(1, 5), (4, 5), (5, 7)], [(2, 6), (4, 6), (6, 7)]]
BCTcube3d.base_cases[13].exterior = [[(0, 1), (0, 2), (0, 4), 0], [(1, 3), (2, 3), (3, 7), 3], [(1, 5), (4, 5), (5, 7), 5], [(2, 6), (4, 6), (6, 7), 6]]
BCTcube3d.base_cases[13].interior = [[(0, 1), (0, 2), (0, 4), (4, 5), (4, 6), 4], [(1, 3), (2, 3), (3, 7), (5, 7), (6, 7), 7], [(1, 5), (4, 5), (5, 7), 1, (0, 1), (1, 3)], [(2, 6), (4, 6), (6, 7), 2, (0, 2), (2, 3)], [(0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 7), (6, 7)]]

# ################################################################################
# ## MC 33 cases and MC 33 face test table for 3D Cube                          ##
# ################################################################################

# 0,1,1,0,0,0,0,0 -> 00000110 # MC33 Case 3.2
BCTcube3d.base_cases[3].mc33.append(Triangulation())
BCTcube3d.base_cases[3].mc33[-1].name = "MC33 Case 3.2"
BCTcube3d.base_cases[3].mc33[-1].faces = [[(0, 2), (2, 6), (0, 1), (1, 5)], [(2, 6), (2, 3), (1, 5), (1, 3)]]
BCTcube3d.base_cases[3].mc33[-1].exterior = [[1, (0, 1), (1, 5), (1, 3)], [2, (0, 2), (2, 6), (2, 3)], [(0, 1), (1, 5), (1, 3), (0, 2), (2, 6), (2, 3)]]
BCTcube3d.base_cases[3].mc33[-1].interior = [[(0, 2), (2, 6), 6, (0, 1), (1, 5), 5], [(2, 6), (2, 3), 6, (1, 5), (1, 3), 5], [(0, 1), (0, 2), 0, 5, 6, 4], [(1, 3), (2, 3), 3, 5, 6, 7]]
BCTcube3d.base_cases[3].tests = binaryheap((TEST_FACE_4, CASE_IS_REGULAR, 0))
# 0,0,0,1,1,0,0,0 -> 00011000 # MC Case 4.2
BCTcube3d.base_cases[8].mc33.append(Triangulation())
BCTcube3d.base_cases[8].mc33[-1].name = "MC33 Case 4.2"
BCTcube3d.base_cases[8].mc33[-1].faces = [[(0, 4), (4, 5), (1, 3)], [(1, 3), (3, 7), (4, 5)], [(4, 5), (3, 7), (4, 6)], [(0, 4), (4, 6), (2, 3)], [(0, 4), (1, 3), (2, 3)], [(2, 3), (3, 7), (4, 6)]]
BCTcube3d.base_cases[8].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(0, 4), (4, 6), (1, 3), (3, 7), (4, 5)], [(0, 4), (4, 6), (1, 3), (3, 7), (2, 3)], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[8].mc33[-1].interior = [[0, (0, 4), 5, (4, 5), (1, 3)], [0, 1, 5, (1, 3)], [0, (0, 4), 6, (4, 6), (2, 3)], [0, 2, 6, (2, 3)], [0, (0, 4), (2, 3), (1, 3)], [(1, 3), (3, 7), (4, 5), 5], [(2, 3), (3, 7), 6, (4, 6)], [5, (4, 5), 6, (4, 6), (3, 7)], [5, 6, 7, (3, 7)]]
BCTcube3d.base_cases[8].tests = binaryheap((TEST_INTERIOR_3, 0, CASE_IS_REGULAR))
# 1,0,0,1,1,0,0,0 -> 00011001 # MC33 Case 6.1.2
BCTcube3d.base_cases[9].mc33.append(Triangulation())
BCTcube3d.base_cases[9].mc33[-1].name = "MC33 Case 6.1.2"
BCTcube3d.base_cases[9].mc33[-1].faces = [[(0, 1), (0, 2), (1, 3), (2, 3)], [(0, 1), (1, 3), (4, 5)], [(1, 3), (4, 5), (3, 7)], [(0, 2), (2, 3), (4, 6)], [(2, 3), (4, 6), (3, 7)], [(4, 5), (4, 6), (3, 7)]]
BCTcube3d.base_cases[9].mc33[-1].exterior = [[0, (0, 1), (0, 2), 4, (4, 5), (4, 6)], [(4, 5), (4, 6), (1, 3), (2, 3), (3, 7)], [(0, 1), (1, 3), (4, 5), (0, 2), (2, 3), (4, 6)], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[9].mc33[-1].interior = [[(4, 5), (4, 6), (3, 7), 7], [(0, 1), (4, 5), (1, 3), 1], [1, (1, 3), (4, 5), 5], [(1, 3), 5, (3, 7), 7, (4, 5)], [(0, 2), (2, 3), (4, 6), 2], [2, (2, 3), (4, 6), 6], [(2, 3), (3, 7), 6, 7, (4, 6)]]
# 1,0,0,1,1,0,0,0 -> 00011001 # MC33 Case 6.2
BCTcube3d.base_cases[9].mc33.append(Triangulation())
BCTcube3d.base_cases[9].mc33[-1].name = "MC33 Case 6.2"
BCTcube3d.base_cases[9].mc33[-1].faces = [[(0, 1), (1, 3), (4, 5)], [(1, 3), (4, 5), (3, 7)], [(0, 2), (2, 3), (4, 6)], [(2, 3), (4, 6), (3, 7)], [(4, 5), (4, 6), (3, 7)]]
BCTcube3d.base_cases[9].mc33[-1].exterior = BCTcube3d.base_cases[9].mc33[0].exterior
BCTcube3d.base_cases[9].mc33[-1].interior = BCTcube3d.base_cases[9].mc33[0].interior
BCTcube3d.base_cases[9].tests = binaryheap((TEST_FACE_4,
                                            1,
                                            (TEST_INTERIOR_3, 0, CASE_IS_REGULAR)
                                            ))
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2 (face 0, 2 inside; face 4 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 4), (4, 5), (4, 6)], [(0, 1), (1, 5), (0, 2), (2, 6)], [(1, 3), (1, 5), (2, 3), (2, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[(0, 4), (4, 5), (4, 6), 4], [(0, 1), 1, (1, 3), (1, 5)], [(0, 2), 2, (2, 3), (2, 6)], [(0, 2), (2, 6), (2, 3), (0, 1), (1, 5), (1, 3)]]
BCTcube3d.base_cases[6].mc33[-1].interior = [[(0, 1), (1, 5), (0, 2), (2, 6), (4, 5), 5, (4, 6), 6], [0, (0, 1), (0, 2), (0, 4), (4, 5), (4, 6)], [(1, 5), (1, 3), (2, 6), (2, 3), 3], [(1, 5), 3, (2, 6), 5, 7, 6]]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2 (face 2, 4 inside; face 0 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2 face 2 and 4 connection"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[0].faces, MIRROR_FACES_0_TO_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[0].exterior, MIRROR_FACES_0_TO_4)
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[0].interior, MIRROR_FACES_0_TO_4)
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2 (face 0, 4 inside; face 2 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2 face 0 and 4 connection"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[1].faces, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[1].exterior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[1].interior, MIRROR_FACES_0_TO_2)
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 0 inside; face 2, 4 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 1), (0, 2), (0, 7), (2, 6)], [(1, 3), (2, 3), (0, 7), (2, 6)], [(0, 1), (0, 7), (0, 4), (4, 6)], [(1, 5), (0, 7), (4, 5), (4, 6)], [(1, 5), (0, 7), (1, 3)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[(1, 3), 1, (0, 7), (1, 5)], [1, (1, 3), (0, 7), (0, 1)], [1, (1, 5), (0, 7), (0, 1)], [(0, 1), (1, 5), (0, 7), (0, 4), (4, 5), (4, 6)], [4, (0, 4), (4, 5), (4, 6)], [(0, 1), (1, 3), (0, 7), (0, 2), (2, 3), (2, 6)], [(0, 2), (2, 3), (2, 6), 2]]
BCTcube3d.base_cases[6].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(0, 2), (0, 1), (0, 4), (2, 6), (0, 7), (4, 6)], [(1, 5), 5, (4, 5), (5, 7)], [(1, 5), (5, 7), (4, 5), (0, 7), (6, 7), (4, 6)], [(0, 7), (2, 6), (4, 6), (6, 7)], [(2, 6), (4, 6), 6, (6, 7)], [(1, 3), (2, 3), (0, 7), (2, 6), 3], [(1, 5), (0, 7), (1, 3), (3, 7)], [(1, 3), 3, (0, 7), (3, 7)], [3, (2, 6), (3, 7), (6, 7), (0, 7)], [(1, 5), (0, 7), (5, 7), (6, 7), (3, 7)], [(5, 7), (6, 7), (3, 7), 7]]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 2 inside; face 0, 4 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3, face 2 connection"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[3].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[3].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[3].interior, ROTATE_FACES_0_2_4)
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 4 inside; face 0, 2 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3, face 4 connection"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[4].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[4].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[4].interior, ROTATE_FACES_0_2_4)
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.4.1
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.4.1"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 3), (1, 5), (4, 5)], [(2, 3), (2, 6), (4, 6)], [(2, 3), (1, 3), (4, 6), (4, 5)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[(2, 3), (1, 3), (4, 6), (4, 5), (0, 4)], [(0, 1), (0, 2), (1, 3), (2, 3), (0, 4)], [(1, 3), (4, 5), (1, 5), (0, 4)], [(1, 3), (1, 5), 1, (0, 1)], [(1, 3), (1, 5), (0, 1), (0, 4)], [(2, 6), (4, 6), (2, 3), (0, 4)], [2, (2, 3), (2, 6), (0, 2)], [(2, 3), (2, 6), (0, 4), (0, 2)], [(0, 4), (4, 5), (4, 6), 4]]
BCTcube3d.base_cases[6].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(2, 3), (1, 3), (4, 6), (4, 5), 7], [(1, 3), (1, 5), (4, 5), 7], [(2, 3), (2, 6), (4, 6), 7], [(4, 5), (1, 5), 7, 5], [(4, 6), (2, 6), 6, 7], [(1, 3), (2, 3), 3, 7]]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.4.2
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.4.2"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 1), (1, 3), (0, 2), (2, 3)], [(0, 1), (1, 3), (1, 5)], [(0, 1), (1, 5), (0, 4), (4, 5)], [(0, 4), (4, 5), (4, 6)], [(0, 4), (4, 6), (0, 2), (2, 6)], [(0, 2), (2, 3), (2, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[1, (0, 1), (1, 3), (1, 5)], [2, (0, 2), (2, 3), (2, 6)], [4, (0, 4), (4, 5), (4, 6)]]
BCTcube3d.base_cases[6].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(0, 1), (0, 2), (0, 4), (0, 7)], [(0, 1), (0, 2), (1, 3), (2, 3), (0, 7)], [(0, 2), (0, 4), (2, 6), (4, 6), (0, 7)], [(0, 1), (0, 4), (1, 5), (4, 5), (0, 7)], [(0, 4), (4, 5), (4, 6), (0, 7)], [(0, 1), (1, 3), (1, 5), (0, 7)], [(0, 2), (2, 3), (2, 6), (0, 7)], [(1, 3), (2, 3), 3, 7], [(1, 3), (2, 3), (0, 7), 7], [(1, 3), (1, 5), (0, 7), 7], [(1, 5), (4, 5), (0, 7), 7], [(4, 5), (4, 6), (0, 7), 7], [(2, 6), (4, 6), (0, 7), 7], [(2, 3), (2, 6), (0, 7), 7], [(1, 5), (4, 5), 5, 7], [(2, 6), (4, 6), 6, 7]]
BCTcube3d.base_cases[6].tests = binaryheap((TEST_FACE_0,
                                            (TEST_FACE_2,
                                             (TEST_FACE_4,
                                              (TEST_INTERIOR_0, 7, 6),
                                              5),
                                             (TEST_FACE_4, 4, 1)),
                                            (TEST_FACE_2,
                                             (TEST_FACE_4, 3, 2),
                                             (TEST_FACE_4, 0, CASE_IS_REGULAR))))
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.1.1 rotated
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].name = "MC33 Case 10.1.1"
BCTcube3d.base_cases[12].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[12].faces, ROTATE_FACES_0_1)
BCTcube3d.base_cases[12].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[12].exterior, ROTATE_FACES_0_1)
BCTcube3d.base_cases[12].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[12].interior, ROTATE_FACES_0_1)
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.2 and its inverse (face 1 inside; face 0 outside) 
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].name = "MC33 Case 10.2"
BCTcube3d.base_cases[12].mc33[-1].faces = [[(0, 4), (0, 2), (0, 7)], [(0, 4), (1, 5), (0, 7)], [(0, 2), (1, 3), (0, 7)], [(1, 5), (5, 7), (0, 7)], [(1, 3), (3, 7), (0, 7)], [(3, 7), (2, 6), (0, 7)], [(5, 7), (4, 6), (0, 7)], [(2, 6), (4, 6), (0, 7)]]
BCTcube3d.base_cases[12].mc33[-1].exterior = [[(0, 4), 4, (4, 6), (1, 5), 5, (5, 7)], [(0, 4), (4, 6), (1, 5), (5, 7), (0, 7)], [(0, 4), (4, 6), (0, 2), (2, 6), (0, 7)], [(1, 3), (3, 7), (0, 2), (2, 6), (0, 7)], [(1, 3), 3, (3, 7), (0, 2), 2, (2, 6)]]
BCTcube3d.base_cases[12].mc33[-1].interior = [[0, (0, 4), (0, 2), 1, (1, 5), (1, 3)], [(0, 2), (0, 4), (1, 3), (1, 5), (0, 7)], [(1, 3), (1, 5), (3, 7), (5, 7), (0, 7)], [(3, 7), (5, 7), (2, 6), (4, 6), (0, 7)], [(3, 7), 7, (5, 7), (2, 6), 6, (4, 6)]]
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.2 and its inverse (face 0 inside; face 1 outside) 
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[12].mc33[1].faces, Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6)))
BCTcube3d.base_cases[12].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[12].mc33[1].exterior, Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6)))
BCTcube3d.base_cases[12].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[12].mc33[1].interior, Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6)))
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.1.2
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].name = "MC33 Case 10.1.2"
BCTcube3d.base_cases[12].mc33[-1].faces = [[(0, 2), (0, 4), (1, 3), (1, 5)], [(1, 3), (1, 5), (3, 7), (5, 7)], [(3, 7), (5, 7), (2, 6), (4, 6)], [(2, 6), (4, 6), (0, 2), (0, 4)]]
BCTcube3d.base_cases[12].mc33[-1].exterior = [[(0, 4), 4, (4, 6), (1, 5), 5, (5, 7)], [(0, 4), (4, 6), (1, 5), (5, 7), (0, 2), (2, 6), (1, 3), (3, 7)], [(0, 2), 2, (2, 6), (1, 3), 3, (3, 7)]]
BCTcube3d.base_cases[12].mc33[-1].interior = [[0, (0, 2), (0, 4), 1, (1, 3), (1, 5)], [(2, 6), 6, (4, 6), (3, 7), 7, (5, 7)]]
BCTcube3d.base_cases[12].tests = binaryheap((TEST_FACE_0,
                                             (TEST_FACE_1, 0, 1),
                                             (TEST_FACE_1,
                                              2,
                                              (TEST_INTERIOR_2, 3, CASE_IS_REGULAR))))
# 0,1,1,1,1,0,0,0 -> 00011110 # Inverse of MC33 Case 12.1.1
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.1.1 inv"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 5), (2, 6), (4, 5), (4, 6)], [(1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(1, 5), (2, 6), (4, 5), (4, 6), (0, 4)], [(0, 1), (0, 2), (1, 5), (2, 6), (0, 4)], [(0, 1), 1, (1, 5), (0, 2), 2 , (2, 6)], [1, 2, 3, (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 5), 5, (4, 5), (2, 6), 6, (4, 6)], [(1, 5), (2, 6), (3, 7), 5, 6, 7]]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.1.2 and its inverse
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.1.2"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(0, 1), (0, 4), (4, 5)], [(0, 1), (4, 5), (1, 5)], [(0, 2), (0, 4), (4, 6)], [(0, 2), (4, 6), (2, 6)], [(1, 5), (4, 5), (3, 7)], [(4, 5), (4, 6), (3, 7)], [(2, 6), (4, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(0, 1), (0, 2), (4, 5), (4, 6), (0, 4)], [(0, 1), (1, 5), (4, 5), (0, 2), (2, 6), (4, 6)], [(1, 5), (4, 5), (2, 6), (4, 6), (3, 7)], [(0, 1), 1, (1, 5), (0, 2), 2, (2, 6)], [1, 2, 3, (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 5), (4, 5), 5, (3, 7)], [(4, 5), 5, (3, 7), 7], [(4, 5), (4, 6), (3, 7), 7], [(4, 6), (2, 6), 6, (3, 7)], [(4, 6), 6, (3, 7), 7]]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.2 and its inverse (face 2 inside; face 0 outside) 
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.2"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 4), (4, 6), (0, 7)], [(4, 6), (4, 5), (0, 7)], [(0, 4), (0, 1), (0, 7)], [(4, 5), (1, 5), (0, 7)], [(1, 5), (3, 7), (0, 7)], [(3, 7), (2, 6), (0, 7)], [(0, 2), (2, 6), (0, 7)], [(0, 1), (0, 2), (0, 7)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), (0, 7)], [(0, 1), (0, 4), (1, 5), (4, 5), (0, 7)], [(0, 1), (0, 7), (1, 5), 1], [1, (1, 5), 3, (3, 7), (0, 7)], [2, (2, 6), 3, (3, 7), (0, 7)], [(0, 1), 1, 2, 3, (0, 7)], [(0, 1), (0, 2), 2, (0, 7)], [(0, 2), 2, (2, 6), (0, 7)]]
BCTcube3d.base_cases[11].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(0, 1), (0, 2), (0, 4), (0, 7)], [(0, 2), (2, 6), (0, 4), (4, 6), (0, 7)], [(2, 6), (0, 7), (4, 6), 6], [(2, 6), 6, (3, 7), 7, (0, 7)], [(3, 7), 7, (1, 5), 5, (0, 7)], [(4, 6), 6, 5, 7, (0, 7)], [(4, 6), (4, 5), (0, 7), 5], [(4, 5), (0, 7), 5, (1, 5)]]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.2 and its inverse (face 0 inside; face 2 outside) 
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[11].mc33[2].faces, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[2].exterior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[2].interior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].tests = binaryheap((TEST_FACE_0,
                                             (TEST_FACE_2, 0, 2),
                                             (TEST_FACE_2,
                                              3,
                                              (TEST_INTERIOR_3, 1, CASE_IS_REGULAR))))
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 3, 4 inside; 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2"
BCTcube3d.base_cases[13].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 3), (2, 3), (3, 7)], [(2, 6), (4, 6), (1, 5), (4, 5)], [(2, 6), (6, 7), (1, 5), (5, 7)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[(0, 1), (0, 2), (0, 4), 0], [(1, 3), (2, 3), (3, 7), 3], [(1, 5), (4, 5), (5, 7), 5], [(1, 5), (4, 5), (5, 7), (2, 6), (4, 6), (6, 7)], [(2, 6), (4, 6), (6, 7), 6]]
BCTcube3d.base_cases[13].mc33[-1].interior = [[1, (1, 5), 2, (2, 6), (0, 4)], [1, (0, 1), 2, (0, 2), (0, 4)], [(0, 4), (1, 5), (2, 6), 4, (4, 5), (4, 6)], [1, (1, 5), 2, (2, 6), (3, 7)], [1, (1, 3), 2, (2, 3), (3, 7)], [(3, 7), (1, 5), (2, 6), 7, (5, 7), (6, 7)]]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 3, 5 inside; 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_1**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_1**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_1**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 4, 5 inside; 3 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_3_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 3, 4, 5 inside; 2 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_2_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 2, 3, 4, 5 inside; 1 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_2_4)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 1, 2, 3, 4, 5 inside; 0 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_3_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 2, 4 inside; 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3"
BCTcube3d.base_cases[13].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(2, 3), (1, 3), (0, 7)], [(2, 3), (2, 6), (0, 7)], [(2, 6), (4, 6), (0, 7)], [(4, 6), (4, 5), (0, 7)], [(4, 5), (1, 5), (0, 7)], [(1, 5), (5, 7), (0, 7)], [(5, 7), (6, 7), (0, 7)], [(6, 7), (3, 7), (0, 7)], [(3, 7), (1, 3), (0, 7)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[(0, 1), (0, 2), (0, 4), 0], [(1, 5), (4, 5), (5, 7), 5], [(1, 5), (4, 5), (5, 7), (0, 7)], [(4, 5), (5, 7), (4, 6), (6, 7), (0, 7)], [(4, 6), (6, 7), (2, 6), (0, 7)], [(4, 6), (6, 7), (2, 6), 6], [(2, 3), (3, 7), (2, 6), (6, 7), (0, 7)], [(1, 3), (2, 3), (3, 7), (0, 7)], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[13].mc33[-1].interior = [[(0, 4), (0, 2), (4, 6), (2, 6), (0, 7)], [(0, 4), (0, 1), (4, 5), (1, 5), (0, 7)], [(0, 1), (1, 3), (0, 2), (2, 3), (0, 7)], [4, (4, 6), (4, 5), (0, 7)], [4, (4, 5), (0, 4), (0, 7)], [4, (4, 6), (0, 4), (0, 7)], [2, (0, 2), (2, 6), (0, 7)], [2, (0, 2), (2, 3), (0, 7)], [2, (2, 6), (2, 3), (0, 7)], [1, (0, 1), (1, 3), (0, 7)], [1, (0, 1), (1, 5), (0, 7)], [1, (1, 3), (1, 5), (0, 7)], [(1, 3), (1, 5), (3, 7), (5, 7), (0, 7)], [(3, 7), (5, 7), (6, 7), (0, 7)], [(3, 7), (5, 7), (6, 7), 7], [(0, 1), (0, 2), (0, 4), (0, 7)]]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 2, 5 inside; 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_1*MIRROR_FACES_0_TO_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_1*MIRROR_FACES_0_TO_1)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_1*MIRROR_FACES_0_TO_1)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 3, 4 inside; 2, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_1**3*MIRROR_FACES_0_TO_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_1**3*MIRROR_FACES_0_TO_1)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_1**3*MIRROR_FACES_0_TO_1)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 3, 5 inside; 2, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_1**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_1**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_1**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 3, 4 inside; 1, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_4)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 3, 5 inside; 1, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_4*ROTATE_FACES_0_1*ROTATE_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_4*ROTATE_FACES_0_1*ROTATE_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_4*ROTATE_FACES_0_1*ROTATE_FACES_0_1)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 4, 5 inside; 1, 3 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_4**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 3, 4, 5 inside; 1, 2 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 3, 4 inside; 0, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 3, 5 inside; 0, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5*ROTATE_FACES_1_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5*ROTATE_FACES_1_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5*ROTATE_FACES_1_2_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 4, 5 inside; 0, 3 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 3, 4, 5 inside; 0, 2 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5**2*ROTATE_FACES_0_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5**2*ROTATE_FACES_0_2_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5**2*ROTATE_FACES_0_2_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 0, 2, 4, INT inside; 1, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(3, 7), (5, 7), (6, 7)], [(1, 5), (4, 5), (2, 6), (4, 6)], [(1, 3), (1, 5), (2, 3), (2, 6)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[(0, 1), (0, 2), (0, 4), 0], [(2, 6), (4, 6), (6, 7), 6], [(2, 6), (4, 6), (6, 7), (1, 5), (4, 5), (5, 7)], [(1, 5), (5, 7), (2, 6), (6, 7), (3, 7)], [(1, 5), (4, 5), (5, 7), 5], [(1, 3), (1, 5), (2, 3), (2, 6), (3, 7)], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[13].mc33[-1].interior = [[(3, 7), (5, 7), (6, 7), 7], [4, (4, 5), (4, 6), (0, 4), (1, 5), (2, 6)], [1, (1, 3), (1, 5), 2, (2, 3), (2, 6)], [1, (1, 5), 2, (2, 6), (0, 4)], [(0, 1), 1, (0, 2), 2, (0, 4)]]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 0, 3, 5, INT inside; 1, 2, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[18].faces, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].exterior, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].interior, ROTATE_FACES_1_2_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 1, 2, 5, INT inside; 0, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[18].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].interior, ROTATE_FACES_0_3_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 1, 3, 4, INT inside; 0, 2, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[18].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].interior, ROTATE_FACES_0_3_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 0, 2, 4 inside; 1, 3, 5, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = [[(3, 7), (5, 7), (6, 7)], [(0, 4), (4, 5), (4, 6)], [(0, 1), (1, 3), (1, 5)], [(0, 2), (2, 3), (2, 6)], [(0, 4), (4, 5), (0, 1), (1, 5)], [(0, 1), (1, 3), (0, 2), (2, 3)], [(0, 2), (0, 4), (2, 6), (4, 6)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 5), (4, 5), (2, 6), (4, 6), (0, 4)], [(0, 1), (1, 5), (0, 2), (2, 6), (0, 4)], [(0, 1), (1, 3), (1, 5), (0, 2), (2, 3), (2, 6)], [(1, 5), (4, 5), 5, (2, 6), (4, 6), 6], [(1, 5), 5, (5, 7), (2, 6), 6, (6, 7)], [(1, 5), (5, 7), (2, 6), (6, 7), (3, 7)], [(1, 5), (3, 7), (2, 6), (1, 3), 3, (2, 3)]]
BCTcube3d.base_cases[13].mc33[-1].interior = [[(0, 1), (1, 3), (1, 5), 1], [(0, 2), (2, 3), (2, 6), 2], [(0, 4), (4, 5), (4, 6), 4], [(3, 7), (5, 7), (6, 7), 7]]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 0, 3, 5 inside; 1, 2, 4, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[22].faces, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].exterior, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].interior, ROTATE_FACES_1_2_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 1, 2, 5 inside; 0, 3, 4, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[22].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].interior, ROTATE_FACES_0_3_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 1, 3, 4 inside; 0, 2, 5, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[22].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].interior, ROTATE_FACES_0_3_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 0, 2, 5 inside; 1, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = [[(0, 4), (0, 1), (0, 7), (1, 3)], [(0, 7), (1, 3), (4, 5), (1, 5)], [(0, 2), (0, 4), (2, 3), (0, 7)], [(2, 3), (0, 7), (2, 6), (4, 6)], [(5, 7), (3, 7), (4, 5), (0, 7)], [(4, 6), (6, 7), (0, 7), (3, 7)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[0, (0, 1), (0, 2), (0, 4)], [(0, 1), (0, 2), (0, 4), (1, 3), (2, 3), (0, 7)], [5, (1, 5), (4, 5), (5, 7)], [(1, 5), (4, 5), (5, 7), (1, 3), (0, 7), (3, 7)], [6, (2, 6), (4, 6), (6, 7)], [(2, 6), (4, 6), (6, 7), (2, 3), (0, 7), (3, 7)], [(1, 3), (2, 3), (3, 7), (0, 7)], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[13].mc33[-1].interior = [[1, (0, 1), (1, 3), (1, 5)], [(0, 1), (1, 3), (1, 5), (0, 4), (0, 7), (4, 5)], [2, (0, 2), (2, 3), (2, 6)], [(0, 2), (2, 3), (2, 6), (0, 4), (0, 7), (4, 6)], [7, (3, 7), (5, 7), (6, 7)], [(3, 7), (5, 7), (6, 7), (0, 7), (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), (0, 7)], [(0, 4), (4, 5), (4, 6), 4]]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 0, 3, 4 inside; 1, 2, 5, outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[26].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].interior, ROTATE_FACES_0_3_5**2)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 1, 2, 4 inside; 0, 3, 5, outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[26].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].interior, ROTATE_FACES_0_2_4)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 1, 3, 5 inside; 0, 2, 4, outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[26].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].interior, ROTATE_FACES_0_3_5)
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2 inside; 1, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[17].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[17].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[17].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 3 inside; 1, 2, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[16].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[16].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[16].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 4 inside; 1, 2, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[15].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[15].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[15].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 5 inside; 1, 2, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[14].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[14].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[14].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2 inside; 0, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[13].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[13].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[13].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 3 inside; 0, 2, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[12].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[12].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[12].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 4 inside; 0, 2, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[11].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[11].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[11].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 5 inside; 0, 2, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[10].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[10].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[10].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 2, 4 inside; 0, 1, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[9].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[9].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[9].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 2, 5 inside; 0, 1, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[8].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[8].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[8].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 3, 4 inside; 0, 1, 2, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[7].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[7].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[7].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 3, 5 inside; 0, 1, 2, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[6].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[6].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[6].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0 inside; 1, 2, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[5].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[5].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[5].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 1 inside; 0, 2, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[4].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[4].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[4].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 2 inside; 0, 1, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[3].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[3].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[3].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 3 inside; 0, 1, 2, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[2].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[2].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[2].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 4 inside; 0, 1, 2, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[1].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[1].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[1].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 5 inside; 0, 1, 2, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].mc33[0].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].mc33[0].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].mc33[0].exterior
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.1 (face 0, 1, 2, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.1 inv"
BCTcube3d.base_cases[13].mc33[-1].faces = BCTcube3d.base_cases[13].faces
BCTcube3d.base_cases[13].mc33[-1].exterior = BCTcube3d.base_cases[13].interior
BCTcube3d.base_cases[13].mc33[-1].interior = BCTcube3d.base_cases[13].exterior
BCTcube3d.base_cases[13].tests = binaryheap((TEST_FACE_0,
                                             (TEST_FACE_1,
                                              (TEST_FACE_2,
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 48, 47),
                                                 46),
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 45, 41),
                                                 40)),
                                               (TEST_FACE_4,
                                                (TEST_FACE_5, 44, 39),
                                                38)),
                                              (TEST_FACE_2,
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 43, 37),
                                                 36),
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 32, 29),
                                                 (TEST_FACE_5,
                                                  (TEST_INTERIOR_3, 25, 21),
                                                  17))),
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5,
                                                  34,
                                                  (TEST_INTERIOR_2, 24, 20)),
                                                 (TEST_FACE_5, 28, 16)),
                                                (TEST_FACE_4,
                                                 15,
                                                 (TEST_FACE_5, 14, 5))))),
                                             (TEST_FACE_1,
                                              (TEST_FACE_2,
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 42, 33),
                                                 32),
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5,
                                                  31,
                                                  (TEST_INTERIOR_1, 23, 19)),
                                                 (TEST_FACE_5, 27, 13))),
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 30, 26),
                                                 (TEST_FACE_5,
                                                  (TEST_INTERIOR_0, 22, 18),
                                                  12)),
                                                (TEST_FACE_4,
                                                 11,
                                                 (TEST_FACE_5, 10, 4)))),
                                              (TEST_FACE_2,
                                               (TEST_FACE_4,
                                                9,
                                                (TEST_FACE_5, 8, 3)),
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 7,
                                                 (TEST_FACE_5, 6, 2)),
                                                (TEST_FACE_4,
                                                 1,
                                                 (TEST_FACE_5, 0, CASE_IS_REGULAR)))))))

# generate code
BCTcube3d.generate()
#BCTcube3d.print_info()

################################################################################
## 3D Simplex                                                                 ##
################################################################################
BCTsimplex3d = LookupGenerator(3,"simplex")
# base cases simplex 3D:
# 0,0,0,0 -> 0000
BCTsimplex3d.base_cases[0].faces = []
BCTsimplex3d.base_cases[0].interior = [[0, 1, 2, 3]]
BCTsimplex3d.base_cases[0].exterior = []
# 1,0,0,0 -> 0001
BCTsimplex3d.base_cases[1].faces = [[(0, 2), (0, 1), (0, 3)]]
BCTsimplex3d.base_cases[1].interior = [[(0, 2), (0, 1), (0, 3), 2, 1, 3]]
BCTsimplex3d.base_cases[1].exterior = [[0, (0, 2), (0, 1), (0, 3)]]
# 1,1,0,0 -> 0011
BCTsimplex3d.base_cases[2].faces = [[(0, 2), (1, 2), (0, 3), (1, 3)]]
BCTsimplex3d.base_cases[2].interior = [[(0, 2), (1, 2), 2, (0, 3), (1, 3), 3]]
BCTsimplex3d.base_cases[2].exterior = [[0, (0, 2), (0, 3), 1, (1, 2), (1, 3)]]
# generate code
BCTsimplex3d.generate()

################################################################################
## 2D Cube                                                                    ##
################################################################################
BCTcube2d = LookupGenerator(2, "cube")

# base cases cube 2D:
# 0,0,0,0 -> 0000
BCTcube2d.base_cases[0].faces = []
BCTcube2d.base_cases[0].interior = [[0, 1, 2, 3]]
BCTcube2d.base_cases[0].exterior = []
# 1,0,0,0 -> 0001
BCTcube2d.base_cases[1].faces = [[(0, 1), (0, 2)]]
BCTcube2d.base_cases[1].interior = [[(0, 1), (0, 2), 1, 2], [1, 2, 3]]
BCTcube2d.base_cases[1].exterior = [[0, (0, 1), (0, 2)]]
# 1,1,0,0 -> 0011
BCTcube2d.base_cases[2].faces = [[(1, 3), (0, 2)]]
BCTcube2d.base_cases[2].interior = [[(0, 2), (1, 3), 2, 3]]
BCTcube2d.base_cases[2].exterior = [[0, 1, (0, 2), (1, 3)]]
# 0,1,1,0 -> 0110
BCTcube2d.base_cases[3].faces = [[(0, 1), (0, 2)], [(2, 3), (1, 3)]]
BCTcube2d.base_cases[3].interior = [[0, (0, 1), (0, 2)], [(2, 3), (1, 3), 3]]
BCTcube2d.base_cases[3].exterior = [[(0, 1), (0, 2), 1, 2], [(2, 3), (1, 3), 2, 1]]

BCTcube2d.base_cases[3].mc33.append(Triangulation())
BCTcube2d.base_cases[3].mc33[-1].faces = [[(1, 3), (0, 1)], [(0, 2), (2, 3)]]
BCTcube2d.base_cases[3].mc33[-1].interior = [[(1, 3), (0, 1), 3, 0], [(0, 2), (2, 3), 0, 3]]
BCTcube2d.base_cases[3].mc33[-1].exterior = [[(1, 3), (0, 1), 1], [(0, 2), (2, 3), 2]]

BCTcube2d.base_cases[3].tests = [TEST_FACE_0, CASE_IS_REGULAR, 0]

# generate code
BCTcube2d.generate()


################################################################################
## 2D Simplex                                                                 ##
################################################################################
BCTsimplex2d = LookupGenerator(2,"simplex")

# base cases simplex 2D:
# 0,0,0 -> 000
BCTsimplex2d.base_cases[0].faces = []
BCTsimplex2d.base_cases[0].interior = [[0, 1, 2]]
BCTsimplex2d.base_cases[0].exterior = []
# 1,0,0 -> 001
BCTsimplex2d.base_cases[1].faces = [[(0, 1), (0, 2)]]
BCTsimplex2d.base_cases[1].interior = [[(0, 1), (0, 2), 1, 2]]
BCTsimplex2d.base_cases[1].exterior = [[0, (0, 1), (0, 2)]]

# generate code
BCTsimplex2d.generate()

################################################################################
## 1D Cube                                                                    ##
################################################################################
BCTany1d = LookupGenerator(1,"any")

# base cases cube 1D:
# 0,0 -> 00
BCTany1d.base_cases[0].faces = []
BCTany1d.base_cases[0].interior = [[0,1]]
BCTany1d.base_cases[0].exterior = []
# 1,0 -> 01
BCTany1d.base_cases[1].faces = [[(0,1)]]
BCTany1d.base_cases[1].interior = [[(0, 1), 1]]
BCTany1d.base_cases[1].exterior = [[0, (0, 1)]]

# generate code
BCTany1d.generate()

################################################################################
## 0D Cube                                                                    ##
################################################################################
BCTany0d = LookupGenerator(0,"any")
# base cases cube 0D:
# 0 -> 0
BCTany0d.base_cases[0].faces = []
BCTany0d.base_cases[0].exterior = [[0]]
BCTany0d.base_cases[0].interior = []
# generate code
BCTany0d.generate()

LookupGenerators = {}
LookupGenerators[(3, "cube")] = BCTcube3d
LookupGenerators[(3, "simplex")] = BCTsimplex3d
LookupGenerators[(2, "cube")] = BCTcube2d
LookupGenerators[(2, "simplex")] = BCTsimplex2d
LookupGenerators[(1, "any")] = BCTany1d
LookupGenerators[(0, "any")] = BCTany0d
