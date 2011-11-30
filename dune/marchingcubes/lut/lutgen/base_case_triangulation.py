from generator import *
from permutation import *

# this file contains the triangulations for the marching-cubes base cases generated
# by the LookupGenerators init-method.
# geometries: (3,"cube"), (3,"simplex"), (2,"cube"), (2,"simplex"), (1,"any"), (0,"any")

# Constants for permutate mc 33 cases
MIRROR_FACES_0_TO_1 = Permutation(-1, (3, 1, 7, 5, 2, 0, 6, 4))
MIRROR_FACES_0_TO_2 = Permutation(-1, (0, 2, 1, 3, 4, 6, 5, 7))
MIRROR_FACES_0_TO_4 = Permutation(-1, (0, 4, 2, 6, 1, 5, 3, 7))
ROTATE_FACES_0_2_4 = Permutation(1, (0, 2, 4, 6, 1, 3, 5, 7))
ROTATE_FACES_0_3_5 = Permutation(1, (5, 1, 4, 0, 7, 3, 6, 2))

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
# # 1,1,1,1,1,0,0,0 -> 00011111 # Inverse of Basic Case 5
# BCTcube3d.base_cases[12].name = "MC33 Case 5 (inverse)"
# BCTcube3d.base_cases[12].faces = [[(4, 5), (4, 6), (1, 5), (2, 6)], [(1, 5), (2, 6), (3, 7)]]
# BCTcube3d.base_cases[12].cells = [[(4, 5), 5, (1, 5), (4, 6), 6, (2, 6)], [6, 5, 7, (2, 6), (1, 5), (3, 7)]]
# # 0,0,1,1,1,1,0,0 -> 00111100 # Basic Case 10 and its inverse
# BCTcube3d.base_cases[13].name = "MC33 Case 10.1"
# BCTcube3d.base_cases[13].faces = [[(0, 2), (1, 3), (2, 6), (3, 7)], [(0, 4), (1, 5), (4, 6), (5, 7)]]
# BCTcube3d.base_cases[13].cells = [[(0, 2), 0, (2, 6), 6, (1, 3), 1, (3, 7), 7], [6, 0, (4, 6), (0, 4), 7, 1, (5, 7), (1, 5)]]
# # 1,0,1,1,1,1,0,0 -> 00111101 # Inverse of Basic Case 6
# BCTcube3d.base_cases[14].name = "MC33 Case 6.1 (inverse)"
# BCTcube3d.base_cases[14].faces = [[(3, 7), (5, 7), (2, 6), (4, 6)], [(0, 1), (1, 3), (1, 5)]]
# BCTcube3d.base_cases[14].cells = [[6, (2, 6), (4, 6), 7, (3, 7), (5, 7)], [(0, 1), (1, 5), (1, 3), 1]]
# # 1,1,1,1,1,1,0,0 -> 00111111 # Inverse of Basic Case 2
# BCTcube3d.base_cases[15].name = "MC33 Case 2 (inverse)"
# BCTcube3d.base_cases[15].faces = [[(3, 7), (2, 6), (5, 7), (4, 6)]]
# BCTcube3d.base_cases[15].cells = [[6, (4, 6), (2, 6), 7, (5, 7), (3, 7)]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # Basic Case 13 and its inverse
# BCTcube3d.base_cases[16].name = "MC33 Case 13.1"
# BCTcube3d.base_cases[16].faces = [[(0, 1), (0, 2), (0, 4)], [(2, 3), (1, 3), (3, 7)], [(4, 5), (5, 7), (1, 5)], [(2, 6), (4, 6), (6, 7)]]
# BCTcube3d.base_cases[16].cells = [[(0, 4), (0, 2), (0, 1), 4, (4, 6), (4, 5)], [(4, 5), (5, 7), (1, 5), (0, 1), (1, 3), 1], [(1, 3), (2, 3), (3, 7), (5, 7), (6, 7), 7], [(2, 6), (4, 6), (6, 7), 2, (0, 2), (2, 3)], [(0, 1), (1, 3), (0, 2), (2, 3), (4, 5), (5, 7), (4, 6), (6, 7)]]
# # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of Basic Case 7
# BCTcube3d.base_cases[17].name = "MC33 Case 7.1 (inverse)"
# BCTcube3d.base_cases[17].faces = [[(2, 3), (2, 6), (0, 2)], [(6, 7), (3, 7), (5, 7)], [(0, 4), (4, 6), (4, 5)]]
# BCTcube3d.base_cases[17].cells = [[(2, 3), 2, (0, 2), (2, 6)], [(4, 5), (4, 6), (0, 4), 4], [(3, 7), (6, 7), (5, 7), 7]]
# # 1,1,1,1,0,1,1,0 -> 01101111 # Inverse of Basic Case 3
# BCTcube3d.base_cases[18].name = "MC33 Case 3.1 (inverse)"
# BCTcube3d.base_cases[18].faces = [[(0, 4), (4, 6), (4, 5)], [(6, 7), (5, 7), (3, 7)]]
# BCTcube3d.base_cases[18].cells = [[4, (4, 5), (0, 4), (4, 6)], [(6, 7), 7, (5, 7), (3, 7)]]
# # 0,1,1,1,1,1,1,0 -> 01111110 # Inverse of Basic Case 4
# BCTcube3d.base_cases[19].name = "MC33 Case 4.1 (inverse)"
# BCTcube3d.base_cases[19].faces = [[(0, 1), (0, 2), (0, 4)], [(3, 7), (5, 7), (6, 7)]]
# BCTcube3d.base_cases[19].cells = [[0, (0, 1), (0, 2), (0, 4)], [(6, 7), (5, 7), (3, 7), 7]]
# # 1,1,1,1,1,1,1,0 -> 01111111 # Inverse of Basic Case 1 
# BCTcube3d.base_cases[20].name = "MC33 Case 1 (inverse)"
# BCTcube3d.base_cases[20].faces = [[(6, 7), (3, 7), (5, 7)]]
# BCTcube3d.base_cases[20].cells = [[(6, 7), (5, 7), (3, 7), 7]]
# # 1,1,1,1,1,1,1,1 -> 11111111 # Inverse of Basic Case 0 
# BCTcube3d.base_cases[21].name = "MC33 Case 0"
# BCTcube3d.base_cases[21].faces = []
# BCTcube3d.base_cases[21].cells = []

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
                                    (TEST_INTERIOR_3, 0, CASE_IS_REGULAR),
                                    1
                                    ))
