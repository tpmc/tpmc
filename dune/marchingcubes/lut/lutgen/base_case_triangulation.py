from generator import LookupGenerator
from permutation import Permutation
from cases import Triangulation
from disambiguate import \
    TEST_FACE_0, TEST_FACE_1, TEST_FACE_2, TEST_FACE_3, TEST_FACE_4, TEST_FACE_5,\
    TEST_INTERIOR_0_0, TEST_INTERIOR_1_0, TEST_INTERIOR_2_0, TEST_INTERIOR_3_0,\
    TEST_INTERIOR_0_2, TEST_INTERIOR_1_2, TEST_INTERIOR_2_2, TEST_INTERIOR_3_2,\
    TEST_INTERIOR_0_4, TEST_INTERIOR_1_4, TEST_INTERIOR_2_4, TEST_INTERIOR_3_4,\
    TEST_INVALID, CASE_IS_REGULAR, binaryheap
from geomobj import permute_geom_list, Center, Face0, Face1, Face2, Face3, Face4, Face5, FacePoint


# this file contains the triangulations for the marching-cubes base cases generated
# by the LookupGenerators init-method.
# geometries: (3,"cube"), (3,"simplex"), (2,"cube"), (2,"simplex"), (1,"any"), (0,"any")

# test are according to:
# test_faces: TEST | OUTSIDE | INSIDE
# test_inter: TEST | ref connected | ref not connected
# where test | test true | test false

# Constants for permutate mc 33 cases
MIRROR_FACES_0_1 = Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6))
MIRROR_FACES_0_TO_2 = Permutation(-1, (0, 2, 1, 3, 4, 6, 5, 7))
MIRROR_FACES_0_TO_4 = Permutation(-1, (0, 4, 2, 6, 1, 5, 3, 7))
MIRROR_FACES_4_5 = Permutation(-1, (4, 5, 6, 7, 0, 1, 2, 3))
MIRROR_FACES_2_3 = Permutation(-1, (2, 3, 0, 1, 6, 7, 4, 5))
ROTATE_FACES_0_2_4 = Permutation(1, (0, 2, 4, 6, 1, 3, 5, 7))
ROTATE_FACES_0_2_5 = Permutation(1, (5, 7, 1, 3, 4, 6, 0, 2))
ROTATE_FACES_0_3_5 = Permutation(1, (5, 1, 4, 0, 7, 3, 6, 2))
ROTATE_FACES_1_2_5 = Permutation(1, (6, 4, 2, 0, 7, 5, 3, 1))
ROTATE_FACES_0_1 = Permutation(1, (4, 5, 0, 1, 6, 7, 2, 3))
MIRROR_PRISM_0_1 = Permutation(1, (0, 2, 1, 3, 5, 4))
MIRROR_PRISM_3_4 = Permutation(1, (3, 4, 5, 0, 1, 2))

################################################################################
## 3D Cube                                                                    ##
################################################################################
BCTcube3d = LookupGenerator(3,"cube")

