import subprocess
import datetime
import re
import copy

repo_features = dict()

feature_run =  subprocess.run(["git", "submodule", "foreach", "/jsontest/jsontest"], stderr=subprocess.PIPE, universal_newlines=True)



exec(feature_run.stderr)


print(features_widgets)


print(repo_features)
