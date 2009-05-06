import math
from referenceelements import ReferenceElements
from sys import exit
from disambiguate import *

# Following constants are copied from marchinglut.hh
# constants for vertex and edge numbering
NO_VERTEX = 1<<6
VERTEX_GO_RIGHT = 1 # x1 = 1
VERTEX_GO_DEPTH = 2 # x2 = 1
VERTEX_GO_UP = 4 # x3 = 1
FACTOR_FIRST_POINT = 1
FACTOR_SECOND_POINT = 8
# vertices start with V
VA = 0
VB = VERTEX_GO_RIGHT
VC = VERTEX_GO_DEPTH
VD = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH
VE = VERTEX_GO_UP;
VF = VERTEX_GO_RIGHT + VERTEX_GO_UP
VG = VERTEX_GO_DEPTH + VERTEX_GO_UP
VH = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP
# edges start with E
EJ = VA * FACTOR_FIRST_POINT + VB * FACTOR_SECOND_POINT + NO_VERTEX
EK = VC * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX
EL = VA * FACTOR_FIRST_POINT + VC * FACTOR_SECOND_POINT + NO_VERTEX
EM = VB * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX
EN = VA * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX
EO = VB * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX
EP = VC * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX
EQ = VD * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX
ER = VE * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX
ES = VG * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX
ET = VE * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX
EU = VF * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX
# Diagonals for simplices
EV = VB * FACTOR_FIRST_POINT + VC * FACTOR_SECOND_POINT + NO_VERTEX
EW = VB * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX
EX = VC * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX
# Center point is in the center of a cube or tetrahedron
EY = VA * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX
# dictionary to get constant names from integers
const_names = {VA:"VA", VB:"VB", VC:"VC", VD:"VD", VE:"VE", \
    VF:"VF", VG:"VG", VH:"VH", EJ:"EJ", EK:"EK", EL:"EL", \
    EM:"EM", EN:"EN", EO:"EO", EP:"EP", EQ:"EQ", ER:"ER", \
    ES:"ES", ET:"ET", EU:"EU", EV:"EV", EW:"EW", EX:"EX", EY:"EY"}
# Constants indicating whether case special treatment when marching cubes' 33 is used.
CASE_UNIQUE_MC33 = 0
CASE_AMIGUOUS_MC33 = 1
# Constant indicates whether basic case was flipped.
CASE_FLIPPED = 4

# Stores a table as C-Code string for marchinglut.cc
class TableStorage:
    def __init__(self):
        # String contatining C-Code for the table
        self.tablestring = ""
        # Integer indicating the number of entries, is used for indexing from other tables
        self.offset = 0
    # Adds some entries to the table
    def append(self, toAppend, numberOfNewEntries):
        self.tablestring += toAppend
        self.offset += numberOfNewEntries