# base cases cube 3D:
# 0,0,0,0,0,0,0,0 -> 00000000 # Basic Case 0
BCTcube3d.base_cases[0].name = "MC33 Case 0"
BCTcube3d.base_cases[0].faces = []
BCTcube3d.base_cases[0].exterior = []
BCTcube3d.base_cases[0].exterior_groups = []
BCTcube3d.base_cases[0].interior = [[0, 1, 2, 3, 4, 5, 6, 7]]
BCTcube3d.base_cases[0].interior_groups = [0]
# 1,0,0,0,0,0,0,0 -> 00000001 # Basic Case 1
BCTcube3d.base_cases[1].name = "MC33 Case 1"
BCTcube3d.base_cases[1].faces = [[(0, 4), (0, 1), (0, 2)]]
BCTcube3d.base_cases[1].exterior = [[0, (0, 4), (0, 1), (0, 2)]]
BCTcube3d.base_cases[1].exterior_groups = [0]
BCTcube3d.base_cases[1].interior = [[(0, 1), (0, 2), (0, 4), 1, 2, 4], [1, 2, 4, 5], [4, 2, 5, 6], [5, 6, 2, 7], [5, 2, 7, 3], [5, 2, 1, 3]]
BCTcube3d.base_cases[1].interior_groups = [1, 1, 1, 1, 1, 1]
# 1,1,0,0,0,0,0,0 -> 00000011 # Basic Case 2
BCTcube3d.base_cases[2].name = "MC33 Case 2"
BCTcube3d.base_cases[2].faces = [[(0, 2), (1, 3), (0, 4), (1, 5)]]
BCTcube3d.base_cases[2].exterior = [[0, (0, 2), (0, 4), 1, (1, 3), (1, 5)]]
BCTcube3d.base_cases[2].exterior_groups = [0]
BCTcube3d.base_cases[2].interior = [[(0, 2), (1, 3), (0, 4), (1, 5), 2, 3, 4, 5], [2, 4, 6, 3, 5, 7]]
BCTcube3d.base_cases[2].interior_groups = [1, 1]
# 0,1,1,0,0,0,0,0 -> 00000110 # Basic Case 3
BCTcube3d.base_cases[3].name = "MC33 Case 3.1"
BCTcube3d.base_cases[3].faces = [[(1, 5), (0, 1), (1, 3)], [(2, 3), (0, 2), (2, 6)]]
BCTcube3d.base_cases[3].exterior = [[1, (1, 5), (0, 1), (1, 3)], [2, (2, 3), (0, 2), (2, 6)]]
BCTcube3d.base_cases[3].exterior_groups = [0, 1]
BCTcube3d.base_cases[3].interior = [[(1, 5), (0, 1), (1, 3), 5, 0, 3], [(2, 3), (0, 2), (2, 6), 3, 0, 6], [5, 6, 7, 3], [0, 3, 5, 6], [0, 4, 5, 6]]
BCTcube3d.base_cases[3].interior_groups = [2, 2, 2, 2, 2]
# 1,1,1,0,0,0,0,0 -> 00000111 # Basic Case 5
BCTcube3d.base_cases[4].name = "MC33 Case 5"
BCTcube3d.base_cases[4].faces = [[(0, 4), (1, 5), (2, 6)], [(1, 5), (2, 6), (1, 3), (2, 3)]]
BCTcube3d.base_cases[4].exterior = [[0, 1, 2, (0, 4), (1, 5) , (2, 6)], [1, (1, 3), (1, 5), 2, (2, 3), (2, 6)]]
BCTcube3d.base_cases[4].exterior_groups = [0, 0]
BCTcube3d.base_cases[4].interior = [[(1, 3), 3, (2, 3), (1, 5), 7, (2, 6)], [(1, 5), (2, 6), 7, 6], [6, 7, 5, (1, 5)], [(2, 6), 6, (1, 5), (0, 4)], [6, (0, 4), (1, 5), 4], [4, 5, 6, (1, 5)]]
BCTcube3d.base_cases[4].interior_groups = [1, 1, 1, 1, 1, 1]
# 1,1,1,1,0,0,0,0 -> 00001111 # Basic Case 8 and its inverse
BCTcube3d.base_cases[5].name = "MC33 Case 8"
BCTcube3d.base_cases[5].faces = [[(0, 4), (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[5].exterior = [[0, 1, 2, 3, (0, 4), (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[5].exterior_groups = [0]
BCTcube3d.base_cases[5].interior = [[(0, 4), (1, 5), (2, 6), (3, 7), 4, 5, 6, 7]]
BCTcube3d.base_cases[5].interior_groups = [1]
# 0,1,1,0,1,0,0,0 -> 00010110 # Basic Case 6
BCTcube3d.base_cases[6].name = "MC33 Case 7.1"
BCTcube3d.base_cases[6].faces = [[(0, 1), (1, 3), (1, 5)], [(0, 2), (2, 6), (2, 3)], [(0, 4), (4, 5), (4, 6)]]
BCTcube3d.base_cases[6].exterior = [[1, (0, 1), (1, 3), (1, 5)], [2, (0, 2), (2, 6), (2, 3)], [4, (0, 4), (4, 5), (4, 6)]]
BCTcube3d.base_cases[6].exterior_groups = [0, 1, 2]
BCTcube3d.base_cases[6].interior = [[0, (0, 1), (0, 2), (0, 4), (1, 5), (2, 6)], [(0, 1), (1, 5), (1, 3), (0, 2), (2, 6), (2, 3)], [(1, 3), 3, (2, 3), (1, 5), 7, (2, 6)], [(1, 5), (2, 6), 7, 5], [(2, 6), 7, 5, 6], [(2, 6), (1, 5), 5, (0, 4)], [(0, 4), (2, 6), 5, 6], [(0, 4), (4, 5), (4, 6), 5], [(0, 4), 5, (4, 6), 6]]
BCTcube3d.base_cases[6].interior_groups = [3, 3, 3, 3, 3, 3, 3, 3, 3]
# 1,1,1,0,1,0,0,0 -> 00010111 # Basic Case 9 and its inverse
BCTcube3d.base_cases[7].name = "MC33 Case 9"
BCTcube3d.base_cases[7].faces = [[(1, 5), (2, 6), (4, 5), (4, 6)], [(1, 5), (2, 6), (1, 3), (2, 3)]]
BCTcube3d.base_cases[7].exterior = [[1, (1, 3), (1, 5), 2, (2, 3), (2, 6)], [4, (4, 5), (4, 6), 0, 1, 2], [1, (1, 5), (4, 5), 2, (2, 6), (4, 6)]]
BCTcube3d.base_cases[7].exterior_groups = [0, 0, 0]
BCTcube3d.base_cases[7].interior = [[5, (4, 5), (1, 5), 6, (4, 6), (2, 6)], [5, (1, 5), (1, 3), 6, (2, 6), (2, 3)], [(2, 3), 3, (1, 3), 6, 7, 5]]
BCTcube3d.base_cases[7].interior_groups = [1, 1, 1]
# 0,0,0,1,1,0,0,0 -> 00011000 # Basic Case 4
BCTcube3d.base_cases[8].name = "MC33 Case 4.1"
BCTcube3d.base_cases[8].faces = [[(0, 4), (4, 6), (4, 5)], [(1, 3), (2, 3), (3, 7)]]
BCTcube3d.base_cases[8].exterior = [[4, (0, 4), (4, 6), (4, 5)], [3, (1, 3), (2, 3), (3, 7)]]
BCTcube3d.base_cases[8].exterior_groups = [1, 0]
BCTcube3d.base_cases[8].interior = [[(0, 4), (4, 6), (4, 5), 0, 2, 1], [(4, 6), 6, 2, (4, 5), 5, 1], [(1, 3), 1, 5, (2, 3), 2, 6], [(1, 3), (2, 3), (3, 7), 5, 6, 7]]
BCTcube3d.base_cases[8].interior_groups = [2, 2, 2, 2]
# 1,0,0,1,1,0,0,0 -> 00011001 # Basic Case 6
BCTcube3d.base_cases[9].name = "MC33 Case 6.1.1"
BCTcube3d.base_cases[9].faces = [[(4, 5), (4, 6), (0, 1), (0, 2)], [(2, 3), (3, 7), (1, 3)]]
BCTcube3d.base_cases[9].exterior = [[0, (0, 1), (0, 2), 4, (4, 5), (4, 6)], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[9].exterior_groups = [0, 1]
BCTcube3d.base_cases[9].interior = [[(4, 5), (4, 6), 5, 6, (0, 1), (0, 2), 1, 2], [1, (1, 3), 5, 2, (2, 3), 6], [(1, 3), (3, 7), (2, 3), 5, 7, 6]]
BCTcube3d.base_cases[9].interior_groups = [2, 2, 2]
# 1,1,0,1,1,0,0,0 -> 00011011 # Basic Case 11 and its inverse
BCTcube3d.base_cases[10].name = "MC33 Case 11"
BCTcube3d.base_cases[10].faces = [[(3, 7), (1, 5), (2, 3)], [(2, 3), (0, 2), (1, 5)], [(1, 5), (4, 5), (0, 2)], [(4, 5), (4, 6), (0, 2)]]
BCTcube3d.base_cases[10].exterior = [[4, (4, 5), (4, 6), (0, 2)], [3, (3, 7), (2, 3), (1, 5)], [0, (0, 2), 4, (4, 5)], [1, (1, 5), (2, 3), 3], [(2, 3), 1, (1, 5), (0, 2)], [0, (0, 2), (4, 5), (1, 5)], [0, (0, 2), 1, (1, 5)]]
BCTcube3d.base_cases[10].exterior_groups = [0, 0, 0, 0, 0, 0, 0]
BCTcube3d.base_cases[10].interior = [[(4, 5), (4, 6), (0, 2), 6], [(2, 3), (3, 7), (1, 5), 7], [(4, 5), (1, 5), 5, 7], [(0, 2), (2, 3), 2, 6], [(4, 5), (2, 3), (1, 5), (0, 2)], [(1, 5), (2, 3), (4, 5), 7], [(4, 5), (2, 3), (0, 2), 6], [(4, 5), 7, 6, (2, 3)]]
BCTcube3d.base_cases[10].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1]
# 0,1,1,1,1,0,0,0 -> 00011110 # Basic Case 12 and its inverse
BCTcube3d.base_cases[11].name = "MC33 Case 12.1.1"
BCTcube3d.base_cases[11].faces = [[(0, 4), (4, 5), (4, 6)], [(0, 1), (0, 2), (1, 5), (2, 6)], [(1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].exterior = [[(0, 4), (4, 5), (4, 6), 4], [(0, 1), 1, (1, 5), (0, 2), 2, (2, 6)], [1, 2, 3, (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].exterior_groups = [1, 0, 0]
BCTcube3d.base_cases[11].interior = [[0, (0, 1), (0, 2), (0, 4), (4, 5), (4, 6)], [(0, 1), (1, 5), (4, 5), (0, 2), (2, 6), (4, 6)], [(1, 5), (4, 5), 5, (2, 6), (4, 6), 6], [(1, 5), (2, 6), (3, 7), 5, 6, 7]]
BCTcube3d.base_cases[11].interior_groups = [2, 2, 2, 2]
# 0,0,1,1,1,1,0,0 -> 00111100 # Basic Case 10 and its inverse
BCTcube3d.base_cases[12].name = "MC33 Case 10.1.1"
BCTcube3d.base_cases[12].faces = [[(0, 4), (1, 5), (4, 6), (5, 7)], [(0, 2), (1, 3), (2, 6), (3, 7)]]
BCTcube3d.base_cases[12].exterior = [[(0, 4), 4, (4, 6), (1, 5), 5, (5, 7)], [(0, 2), 2, (2, 6), (1, 3), 3, (3, 7)]]
BCTcube3d.base_cases[12].exterior_groups = [1, 0]
BCTcube3d.base_cases[12].interior = [[0, (0, 4), 6, (4, 6), 1, (1, 5), 7, (5, 7)], [0, (0, 2), 6, (2, 6), 1, (1, 3), 7, (3, 7)]]
BCTcube3d.base_cases[12].interior_groups = [2, 2]
# 1,0,0,1,0,1,1,0 -> 01101001 # Basic Case 13 and its inverse
BCTcube3d.base_cases[13].name = "MC33 Case 13.1"
BCTcube3d.base_cases[13].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 3), (2, 3), (3, 7)], [(1, 5), (4, 5), (5, 7)], [(2, 6), (4, 6), (6, 7)]]
BCTcube3d.base_cases[13].exterior = [[(0, 1), (0, 2), (0, 4), 0], [(1, 3), (2, 3), (3, 7), 3], [(1, 5), (4, 5), (5, 7), 5], [(2, 6), (4, 6), (6, 7), 6]]
BCTcube3d.base_cases[13].exterior_groups = [0, 1, 2, 3]
BCTcube3d.base_cases[13].interior = [[(0, 1), (0, 2), (0, 4), (4, 5), (4, 6), 4], [(1, 3), (2, 3), (3, 7), (5, 7), (6, 7), 7], [(1, 5), (4, 5), (5, 7), 1, (0, 1), (1, 3)], [(2, 6), (4, 6), (6, 7), 2, (0, 2), (2, 3)], [(0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 7), (6, 7)]]
BCTcube3d.base_cases[13].interior_groups = [4, 4, 4, 4, 4]

# ################################################################################
# ## MC 33 cases and MC 33 face test table for 3D Cube                          ##
# ################################################################################

# 0,1,1,0,0,0,0,0 -> 00000110 # MC33 Case 3.2
BCTcube3d.base_cases[3].mc33.append(Triangulation())
BCTcube3d.base_cases[3].mc33[-1].name = "MC33 Case 3.2"
BCTcube3d.base_cases[3].mc33[-1].faces = [[(0, 2), (2, 6), (0, 1), (1, 5)], [(2, 6), (2, 3), (1, 5), (1, 3)]]
BCTcube3d.base_cases[3].mc33[-1].exterior = [[1, (0, 1), (1, 5), (1, 3)], [2, (0, 2), (2, 6), (2, 3)], [(0, 1), (1, 5), (1, 3), (0, 2), (2, 6), (2, 3)]]
BCTcube3d.base_cases[3].mc33[-1].exterior_groups = [0, 0, 0]
BCTcube3d.base_cases[3].mc33[-1].interior = [[(0, 2), (2, 6), 6, (0, 1), (1, 5), 5], [(2, 6), (2, 3), 6, (1, 5), (1, 3), 5], [(0, 1), (0, 2), 0, 5, 6, 4], [(1, 3), (2, 3), 3, 5, 6, 7]]
BCTcube3d.base_cases[3].mc33[-1].interior_groups = [1, 1, 1, 1]
BCTcube3d.base_cases[3].tests = binaryheap((TEST_FACE_4, 0, CASE_IS_REGULAR))
# 0,0,0,1,1,0,0,0 -> 00011000 # MC Case 4.2
BCTcube3d.base_cases[8].mc33.append(Triangulation())
BCTcube3d.base_cases[8].mc33[-1].name = "MC33 Case 4.2"
BCTcube3d.base_cases[8].mc33[-1].faces = [[(0, 4), (4, 5), (1, 3)], [(1, 3), (3, 7), (4, 5)], [(4, 5), (3, 7), (4, 6)], [(0, 4), (4, 6), (2, 3)], [(0, 4), (1, 3), (2, 3)], [(2, 3), (3, 7), (4, 6)]]
BCTcube3d.base_cases[8].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(1, 3), (2, 3), (3, 7), 3], [(0, 4), (4, 5), (4, 6), (3, 7)], [(1, 3), (2, 3), (3, 7), (0, 4)], [(0, 4), (4, 5), (1, 3), (3, 7)], [(0, 4), (4, 6), (2, 3), (3, 7)]]
BCTcube3d.base_cases[8].mc33[-1].exterior_groups = [0, 0, 0, 0, 0, 0]
BCTcube3d.base_cases[8].mc33[-1].interior = [[(0, 4), (4, 5), (1, 3), 1], [(1, 3), (3, 7), (4, 5), 5], [(4, 5), (4, 6), (3, 7), 7], [(3, 7), (2, 3), (4, 6), 6], [(0, 4), (4, 6), (2, 3), 2], [(2, 3), (1, 3), (0, 4), 0], [0, (0, 4), (1, 3), 1], [(4, 5), 5, 1, (1, 3)], [(4, 5), 5, (3, 7), 7], [(0, 4), 0, (2, 3), 2], [(4, 6), 6, 2, (2, 3)], [(4, 6), 6, (3, 7), 7]]
BCTcube3d.base_cases[8].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BCTcube3d.base_cases[8].tests = binaryheap((TEST_INTERIOR_3_4, 0, CASE_IS_REGULAR))
# 1,0,0,1,1,0,0,0 -> 00011001 # MC33 Case 6.1.2
BCTcube3d.base_cases[9].mc33.append(Triangulation())
BCTcube3d.base_cases[9].mc33[-1].name = "MC33 Case 6.1.2"
BCTcube3d.base_cases[9].mc33[-1].faces = [[(0, 1), (Face1, 0), (4, 5)], [(4, 5), (Face1, 4), (Face1, 0)], [(Face1, 4), (Face1, 0), (3, 7)], [(Face1, 0), (1, 3), (3, 7)], [(4, 5), (Face3, 4), (Face1, 4)], [(4, 5), (4, 6), (Face3, 4)], [(Face1, 4), (Face3, 4), (3, 7)], [(0, 2), (Face3, 0), (4, 6)], [(Face3, 0), (Face3, 4), (4, 6)], [(Face3, 0), (Face3, 4), (3, 7)], [(Face3, 0), (2, 3), (3, 7)], [(0, 1), (0, 2), (Face1, 0)], [(0, 2), (Face3, 0), (Face1, 0)], [(Face1, 0), (Face3, 0), (1, 3)], [(1, 3), (2, 3), (Face3, 0)]]
BCTcube3d.base_cases[9].mc33[-1].exterior = [[0, (0, 1), (0, 2), 4], [4, (4, 5), (4, 6), (0, 2)], [(0, 1), (0, 2), 4, (4, 5)], [(0, 1), (0, 2), (4, 5), (Face1, 0)], [(4, 5), (4, 6), (0, 2), (Face3, 0)], [(0, 2), (Face1, 0), (Face3, 0), (4, 5)], [(Face1, 0), (Face3, 0), (Face1, 4), (4, 5)], [(4, 5), (Face1, 4), (Face3, 0), (Face3, 4)], [(4, 5), (4, 6), (Face3, 0), (Face3, 4)], [(Face1, 0), (Face3, 0), (1, 3), (3, 7)], [(Face3, 0), (2, 3), (1, 3), (3, 7)], [(Face1, 0), (Face3, 0), (Face1, 4), (3, 7)], [(Face3, 0), (Face1, 4), (Face3, 4), (3, 7)], [(1, 3), (2, 3), 3, (3, 7)]]
BCTcube3d.base_cases[9].mc33[-1].exterior_groups = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
BCTcube3d.base_cases[9].mc33[-1].interior = [[(0, 1), (0, 2), (Face1, 0), (1, 3)], [(0, 2), (Face1, 0), (Face3, 0), (1, 3)], [(0, 1), (1, 3), (Face1, 0), 1], [(1, 3), (2, 3), (0, 2), (Face3, 0)], [(0, 2), (2, 3), (Face3, 0), 2], [(0, 1), 1, (Face1, 0), (4, 5)], [(0, 2), 2, (Face3, 0), (4, 6)], [1, (Face1, 0), (Face1, 4), (4, 5)], [2, (Face3, 0), (Face3, 4), (4, 6)], [1, (4, 5), 5, (Face1, 4)], [2, (4, 6), 6, (Face3, 4)], [1, (Face1, 0), (1, 3), (Face1, 4)], [2, (Face3, 0), (2, 3), (Face3, 4)], [(Face1, 0), (1, 3), (3, 7), (Face1, 4)], [(Face3, 0), (2, 3), (3, 7), (Face3, 4)], [1, (1, 3), (Face1, 4), 5], [2, (2, 3), (Face3, 4), 6], [(Face1, 4), (1, 3), (3, 7), 5], [(Face3, 4), (2, 3), (3, 7), 6], [(4, 5), (4, 6), (Face3, 4), 6], [(4, 5), (Face3, 4), (Face1, 4), 5], [(Face3, 4), 6, (4, 5), 5], [5, (Face3, 4), 6, (3, 7)], [5, (Face1, 4), (Face3, 4), (3, 7)], [5, 6, (3, 7), 7]]
BCTcube3d.base_cases[9].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# version with center at the bottom:
#BCTcube3d.base_cases[9].mc33.append(Triangulation())
#BCTcube3d.base_cases[9].mc33[-1].name = "MC33 Case 6.1.2"
#BCTcube3d.base_cases[9].mc33[-1].faces = [[(0, 1), (0, 2), (Center, 2)], [(Center, 1), (Center, 2), (0, 1)], [(0, 2), (Center, 2), (4, 6)], [(0, 1), (Center, 1), (4, 5)], [(1, 3), (2, 3), (Center, 1)], [(Center, 1), (Center, 2), (2, 3)], [(1, 3), (Center, 1), (3, 7)], [(2, 3), (Center, 2), (3, 7)], [(Center, 1), (4, 5), (3, 7)], [(Center, 2), (4, 6), (3, 7)], [(4, 5), (4, 6), (3, 7)]]
#BCTcube3d.base_cases[9].mc33[-1].exterior = [[(1, 3), (2, 3), (3, 7), 3], [(2, 3), (1, 3), (3, 7), (Center, 1)], [(Center, 1), (Center, 2), (2, 3), (3, 7)], [0, (0, 1), (0, 2), (4, 5)], [0, (0, 2), 4, (4, 5)], [4, (4, 6), (4, 5), (0, 2)], [(0, 1), (0, 2), (Center, 2), (4, 5)], [(0, 1), (Center, 1), (Center, 2), (4, 5)], [(Center, 2), (0, 2), (4, 5), (4, 6)], [(4, 5), (Center, 1), (Center, 2), (3, 7)], [(4, 5), (4, 6), (Center, 2), (3, 7)]]
#BCTcube3d.base_cases[9].mc33[-1].exterior_groups = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#BCTcube3d.base_cases[9].mc33[-1].interior = [[(0, 1), 1, (1, 3), (Center, 1)], [(0, 2), 2, (2, 3), (Center, 2)], [(0, 1), 1, (Center, 1), (4, 5)], [(0, 2), 2, (Center, 2), (4, 6)], [1, (1, 3), (Center, 1), (3, 7)], [2, (2, 3), (Center, 2), (3, 7)], [(0, 1), (2, 3), (1, 3), (Center, 1)], [(0, 1), (0, 2), (Center, 2), (2, 3)], [(0, 1), (Center, 1), (Center, 2), (2, 3)], [1, (4, 5), (3, 7), (Center, 1)], [2, (4, 6), (3, 7), (Center, 2)], [(4, 5), 1, (3, 7), 5], [(4, 6), 2, (3, 7), 6], [(4, 5), (4, 6), (3, 7), 7], [(4, 5), 5, (3, 7), 7], [(4, 6), 6, (3, 7), 7]]
#BCTcube3d.base_cases[9].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# 1,0,0,1,1,0,0,0 -> 00011001 # MC33 Case 6.2
BCTcube3d.base_cases[9].mc33.append(Triangulation())
BCTcube3d.base_cases[9].mc33[-1].name = "MC33 Case 6.2"
BCTcube3d.base_cases[9].mc33[-1].faces = [[(0, 1), (Face4, 5), (4, 5)], [(0, 1), (Face4, 5), (1, 3)], [(Face4, 5), (3, 7), (1, 3)], [(4, 5), (4, 6), (Face4, 5)], [(4, 6), (Face4, 5), (Face4, 6)], [(Face4, 5), (Face4, 6), (3, 7)], [(3, 7), (Face4, 6), (2, 3)], [(2, 3), (0, 2), (Face4, 6)], [(Face4, 6), (0, 2), (4, 6)]]
BCTcube3d.base_cases[9].mc33[-1].exterior = [[3, (1, 3), (2, 3), (3, 7)], [(1, 3), (2, 3), (3, 7), (Face4, 6)], [(Face4, 6), (Face4, 5), (3, 7), (1, 3)], [(Face4, 6), (2, 3), (1, 3), (0, 2)], [(Face4, 5), (Face4, 6), (1, 3), (0, 2)], [(Face4, 5), (1, 3), (0, 2), (0, 1)], [(0, 2), (Face4, 6), (Face4, 5), (4, 6)], [(0, 2), (0, 1), (Face4, 5), (4, 6)], [(4, 5), (4, 6), (0, 1), (Face4, 5)], [0, (0, 1), (0, 2), (4, 6)], [0, (4, 6), 4, (0, 1)], [4, (4, 6), (4, 5), (0, 1)]]
BCTcube3d.base_cases[9].mc33[-1].exterior_groups = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
BCTcube3d.base_cases[9].mc33[-1].interior = [[1, (0, 1), (1, 3), (Face4, 5)], [2, (0, 2), (2, 3), (Face4, 6)], [(0, 1), 1, (Face4, 5), (4, 5)], [(0, 2), 2, (Face4, 6), (4, 6)], [(1, 3), (3, 7), (Face4, 5), 5], [(2, 3), (3, 7), (Face4, 6), 6], [(3, 7), (Face4, 5), (Face4, 6), (4, 6)], [(3, 7), (Face4, 6), 6, (4, 6)], [5, (4, 5), (Face4, 5), (3, 7)], [(4, 5), (4, 6), (Face4, 5), (3, 7)], [5, (4, 5), (3, 7), 7], [(4, 5), (4, 6), (3, 7), 7], [(4, 6), 6, (3, 7), 7], [1, (1, 3), (Face4, 5), 5], [1, (Face4, 5), 5, (4, 5)], [2, (2, 3), (Face4, 6), 6], [2, (Face4, 6), (4, 6), 6]]
BCTcube3d.base_cases[9].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BCTcube3d.base_cases[9].tests = binaryheap((TEST_FACE_4,
                                            1,
                                            (TEST_INTERIOR_3_4, 0, CASE_IS_REGULAR)
                                            ))
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2 (face 0, 2 inside; face 4 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2 face 0 and 2 inside"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 4), (4, 5), (4, 6)], [(0, 1), (1, 5), (0, 2), (2, 6)], [(1, 3), (1, 5), (2, 3), (2, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[(0, 4), (4, 5), (4, 6), 4], [(0, 1), 1, (1, 3), (1, 5)], [(0, 2), 2, (2, 3), (2, 6)], [(0, 2), (2, 6), (2, 3), (0, 1), (1, 5), (1, 3)]]
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = [0, 1, 1, 1]
BCTcube3d.base_cases[6].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4), (1, 5), (2, 6)], [(1, 3), 3, (2, 3), (1, 5), 7, (2, 6)], [(2, 6), (1, 5), 7, 6], [5, 6, 7, (1, 5)], [(0, 4), (1, 5), (2, 6), 6], [(0, 4), (1, 5), 6, 5], [(4, 5), 5, 6, (0, 4)], [(4, 5), (4, 6), 6, (0, 4)]]
BCTcube3d.base_cases[6].mc33[-1].interior_groups = [2, 2, 2, 2, 2, 2, 2, 2]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2 (face 2, 4 inside; face 0 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2 face 2 and 4 inside"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[0].faces, MIRROR_FACES_0_TO_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[0].exterior, MIRROR_FACES_0_TO_4)
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = BCTcube3d.base_cases[6].mc33[0].exterior_groups
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[0].interior, MIRROR_FACES_0_TO_4)
BCTcube3d.base_cases[6].mc33[-1].interior_groups = BCTcube3d.base_cases[6].mc33[0].interior_groups
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2 (face 0, 4 inside; face 2 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2 face 0 and 4 inside"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[1].faces, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[1].exterior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = BCTcube3d.base_cases[6].mc33[1].exterior_groups
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[1].interior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[6].mc33[-1].interior_groups = BCTcube3d.base_cases[6].mc33[1].interior_groups
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 0 inside; face 2, 4 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3 face 0 inside"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(4, 5), (4, 6), (Face2, 6)], [(4, 5), (Face2, 6), (Face4, 5)], [(4, 5), (Face4, 5), (1, 5)], [(Face4, 5), (1, 5), (1, 3)], [(1, 3), (Face4, 5), (2, 3)], [(Face4, 5), (Face4, 6), (2, 3)], [(Face4, 6), (2, 3), (2, 6)], [(0, 4), (4, 6), (Face2, 6)], [(0, 4), (Face2, 6), (0, 1)], [(0, 1), (Face2, 6), (Face4, 5)], [(0, 1), (Face4, 5), (Face4, 6)], [(0, 1), (0, 2), (Face4, 6)], [(0, 2), (Face4, 6), (2, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [1, (0, 1), (1, 3), (1, 5)], [2, (0, 2), (2, 3), (2, 6)], [(0, 4), (4, 5), (4, 6), (Face2, 6)], [(0, 2), (2, 3), (2, 6), (Face4, 6)], [(0, 1), (1, 3), (1, 5), (Face4, 5)], [(0, 4), (4, 5), (Face2, 6), (0, 1)], [(0, 1), (1, 5), (4, 5), (Face4, 5)], [(4, 5), (0, 1), (Face2, 6), (Face4, 5)], [(0, 1), (1, 3), (Face4, 5), (2, 3)], [(0, 1), (2, 3), (0, 2), (Face4, 6)], [(Face4, 5), (0, 1), (2, 3), (Face4, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
BCTcube3d.base_cases[6].mc33[-1].interior = [[(0, 1), (Face4, 6), (Face4, 5), (Face2, 6)], [(Face2, 6), (Face4, 6), (0, 1), (0, 2)], [(0, 2), (0, 4), (4, 6), (Face2, 6)], [(Face2, 6), (4, 6), (0, 2), (2, 6)], [(0, 2), (Face2, 6), (Face4, 6), (2, 6)], [(Face2, 6), (0, 1), (0, 2), (0, 4)], [0, (0, 1), (0, 2), (0, 4)], [(1, 3), (2, 3), 3, 7], [(1, 3), (2, 3), 7, (Face4, 5)], [(Face4, 5), (Face4, 6), (2, 3), 7], [(Face4, 5), (Face4, 6), (Face2, 6), 7], [(1, 3), (1, 5), (Face4, 5), 7], [(1, 5), (Face4, 5), 7, (4, 5)], [(4, 5), 7, (1, 5), 5], [(Face4, 5), (Face2, 6), (4, 5), 7], [(2, 3), (2, 6), (Face4, 6), 7], [(Face4, 6), (Face2, 6), 7, (2, 6)], [(4, 5), (4, 6), (Face2, 6), 7], [(2, 6), (4, 6), (Face2, 6), 7], [7, 6, (4, 6), (2, 6)]]
BCTcube3d.base_cases[6].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 2 inside; face 0, 4 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3, face 2 inside"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[3].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[3].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = BCTcube3d.base_cases[6].mc33[3].exterior_groups
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[3].interior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].interior_groups = BCTcube3d.base_cases[6].mc33[3].interior_groups
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 4 inside; face 0, 2 outside)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3, face 4 inside"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[4].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[4].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = BCTcube3d.base_cases[6].mc33[4].exterior_groups
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[4].interior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].interior_groups = BCTcube3d.base_cases[6].mc33[4].interior_groups
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.4.1
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.4.1"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 3), (1, 5), (4, 5)], [(4, 5), (2, 3), (1, 3)], [(4, 5), (4, 6), (2, 3)], [(4, 6), (2, 3), (2, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[1, (0, 1), (1, 3), (1, 5)], [2, (0, 2), (2, 3), (2, 6)], [4, (0, 4), (4, 5), (4, 6)], [(0, 1), (0, 2), (0, 4), (2, 3)], [(0, 1), (0, 4), (2, 3), (1, 3)], [(0, 1), (0, 4), (1, 3), (1, 5)], [(0, 2), (2, 3), (2, 6), (0, 4)], [(0, 4), (4, 5), (4, 6), (2, 3)], [(0, 4), (2, 3), (1, 3), (4, 5)], [(0, 4), (4, 5), (1, 5), (1, 3)], [(0, 4), (4, 6), (2, 6), (2, 3)]]
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BCTcube3d.base_cases[6].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 3), (4, 5), (1, 5), 5], [(2, 3), (2, 6), (4, 6), 6], [(1, 3), (2, 3), 3, 7], [(1, 3), (2, 3), (4, 5), 7], [(4, 5), (4, 6), (2, 3), 7], [(1, 3), 7, (4, 5), 5], [(2, 3), 7, (4, 6), 6]]
BCTcube3d.base_cases[6].mc33[-1].interior_groups = [0, 2, 2, 2, 2, 2, 2, 2]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.4.2
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.4.2"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(Center, 4), (4, 5), (4, 6)], [(Center, 1), (1, 5), (1, 3)], [(Center, 2), (2, 6), (2, 3)], [(0, 1), (0, 4), (Center, 4)], [(0, 1), (Center, 4), (Center, 1)], [(Center, 4), (Center, 1), (4, 5)], [(Center, 1), (4, 5), (1, 5)], [(0, 2), (0, 4), (Center, 4)], [(0, 2), (Center, 2), (Center, 4)], [(Center, 2), (Center, 4), (4, 6)], [(4, 6), (Center, 2), (2, 6)], [(0, 1), (0, 2), (Center, 1)], [(0, 2), (Center, 2), (Center, 1)], [(Center, 2), (Center, 1), (1, 3)], [(2, 3), (1, 3), (Center, 2)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), (Center, 4)], [2, (0, 2), (2, 3), (2, 6)], [(0, 2), (2, 3), (2, 6), (Center, 2)], [1, (0, 1), (1, 3), (1, 5)], [(0, 1), (1, 3), (1, 5), (Center, 1)], [(0, 4), (4, 5), (Center, 4), (0, 1)], [(0, 1), (1, 3), (Center, 1), (0, 2)], [(0, 1), (1, 5), (Center, 1), (4, 5)], [(0, 2), (2, 3), (Center, 2), (1, 3)], [(Center, 1), (1, 3), (0, 2), (Center, 2)], [(Center, 1), (0, 1), (Center, 4), (4, 5)], [(Center, 4), (0, 4), (0, 2), (4, 6)], [(Center, 2), (0, 2), (Center, 4), (4, 6)], [(0, 2), (2, 6), (Center, 2), (4, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior_groups = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
BCTcube3d.base_cases[6].mc33[-1].interior = [[(0, 1), (0, 2), (Center, 1), (Center, 4)], [(0, 1), (0, 2), (0, 4), (Center, 4)], [(Center, 1), (Center, 2), (Center, 4), (0, 2)], [0, (0, 1), (0, 2), (0, 4)], [(4, 5), (4, 6), (Center, 4), 7], [(1, 5), (1, 3), (Center, 1), 7], [(2, 3), (2, 6), (Center, 2), 7], [(Center, 1), (Center, 2), (Center, 4), 7], [(4, 5), (Center, 1), (Center, 4), 7], [(1, 3), (Center, 1), (Center, 2), 7], [(4, 6), (Center, 4), (Center, 2), 7], [(4, 5), (1, 5), (Center, 1), 7], [(1, 3), (2, 3), (Center, 2), 7], [(Center, 2), (2, 6), (4, 6), 7], [(4, 5), (1, 5), 7 , 5], [(1, 3), (2, 3), 7, 3], [(2, 6), (4, 6), 6, 7]]
BCTcube3d.base_cases[6].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BCTcube3d.base_cases[6].tests = binaryheap((TEST_FACE_0,
                                            (TEST_FACE_2,
                                             (TEST_FACE_4,
                                              (TEST_INTERIOR_0_4, 7, 6),
                                              5),
                                             (TEST_FACE_4, 4, 1)),
                                            (TEST_FACE_2,
                                             (TEST_FACE_4, 3, 2),
                                             (TEST_FACE_4, 0, CASE_IS_REGULAR))))
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.1.1 rotated
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].name = "MC33 Case 10.1.1"
BCTcube3d.base_cases[12].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[12].faces, ROTATE_FACES_0_1)
BCTcube3d.base_cases[12].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[12].interior, ROTATE_FACES_0_1)
BCTcube3d.base_cases[12].mc33[-1].exterior_groups = BCTcube3d.base_cases[12].interior_groups
BCTcube3d.base_cases[12].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[12].exterior, ROTATE_FACES_0_1)
BCTcube3d.base_cases[12].mc33[-1].interior_groups = BCTcube3d.base_cases[12].exterior_groups
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.2 and its inverse (face 1 inside; face 0 outside) 
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].name = "MC33 Case 10.2 0 in 1 out"
BCTcube3d.base_cases[12].mc33[-1].faces = [[(0, 4), (1, 5), (Face1, 0)], [(0, 4), (Face1, 0), (Face1, 6)], [(0, 4), (Face1, 6), (4, 6)], [(4, 6), (Face1, 6), (5, 7)], [(1, 3), (0, 2), (Face1, 0)], [(Face1, 0), (Face1, 6), (0, 2)], [(0, 2), (2, 6), (Face1, 6)], [(2, 6), (3, 7), (Face1, 6)], [(3, 7), (Face1, 6), (5, 7)], [(1, 3), (1, 5), (Face1, 0)]]
BCTcube3d.base_cases[12].mc33[-1].exterior = [[(0, 2), (2, 6), (Face1, 6), 3], [(0, 2), (2, 6), 2, 3], [(Face1, 6), (3, 7), (2, 6), 3], [(0, 2), 3, (Face1, 6), (Face1, 0)], [(0, 2), (Face1, 0), (1, 3), 3], [(1, 3), (Face1, 0), 3, (1, 5)], [3, (3, 7), (Face1, 6), (5, 7)], [(Face1, 0), (Face1, 6), (5, 7), 3], [(1, 5), (5, 7), (Face1, 0), 3], [(Face1, 6), (5, 7), (0, 4), (4, 6)], [(0, 4), (Face1, 0), (Face1, 6), (5, 7)], [(0, 4), (1, 5), (5, 7), (Face1, 0)], [(0, 4), (1, 5), (5, 7), 5], [4, (0, 4), 5, (5, 7)], [(0, 4), (4, 6), 4, (5, 7)]]
BCTcube3d.base_cases[12].mc33[-1].exterior_groups = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
BCTcube3d.base_cases[12].mc33[-1].interior = [[(3, 7), (5, 7), (Face1, 6), 6], [(1, 3), (1, 5), (Face1, 0), 0], [(1, 3), 0, 1, (1, 5)], [7, (5, 7), (3, 7), 6], [(Face1, 0), (Face1, 6), (0, 2), (0, 4)], [(Face1, 0), 0, (0, 2), (0, 4)], [(Face1, 6), (3, 7), (2, 6), 6], [(Face1, 6), (5, 7), 6, (4, 6)], [(2, 6), (4, 6), (Face1, 6), 6], [(Face1, 6), (0, 4), (4, 6), (2, 6)], [(Face1, 6), (2, 6), (0, 2), (0, 4)], [(Face1, 0), (0, 2), 0, (1, 3)], [0, (0, 4), (1, 5), (Face1, 0)]]
BCTcube3d.base_cases[12].mc33[-1].interior_groups = [1,1,1,1,1,1,1,1,1,1,1,1,1]
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.2 and its inverse (face 0 inside; face 1 outside) 
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].name = "MC33 Case 10.2 1 in 0 out"
BCTcube3d.base_cases[12].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[12].mc33[1].faces, Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6)))
BCTcube3d.base_cases[12].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[12].mc33[1].exterior, Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6)))
BCTcube3d.base_cases[12].mc33[-1].exterior_groups = BCTcube3d.base_cases[12].mc33[1].exterior_groups
BCTcube3d.base_cases[12].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[12].mc33[1].interior, Permutation(-1, (1, 0, 3, 2, 5, 4, 7, 6)))
BCTcube3d.base_cases[12].mc33[-1].interior_groups = BCTcube3d.base_cases[12].mc33[1].interior_groups
# 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.1.2
BCTcube3d.base_cases[12].mc33.append(Triangulation())
BCTcube3d.base_cases[12].mc33[-1].name = "MC33 Case 10.1.2"
BCTcube3d.base_cases[12].mc33[-1].faces = [[(0, 4), (Center, 0), (1, 5), (Center, 1)], [(Center, 0), (0, 2), (Center, 1), (1, 3)], [(0, 4), (4, 6), (Center, 0), (Center, 6)], [(Center, 0), (Center, 6), (0, 2), (2, 6)], [(1, 5), (5, 7), (Center, 1), (Center, 7)], [(Center, 1), (Center, 7), (1, 3), (3, 7)], [(4, 6), (5, 7), (Center, 6), (Center, 7)], [(Center, 6), (Center, 7), (2, 6), (3, 7)]]
BCTcube3d.base_cases[12].mc33[-1].exterior = [[4, (0, 4), (4, 6), 5, (1, 5), (5, 7)], [(0, 4), (1, 5), (4, 6), (5, 7), (Center, 0), (Center, 1), (Center, 6), (Center, 7)], [(Center, 0), (Center, 1), (Center, 6), (Center, 7), (0, 2), (1, 3), (2, 6), (3, 7)], [(0, 2), 2, (2, 6), (1, 3), 3, (3, 7)]]
BCTcube3d.base_cases[12].mc33[-1].exterior_groups = [0, 0, 0, 0]
BCTcube3d.base_cases[12].mc33[-1].interior = [[0, (Center, 0), (0, 4), 1, (Center, 1), (1, 5)], [0, (Center, 0), (0, 2), 1, (Center, 1), (1, 3)], [1, (1, 3), (1, 5), (Center, 1)], [(1, 3), (1, 5), (Center, 1), (3, 7), (5, 7), (Center, 7)], [0, (0, 2), (0, 4), (Center, 0)], [(0, 2), (0, 4), (Center, 0), (2, 6), (4, 6), (Center, 6)], [(Center, 6), (4, 6), 6, (Center, 7), (5, 7), 7], [(Center, 6), (2, 6), 6, (Center, 7), (3, 7), 7], [(2, 6), (Center, 6), (4, 6), 6], [(3, 7), (5, 7), 7, (Center, 7)]]
BCTcube3d.base_cases[12].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BCTcube3d.base_cases[12].tests = binaryheap((TEST_FACE_0,
                                             (TEST_FACE_1, 0, 2),
                                             (TEST_FACE_1,
                                              1,
                                              (TEST_INTERIOR_2_0, 3, CASE_IS_REGULAR))))
