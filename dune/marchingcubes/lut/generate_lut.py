#!/usr/bin/env python

from sys import exit

from lutgen.vtk import Vtk
from lutgen.generator import LookupGenerator
from lutgen.generator import BaseCase
#from generator import GeneratorContainer
from lutgen.consistencycheck import Consistency
from lutgen.dunecode import DuneCode

# Constants for mc 33 test order
TEST_FACE_1 = -1
TEST_FACE_2 = -2
TEST_FACE_3 = -3
TEST_FACE_4 = -4
TEST_FACE_5 = -5
TEST_FACE_0 = -6
TEST_CENTER = -7
CASE_IS_REGULAR = -8

################################################################################
## 3D Cube                                                                    ##
################################################################################
cube3d = LookupGenerator(3,"cube")
# base cases cube 3D:
# 0,0,0,0,0,0,0,0 -> 00000000 # Basic Case 0
cube3d.base_cases[0].faces = []
cube3d.base_cases[0].cells = [[0, 1, 2, 3, 4, 5, 6, 7]]
# 1,0,0,0,0,0,0,0 -> 00000001 # Basic Case 1
cube3d.base_cases[1].faces = [[(0, 4), (0, 1), (0, 2)]]
cube3d.base_cases[1].cells = [[(0, 4), (0, 1), (0, 2), 4, 5, 6], [(0, 1), 1, 5, (0, 2), 2, 6], [1, 3, 2, 5, 7, 6]]
# 1,1,0,0,0,0,0,0 -> 00000011 # Basic Case 2
cube3d.base_cases[2].faces = [[(0, 2), (1, 3), (0, 4), (1, 5)]]
cube3d.base_cases[2].cells = [[(1, 3), 3, (1, 5), 7, (0, 2), 2, (0, 4), 6], [(1, 5), 7, 5, (0, 4), 6, 4]]
# 0,1,1,0,0,0,0,0 -> 00000110 # Basic Case 3
cube3d.base_cases[3].faces = [[(1, 5), (0, 1), (1, 3)], [(2, 3), (0, 2), (2, 6)]]
cube3d.base_cases[3].cells = [[(1, 5), (1, 3), (0, 1), 5, 7, 4], [(1, 3), 3, 7, (0, 1), 0, 4], [(2, 3), 3, 7, (0, 2), 0, 4], [(2, 3), (0, 2), (2, 6), 7, 4, 6]]
# 1,1,1,0,0,0,0,0 -> 00000111 # Case 5
cube3d.base_cases[4].faces = [[(1, 3), (2, 3), (1, 5), (2, 6)], [(1, 5), (2, 6), (0, 4)]]
cube3d.base_cases[4].cells = [[(1, 5), (2, 6), (0, 4), 5, 6, 4], [3, (2, 3), (1, 3), 7, 6, 5], [(2, 3), (2, 6), 6, (1, 3), (1, 5), 5]]
# 1,1,1,1,0,0,0,0 -> 00001111 # Basic Case 8 and its inverse
cube3d.base_cases[5].faces = [[(0, 4), (1, 5), (2, 6), (3, 7)]]
cube3d.base_cases[5].cells = [[(0, 4), (1, 5), (2, 6), (3, 7), 4, 5, 6, 7]]
# 0,1,1,0,1,0,0,0 -> 00010110 # Basic Case 7
cube3d.base_cases[6].faces = [[(0, 1), (1, 3), (1, 5)], [(0, 2), (2, 6), (2, 3)], [(0, 4), (4, 5), (4, 6)]]
cube3d.base_cases[6].cells = [[(1, 5), (0, 1), (1, 3), 5, 0, 3], [(4, 5), (0, 4), (4, 6), 5, 0, 6], [(2, 3), (2, 6), (0, 2), 3, 6, 0], [5, 3, 6, 0], [5, 3, 6, 7]]
# 1,1,1,0,1,0,0,0 -> 00010111 # Basic Case 9 and its inverse
cube3d.base_cases[7].faces = [[(2, 3), (1, 3), (2, 6), (1, 5)], [(2, 6), (1, 5), (4, 6), (4, 5)]]
cube3d.base_cases[7].cells = [[(2, 3), (1, 3), 3, 6, 5, 7], [6, (2, 6), (2, 3), 5, (1, 5), (1, 3)], [(4, 6), (2, 6), 6, (4, 5), (1, 5), 5]]
# 0,0,0,1,1,0,0,0 -> 00011000 # Basic Case 4
cube3d.base_cases[8].faces = [[(0, 4), (4, 6), (4, 5)], [(1, 3), (2, 3), (3, 7)]]
cube3d.base_cases[8].cells = [[(0, 4), (4, 6), (4, 5), 0, 2, 1], [(4, 6), (4, 5), 6, 5, 2, 1, (2, 3), (1, 3)], [(1, 3), (2, 3), (3, 7), 5, 6, 7]]
# 1,0,0,1,1,0,0,0 -> 00011001 # Basic Case 6
cube3d.base_cases[9].faces = [[(4, 5), (4, 6), (0, 1), (0, 2)], [(2, 3), (3, 7), (1, 3)]]
cube3d.base_cases[9].cells = [[(4, 6), (4, 5), (0, 2), (0, 1), 7, 5, (1, 3), 1], [(4, 6), 6, 7, (0, 2), 2, (1, 3)], [6, 2, (1, 3), 7, (3, 7)], [2, (3, 7), (1, 3), (2, 3)]];
# 1,1,0,1,1,0,0,0 -> 00011011 # Basic Case 11 and its inverse
cube3d.base_cases[10].faces = [[(6, 4), (4, 5), (2, 0)], [(4, 5), (7, 3), (2, 0)], [(4, 5), (7, 3), (5, 1)], [(7, 3), (2, 0), (2, 3)]]
cube3d.base_cases[10].cells = [[(4, 5), (6, 4), (2, 0), (7, 3)], [(6, 4), 6, 2, (2, 0), (7, 3)], [(7, 3), (2, 0), 2, (2, 3)], [7, (4, 5), (6, 4), 6, (7, 3)], [7, (7, 3), (5, 1), 5, (4, 5)]]
# 0,1,1,1,1,0,0,0 -> 00011110 # Basic Case 12 and its inverse [TODO: Is here a face missing? (1, 5), (2, 6), (3, 7)] 
cube3d.base_cases[11].faces = [[(0, 1), (0, 2), (1, 5), (2, 6)], [(0, 4), (4, 5), (4, 6)]]
cube3d.base_cases[11].cells = [[0, (0, 1), (0, 2), (0, 4), (4, 5), (4, 6)], [(0, 2), (0, 1), (2, 6), (1, 5), (4, 6), (4, 5), 6, 5], [(2, 6), (1, 5), (3, 7), 6, 5, 7]]
# 1,1,1,1,1,0,0,0 -> 00011111 # Inverse of Basic Case 5
cube3d.base_cases[12].faces = [[(4, 5), (4, 6), (1, 5), (2, 6)], [(1, 5), (2, 6), (3, 7)]]
cube3d.base_cases[12].cells = [[(4, 5), 5, (1, 5), (4, 6), 6, (2, 6)], [6, 5, 7, (2, 6), (1, 5), (3, 7)]]
# 0,0,1,1,1,1,0,0 -> 00111100 # Basic Case 10 and its inverse 
cube3d.base_cases[13].faces = [[(0, 2), (1, 3), (2, 6), (3, 7)], [(0, 4), (1, 5), (4, 6), (5, 7)]]
cube3d.base_cases[13].cells = [[(0, 2), 0, (2, 6), 6, (1, 3), 1, (3, 7), 7], [6, 0, (4, 6), (0, 4), 7, 1, (5, 7), (1, 5)]]
# 1,0,1,1,1,1,0,0 -> 00111101 # Inverse of Basic Case 6
cube3d.base_cases[14].faces = [[(3, 7), (5, 7), (2, 6), (4, 6)], [(0, 1), (1, 3), (1, 5)]]
cube3d.base_cases[14].cells = [[6, (2, 6), (4, 6), 7, (3, 7), (5, 7)], [(0, 1), (1, 5), (1, 3), 1]]
# 1,1,1,1,1,1,0,0 -> 00111111 # Inverse of Basic Case 2
cube3d.base_cases[15].faces = [[(3, 7), (2, 6), (5, 7), (4, 6)]]
cube3d.base_cases[15].cells = [[6, (4, 6), (2, 6), 7, (5, 7), (3, 7)]]
# 1,0,0,1,0,1,1,0 -> 01101001 # Basic Case 13 and its inverse
cube3d.base_cases[16].faces = [[(0, 1), (0, 2), (0, 4)], [(2, 3), (1, 3), (3, 7)], [(4, 5), (5, 7), (1, 5)], [(2, 6), (4, 6), (6, 7)]]
cube3d.base_cases[16].cells = [[(0, 4), (0, 2), (0, 1), 4, (4, 6), (4, 5)], [(4, 5), (5, 7), (1, 5), (0, 1), (1, 3), 1], [(1, 3), (2, 3), (3, 7), (5, 7), (6, 7), 7], [(2, 6), (4, 6), (6, 7), 2, (0, 2), (2, 3)], [(0, 1), (1, 3), (0, 2), (2, 3), (4, 5), (5, 7), (4, 6), (6, 7)]]
# 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of Basic Case 7
cube3d.base_cases[17].faces = [[(2, 3), (2, 6), (0, 2)], [(6, 7), (3, 7), (5, 7)], [(0, 4), (4, 6), (4, 5)]]
cube3d.base_cases[17].cells = [[(2, 3), 2, (0, 2), (2, 6)], [(4, 5), (4, 6), (0, 4), 4], [(3, 7), (6, 7), (5, 7), 7]]
# 1,1,1,1,0,1,1,0 -> 01101111 # Inverse of Basic Case 3
cube3d.base_cases[18].faces = [[(0, 4), (4, 6), (4, 5)], [(6, 7), (5, 7), (3, 7)]]
cube3d.base_cases[18].cells = [[4, (4, 5), (0, 4), (4, 6)], [(6, 7), 7, (5, 7), (3, 7)]]
# 0,1,1,1,1,1,1,0 -> 01111110 # Inverse of Basic Case 4
cube3d.base_cases[19].faces = [[(0, 1), (0, 2), (0, 4)], [(3, 7), (5, 7), (6, 7)]]
cube3d.base_cases[19].cells = [[0, (0, 1), (0, 2), (0, 4)], [(6, 7), (5, 7), (3, 7), 7]]
# 1,1,1,1,1,1,1,0 -> 01111111 # Inverse of Basic Case 1 
cube3d.base_cases[20].faces = [[(6, 7), (3, 7), (5, 7)]]
cube3d.base_cases[20].cells = [[(6, 7), (5, 7), (3, 7), 7]]
# 1,1,1,1,1,1,1,1 -> 11111111 # Inverse of Basic Case 0 
cube3d.base_cases[21].faces = []
cube3d.base_cases[21].cells = []
# generate code
cube3d.generate()