# Generates the tables, writes marchinglut.cc
class DuneCode:
    def __init__(self, lg):
        self.lg = lg
        self.referenceElement = ReferenceElements[self.lg.geometryType]
    # Generate lookup table
    def write(self, file):
        # generate value for a point on a vertex or in the center
        def edge(a, b):
            # ensure a < b
            if a > b:
                t = a
                a = b
                b = t
            # get center points
            if a == VA and b == VH or a == VB and b == VG \
                or a == VC and b == VF or a == VD and b == VE:
                return EY
            # points on an edge"
            try:
                # check whether edge exists, excpect 3D simplex because of changed numering
                if self.lg.basicType != "simplex" or self.lg.dim != 3:
                    self.referenceElement.edges.index(set([a,b]))
                return a * FACTOR_FIRST_POINT + b * FACTOR_SECOND_POINT + NO_VERTEX
            except ValueError:
                raise ValueError, "Edge (%i, %i) does not exist in %s" % \
                    (a, b, repr(self.lg.geometryType))
        # returns the constant name of the point as a string given by its number
        def get_point_name(v):
            # point is a vertex
            if type(v) is int:
                return const_names[v]
            # point is on a edge or in the center
            return const_names[edge(v[0], v[1])]
        # create a table line for codimX tables
        def create_codim_line(table, entry, new_elements):
            # change 3D simplex numbering scheme to 3D cube's one
            if self.lg.geometryType == (3,"simplex"):
                for i in range(len(new_elements)):
                    for j in range(len(new_elements[i])):
                        if type(new_elements[i][j]) is int:
                            if new_elements[i][j] == 3:
                                new_elements[i][j] = 4
                        else:
                            if new_elements[i][j][0] == 3:
                                new_elements[i][j] = (4, new_elements[i][j][1]) 
                            if new_elements[i][j][1] == 3:
                                new_elements[i][j] = (new_elements[i][j][0], 4)
            # write comment in front of data
            assert entry.base_case in self.lg.base_cases
            base_case_number = self.lg.base_cases.index(entry.base_case)
            table.append("      /* %s / %i / %s / %i */ " \
                % (entry.case, entry.permutation.orientation * base_case_number, \
                   ", ".join(map((str), map(len, new_elements))), \
                   table.offset), 0)
            if len(new_elements) > 0:
                # write all points of every element
                for element in new_elements:
                    table.append("%i, " % len(element), 1)
                    table.append("%s, " % ", ".join(map(get_point_name, element)), \
                                 len(element))
            else:
                table.append(" /* no elements */", 0)
            table.append("\n", 0)
        # creates string tables out of case tables
        def create_tables(self, offsets, codim0, codim1):
            for entry in self.lg.all_cases:
                # Constant whether unique MC33 case and whether inverted
                unique_case = CASE_UNIQUE_MC33
                if entry.permutation.orientation == -1:
                    unique_case += CASE_FLIPPED
                if entry.base_case.tests != []:
                    unique_case += CASE_AMIGUOUS_MC33
                # write offsets to offsets table
                assert entry.base_case in self.lg.base_cases
                base_case_number = self.lg.base_cases.index(entry.base_case)
                offsets.append("      /* %s / %i */ " \
                    % (entry.case, entry.permutation.orientation * base_case_number)
                    + "{%i, %i, %i, %i, %i},\n" \
                    % (codim0.offset, len(entry.cells), \
                       codim1.offset, len(entry.faces), unique_case), 1)
                create_codim_line(codim0, entry, entry.cells)
                create_codim_line(codim1, entry, entry.faces)
        # creates mc33 caste table and mc33 test table and returns 
        def create_mc33_tables(self, offsets, codim0, codim1, mc33_offsets, mc33_tests):
            offsets.append("      /* MC 33 cases follow */\n", 0)
            for entry in self.lg.all_cases:
                # above code should be obsolete
                assert len(entry.base_case.tests) == len(entry.tests)
                if entry.tests != []:
                    mc33_offsets.append("    /* %s / %i */ " \
                        % (entry.case, mc33_offsets.offset), 0)
                    mc33_offsets.append("%i,\n" \
                        % (mc33_tests.offset), 1)
                    # Generate tests table
                    mc33_tests.append("\n      /* %i / %s */" \
                        % (mc33_tests.offset, entry.case), 0)
                    i = 0
                    for test in entry.tests:
                        i = i + 1
                        if math.log(i)/math.log(2.0) == round(math.log(i)/math.log(2.0)):
                            mc33_tests.append("\n      ", 0)
                        if type(test) is int:
                            mc33_tests.append(str(offsets.offset + test) + ", ", 1)
                        else:
                            mc33_tests.append(repr(test) + ", ", 1)
                    # Case tables for mc 33 cases
                    for mc33_case in entry.mc33:
                        base_case_number = self.lg.base_cases.index(entry.base_case)
                        offsets.append("      /* %d test index:%d */ " \
                            % (base_case_number, i)
                            +"{%i, %i, %i, %i, 0},\n" \
                            % (codim0.offset, len(mc33_case.cells), \
                               codim1.offset, len(mc33_case.faces)), 1)
                        create_codim_line(codim0, entry, mc33_case.cells)
                        create_codim_line(codim1, entry, mc33_case.faces)
                else:
                    mc33_offsets.append("    /* %s / %i */ " \
                        % (entry.case, mc33_offsets.offset), 0)
                    mc33_offsets.append("255,\n", 1)
            mc33_tests.append("\n", 0)
        
        # Start output with table definitions
        table_offsets = TableStorage()
        table_offsets.tablestring = "    " \
            "const short table_%(T)s%(D)id_cases_offsets[][5] = {\n" \
            % { "D" : self.lg.dim, "T" : self.lg.basicType } \
            + "     /* vv: vertex values with 0=in, 1=out\n" \
            "      * cn: case number\n" \
            "      * bc: basic case, if negative it's inverted\n" \
            "      * c1: element count of co-dimension 1 elements\n" \
            "      * o1: table offset for co-dimension 1\n" \
            "      * c0: element count of co-dimension 0 elements\n" \
            "      * o0: table offset for co-dimension 0\n" \
            "      * uniq: whether the case is ambiguous for MC33 */\n" \
            "      /* vv / cn / bc / c0, o0, c1, o1, uniq */\n"
        table_codim0 = TableStorage()
        table_codim0.tablestring = "    " \
            "const short table_%(T)s%(D)id_codim_0[] = {\n" \
            % { "D" : self.lg.dim, "T" : self.lg.basicType } \
            + "     /* cn: case number\n" \
            "      * bc: basic case, if negative it's inverted\n" \
            "      * el: elements specified by number of vertices\n" \
            "      * cp: current position in array = offset */\n" \
            "      /* cn / bc / el / cp */\n"
        table_codim1 = TableStorage()
        table_codim1.tablestring = "    " \
            "const short table_%(T)s%(D)id_codim_1[] = {\n" \
            % { "D" : self.lg.dim, "T" : self.lg.basicType } \
            + "     /* cn: case number\n" \
            "      * bc: basic case, if negative it's inverted\n" \
            "      * el: elements specified by number of vertices\n" \
            "      * cp: current position in array = offset */\n" \
            "      /* cn / bc / el / cp */\n"
        # write elements into the array
        create_tables(self, table_offsets, table_codim0, table_codim1)
        
        # tables for mc 33
        if self.lg.basicType == "cube":
            table_mc33_offsets = TableStorage() #TODO: Typ der Tabelle von char auf int (?) aendern
            table_mc33_offsets.tablestring = "    " \
                "const short table_%(T)s%(D)id_mc33_offsets[] = {\n" \
                % { "D" : self.lg.dim, "T" : self.lg.basicType }
            table_mc33_tests = TableStorage()
            table_mc33_tests.tablestring = "    " \
                "const short table_%(T)s%(D)id_mc33_face_test_order[] = {\n" \
                % { "D" : self.lg.dim, "T" : self.lg.basicType } \
                + "      /* dummy entry/not used but the index has to start with 1*/\n" \
                + "      1,\n"
            create_mc33_tables(self, table_offsets, table_codim0, table_codim1, \
                               table_mc33_offsets, table_mc33_tests)
        # close the arrays and write them
        table_offsets.append("    };\n\n\n", 0)
        table_codim0.append("    };\n\n\n", 0)
        table_codim1.append("    };\n\n\n", 0)
        file.write(table_offsets.tablestring)
        file.write(table_codim0.tablestring)
        file.write(table_codim1.tablestring)
        if self.lg.basicType == "cube":
            table_mc33_offsets.append("    };\n\n\n", 0)
            table_mc33_tests.append("    };\n\n\n", 0)
            file.write(table_mc33_offsets.tablestring)
            file.write(table_mc33_tests.tablestring)