# 0,1,1,1,1,0,0,0 -> 00011110 # Inverse of MC33 Case 12.1.1
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.1.1 inv"
BCTcube3d.base_cases[11].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[11].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[11].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[11].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[11].mc33[-1].exterior_groups = BCTcube3d.base_cases[11].interior_groups
BCTcube3d.base_cases[11].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[11].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[11].mc33[-1].interior_groups = BCTcube3d.base_cases[11].exterior_groups
#BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 5), (2, 6), (4, 5), (4, 6)], [(1, 5), (2, 6), (3, 7)]]
#BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(1, 5), (2, 6), (4, 5), (4, 6), (0, 4)], [(0, 1), (0, 2), (1, 5), (2, 6), (0, 4)], [(0, 1), 1, (1, 5), (0, 2), 2 , (2, 6)], [1, 2, 3, (1, 5), (2, 6), (3, 7)]]
#BCTcube3d.base_cases[11].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 5), 5, (4, 5), (2, 6), 6, (4, 6)], [(1, 5), (2, 6), (3, 7), 5, 6, 7]]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.1.2 and its inverse
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.1.2"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 2), (0, 1), ((0, 4), 3)], [((0, 4), 3), (0, 1), ((4, 5), 3)], [(0, 1), (1, 5), ((4, 5), 3)], [((4, 5), 3), (1, 5), (3, 7)], [((4, 5), 3), ((4, 6), 3), (3, 7)], [(2, 6), ((4, 6), 3), (3, 7)], [((4, 6), 3), (2, 6), (0, 2)], [(0, 2), ((0, 4), 3), ((4, 6), 3)], [(0, 4), ((0, 4), 3), (4, 5)], [((0, 4), 3), (4, 5), ((4, 5), 3)], [(4, 5), (4, 6), ((4, 5), 3)], [(4, 6), ((4, 5), 3), ((4, 6), 3)], [(4, 6), ((4, 6), 3), ((0, 4), 3)], [((0, 4), 3), (4, 6), (0, 4)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (4, 5), (4, 6), (0, 4)], [(0, 1), (0, 2), 3, ((0, 4), 3)], [1, 3, (0, 1), (1, 5)], [3, 2, (0, 2), (2, 6)], [(0, 1), ((0, 4), 3), ((4, 5), 3), 3], [3, (0, 2), ((0, 4), 3), ((4, 6), 3)], [((0, 4), 3), ((4, 5), 3), ((4, 6), 3), 3], [(1, 5), (0, 1), ((4, 5), 3), 3], [(0, 2), 3, (2, 6), ((4, 6), 3)], [3, (1, 5), ((4, 5), 3), (3, 7)], [3, (3, 7), ((4, 5), 3), ((4, 6), 3)], [3, (3, 7), ((4, 6), 3), (2, 6)], [(0, 4), (4, 5), (4, 6), ((0, 4), 3)], [(4, 5), (4, 6), ((0, 4), 3), ((4, 5), 3)], [((0, 4), 3), ((4, 5), 3), ((4, 6), 3), (4, 6)]]
BCTcube3d.base_cases[11].mc33[-1].exterior_groups = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
BCTcube3d.base_cases[11].mc33[-1].interior = [[(0, 2), (0, 1), 0, (0, 4)], [(0, 1), (0, 2), (0, 4), ((0, 4), 3)], [(0, 2), ((0, 4), 3), (0, 4), (4, 6)], [((0, 4), 3), ((4, 6), 3), (0, 2), (4, 6)], [(0, 2), ((4, 6), 3), (2, 6), (4, 6)], [(2, 6), (4, 6), 6, ((4, 6), 3)], [(2, 6), 6, ((4, 6), 3), (3, 7)], [((4, 6), 3), (4, 6), 6, (3, 7)], [((4, 6), 3), ((4, 5), 3), (4, 6), (3, 7)], [(3, 7), 7, (4, 6), 6], [(4, 6), (4, 5), ((4, 5), 3), (3, 7)], [(4, 5), (4, 6), (3, 7), 7], [(0, 4), (0, 1), ((0, 4), 3), (4, 5)], [((0, 4), 3), (4, 5), ((4, 5), 3), (0, 1)], [(0, 1), (1, 5), ((4, 5), 3), (4, 5)], [((4, 5), 3), (4, 5), (1, 5), (3, 7)], [(4, 5), (3, 7), (1, 5), 5], [5, (4, 5), (3, 7), 7]]
BCTcube3d.base_cases[11].mc33[-1].interior_groups = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.2 and its inverse (face 2 inside; face 0 outside) 
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.2 0 in 2 out"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 4), (4, 6), (Face0, 1)], [(4, 6), (4, 5), (Face0, 1)], [(0, 4), (0, 1), (Face0, 1)], [(4, 5), (1, 5), (Face0, 1)], [(Face0, 1), (3, 7), (1, 5)], [(0, 1), (Face0, 1), (Face0, 3)], [(3, 7), (Face0, 1), (Face0, 3)], [(0, 1), (0, 2), (Face0, 3)], [(0, 2), (2, 6), (Face0, 3)], [(Face0, 3), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), (Face0, 1)], [(0, 4), (4, 5), (Face0, 1), 1], [2, 3, (0, 2), (Face0, 3)], [2, 3, (2, 6), (Face0, 3)], [3, (2, 6), (Face0, 3), (3, 7)], [(0, 1), 1, (0, 4), (Face0, 1)], [(4, 5), 1, (1, 5), (Face0, 1)], [(0, 2), (0, 1), (Face0, 3), 3], [(0, 1), 3, (Face0, 1), (Face0, 3)], [(Face0, 1), (Face0, 3), 3, (3, 7)], [1, 3, (0, 1), (Face0, 1)], [1, 3, (3, 7), (Face0, 1)], [1, (3, 7), (Face0, 1), (1, 5)], [2, (0, 2), (2, 6), (Face0, 3)]]
BCTcube3d.base_cases[11].mc33[-1].exterior_groups = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
BCTcube3d.base_cases[11].mc33[-1].interior = [[(Face0, 1), (0, 1), (0, 4), 0], [(0, 1), 0, (Face0, 1), (Face0, 3)], [(0, 1), 0, (0, 2), (Face0, 3)], [0, (Face0, 1), (Face0, 3), (0, 4)], [(Face0, 1), (Face0, 3), (0, 4), (4, 6)], [0, (0, 2), (0, 4), (Face0, 3)], [(0, 2), (0, 4), (4, 6), (Face0, 3)], [(0, 2), (2, 6), (4, 6), (Face0, 3)], [6, 7, (4, 6), (2, 6)], [(Face0, 3), (3, 7), (2, 6), 7], [(4, 6), (2, 6), (Face0, 3), 7], [(Face0, 1), (Face0, 3), (3, 7), 7], [(Face0, 1), (Face0, 3), 7, (4, 6)], [(3, 7), 7, (1, 5), (Face0, 1)], [(Face0, 1), 7, (4, 5), (4, 6)], [(Face0, 1), 7, (4, 5), (1, 5)], [(1, 5), 7, (4, 5), 5]]
BCTcube3d.base_cases[11].mc33[-1].interior_groups = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.2 and its inverse (face 0 inside; face 2 outside) 
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.2 2 in 0 out"
BCTcube3d.base_cases[11].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[11].mc33[2].faces, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[2].exterior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].mc33[-1].exterior_groups = BCTcube3d.base_cases[11].mc33[2].exterior_groups
BCTcube3d.base_cases[11].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[2].interior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].mc33[-1].interior_groups = BCTcube3d.base_cases[11].mc33[2].interior_groups
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.1.2 inverse
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.1.2 inv"
BCTcube3d.base_cases[11].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[11].mc33[1].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[11].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[1].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[11].mc33[-1].exterior_groups = BCTcube3d.base_cases[11].mc33[1].interior_groups
BCTcube3d.base_cases[11].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[1].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[11].mc33[-1].interior_groups = BCTcube3d.base_cases[11].mc33[1].exterior_groups
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.1.1 inverse (face 0, 2 outside) 
BCTcube3d.base_cases[11].tests = binaryheap((TEST_FACE_0,
                                             (TEST_FACE_2, 
                                              (TEST_INTERIOR_0_4, 4, 0),
                                              3),
                                             (TEST_FACE_2,
                                              2,
                                              (TEST_INTERIOR_3_4, 1, CASE_IS_REGULAR))))
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 5, 1, 2, 3, 4 inside; 0 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 5, 1, 2, 3, 4 inside; 0 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = [[(2, 3), (1, 3), (3, 7)], [(5, 7), (1, 5), (4, 5)], [(0, 1), (0, 4), (4, 6)], [(4, 6), (6, 7), (0, 1)], [(0, 1), (6, 7), (2, 6)], [(0, 1), (0, 2), (2, 6)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[3, (1, 3), (2, 3), (3, 7)], [5, (4, 5), (1, 5), (5, 7)], [(6, 7), (4, 6), (2, 6), (0, 1)], [(4, 6), (2, 6), (6, 7), 6], [(0, 2), (0, 1), (2, 6), (4, 6)], [(0, 2), (0, 4), (0, 1), (4, 6)], [(0, 2), (0, 1), (0, 4), 0]]
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = [0,1,2,2,2,2,2]
BCTcube3d.base_cases[13].mc33[-1].interior = [[(0, 1), (0, 2), (2, 6), (2, 3)], [(2, 3), (0, 1), (2, 6), (6, 7)], [(2, 3), (0, 2), (2, 6), 2], [(0, 1), (2, 3), (1, 3), (3, 7)], [(0, 1), (2, 3), (3, 7), (6, 7)], [(0, 1), (0, 4), (4, 6), (1, 5)], [(1, 5), (0, 1), (4, 6), (6, 7)], [4, (4, 6), (0, 4), (1, 5)], [(4, 6), (1, 5), (4, 5), 4], [(1, 5), (4, 5), (5, 7), (4, 6)], [(1, 5), (5, 7), (6, 7), (4, 6)], [(0, 1), (1, 3), (3, 7), 1], [(1, 5), (5, 7), (6, 7), 7], [(0, 1), (1, 5), (3, 7), (6, 7)], [(1, 5), (3, 7), (6, 7), 7], [1, (0, 1), (1, 5), (3, 7)]]
BCTcube3d.base_cases[13].mc33[-1].interior_groups = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 3, 5 inside; 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 0, 1, 2, 3, 5 inside; 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[0].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[0].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 4, 5 inside; 3 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 0, 1, 2, 4, 5 inside; 3 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[0].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[0].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 3, 4, 5 inside; 2 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 0, 1, 3, 4, 5 inside; 2 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[0].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[0].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 2, 3, 4, 5 inside; 1 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 0, 2, 3, 4, 5 inside; 1 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_2_4*ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_2_4*ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[0].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_2_4*ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[0].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 1, 2, 3, 4, 5 inside; 0 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 1, 2, 3, 4, 5 inside; 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[0].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[0].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 2, 4 inside; 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 1, 2, 4 inside; 3, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = [[(2, 3), (1, 3), (Face3, 1)], [(1, 3), (3, 7), (Face3, 1)], [(2, 3), (2, 6), (Face3, 1)], [(3, 7), (6, 7), (Face3, 1)], [(5, 7), (1, 5), (Face5, 1)], [(4, 5), (1, 5), (Face5, 1)], [(5, 7), (Face5, 1), (6, 7)], [(Face3, 1), (Face5, 1), (6, 7)], [(4, 6), (4, 5), (Face5, 1)], [(Face5, 1), (Face3, 1), (2, 6)], [(2, 6), (Face5, 1), (4, 6)], [(0, 2), (0, 1), (0, 4)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[(4, 5), (4, 6), (Face5, 1), (5, 7)], [(Face5, 1), (4, 6), (5, 7), (6, 7)], [(Face5, 1), (4, 6), (2, 6), (6, 7)], [(2, 6), (Face3, 1), (Face5, 1), (6, 7)], [(5, 7), (4, 5), (1, 5), (Face5, 1)], [(1, 5), (4, 5), (5, 7), 5], [(2, 6), (4, 6), (6, 7), 6], [(Face3, 1), (6, 7), (3, 7), (2, 3)], [(6, 7), (2, 6), (2, 3), (Face3, 1)], [(1, 3), (2, 3), (3, 7), (Face3, 1)], [3, (1, 3), (2, 3), (3, 7)], [0, (0, 1), (0, 2), (0, 4)]]
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = [0,0,0,0,0,0,0,0,0,0,0,1]
BCTcube3d.base_cases[13].mc33[-1].interior = [[(Face3, 1), (Face5, 1), (5, 7), (6, 7)], [(6, 7), (5, 7), (Face3, 1), (3, 7)], [7, (3, 7), (5, 7), (6, 7)], [(Face3, 1), (5, 7), (3, 7), 1], [(Face3, 1), (3, 7), (1, 3), 1], [(Face3, 1), (Face5, 1), (5, 7), 1], [(Face5, 1), (5, 7), (1, 5), 1], [(2, 3), (1, 3), (Face3, 1), (0, 2)], [1, (1, 3), (Face3, 1), (0, 2)], [(Face5, 1), (0, 1), 1, (1, 5)], [(0, 2), (0, 1), 1, (Face5, 1)], [(0, 2), 1, (Face3, 1), (Face5, 1)], [(0, 1), (0, 2), (Face5, 1), (0, 4)], [(0, 1), (0, 4), (1, 5), (Face5, 1)], [(0, 4), (Face5, 1), (1, 5), (4, 5)], [(2, 3), (2, 6), (0, 2), (Face3, 1)], [(0, 2), (2, 6), (Face3, 1), (Face5, 1)], [(Face5, 1), (4, 5), (0, 4), (4, 6)], [(0, 2), (0, 4), (Face5, 1), (4, 6)], [(0, 2), (2, 6), (4, 6), (Face5, 1)], [(0, 2), (2, 3), (2, 6), 2], [(0, 4), (4, 5), (4, 6), 4]]
BCTcube3d.base_cases[13].mc33[-1].interior_groups = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 2, 5 inside; 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 1, 2, 5 inside; 3, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_1*MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_1*MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_1*MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 3, 4 inside; 2, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 1, 3, 4 inside; 2, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_1**3*MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_1**3*MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_1**3*MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 3, 5 inside; 2, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 1, 3, 5 inside; 2, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_1**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_1**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_1**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 3, 4 inside; 1, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 2, 3, 4 inside; 1, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 3, 5 inside; 1, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 2, 3, 5 inside; 1, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_4*ROTATE_FACES_0_1*ROTATE_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_4*ROTATE_FACES_0_1*ROTATE_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_4*ROTATE_FACES_0_1*ROTATE_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 4, 5 inside; 1, 3 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 2, 4, 5 inside; 1, 3 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_4**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 3, 4, 5 inside; 1, 2 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 0, 3, 4, 5 inside; 1, 2 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 3, 4 inside; 0, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 1, 2, 3, 4 inside; 0, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 3, 5 inside; 0, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 1, 2, 3, 5 inside; 0, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5*ROTATE_FACES_1_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5*ROTATE_FACES_1_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5*ROTATE_FACES_1_2_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 4, 5 inside; 0, 3 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 1, 2, 4, 5 inside; 0, 3 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 3, 4, 5 inside; 0, 2 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 1, 3, 4, 5 inside; 0, 2 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, ROTATE_FACES_0_3_5**2*ROTATE_FACES_0_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, ROTATE_FACES_0_3_5**2*ROTATE_FACES_0_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, ROTATE_FACES_0_3_5**2*ROTATE_FACES_0_2_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 0, 2, 4, INT inside; 1, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.1 0, 2, 4, INT inside; 1, 3, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = [[(3, 7), (5, 7), (6, 7)], [(0, 1), (0, 2), (0, 4)], [(2, 6), (4, 6), (1, 5)], [(1, 5), (4, 5), (4, 6)], [(2, 3), (1, 3), (1, 5)], [(2, 3), (2, 6), (1, 5)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 3), (2, 3), (3, 7), 3], [(1, 5), (4, 5), 5, (5, 7)], [(2, 6), (4, 6), 6, (6, 7)], [(4, 6), (4, 5), (1, 5), (5, 7)], [(2, 6), (1, 5), (4, 6), (5, 7)], [(5, 7), (2, 6), (4, 6), (6, 7)], [(1, 3), (1, 5), (2, 3), (3, 7)], [(3, 7), (2, 3), (2, 6), (1, 5)], [(1, 5), (3, 7), (2, 6), (5, 7)], [(2, 6), (3, 7), (5, 7), (6, 7)]]
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = [0,1,1,1,1,1,1,1,1,1,1]
BCTcube3d.base_cases[13].mc33[-1].interior = [[7, (3, 7), (5, 7), (6, 7)], [(1, 3), (1, 5), 1, (0, 1)], [2, (0, 2), (2, 3), (2, 6)], [(0, 1), (0, 2), (0, 4), (2, 3)], [(0, 1), (0, 4), (2, 3), (1, 3)], [(0, 1), (0, 4), (1, 3), (1, 5)], [(0, 4), (1, 3), (1, 5), (2, 3)], [(0, 2), (0, 4), (2, 3), (2, 6)], [(2, 3), (2, 6), (1, 5), (0, 4)], [(0, 4), (1, 5), (2, 6), (4, 6)], [(0, 4), (1, 5), (4, 6), (4, 5)], [(0, 4), (4, 5), (4, 6), 4]]
BCTcube3d.base_cases[13].mc33[-1].interior_groups = [2,3,3,3,3,3,3,3,3,3,3,3]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 0, 3, 5, INT inside; 1, 2, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.1 0, 3, 5, INT inside; 1, 2, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[18].faces, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].exterior, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[18].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].interior, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[18].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 1, 2, 5, INT inside; 0, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.1 1, 2, 5, INT inside; 0, 3, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[18].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[18].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].interior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[18].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 1, 3, 4, INT inside; 0, 2, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.1 1, 3, 4, INT inside; 0, 2, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[18].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[18].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[18].interior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[18].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 0, 2, 4 inside; 1, 3, 5, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.2 0, 2, 4 inside; 1, 3, 5, INT outside"
BCTcube3d.base_cases[13].mc33[-1].faces = [[(4, 5), (4, 6), ((0, 4), (3, 7))], [(2, 3), (2, 6), ((0, 2), (3, 7))], [(1, 3), (1, 5), ((0, 1), (3, 7))], [(0, 2), (0, 4), ((0, 2), (3, 7))], [(0, 1), (0, 4), ((0, 1), (3, 7))], [(0, 4), ((0, 1), (3, 7)), ((0, 4), (3, 7))], [(0, 4), ((0, 2), (3, 7)), ((0, 4), (3, 7))], [(6, 7), (5, 7), (3, 7)], [((0, 2), (3, 7)), ((0, 4), (3, 7)), (4, 6)], [((0, 2), (3, 7)), (2, 6), (4, 6)], [(0, 1), (0, 2), ((0, 1), (3, 7))], [((0, 1), (3, 7)), ((0, 2), (3, 7)), (0, 2)], [(2, 3), ((0, 2), (3, 7)), ((0, 1), (3, 7))], [(1, 3), (2, 3), ((0, 1), (3, 7))], [((0, 1), (3, 7)), ((0, 4), (3, 7)), (4, 5)], [(1, 5), (4, 5), ((0, 1), (3, 7))]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[(0, 2), ((0, 1), (3, 7)), ((0, 2), (3, 7)), (0, 4)], [((0, 1), (3, 7)), (0, 1), (0, 2), (0, 4)], [0, (0, 1), (0, 2), (0, 4)], [(0, 4), ((0, 4), (3, 7)), ((0, 1), (3, 7)), ((0, 2), (3, 7))], [(1, 3), (2, 3), ((0, 1), (3, 7)), (3, 7)], [(1, 3), (2, 3), (3, 7), 3], [((0, 1), (3, 7)), ((0, 2), (3, 7)), (2, 3), (3, 7)], [((0, 1), (3, 7)), ((0, 2), (3, 7)), ((0, 4), (3, 7)), (3, 7)], [(3, 7), (5, 7), (6, 7), ((0, 4), (3, 7))], [((0, 4), (3, 7)), (5, 7), (6, 7), (4, 6)], [(5, 7), (4, 6), (4, 5), ((0, 4), (3, 7))], [((0, 2), (3, 7)), ((0, 4), (3, 7)), (3, 7), (6, 7)], [((0, 2), (3, 7)), ((0, 4), (3, 7)), (6, 7), (4, 6)], [((0, 2), (3, 7)), (2, 6), (4, 6), (6, 7)], [(2, 3), (3, 7), (6, 7), ((0, 2), (3, 7))], [(2, 3), (2, 6), (6, 7), ((0, 2), (3, 7))], [(2, 6), (4, 6), (6, 7), 6], [((0, 1), (3, 7)), ((0, 4), (3, 7)), (3, 7), (5, 7)], [((0, 1), (3, 7)), ((0, 4), (3, 7)), (5, 7), (4, 5)], [(1, 3), (3, 7), (5, 7), ((0, 1), (3, 7))], [((0, 1), (3, 7)), (1, 3), (1, 5), (5, 7)], [(1, 5), (5, 7), (4, 5), ((0, 1), (3, 7))], [(1, 5), (4, 5), (5, 7), 5]]
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
BCTcube3d.base_cases[13].mc33[-1].interior = [[(3, 7), (5, 7), (6, 7), 7], [(2, 3), (0, 2), ((0, 1), (3, 7)), ((0, 2), (3, 7))], [(0, 2), (2, 3), ((0, 2), (3, 7)), (2, 6)], [(2, 3), (0, 2), (2, 6), 2], [(0, 2), (2, 6), (4, 6), ((0, 2), (3, 7))], [(0, 2), (0, 4), ((0, 2), (3, 7)), (4, 6)], [(0, 4), ((0, 2), (3, 7)), ((0, 4), (3, 7)), (4, 6)], [(4, 6), ((0, 4), (3, 7)), (0, 4), (4, 5)], [(0, 4), ((0, 1), (3, 7)), ((0, 4), (3, 7)), (4, 5)], [(0, 1), (0, 4), (4, 5), ((0, 1), (3, 7))], [(0, 1), (1, 5), (4, 5), ((0, 1), (3, 7))], [(0, 1), (1, 3), (1, 5), ((0, 1), (3, 7))], [(0, 4), (4, 5), (4, 6), 4], [(0, 1), (1, 3), (1, 5), 1], [(0, 1), (0, 2), (1, 3), ((0, 1), (3, 7))], [((0, 1), (3, 7)), (1, 3), (0, 2), (2, 3)]]
BCTcube3d.base_cases[13].mc33[-1].interior_groups = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 0, 3, 5 inside; 1, 2, 4, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.2 0, 3, 5 inside; 1, 2, 4, INT outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[22].faces, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].exterior, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[22].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].interior, ROTATE_FACES_1_2_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[22].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 1, 2, 5 inside; 0, 3, 4, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.2 1, 2, 5 inside; 0, 3, 4, INT outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[22].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[22].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].interior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[22].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 1, 3, 4 inside; 0, 2, 5, INT outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.5.2 1, 3, 4 inside; 0, 2, 5, INT outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[22].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[22].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[22].interior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[22].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 0, 2, 5 inside; 1, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.4 0, 2, 5 inside; 1, 3, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = [[(0, 4), (0, 1), Center, (1, 3)], [Center, (1, 3), (4, 5), (1, 5)], [(0, 2), (0, 4), (2, 3), Center], [(2, 3), Center, (2, 6), (4, 6)], [(5, 7), (3, 7), (4, 5), Center], [(4, 6), (6, 7), Center, (3, 7)]]
BCTcube3d.base_cases[13].mc33[-1].exterior = [[0, (0, 1), (0, 2), (0, 4)], [(0, 1), (0, 2), (0, 4), (1, 3), (2, 3), Center], [5, (1, 5), (4, 5), (5, 7)], [(1, 5), (4, 5), (5, 7), (1, 3), Center, (3, 7)], [6, (2, 6), (4, 6), (6, 7)], [(2, 6), (4, 6), (6, 7), (2, 3), Center, (3, 7)], [(1, 3), (2, 3), (3, 7), Center], [(1, 3), (2, 3), (3, 7), 3]]
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = [0, 0, 0, 0, 0, 0, 0, 0]
BCTcube3d.base_cases[13].mc33[-1].interior = [[1, (0, 1), (1, 3), (1, 5)], [(0, 1), (1, 3), (1, 5), (0, 4), Center, (4, 5)], [2, (0, 2), (2, 3), (2, 6)], [(0, 2), (2, 3), (2, 6), (0, 4), Center, (4, 6)], [7, (3, 7), (5, 7), (6, 7)], [(3, 7), (5, 7), (6, 7), Center, (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), Center], [(0, 4), (4, 5), (4, 6), 4]]
BCTcube3d.base_cases[13].mc33[-1].interior_groups = [1, 1, 1, 1, 1, 1, 1, 1]
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 0, 3, 4 inside; 1, 2, 5, outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.4 0, 3, 4 inside; 1, 2, 5, outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[26].faces, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].exterior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[26].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].interior, ROTATE_FACES_0_3_5**2)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[26].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 1, 2, 4 inside; 0, 3, 5, outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.4 1, 2, 4 inside; 0, 3, 5, outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[26].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[26].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].interior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[26].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 1, 3, 5 inside; 0, 2, 4, outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.4 1, 3, 5 inside; 0, 2, 4, outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[26].faces, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].exterior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[26].exterior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[26].interior, ROTATE_FACES_0_3_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[26].interior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2 inside; 1, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 0, 2 inside; 1, 3, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[17].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[17].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[17].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[17].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[17].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 3 inside; 1, 2, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 0, 3 inside; 1, 2, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[16].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[16].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[16].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[16].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[16].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 4 inside; 1, 2, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 0, 4 inside; 1, 2, 3, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[15].faces, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[15].interior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[15].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[15].exterior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[15].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 5 inside; 1, 2, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 0, 5 inside; 1, 2, 3, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[14].faces, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[14].interior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[14].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[14].exterior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[14].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2 inside; 0, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 1, 2 inside; 0, 3, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[13].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[13].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[13].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[13].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[13].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 3 inside; 0, 2, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 1, 3 inside; 0, 2, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[12].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[12].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[12].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[12].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[12].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 4 inside; 0, 2, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 1, 4 inside; 0, 2, 3, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[11].faces, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[11].interior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[11].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[11].exterior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[11].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 5 inside; 0, 2, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 1, 5 inside; 0, 2, 3, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[10].faces, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[10].interior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[10].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[10].exterior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[10].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 2, 4 inside; 0, 1, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 2, 4 inside; 0, 1, 3, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[9].faces, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[9].interior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[9].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[9].exterior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[9].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 2, 5 inside; 0, 1, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 2, 5 inside; 0, 1, 3, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[8].faces, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[8].interior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[8].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[8].exterior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[8].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 3, 4 inside; 0, 1, 2, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 3, 4 inside; 0, 1, 2, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[7].faces, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[7].interior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[7].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[7].exterior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[7].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 3, 5 inside; 0, 1, 2, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.3 inv 3, 5 inside; 0, 1, 2, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[6].faces, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].interior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[6].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[6].exterior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[6].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0 inside; 1, 2, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv 0 inside; 1, 2, 3, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[5].faces, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[5].interior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[5].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[5].exterior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[5].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 1 inside; 0, 2, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv 1 inside; 0, 2, 3, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[4].faces, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[4].interior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[4].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[4].exterior, MIRROR_FACES_2_3)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[4].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 2 inside; 0, 1, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv 2 inside; 0, 1, 3, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[3].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[3].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[3].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[3].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[3].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 3 inside; 0, 1, 2, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv 3 inside; 0, 1, 2, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[2].faces, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[2].interior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[2].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[2].exterior, MIRROR_FACES_4_5)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[2].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 4 inside; 0, 1, 2, 3, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv 4 inside; 0, 1, 2, 3, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[1].faces, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[1].interior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[1].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[1].exterior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[1].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 5 inside; 0, 1, 2, 3, 4 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.2 inv 5 inside; 0, 1, 2, 3, 4 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[0].faces, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].interior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].mc33[0].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[0].exterior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].mc33[0].exterior_groups
# 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.1 (face 0, 1, 2, 3, 4, 5 outside)
BCTcube3d.base_cases[13].mc33.append(Triangulation())
BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 13.1 inv 0, 1, 2, 3, 4, 5 outside"
BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].faces, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[13].interior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].exterior_groups = BCTcube3d.base_cases[13].interior_groups
BCTcube3d.base_cases[13].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[13].exterior, MIRROR_FACES_0_1)
BCTcube3d.base_cases[13].mc33[-1].interior_groups = BCTcube3d.base_cases[13].exterior_groups
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
                                                 (TEST_FACE_5, 35, 29),
                                                 (TEST_FACE_5,
                                                  (TEST_INTERIOR_3_4, 25, 21),
                                                  17))),
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5,
                                                  34,
                                                  (TEST_INTERIOR_2_4, 24, 20)),
                                                 (TEST_FACE_5, 28, 16)),
                                                (TEST_FACE_4,
                                                 15,
                                                 (TEST_FACE_5, 14, 0))))),
                                             (TEST_FACE_1,
                                              (TEST_FACE_2,
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 42, 33),
                                                 32),
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5,
                                                  31,
                                                  (TEST_INTERIOR_1_4, 23, 19)),
                                                 (TEST_FACE_5, 27, 13))),
                                               (TEST_FACE_3,
                                                (TEST_FACE_4,
                                                 (TEST_FACE_5, 30, 26),
                                                 (TEST_FACE_5,
                                                  (TEST_INTERIOR_0_4, 22, 18),
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
                                                 (TEST_FACE_5, 5, CASE_IS_REGULAR)))))))

