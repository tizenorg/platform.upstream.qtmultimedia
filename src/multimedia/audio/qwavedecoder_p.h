/****************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser General Public
** License version 2.1 as published by the Free Software Foundation and
** appearing in the file LICENSE.LGPL included in the packaging of this
** file. Please review the following information to ensure the GNU Lesser
** General Public License version 2.1 requirements will be met:
** http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** In addition, as a special exception, Nokia gives you certain additional
** rights. These rights are described in the Nokia Qt LGPL Exception
** version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU General
** Public License version 3.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of this
** file. Please review the following information to ensure the GNU General
** Public License version 3.0 requirements will be met:
** http://www.gnu.org/copyleft/gpl.html.
**
** Other Usage
** Alternatively, this file may be used in accordance with the terms and
** conditions contained in a signed written agreement between you and Nokia.
**
**
**
**
**
** $QT_END_LICENSE$
**
****************************************************************************/

#ifndef WAVEDECODER_H
#define WAVEDECODER_H

//
//  W A R N I N G
//  -------------
//
// This file is not part of the Qt API.  It exists for the convenience
// of other Qt classes.  This header file may change from version to
// version without notice, or even be removed.
//
// We mean it.
//

#include <QtCore/qiodevice.h>
#include <qaudioformat.h>


QT_BEGIN_HEADER

QT_BEGIN_NAMESPACE

QT_MODULE(Multimedia)



class QWaveDecoder : public QIODevice
{
    Q_OBJECT

public:
    explicit QWaveDecoder(QIODevice *source, QObject *parent = 0);
    ~QWaveDecoder();

    QAudioFormat audioFormat() const;
    int duration() const;

    qint64 size() const;
    bool isSequential() const;
    qint64 bytesAvailable() const;

Q_SIGNALS:
    void formatKnown();
    void parsingError();

private Q_SLOTS:
    void handleData();

private:
    qint64 readData(char *data, qint64 maxlen);
    qint64 writeData(const char *data, qint64 len);

    bool enoughDataAvailable();
    bool findChunk(const char *chunkId);
    void discardBytes(qint64 numBytes);
    void parsingFailed();

    enum State {
        InitialState,
        WaitingForFormatState,
        WaitingForDataState
    };

    struct chunk
    {
        char        id[4];
        quint32     size;
    };
    bool peekChunk(chunk* pChunk);

    struct RIFFHeader
    {
        chunk       descriptor;
        char        type[4];
    };
    struct WAVEHeader
    {
        chunk       descriptor;
        quint16     audioFormat;
        quint16     numChannels;
        quint32     sampleRate;
        quint32     byteRate;
        quint16     blockAlign;
        quint16     bitsPerSample;
    };

    bool haveFormat;
    qint64 dataSize;
    QAudioFormat format;
    QIODevice *source;
    State state;
    quint32 junkToSkip;
    bool bigEndian;
};

QT_END_NAMESPACE

QT_END_HEADER

#endif // WAVEDECODER_H