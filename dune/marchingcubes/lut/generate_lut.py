#!/usr/bin/env python
"""This script generates the lookup tables for the marching-cubes 33
algorithm """

import sys
import os
import time
import logging, argparse

sys.path.append(os.path.dirname(sys.argv[0]))

# parse command line arguments
parser = argparse.ArgumentParser('generate_lut')
parser.add_argument('--log', nargs = 1, dest = 'loglevel',
                    choices = ["DEBUG", "ERROR"],
                    help = "sets the log level")
parser.add_argument("--symmetric", help="generate symmetric versions of lookup tables",
                    action="store_true")
args = parser.parse_args(sys.argv[1:])

# initialize logging
if args.loglevel:
    loglevel = args.loglevel[0]
else:
    loglevel = "ERROR"

LOGGER = logging.getLogger('lutgen')
LOGGER.setLevel(loglevel)
ch = logging.StreamHandler()
ch.setLevel(loglevel)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                              ' - %(message)s' ,
                              '%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
LOGGER.addHandler(ch)

from lutgen.dunecode import DuneCode
from lutgen.vtk import Vtk
from lutgen.test import Test
from lutgen.base_case_triangulation import LookupGenerators

################################################################################
## LookupGenerators                                                           ##
################################################################################

cube3d = LookupGenerators[(3,"cube")]['standard']
cube3dsym = LookupGenerators[(3,"cube")]['symmetric']
pyramid3d = LookupGenerators[(3,"pyramid")]['standard']
prism3d = LookupGenerators[(3,"prism")]['standard']
prism3dsym = LookupGenerators[(3,"prism")]['symmetric']
simplex3d = LookupGenerators[(3,"simplex")]['standard']
cube2d = LookupGenerators[(2,"cube")]['standard']
simplex2d = LookupGenerators[(2,"simplex")]['standard']
lut1d = LookupGenerators[(1,"any")]['standard']
lut0d = LookupGenerators[(0,"any")]['standard']

################################################################################
## Tests                                                                      ##
################################################################################

# TODO commented tests until they are fixed

start = time.time()
Test(prism3d).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))
start = time.time()
Test(prism3dsym).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))
start = time.time()
Test(cube2d).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))
start = time.time()
Test(cube3dsym).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))
start = time.time()
Test(cube3d).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))
start = time.time()
Test(simplex2d).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))
start = time.time()
Test(simplex3d).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))
start = time.time()
Test(pyramid3d).test()
LOGGER.info("time elapsed: {0}s".format(time.time()-start))

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

DuneCode(lut0d).write(ccfile)
DuneCode(lut1d).write(ccfile)
DuneCode(simplex2d).write(ccfile)
DuneCode(cube2d).write(ccfile)
DuneCode(simplex3d).write(ccfile)
DuneCode(pyramid3d).write(ccfile)
DuneCode(prism3d).write(ccfile)
DuneCode(cube3d).write(ccfile)
DuneCode(cube3dsym, "sym").write(ccfile)

ccfile.write("}\n")
ccfile.close()

Vtk(prism3d).write("lutgen/vtk")
Vtk(pyramid3d).write("lutgen/vtk")
Vtk(cube3d).write("lutgen/vtk")
Vtk(cube2d).write("lutgen/vtk")
Vtk(simplex2d).write("lutgen/vtk")
Vtk(simplex3d).write("lutgen/vtk")
