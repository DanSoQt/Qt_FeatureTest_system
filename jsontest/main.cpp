#include <QCoreApplication>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QJsonValue>
#include <QFile>
#include <QDebug>
#include <QDir>
#include <QDirIterator>

int main(int argc, char *argv[])
{
    QDir dir = QDir::current();
    dir.setNameFilters(QStringList() << "configure.json");
    QDirIterator it(dir, QDirIterator::Subdirectories);

    QStringList modules;
    QByteArray repo = QDir::current().dirName().toLocal8Bit();
    while (it.hasNext()) {
        it.next();

        QFile f(it.filePath());
        f.open(QIODevice::ReadOnly);
        QByteArray b = f.readAll();

        auto doc = QJsonDocument::fromJson(b);
//    qDebug() << doc.toJson().constData();
//    qDebug() << doc.isArray() << doc.isObject() << doc.isEmpty();
        auto obj = doc.object();
        auto module = obj.value("module");

//    qDebug() << module.isArray() << module.isObject() << module.isNull() << module.isString() << module.toString();

        QString moduleName = module.toString();
        if (moduleName.isEmpty())
            continue;
#if 0
        if (moduleName == "widgets")
            continue; //#########
#endif
        auto fval = obj.value("features");
//    qDebug() << fval.isArray() << fval.isObject() << fval.isNull();

        if (fval.isObject()) {
            bool foundPurpose = false;

            const auto features = fval.toObject();

            auto i = features.constBegin();
            while (i != features.constEnd()) {
                auto o = i.value().toObject();
                if (o.contains("purpose")) {
                    if (!foundPurpose) {
                        modules << moduleName;
                        QByteArray mf = "features_" + moduleName.toLocal8Bit();
                        qDebug() << mf.constData() << "= [";
                        foundPurpose = true;
                    }
                    qDebug().nospace() << "    '-no-feature-" << i.key().toLocal8Bit().constData() <<"',";
                }
                ++i;
            }
            if (foundPurpose)
                qDebug() << "]";
        }

    }


    QByteArray rf = "repo_features['" + repo + "']";


    if (!modules.isEmpty()) {
        qDebug() << rf.constData() << "= []";
        for (auto s : modules) {
            QByteArray mf = "features_" + s.toLocal8Bit();
            qDebug() << rf.constData() << "+=" << mf.constData();
        }
    }
}