################################################################################
## MC 33 cases and MC 33 face test table for 3D Cube                          ##
################################################################################
cube3d.mc33_cases = [[] for x in range(len(cube3d.base_cases))]
cube3d.base_case_numbers = { \
    (0, 0, 0, 0, 0, 0, 0, 0): 0, (1, 0, 0, 0, 0, 0, 0, 0): 1, (1, 1, 0, 0, 0, 0, 0, 0): 2, \
    (0, 1, 1, 0, 0, 0, 0, 0): 3, (0, 0, 0, 1, 1, 0, 0, 0): 4, (1, 1, 1, 0, 0, 0, 0, 0): 5, \
    (1, 0, 0, 1, 1, 0, 0, 0): 6, (0, 1, 1, 0, 1, 0, 0, 0): 7, (1, 1, 1, 1, 0, 0, 0, 0): 8, \
    (1, 1, 1, 0, 1, 0, 0, 0): 9, (0, 0, 1, 1, 1, 1, 0, 0): 10, (1, 1, 0, 1, 1, 0, 0, 0): 11, \
    (0, 1, 1, 1, 1, 0, 0, 0): 12, (1, 0, 0, 1, 0, 1, 1, 0): 13, (1, 0, 1, 1, 1, 0, 0, 0): 14, \
    (1, 1, 1, 1, 1, 1, 1, 1): 21, (1, 1, 0, 1, 0, 1, 1, 0): -7, (1, 0, 1, 1, 1, 1, 0, 0): -6, \
    (1, 1, 1, 1, 1, 0, 0, 0): -5, \
    (0, 1, 1, 1, 1, 1, 1, 0): 19, (1, 1, 1, 1, 0, 1, 1, 0): 18, (1, 1, 1, 1, 1, 1, 0, 0): 15, \
    (1, 1, 1, 1, 1, 1, 1, 0): -1
    } # TODO: korrekt missnamed basis cases
cube3d.mc33_tests = [[] for x in range(len(cube3d.base_cases))]


