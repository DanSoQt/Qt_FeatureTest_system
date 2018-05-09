############################################
# Qt Featuretest System
# Developed by Paul Tvete 2017
# Adapted for Windows by Daniel Smith 2018
############################################

This script is designed to pull a specified branch of the Qt source code, seach for feature options,
and build all modules repeatedly testing each feature with the --no-feature-[featurename] configure switch.

Arguments: ####  platform, arch, and working Directory are required.  ####
  --platform PLATFORM   The platform that will be running tests. For example:
                        'Ubuntu_16.04' or 'Windows_10'. If running in windows,
                        you MUST include the text'windows' somewhere in this
                        parameter value.

  --arch ARCH           The processor architecture that will be running tests.
                        Expected values are 'x86', 'x64', 'AArch_32',
                        'AArch_64'

  --workingDir WORKINGDIR
                        Specify the working directory for the testing. Ensure
                        that the user running tests has read/write access.
                        Example: /home/feature-test/ or C:\feature-test\

  --testRun TESTRUN     Setting this to True should run with a short test-set
                        of features to build

  --qtVersion QTVERSION
                        Specify a particular branch to test. Defaults to 'dev'
                        if not set. E.g. 5.9.0 or 5.11

  --logSuffix LOGSUFFIX
                        Specify a suffix or file extension for the log file.
                        Default is .log if not set

  --featureJSON FEATUREJSON
                        Specify the absoulte or relative path to a json file
                        containing a feature set to test. Default will scan
                        the qt installation for features.

  --buildCores BUILDCORES
                        Specify the number of CPU cores to use for building.
                        Defaults to 2 as a safe value.

  --vsDevCmd VSDEVCMD   Specify the location of the VsDevCmd.bat file for
                        setting up the build environment on Windows. This
                        parameter is not required on linux and assumes that
                        Visual Studio Build Tools (2017) is installed on 
						windows if left blank.

###############################
# Dependencies
###############################

Python3+: https://www.python.org/downloads/
	Python modules:
		argparse
		requests

Perl (windows): https://www.activestate.com/activeperl

Visual Studio Build Tools (Windows): http://landinghub.visualstudio.com/visual-cpp-build-tools
	On installation, check "Visual C++ Build Tools"
	It is possible to uncheck all optional features.
	Please keep the default install directory. Otherwise use the command line argument with test.py "--vsDevCmd" to
		specify the absolute path to VsDevCmd.bat (including the filename) from the VSC++ Build Tools installation.