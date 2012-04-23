"""
Contains classes/constants for export to dune marchinglut.cc
"""

import math
from referenceelements import ReferenceElements, CenterPoint

# Following constants are copied from marchinglut.hh
# constants for vertex and edge numbering
NO_VERTEX = 1 << 8
VERTEX_GO_RIGHT = 1 # x1 = 1
VERTEX_GO_DEPTH = 2 # x2 = 1
VERTEX_GO_UP = 4 # x3 = 1
FACTOR_FIRST_POINT = 1
FACTOR_SECOND_POINT = 16
# vertices start with V
VA = 0
VB = VERTEX_GO_RIGHT
VC = VERTEX_GO_DEPTH
VD = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH
VE = VERTEX_GO_UP
VF = VERTEX_GO_RIGHT + VERTEX_GO_UP
VG = VERTEX_GO_DEPTH + VERTEX_GO_UP
VH = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP
# center point
CP = 1 << 3
# edges start with E
EI = VA * FACTOR_FIRST_POINT + VB * FACTOR_SECOND_POINT + NO_VERTEX
EJ = VC * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX
EK = VA * FACTOR_FIRST_POINT + VC * FACTOR_SECOND_POINT + NO_VERTEX
EL = VB * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX
EM = VA * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX
EN = VB * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX
EO = VC * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX
EP = VD * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX
EQ = VE * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX
ER = VG * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX
ES = VE * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX
ET = VF * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX
# Diagonals for simplices
EU = VB * FACTOR_FIRST_POINT + VC * FACTOR_SECOND_POINT + NO_VERTEX
EV = VB * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX
EW = VC * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX
# Diagonal for pyramid
EX = VD * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX
# Diagonal for prism
EY = VF * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX
# connections from center to vertices
CA = VA * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
CB = VB * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
CC = VC * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
CD = VD * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
CE = VE * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
CF = VF * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
CG = VG * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
CH = VH * FACTOR_FIRST_POINT + CP * FACTOR_SECOND_POINT + NO_VERTEX
# dictionary to get constant names from integers
CONST_NAMES = {VA:"VA", VB:"VB", VC:"VC", VD:"VD", VE:"VE", 
               VF:"VF", VG:"VG", VH:"VH", EI:"EI", EJ:"EJ", EK:"EK", 
               EL:"EL", EM:"EM", EN:"EN", EO:"EO", EP:"EP", EQ:"EQ", 
               ER:"ER", ES:"ES", ET:"ET", EU:"EU", EV:"EV", EW:"EW", 
               EX:"EX", EY:"EY", CP:"CP", CA:"CA", CB:"CB", CC:"CC",
               CD:"CD", CE:"CE", CF:"CF", CG:"CG", CH:"CH"}
# Constants indicating whether case special treatment when 
# marching cubes' 33 is used.
CASE_UNIQUE_MC33 = 0
CASE_AMIGUOUS_MC33 = 1
# Constant indicates whether basic case was flipped.
CASE_FLIPPED = 4

class TableStorage:
    """ Stores a table as C-Code string for marchinglut.cc """
    def __init__(self):
        # String contatining C-Code for the table
        self.tablestring = ""
        # Integer indicating the number of entries, is used for 
        # indexing from other tables
        self.offset = 0
    def append(self, to_append, count):
        """ Adds some entries to the table """
        self.tablestring += to_append
        self.offset += count