# 0,1,1,0,1,0,0,dun0 -> 00010110 # MC33 Case 7.2 (face 0 and face 2 connection)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 4), (4, 5), (4, 6)], [(0, 1), (1, 5), (0, 2), (2, 6)], [(1, 3), (1, 5), (2, 3), (2, 6)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[(0, 4), (4, 5), (4, 6), 4], [(0, 1), 1, (1, 3), (1, 5)], [(0, 2), 2, (2, 3), (2, 6)], [(0, 2), (2, 6), (2, 3), (0, 1), (1, 5), (1, 3)]]
BCTcube3d.base_cases[6].mc33[-1].interior = [[(0, 1), (1, 5), (0, 2), (2, 6), (4, 5), 5, (4, 6), 6], [0, (0, 1), (0, 2), (0, 4), (4, 5), (4, 6)], [(1, 5), (1, 3), (2, 6), (2, 3), 3], [(1, 5), 3, (2, 6), 5, 7, 6]]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2  (face 2 and face 4 connection)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2 face 2 and 4 connection"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[0].faces, MIRROR_FACES_0_TO_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[0].exterior, MIRROR_FACES_0_TO_4)
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[0].interior, MIRROR_FACES_0_TO_4)
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.2  (face 0 and face 4 connection)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.2 face 0 and 4 connection"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[1].faces, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[1].exterior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[1].interior, MIRROR_FACES_0_TO_2)
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 0 connection)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3"
BCTcube3d.base_cases[6].mc33[-1].faces = [[(0, 1), (0, 2), (0, 7), (2, 6)], [(1, 3), (2, 3), (0, 7), (2, 6)], [(0, 1), (0, 7), (0, 4), (4, 6)], [(1, 5), (0, 7), (4, 5), (4, 6)], [(1, 5), (0, 7), (1, 3)]]
BCTcube3d.base_cases[6].mc33[-1].exterior = [[(1, 3), 1, (0, 7), (1, 5)], [1, (1, 3), (0, 7), (0, 1)], [1, (1, 5), (0, 7), (0, 1)], [(0, 1), (1, 5), (0, 7), (0, 4), (4, 5), (4, 6)], [4, (0, 4), (4, 5), (4, 6)], [(0, 1), (1, 3), (0, 7), (0, 2), (2, 3), (2, 6)], [(0, 2), (2, 3), (2, 6), 2]]
BCTcube3d.base_cases[6].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(0, 2), (0, 1), (0, 4), (2, 6), (0, 7), (4, 6)], [(1, 5), 5, (4, 5), (5, 7)], [(1, 5), (5, 7), (4, 5), (0, 7), (6, 7), (4, 6)], [(0, 7), (2, 6), (4, 6), (6, 7)], [(2, 6), (4, 6), 6, (6, 7)], [(1, 3), (2, 3), (0, 7), (2, 6), 3], [(1, 5), (0, 7), (1, 3), (3, 7)], [(1, 3), 3, (0, 7), (3, 7)], [3, (2, 6), (3, 7), (6, 7), (0, 7)], [(1, 5), (0, 7), (5, 7), (6, 7), (3, 7)], [(5, 7), (6, 7), (3, 7), 7]]
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 2 connection)
BCTcube3d.base_cases[6].mc33.append(Triangulation())
BCTcube3d.base_cases[6].mc33[-1].name = "MC33 Case 7.3, face 2 connection"
BCTcube3d.base_cases[6].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[6].mc33[3].faces, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[3].exterior, ROTATE_FACES_0_2_4)
BCTcube3d.base_cases[6].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[6].mc33[3].interior, ROTATE_FACES_0_2_4)
# 0,1,1,0,1,0,0,0 -> 00010110 # MC33 Case 7.3 (face 4 connection)
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
                                          (TEST_FACE_4, CASE_IS_REGULAR, 0),
                                          (TEST_FACE_4, 2, 3)),
                                         (TEST_FACE_2,
                                          (TEST_FACE_4, 1, 4),
                                          (TEST_FACE_4,
                                           5,
                                           (TEST_INTERIOR_0, 7, 6)))
                                         ))
