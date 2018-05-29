import subprocess
import datetime
import re
import copy
import sys
import collections
import platform
import time
import os
import json
import shutil
import argparse

# --- dependency modules --- make sure to install these on the local system.
import requests

# --- Local modules
import htmlwriter

#This application is not object oriented and does not use the __init__ method.




cmd_args = {}

def parseArguments():
    parser = argparse.ArgumentParser(description='Process platform, arch, and working Directory.')
    parser.add_argument('--platform', dest='platform', action='store', default='UNKNOWN', required=True, help='The platform that will be running tests. For example: \'Ubuntu_16.04\' or \'Windows_10\'. If running in windows, you MUST include the text\'windows\' somewhere in this parameter value.')
    parser.add_argument('--arch', dest='arch', action='store', default='x64', required=True, help='The processor architecture that will be running tests. Expected values are \'x86\', \'x64\', \'AArch_32\', \'AArch_64\'')
    parser.add_argument('--workingDir', dest='workingDir', action='store', default='', required=True, help='Specify the working directory for the testing. Ensure that the user running tests has read/write access. Example: /home/feature-test/ or C:\\feature-test\\')
    parser.add_argument('--testRun', dest='testRun', action='store', default=False, required=False, help='Setting this to True should run with a short test-set of features to build')
    parser.add_argument('--qtVersion', dest='qtVersion', action='store', default='dev', required=False, help='Specify a particular branch to test. Defaults to \'dev\' if not set.')
    #parser.add_argument('--logSuffix', dest='logSuffix', action='store', default='.log', required=False, help='Specify a suffix or file extension for the log file. Default is .log if not set')
    parser.add_argument('--featureJSON', dest='featureJSON', action='store', default='', required=False, help='Specify the absoulte or relative path to a json file containing a feature set to test. Default will scan the qt installation for features.')
    parser.add_argument('--buildCores', dest='buildCores', action='store', default='2', required=False, help='Specify the number of CPU cores to use for building. Defaults to 2 as a safe value.')
    parser.add_argument('--vsDevCmd', dest='vsDevCmd', action='store', default='C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\Common7\\Tools\\VsDevCmd.bat', required=False, help='Specify the location of the VsDevCmd.bat file for setting up the build environment on Windows.\nThis parameter is not required on linux and assumes that VS2017 is installed on windows if left blank.')

    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)
        exit
    
    cmd_args["platform"] = args.platform
    cmd_args["arch"] = args.arch
    cmd_args["workingDir"] = args.workingDir
    cmd_args["testRun"] = args.testRun
    cmd_args["qt_version"] = args.qtVersion
    #cmd_args["logSuffix"] = args.logSuffix
    cmd_args["featureJSON"] = args.featureJSON
    cmd_args["buildCores"] = args.buildCores
    cmd_args["vsDevCmd"] = args.vsDevCmd

parseArguments()
# Set the output dir for result files.
my_output_dir = cmd_args["workingDir"]

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

process_start_time = timestamp()

#shutil.rmtree(cmd_args["workingDir"] + cmd_args["qt_version"])

#If we're on Windows, set a flag and do some environment setup.
isWindows = False

if (cmd_args["platform"].lower().find('windows') > -1):
    isWindows = True
    #runs the vsDevCmd file from the visual studio installation
    vars = subprocess.check_output([cmd_args["vsDevCmd"], '&&', 'set'])

    # splits the output of the batch file and saves PATH variables from the batch to the local os.environ
    for var in vars.splitlines():
        var = var.decode('cp1252')
        k, _, v = map(str.strip, var.strip().partition('='))
        if k.startswith('?'):
            continue
        os.environ[k] = v

    os.environ["CL"]="/MP" #set multicore building
    os.environ["PATH"]+=cmd_args["workingDir"].replace("/", "\\") + cmd_args["qt_version"] + "\\" # add the qt version we're working on to the windows PATH.

