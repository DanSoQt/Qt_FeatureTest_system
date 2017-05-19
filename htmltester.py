import subprocess
import datetime
import re
import copy
import sys
import collections

#from socket import gethostname
import requests
import time
import os
import json
import htmlwriter





feature_dict = {'qtwayland': [], 'qtmultimedia': [], 'qtimageformats': [], 'qtspeech': [], 'qtdeclarative': ['-no-feature-qml-network', '-no-feature-qml-interpreter', '-no-feature-qml-profiler', '-no-feature-quick-particles', '-no-feature-quick-shadereffect', '-no-feature-quick-sprite', '-no-feature-quick-designer', '-no-feature-quick-pathview', '-no-feature-quick-animatedimage', '-no-feature-quick-canvas', '-no-feature-quick-gridview', '-no-feature-quick-listview', '-no-feature-quick-positioners', '-no-feature-d3d12', '-no-feature-quick-path', '-no-feature-quick-flipable'], 'qtnetworkauth': [], 'qtpurchasing': [], 'qtgamepad': [], 'qtwebchannel': [], 'qtbase': ['__baseline__', '-no-feature-fscompleter', '-no-feature-filesystemmodel', '-no-feature-completer', '-no-feature-dialogbuttonbox', '-no-feature-tablewidget', '-no-feature-tabwidget', '-no-feature-pushbutton', '-no-feature-spinbox', '-no-feature-toolbutton', '-no-feature-lcdnumber', '-no-feature-label', '-no-feature-checkbox', '-no-feature-tableview', '-no-feature-colordialog', '-no-feature-syntaxhighlighter', '-no-feature-datetimeedit', '-no-feature-splashscreen', '-no-feature-abstractslider', '-no-feature-dial', '-no-feature-fontdialog', '-no-feature-textbrowser', '-no-feature-columnview', '-no-feature-combobox', '-no-feature-scrollarea', '-no-feature-formlayout', '-no-feature-undostack', '-no-feature-statustip', '-no-feature-graphicsview', '-no-feature-dockwidget', '-no-feature-tooltip', '-no-feature-groupbox', '-no-feature-scrollbar', '-no-feature-rubberband', '-no-feature-radiobutton', '-no-feature-sizegrip', '-no-feature-progressbar', '-no-feature-scroller', '-no-feature-menu', '-no-feature-toolbox', '-no-feature-statusbar', '-no-feature-wizard', '-no-feature-datawidgetmapper', '-no-feature-treeview', '-no-feature-dialog', '-no-feature-paint_debug', '-no-feature-textedit', '-no-feature-abstractbutton', '-no-feature-listwidget', '-no-feature-commandlinkbutton', '-no-feature-tabbar', '-no-feature-progressdialog', '-no-feature-mdiarea', '-no-feature-messagebox', '-no-feature-toolbar', '-no-feature-graphicseffect', '-no-feature-filedialog', '-no-feature-itemviews', '-no-feature-treewidget', '-no-feature-buttongroup', '-no-feature-undocommand', '-no-feature-style-stylesheet', '-no-feature-contextmenu', '-no-feature-lineedit', '-no-feature-undogroup', '-no-feature-dirmodel', '-no-feature-undoview', '-no-feature-calendarwidget', '-no-feature-fontcombobox', '-no-feature-resizehandler', '-no-feature-stackedwidget', '-no-feature-menubar', '-no-feature-effects', '-no-feature-widgettextcontrol', '-no-feature-mainwindow', '-no-feature-splitter', '-no-feature-slider', '-no-feature-errormessage', '-no-feature-whatsthis', '-no-feature-keysequenceedit', '-no-feature-listview', '-no-feature-inputdialog', '-no-feature-networkinterface', '-no-feature-localserver', '-no-feature-http', '-no-feature-udpsocket', '-no-feature-bearermanagement', '-no-feature-ftp', '-no-feature-socks5', '-no-feature-networkdiskcache', '-no-feature-networkproxy', '-no-feature-printer', '-no-feature-printpreviewwidget', '-no-feature-printdialog', '-no-feature-printpreviewdialog', '-no-feature-cups', '-no-feature-topleveldomain', '-no-feature-datestring', '-no-feature-timezone', '-no-feature-codecs', '-no-feature-textdate', '-no-feature-filesystemwatcher', '-no-feature-sharedmemory', '-no-feature-settings', '-no-feature-sortfilterproxymodel', '-no-feature-translation', '-no-feature-big_codecs', '-no-feature-processenvironment', '-no-feature-gestures', '-no-feature-xmlstreamwriter', '-no-feature-systemsemaphore', '-no-feature-itemmodel', '-no-feature-identityproxymodel', '-no-feature-process', '-no-feature-library', '-no-feature-animation', '-no-feature-iconv', '-no-feature-commandlineparser', '-no-feature-properties', '-no-feature-filesystemiterator', '-no-feature-textcodec', '-no-feature-temporaryfile', '-no-feature-sha3-fast', '-no-feature-statemachine', '-no-feature-mimetype', '-no-feature-stringlistmodel', '-no-feature-xmlstream', '-no-feature-xmlstreamreader', '-no-feature-regularexpression', '-no-feature-proxymodel', '-no-feature-shortcut', '-no-feature-freetype', '-no-feature-image_heuristic_mask', '-no-feature-imageformat_jpeg', '-no-feature-imageformat_xpm', '-no-feature-imageformat_ppm', '-no-feature-highdpiscaling', '-no-feature-pdf', '-no-feature-tabletevent', '-no-feature-imageformat_png', '-no-feature-standarditemmodel', '-no-feature-texthtmlparser', '-no-feature-cursor', '-no-feature-colornames', '-no-feature-draganddrop', '-no-feature-im', '-no-feature-imageformat_bmp', '-no-feature-sessionmanager', '-no-feature-picture', '-no-feature-wheelevent', '-no-feature-accessibility', '-no-feature-imageformat_xbm', '-no-feature-cssparser', '-no-feature-clipboard', '-no-feature-textodfwriter', '-no-feature-imageformatplugin', '-no-feature-systemtrayicon', '-no-feature-action', '-no-feature-validator', '-no-feature-movie', '-no-feature-desktopservices', '-no-feature-image_text', '-no-feature-dom', '-no-widgets', '-no-dbus', '-no-gui', '-no-accessibility', '-no-opengl', '-no-cups', '-no-fontconfig', '-no-harfbuzz', '-no-ssl', '-no-xkbcommon', '-no-xkbcommon-evdev'], 'qtlocation': [], 'qt3d': [], 'qtquickcontrols': [], 'qtvirtualkeyboard': [], 'qtx11extras': [], 'qtquickcontrols2': ['-no-feature-quicktemplates2-hover', '-no-feature-quickcontrols2-universal', '-no-feature-quickcontrols2-material'], 'qtsensors': [], 'qtxmlpatterns': ['-no-feature-xml-schema'], 'qtwinextras': [], 'qtserialbus': [], 'qtcharts': [], 'qtactiveqt': [], 'qtwebview': [], 'qtgraphicaleffects': [], 'qtdatavis3d': [], 'qtscxml': [], 'qtserialport': [], 'qtmacextras': [], 'qtsvg': [], 'qtwebsockets': [], 'qtandroidextras': [], 'qtcanvas3d': [], 'qtconnectivity': []}


