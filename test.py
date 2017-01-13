import subprocess
import datetime

repo_features = dict()

features_qml = (
    '-no-feature-qml-interpreter',
    '-no-feature-qml-network',
)
features_quick = (
    '-no-feature-d3d12',
    '-no-feature-quick-animatedimage',
    '-no-feature-quick-canvas',
    '-no-feature-quick-designer',
    '-no-feature-quick-flipable',
    '-no-feature-quick-gridview',
    '-no-feature-quick-listview',
    '-no-feature-quick-path',
    '-no-feature-quick-pathview',
    '-no-feature-quick-positioners',
    '-no-feature-quick-shadereffect',
    '-no-feature-quick-sprite',
)

repo_features['qtdeclarative'] = features_qml + features_quick

features_xmlpatterns = (
    '-no-feature-xml-schema',
)

repo_features['qtxmlpatterns'] = features_xmlpatterns

features_widgets = (
    '-no-feature-buttongroup',
    '-no-feature-calendarwidget',
    '-no-feature-colordialog',
    '-no-feature-columnview',
    '-no-feature-combobox',
    '-no-feature-completer',
    '-no-feature-contextmenu',
    '-no-feature-datawidgetmapper',
    '-no-feature-datetimeedit',
    '-no-feature-dial',
    '-no-feature-dirmodel',
    '-no-feature-dockwidget',
    '-no-feature-effects',
    '-no-feature-errormessage',
    '-no-feature-filedialog',
    '-no-feature-filesystemmodel',
    '-no-feature-fontcombobox',
    '-no-feature-fontdialog',
    '-no-feature-fscompleter',
    '-no-feature-graphicseffect',
    '-no-feature-graphicsview',
    '-no-feature-groupbox',
    '-no-feature-inputdialog',
    '-no-feature-itemviews',
    '-no-feature-keysequenceedit',
    '-no-feature-lcdnumber',
    '-no-feature-lineedit',
    '-no-feature-listview',
    '-no-feature-listwidget',
    '-no-feature-mainwindow',
    '-no-feature-mdiarea',
    '-no-feature-menu',
    '-no-feature-menubar',
    '-no-feature-messagebox',
    '-no-feature-paint_debug',
    '-no-feature-progressbar',
    '-no-feature-progressdialog',
    '-no-feature-resizehandler',
    '-no-feature-rubberband',
    '-no-feature-scrollarea',
    '-no-feature-scrollbar',
    '-no-feature-sizegrip',
    '-no-feature-slider',
    '-no-feature-spinbox',
    '-no-feature-splashscreen',
    '-no-feature-splitter',
    '-no-feature-stackedwidget',
    '-no-feature-statusbar',
    '-no-feature-statustip',
    '-no-feature-style-stylesheet',
    '-no-feature-syntaxhighlighter',
    '-no-feature-tabbar',
    '-no-feature-tableview',
    '-no-feature-tablewidget',
    '-no-feature-tabwidget',
    '-no-feature-textbrowser',
    '-no-feature-textedit',
    '-no-feature-toolbar',
    '-no-feature-toolbox',
    '-no-feature-toolbutton',
    '-no-feature-tooltip',
    '-no-feature-treeview',
    '-no-feature-treewidget',
    '-no-feature-undocommand',
    '-no-feature-undogroup',
    '-no-feature-undostack',
    '-no-feature-undoview',
    '-no-feature-whatsthis',
    '-no-feature-wizard',
)
features_network = (
    '-no-feature-bearermanagement',
    '-no-feature-ftp',
    '-no-feature-http',
    '-no-feature-localserver',
    '-no-feature-networkdiskcache',
    '-no-feature-networkinterface',
    '-no-feature-networkproxy',
    '-no-feature-socks5',
    '-no-feature-udpsocket',
)
features_printsupport = (
    '-no-feature-cups',
    '-no-feature-printdialog',
    '-no-feature-printer',
    '-no-feature-printpreviewdialog',
    '-no-feature-printpreviewwidget',
)
features_core = (
    '-no-feature-animation',
    '-no-feature-big_codecs',
    '-no-feature-codecs',
    '-no-feature-commandlineparser',
    '-no-feature-datestring',
    '-no-feature-filesystemiterator',
    '-no-feature-filesystemwatcher',
    '-no-feature-gestures',
    '-no-feature-iconv',
    '-no-feature-identityproxymodel',
    '-no-feature-itemmodel',
    '-no-feature-library',
    '-no-feature-mimetype',
    '-no-feature-process',
    '-no-feature-properties',
    '-no-feature-proxymodel',
    '-no-feature-regularexpression',
    '-no-feature-settings',
    '-no-feature-sha3-fast',
    '-no-feature-sharedmemory',
    '-no-feature-sortfilterproxymodel',
    '-no-feature-statemachine',
    '-no-feature-stringlistmodel',
    '-no-feature-systemsemaphore',
    '-no-feature-temporaryfile',
    '-no-feature-textcodec',
    '-no-feature-textdate',
    '-no-feature-timezone',
    '-no-feature-topleveldomain',
    '-no-feature-translation',
    '-no-feature-xmlstream',
    '-no-feature-xmlstreamreader',
    '-no-feature-xmlstreamwriter',
)
features_gui = (
    '-no-feature-accessibility',
    '-no-feature-action',
    '-no-feature-clipboard',
    '-no-feature-colornames',
    '-no-feature-cssparser',
    '-no-feature-cursor',
    '-no-feature-desktopservices',
    '-no-feature-draganddrop',
    '-no-feature-freetype',
    '-no-feature-highdpiscaling',
    '-no-feature-im',
    '-no-feature-image_heuristic_mask',
    '-no-feature-image_text',
    '-no-feature-imageformat_bmp',
    '-no-feature-imageformat_jpeg',
    '-no-feature-imageformat_png',
    '-no-feature-imageformat_ppm',
    '-no-feature-imageformat_xbm',
    '-no-feature-imageformat_xpm',
    '-no-feature-imageformatplugin',
    '-no-feature-movie',
    '-no-feature-pdf',
    '-no-feature-picture',
    '-no-feature-sessionmanager',
    '-no-feature-shortcut',
    '-no-feature-standarditemmodel',
    '-no-feature-systemtrayicon',
    '-no-feature-tabletevent',
    '-no-feature-texthtmlparser',
    '-no-feature-textodfwriter',
    '-no-feature-validator',
    '-no-feature-wheelevent',
)
features_xml = (
    '-no-feature-dom',
)