# Checkout the branch and update it if it's already downloaded. Clone it and run init-repo on it if it's not available locally.
def setup_qt_workspace():
    if not os.path.exists(cmd_args["workingDir"]):
        os.makedirs(cmd_args["workingDir"])

    if os.path.exists(cmd_args["workingDir"] + cmd_args["qt_version"]):
        #assume we have a version cloned already!
        print(subprocess.run(["git", "checkout", cmd_args["qt_version"]], stdout=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"]).stdout)
        print(subprocess.run(["git", "fetch", "--recurse-submodules=yes", "-v"], stdout=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"]).stdout)
        print(subprocess.run(["git", "reset", "--hard", "origin/"+cmd_args["qt_version"]], stdout=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"]).stdout)
        #print(subprocess.run(["git", "submodule", "foreach", "git", "submodule", "update"], stdout=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"]).stdout)
        print(subprocess.run(["git", "clean", "-fdx"], stdout=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"]).stdout)
    else:
        attempts = 0
        returncode = -1
        while returncode !=0: # clone out the target branch to the working directory
            proc = subprocess.run(["git", "clone", "-b", cmd_args["qt_version"], "--single-branch", 'https://code.qt.io/cgit/qt/qt5.git', cmd_args["qt_version"]], stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"])
            print(proc.stdout, proc.stderr)
            returncode = proc.returncode
            attempts = attempts + 1
            if attempts > 14:
                attempts = 0
                if (returncode !=0):
                    raise Exception("Failed to clone the repository after 15 tries. Maybe there's something wrong with the endpoint or your network connection.")
                break
            if returncode!=0:
                print("There was an error while trying to clone the repo. Try " + str(attempts) + "/15 max.  Retrying.")
            
        print(subprocess.run(["git", "checkout", cmd_args["qt_version"]], stdout=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"]).stdout)
    
    attempts = 0
    returncode = -1
    proc = None
        
        #This step likes to fail while cloning large data from the repo. Try it up to 15 times. The init-repo script should pick up where it left off each time.
    while returncode != 0:
        print("running the init-repo step.")
        proc = subprocess.run(["perl", "init-repository", "-f"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"])
        print("Finished the step or errored out. Printing results next...")
        print(proc.stdout, proc.stderr)
        returncode = proc.returncode
        attempts = attempts + 1
        if attempts > 14:
            attempts = 0
            if (returncode !=0):
                raise Exception("Failed to initialize the branch repo. Maybe there's something wrong with the endpoint or your network connection. You can run the init-repository script yourself with perl /workingDirectory/qtVersion/init-repository -f")
        if returncode!=0: print("There was an error while trying to initialize the repo. Try " + str(attempts) + "/15 max. Retrying.")    



setup_qt_workspace()

components_qtbase = [
    '-no-widgets',
    '-no-dbus',
    '-no-gui',
    '-no-accessibility',
    '-no-opengl',
    '-no-cups',
    '-no-fontconfig',
    '-no-harfbuzz',
    '-no-ssl',
    '-no-xkbcommon',
    '-no-xkbcommon-evdev',
]

connect_to_database = True

timestamp_nano = time.time() * 1e9

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def submit_stats(moduleName, featureName, success, sha1):
    if not connect_to_database:
        return
    #hostname = gethostname()

    measurement = 'build_test'
    status = 'success' if success else 'failure'
    result = 0 if success else 1;
    prettyFeatureName = remove_prefix(featureName, '-no-feature-')
    tags = ('machineName=' + platform.node(), 'platform=' + cmd_args['platform'], 'arch=' + cmd_args['arch'], 'module='+moduleName, 'status='+status, 'feature='+prettyFeatureName)
    fields = ('failure={:d}i'.format(result) , 'sha1="{}"'.format(sha1))

    data = '%s,%s %s %i' % (measurement, ','.join(tags), ','.join(fields), timestamp_nano)

    print(data)

    requests.post("https://testresults.qt.io/influxdb/write?db=feature_system", auth=('feature_system_service', 'Yk2HxxKRm'), data=data.encode('utf-8'))

def submit_numstats(moduleName, failure_ratio, failure_count, sha1):
    if not connect_to_database:
        return
    measurement = 'build_stats'

    tags = ('platform=' + cmd_args["platform"], 'module=' + moduleName)
    fields = ('failurepercent={:f}'.format(failure_ratio*100) , 'failurecount={:d}'.format(failure_count), 'sha1="{}"'.format(sha1))

    ###timestamp_nano = timestamp_secs * 1e9

    data = '%s,%s %s %i' % (measurement, ','.join(tags), ','.join(fields), timestamp_nano)

    print(data)

    requests.post("https://testresults.qt.io/influxdb/write?db=feature_system", auth=('feature_system_service', 'Yk2HxxKRm'), data=data.encode('utf-8'))

log_suffix = "_" + process_start_time.replace(" ", "_").replace(":", ".")

#### Selftest logic ####

quick_test_run = True if (cmd_args["testRun"] == "True") else False
test_feature_dict = {}

if (cmd_args['featureJSON'] != ''):
    try:
        json_feature_arg = cmd_args['featureJSON']
        test_feature_dict = json.loads(json_feature_arg)
        repo_list = list(test_feature_dict.keys())
        print("Running full test from json...")
    except IndexError as e:
        # normal run: autodetect repos and features
        print("Exception when loading json features: ")
        repo_list = []
        pass

    else:
        # test run: use the specified repos and features
        print("Running as a quick test run...")
        quick_test_run = True
        components_qtbase = []

else:
    repo_list = []



#-------------------------------------------------------------------
#
# Repos and dependencies
#
#-------------------------------------------------------------------

if not repo_list:
    print("Getting the repo list.")
    repo_run = subprocess.run(["git", "submodule", "foreach", "-q", r"echo $path"], stdout=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"])
    repo_list = repo_run.stdout.splitlines()


print('Repositories:', repo_list)
print('-------------------------------------------')

repo_sha1s = {}

def get_sha1(repo):
    print("Directory is currently: " + repo)
    sha1_run =  subprocess.run(["git", "rev-parse", "HEAD"], cwd=cmd_args["workingDir"] + cmd_args["qt_version"] + "/"+ repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
    repo_sha1s[repo] =  sha1_run.stdout.splitlines()[0]



for r in repo_list:
    get_sha1(r)
    htmlwriter.registerRepo(r, repo_sha1s[r])

print(repo_sha1s)
print('-------------------------------------------')

tmp_repo_set = set(repo_list)
dependencies = dict()

def add_dependency(parent, child):
    if parent in tmp_repo_set and child in tmp_repo_set:
        dependencies.setdefault(parent, []).append(child)


current_sub = 'UNKNOWN'

with open(cmd_args["workingDir"] + cmd_args["qt_version"] + "/.gitmodules") as f:
    for line in f:
        match = re.search(r'^\[submodule "(.*)"\]', line)
        if match:
            # print('Submodule found: ', match.group(1))
            current_sub = match.group(1)
            continue
        match = re.search(r'depends = (.*)', line)
        if match:
            for dep in match.group(1).split(' '):
                add_dependency(current_sub, dep)
            continue
        match = re.search(r'recommends = (.*)', line)
        if match:
            for dep in match.group(1).split(' '):
                add_dependency(current_sub, dep)
            continue

def deps_recursive(repo):
    retval = set()
    if not repo in dependencies:
        return retval
    for r in dependencies[repo]:
        retval.add(r)
        retval |= deps_recursive(r)
    return retval


rrdeps = {x:{x} for x in repo_list}


for r in repo_list:
    dr = deps_recursive(r)
    #print("deps of", r, "=", dr)
    for rr in dr:
        if rr in rrdeps:
            rrdeps[rr].add(r)



print('Dependencies:')
for key in rrdeps:
    print('  ', key, ':', rrdeps[key])
print('-------------------------------------------')

repos_to_sort = copy.deepcopy(rrdeps)
sorted_repos = []

for repo in repos_to_sort:
    repos_to_sort[repo].discard(repo)


while repos_to_sort:
    rlist = list(repos_to_sort.keys())
    for repo in rlist:
        if not repos_to_sort[repo]:
            for r in repos_to_sort:
                repos_to_sort[r].discard(repo)
            del repos_to_sort[repo]
            sorted_repos.insert(0, repo)

print('Sort order:')
print('  ', sorted_repos)


#-------------------------------------------------------------------
#
# Features
#
#-------------------------------------------------------------------

repo_features = dict()


def getFeaturesFromJson(json_obj):
    print("trying to get features from json...")
    features = []
    if 'features' in json_obj:
        print ("found features...")
        for feature, content in json_obj['features'].items():
            if 'purpose' in content:
                features.append('-no-feature-'+feature)
                print("Adding -no-feature-" + feature + " to the list to test")
    print("\n")
    return features


def getFeaturesFromRepo(repo):
    print("\nAttempting to get features from repo: " + repo)
    repo_features[repo] = []
    configureFound = False
    #return #remove this to reenable full test.
    try:
        for root, dirs, files in os.walk(cmd_args["workingDir"] + cmd_args["qt_version"] + "/" + repo):
            for file in files:
                if file == 'configure.json':
                    configureFound = True
                    print("found configure.json. Trying to load it.")
                    path = os.path.join(root, file)
                    print(path)
                    with open(path) as json_data:
                        try:
                            d = json.load(json_data, strict = False)
                            repo_features[repo] += getFeaturesFromJson(d)
                            #print("loaded the json. Found features:\n" + getFeaturesFromJson(d))
                        except json.decoder.JSONDecodeError as e:
                            print('****', path, e.lineno, "-----", e.msg)
                        except KeyError:
                            pass

    except Exception as e:
        print("there was an error walking the dirs.\n")
        print(e)

    if (configureFound == False):
        print("Configure file not found for repo: " + repo)

if quick_test_run:
    repo_features = test_feature_dict
    repo_features['qtbase'] = []

else:
    for repo in sorted_repos:
        getFeaturesFromRepo(repo)

repo_features['qtbase'] += components_qtbase
repo_features['qtbase'].insert(0, '__baseline__')


print("Features:", repo_features)
print("------------------------------------------")

#-------------------------------------------------------------------
#
# Do the build tests
#
#-------------------------------------------------------------------


###### "-developer-build", does not play well with syncqt

if(isWindows):
    configuretemplate = [ "configure.bat", "-recheck-all", "-no-pch", "-release", "-no-warnings-are-errors", "-nomake", "examples", "-nomake", "tests", "-nomake", "tools", "-opensource", "-confirm-license"]
else:
    configuretemplate = [ "./configure", "-recheck-all", "-no-pch", "-release", "-no-warnings-are-errors", "-nomake", "examples", "-nomake", "tests", "-nomake", "tools", "-opensource", "-confirm-license" ]

outfile = open(my_output_dir+'results'+log_suffix+'.log', 'a')
errfile = open(my_output_dir+'errors'+log_suffix+'.log', 'a')
warnfile = open(my_output_dir+'warnings'+log_suffix+'.log', 'a')


def clean_repos(repos_to_clean):
    for r in repos_to_clean:
        print("cleaning", r)
        subprocess.run(["git", "clean", "-fdx"], cwd=cmd_args["workingDir"] + cmd_args["qt_version"] + "/" + r, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def configure_qt(opt, repo = ''):
    print(timestamp(), "Configuring", opt, file=outfile, flush=True)
    configurecmd = configuretemplate.copy()
    if opt != '__baseline__':
        configurecmd.append(opt)

    print("configuring", opt)
    print("trying to run:" + cmd_args["workingDir"] + cmd_args["qt_version"] + "/" + str(configurecmd))
    conf_retc = subprocess.run(configurecmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cmd_args["workingDir"] + cmd_args["qt_version"], shell=(True if isWindows else False))
    print(timestamp(), 'Configure result', conf_retc.returncode,  file=outfile, flush=True)
    print(timestamp(), 'Configure result: ', conf_retc.returncode)
    print(conf_retc.stdout, "\n\n", conf_retc.stderr)
    if conf_retc.returncode != 0:
        print("Configure error:", opt)
        print("Configure error:", opt, file=errfile, flush=True)
    return conf_retc.returncode == 0

#########################################################################################################################################################################
#------------------------------------------------- Make this platform independent since Make won't be used on Windows --------------------------------------------------#
#########################################################################################################################################################################

def report_errors(featurename, modulename, log):
    print(log)
    err_str = ''
    for line in log.splitlines():
        if 'error:' in line or 'Project ERROR:' in line or line.startswith('make['):
            if (err_str):
                err_str += '\n'
            err_str += line
            print('        ', line, file=errfile, flush=True)
    print('----------------------------------------------------------\n')
    htmlwriter.registerError(modulename, featurename, err_str)

baseline_warnings = {}

def report_warnings(featurename, modulename, log, baseline):
    warn_count = 0
    warnings_seen = set()
    warn_string = ''
    if not baseline:
        warnings_seen = baseline_warnings[modulename]

    for line in log.splitlines():
        if 'warning:' in line and not line in warnings_seen:
            if warn_string:
                warn_string += '\n'
            warn_string += line
            warn_count += 1
            warnings_seen.add(line)
            print('        ', line, file=warnfile)
    if warn_count > 0:
        print('Warnings for:', modulename, 'feature:', featurename, 'warning count:', warn_count, file=warnfile)
        print(warn_string, file=warnfile)
        print('----------\n', file=warnfile, flush=True)
        if not baseline:
            htmlwriter.registerWarning(modulename, featurename, warn_count, warn_string)
    if baseline:
        baseline_warnings[modulename] = warnings_seen

###skip_list = set()

#### testing
####skip_list = {"qtbase", "qtxmlpatterns"}

baseline_errors = set()

total_build_count = 0

error_counts = collections.defaultdict(int)
total_error_count = 0

databaseError = False

# start out clean
print("cleaning all")
subprocess.run(["git", "submodule", "foreach", " git", "clean", "-fdx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cmd_args["workingDir"] + cmd_args["qt_version"])

# test all features connected to each repo

for current_repo in sorted_repos:
    print('hello', current_repo)
    if not current_repo in repo_features:
        continue


##    if current_repo in skip_list:
##        continue

    repos_to_test = rrdeps[current_repo]

    for test_feature in repo_features[current_repo]:
        baseline_build = (test_feature == '__baseline__')
        clean_repos(repos_to_test)
        r_to_test = repos_to_test.copy()
        
        print("configuring the repo. ")
        configure_qt(test_feature, current_repo)
        for r in sorted_repos:
            print("Current Repo: " + r)
            if r in r_to_test and not r in baseline_errors:
                print("Repo was in the list to test. Attempting to build...")
                print(timestamp(), "Building", r, "with", test_feature, file=outfile, flush=True)
                print("Building", r, "...")
                if (isWindows):
                    build_retc = subprocess.run([os.getcwd() + "\\JOM\\jom.exe", "-j",  cmd_args["buildCores"], "module-" + r],
                                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"], shell=True)
                else:
                    build_retc = subprocess.run(["make", "-j",  cmd_args["buildCores"], "module-" + r],
                                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True, cwd=cmd_args["workingDir"] + cmd_args["qt_version"])
                print(timestamp(), 'Build result',
                      build_retc.returncode, file=outfile, flush=True)
                print(build_retc.check_returncode)
                success = build_retc.returncode == 0
                total_build_count += 1
                if not success:
                    error_counts[r] += 1
                    total_error_count += 1
                if not databaseError:
                    try:
                        submit_stats(r, test_feature, success, repo_sha1s[r])
                    except:
                        databaseError = True
                        print('Cannot connect to database')
                if not success:
                    print(timestamp(), 'Build error', r, test_feature, "(from", current_repo, ")", file=errfile, flush=True)
                    r_to_test -= rrdeps[r]
                    report_errors(test_feature, r, build_retc.stderr)
                else:
                    report_warnings(test_feature, r, build_retc.stderr, baseline_build)

                # if the baseline does not build, there's no point in testing features
                if baseline_build and not success:
                    baseline_errors.update(rrdeps[r])

    #clean all rdeps before testing next repo
    clean_repos(repos_to_test)

    
#------------------------
# End of test run
#------------------------



htmlwriter.registerStats(buildcount=total_build_count)

with open(my_output_dir+'featuretest'+log_suffix+'.html', 'w') as htmlfile:
    htmlwriter.writeHtml(htmlfile)


# report build stats for each repo (no error handling since the script ends here anyway)

for repo in sorted_repos:
    errorCount = error_counts[repo]
    errorRatio = errorCount / total_build_count
    submit_numstats(repo, errorRatio, errorCount, repo_sha1s[repo])