"""
htmlwriter.registerWarning('qtbase', '-no-feature-label', 7, '''\
         itemviews/qheaderview.cpp:3183:53: warning: unused parameter ‘section’ [-Wunused-parameter]
         itemviews/qheaderview.cpp:3183:66: warning: unused parameter ‘position’ [-Wunused-parameter]
         dialogs/qdialog.cpp:63:50: warning: unused parameter ‘dialog’ [-Wunused-parameter]
         util/qsystemtrayicon.cpp:498:15: warning: unused variable ‘iconSize’ [-Wunused-variable]
         util/qsystemtrayicon.cpp:478:39: warning: unused parameter ‘icon’ [-Wunused-parameter]
         util/qsystemtrayicon.cpp:478:60: warning: unused parameter ‘title’ [-Wunused-parameter]
         util/qsystemtrayicon.cpp:479:41: warning: unused parameter ‘message’ [-Wunused-parameter]''')







htmlwriter.registerWarning('qtbase', '-no-feature-widgettextcontrol', 3, '''\
         itemviews/qabstractitemdelegate.cpp:535:54: warning: unused parameter ‘editor’ [-Wunused-parameter]
         util/qflickgesture.cpp:273:54: warning: unused parameter ‘flags’ [-Wunused-parameter]
         itemviews/qitemeditorfactory.cpp:232:73: warning: unused parameter ‘parent’ [-Wunused-parameter]''')







htmlwriter.registerError('qtbase',  '-no-feature-stylesheet', '''\
         widgets/qmenu.cpp:132:26: error: ‘class QMenu’ has no member named ‘styleSheet’; did you mean ‘style’?
         widgets/qmenu.cpp:132:38: error: ‘setStyleSheet’ was not declared in this scope
         make[3]: *** [.obj/qmenu.o] Error 1
         make[3]: *** Waiting for unfinished jobs....
         make[2]: *** [sub-widgets-make_first] Error 2
         make[1]: *** [sub-src-make_first] Error 2''')

htmlwriter.registerError('qtbase',  '-no-feature-http', '''\
         access/http2/http2streams_p.h:85:18: error: ‘HttpMessagePair’ does not name a type
         access/http2/http2streams_p.h:90:5: error: ‘QHttpNetworkReply’ does not name a type
         access/http2/http2streams_p.h:91:11: error: ‘QHttpNetworkRequest’ does not name a type
         access/http2/http2streams_p.h:92:5: error: ‘QHttpNetworkRequest’ does not name a type
         access/http2/http2streams_p.h:93:5: error: ‘QHttpNetworkRequest’ does not name a type
         access/http2/http2streams_p.h:98:5: error: ‘HttpMessagePair’ does not name a type
         access/http2/http2streams.cpp:56:22: error: ‘Templ<HttpMessagePair>’ does not name a type
         access/http2/http2streams.cpp:57:7: error: class ‘Http2::Stream’ does not have any field named ‘httpPair’
         access/http2/http2streams.cpp:73:1: error: ‘QHttpNetworkReply’ does not name a type
         access/http2/http2streams.cpp:78:7: error: ‘QHttpNetworkRequest’ does not name a type
         access/http2/http2streams.cpp:83:1: error: ‘QHttpNetworkRequest’ does not name a type
         access/http2/http2streams.cpp:88:1: error: ‘QHttpNetworkRequest’ does not name a type
         access/http2/http2streams.cpp:95:22: error: ‘priority’ was not declared in this scope
         access/http2/http2streams.cpp:96:10: error: ‘QHttpNetworkRequest’ has not been declared
         access/http2/http2streams.cpp:98:10: error: ‘QHttpNetworkRequest’ has not been declared
         access/http2/http2streams.cpp:100:10: error: ‘QHttpNetworkRequest’ has not been declared
         access/http2/http2streams.cpp:108:12: error: ‘httpPair’ was not declared in this scope
         make[3]: *** [.obj/http2streams.o] Error 1
         make[3]: *** Waiting for unfinished jobs....
         make[2]: *** [sub-network-make_first] Error 2
         make[2]: *** Waiting for unfinished jobs....
         make[1]: *** [sub-src-make_first] Error 2''')




htmlwriter.registerError('qtserialbus', '-no-feature-regularexpression', '''\
         canbusutil.cpp:152:32: error: variable ‘const QRegularExpression re’ has initializer but incomplete type
         make[4]: *** [.obj/canbusutil.o] Error 1
         make[3]: *** [sub-canbusutil-make_first] Error 2
         make[2]: *** [sub-tools-make_first] Error 2
         make[1]: *** [sub-src-make_first] Error 2''')


htmlwriter.registerWarning('qtquickcontrols', '-no-feature-shortcut', 5, '''\
         qquickaction.cpp:292:49: warning: unused parameter ‘arg’ [-Wunused-parameter]
         qquickaction.cpp:317:56: warning: unused parameter ‘text’ [-Wunused-parameter]
         qquickaction.cpp:427:35: warning: unused parameter ‘e’ [-Wunused-parameter]
         qquickaction.cpp:248:6: warning: ‘bool {anonymous}::qMnemonicContextMatcher(QObject*, Qt::ShortcutContext)’ defined but not used [-Wunused-function]
         qquickaction.cpp:222:6: warning: ‘bool {anonymous}::qShortcutContextMatcher(QObject*, Qt::ShortcutContext)’ defined but not used [-Wunused-function]''')
"""