# 0,1,1,0,0,0,0,0 -> 00000110 # MC33 Case 3.2
cube3d.mc33_cases[3].append(BaseCase(cube3d.base_cases[3].dim, cube3d.base_cases[3].case))
cube3d.mc33_cases[3][0].faces = [[(0, 2), (2, 6), (0, 1), (1, 5)], [(2, 6), (2, 3), (1, 5), (1, 3)]]
cube3d.mc33_cases[3][0].cells = [[0, (0, 1), (0, 2), 4, 5, 6], [5, (1, 5), (0, 1), 6, (2, 6), (0, 2)], [5, (1, 5), (1, 3), 6, (2, 6), (2, 3)], [3, (2, 3), (1, 3), 7, 6, 5]]
cube3d.mc33_tests[3] = [TEST_FACE_4, CASE_IS_REGULAR, 0]
# 0,0,0,1,1,0,0,0 -> 00011000 # MC Case 4.2
cube3d.mc33_cases[8].append(BaseCase(cube3d.base_cases[8].dim, cube3d.base_cases[8].case))
cube3d.mc33_cases[8][0].faces = [[(4, 5), (6, 7), (0, 4), (2, 3)], [(4, 5), (3, 7), (4, 5), (6, 7)], [(0, 4), (2, 3), (4, 5), (3, 7)]]
cube3d.mc33_cases[8][0].cells = [[(4, 5), (3, 7), (1, 3), 5], [(4, 6), (4, 5), (3, 7), 7], [5, 7, (4, 5), (3, 7)], [6, (4, 5), (3, 7), (2, 3)], [2, (0, 4), (4, 5), (2, 3)], [0, (0, 4), 2, (2, 3)], [(4, 6), 6, 7, (3, 7)], [(4, 6), 6, (2, 3), 2], [1, (1, 3), 5, (4, 5)], [1, (1, 3), (0, 4), (4, 5)], [1, (1, 3), (0, 4), 0], [(1, 3), (2, 3), (0, 4), 0]]
cube3d.mc33_tests[8] = [TEST_FACE_3, CASE_IS_REGULAR, 0]
# 1,0,0,1,1,0,0,0 -> 00011001 # MC33 Case 6.1.2
cube3d.mc33_cases[9].append(BaseCase(cube3d.base_cases[9].dim, cube3d.base_cases[9].case))
cube3d.mc33_cases[9][0].faces = [[(1, 3), (1, 5), (3, 7), (5, 7)], [(0, 4), (5, 7), (1, 5)], [(0, 2), (0, 4), (3, 7), (6, 7)], [(0, 2), (3, 7), (1, 3)]]
cube3d.mc33_cases[9][0].cells = [[1, (0, 1), (1, 3), 5, (4, 5), (3, 7)], [5, (4, 5), (3, 7), 7], [(4, 5), (3, 7), 7, (4, 6)], [(3, 7), 7, (4, 6), (2, 3)], [(2, 3), (0, 2), 2, (6, 7), (4, 6), 6]]
# 1,0,0,1,1,0,0,0 -> 00011001 # MC33 Case 6.2
cube3d.mc33_cases[9].append(BaseCase(cube3d.base_cases[9].dim, cube3d.base_cases[9].case))
cube3d.mc33_cases[9][1].faces = [[(0, 4), (5, 7), (1, 5)], [(0, 2), (0, 4), (3, 7), (6, 7)], [(0, 2), (3, 7), (1, 3)]]
cube3d.mc33_cases[9][1].cells = cube3d.mc33_cases[9][0].cells
cube3d.mc33_tests[9] = [TEST_FACE_1, 1, TEST_CENTER, 1, 1, 0, CASE_IS_REGULAR]
# 0,1,1,0,1,0,0,0 -> 00010110 # Basic Case 7
cube3d.mc33_cases[6].append(BaseCase(cube3d.base_cases[6].dim, cube3d.base_cases[6].case))
cube3d.mc33_cases[6][0].faces = []
cube3d.mc33_cases[6][0].cells = []
cube3d.mc33_tests[6] = [TEST_FACE_1, 1, TEST_CENTER, 1, 1, 0, CASE_IS_REGULAR]


# 1,1,1,1,0,1,1,0 -> 01101111 # Inverse of MC33 Case 3.2
cube3d.mc33_cases[18].append(BaseCase(cube3d.base_cases[18].dim, cube3d.base_cases[18].case))
cube3d.mc33_cases[18][0].faces = [[(4, 5), (0, 4), (5, 7), (3, 7)], [(0, 4), (4, 6), (3, 7), (6, 7)]]
cube3d.mc33_cases[18][0].cells = [[4, (0, 4), (4, 5), (4, 6)], [(0, 4), (4, 5), (4, 6), (3, 7), (5, 7), (6, 7)], [7, (3, 7), (5, 7), (6, 7)]]
cube3d.mc33_tests[18] = [TEST_FACE_5, CASE_IS_REGULAR, 0]
# 0,1,1,1,1,1,1,0 -> 01111110 # Inverse of MC Case 4.2
cube3d.mc33_cases[19].append(BaseCase(cube3d.base_cases[19].dim, cube3d.base_cases[19].case))
cube3d.mc33_cases[19][0].faces = [[(0, 1), (3, 7), (0, 4), (5, 7)], [(0, 4), (5, 7), (0, 2), (6, 7)], [(0, 2), (6, 7), (0, 1), (3, 7)]]
cube3d.mc33_cases[19][0].cells = [[0, (0, 1), (0, 2), (0, 4)], [(0, 1), (0, 2), (0, 4), (3, 7), (6, 7), (5, 7)], [7, (3, 7), (5, 7), (6, 7)]]
cube3d.mc33_tests[19] = [TEST_FACE_2, CASE_IS_REGULAR, 0]
# 1,0,1,1,1,1,0,0 -> 00111101 # Inverse of MC33 Case 6.1.2
cube3d.mc33_cases[14].append(BaseCase(cube3d.base_cases[14].dim, cube3d.base_cases[14].case))
cube3d.mc33_cases[14][0].faces = [[(1, 5), (1, 3), (5, 7), (3, 7)], [(2, 6), (3, 7), (1, 3)], [(1, 3), (0, 1), (2, 6), (4, 6)], [(3, 5), (5, 7), (4, 6)]]
cube3d.mc33_cases[14][0].cells = [[6, (2, 6), (4, 6), 7, (3, 7), (5, 7)], [(2, 6), (4, 6), (3, 7), (5, 7), (0, 1), 1, (1, 3), (1, 5)]]
# 1,0,1,1,1,1,0,0 -> 00111101 # Inverse of MC33 Case 6.2
cube3d.mc33_cases[14].append(BaseCase(cube3d.base_cases[14].dim, cube3d.base_cases[14].case))
cube3d.mc33_cases[14][1].faces = [[(2, 6), (3, 7), (1, 3)], [(1, 3), (0, 1), (2, 6), (4, 6)], [(3, 5), (5, 7), (4, 6)]]
cube3d.mc33_cases[14][1].cells = cube3d.mc33_cases[14][0].cells
cube3d.mc33_tests[14] = [TEST_FACE_1, 1, TEST_CENTER, 1, 1, 0, CASE_IS_REGULAR]
# 1,1,0,1,0,1,1,0 -> 01101011 # Inverse of Basic Case 7
cube3d.mc33_cases[17].append(BaseCase(cube3d.base_cases[17].dim, cube3d.base_cases[17].case))
cube3d.mc33_cases[17][0].faces = []
cube3d.mc33_cases[17][0].cells = []
cube3d.mc33_tests[17] = [TEST_FACE_1, 1, TEST_CENTER, 1, 1, 0, CASE_IS_REGULAR]