# generate code
BCTcube3d.generate()

################################################################################
## 3D Prism                                                                   ##
################################################################################
BCTprism3d = LookupGenerator(3,"prism")
# 0,0,0,0,0,0 -> 000000
BCTprism3d.base_cases[0].faces = []
BCTprism3d.base_cases[0].interior = [[0, 1, 2, 3, 4, 5]]
BCTprism3d.base_cases[0].interior_groups = [0]
BCTprism3d.base_cases[0].exterior = []
BCTprism3d.base_cases[0].exterior_groups = []
# 1,0,0,0,0,0 -> 000001
BCTprism3d.base_cases[1].faces = [[(0, 1), (0, 2), (0, 3)]]
BCTprism3d.base_cases[1].interior = [[(0, 1), (0, 2), 1, 2, (0, 3)], [1, 2, (0, 3), 4, 5, 3]]
BCTprism3d.base_cases[1].interior_groups = [0, 0]
BCTprism3d.base_cases[1].exterior = [[(0, 1), (0, 2), (0, 3), 0]]
BCTprism3d.base_cases[1].exterior_groups = [1]
# 1,1,0,0,0,0 -> 000011
BCTprism3d.base_cases[2].faces = [[(0, 2), (1, 2), (0, 3), (1, 4)]]
BCTprism3d.base_cases[2].interior = [[(0, 2), (1, 2), (0, 3), (1, 4), 2], [(0, 3), (1, 4), 2, 3, 4, 5]]
BCTprism3d.base_cases[2].interior_groups = [0, 0]
BCTprism3d.base_cases[2].exterior = [[0, (0, 2), (0, 3), 1, (1, 2), (1, 4)]]
BCTprism3d.base_cases[2].exterior_groups = [1]
# 1,1,1,0,0,0 -> 000111
BCTprism3d.base_cases[3].faces = [[(0, 3), (1, 4), (2, 5)]]
BCTprism3d.base_cases[3].interior = [[(0, 3), (1, 4), (2, 5), 3, 4, 5]]
BCTprism3d.base_cases[3].interior_groups = [0]
BCTprism3d.base_cases[3].exterior = [[(0, 3), (1, 4), (2, 5), 0, 1, 2]]
BCTprism3d.base_cases[3].exterior_groups = [1]
# 1,0,0,1,0,0 -> 001001
BCTprism3d.base_cases[4].faces = [[(0, 1), (0, 2), (3, 4), (3, 5)]]
BCTprism3d.base_cases[4].interior = [[(0, 1), (0, 2), (3, 4), (3, 5), 1, 2, 4, 5]]
BCTprism3d.base_cases[4].interior_groups = [0]
BCTprism3d.base_cases[4].exterior = [[0, (0, 1), (0, 2), 3, (3, 4), (3, 5)]]
BCTprism3d.base_cases[4].exterior_groups = [1]
# 0,1,0,1,0,0 -> 001010 (face 0 outside)
BCTprism3d.base_cases[5].name = "MC33 Prism Case 5, face 0 outside"
BCTprism3d.base_cases[5].faces = [[(0, 1), (1, 2), (0, 3), (3, 5)], [(1, 2), (1, 4), (3, 5), (3, 4)]]
BCTprism3d.base_cases[5].interior = [[0, (0, 3), (0, 1), 2], [(1, 2), (1, 4), (3, 5), (3, 4), 4], [(3, 5), 4, 5, (1, 2)], [(0, 3), (3, 5), (0, 1), (1, 2), 2], [2, (1, 2), (3, 5), 5]]
BCTprism3d.base_cases[5].interior_groups = [0, 0, 0, 0, 0]
BCTprism3d.base_cases[5].exterior = [[3, (0, 3), (3, 4), (3, 5)], [1, (0, 1), (1, 2), (1, 4)], [(0, 3), (3, 4), (3, 5), (0, 1), (1, 4), (1, 2)]]
BCTprism3d.base_cases[5].exterior_groups = [1, 1, 1]
# 1,1,0,1,0,0 -> 001101
BCTprism3d.base_cases[6].name = "MC33 Prism Case 6"
BCTprism3d.base_cases[6].faces = [[(3, 5), (3, 4), (0, 2)], [(3, 4), (1, 4), (0, 2)], [(1, 4), (0, 2), (1, 2)]]
BCTprism3d.base_cases[6].interior = [[(0, 2), (1, 2), (1, 4), 2], [(0, 2), (1, 4), (3, 4), 2], [4, (1, 4), (3, 4), 2], [4, (3, 4), 2, 5], [5, (3, 4), 2, (0, 2)], [5, (3, 4), (3, 5), (0, 2)]]
BCTprism3d.base_cases[6].interior_groups = [0, 0, 0, 0, 0, 0]
BCTprism3d.base_cases[6].exterior = [[0, 1, (1, 2), (1, 4)], [(1, 2), (1, 4), (0, 2), 0], [(1, 4), (3, 4), (0, 2), 0], [0, (3, 4), 3, (0, 2)], [3, (3, 4), (3, 5), (0, 2)]]
BCTprism3d.base_cases[6].exterior_groups = [1, 1, 1, 1, 1]
# 0,1,1,1,0,0 -> 001110 (face 0, 1 outside)
BCTprism3d.base_cases[7].name = "MC33 Prism Case 7, face 0, 1 outside"
BCTprism3d.base_cases[7].faces = [[(0, 1), (0, 2), (0, 3)], [(1, 4), (3, 4), (2, 5), (3, 5)]]
BCTprism3d.base_cases[7].interior = [[(0, 1), (0, 2), (0, 3), 0], [(3, 4), (1, 4), 4, (3, 5), (2, 5), 5]]
BCTprism3d.base_cases[7].interior_groups = [0, 1]
BCTprism3d.base_cases[7].exterior = [[(0, 1), 1, (1, 4), (0, 2), 2, (2, 5)], [(0, 1), (1, 4), (3, 4), (0, 2), (2, 5), (3, 5)], [(0, 1), (0, 2), (3, 4), (3, 5), (0, 3)], [(0, 3), (3, 4), (3, 5), 3]]
BCTprism3d.base_cases[7].exterior_groups = [2, 2, 2, 2]
# mc33 cases follow
# 0,1,0,1,0,0 -> 001010 (face 0 inside)
BCTprism3d.base_cases[5].mc33.append(Triangulation())
BCTprism3d.base_cases[5].mc33[-1].name = "MC33 Prism Case 5, face 0 inside"
BCTprism3d.base_cases[5].mc33[-1].faces = [[(0, 3), (3, 4), (3, 5)], [(0, 1), (1, 2), (1, 4)]]
BCTprism3d.base_cases[5].mc33[-1].interior = [[0, (0, 3), (0, 1), 2], [(1, 2), (1, 4), (3, 5), (3, 4), 4], [(3, 5), 4, 5, (1, 2)], [(0, 3), (3, 5), (0, 1), (1, 2), 2], [2, (1, 2), (3, 5), 5], [(0, 3), (3, 4), (3, 5), (0, 1), (1, 4), (1, 2)]]
BCTprism3d.base_cases[5].mc33[-1].interior_groups = [0, 0, 0, 0, 0, 0]
BCTprism3d.base_cases[5].mc33[-1].exterior = [[(0, 3), (3, 4), (3, 5), 3], [(0, 1), (1, 2), (1, 4), 1]]
BCTprism3d.base_cases[5].mc33[-1].exterior_groups = [1, 2]
BCTprism3d.base_cases[5].tests = [TEST_FACE_0, CASE_IS_REGULAR , 0]
# 0,1,1,1,0,0 -> 001110 (face 1 outside, 0 inside)
BCTprism3d.base_cases[7].mc33.append(Triangulation())
BCTprism3d.base_cases[7].mc33[-1].name = "MC33 Prism Case 7, face 1 outside, 0 inside"
BCTprism3d.base_cases[7].mc33[-1].faces = [[(0, 3), (3, 4), (0, 2)], [(3, 4), (3, 5), (2, 5)], [(3, 4), (2, 5), (0, 2)], [(0, 2), (0, 1), (2, 5), (1, 4)]]
BCTprism3d.base_cases[7].mc33[-1].interior = [[(3, 4), 4, (3, 5), 5, (2, 5)], [(3, 4), (1, 4), 4, (2, 5)], [(2, 5), (1, 4), (0, 2), (0, 1), (3, 4)], [(0, 3), (0, 1), (0, 2), (3, 4)], [(0, 3), (0, 1), (0, 2), 0]]
BCTprism3d.base_cases[7].mc33[-1].interior_groups = [0, 0, 0, 0, 0]
BCTprism3d.base_cases[7].mc33[-1].exterior = [[(0, 3), (3, 4), (3, 5), 3], [(0, 3), (0, 2), (3, 5), (2, 5), (3, 4)], [(0, 2), 2, (2, 5), (0, 1), 1, (1, 4)]]
BCTprism3d.base_cases[7].mc33[-1].exterior_groups = [1, 1, 1]
# 0,1,1,1,0,0 -> 001110 (face 0 outside, 1 inside)
BCTprism3d.base_cases[7].mc33.append(Triangulation())
BCTprism3d.base_cases[7].mc33[-1].name = "MC33 Prism Case 7, face 0 outside, 1 inside"
BCTprism3d.base_cases[7].mc33[-1].faces = permute_geom_list(2, BCTprism3d.base_cases[7].mc33[0].faces, MIRROR_PRISM_0_1)
BCTprism3d.base_cases[7].mc33[-1].interior = permute_geom_list(3, BCTprism3d.base_cases[7].mc33[0].interior, MIRROR_PRISM_0_1)
BCTprism3d.base_cases[7].mc33[-1].interior_groups = BCTprism3d.base_cases[7].mc33[0].interior_groups
BCTprism3d.base_cases[7].mc33[-1].exterior = permute_geom_list(3, BCTprism3d.base_cases[7].mc33[0].exterior, MIRROR_PRISM_0_1)
BCTprism3d.base_cases[7].mc33[-1].exterior_groups = BCTprism3d.base_cases[7].mc33[0].exterior_groups
# 0,1,1,1,0,0 -> 001110 (face 0, 1 inside)
BCTprism3d.base_cases[7].mc33.append(Triangulation())
BCTprism3d.base_cases[7].mc33[-1].name = "MC33 Prism Case 7, face 0, 1 inside"
BCTprism3d.base_cases[7].mc33[-1].faces = [[(0, 3), (3, 4), (3, 5)], [(0, 1), (0, 2), (1, 4), (2, 5)]]
BCTprism3d.base_cases[7].mc33[-1].interior = [[(1, 4), 4, (3, 4), (2, 5), 5, (3, 5)], [(1, 4), (3, 4), (2, 5), (3, 5), (0, 3)], [(0, 1), (1, 4), (0, 2), (2, 5), (0, 3)], [(0, 1), (0, 2), (0, 3), 0]]
BCTprism3d.base_cases[7].mc33[-1].interior_groups = [0, 0, 0, 0]
BCTprism3d.base_cases[7].mc33[-1].exterior = [[(0, 3), (3, 4), (3, 5), 3], [(0, 1), 1, (1, 4), (0, 2), 2, (2, 5)]]
BCTprism3d.base_cases[7].mc33[-1].exterior_groups = [1, 2]
BCTprism3d.base_cases[7].tests = binaryheap((TEST_FACE_0,
                                             (TEST_FACE_1, CASE_IS_REGULAR, 1),
                                             (TEST_FACE_1, 0, 2)))