# # 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.1.2 and its inverse
# BCTcube3d.base_cases[13].mc33.append(Triangulation())
# BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 10.1.2"
# BCTcube3d.base_cases[13].mc33[-1].faces = [[(0, 2), (0, 4), (1, 3), (1, 5)], [(2, 6), (4, 6), (3, 7), (5, 7)], [(0, 2), (0, 4), (2, 6), (4, 6)], [(1, 3), (1, 5), (3, 7), (5, 7)]]
# BCTcube3d.base_cases[13].mc33[-1].cells = [[0, (0, 2), (0, 4), 1, (1, 3), (1, 5)], [6, (2, 6), (4, 6), 7, (3, 7), (5, 7)]]
# # 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.2 and its inverse (face 0 connection) 
# BCTcube3d.base_cases[13].mc33.append(Triangulation())
# BCTcube3d.base_cases[13].mc33[-1].name = "MC33 Case 10.2"
# BCTcube3d.base_cases[13].mc33[-1].faces = [[(1, 3), (1, 5), (0, 7)], [(1, 5), (0, 7), (0, 4)], [(0, 7), (0, 4), (4, 6)], [(0, 7), (4, 6), (5, 7)], [(0, 7), (5, 7), (3, 7)], [(0, 7), (3, 7), (2, 6)], [(0, 7), (2, 6), (0, 2)], [(0, 7), (0, 2), (1, 3)]]
# BCTcube3d.base_cases[13].mc33[-1].cells = [[0, (0, 2), (0, 4), 1, (1, 3), (1, 5)], [(0, 2), (1, 3), (1, 5), (0, 4), (0, 7)], [(0, 2), (2, 6), (4, 6), (0, 4), (0, 7)], [(2, 6), (3, 7), (5, 7), (4, 6), (0, 7)], [6, (2, 6), (4, 6), 7, (3, 7), (5, 7)]]
# # 0,0,1,1,1,1,0,0 -> 00111100 # MC33 Case 10.2 and its inverse (face 1 connection) 
# #BCTcube3d.base_cases[13].mc33.append(Triangulation())
# #BCTcube3d.base_cases[13].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[13].mc33[1].faces, Permutation(1, (2, 3, 0, 1, 6, 7, 4, 5)))
# #BCTcube3d.base_cases[13].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[13].mc33[1].cells, Permutation(1, (2, 3, 0, 1, 6, 7, 4, 5)))
# BCTcube3d.base_cases[13].tests = binaryheap((TEST_FACE_0,
#                                     (TEST_FACE_1, CASE_IS_REGULAR, 2),
#                                     (TEST_FACE_1,
#                                      1,
#                                      (TEST_INTERIOR_0, 0, CASE_IS_REGULAR))
#                                     ))
# 0,1,1,1,1,0,0,0 -> 00011110 # Inverse of MC33 Case 12.1.2 (12.1.1 with center connection, no face missing)
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.1.2"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(1, 5), (2, 6), (4, 5), (4, 6)], [(1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(1, 5), (2, 6), (4, 5), (4, 6), (0, 4)], [(0, 1), (0, 2), (1, 5), (2, 6), (0, 4)], [(0, 1), 1, (1, 5), (0, 2), 2 , (2, 6)], [1, 2, 3, (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 5), 5, (4, 5), (2, 6), 6, (4, 6)], [(1, 5), (2, 6), (3, 7), 5, 6, 7]]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.1.2 and its inverse
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.1.2"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 1), (0, 2), (0, 4)], [(0, 1), (0, 4), (4, 5)], [(0, 1), (4, 5), (1, 5)], [(0, 2), (0, 4), (4, 6)], [(0, 2), (4, 6), (2, 6)], [(1, 5), (4, 5), (3, 7)], [(4, 5), (4, 6), (3, 7)], [(2, 6), (4, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(0, 1), (0, 2), (4, 5), (4, 6), (0, 4)], [(0, 1), (1, 5), (4, 5), (0, 2), (2, 6), (4, 6)], [(1, 5), (4, 5), (2, 6), (4, 6), (3, 7)], [(0, 1), 1, (1, 5), (0, 2), 2, (2, 6)], [1, 2, 3, (1, 5), (2, 6), (3, 7)]]
BCTcube3d.base_cases[11].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(1, 5), (4, 5), 5, (3, 7)], [(4, 5), 5, (3, 7), 7], [(4, 5), (4, 6), (3, 7), 7], [(4, 6), (2, 6), 6, (3, 7)], [(4, 6), 6, (3, 7), 7]]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.2 and its inverse (face 0 connection) 
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].name = "MC33 Case 12.2"
BCTcube3d.base_cases[11].mc33[-1].faces = [[(0, 4), (4, 6), (0, 7)], [(4, 6), (4, 5), (0, 7)], [(0, 4), (0, 1), (0, 7)], [(4, 5), (1, 5), (0, 7)], [(1, 5), (3, 7), (0, 7)], [(3, 7), (2, 6), (0, 7)], [(0, 2), (2, 6), (0, 7)], [(0, 1), (0, 2), (0, 7)]]
BCTcube3d.base_cases[11].mc33[-1].exterior = [[4, (0, 4), (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), (0, 7)], [(0, 1), (0, 4), (1, 5), (4, 5), (0, 7)], [(0, 1), (0, 7), (1, 5), 1], [1, (1, 5), 3, (3, 7), (0, 7)], [2, (2, 6), 3, (3, 7), (0, 7)], [(0, 1), 1, 2, 3, (0, 7)], [(0, 1), (0, 2), 2, (0, 7)], [(0, 2), 2, (2, 6), (0, 7)]]
BCTcube3d.base_cases[11].mc33[-1].interior = [[0, (0, 1), (0, 2), (0, 4)], [(0, 1), (0, 2), (0, 4), (0, 7)], [(0, 2), (2, 6), (0, 4), (4, 6), (0, 7)], [(2, 6), (0, 7), (4, 6), 6], [(2, 6), 6, (3, 7), 7, (0, 7)], [(3, 7), 7, (1, 5), 5, (0, 7)], [(4, 6), 6, 5, 7, (0, 7)], [(4, 6), (4, 5), (0, 7), 5], [(4, 5), (0, 7), 5, (1, 5)]]
# 0,1,1,1,1,0,0,0 -> 00011110 # MC33 Case 12.2 and its inverse (face 2 connection) 
BCTcube3d.base_cases[11].mc33.append(Triangulation())
BCTcube3d.base_cases[11].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[11].mc33[2].faces, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].mc33[-1].exterior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[2].exterior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].mc33[-1].interior = permute_geom_list(3, BCTcube3d.base_cases[11].mc33[2].interior, MIRROR_FACES_0_TO_2)
BCTcube3d.base_cases[11].tests = binaryheap((TEST_FACE_0,
                                    (TEST_FACE_2, CASE_IS_REGULAR, 2),
                                    (TEST_FACE_2,
                                     3,
                                     (TEST_INTERIOR_0, 0, 1))
                                    ))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 1, 2, 3, 4, 5 connection; 0 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.2"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(5, 1), (5, 7), (5, 4)], [(7, 3), (1, 3), (3, 2)], [(4, 6), (4, 0), (7, 6), (1, 0)], [(7, 6), (1, 0), (6, 2), (0, 2)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[(5, 4), (5, 7), (5, 1), 4, (4, 6), (4, 0)], [7, (5, 7), (4, 6), 1, (5, 1), (4, 0)], [7, (7, 6), (4, 6), 1, (1, 0), (4, 0)], [1, (1, 0), (0, 2), 7, (7, 6), (6, 2)], [1, (1, 3), (0, 2), 7, (7, 3), (6, 2)], [(3, 2), (1, 3), (7, 3), 2, (0, 2), (6, 2)]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 2, 3, 4, 5 connection; 1 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[0].faces, ROTATE_FACES_0_2_4 * ROTATE_FACES_0_3_5)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[0].cells, ROTATE_FACES_0_2_4 * ROTATE_FACES_0_3_5)
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 3, 4, 5 connection; 2 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[0].faces, MIRROR_FACES_0_TO_2)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[0].cells, MIRROR_FACES_0_TO_2)
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 4, 5 connection; 3 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[0].faces, ROTATE_FACES_0_3_5)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[0].cells, ROTATE_FACES_0_3_5)
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 3, 5 connection; 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[0].faces, MIRROR_FACES_0_TO_4)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[0].cells, MIRROR_FACES_0_TO_4)
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.2 (face 0, 1, 2, 3, 4 connection; 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[0].faces, ROTATE_FACES_0_3_5 * ROTATE_FACES_0_3_5)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[0].cells, ROTATE_FACES_0_3_5 * ROTATE_FACES_0_3_5)
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 3, 4 connection; 2, 5 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.3"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(2, 3), (1, 3), (3, 7)], [(0, 4), (0, 1), (4, 6), (0, 7)], [(4, 6), (0, 7), (4, 5), (1, 5)], [(5, 7), (1, 5), (0, 7)], [(5, 7), (0, 7), (6, 7), (2, 6)], [(2, 6), (0, 7), (0, 2), (0, 1)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[4, (4, 6), (4, 5), (0, 1), (0, 7), (1, 5)], [(4, 6), (0, 1), (0, 4), (0, 7)], [(4, 6), (0, 1), (0, 4), 4], [(5, 7), 7, (0, 7), (6, 7)], [(2, 3), 7, (0, 7), (6, 7)], [(2, 3), (2, 6), (0, 7), (6, 7)], [(2, 3), (2, 6), (0, 2), 2], [1, (1, 3), (0, 7), (0, 1)], [(2, 3), (2, 6), (0, 2), (1, 3), (0, 7), (0, 1)], [(0, 7), (5, 7), 7, (2, 3), (1, 3), (3, 7)], [(1, 5), (0, 1), 1, (5, 7), (0, 7), (1, 3)]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 3, 4 connection; 0, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(-1, (0, 2, 1, 6, 4, 5, 3, 7)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(-1, (0, 2, 1, 6, 4, 5, 3, 7)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 3, 4 connection; 1, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(1, (3, 2, 1, 0, 7, 6, 5, 4)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(1, (3, 2, 1, 0, 7, 6, 5, 4)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 2, 4 connection; 3, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(-1, (2, 3, 0, 1, 6, 7, 4, 5)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(-1, (2, 3, 0, 1, 6, 7, 4, 5)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 3, 5 connection; 0, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(1, (4, 6, 5, 7, 0, 2, 1, 3)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(1, (4, 6, 5, 7, 0, 2, 1, 3)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 3, 5 connection; 1, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(1, (7, 5, 6, 4, 3, 1, 2, 0)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(1, (7, 5, 6, 4, 3, 1, 2, 0)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 3, 5 connection; 2, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(-1, (4, 5, 6, 7, 0, 1, 2, 3)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(-1, (4, 5, 6, 7, 0, 1, 2, 3)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 1, 2, 5 connection; 3, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(1, (6, 7, 4, 5, 2, 3, 0, 1)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(1, (6, 7, 4, 5, 2, 3, 0, 1)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 2, 4, 5 connection; 0, 3 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(1, (7, 3, 5, 1, 6, 2, 4, 0)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(1, (7, 3, 5, 1, 6, 2, 4, 0)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 2, 4, 5 connection; 1, 3 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(1, (2, 6, 0, 4, 3, 7, 1, 5)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(1, (2, 6, 0, 4, 3, 7, 1, 5)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 0, 3, 4, 5 connection; 1, 2 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(-1, (0, 4, 2, 6, 1, 5, 3, 7)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(-1, (0, 4, 2, 6, 1, 5, 3, 7)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.3 (face 1, 3, 4, 5 connection; 0, 2 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[6].faces, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[6].cells, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 0, 2, 5 connection; 1, 3, 4 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.4"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(6, 4), (2, 5), (2, 6), (2, 3)], [(2, 3), (2, 5), (2, 0), (0, 4)], [(6, 4), (2, 5), (6, 7), (3, 7)], [(4, 5), (2, 5), (7, 5), (3, 7)], [(3, 1), (2, 5), (1, 5), (4, 5)], [(3, 1), (2, 5), (0, 1), (0, 4)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[(7, 5), (6, 4), (2, 5), 7, (6, 7), (3, 7)], [(4, 5), 4, (0, 4), (7, 5), (6, 4), (2, 5)], [4, (2, 5), (0, 4), (6, 4)], [(2, 6), (2, 0), (2, 3), (6, 4), (0, 4), (2, 5)], [(2, 3), 2, (2, 0), (2, 6)], [(4, 5), (0, 4), (0, 1), (1, 5), (2, 5)], [(1, 5), (2, 5), (3, 1), (0, 1)], [(1, 5), 1, (3, 1), (0, 1)]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 1, 3, 5 connection; 0, 2, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[18].faces, Permutation(-1, (3, 1, 2, 0, 7, 5, 6, 4)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[18].faces, Permutation(-1, (3, 1, 2, 0, 7, 5, 6, 4)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 0, 3, 4 connection; 1, 2, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[18].faces, Permutation(1, (6, 7, 4, 5, 2, 3, 0, 1)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[18].faces, Permutation(1, (6, 7, 4, 5, 2, 3, 0, 1)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.4 (face 1, 2, 4 connection; 0, 3, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[18].faces, Permutation(1, (5, 4, 7, 6, 1, 0, 3, 2)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[18].faces, Permutation(1, (5, 4, 7, 6, 1, 0, 3, 2)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 0, 2, 4 connection; 1, 3, 5 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.5.1"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(2, 0), (1, 0), (4, 0)], [(6, 2), (3, 2), (6, 4), (3, 1)], [(6, 4), (3, 1), (5, 4), (5, 1)], [(7, 5), (7, 3), (7, 6)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[1, 4, (2, 0), (3, 2), (6, 2), 2], [1, (1, 0), (4, 0), 4, (2, 0)], [4, (6, 4), (6, 2), 1, (3, 1), (3, 2)], [(5, 4), (6, 4), 4, (5, 1), (3, 1), 1], [(7, 5), 7, (7, 3), (7, 6)]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 0, 3, 5 connection; 1, 2, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[22].faces, Permutation(-1, (6, 7, 2, 3, 4, 5, 0, 1)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[22].cells, Permutation(-1, (6, 7, 2, 3, 4, 5, 0, 1)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 1, 2, 5 connection; 0, 3, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[22].faces, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[22].cells, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.1 (face 1, 3, 4 connection; 0, 2, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[22].faces, Permutation(-1, (3, 1, 2, 0, 7, 5, 6, 4)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[22].cells, Permutation(-1, (3, 1, 2, 0, 7, 5, 6, 4)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 0, 2, 4 connection; 1, 3, 5 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.5.2"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(5, 7), (6, 7), (3, 7)], [(0, 4), (4, 5), (0, 1), (1, 5)], [(0, 1), (1, 5), (1, 3)], [(1, 3), (0, 1), (2, 3), (0, 2)], [(2, 3), (0, 2), (2, 6)], [(0, 2), (2, 6), (0, 4), (4, 6)], [(0, 4), (4, 6), (4, 5)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[4, (0, 4), (4, 5), (4, 6)], [(7, 3), 7, (6, 7), (5, 7)], [(1, 3), 1, (0, 1), (5, 1)], [(2, 3), 2, (0, 2), (6, 2)]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 0, 3, 5 connection; 1, 2, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[26].faces, Permutation(-1, (6, 7, 2, 3, 4, 5, 0, 1)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[26].cells, Permutation(-1, (6, 7, 2, 3, 4, 5, 0, 1)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 1, 2, 5 connection; 0, 3, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[26].faces, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[26].cells, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # MC33 Case 13.5.2 (face 1, 3, 4 connection; 0, 2, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[26].faces, Permutation(-1, (3, 1, 2, 0, 7, 5, 6, 4)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[26].cells, Permutation(-1, (3, 1, 2, 0, 7, 5, 6, 4)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 2, 5 connection; 0, 1, 3, 4 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.3 (inverse)"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(2, 3), (0, 2), (2, 6)], [(0, 7), (4, 6), (0, 4)], [(0, 7), (4, 6), (3, 7), (6, 7)], [(0, 4), (0, 7), (0, 1), (1, 3)], [(5, 7), (4, 5), (3, 7), (0, 7)], [(4, 5), (1, 5), (0, 7), (1, 3)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[2, (2, 3), (0, 2), (2, 6)], [(5, 7), (7, 3), (7, 6), 7], [(5, 7), (7, 6), (7, 3), (5, 4), (4, 6), (5, 2)], [(5, 4), (4, 6), (4, 0), 4], [(5, 4), (4, 6), (4, 0), (5, 2)], [(5, 4), (4, 0), (5, 2), (5, 1), (1, 0), (1, 3)], [(5, 1), (1, 3), (1, 0), 1]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 0, 5 connection; 1, 2, 3, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(-1, (0, 2, 1, 6, 4, 5, 3, 7)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(-1, (0, 2, 1, 6, 4, 5, 3, 7)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 1, 5 connection; 0, 2, 3, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(1, (3, 2, 1, 0, 7, 6, 5, 4)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(1, (3, 2, 1, 0, 7, 6, 5, 4)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 3, 5 connection; 0, 1, 2, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(-1, (2, 3, 0, 1, 6, 7, 4, 5)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(-1, (2, 3, 0, 1, 6, 7, 4, 5)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 0, 4 connection; 1, 2, 3, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(1, (4, 6, 5, 7, 0, 2, 1, 3)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(1, (4, 6, 5, 7, 0, 2, 1, 3)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 1, 4 connection; 0, 2, 3, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(1, (7, 5, 6, 4, 3, 1, 2, 0)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(1, (7, 5, 6, 4, 3, 1, 2, 0)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 2, 4 connection; 0, 1, 3, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(-1, (4, 5, 6, 7, 0, 1, 2, 3)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(-1, (4, 5, 6, 7, 0, 1, 2, 3)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 3, 4 connection; 0, 1, 2, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(1, (6, 7, 4, 5, 2, 3, 0, 1)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(1, (6, 7, 4, 5, 2, 3, 0, 1)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 0, 3 connection; 1, 2, 4, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(1, (7, 3, 5, 1, 6, 2, 4, 0)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(1, (7, 3, 5, 1, 6, 2, 4, 0)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 1, 3 connection; 0, 2, 4, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(1, (2, 6, 0, 4, 3, 7, 1, 5)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(1, (2, 6, 0, 4, 3, 7, 1, 5)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 1, 2 connection; 0, 3, 4, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(-1, (0, 4, 2, 6, 1, 5, 3, 7)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(-1, (0, 4, 2, 6, 1, 5, 3, 7)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.3 (face 0, 2 connection; 1, 3, 4, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[30].faces, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[30].cells, Permutation(-1, (5, 1, 7, 3, 4, 0, 6, 2)))
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.2 (face 0 connection; 1, 2, 3, 4, 5 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.2 (inverse)"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(1, 0), (1, 3), (1, 5)], [(7, 6), (5, 7), (3, 7)], [(0, 4), (0, 2), (5, 4), (3, 2)], [(5, 4), (3, 2), (4, 6), (2, 6)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[(1, 0), 1, (1, 3), (1, 5)], [(7, 6), 7, (5, 7), (3, 7)], [(4, 0), 4, (4, 6), (4, 5)], [(2, 3), 2, (0, 2), (6, 2)], [(6, 2), (0, 2), (2, 3), (4, 6), (4, 0), (4, 5)]]
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.2 (face 1 connection; 0, 2, 3, 4, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[42].faces, ROTATE_FACES_0_2_4 * ROTATE_FACES_0_3_5)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[42].cells, ROTATE_FACES_0_2_4 * ROTATE_FACES_0_3_5)
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.2 (face 2 connection; 0, 1, 3, 4, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[42].faces, MIRROR_FACES_0_TO_2)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[42].cells, MIRROR_FACES_0_TO_2)
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.2 (face 3 connection; 0, 1, 2, 4, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[42].faces, ROTATE_FACES_0_3_5)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[42].cells, ROTATE_FACES_0_3_5)
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.2 (face 4 connection; 0, 1, 2, 3, 5 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[42].faces, MIRROR_FACES_0_TO_4)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[42].cells, MIRROR_FACES_0_TO_4)
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.2 (face 5 connection; 0, 1, 2, 3, 4 missing)
# #BCTcube3d.base_cases[16].mc33.append(Triangulation())
# #BCTcube3d.base_cases[16].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[16].mc33[42].faces, ROTATE_FACES_0_3_5 * ROTATE_FACES_0_3_5)
# #BCTcube3d.base_cases[16].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[16].mc33[42].cells, ROTATE_FACES_0_3_5 * ROTATE_FACES_0_3_5)
# # 1,0,0,1,0,1,1,0 -> 01101001 # Inverse of MC33 Case 13.1 (no face connection; 0, 1, 2, 3, 4, 5, 6, 7 missing)
# BCTcube3d.base_cases[16].mc33.append(Triangulation())
# BCTcube3d.base_cases[16].mc33[-1].name = "MC33 Case 13.1 (inverse)"
# BCTcube3d.base_cases[16].mc33[-1].faces = [[(0, 1), (1, 3), (1, 5)], [(0, 2), (2, 3), (2, 6)], [(0, 4), (4, 5), (4, 6)], [(3, 7), (5, 7), (6, 7)]]
# BCTcube3d.base_cases[16].mc33[-1].cells = [[1, (0, 1), (1, 3), (1, 5)], [2, (0, 2), (2, 3), (2, 6)], [4, (0, 4), (4, 5), (4, 6)], [7, (3, 7), (5, 7), (6, 7)]]
# BCTcube3d.base_cases[16].tests = binaryheap((TEST_FACE_0,
#                                           (TEST_FACE_1,
#                                            (TEST_FACE_2,
#                                             (TEST_FACE_3,
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5, CASE_IS_REGULAR, 5),
#                                               4), # 0,1,2,3 impossible
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5, 3, 9),
#                                               13)), # 0,1,2 impossible
#                                              # Face 2 outside
#                                             (TEST_FACE_4,
#                                              (TEST_FACE_5, 2, 6),
#                                              12), # 0,1,3 impossible
#                                             ), # 0,2,3; 1,2,3; 2,3,4; 2,3,5 impossible
#                                             # Face 1 outside
#                                            (TEST_FACE_2,
#                                             (TEST_FACE_3,
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5, 1, 8),
#                                               11), # 0,2,3 impossible
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5,
#                                                15,
#                                                (TEST_INTERIOR_1, 22, 26)),
#                                               (TEST_FACE_5, 18, 41))),
#                                             (TEST_FACE_3,
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5, 16, 20),
#                                               (TEST_FACE_5,
#                                                (TEST_INTERIOR_2, 23, 27),
#                                                38)),
#                                              (TEST_FACE_4,
#                                               34, # 0,4,5 impossible
#                                               (TEST_FACE_5, 31, 42))))),
#                                            # Face 0 outside
#                                           (TEST_FACE_1,
#                                            (TEST_FACE_2,
#                                             (TEST_FACE_3,
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5, 0, 7),
#                                               10), # 1,2,3 impossible
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5, 14, 21),
#                                               (TEST_FACE_5,
#                                                (TEST_INTERIOR_1, 24, 28),
#                                                40))),
#                                             (TEST_FACE_3,
#                                              (TEST_FACE_4,
#                                               (TEST_FACE_5,  
#                                                17,
#                                                (TEST_INTERIOR_1, 25, 29)),
#                                               (TEST_FACE_5, 19, 39)),
#                                              (TEST_FACE_4,
#                                               35, # 1,4,5 impossible
#                                               (TEST_FACE_5, 32, 43)))),
#                                             # Face 0, 1 outside
#                                            (TEST_FACE_2,
#                                             # 2,3,4,5; 2,3,4; 2,3,5; 2,3 impossible
#                                             (TEST_FACE_4,
#                                              36, # 2,3,4 impossible
#                                              (TEST_FACE_5, 30, 44)),
#                                             (TEST_FACE_3,
#                                              (TEST_FACE_4,
#                                               37, # 3,4,5 impossible
#                                               (TEST_FACE_5, 33, 45)),
#                                              (TEST_FACE_4,
#                                               46, # 4,5 impossible
#                                               (TEST_FACE_5, 47, 48)))))))
# # 1,1,1,1,0,1,1,0 -> 01101111 # Inverse of MC33 Case 3.2
# BCTcube3d.base_cases[18].mc33.append(Triangulation())
# BCTcube3d.base_cases[18].mc33[-1].name = "MC33 Case 3.2 (inverse)"
# BCTcube3d.base_cases[18].mc33[-1].faces = [[(4, 5), (0, 4), (5, 7), (3, 7)], [(0, 4), (4, 6), (3, 7), (6, 7)]]
# BCTcube3d.base_cases[18].mc33[-1].cells = [[4, (0, 4), (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), (3, 7), (5, 7), (6, 7)], [7, (3, 7), (5, 7), (6, 7)]]
# BCTcube3d.base_cases[18].tests = binaryheap((TEST_FACE_5, CASE_IS_REGULAR, 0))
# # 0,1,1,1,1,1,1,0 -> 01111110 # Inverse of MC Case 4.2
# BCTcube3d.base_cases[19].mc33.append(Triangulation())
# BCTcube3d.base_cases[19].mc33[-1].name = "MC33 Case 4.2 (inverse)"
# BCTcube3d.base_cases[19].mc33[-1].faces = [[(0, 1), (3, 7), (0, 4), (5, 7)], [(0, 4), (5, 7), (0, 2), (6, 7)], [(0, 2), (6, 7), (0, 1), (3, 7)]]
# BCTcube3d.base_cases[19].mc33[-1].cells = [[0, (0, 1), (0, 2), (0, 4)], [(0, 1), (0, 2), (0, 4), (3, 7), (6, 7), (5, 7)], [7, (3, 7), (5, 7), (6, 7)]]
# BCTcube3d.base_cases[19].tests = binaryheap((TEST_INTERIOR_0, 0, CASE_IS_REGULAR))
# # 1,0,1,1,1,1,0,0 -> 00111101 # Inverse of MC33 Case 6.1.2
# ############## TODO : ALLE 14er NEU MACHEN !!!!!
# BCTcube3d.base_cases[14].mc33.append(Triangulation())
# BCTcube3d.base_cases[14].mc33[-1].name = "MC33 Case 6.1.2 (inverse)"
# BCTcube3d.base_cases[14].mc33[-1].faces = [[(1, 5), (1, 3), (5, 7), (3, 7)], [(2, 6), (3, 7), (1, 3)], [(1, 3), (0, 1), (2, 6), (4, 6)], [(3, 7), (5, 7), (4, 6)]]
# BCTcube3d.base_cases[14].mc33[-1].cells = [[6, (2, 6), (4, 6), 7, (3, 7), (5, 7)], [(2, 6), (4, 6), (3, 7), (5, 7), (0, 1), 1, (1, 3), (1, 5)]]
# # 1,0,1,1,1,1,0,0 -> 00111101 # Inverse of MC33 Case 6.2
# BCTcube3d.base_cases[14].mc33.append(Triangulation())
# BCTcube3d.base_cases[14].mc33[-1].name = "MC33 Case 6.2 (inverse)"
# BCTcube3d.base_cases[14].mc33[-1].faces = [[(2, 6), (3, 7), (1, 3)], [(1, 3), (0, 1), (2, 6), (4, 6)], [(3, 7), (5, 7), (4, 6)]]
# BCTcube3d.base_cases[14].mc33[-1].cells = BCTcube3d.base_cases[14].mc33[0].cells
# BCTcube3d.base_cases[14].tests = binaryheap((TEST_FACE_1,
#                                     1,
#                                     (TEST_INTERIOR_1, 0, CASE_IS_REGULAR)
#                                     ))
# # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.2 (face 0 connection)
# BCTcube3d.base_cases[17].mc33.append(Triangulation())
# BCTcube3d.base_cases[17].mc33[-1].name = "MC33 Case 7.2 (inverse)"
# BCTcube3d.base_cases[17].mc33[-1].faces = [[(3, 7), (5, 7), (6, 7)], [(2, 3), (4, 5), (0, 2), (0, 4)], [(2, 6), (4, 6), (2, 3), (4, 5)]]
# BCTcube3d.base_cases[17].mc33[-1].cells = [[(2, 3), 2, (0, 2), (2, 6)], [(4, 5), (4, 6), (0, 4), 4], [(3, 7), (6, 7), (5, 7), 7], [(0, 2), (2, 3), (2, 6), (0, 4), (4, 5), (4, 6)]]
# # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.2 (face 3 connection)
# ## BCTcube3d.base_cases[17].mc33.append(Triangulation())
# ## BCTcube3d.base_cases[17].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[17].mc33[0].faces, ROTATE_FACES_0_3_5)
# ## BCTcube3d.base_cases[17].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[17].mc33[0].cells, ROTATE_FACES_0_3_5)
# ## # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.2 (face 5 connection)
# ## BCTcube3d.base_cases[17].mc33.append(Triangulation())
# ## BCTcube3d.base_cases[17].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[17].mc33[1].faces, ROTATE_FACES_0_3_5)
# ## BCTcube3d.base_cases[17].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[17].mc33[1].cells, ROTATE_FACES_0_3_5)
# # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.3 (face 0 and face 3 connection)
# BCTcube3d.base_cases[17].mc33.append(Triangulation())
# BCTcube3d.base_cases[17].mc33[-1].name = "MC33 Case 7.3 (inverse)"
# BCTcube3d.base_cases[17].mc33[-1].faces = [[(0, 2), (2, 3), (0, 7)], [(2, 3), (0, 7), (3, 7), (5, 7)], [(0, 7), (0, 2), (4, 5), (0, 4)], [(2, 6), (6, 7), (0, 7), (5, 7)], [(4, 6), (2, 6), (4, 5), (0, 7)]]
# BCTcube3d.base_cases[17].mc33[-1].cells = [[(7, 5), 7, (7, 3), (6, 7)], [(6, 2), (2, 3), (6, 1), (6, 7), (7, 3), (7, 5)], [(2, 3), 2, (2, 0), (6, 2)], [(2, 3), (6, 1), (2, 0), (6, 2)], [(6, 4), (4, 0), (4, 5), (6, 2), (2, 0), (6, 1)], [(4, 5), 4, (4, 0), (6, 4)]]
# # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.3 (face 3 and face 5 connection)
# ## BCTcube3d.base_cases[17].mc33.append(Triangulation())
# ## BCTcube3d.base_cases[17].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[17].mc33[3].faces, ROTATE_FACES_0_3_5)
# ## BCTcube3d.base_cases[17].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[17].mc33[3].cells, ROTATE_FACES_0_3_5)
# ## # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.3 (face 0 and face 5 connection)
# ## BCTcube3d.base_cases[17].mc33.append(Triangulation())
# ## BCTcube3d.base_cases[17].mc33[-1].faces = permute_geom_list(2, BCTcube3d.base_cases[17].mc33[4].faces, ROTATE_FACES_0_3_5)
# ## BCTcube3d.base_cases[17].mc33[-1].cells = permute_geom_list(3, BCTcube3d.base_cases[17].mc33[4].cells, ROTATE_FACES_0_3_5)
# # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.4.1
# BCTcube3d.base_cases[17].mc33.append(Triangulation())
# BCTcube3d.base_cases[17].mc33[-1].name = "MC33 Case 7.4.1 (inverse)"
# BCTcube3d.base_cases[17].mc33[-1].faces = [[(7, 3), (2, 3), (7, 5), (2, 0)], [(7, 5), (2, 0), (4, 5), (4, 0)], [(6, 4), (6, 2), (6, 7)]]
# BCTcube3d.base_cases[17].mc33[-1].cells = [[(2, 3), 2, (0, 2), (2, 6)], [(4, 5), (4, 6), (0, 4), 4], [(3, 7), (6, 7), (5, 7), 7], [(0, 2), (2, 3), (2, 6), (0, 4), (4, 5), (4, 6)], [(3, 7), (2, 3), (2, 6), (5, 7), (4, 5), (4, 6)], [(6, 7), (5, 7), (3, 7), (4, 6)], [(6, 7), (5, 7), (3, 7), (2, 6)], [(6, 7), (5, 7), (4, 6), (2, 6)]]
# # 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of MC33 Case 7.4.2
# BCTcube3d.base_cases[17].mc33.append(Triangulation())
# BCTcube3d.base_cases[17].mc33[-1].name = "MC33 Case 7.4.2 (inverse)"
# BCTcube3d.base_cases[17].mc33[-1].faces = [[(7, 5), (7, 3), (6, 7)], [(6, 2), (6, 7), (2, 3), (7, 3)], [(2, 3), (2, 0), (6, 2)], [(6, 4), (6, 2), (4, 0), (2, 0)], [(4, 0), (4, 5), (6, 4)], [(6, 4), (6, 7), (4, 5), (7, 5)]]
# BCTcube3d.base_cases[17].mc33[-1].cells = BCTcube3d.base_cases[17].cells
# BCTcube3d.base_cases[17].tests = binaryheap((TEST_FACE_0,
#                                           (TEST_FACE_3,
#                                            (TEST_FACE_5,
#                                             (TEST_INTERIOR_1, 7, 6),
#                                             3),
#                                            (TEST_FACE_5, 5, 0)),
#                                           (TEST_FACE_3,
#                                            (TEST_FACE_5, 4, 1),
#                                            (TEST_FACE_5, CASE_IS_REGULAR, 2))))
# # generate code
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
