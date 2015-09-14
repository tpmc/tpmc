def generate_lut(ext, build_dir):
        from os import path
        from distutils.dep_util import newer
        filename = path.join(build_dir, 'tpmc_lut.cc')
        if newer(__file__, filename):
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

#include <tpmc/marchinglut.hh>

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
        return filename

metadata = dict(
        description = 'python classes to generate TPMC lookup tables',
        author = 'Christian Engwer',
        author_email = 'christi@mathe-macht-spass.de',
        url = 'https://docs.python.org/extending/building',
        long_description = '''
        Implementation of the topology preserving marching cubes.
        ''',
        py_modules= ['tpmc.__version__',
                     'tpmc.lut',
                     'tpmc.lut.generate_lut',
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
        ]
)


constants = dict(
        header_dir = 'tpmc/include/tpmc', # this is relative to config.path_in_package
        lib_dir = 'tpmc/lib' # this is relative to install path
)


def configuration(parent_package='', top_path=None):
        from numpy.distutils.misc_util import Configuration
        from numpy.distutils.system_info import get_info

        config = Configuration('tpmc',parent_package,top_path)
        ## cmake files
        config.add_data_files('FindTpmc.cmake')
        ## header files
        config.add_data_files(constants['header_dir'] + '/*.hh')
        from os.path import join
        config.add_include_dirs(join('tpmc', 'include'))
        config.add_include_dirs(join('tpmc', 'lut'))
        ## libtpmc_tables
        config.add_installed_library('tpmc_tables',
                                     sources = ['tpmc/src/marchingcubestables.cc', generate_lut],
                                     install_dir = constants['lib_dir'])
        ## read version info from file
        config.get_version('tpmc/__version__.py')
        ## tpmc-config script
        config.add_scripts('tpmc-config')
        return config


def subst_config_file(source, target ,inputdict):
        # read tpmc-config script
        print "substituting configuration: %s -> %s" % (source, target)
        infile = open(source,'r')
        content = ""
        for line in infile:
                content = content + line
        for key, value in inputdict.iteritems():
                content = content.replace("@"+key+"@", value)
        outfile = open(target, 'w')
        print >> outfile, content


def substitute_setup_configuration (setup):
        install_scripts = None
        try:
                install_scripts = setup.command_obj['install_scripts']
                print "running install_scripts post-hook"
        except KeyError:
                pass
        if install_scripts != None:

                libdir = setup.command_obj['install_clib'].install_dir + "/" + constants['lib_dir']
                incdir = setup.command_obj['install_data'].install_dir + "/tpmc/" + constants['header_dir']
                for target in install_scripts.outfiles:
                        from os import path
                        (bindir, source) = path.split(target) # get file name and bin directory from the path object
                        substitutes = { 'incdir' : path.relpath(incdir,bindir) , 'libdir' : path.relpath(libdir,bindir) }
                        subst_config_file(source, target, substitutes)


if __name__ == '__main__':
        from numpy.distutils.core import setup as Setup
        metadata['configuration'] = configuration
        setup = Setup (**metadata)
        substitute_setup_configuration(setup)
        ### save the installation record for debugging
        # import sys
        # if len(sys.argv) >= 4 and sys.argv[2] == '--record':
        #         import shutil
        #         shutil.copy(sys.argv[3], '/tmp/log')