#cube3d_mc33 = LookupGenerator(3, "cube3d")
## base cases cube 3D for marching cubes 33:
#
## DUNE: 0,1,1,0,0,0,0,0 -> MC: 00000110 # MC33 Case 3.1
#cube3d_mc33.base_cases[0].faces = cube3d.base_cases[3].faces
#cube3d_mc33.base_cases[0].faces = cube3d.base_cases[3].cells
## DUNE: 0,1,1,0,0,0,0,0 -> MC: 00000110 # MC33 Case 3.2
#cube3d_mc33.base_cases[1].faces = [[(0, 4), (0, 1), (0, 2), (1, 3)], [(0, 2), (1, 3), (4, 5), (1, 5)]]
#cube3d_mc33.base_cases[1].cells = [[(0, 2), (5, 7), 6, (0, 4), (4, 5), 4], [2, (0, 2), 3, 6], [(0, 2), (5, 7), 3, 6], [7, (5, 7), 3, 6], [(0, 2), (5, 7), 3, (0, 1), (1, 5), 1]]
## DUNE: 0,0,0,1,1,0,0,0 -> MC: 00011000 # MC33 Case 4.1
#cube3d_mc33.base_cases[2].faces = cube3d.base_cases[8].faces
#cube3d_mc33.base_cases[2].faces = cube3d.base_cases[8].cells
## DUNE: 0,0,0,1,1,0,0,0 -> MC: 00011000 # MC33 Case 4.2
#cube3d_mc33.base_cases[3].faces = [[(0, 1), (0, 2), (3, 7), (5, 7)], [(0, 2), (0, 4), (3, 7), (6, 7)], [(0, 1), (0, 4), (5, 7), (6, 7)]]
#cube3d_mc33.base_cases[3].cells = [[(0, 1), (1, 3), (1, 5), 1], [(0, 2), (0, 1), (3, 7), 3], [1, 3, (0, 1), (1, 3)], [2, (0, 1), (3, 7), (6, 7)], [6, (2, 6), (0, 1), (6, 7)], [4, (0, 4), 6, (6, 7)], [(0, 2), 2, 3, (3, 7)], [(0, 2), 2, (6, 7), 6], [5, (5, 7), 1, (0, 1)], [5, (5, 7), (0, 4), (0, 1)], [5, (5, 7), (0, 4), 4], [(5, 7), (6, 7), (0, 4), 4]]
## DUNE: 1,0,0,1,1,0,0,0 -> MC: 00011001 # MC33 Case 6.1.1
#cube3d_mc33.base_cases[3].faces = cube3d.base_cases[9].faces
#cube3d_mc33.base_cases[3].faces = cube3d.base_cases[9].cells
## DUNE: 1,0,0,1,1,0,0,0 -> MC: 00011001 # MC33 Case 6.1.2
#cube3d_mc33.base_cases[4].faces = [[(0, 4), (1, 5), (6, 7), (5, 7)], [(0, 2), (0, 4), (6, 7)], [(0, 2), (1, 3), (6, 7), (3, 7)], [(0, 1), (0, 4), (1,5), (4, 5)]]
#cube3d_mc33.base_cases[4].cells = [[(0, 4), (6, 7), 4, (1, 5), (4, 6), 5], [(0, 4), 6, (6, 7), 4], [(0, 4), 6, (6, 7), (0, 2)], [(0, 2), (6, 7), (3, 7), 6], [2, 6, (0, 2), 3, (3, 7), (1, 3)]]
## DUNE: 1,0,0,1,1,0,0,0 -> MC: 00011001 # MC33 Case 6.2
#cube3d_mc33.base_cases[5].faces = [[(0, 4), (1, 5), (6, 7), (5, 7)], [(0, 2), (0, 4), (6, 7)], [(0, 2), (1, 3), (6, 7), (3, 7)]]
#cube3d_mc33.base_cases[5].cells = cube3d_mc33.base_cases[4].cells
## DUNE: 0,1,1,0,1,0,0,0 -> MC: 00010110 # MC33 Case 7.1
#cube3d_mc33.base_cases[6].faces = cube3d.base_cases[6].faces
#cube3d_mc33.base_cases[6].cells = cube3d.base_cases[6].cells
## DUNE: 0,1,1,0,1,0,0,0 -> MC: 00010110 # MC33 Case 7.2
#cube3d_mc33.base_cases[7].faces = [[(0, 1), (1, 3), (1, 5)], [(4, 5), (5, 7), (0, 4), (3, 7)], [(0, 4), (3, 7), (4, 6), (6, 7)]]
#cube3d_mc33.base_cases[7].cells = [[3, 0, 2, (6, 7), (4, 6), 6], [(4, 6), (0, 4), 0, (6, 7), (3, 7), 6], [0, (0,4), (4, 5), 3, (3, 7), (5, 7)], [0, (0,4), (4, 5), 3, (1, 3), (5, 7)], [5, (5, 7), (4, 5), (1, 5), (1, 3), (0, 1)]]
## DUNE: 0,1,1,0,1,0,0,0 -> MC: 00010110 # MC33 Case 7.3
#cube3d_mc33.base_cases[8].faces = [[(4, 5), (5, 7), (0, 4), (0, 7)], [(5, 7), (0, 7), (1, 5), (0, 1)], [(0, 1), (0, 7), (1, 3), (3, 7)], [(3, 7), (0, 7), (6, 7), (4, 6)], [(0, 4), (4, 6), (0, 7)]]
#cube3d_mc33.base_cases[8].cells = [[5, (5, 7), (4, 5), (1, 5), (0, 7), (0, 4)], [(0, 4), (0, 1), (1, 5), (0, 7)], [0, 2, (0, 7), (0, 1)], [(1, 3), 2, (0, 7), (0, 1)], [(1, 3), 3, (0, 7), 2], [(1, 3), (3, 7), (0, 7), 3], [(1, 3), 2, (0, 7), 3], [2, (1, 3), (0, 7), (6, 7)], [(4, 6), 6, (0, 7), (6, 7)], [(4, 6), 6, (0, 7), 2], [(6, 7), 6, (0, 7), 2], [(0, 4), (0, 1), 0, (4, 6), (0, 7), 2]]
## DUNE: 0,1,1,0,1,0,0,0 -> MC: 00010110 # MC33 Case 7.4.1
#cube3d_mc33.base_cases[9].faces = [[(1, 5), (4, 5), (5, 7)], [(0, 1), (0, 4), (1, 3), (3, 7)], [(0, 4), (4, 6), (3, 7), (6, 7)]]
#cube3d_mc33.base_cases[9].cells = [[0, (0, 4), (0, 1), 3, (3, 7), (1, 3)], [0, 2, 3, (0, 4), 6, (3, 7)], [(6, 7), (4, 6), (3, 7), 6], [(6, 7), (4, 6), 6, (0, 4)], [5, (4, 5), (5, 7), (1, 5)]]
## DUNE: 0,1,1,0,1,0,0,0 -> MC: 00010110 # MC33 Case 7.4.2
#cube3d_mc33.base_cases[10].faces = [[(0, 4), (4, 5), (4, 6)], [(4, 5), (4, 6), (5, 7), (6, 7)], [(3, 7), (5, 7), (6, 7)], [(3, 7), (5, 7), (1, 3), (1, 5)], [(0, 1), (1, 3), (1, 5)], [(0, 1), (1, 5), (0, 4), (4, 5)]]
#cube3d_mc33.base_cases[10].cells = cube3d_mc33.base_cases[6].cells
## DUNE: 0,0,1,1,1,1,0,0 -> MC: 00111100 # MC33 Case 10.1.1 and inverse of MC33 Case 10.1.2
#cube3d_mc33.base_cases[11].faces = cube3d.base_cases[13].faces
#cube3d_mc33.base_cases[11].cells = cube3d.base_cases[13].cells
## DUNE: 0,0,1,1,1,1,0,0 -> MC: 00111100 # MC33 Case 10.1.2 and inverse of MC33 Case 10.1.1
#cube3d_mc33.base_cases[12].faces = [[(4, 5), (5, 7), (4, 6), (6, 7)], [(4, 6), (6, 7), (0, 2), (2, 3)], [(0, 2), (2, 3), (0, 1), (1, 3)], [(0, 1), (1, 3), (4, 5), (5, 7)]]
#cube3d_mc33.base_cases[12].cells = [[0, (0, 2), (6, 7), 4, (4, 6), (4, 5)], [(0, 2), (0, 1), (2, 3), (4, 6), (4, 5), (6, 7)], [(4, 5), (5, 7), (6, 7), (0, 1), (1, 3), (2, 3)], [7, (5, 7), (6, 7), 6, (4, 6), (2, 3)]]
## DUNE: 0,0,1,1,1,1,0,0 -> MC: 00111100 # MC33 Case 10.2 and its inverse
#cube3d_mc33.base_cases[13].faces = [[(0, 7), (0, 1), (4, 6), (4, 5)], [(4, 6), (0, 7), (0, 2), (2, 3)], [(2, 3), (0, 7), (6, 7), (5, 7)], [(0, 7), (5, 7), (0, 1), (1, 3)]]
#cube3d_mc33.base_cases[13].cells = [[0, (0, 2), (0, 1), 4, (4, 6), (4, 5)], [(0, 2), (0, 7), (4, 6), (4, 5)], [(0, 2), (0, 1), (0, 7), (4, 5)], [(0, 2), (0, 1), (0, 7), (1, 3)], [(0, 2), (1, 3), (0, 7), (2, 3)], [(6, 7), (1, 3), (0, 7), (2, 3)], [(6, 7), (1, 3), (0, 7), (5, 7)], [7, (5, 7), (6, 7), 3, (1, 3), (2, 3)]]
## DUNE: 0,1,1,1,1,0,0,0 -> MC: 00011110 # MC33 Case 12.1.1
#cube3d_mc33.base_cases[14].faces = cube3d.base_cases[11].faces
#cube3d_mc33.base_cases[14].cells = cube3d.base_cases[11].cells
## DUNE: 0,1,1,1,1,0,0,0 -> MC: 00011110 # MC33 Case 12.1.2
#cube3d_mc33.base_cases[15].faces = [[(0, 1), (1, 5), (0, 4), (4, 5)], [(1, 5), (4, 5), (3, 7), (4, 6)], [(3, 7), (4, 6), (2, 6)], [(2, 6), (4, 6), (0, 2), (0, 4)], [(0, 2), (0, 4), (0, 1)]]
#cube3d_mc33.base_cases[15].cells = [[5, (4, 5), (1, 5), 7, (4, 6), (3, 7)], [0, (0, 4), (0, 1), (0, 2)], [6, 7, (4, 6), (3, 7)], [6, (4, 6), (4, 6), (3, 7)]]
## DUNE: 0,1,1,1,1,0,0,0 -> MC: 00011110 # MC33 Case 12.2
#cube3d_mc33.base_cases[16].faces = [[(0, 1), (0, 2), (0, 7), (2, 6)], [(0, 7), (2, 6), (1, 5), (3, 7)], [(1, 5), (0, 7), (4, 5), (4, 6)], [(4, 6), (0, 7), (0, 4), (0, 1)]]
#cube3d_mc33.base_cases[16].cells = [[5, (1, 5), (4, 5), (5, 7), (3, 7), (4, 6)], [(4, 6), 6, (2, 6), (5, 7), 7, (3, 7)], [(3, 7), (4, 5), (1, 5), (2, 6), (4, 6), (0, 7)], [(4, 6), (2, 6), (0, 7), (0, 4), (0, 2), (0, 1)], [0, (0, 4), (0, 2), (0, 1)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Basic Case 13.1
#cube3d_mc33.base_cases[17].faces = cube3d.base_cases[16].faces
#cube3d_mc33.base_cases[17].cells = cube3d.base_cases[16].faces
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Basic Case 13.2
#cube3d_mc33.base_cases[18].faces = [[(0, 4), (0, 2), (0, 1)], [(3, 7), (1, 3), (2, 3)], [(4, 5), (4, 6), (1, 5), (2, 6)], [(1, 5), (2, 6), (5, 7), (6, 7)]]
#cube3d_mc33.base_cases[18].cells = [[6, (6, 7), (2, 6), (4, 6)], [(5, 7), (1, 5), (4, 5), (6, 7), (2, 6), (4, 6)], [5, (1, (4, 5), 5), (5, 7)], [0, (0, 4), (0, 2), (0, 1)], [3, (3, 7), (1, 3), (2, 3)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Basic Case 13.3
#cube3d_mc33.base_cases[19].faces = [[(2, 3), (1, 3), (3, 7)], [(0, 4), (0, 1), (4, 6), (0, 7)], [(4, 6), (0, 7), (4, 5), (1, 5)], [(5, 7), (1, 5), (0, 7)], [(5, 7), (0, 7), (6, 7), (2, 6)], [(2, 6), (0, 7), (0, 2), (0, 1)]]
#cube3d_mc33.base_cases[19].cells = [[5, (4, 5), (1, 5), (5, 7), (4, 6), (0, 7)], [(5, 7), (4, 6), (0, 7), (6, 7), 6, (2, 6)], [(0, 7), (4, 6), (2, 6), 6], [(4, 6), (2, 6), (0, 7), (0, 4), (0, 2), (0, 1)], [0, (0, 4), (0, 2), (0, 1)], [3, (2, 3), (1, 3), (3, 7)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Basic Case 13.4 and its inverse
#cube3d_mc33.base_cases[20].faces = [[(0, 7), (4, 6), (0, 1), (0, 4)], [(0, 7), (0, 1), (2, 6), (0, 2)], [(0, 7), (4, 6), (1, 5), (4, 5)], [(0, 7), (6, 7), (1, 5), (5, 7)], [(0, 7), (1, 3), (6, 7), (3, 7)], [(0, 7), (1, 3), (2, 6), (2, 3)]]
#cube3d_mc33.base_cases[20].cells = [[5, (4, 5), (1, 5), (5, 7), (4, 6), (0, 7)], [(5, 7), (4, 6), (0, 7), (6, 7), 6, (2, 6)], [(0, 7), (4, 6), (2, 6), 6], [(4, 6), (2, 6), (0, 7), (0, 4), (0, 2), (0, 1)], [0, (0, 4), (0, 2), (0, 1)], [(2, 6), (0, 7), (4, 6), (2, 3), (1, 3), (3, 7)], [3, (2, 3), (1, 3), (3, 7)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Basic Case 13.5.1
#cube3d_mc33.base_cases[21].faces = [[(0, 4), (0, 2), (0, 1)], [(5, 7), (6, 7), (3, 7)], [(1, 3), (2, 3), (1, 5), (2, 6)], [(1, 5), (2, 6), (4, 5), (4, 6)]]
#cube3d_mc33.base_cases[21].cells = [[2, (0, 2), (1, 5), (1, 3)], [(0, 2), (2, 6), (2, 3), (0, 2), (1, 5), (1, 3)], [(0, 1), (4, 5), (1, 5), (0, 2), (4, 6), (2, 6)], [(0, 2), (0, 1), (0, 4), (4, 5), 4], [2, (2, 3), (2, 6), (0, 2)], [7, (3, 7), (5, 7), (6, 7)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Basic Case 13.5.2
#cube3d_mc33.base_cases[22].faces = [[(5, 7), (6, 7), (3, 7)], [(0, 4), (4, 5), (0, 1), (1, 5)], [(0, 1), (1, 5), (1, 3)], [(1, 3), (0, 1), (2, 3), (0, 2)], [(2, 3), (0, 2), (2, 6)], [(0, 2), (2, 6), (0, 4), (4, 6)] [(0, 4), (4, 6), (4, 5)]]
#cube3d_mc33.base_cases[22].cells = [[1, (0, 1), (1, 3), (1, 5)], [3, (1, 3), (2, 3), (3, 7)], [5, (1, 5), (4, 5), (5, 7)], [6, (2, 6), (4, 6), (6, 7)]]
#
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Inverse of MC33 Case 13.1
#cube3d_mc33.base_cases[23].faces = cube3d_mc33.base_cases[17].faces
#cube3d_mc33.base_cases[23].cells = [[0, (0, 1), (0, 2), (0, 4)], [3, (2, 3), (1, 3), (3, 7)], [5, (4, 5), (5, 7), (1, 5)], [6, (2, 6), (4, 6), (6, 7)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Inverse of MC33 Case 13.2
#cube3d_mc33.base_cases[24].faces = cube3d_mc33.base_cases[18].faces
#cube3d_mc33.base_cases[24].cells = [[4, (4, 6), (4, 5), (0, 4), (0, 2), (0, 1)], [1, (0, 1), (4, 5), 2, (0, 2), (4, 6)], [1, (1, 5), (4, 5), 2, (2, 6), (4, 6)], [2, (2, 6), (6, 7), 1, (1, 5), (5, 7)], [2, (2, 3), (6, 7), 1, (1, 3), (5, 7)], [7, (5, 7), (6, 7), (3, 7), (1, 3), (2, 3)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Inverse of MC33 Case 13.3
#cube3d_mc33.base_cases[25].faces = cube3d_mc33.base_cases[19].faces
#cube3d_mc33.base_cases[25].cells = [[4, (4, 6), (4, 5), (0, 1), (0, 7), (1, 5)], [(1, 5), (0, 1), (0, 4), (0, 7)], [(5, 7), 7, (0, 7), (6, 7)], [(2, 3), 7, (0, 7), (6, 7)], [(2, 3), (2, 6), (0, 7), (6, 7)], [(2, 3), (2, 6), (0, 2), 2], [1, (1, 3), (0, 7), (0, 1)], [(2, 3), (2, 6), (0, 2), (1, 3), (0, 7), (0, 1)], [(0, 7), (5, 7), 7, (2, 3), (1, 3), (3, 7)], [(1, 5), (0, 1), 1, (5, 7), (0, 7), (1, 3)]]
## DUNE: 1,0,0,1,0,1,1,0 -> MC: 01101001 # Inverse of Basic Case 13.5.2
#cube3d_mc33.base_cases[26].faces = cube3d_mc33.base_cases[22].faces
#cube3d_mc33.base_cases[26].cells = cube3d_mc33.base_cases[23].faces
## DUNE: 0,1,1,1,1,0,0,0 -> MC: 00011110 # Inverse of MC33 Case 12.1.1
#cube3d_mc33.base_cases[27].faces = cube3d_mc33.base_cases[14].faces
#cube3d_mc33.base_cases[27].cells = cube3d_mc33.base_cases[14].cells
## DUNE: 0,1,1,1,1,0,0,0 -> MC: 00011110 # Inverse of MC33 Case 12.1.2
#cube3d_mc33.base_cases[28].faces = cube3d_mc33.base_cases[15].faces
#cube3d_mc33.base_cases[28].cells = [[4, (4, 5), (4, 6), (0, 4), (0, 1), (0, 2)], [(3, 7), (4, 5), (1, 5), 3, (0, 1), 1], [(3, 7), (4, 5), (4, 6), 3, (0, 1), (1, 3)], [(3, 7), (2, 6), (4, 6), 3, 2, (1, 3)]]
## DUNE: 0,1,1,1,1,0,0,0 -> MC: 00011110 # Inverse of MC33 Case 12.2
#cube3d_mc33.base_cases[29].faces = cube3d_mc33.base_cases[16].faces
#cube3d_mc33.base_cases[29].cells = [[2, (2, 6), (0, 2), (2, 3), (3, 7), (0, 1)], [(0, 1), 1, (1, 5), (2, 3), 3, (3, 7)], [(3, 7), (0, 2), (2, 6), (1, 5), (0, 1), (0, 7)], [(0, 1), (1, 5), (0, 7), (0, 4), (4, 5), (4, 6)], [4, (0, 4), (4, 5), (4, 6)]]
## DUNE: 1,1,0,1,0,1,1,0 -> MC: 01101011 # Inverse of MC33 Case 7.1
#cube3d_mc33.base_cases[30].faces = cube3d.base_cases[17].faces
#cube3d_mc33.base_cases[30].cells = cube3d.base_cases[17].cells
## DUNE: 1,1,0,1,0,1,1,0 -> MC: 01101011 # Inverse of MC33 Case 7.2
#cube3d_mc33.base_cases[31].faces = cube3d_mc33.base_cases[7].faces
#cube3d_mc33.base_cases[31].cells = [[7, (6, 7), (3, 7), (5, 7)], [(4, 6), (0, 4), (4, 5), (6, 7), (3, 7), ((5, 7))], [4, (4, 5), (0, 4), (4, 6)], [1, (0, 1), (1, 3), (1, 5)]]
## DUNE: 1,1,0,1,0,1,1,0 -> MC: 01101011 # Inverse of MC33 Case 7.3
#cube3d_mc33.base_cases[32].faces = cube3d_mc33.base_cases[8].faces
#cube3d_mc33.base_cases[32].cells = [[4, (4, 5), (0, 4), (4, 6), (5, 7), (0, 7)], [(4, 6), (5, 7), (0, 7), (6, 7), 7, (3, 7)], [(0, 7), (5, 7), (3, 7), 7], [(5, 7), (3, 7), (0, 7), (1, 5), (1, 3), (0, 1)], [1, (0, 1), (1, 3), (1, 5)]]
## DUNE: 1,1,0,1,0,1,1,0 -> MC: 01101011 # Inverse of MC33 Case 7.4.1
#cube3d_mc33.base_cases[33].faces = cube3d_mc33.base_cases[9].faces
#cube3d_mc33.base_cases[33].cells = [[4, (0,4), (4, 6), (5, 7), (3, 7), (6, 7)], [4, (0,4), (0, 1), (5, 7), (3, 7), (1, 3)], [7, (3, 7), (5, 7), (6, 7)], [4, (5, 7), (1, 5), (0, 1), (1, 3), 1], [4, (0, 4), (4, 5), (4, 6)]]
## DUNE: 1,1,0,1,0,1,1,0 -> MC: 01101011 # Inverse of MC33 Case 7.4.2
#cube3d_mc33.base_cases[34].faces = cube3d_mc33.base_cases[10].faces
#cube3d_mc33.base_cases[34].cells = cube3d_mc33.base_cases[30].cells
## DUNE: 1,0,1,1,1,1,0,0 -> MC: 00111101 # Inverse of MC33 Case 6.1.1
#cube3d_mc33.base_cases[35].faces = cube3d.base_cases[14].faces
#cube3d_mc33.base_cases[35].faces = cube3d.base_cases[14].cells
## DUNE: 1,0,1,1,1,1,0,0 -> MC: 00111101 # Inverse of MC33 Case 6.1.2
#cube3d_mc33.base_cases[36].faces = cube3d_mc33.base_cases[4].faces
#cube3d_mc33.base_cases[36].cells = [[0, (0, 2), (0, 1), 1, (1, 3), (1, 5)], [(0, 4), (1, 3), (1, 5), (6, 7), (3, 7), (3, 7)], [(0, 4), (1, 3), (6, 7), (0, 2)], [(3, 7), (1, 3), (6, 7), (0, 2)], [7, (6, 7), (3, 7), (5, 7)]]
## DUNE: 1,0,1,1,1,1,0,0 -> MC: 00111101 # Inverse of MC33 Case 6.2
#cube3d_mc33.base_cases[37].faces = cube3d_mc33.base_cases[5].faces
#cube3d_mc33.base_cases[37].cells = cube3d_mc33.base_cases[36].cells
## DUNE: 0,1,1,1,1,1,1,0 -> MC: 01111110 # Inverse of MC33 Case 4.1
#cube3d_mc33.base_cases[38].faces = cube3d.base_cases[19].faces
#cube3d_mc33.base_cases[38].faces = cube3d.base_cases[19].cells
## DUNE: 0,1,1,1,1,1,1,0 -> MC: 01111110 # Inverse of MC33 Case 4.2
#cube3d_mc33.base_cases[39].faces = cube3d_mc33.base_cases[3].faces
#cube3d_mc33.base_cases[39].cells = [((0, 1), (0, 2), (0, 4), 0), ((0, 1), (0, 2), (0, 4), (5, 7), (3, 7), (6, 7)), ((3, 7), (5, 7), (6, 7), 7)]
## DUNE: 1,1,1,1,0,1,1,0 -> MC: 01101111 # Inverse of MC33 Case 3.1
#cube3d_mc33.base_cases[40].faces = cube3d.base_cases[18].faces
#cube3d_mc33.base_cases[40].faces = cube3d.base_cases[18].cells
## DUNE: 1,1,1,1,0,1,1,0 -> MC: 01101111 # Inverse of MC33 Case 3.2
#cube3d_mc33.base_cases[41].faces = cube3d_mc33.base_cases[1].faces
#cube3d_mc33.base_cases[41].cells = [[5, (1, 5) , (5, 7), (4, 5)], [(4, 5), (5, 7), (1, 5), (0, 4), (0, 2), (0, 1)], [0, (0, 1), (0, 4), (0, 2)]]