long_errmsg = '''\
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from animations/chartanimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
animations/chartanimation.cpp: In constructor ‘QtCharts::ChartAnimation::ChartAnimation(QObject*)’:
animations/chartanimation.cpp:35:5: error: class ‘QtCharts::ChartAnimation’ does not have any field named ‘QVariantAnimation’
     QVariantAnimation(parent),
     ^~~~~~~~~~~~~~~~~
animations/chartanimation.cpp: In member function ‘void QtCharts::ChartAnimation::stopAndDestroyLater()’:
animations/chartanimation.cpp:43:10: error: ‘stop’ was not declared in this scope
     stop();
          ^
animations/chartanimation.cpp:44:17: error: ‘deleteLater’ was not declared in this scope
     deleteLater();
                 ^
animations/chartanimation.cpp: In member function ‘void QtCharts::ChartAnimation::startChartAnimation()’:
animations/chartanimation.cpp:50:15: error: ‘start’ was not declared in this scope
         start();
               ^
make[3]: *** [.obj/chartanimation.o] Error 1
make[3]: *** Waiting for unfinished jobs....
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/axisanimation_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/axisanimation_p.h:1,
                 from animations/axisanimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
animations/axisanimation.cpp: In constructor ‘QtCharts::AxisAnimation::AxisAnimation(QtCharts::ChartAxisElement*, int, QEasingCurve&)’:
animations/axisanimation.cpp:44:25: error: ‘setDuration’ was not declared in this scope
     setDuration(duration);
                         ^
animations/axisanimation.cpp:45:25: error: ‘setEasingCurve’ was not declared in this scope
     setEasingCurve(curve);
                         ^
animations/axisanimation.cpp: In member function ‘void QtCharts::AxisAnimation::setAnimationType(QtCharts::AxisAnimation::Animation)’:
animations/axisanimation.cpp:54:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped)
               ^
animations/axisanimation.cpp:54:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped)
                    ^~~~~~~~~~~~~~~~~~
animations/axisanimation.cpp:55:14: error: ‘stop’ was not declared in this scope
         stop();
              ^
animations/axisanimation.cpp: In member function ‘void QtCharts::AxisAnimation::setAnimationPoint(const QPointF&)’:
animations/axisanimation.cpp:61:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped)
               ^
animations/axisanimation.cpp:61:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped)
                    ^~~~~~~~~~~~~~~~~~
animations/axisanimation.cpp:62:14: error: ‘stop’ was not declared in this scope
         stop();
              ^
animations/axisanimation.cpp: In member function ‘void QtCharts::AxisAnimation::setValues(QVector<double>&, QVector<double>&)’:
animations/axisanimation.cpp:68:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped) stop();
               ^
animations/axisanimation.cpp:68:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped) stop();
                    ^~~~~~~~~~~~~~~~~~
animations/axisanimation.cpp:68:54: error: ‘stop’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped) stop();
                                                      ^
animations/axisanimation.cpp:114:5: error: ‘QVariantAnimation’ has not been declared
     QVariantAnimation::KeyValues value;
     ^~~~~~~~~~~~~~~~~
animations/axisanimation.cpp:115:18: error: ‘value’ was not declared in this scope
     setKeyValues(value); //workaround for wrong interpolation call
                  ^~~~~
animations/axisanimation.cpp:115:23: error: ‘setKeyValues’ was not declared in this scope
     setKeyValues(value); //workaround for wrong interpolation call
                       ^
animations/axisanimation.cpp:116:52: error: ‘setKeyValueAt’ was not declared in this scope
     setKeyValueAt(0.0, qVariantFromValue(oldLayout));
                                                    ^
animations/axisanimation.cpp: In member function ‘void QtCharts::AxisAnimation::updateCurrentValue(const QVariant&)’:
animations/axisanimation.cpp:138:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped) { //workaround
               ^
animations/axisanimation.cpp:138:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped) { //workaround
                    ^~~~~~~~~~~~~~~~~~
make[3]: *** [.obj/axisanimation.o] Error 1
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/axisanimation_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/axisanimation_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/chartaxiselement_p.h:44,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/chartaxiselement_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/qabstractaxis_p.h:43,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/qabstractaxis_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/chartdataset_p.h:44,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/chartdataset_p.h:1,
                 from chartelement.cpp:33:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
make[3]: *** [.obj/chartelement.o] Error 1
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/piesliceanimation_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/piesliceanimation_p.h:1,
                 from animations/piesliceanimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
animations/piesliceanimation.cpp: In member function ‘void QtCharts::PieSliceAnimation::setValue(const QtCharts::PieSliceData&, const QtCharts::PieSliceData&)’:
animations/piesliceanimation.cpp:83:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped)
               ^
animations/piesliceanimation.cpp:83:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped)
                    ^~~~~~~~~~~~~~~~~~
animations/piesliceanimation.cpp:84:14: error: ‘stop’ was not declared in this scope
         stop();
              ^
animations/piesliceanimation.cpp:88:53: error: ‘setKeyValueAt’ was not declared in this scope
     setKeyValueAt(0.0, qVariantFromValue(startValue));
                                                     ^
animations/piesliceanimation.cpp: In member function ‘void QtCharts::PieSliceAnimation::updateValue(const QtCharts::PieSliceData&)’:
animations/piesliceanimation.cpp:94:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped)
               ^
animations/piesliceanimation.cpp:94:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped)
                    ^~~~~~~~~~~~~~~~~~
animations/piesliceanimation.cpp:95:14: error: ‘stop’ was not declared in this scope
         stop();
              ^
animations/piesliceanimation.cpp:97:57: error: ‘setKeyValueAt’ was not declared in this scope
     setKeyValueAt(0.0, qVariantFromValue(m_currentValue));
                                                         ^
animations/piesliceanimation.cpp: In member function ‘void QtCharts::PieSliceAnimation::updateCurrentValue(const QVariant&)’:
animations/piesliceanimation.cpp:131:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped) { //workaround
               ^
animations/piesliceanimation.cpp:131:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped) { //workaround
                    ^~~~~~~~~~~~~~~~~~
make[3]: *** [.obj/piesliceanimation.o] Error 1
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/xyanimation_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/xyanimation_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/scatteranimation_p.h:41,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/scatteranimation_p.h:1,
                 from animations/scatteranimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/xyanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/scatteranimation_p.h:41,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/scatteranimation_p.h:1,
                 from animations/scatteranimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/xyanimation_p.h:62:22: error: ‘QAbstractAnimation’ has not been declared
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                      ^~~~~~~~~~~~~~~~~~
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/xyanimation_p.h:62:48: error: expected ‘,’ or ‘...’ before ‘newState’
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                                                ^~~~~~~~
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/scatteranimation_p.h:1:0,
                 from animations/scatteranimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/scatteranimation_p.h:54:22: error: ‘QAbstractAnimation’ has not been declared
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                      ^~~~~~~~~~~~~~~~~~
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/scatteranimation_p.h:54:48: error: expected ‘,’ or ‘...’ before ‘newState’
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                                                ^~~~~~~~
animations/scatteranimation.cpp:45:36: error: variable or field ‘updateState’ declared void
 void ScatterAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)
                                    ^~~~~~~~~~~~~~~~~~
animations/scatteranimation.cpp:45:36: error: ‘QAbstractAnimation’ has not been declared
animations/scatteranimation.cpp:45:72: error: ‘QAbstractAnimation’ has not been declared
 void ScatterAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)
                                                                        ^~~~~~~~~~~~~~~~~~
animations/scatteranimation.cpp:59:1: error: expected ‘}’ at end of input
 QT_CHARTS_END_NAMESPACE
 ^
make[3]: *** [.obj/scatteranimation.o] Error 1
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/xyanimation_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/xyanimation_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/splineanimation_p.h:41,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/splineanimation_p.h:1,
                 from animations/splineanimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/xyanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/splineanimation_p.h:41,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/splineanimation_p.h:1,
                 from animations/splineanimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/xyanimation_p.h:62:22: error: ‘QAbstractAnimation’ has not been declared
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                      ^~~~~~~~~~~~~~~~~~
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/xyanimation_p.h:62:48: error: expected ‘,’ or ‘...’ before ‘newState’
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                                                ^~~~~~~~
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/splineanimation_p.h:1:0,
                 from animations/splineanimation.cpp:30:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/splineanimation_p.h:60:22: error: ‘QAbstractAnimation’ has not been declared
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                      ^~~~~~~~~~~~~~~~~~
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/splineanimation_p.h:60:48: error: expected ‘,’ or ‘...’ before ‘newState’
     void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState);
                                                ^~~~~~~~
animations/splineanimation.cpp: In member function ‘void QtCharts::SplineAnimation::setup(QVector<QPointF>&, QVector<QPointF>&, QVector<QPointF>&, QVector<QPointF>&, int)’:
animations/splineanimation.cpp:64:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped) {
               ^
animations/splineanimation.cpp:64:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped) {
                    ^~~~~~~~~~~~~~~~~~
animations/splineanimation.cpp:65:14: error: ‘stop’ was not declared in this scope
         stop();
              ^
animations/splineanimation.cpp:122:54: error: ‘setKeyValueAt’ was not declared in this scope
     setKeyValueAt(0.0, qVariantFromValue(m_oldSpline));
                                                      ^
animations/splineanimation.cpp: In member function ‘void QtCharts::SplineAnimation::updateCurrentValue(const QVariant&)’:
animations/splineanimation.cpp:181:15: error: ‘state’ was not declared in this scope
     if (state() != QAbstractAnimation::Stopped && m_valid) { //workaround
               ^
animations/splineanimation.cpp:181:20: error: ‘QAbstractAnimation’ has not been declared
     if (state() != QAbstractAnimation::Stopped && m_valid) { //workaround
                    ^~~~~~~~~~~~~~~~~~
animations/splineanimation.cpp: At global scope:
animations/splineanimation.cpp:191:35: error: variable or field ‘updateState’ declared void
 void SplineAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)
                                   ^~~~~~~~~~~~~~~~~~
animations/splineanimation.cpp:191:35: error: ‘QAbstractAnimation’ has not been declared
animations/splineanimation.cpp:191:71: error: ‘QAbstractAnimation’ has not been declared
 void SplineAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)
                                                                       ^~~~~~~~~~~~~~~~~~
animations/splineanimation.cpp:219:1: error: expected ‘}’ at end of input
 QT_CHARTS_END_NAMESPACE
 ^
make[3]: *** [.obj/splineanimation.o] Error 1
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/axisanimation_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/axisanimation_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/chartaxiselement_p.h:44,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/chartaxiselement_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/cartesianchartaxis_p.h:43,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/cartesianchartaxis_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/verticalaxis_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/verticalaxis_p.h:1,
                 from axis/verticalaxis.cpp:34:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
make[3]: *** [.obj/verticalaxis.o] Error 1
In file included from ../../include/QtCharts/5.9.0/QtCharts/private/chartanimation_p.h:1:0,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/axisanimation_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/axisanimation_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/chartaxiselement_p.h:44,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/chartaxiselement_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/cartesianchartaxis_p.h:43,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/cartesianchartaxis_p.h:1,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/axis/horizontalaxis_p.h:42,
                 from ../../include/QtCharts/5.9.0/QtCharts/private/horizontalaxis_p.h:1,
                 from axis/horizontalaxis.cpp:34:
../../include/QtCharts/5.9.0/QtCharts/private/../../../../../src/charts/animations/chartanimation_p.h:50:1: error: expected class-name before ‘{’ token
 {
 ^
make[3]: *** [.obj/horizontalaxis.o] Error 1
make[2]: *** [sub-charts-make_first-ordered] Error 2
make[1]: *** [sub-src-make_first] Error 2
make: *** [module-qtcharts] Error 2'''


