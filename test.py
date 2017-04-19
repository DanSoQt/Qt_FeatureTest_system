import subprocess
import datetime
import re
import copy
import sys
import collections

import requests
import time
import os
import json


# --- Local modules

import htmlwriter


my_output_dir = "/home/paul/dev/ex/git/feature-test/"

components_qtbase = [
    '-no-widgets',
    '-no-dbus',
    '-no-gui',
    '-no-accessibility',
    '-no-opengl',
    '-no-cups',
    '-no-fontconfig',
####    '-no-freetype',
    '-no-harfbuzz',
    '-no-ssl',
    '-no-xkbcommon',
    '-no-xkbcommon-evdev',
]

connect_to_database = True

#HOSTNAME="10.213.255.45"


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
    tags = ('platform=Ubuntu_16.04', 'module='+moduleName, 'status='+status, 'feature='+prettyFeatureName)
    fields = ('failure={:d}i'.format(result) , 'sha1="{}"'.format(sha1))

    data = '%s,%s %s %i' % (measurement, ','.join(tags), ','.join(fields), timestamp_nano)

    print(data)

    requests.post("http://10.213.255.45:8086/write?db=feature_system", data=data.encode('utf-8'))
    pass




def submit_numstats(moduleName, failure_ratio, failure_count, sha1):
    if not connect_to_database:
        return
    measurement = 'build_stats'

    tags = ('platform=Ubuntu_16.04', 'module='+moduleName)
    fields = ('failurepercent={:f}'.format(failure_ratio*100) , 'failurecount={:d}'.format(failure_count), 'sha1="{}"'.format(sha1))

    ###timestamp_nano = timestamp_secs * 1e9

    data = '%s,%s %s %i' % (measurement, ','.join(tags), ','.join(fields), timestamp_nano)

    print(data)

    requests.post("http://10.213.255.45:8086/write?db=feature_system", data=data.encode('utf-8'))

try:
    log_suffix = '_'+sys.argv[1]
except IndexError:
    log_suffix = '_log'


#-------------------------------------------------------------------
#
# Repos and dependencies
#
#-------------------------------------------------------------------


repo_list = sys.argv[2:]

if not repo_list:
    repo_run = subprocess.run(["git", "submodule", "foreach", "-q", r"echo $path"], stdout=subprocess.PIPE, universal_newlines=True)

    repo_list = repo_run.stdout.splitlines();


print('Repositories:', repo_list)
print('-------------------------------------------')


repo_sha1s = {}

def get_sha1(repo):
    sha1_run =  subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
    repo_sha1s[repo] =  sha1_run.stdout.splitlines()[0]



for r in repo_list:
    get_sha1(r)

print(repo_sha1s)
print('-------------------------------------------')

tmp_repo_set = set(repo_list)
dependencies = dict()

def add_dependency(parent, child):
    if parent in tmp_repo_set and child in tmp_repo_set:
        dependencies.setdefault(parent, []).append(child)


current_sub = 'UNKNOWN'
#opt_deps = dict()
with open('.gitmodules') as f:
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

#print('-------------------------------------------')

#print(dependencies)
#print('-------------------------------------------')


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
    features = []
    if json_obj.get('module') and 'features' in json_obj:
        for feature, content in json_obj['features'].items():
            if 'purpose' in content:
                features.append('-no-feature-'+feature)
    return features


def getFeaturesFromRepo(repo):
    repo_features[repo] = []
    for root, dirs, files in os.walk(repo):
        for file in files:
            if file == 'configure.json':
                path = os.path.join(root, file)
                print('\n', path)
                with open(path) as json_data:
                    try:
                        d = json.load(json_data, strict = False)
                        repo_features[repo] += getFeaturesFromJson(d)
                    except json.decoder.JSONDecodeError as e:
                        print('****', path, e.lineno, "-----", e.msg)
                    except KeyError:
                        pass



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

configuretemplate = [ "./configure", "-recheck-all", "-no-pch", "-release", "-no-warnings-are-errors", "-nomake", "examples", "-nomake", "tests", "-nomake", "tools", "-opensource", "-confirm-license" ]

outfile = open(my_output_dir+'results'+log_suffix, 'a')
errfile = open(my_output_dir+'errors'+log_suffix, 'a')
warnfile = open(my_output_dir+'warnings'+log_suffix, 'a')

htmlfile = open(my_output_dir+'featuretest'+log_suffix+'.html', 'a')


#./configure -recheck-all -no-pch -release -developer-build -no-warnings-are-errors -nomake examples -nomake tests -opensource -confirm-license -no-feature-wheelevent

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

def clean_repos(repos_to_clean):
    for r in repos_to_clean:
        print("cleaning", r)
        subprocess.run(["git", "clean", "-fdx"], cwd=r, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def configure_qt(opt):
    print(timestamp(), "Configuring", opt, file=outfile, flush=True)
    configurecmd = configuretemplate.copy()
    if opt != '__baseline__':
        configurecmd.append(opt)

    print("configuring", opt)
    ### TODO: capture stderr
    conf_retc = subprocess.run(configurecmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(timestamp(), 'Configure result', conf_retc.returncode,  file=outfile, flush=True)
    if conf_retc.returncode != 0:
        print("Configure error:", opt, file=errfile, flush=True)
    return conf_retc.returncode == 0

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

databaseError = False

# start out clean
print("cleaning all")
subprocess.run(["git", "submodule", "foreach", "git", "clean", "-fdx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

        configure_qt(test_feature)
        for r in sorted_repos:
            if r in r_to_test and not r in baseline_errors:
                print(timestamp(), "Building", r, "with", test_feature, file=outfile, flush=True)
                print("Building", r, "...")
                build_retc = subprocess.run(["make", "-s", "module-" + r],
                                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True)
                print(timestamp(), 'Build result',
                      build_retc.returncode, file=outfile, flush=True)
                success = build_retc.returncode == 0
                total_build_count += 1
                if not success:
                    error_counts[r] += 1
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


htmlwriter.writeHtml(htmlfile)


# report build stats for each repo (no error handling since the script ends here anyway)

for repo in sorted_repos:
    errorCount = error_counts[repo]
    errorRatio = errorCount / total_build_count
    submit_numstats(repo, errorRatio, errorCount, repo_sha1s[repo])