################################################################################
## 3D Simplex                                                                 ##
################################################################################
simplex3d = LookupGenerator(3,"simplex")
# base cases simplex 3D:
# 0,0,0,0 -> 0000
simplex3d.base_cases[0].faces = []
simplex3d.base_cases[0].cells = [[0, 1, 2, 3]]
# 1,0,0,0 -> 0001
simplex3d.base_cases[1].faces = [[(0,2), (0,1), (0,3)]]
simplex3d.base_cases[1].cells = [[(0,1), (0,2), (0,3), 1, 2, 3]]
# 1,1,0,0 -> 0011
simplex3d.base_cases[2].faces = [[(0,2), (1,2), (0,3), (1,3)]]
simplex3d.base_cases[2].cells = [[(0,2), (1,2), 2, (0,3), (1,3), 3]]
# 1,1,1,0 -> 0111
simplex3d.base_cases[3].faces = [[(1,3), (0,3), (2,3)]]
simplex3d.base_cases[3].cells = [[(0,3), (1,3), (2,3), 3]]
# 1,1,1,1 -> 1111
simplex3d.base_cases[4].faces = []
simplex3d.base_cases[4].cells = []
# generate code
simplex3d.generate()
simplex3d.base_case_numbers = {(0, 0, 0, 0): 0, (1, 0, 0, 0): 1, \
    (1, 1, 0, 0): 2, (1, 1, 1, 0): 3, (1, 1, 1, 1): 4}

