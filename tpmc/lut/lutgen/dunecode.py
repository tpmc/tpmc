"""
Contains classes/constants for export to dune marchinglut.cc
"""

# file deepcode ignore DuplicateKey: The check triggers a false positive. We reate keys from other keys and the check accidentially thinks we are using the same key multiple times

import math
import operator
from .referenceelements import ReferenceElements
from .geomobj import FacePoint, CenterPoint, RootPoint

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
# faces
FA = VH + 1
FB = VH + 2
FC = VH + 3
FD = VH + 4
FE = VH + 5
FF = VH + 6
# center point
CA = FF + 1
CB = FF + 2
CC = FF + 3
CD = FF + 4
CE = FF + 5
CF = FF + 6
# root point
RA = CF + 1
RB = CF + 2
RC = CF + 3
RD = CF + 4
RE = CF + 5
RF = CF + 6
# dictionary to get constant names from integers
CONST_NAMES = {VA:"VA", VB:"VB", VC:"VC", VD:"VD", VE:"VE", 
               VF:"VF", VG:"VG", VH:"VH", FA:"FA", FB:"FB", 
               FC:"FC", FD:"FD", FE:"FE", FF:"FF", CA:"CA",
               CB:"CB", CC:"CC", CD:"CD", CE:"CE", CF:"CF",
               RA:"RA", RB:"RB", RC:"RC", RD:"RD", RE:"RE",
               RF:"RF"}
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

class VertexMapper:
    def __init__(self):
        self.table = TableStorage()
        self.vertices = dict()
        self.max_local_count = 0
    def id(self, vertex):
        if vertex in self.vertices:
            return self.vertices[vertex]
        else:
            if type(vertex) is tuple:
                id0 = self.id(vertex[0])
                id1 = self.id(vertex[1])
                offset = self.table.offset
                self.vertices[vertex] = offset
                self.table.append("      /* {2} / {3} */ {0}, {1}, \n".format(id0,
                                                                              id1,
                                                                              repr(vertex),
                                                                              offset),
                                  2)
                return offset
            else:
                faceids = [FA, FB, FC, FD, FE, FF]
                centerids = [CA, CB, CC, CD, CE, CF]
                rootids = [RA, RB, RC, RD, RE, RF]
                val = vertex
                if type(vertex) is CenterPoint:
                    val = centerids[vertex.id]
                elif type(vertex) is FacePoint:
                    val = faceids[vertex.id]
                elif type(vertex) is RootPoint:
                    val = rootids[vertex.id]
                return -val;

class LocalVertexMapper:
    def __init__(self, vmapper):
      self.vmapper = vmapper
      self.vertices = dict()
    def id(self, vertex):
      vid = self.vmapper.id(vertex)
      if vid <= -VA and vid >= -VH:
        return vid-1
      if not vid in self.vertices:
        self.vertices[vid] = len(self.vertices)
      return self.vertices[vid]