warn_msg="""\
kernel/qclipboard.cpp:298:12: warning: ‘QString::QString(const QByteArray&)’ is deprecated [-Wdeprecated-declarations]
qxcbmime.cpp:164:55: warning: unused parameter ‘requestedType’ [-Wunused-parameter]"""


warn_msg2="""\
itemviews/qheaderview.cpp:3183:53: warning: unused parameter ‘section’ [-Wunused-parameter]
itemviews/qheaderview.cpp:3183:66: warning: unused parameter ‘position’ [-Wunused-parameter]
dialogs/qdialog.cpp:63:50: warning: unused parameter ‘dialog’ [-Wunused-parameter]
util/qsystemtrayicon.cpp:498:15: warning: unused variable ‘iconSize’ [-Wunused-variable]
util/qsystemtrayicon.cpp:478:39: warning: unused parameter ‘icon’ [-Wunused-parameter]
util/qsystemtrayicon.cpp:478:60: warning: unused parameter ‘title’ [-Wunused-parameter]
util/qsystemtrayicon.cpp:479:41: warning: unused parameter ‘message’ [-Wunused-parameter]"""

warn_msg3 = '''api/qeglfsscreen.cpp:150:51: warning: unused parameter ‘pos’ [-Wunused-parameter]'''


i = 0;
for (repo,features) in feature_dict.items():
    htmlwriter.registerRepo(repo, "badf00d")
    for feature in features:
        htmlwriter.registerError(repo, feature, long_errmsg)
    i += 1;
    if (i % 5 == 0):
        htmlwriter.registerWarning(repo, '-no-such-feature', 2, warn_msg)
    if (i % 3 == 0):
        htmlwriter.registerWarning(repo, '-no-feature-dummy', 7, warn_msg2)
    if (i % 7 == 0):
        htmlwriter.registerWarning(repo, '-no-feature-something', 1, warn_msg3)




htmlwriter.registerStats(buildcount = 4321)




htmlfile = open('ffeaturetest_test'+'.html', 'w')


htmlwriter.writeHtml(htmlfile)