################################################################################
## 2D Cube                                                                    ##
################################################################################
cube2d = LookupGenerator(2, "cube")
# base cases cube 2D:
# 0,0,0,0 -> 0000
cube2d.base_cases[0].faces = []
cube2d.base_cases[0].cells = [[0, 1, 2, 3]]
# 1,0,0,0 -> 0001
cube2d.base_cases[1].faces = [[(0, 1), (0, 2)]]
cube2d.base_cases[1].cells = [[1, 2, 3], [1, (0, 1), (0, 2), 2]]
# 1,1,0,0 -> 0011
cube2d.base_cases[2].faces = [[(1, 3), (0, 2)]]
cube2d.base_cases[2].cells = [[(0, 2), (1, 3), 2, 3]]
# 0,1,1,0 -> 0110
cube2d.base_cases[3].faces = [[(0, 1), (1, 3)], [(0, 2), (2, 3)]]
cube2d.base_cases[3].cells = [[0, 3, (0, 2), (2, 3)], [(0, 1), (1, 3), 0, 3]]
# 1,1,1,0 -> 0111
cube2d.base_cases[4].faces = [[(2, 3), (1, 3)]]
cube2d.base_cases[4].cells = [[3, (2, 3), (1, 3)]]
# 1,1,1,1 -> 1111
cube2d.base_cases[5].faces = []
cube2d.base_cases[5].cells = []
# generate code
cube2d.generate()