BCTprism3d.generate()

################################################################################
## 3D Pyramid                                                                 ##
################################################################################
BCTpyramid3d = LookupGenerator(3,"pyramid")
# 0,0,0,0,0 -> 00000
BCTpyramid3d.base_cases[0].faces = []
BCTpyramid3d.base_cases[0].interior = [[0, 1, 2, 3, 4]]
BCTpyramid3d.base_cases[0].interior_groups = [0]
BCTpyramid3d.base_cases[0].exterior = []
BCTpyramid3d.base_cases[0].exterior_groups = []
# 1,0,0,0,0 -> 00001
BCTpyramid3d.base_cases[1].faces = [[(0, 1), (0, 2), (0, 4)]]
BCTpyramid3d.base_cases[1].interior = [[(0, 1), (0, 2), (0, 4), 1, 2, 4], [1, 2, 4, 3]]
BCTpyramid3d.base_cases[1].interior_groups = [0, 0]
BCTpyramid3d.base_cases[1].exterior = [[(0, 1), (0, 2), (0, 4), 0]]
BCTpyramid3d.base_cases[1].exterior_groups = [1]
# 1,1,0,0,0 -> 00011
BCTpyramid3d.base_cases[2].faces = [[(0, 2), (1, 3), (0, 4), (1, 4)]]
BCTpyramid3d.base_cases[2].interior = [[(0, 2), (1, 3), (0, 4), (1, 4), 4], [(0, 2), (1, 3), 2, 3, 4]]
BCTpyramid3d.base_cases[2].interior_groups = [0, 0]
BCTpyramid3d.base_cases[2].exterior = [[0, (0, 2), (0, 4), 1, (1, 3), (1, 4)]]
BCTpyramid3d.base_cases[2].exterior_groups = [1]
# 0,1,1,0,0 -> 00110 # (face 0 outside)
BCTpyramid3d.base_cases[3].faces = [[1, (0, 1), (1, 4)], [1, (1, 3), (1, 4)], [2, (0, 2), (2, 4)], [2, (2, 3), (2, 4)], [(0, 2), (0, 1), (2, 4), (1, 4)], [(1, 3), (2, 3), (1, 4), (2, 4)]]
BCTpyramid3d.base_cases[3].interior = [[0, (0, 1), (0, 2), 4, (1, 4), (2, 4)], [3, (1, 3), (2, 3), 4, (1, 4), (2, 4)]]
BCTpyramid3d.base_cases[3].interior_groups = [0, 0]
BCTpyramid3d.base_cases[3].exterior = [[1, (0, 1), (1, 3), (1, 4)], [2, (0, 2), (2, 3), (2, 4)], [(0, 1), (1, 3), (1, 4), (0, 2), (2, 3), (2, 4)]]
BCTpyramid3d.base_cases[3].exterior_groups = [1, 1, 1]
# 1,1,1,0,0 -> 00111
BCTpyramid3d.base_cases[4].faces = [[(0, 4), (1, 4), (2, 4)], [(1, 4), (1, 3), (2, 4), (2, 3)]]
BCTpyramid3d.base_cases[4].interior = [[(0, 4), (1, 4), (2, 4), 4], [(1, 4), (2, 4), 4, (1, 3), (2, 3), 3]]
BCTpyramid3d.base_cases[4].interior_groups = [0, 0]
BCTpyramid3d.base_cases[4].exterior = [[0, 1, 2, (0, 4), (1, 4), (2, 4)], [1, (1, 3), (1, 4), 2, (2, 3), (2, 4)]]
BCTpyramid3d.base_cases[4].exterior_groups = [1, 1]
# 1,1,1,1,0 -> 01111
BCTpyramid3d.base_cases[5].faces = [[(0, 4), (1, 4), (2, 4), (3, 4)]]
BCTpyramid3d.base_cases[5].interior = [[(0, 4), (1, 4), (2, 4), (3, 4), 4]]
BCTpyramid3d.base_cases[5].interior_groups = [0]
BCTpyramid3d.base_cases[5].exterior = [[0, 1, 2, 3, (0, 4), (1, 4), (2, 4), (3, 4)]]
BCTpyramid3d.base_cases[5].exterior_groups = [1]
# mc33 case follows
# 0,1,1,0,0 -> 00110 # (face 0 inside)
BCTpyramid3d.base_cases[3].mc33.append(Triangulation())
BCTpyramid3d.base_cases[3].mc33[-1].faces = [[(0, 1), (1, 3), (1, 4)], [(0, 2), (2, 3), (2, 4)]]
BCTpyramid3d.base_cases[3].mc33[-1].interior = [[0, (0, 1), (0, 2), 4, (1, 4), (2, 4)], [3, (1, 3), (2, 3), 4, (1, 4), (2, 4)], [(0, 1), (1, 3), (1, 4), (0, 2), (2, 3), (2, 4)]]
BCTpyramid3d.base_cases[3].mc33[-1].interior_groups = [0, 0, 0]
BCTpyramid3d.base_cases[3].mc33[-1].exterior = [[1, (0, 1), (1, 3), (1, 4)], [2, (0, 2), (2, 3), (2, 4)]]
BCTpyramid3d.base_cases[3].mc33[-1].exterior_groups = [1, 2]
BCTpyramid3d.base_cases[3].tests = [TEST_FACE_0, CASE_IS_REGULAR , 0]