components_qtbase = (
    '__baseline__',
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
    '-no-xkbcommon'
)

repo_features['qtbase'] = components_qtbase

repo_features['qtbase'] += features_network + features_printsupport + features_core + features_gui + features_xml

### repo_features['qtbase'] += features_widgets


repos = [
    'qtbase',
    'qtxmlpatterns',
    'qtdeclarative',
    'qtquickcontrols',
    'qt3d',
    'qtactiveqt',
    'qtandroidextras',
    'qtwayland',
    'qtcanvas3d',
    'qtcharts',
    'qtconnectivity',
    'qtdatavis3d',
#    'qtdoc',
    'qtgamepad',
    'qtgraphicaleffects',
    'qtimageformats',
    'qtlocation',
    'qtmacextras',
    'qtmultimedia',
####    'qtnetworkauth',
    'qtpurchasing',
#    'qtqa',
    'qtquickcontrols2',
#    'qtrepotools',
#    'qtscript',
    'qtscxml',
    'qtsensors',
    'qtserialbus',
    'qtserialport',
    'qtspeech',
    'qtsvg',
#    'qttools',
#    'qttranslations',
    'qtvirtualkeyboard',
#    'qtwebchannel',
#    'qtwebsockets',
#    'qtwebview',
    'qtwinextras',
    'qtx11extras',
]



deps = dict()
deps["qtdeclarative"] = ('qtxmlpatterns',)

