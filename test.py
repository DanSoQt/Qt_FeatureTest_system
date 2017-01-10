import subprocess
import datetime

features = [
#    "__baseline__",
    "no_such_feature",
    "concurrent",
    "buttongroup",
    "calendarwidget",
    "colordialog",
    "columnview",
    "combobox",
    "completer",
    "contextmenu",
    "datawidgetmapper",
    "datetimeedit",
    "dial",
    "dirmodel",
    "dockwidget",
    "effects",
    "errormessage",
    "filedialog",
    "filesystemmodel",
    "fontcombobox",
    "fontdialog",
    "fscompleter",
    "graphicseffect",
    "graphicsview",
    "groupbox",
    "inputdialog",
    "itemviews",
    "keysequenceedit",
    "lcdnumber",
    "lineedit",
    "listview",
    "listwidget",
    "mainwindow",
    "mdiarea",
    "menu",
    "menubar",
    "messagebox",
    "paint_debug",
    "progressbar",
    "progressdialog",
    "resizehandler",
    "rubberband",
    "scrollarea",
    "scrollbar",
    "sizegrip",
    "slider",
    "spinbox",
    "splashscreen",
    "splitter",
    "stackedwidget",
    "statusbar",
    "statustip",
    "style-stylesheet",
    "syntaxhighlighter",
    "tabbar",
    "tableview",
    "tablewidget",
    "tabwidget",
    "textbrowser",
    "textedit",
    "toolbar",
    "toolbox",
    "toolbutton",
    "tooltip",
    "treeview",
    "treewidget",
    "undocommand",
    "undogroup",
    "undostack",
    "undoview",
    "whatsthis",
    "wizard",
    "bearermanagement",
    "ftp",
    "http",
    "localserver",
    "networkdiskcache",
    "networkinterface",
    "networkproxy",
    "socks5",
    "udpsocket",
    "cups",
    "printdialog",
    "printer",
    "printpreviewdialog",
    "printpreviewwidget",
    "animation",
    "big_codecs",
    "codecs",
    "commandlineparser",
    "datestring",
    "filesystemiterator",
    "filesystemwatcher",
    "gestures",
    "iconv",
    "identityproxymodel",
    "itemmodel",
    "library",
    "mimetype",
    "process",
    "properties",
    "proxymodel",
    "regularexpression",
    "settings",
    "sha3-fast",
    "sharedmemory",
    "sortfilterproxymodel",
    "statemachine",
    "stringlistmodel",
    "systemsemaphore",
    "temporaryfile",
    "textcodec",
    "textdate",
    "timezone",
    "topleveldomain",
    "translation",
    "xmlstream",
    "xmlstreamreader",
    "xmlstreamwriter",
    "accessibility",
    "action",
    "clipboard",
    "colornames",
    "cssparser",
    "cursor",
    "desktopservices",
    "draganddrop",
    "freetype",
    "highdpiscaling",
    "im",
    "image_heuristic_mask",
    "image_text",
    "imageformat_bmp",
    "imageformat_jpeg",
    "imageformat_png",
    "imageformat_ppm",
    "imageformat_xbm",
    "imageformat_xpm",
    "imageformatplugin",
    "movie",
    "pdf",
    "picture",
    "sessionmanager",
    "shortcut",
    "standarditemmodel",
    "systemtrayicon",
    "tabletevent",
    "texthtmlparser",
    "textodfwriter",
    "validator",
    "wheelevent",
    "dom"
]

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
    'qtdoc',
    'qtgamepad',
    'qtgraphicaleffects',
    'qtimageformats',
    'qtlocation',
    'qtmacextras',
    'qtmultimedia',
    'qtnetworkauth',
    'qtpurchasing',
    'qtqa',
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


#./configure -recheck-all -no-pch -release -developer-build -no-warnings-are-errors -nomake examples -nomake tests -opensource -confirm-license -no-feature-wheelevent


def timestamp():
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())



configuretemplate = [ "./configure", "-recheck-all", "-no-pch", "-release", "-developer-build", "-no-warnings-are-errors", "-nomake", "examples", "-nomake", "tests", "-opensource", "-confirm-license" ]

outfile = open('results.txt', 'w')
errfile = open('errors.txt', 'w')


for f in features:
    print("cleaning")
    subprocess.run(["git", "submodule", "foreach", "git", "clean", "-fdx"])
    print(timestamp(), "Configuring", f, file=outfile, flush=True)
    configurecmd = configuretemplate.copy()
    if f != '__baseline__':
        configurecmd.append("-no-feature-"+f)
        
    print("configuring", f)
    conf_retc = subprocess.run(configurecmd, check=False)
    print(timestamp(), 'Configure result', conf_retc.returncode,  file=outfile, flush=True)
    if conf_retc.returncode != 0:
        print("Configure error:", f, file=errfile, flush=True)
        continue
    for r in repos:
        print(timestamp(), "Building",
              r, "without feature", f, file=outfile, flush=True)
        build_retc = subprocess.run(["make", "-s", "module-" + r])
        print(timestamp(), 'Build result',
              build_retc.returncode, file=outfile, flush=True)
        if build_retc.returncode != 0:
            print(timestamp(), 'Build error',
                  r, f, file=errfile, flush=True)
            if r == 'qtbase':
                break
            





##result = subprocess.run(["ls", "-l", "."], stdout=subprocess.PIPE)
