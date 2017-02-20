import subprocess
import datetime
import re
import copy
import sys

from socket import gethostname
import requests
import time


my_output_dir = "/home/paul/dev/ex/git/feature-test/"
my_json_parser = "/home/paul/dev/ex/git/feature-test/jsontest/jsontest"

components_qtbase = [
    '-no-widgets',
    '-no-dbus',
    '-no-gui',
    '-no-accessibility',
    '-no-opengl',
    '-no-cups',
    '-no-fontconfig',
    '-no-freetype',
    '-no-harfbuzz',
    '-no-ssl',
    '-no-xkbcommon',
]



HOSTNAME="10.213.255.45"


timestamp_nano = time.time() * 1e9

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def submit_stats(moduleName, featureName, success, sha1):
    hostname = gethostname()

    measurement = 'build_test'
    status = 'success' if success else 'failure'
    result = 0 if success else 1;
    prettyFeatureName = remove_prefix(featureName, '-no-feature-')
    tags = ('platform=Ubuntu_16.04', 'module='+moduleName, 'status='+status, 'feature='+prettyFeatureName)
    fields = ('failure={:d}i'.format(result) , 'sha1="{}"'.format(sha1))

    data = '%s,%s %s %i' % (measurement, ','.join(tags), ','.join(fields), timestamp_nano)

    print(data)

    requests.post("http://10.213.255.45:8086/write?db=feature_system", data=data.encode('utf-8'))


try:
    log_suffix = '_'+sys.argv[1]
except IndexError:
    log_suffix = '_log'

repo_features = dict()

feature_run =  subprocess.run(["git", "submodule", "foreach", my_json_parser], stderr=subprocess.PIPE, universal_newlines=True)
exec(feature_run.stderr)

repo_features['qtbase'] += components_qtbase
repo_features['qtbase'].insert(0, '__baseline__')


print("Features:", repo_features)
print("------------------------------------------")

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
# Do the build tests
#
#-------------------------------------------------------------------



configuretemplate = [ "./configure", "-recheck-all", "-no-pch", "-release", "-developer-build", "-no-warnings-are-errors", "-nomake", "examples", "-nomake", "tests", "-opensource", "-confirm-license" ]

outfile = open(my_output_dir+'results'+log_suffix, 'a')
errfile = open(my_output_dir+'errors'+log_suffix, 'a')


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



def print_errors(log):
    print(log)
    for line in log.splitlines():
        if 'error:' in line or 'Project ERROR:' in line or line.startswith('make['):
            print('        ', line, file=errfile, flush=True)
    print('----------------------------------------------------------\n')


skip_list = []

#### testing
####skip_list = ["qtbase", "qtxmlpatterns"]


# start out clean
print("cleaning all")
subprocess.run(["git", "submodule", "foreach", "git", "clean", "-fdx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# test all features connected to each repo

for current_repo in sorted_repos:
    print('hello', current_repo)
    if not current_repo in repo_features:
        continue


    if current_repo in skip_list:
        continue

    repos_to_test = rrdeps[current_repo]

    for test_feature in repo_features[current_repo]:
        clean_repos(repos_to_test)
        r_to_test = repos_to_test.copy()

        configure_qt(test_feature)
        for r in sorted_repos:
            if r in r_to_test:
                print(timestamp(), "Building", r, "with", test_feature, file=outfile, flush=True)
                print("Building", r, "...")
                build_retc = subprocess.run(["make", "-s", "module-" + r],
                                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True)
                print(timestamp(), 'Build result',
                      build_retc.returncode, file=outfile, flush=True)
                success = build_retc.returncode == 0
                submit_stats(r, test_feature, success, repo_sha1s[r])
                if not success:
                    print(timestamp(), 'Build error', r, test_feature, "(from", current_repo, ")", file=errfile, flush=True)
                    r_to_test -= rrdeps[r]
                    print_errors(build_retc.stderr)




    #clean all rdeps before testing next repo
    clean_repos(repos_to_test)