################################################################################
## MC 33 cases and MC 33 face test table for 2D Cube                          ##
################################################################################
cube2d.mc33_cases = [[] for x in range(len(cube2d.base_cases))]
cube2d.base_case_numbers = {(0, 0, 0, 0): 0, (1, 0, 0, 0): 1, \
    (1, 1, 0, 0): 2, (0, 1, 1, 0): 3, (1, 1, 1, 0): 4, (1, 1, 1, 1): 5}
cube2d.mc33_tests = [[] for x in range(len(cube2d.base_cases))]

# 0,1,1,0 -> 0110
cube2d.mc33_cases[3].append(BaseCase(cube2d.base_cases[3].dim, cube2d.base_cases[3].case))
cube2d.mc33_cases[3][0].faces = [[(1, 3), (0, 1)], [(2, 3), (0, 2)]]
cube2d.mc33_cases[3][0].cells = [[2, (2, 3), (0, 2)], [1, (1, 3), (0, 1)]]
cube2d.mc33_tests[3] = [TEST_FACE_0, CASE_IS_REGULAR, 0]


################################################################################
## 2D Simplex                                                                 ##
################################################################################
simplex2d = LookupGenerator(2,"simplex")
# base cases simplex 2D:
# 0,0,0 -> 000
simplex2d.base_cases[0].faces = []
simplex2d.base_cases[0].cells = [[0, 1, 2]]
# 1,0,0 -> 001
simplex2d.base_cases[1].faces = [[(0, 1), (0, 2)]]
simplex2d.base_cases[1].cells = [[(0, 2), (0, 1), 2, 1]]
# 1,1,0 -> 011
simplex2d.base_cases[2].faces = [[(0, 2), (1, 2)]]
simplex2d.base_cases[2].cells = [[(0, 2), (1, 2), 2]]
# 1,1,1 -> 111
simplex2d.base_cases[3].faces = []
simplex2d.base_cases[3].cells = []
# generate code
simplex2d.generate()
simplex2d.base_case_numbers = {(0, 0, 0): 0, (1, 0, 0): 1, \
    (1, 1, 0): -1, (1, 1, 1): 16}