class DuneCode:
    """ Generates the tables, writes marchinglut.cc """
    def __init__(self, generator):
        self.generator = generator
        self.ref_elem = ReferenceElements[self.generator.geometry_type]
    def write(self, dune_file):
        """ Generate lookup table """
        def edge(first, second):
            """ generate value for a point on a vertex or in the center """
            # ensure first < second
            if type(first)==CenterPoint:
                first = CP
            if type(second)==CenterPoint:
                second = CP
            if first > second:
                first, second = second, first
            # get center points
            if (first == VA and second == VH
                or first == VB and second == VG 
                or first == VC and second == VF 
                or first == VD and second == VE):
                return CP
            # points on an edge"
            try:
                # check whether edge exists, except 3D simplex, prism or 
                # pyramid because of changed numering
                if ((self.generator.basic_type != "simplex" 
                     and self.generator.basic_type != "prism"
                     and self.generator.basic_type != "pyramid")
                    and self.generator.dim != 3
                    and (first != CP and second != CP)):
                    self.ref_elem.edges.index(set([first, second]))
                return (first * FACTOR_FIRST_POINT 
                        + second * FACTOR_SECOND_POINT + NO_VERTEX)
            except ValueError:
                msg = "Edge ({0}, {1}) does not exist in {2}"
                raise ValueError, (msg.format(first, second, 
                                              self.generator.geometry_type))
        def get_point_name(vertex):
            """ 
            returns the constant name of the point as a string given by 
            its number 
            """
            # point is a vertex
            if type(vertex) is int:
                return CONST_NAMES[vertex]
            # point is on a edge or in the center
            #print vertex," in ",self.generator.geometry_type,": ",edge(vertex[0],vertex[1])
            return CONST_NAMES[edge(vertex[0], vertex[1])]
        def create_codim0_line(table, table_groups, entry, new_elements, new_elements_groups):
            """ create a table line for codimX tables """
            # change 3D simplex, prism & pyramid numbering scheme to 3D cube's one
            rename_vertices = {(3,"simplex"): [0,1,2,4],
                               (3,"prism"): [0,1,2,4,5,6]}
            if self.generator.geometry_type in rename_vertices:
                rename = rename_vertices[self.generator.geometry_type]
                for i in range(len(new_elements)):
                    for j in range(len(new_elements[i])):
                        if type(new_elements[i][j]) is int:
                            new_elements[i][j] = rename[new_elements[i][j]]
                        else:
                            new_elements[i][j] = (rename[new_elements[i][j][0]],
                                                  rename[new_elements[i][j][1]])
            # write comment in front of data
            assert entry.base_case in self.generator.base_cases
            base_case_number = self.generator.base_cases.index(entry.base_case)
            table_comment = "      /* {0} / {1} / {2} / {3} */ "
            table.append(table_comment.format(entry.case, 
                                              (entry.transformation.orientation
                                               * base_case_number),
                                              ", ".join(str(len(x))
                                                        for x in new_elements),
                                              table.offset), 0)
            table_groups_comment = "      /* {0} / {1} / {2} */ "
            table_groups.append(table_groups_comment.format(entry.case, (entry.transformation.orientation
                                                                  * base_case_number), table_groups.offset)
                                , 0)
            if len(new_elements) > 0:
                # write all points of every element
                #print "wrinting elements: ", new_elements
                for element in new_elements:
                    table.append("%i, " % len(element), 1)
                    table.append("%s, " % ", ".join(get_point_name(x) 
                                                    for x in element),
                                 len(element))
                table_groups.append("%s, " % ", ".join(str(x) for x in new_elements_groups), len(new_elements_groups))
            else:
                table.append(" /* no elements */", 0)
                table_groups.append(" /* no elements */", 0)
            table.append("\n", 0)
            table_groups.append("\n", 0)
        def create_codim1_line(table, entry, new_elements):
            """ create a table line for codimX tables """
            # change 3D simplex, prism & pyramid numbering scheme to 3D cube's one
            rename_vertices = {(3,"simplex"): [0,1,2,4],
                               (3,"prism"): [0,1,2,4,5,6],
                               (3,"pyramid"): [0,1,4,5,2]}
            if self.generator.geometry_type in rename_vertices:
                rename = rename_vertices[self.generator.geometry_type]
                for i in range(len(new_elements)):
                    for j in range(len(new_elements[i])):
                        if type(new_elements[i][j]) is int:
                            new_elements[i][j] = rename[new_elements[i][j]]
                        else:
                            new_elements[i][j] = (rename[new_elements[i][j][0]],
                                                  rename[new_elements[i][j][1]])
            # write comment in front of data
            assert entry.base_case in self.generator.base_cases
            base_case_number = self.generator.base_cases.index(entry.base_case)
            table_comment = "      /* {0} / {1} / {2} / {3} */ "
            table.append(table_comment.format(entry.case, 
                                              (entry.transformation.orientation
                                               * base_case_number),
                                              ", ".join(str(len(x))
                                                        for x in new_elements),
                                              table.offset), 0)
            if len(new_elements) > 0:
                # write all points of every element
                for element in new_elements:
                    table.append("%i, " % len(element), 1)
                    table.append("%s, " % ", ".join(get_point_name(x) 
                                                    for x in element),
                                 len(element))
            else:
                table.append(" /* no elements */", 0)
            table.append("\n", 0)
        def create_vertex_groups_line(entry, groups, table):
            base_case_number = \
                self.generator.base_cases.index(entry.base_case)
            table.append("      /* {0} / {1} / {2} */ {3}, \n".format(entry.case,
                                                              (entry.transformation.orientation
                                                               * base_case_number),
                                                              table.offset,
                                                              ", ".join(str(g) for g in groups)), len(groups));
        def create_tables(self, offsets, vertex_groups, codim0_exterior, codim0_exterior_groups, codim0_interior, codim0_interior_groups, codim1):
            """ creates string tables out of case tables """
            for entry in self.generator.all_cases:
                #print "AHHH writing entry ", entry
                # Constant whether unique MC33 case and whether inverted
                unique_case = CASE_UNIQUE_MC33
                if entry.transformation.orientation == -1:
                    unique_case += CASE_FLIPPED
                if entry.base_case.tests != []:
                    unique_case += CASE_AMIGUOUS_MC33
                # write offsets to offsets table
                assert entry.base_case in self.generator.base_cases
                base_case_number = \
                    self.generator.base_cases.index(entry.base_case)
                oline = ("      /* {0} / {1} */ "
                               "{{{2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}}},\n")
                offsets.append(oline.format(entry.case,
                                            (entry.transformation.orientation
                                             * base_case_number),
                                            codim0_exterior.offset, codim0_exterior_groups.offset, 
                                            len(entry.exterior),
                                            codim0_interior.offset, codim0_interior_groups.offset,
                                            len(entry.interior),
                                            codim1.offset, len(entry.faces),
                                            vertex_groups.offset,
                                            unique_case), 1)
                create_vertex_groups_line(entry, entry.vertex_groups, vertex_groups)
                create_codim0_line(codim0_exterior, codim0_exterior_groups, entry, entry.exterior, entry.exterior_groups)
                create_codim0_line(codim0_interior, codim0_interior_groups, entry, entry.interior, entry.interior_groups)
                create_codim1_line(codim1, entry, entry.faces)
        def create_mc33_tables(self, offsets, vertex_groups, codim0_exterior, codim0_exterior_groups, codim0_interior, codim0_interior_groups, codim1, mc33_offsets, 
                               mc33_tests):
            """ creates mc33 caste table and mc33 test table and returns  """
            offsets.append("      /* MC 33 cases follow */\n", 0)
            offsets.append("      {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, /* dummy entry for regular case */\n", 1)
            for entry in self.generator.all_cases:
                # above code should be obsolete
                assert len(entry.base_case.tests) == len(entry.tests)
                if entry.tests:
                    mc33_offsets.append("    /* {0} / {1} */ {2},"
                                        "\n".format(entry.case, 
                                                          mc33_offsets.offset,
                                                          mc33_tests.offset), 1)
                    # Generate tests table
                    mc33_tests.append("\n      /* {0} / {1} "
                                      "*/".format(mc33_tests.offset, entry.case)
                                      , 0)
                    for (i, test) in enumerate(entry.tests):
                        if math.log(i+1)/math.log(2.0) == round(math.log(i+1)
                                                              /math.log(2.0)):
                            mc33_tests.append("\n      ", 0)
                        if type(test) is int:
                            mc33_tests.append(str(offsets.offset + test) 
                                              + ", ", 1)
                        else:
                            mc33_tests.append(repr(test) + ", ", 1)
                    # Case tables for mc 33 cases
                    for mc33_case in entry.mc33:
                        #print "writing mc33 case: ", mc33_case
                        base_case_number = \
                            self.generator.base_cases.index(entry.base_case)
                        oline = ("      /* {0} test index:{1} */ "
                                 "{{{2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, 0}},\n")
                        offsets.append(oline.format(base_case_number,
                                                    len(entry.tests),
                                                    codim0_exterior.offset,
                                                    codim0_exterior_groups.offset,
                                                    len(mc33_case.exterior),
                                                    codim0_interior.offset,
                                                    codim0_interior_groups.offset,
                                                    len(mc33_case.interior),
                                                    codim1.offset,
                                                    len(mc33_case.faces),
                                                    vertex_groups.offset),
                                       1)
                        create_vertex_groups_line(entry, mc33_case.vertex_groups, vertex_groups)
                        create_codim0_line(codim0_exterior, codim0_exterior_groups, entry, mc33_case.exterior, mc33_case.exterior_groups)
                        create_codim0_line(codim0_interior, codim0_interior_groups, entry, mc33_case.interior, mc33_case.interior_groups)
                        create_codim1_line(codim1, entry, mc33_case.faces)
                else:
                    mc33_offsets.append("    /* {0} / {1} */"
                                        " ".format(entry.case, 
                                                   mc33_offsets.offset), 0)
                    # ??? why 255?
                    mc33_offsets.append("255,\n", 1)
            mc33_tests.append("\n", 0)
        
        # Start output with table definitions
        table_offsets = TableStorage()
        table_dict = {"D": self.generator.dim, "T": self.generator.basic_type}
        table_offsets.tablestring = \
            ("    "
             "const int table_{0[T]}{0[D]}d_cases_offsets[][10] = {{\n"
             "     /* vv: vertex values with 0=in, 1=out\n"
             "      * cn: case number\n"
             "      * bc: basic case, if negative it's inverted\n"
             "      * c1: element count of co-dimension 1 elements\n"
             "      * o1: table offset for co-dimension 1\n"
             "      * c0e: element count of co-dimension 0 exterior elements\n"
             "      * o0e: table offset for co-dimension 0 exterior\n"
             "      * c0i: element count of co-dimension 0 interior elements\n"
             "      * o0i: table offset for co-dimension 0 interior\n"
             "      * vg: table offset for vertex_groups\n"
             "      * uniq: whether the case is ambiguous for MC33 */\n"
             "      /* vv / cn / bc / o0e, o0eg, c0e, o0i, o0ig, c0i, o1, c1, vg, uniq */"
             "\n".format(table_dict))
        table_vertex_groups = TableStorage()
        table_vertex_groups.tablestring = \
            ("    "
             "const short table_{0[T]}{0[D]}d_vertex_groups[] = {{\n"
             "     /* vv: vertex values with 0=in, 1=out\n"
             "      * bc: basic case, if negative it's invertex\n"
             "      * cp: current position\n"
             "      * vg: vertex_groups */\n"
             "      /* vv / bc / cp / vg */"
             "\n".format(table_dict))
        table_codim0_exterior = TableStorage()
        table_codim0_exterior.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d_codim_0_exterior[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * el: elements specified by number of vertices\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / el / cp */"
                  "\n".format(table_dict))
        table_codim0_exterior_groups = TableStorage()
        table_codim0_exterior_groups.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d_exterior_groups[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / cp */"
                  "\n".format(table_dict))
        table_codim0_interior = TableStorage()
        table_codim0_interior.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d_codim_0_interior[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * el: elements specified by number of vertices\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / el / cp */"
                  "\n".format(table_dict))
        table_codim0_interior_groups = TableStorage()
        table_codim0_interior_groups.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d_interior_groups[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / cp */"
                  "\n".format(table_dict))
        table_codim1 = TableStorage()
        table_codim1.tablestring = \
            ("    "
             "const short table_{0[T]}{0[D]}d_codim_1[] = {{\n"
             "     /* cn: case number\n"
             "      * bc: basic case, if negative it's inverted\n"
             "      * el: elements specified by number of vertices\n"
             "      * cp: current position in array = offset */\n"
             "      /* cn / bc / el / cp */"
             "\n".format(table_dict))
        # write elements into the array
        create_tables(self, table_offsets, table_vertex_groups, table_codim0_exterior, table_codim0_exterior_groups ,
                      table_codim0_interior, table_codim0_interior_groups, table_codim1)
        
        # tables for mc 33
        generate_mc33 = set(["cube", "prism", "pyramid"])
        if self.generator.basic_type in generate_mc33:
            table_mc33_offsets = TableStorage() 
            # TODO: Typ der Tabelle von char auf int (?) aendern
            table_mc33_offsets.tablestring = \
                ("    "
                "const short table_{0[T]}{0[D]}d_mc33_offsets[] = {{"
                 "\n".format(table_dict))
            table_mc33_tests = TableStorage()
            table_mc33_tests.tablestring = \
                ("    "
                 "const short table_{0[T]}{0[D]}d_mc33_face_test_order[] "
                 "= {{\n"
                 "      /* dummy entry not used but the index has to "
                 "start with 1*/\n"
                 "      1,\n".format(table_dict))
            create_mc33_tables(self, table_offsets, table_vertex_groups, table_codim0_exterior, table_codim0_exterior_groups, 
                               table_codim0_interior, table_codim0_interior_groups, table_codim1, 
                               table_mc33_offsets, table_mc33_tests)
        # close the arrays and write them
        table_offsets.append("    };\n\n\n", 0)
        table_vertex_groups.append("    };\n\n\n", 0)
        table_codim0_exterior.append("    };\n\n\n", 0)
        table_codim0_exterior_groups.append("    };\n\n\n", 0)
        table_codim0_interior.append("    };\n\n\n", 0)
        table_codim0_interior_groups.append("    };\n\n\n", 0)
        table_codim1.append("    };\n\n\n", 0)
        dune_file.write(table_offsets.tablestring)
        dune_file.write(table_vertex_groups.tablestring)
        dune_file.write(table_codim0_exterior.tablestring)
        dune_file.write(table_codim0_exterior_groups.tablestring)
        dune_file.write(table_codim0_interior.tablestring)
        dune_file.write(table_codim0_interior_groups.tablestring)
        dune_file.write(table_codim1.tablestring)
        if self.generator.basic_type in generate_mc33:
            table_mc33_offsets.append("    };\n\n\n", 0)
            table_mc33_tests.append("    };\n\n\n", 0)
            dune_file.write(table_mc33_offsets.tablestring)
            dune_file.write(table_mc33_tests.tablestring)