class DuneCode:
    """ Generates the tables, writes marchinglut.cc """
    def __init__(self, generator, suffix = ""):
        self.generator = generator
        self.suffix = suffix
        self.ref_elem = ReferenceElements[self.generator.geometry_type]
    def write(self, dune_file):
        """ Generate lookup table """
        def create_codim0_line(vmapper, table, table_groups, entry, new_elements, new_elements_groups):
            """ create a table line for codimX tables """
            # change 3D simplex, prism & pyramid numbering scheme to 3D cube's one
            def renameVertex(gt,v):
              rename_vertices = {(3,"simplex"): [0,1,2,4],
                                 (3,"prism"): [0,1,2,4,5,6]}
              if gt in rename_vertices:
                rn = rename_vertices[gt]
                if type(v) is int:
                  return rn[v]
                elif type(v) is tuple:
                  return (renameVertex(gt,v[0]),renameVertex(gt,v[1]))
              return v
            new_elements = [[renameVertex(self.generator.geometry_type,v) for v in t] for t in new_elements]
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
                    table.append("%s, " % ", ".join(str(vmapper.id(x)) 
                                                    for x in element),
                                 len(element))
                table_groups.append("%s, " % ", ".join(str(x) for x in new_elements_groups), len(new_elements_groups))
            else:
                table.append(" /* no elements */", 0)
                table_groups.append(" /* no elements */", 0)
            table.append("\n", 0)
            table_groups.append("\n", 0)
        def create_codim1_line(vmapper,table, entry, new_elements):
            """ create a table line for codimX tables """
            # change 3D simplex, prism & pyramid numbering scheme to 3D cube's one
            def renameVertex(gt,v):
              rename_vertices = {(3,"simplex"): [0,1,2,4],
                                 (3,"prism"): [0,1,2,4,5,6]}
              if gt in rename_vertices:
                rn = rename_vertices[gt]
                if type(v) is int:
                  return rn[v]
                elif type(v) is tuple:
                  return (renameVertex(gt,v[0]),renameVertex(gt,v[1]))
              return v
            new_elements = [[renameVertex(self.generator.geometry_type,v) for v in t] for t in new_elements]
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
                    table.append("%s, " % ", ".join(str(vmapper.id(x)) 
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
        def create_complex_vertices_line(lmapper, table):
            sorted_keys = [x[0] for x in sorted(list(lmapper.vertices.items()), key=operator.itemgetter(1))]
            table.append("      /* {} */ {}, {} \n".format(table.offset, len(sorted_keys), "{} ,".format(", ".join(str(x) for x in sorted_keys)) if len(sorted_keys) else ""),1+len(sorted_keys))
        def create_tables(self, vmapper, offsets, complex_vertices, vertex_groups, codim0_exterior, codim0_exterior_groups, codim0_interior, codim0_interior_groups, codim1):
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
                               "{{{2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}}},\n")
                offsets.append(oline.format(entry.case,
                                            (entry.transformation.orientation
                                             * base_case_number),
                                            codim0_exterior.offset, codim0_exterior_groups.offset, 
                                            len(entry.exterior),
                                            codim0_interior.offset, codim0_interior_groups.offset,
                                            len(entry.interior),
                                            codim1.offset, len(entry.faces),
                                            vertex_groups.offset,
                                            complex_vertices.offset,
                                            unique_case), 1)
                create_vertex_groups_line(entry, entry.vertex_groups, vertex_groups)
                lmapper = LocalVertexMapper(vmapper)
                create_codim0_line(lmapper, codim0_exterior, codim0_exterior_groups, entry, entry.exterior, entry.exterior_groups)
                create_codim0_line(lmapper, codim0_interior, codim0_interior_groups, entry, entry.interior, entry.interior_groups)
                create_codim1_line(lmapper, codim1, entry, entry.faces)
                create_complex_vertices_line(lmapper, complex_vertices);
                vmapper.max_local_count = max(vmapper.max_local_count, len(lmapper.vertices))
        def create_mc33_tables(self, vmapper, offsets, complex_vertices, vertex_groups, codim0_exterior, codim0_exterior_groups, codim0_interior, codim0_interior_groups, codim1, mc33_offsets, 
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
                                 "{{{2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, 0}},\n")
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
                                                    vertex_groups.offset,
                                                    complex_vertices.offset),
                                       1)
                        lmapper = LocalVertexMapper(vmapper)
                        create_vertex_groups_line(entry, mc33_case.vertex_groups, vertex_groups)
                        create_codim0_line(lmapper, codim0_exterior, codim0_exterior_groups, entry, mc33_case.exterior, mc33_case.exterior_groups)
                        create_codim0_line(lmapper, codim0_interior, codim0_interior_groups, entry, mc33_case.interior, mc33_case.interior_groups)
                        create_codim1_line(lmapper, codim1, entry, mc33_case.faces)
                        create_complex_vertices_line(lmapper, complex_vertices)
                        vmapper.max_local_count = max(vmapper.max_local_count, len(lmapper.vertices))
                else:
                    mc33_offsets.append("    /* {0} / {1} */"
                                        " ".format(entry.case, 
                                                   mc33_offsets.offset), 0)
                    # ??? why 255?
                    mc33_offsets.append("255,\n", 1)
            mc33_tests.append("\n", 0)
        
        # Start output with table definitions
        table_dict = {"D": self.generator.dim, "T": self.generator.basic_type,
                      "S": self.suffix}
        vmapper = VertexMapper()
        vmapper.table.tablestring = \
            ("    "
             "const short table_{0[T]}{0[D]}d{0[S]}_vertices[] = {{"
             "\n    /* <=0: single vertex, >0 offset in table */\n"
             "      1, /* dummy entry so offset starts with 1 */\n".format(table_dict))
        vmapper.table.offset = 1;
        table_offsets = TableStorage()
        table_offsets.tablestring = \
            ("    "
             "const unsigned short table_{0[T]}{0[D]}d{0[S]}_cases_offsets[][11] = {{\n"
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
             "      * cv: table offset for complex vertices\n"
             "      * uniq: whether the case is ambiguous for MC33 */\n"
             "      /* vv / cn / bc / o0e, o0eg, c0e, o0i, o0ig, c0i, o1, c1, vg, cv, uniq */"
             "\n".format(table_dict))
        table_complex_vertices_used = TableStorage()
        table_complex_vertices_used.tablestring = \
            ("    "
             "const short table_{0[T]}{0[D]}d{0[S]}_complex_vertices[] = {{"
             "\n    /* offset in vertex table */\n".format(table_dict))
        table_vertex_groups = TableStorage()
        table_vertex_groups.tablestring = \
            ("    "
             "const short table_{0[T]}{0[D]}d{0[S]}_vertex_groups[] = {{\n"
             "     /* vv: vertex values with 0=in, 1=out\n"
             "      * bc: basic case, if negative it's invertex\n"
             "      * cp: current position\n"
             "      * vg: vertex_groups */\n"
             "      /* vv / bc / cp / vg */"
             "\n".format(table_dict))
        table_codim0_exterior = TableStorage()
        table_codim0_exterior.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d{0[S]}_codim_0_exterior[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * el: elements specified by number of vertices\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / el / cp */"
                  "\n".format(table_dict))
        table_codim0_exterior_groups = TableStorage()
        table_codim0_exterior_groups.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d{0[S]}_exterior_groups[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / cp */"
                  "\n".format(table_dict))
        table_codim0_interior = TableStorage()
        table_codim0_interior.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d{0[S]}_codim_0_interior[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * el: elements specified by number of vertices\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / el / cp */"
                  "\n".format(table_dict))
        table_codim0_interior_groups = TableStorage()
        table_codim0_interior_groups.tablestring = \
                 ("    "
                  "const short table_{0[T]}{0[D]}d{0[S]}_interior_groups[] = {{\n" 
                  "     /* cn: case number\n"
                  "      * bc: basic case, if negative it's inverted\n"
                  "      * cp: current position in array = offset */\n"
                  "      /* cn / bc / cp */"
                  "\n".format(table_dict))
        table_codim1 = TableStorage()
        table_codim1.tablestring = \
            ("    "
             "const short table_{0[T]}{0[D]}d{0[S]}_codim_1[] = {{\n"
             "     /* cn: case number\n"
             "      * bc: basic case, if negative it's inverted\n"
             "      * el: elements specified by number of vertices\n"
             "      * cp: current position in array = offset */\n"
             "      /* cn / bc / el / cp */"
             "\n".format(table_dict))
        # write elements into the array
        create_tables(self, vmapper, table_offsets, table_complex_vertices_used, table_vertex_groups, table_codim0_exterior, table_codim0_exterior_groups ,
                      table_codim0_interior, table_codim0_interior_groups, table_codim1)
        
        # tables for mc 33
        generate_mc33 = set(["cube", "prism", "pyramid"])
        if self.generator.basic_type in generate_mc33:
            table_mc33_offsets = TableStorage() 
            # TODO: Typ der Tabelle von char auf int (?) aendern
            table_mc33_offsets.tablestring = \
                ("    "
                "const short table_{0[T]}{0[D]}d{0[S]}_mc33_offsets[] = {{"
                 "\n".format(table_dict))
            table_mc33_tests = TableStorage()
            table_mc33_tests.tablestring = \
                ("    "
                 "const short table_{0[T]}{0[D]}d{0[S]}_mc33_face_test_order[] "
                 "= {{\n"
                 "      /* dummy entry not used but the index has to "
                 "start with 1*/\n"
                 "      1,\n".format(table_dict))
            create_mc33_tables(self, vmapper, table_offsets, table_complex_vertices_used, table_vertex_groups, table_codim0_exterior, table_codim0_exterior_groups, 
                               table_codim0_interior, table_codim0_interior_groups, table_codim1, 
                               table_mc33_offsets, table_mc33_tests)
        # close the arrays and write them
        vmapper.table.append("    };\n\n\n", 0)
        table_offsets.append("    };\n\n\n", 0)
        table_complex_vertices_used.append("    };\n\n\n", 0)
        table_vertex_groups.append("    };\n\n\n", 0)
        table_codim0_exterior.append("    };\n\n\n", 0)
        table_codim0_exterior_groups.append("    };\n\n\n", 0)
        table_codim0_interior.append("    };\n\n\n", 0)
        table_codim0_interior_groups.append("    };\n\n\n", 0)
        table_codim1.append("    };\n\n\n", 0)
        complex_vertex_count_string = "const int table_{0[T]}{0[D]}d{0[S]}_max_complex_vertex_count = {1};\n".format(table_dict, vmapper.max_local_count);
        dune_file.write(complex_vertex_count_string);
        dune_file.write(vmapper.table.tablestring)
        dune_file.write(table_offsets.tablestring)
        dune_file.write(table_complex_vertices_used.tablestring)
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