################################################################################
## 1D Cube                                                                    ##
################################################################################
lut1d = LookupGenerator(1,"any")
# base cases cube 1D:
# 0,0 -> 00
lut1d.base_cases[0].faces = []
lut1d.base_cases[0].cells = [[0,1]]
# 1,0 -> 01
lut1d.base_cases[1].faces = [[(0,1)]]
lut1d.base_cases[1].cells = [[(0,1), 1]]
# 1,1 -> 11
lut1d.base_cases[2].faces = []
lut1d.base_cases[2].cells = []
# generate code
lut1d.generate()
lut1d.base_case_numbers = {(0, 0): 0, (1, 0): 1, (1, 1): 16}

################################################################################
## 0D Cube                                                                    ##
################################################################################
lut0d = LookupGenerator(0,"any")
# base cases cube 0D:
# 0 -> 0
lut0d.base_cases[0].faces = []
lut0d.base_cases[0].cells = [[0]]
# 1 -> 1
lut0d.base_cases[1].faces = []
lut0d.base_cases[1].cells = []
# generate code
lut0d.generate()

################################################################################
## Output                                                                     ##
################################################################################

#print """namespace Dune {
#
#    namespace MarchingInternal {
#"""

ccfile = open("marchinglut.cc", "w")
ccfile.write("""
    /*
     * This file is autogenerated using generate_lut.py
     *
     * Don't edit this file!
     */

#include "marchinglut.hh"

extern \"C\" {

""")


DuneCode(cube3d).write(ccfile)
DuneCode(simplex3d).write(ccfile)
DuneCode(cube2d).write(ccfile)
DuneCode(simplex2d).write(ccfile)
DuneCode(lut1d).write(ccfile)
#DuneCode(lut0d).write(ccfile)

ccfile.write("}\n")
ccfile.close()

#Vtk(cube3d).write()
#Vtk(simplex3d).write()
#Vtk(cube2d).write()
#Vtk(simplex2d).write()

generators = {
    (1,"any"): lut1d,
	(2, "simplex"): simplex2d,
	(2, "cube"): cube2d,
	(3, "simplex"): simplex3d,
#	(3, "prism"): prism3d,
#	(3, "pyramid"): pyramid3d,
	(3, "cube"): cube3d
	}

#Consistency(generators).check(3, "simplex")
# Consistency(generators).check(3, "cube")