deps["qtmultimedia"] = ('qtdeclarative',)
deps["qtlocation"] = ('qtdeclarative', 'qtquickcontrols', 'qtserialport',)
deps["qtsensors"] = ('qtdeclarative', 'qtsvg',)
####deps["qtsystems"] = ('qtdeclarative',)
####deps["qtfeedback"] = ('qtdeclarative', 'qtmultimedia',)
####deps["qtpim"] = ('qtdeclarative',)
deps["qtconnectivity"] = ('qtdeclarative', 'qtandroidextras',)
deps["qtwayland"] = ('qtdeclarative',)
deps["qt3d"] = ('qtdeclarative', 'qtimageformats', 'qtgamepad',)
deps["qtgraphicaleffects"] = ('qtdeclarative',)
deps["qtquickcontrols"] = ('qtdeclarative', 'qtgraphicaleffects',)
deps["qtserialbus"] = ('qtserialport',)
deps["qtwinextras"] = ('qtdeclarative', 'qtmultimedia',)
deps["qtcanvas3d"] = ('qtdeclarative',)
deps["qtquickcontrols2"] = ('qtgraphicaleffects',)
deps["qtpurchasing"] = ('qtandroidextras', 'qtdeclarative',)
deps["qtcharts"] = ('qtdeclarative', 'qtmultimedia',)
deps["qtdatavis3d"] = ('qtdeclarative', 'qtmultimedia',)
deps["qtvirtualkeyboard"] = ('qtdeclarative', 'qtsvg', 'qtmultimedia', 'qtquickcontrols',)
deps["qtgamepad"] = ('qtdeclarative',)
deps["qtscxml"] = ('qtdeclarative',)
deps["qtspeech"] = ('qtdeclarative', 'qtmultimedia',)
####deps["qtnetworkauth"] = ('qtwebview',)


def deps_recursive(repo):
    retval = set()
    if not repo in deps:
        return retval
    for r in deps[repo]:
        retval.add(r)
        retval |= deps_recursive(r)
    return retval
    

rrdeps = {x:{x} for x in repos}

#print("one", rrdeps)

for r in repos:
    dr = deps_recursive(r)
    #print("deps of", r, "=", dr)
    for rr in dr:
        rrdeps[rr].add(r)

#for key, value in deps.items():
#    for d in value:
#        print("dep", key, "is", d)
#        rdeps[d].append(key)
#
#
#rdeps['qtbase'] = repos.copy()
#rdeps['qtbase'].remove('qtbase')
#

rrdeps['qtbase'] = set(repos)

print(rrdeps)

configuretemplate = [ "./configure", "-recheck-all", "-no-pch", "-release", "-developer-build", "-no-warnings-are-errors", "-nomake", "examples", "-nomake", "tests", "-opensource", "-confirm-license" ]

outfile = open('results.txt', 'w')
errfile = open('errors.txt', 'w')


#./configure -recheck-all -no-pch -release -developer-build -no-warnings-are-errors -nomake examples -nomake tests -opensource -confirm-license -no-feature-wheelevent

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())


#def allrdeps(repo):
#    res = set(rdeps[repo])
#    for r in rdeps[repo]:
#        res |= allrdeps(r)
#    res.add(repo)
#    return res
#

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
        if ': error:' in line or 'Project ERROR:' in line or line.startswith('make['):
            print('        ', line, file=errfile, flush=True)
    print('----------------------------------------------------------\n')


skip_list = []

#### testing
####skip_list = ["qtbase", "qtxmlpatterns"]


# start out clean
print("cleaning all")
subprocess.run(["git", "submodule", "foreach", "git", "clean", "-fdx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# test all features connected to each repo

for current_repo in repos:
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
        for r in repos:
            if r in r_to_test:
                print(timestamp(), "Building", r, "with", test_feature, file=outfile, flush=True)
                print("Building", r, "...")
                build_retc = subprocess.run(["make", "-s", "module-" + r],
                                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True)
                print(timestamp(), 'Build result',
                      build_retc.returncode, file=outfile, flush=True)
                success = build_retc.returncode == 0
                if not success:
                    print(timestamp(), 'Build error', r, test_feature, "(from", current_repo, ")", file=errfile, flush=True)
                    r_to_test -= rrdeps[r]
                    print_errors(build_retc.stderr)




    #clean all rdeps before testing next repo
    clean_repos(repos_to_test)