BCTpyramid3d.generate()

################################################################################
## 3D Simplex                                                                 ##
################################################################################
BCTsimplex3d = LookupGenerator(3,"simplex")
# base cases simplex 3D:
# 0,0,0,0 -> 0000
BCTsimplex3d.base_cases[0].faces = []
BCTsimplex3d.base_cases[0].interior = [[0, 1, 2, 3]]
BCTsimplex3d.base_cases[0].interior_groups = [0]
BCTsimplex3d.base_cases[0].exterior = []
BCTsimplex3d.base_cases[0].exterior_groups = []
# 1,0,0,0 -> 0001
BCTsimplex3d.base_cases[1].faces = [[(0, 2), (0, 1), (0, 3)]]
BCTsimplex3d.base_cases[1].interior = [[(0, 2), (0, 1), (0, 3), 2, 1, 3]]
BCTsimplex3d.base_cases[1].interior_groups = [0]
BCTsimplex3d.base_cases[1].exterior = [[0, (0, 2), (0, 1), (0, 3)]]
BCTsimplex3d.base_cases[1].exterior_groups = [1]
# 1,1,0,0 -> 0011
BCTsimplex3d.base_cases[2].faces = [[(0, 2), (1, 2), (0, 3), (1, 3)]]
BCTsimplex3d.base_cases[2].interior = [[(0, 2), (1, 2), 2, (0, 3), (1, 3), 3]]
BCTsimplex3d.base_cases[2].interior_groups = [0]
BCTsimplex3d.base_cases[2].exterior = [[0, (0, 2), (0, 3), 1, (1, 2), (1, 3)]]
BCTsimplex3d.base_cases[2].exterior_groups = [1]
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
BCTcube2d.base_cases[0].interior_groups = [0]
BCTcube2d.base_cases[0].exterior = []
BCTcube2d.base_cases[0].exterior_groups = []
# 1,0,0,0 -> 0001
BCTcube2d.base_cases[1].faces = [[(0, 1), (0, 2)]]
BCTcube2d.base_cases[1].interior = [[(0, 1), (0, 2), 1, 2], [1, 2, 3]]
BCTcube2d.base_cases[1].interior_groups = [0, 0]
BCTcube2d.base_cases[1].exterior = [[0, (0, 1), (0, 2)]]
BCTcube2d.base_cases[1].exterior_groups = [1]
# 1,1,0,0 -> 0011
BCTcube2d.base_cases[2].faces = [[(1, 3), (0, 2)]]
BCTcube2d.base_cases[2].interior = [[(0, 2), (1, 3), 2, 3]]
BCTcube2d.base_cases[2].interior_groups = [0]
BCTcube2d.base_cases[2].exterior = [[0, 1, (0, 2), (1, 3)]]
BCTcube2d.base_cases[2].exterior_groups = [1]
# 0,1,1,0 -> 0110
BCTcube2d.base_cases[3].faces = [[(0, 1), (0, 2)], [(2, 3), (1, 3)]]
BCTcube2d.base_cases[3].interior = [[0, (0, 1), (0, 2)], [(2, 3), (1, 3), 3]]
BCTcube2d.base_cases[3].interior_groups = [0, 1]
BCTcube2d.base_cases[3].exterior = [[(0, 1), (0, 2), 1, 2], [(2, 3), (1, 3), 2, 1]]
BCTcube2d.base_cases[3].exterior_groups = [2, 2]

