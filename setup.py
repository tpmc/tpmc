from numpy.distutils.core import setup

def generate_lut(filename):
        from tpmc.lut.lutgen.dunecode import DuneCode
        print "importing lookup generators"
        from tpmc.lut.lutgen.base_case_triangulation import LookupGenerators
        ## geometries of LookupGenerators
        geometries = [(0,"any"),
                      (1,"any"),
                      (2,"simplex"), (2,"cube"),
                      (3,"simplex"), (3,"prism"), (3,"pyramid"), (3,"cube")]
        ## Output C code
        ccfile = open(filename, "w")
        ccfile.write("""
    /*
     * This file is autogenerated using generate_lut.py
     *
     * Don't edit this file!
     */

#include "marchinglut.hh"

extern \"C\" {

""")
        for g in geometries:
                print "generating table for %id %s" % g
                generator = LookupGenerators[g]['standard']
                generator.generate()
                print "writing code for %id %s" % g
                DuneCode(generator).write(ccfile)
        g = (3,'cube')
        print "generating symmetric table for %id %s" % g
        generator = LookupGenerators[g]['symmetric']
        generator.generate()
        print "writing symmetric code for %id %s" % g
        DuneCode(generator, 'sym').write(ccfile)
        ccfile.write("}\n")
        ccfile.close()

def configuration(parent_package='', top_path=None):
        import numpy
        from numpy.distutils.misc_util import Configuration
        config = Configuration('tpmc',parent_package,top_path)
        config.header_dir = 'include/tpmc' # this is relative to config.path_in_package
        config.lib_dir = 'tpmc/lib' # this is relative to install path
        ## header files
        # config.add_include_dirs(['tpmc/include/tpmc/*.hh', 'tpmc/lut/*.hh'])
        config.add_data_files((config.header_dir, 'tpmc/include/tpmc/*.hh'))
        config.add_data_files((config.header_dir, 'tpmc/lut/*.hh'))
        #config.add_headers('tpmc/include/tpmc/*.hh'])
        #config.add_headers('tpmc/lut/*.hh')
        ## libmarchinglut
        lutfile = 'build/tpmc_lut.cc'
        generate_lut(lutfile)
        config.add_installed_library('tpmc_lut',
                                     sources = [lutfile],
                                     install_dir = config.lib_dir,
                                     build_info = {
                                             'include_dirs' : [ 'tpmc/lut' ]
                                     })
        # config.add_installed_library(..., install_dir='../..') to install in /usr/local/lib
        return config

setup (
       version = '1.0',
       description = 'python classes to generate TPMC lookup tables',
       author = 'Christian Engwer',
       author_email = 'christi@mathe-macht-spass.de',
       url = 'https://docs.python.org/extending/building',
       long_description = '''
       Implementation of the topology preserving marching cubes.
       ''',
       py_modules= ['tpmc', 'tpmc.lut', 'tpmc.lut.lutgen',
                    'tpmc.lut.lutgen.base_case_triangulation',
                    'tpmc.lut.lutgen.cases',
                    'tpmc.lut.lutgen.consistencycheck',
                    'tpmc.lut.lutgen.coordinates',
                    'tpmc.lut.lutgen.disambiguate',
                    'tpmc.lut.lutgen.dunecode',
                    'tpmc.lut.lutgen.generator',
                    'tpmc.lut.lutgen.geomobj',
                    'tpmc.lut.lutgen.output',
                    'tpmc.lut.lutgen.permutation',
                    'tpmc.lut.lutgen.polygon',
                    'tpmc.lut.lutgen.referenceelements',
                    'tpmc.lut.lutgen.sk',
                    'tpmc.lut.lutgen.test',
                    'tpmc.lut.lutgen.transformation',
                    'tpmc.lut.lutgen.vtk'
            ],
       configuration=configuration
)
