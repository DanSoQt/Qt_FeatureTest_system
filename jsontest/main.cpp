#include <QCoreApplication>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QJsonValue>
#include <QFile>
#include <QDebug>

int main(int argc, char *argv[])
{
    QString fn = "configure.json";
    if (argc > 1)
        fn = argv[1];
    
    QFile f(fn);
    f.open(QIODevice::ReadOnly);
    QByteArray b = f.readAll();

    auto doc = QJsonDocument::fromJson(b);
//    qDebug() << doc.toJson().constData();
//    qDebug() << doc.isArray() << doc.isObject() << doc.isEmpty();
    auto obj = doc.object();
    auto fval = obj.value("features");
//    qDebug() << fval.isArray() << fval.isObject() << fval.isNull();
    if (fval.isArray()) {
        auto features = fval.toArray();
        qDebug() << QJsonDocument(features).toJson().constData();
    }
    if (fval.isObject()) {
        const auto features = fval.toObject();

        auto i = features.constBegin();
        while (i != features.constEnd()) {
            auto o = i.value().toObject();
            if (o.contains("purpose"))
                qDebug() << i.key().toLocal8Bit().constData();
            ++i;
        }
    }
}