BCTcube2d.base_cases[3].mc33.append(Triangulation())
BCTcube2d.base_cases[3].mc33[-1].faces = [[(1, 3), (0, 1)], [(0, 2), (2, 3)]]
BCTcube2d.base_cases[3].mc33[-1].interior = [[(1, 3), (0, 1), 3, 0], [(0, 2), (2, 3), 0, 3]]
BCTcube2d.base_cases[3].mc33[-1].interior_groups = [0, 0]
BCTcube2d.base_cases[3].mc33[-1].exterior = [[(1, 3), (0, 1), 1], [(0, 2), (2, 3), 2]]
BCTcube2d.base_cases[3].mc33[-1].exterior_groups = [1, 2]

BCTcube2d.base_cases[3].tests = [TEST_FACE_0, CASE_IS_REGULAR , 0]

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
BCTsimplex2d.base_cases[0].interior_groups = [0]
BCTsimplex2d.base_cases[0].exterior = []
BCTsimplex2d.base_cases[0].exterior_groups = []
# 1,0,0 -> 001
BCTsimplex2d.base_cases[1].faces = [[(0, 1), (0, 2)]]
BCTsimplex2d.base_cases[1].interior = [[(0, 1), (0, 2), 1, 2]]
BCTsimplex2d.base_cases[1].interior_groups = [0]
BCTsimplex2d.base_cases[1].exterior = [[0, (0, 1), (0, 2)]]
BCTsimplex2d.base_cases[1].exterior_groups = [1]

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
BCTany1d.base_cases[0].interior_groups = [0]
BCTany1d.base_cases[0].exterior = []
BCTany1d.base_cases[0].exterior_groups = []
# 1,0 -> 01
BCTany1d.base_cases[1].faces = [[(0,1)]]
BCTany1d.base_cases[1].interior = [[(0, 1), 1]]
BCTany1d.base_cases[1].interior_groups = [0]
BCTany1d.base_cases[1].exterior = [[0, (0, 1)]]
BCTany1d.base_cases[1].exterior_groups = [1]

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
BCTany0d.base_cases[0].exterior_groups = [0]
BCTany0d.base_cases[0].interior = []
BCTany0d.base_cases[0].interior_groups = []
# generate code
BCTany0d.generate()

LookupGenerators = {(3, "cube") : BCTcube3d,
                    (3, "prism") : BCTprism3d,
                    (3, "pyramid") : BCTpyramid3d,
                    (3, "simplex") : BCTsimplex3d, 
                    (2, "cube") : BCTcube2d,
                    (2, "simplex") : BCTsimplex2d,
                    (1, "any") : BCTany1d,
                    (0, "any") : BCTany0d}
