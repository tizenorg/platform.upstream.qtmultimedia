
%if "%{tizen}" == "2.1"
%define profile mobile
%endif

%if "%{tizen}" == "2.3"
%define profile wearable
%define _with_only_free_components 1
%endif

%if "%{profile}" != "mobile" && "%{profile}" != "wearable"
%define _with_gstreamer1 1
%endif

%bcond_with only_free_components
%bcond_with gstreamer1

Name:       qt5-qtmultimedia
Summary:    Qt Multimedia module
Version:    5.3.1
Release:    0
Group:      Base/Libraries
License:    LGPL-2.1+ or GPL-3.0
URL:        http://qt.digia.com
Source0:    %{name}-%{version}.tar.bz2
Source1001: %{name}.manifest
BuildRequires:  qt5-qtcore-devel
BuildRequires:  qt5-qtgui-devel
BuildRequires:  qt5-qtwidgets-devel
BuildRequires:  qt5-qtopengl-devel
BuildRequires:  qt5-qtnetwork-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtdeclarative-qtquick-devel
BuildRequires:  qt5-qmake
BuildRequires:  pkgconfig(alsa)
BuildRequires:  fdupes
#BuildRequires:  pkgconfig(libpulse)
#BuildRequires:  pkgconfig(libpulse-mainloop-glib)
%if %{with gstreamer1}
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
%else
BuildRequires:  pkgconfig(gstreamer-0.10)
BuildRequires:  pkgconfig(gstreamer-base-0.10)
BuildRequires:  pkgconfig(gstreamer-interfaces-0.10)
BuildRequires:  pkgconfig(gstreamer-audio-0.10)
BuildRequires:  pkgconfig(gstreamer-video-0.10)
BuildRequires:  pkgconfig(gstreamer-pbutils-0.10)
BuildRequires:  pkgconfig(gstreamer-app-0.10)
%if ! %{with only_free_components}
BuildRequires:  pkgconfig(gstreamer-plugins-bad-0.10)
%endif
%endif

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the QtMultimedia module


%package devel
Summary:    Qt Multimedia - development files
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the QtMultimedia module development files

%package -n qt5-qtdeclarative-import-multimedia
Summary:    QtQml multimedia import
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   qt5-qtdeclarative

%description -n qt5-qtdeclarative-import-multimedia
This package contains the Multimedia import for QtQml

%package gsttools
Summary:    Qt Multimedia - Utility library for GStreamer media services
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}

%description gsttools
This package contains a shared library for the GStreamer QtMultimedia media services

%package plugin-mediaservice-gstaudiodecoder
Summary:    Qt Multimedia - GStreamer audio decoder media service
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   qt5-qtmultimedia-gsttools = %{version}-%{release}

%description plugin-mediaservice-gstaudiodecoder
This package contains the GStreamer audio decoder plugin for QtMultimedia

%package plugin-mediaservice-gstcamerabin
Summary:    Qt Multimedia - GStreamer camerabin video capture media service
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   qt5-qtmultimedia-gsttools = %{version}-%{release}

%description plugin-mediaservice-gstcamerabin
This package contains the GStreamer camerabin video capture plugin for QtMultimedia

%package plugin-mediaservice-gstmediacapture
Summary:    Qt Multimedia - GStreamer video4linux2 video capture media service
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   qt5-qtmultimedia-gsttools = %{version}-%{release}

%description plugin-mediaservice-gstmediacapture
This package contains the GStreamer video4linux2 video capture plugin for QtMultimedia

%package plugin-mediaservice-gstmediaplayer
Summary:    Qt Multimedia - GStreamer playback media service
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   qt5-qtmultimedia-gsttools = %{version}-%{release}

%description plugin-mediaservice-gstmediaplayer
This package contains the GStreamer media playback plugin for QtMultimedia

%package plugin-playlistformats-m3u
Summary:    Qt Multimedia - M3U playlist support
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   qt5-qtmultimedia-gsttools = %{version}-%{release}

%description plugin-playlistformats-m3u
This package contains the M3U playlist support

# %package plugin-audio-pulseaudio
# Summary:    Qt Multimedia - Pulse Audio plugin
# Group:      Base/Libraries
# Requires:   %{name} = %{version}-%{release}
#
# %description plugin-audio-pulseaudio
# This package contains the pulse audio sound effect support.

%package plugin-audio-alsa
Summary:    Qt Multimedia - Alsa Audio plugin
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}

%description plugin-audio-alsa
This package contains the pulse audio sound effect support.

#### Build section

%prep
%setup -q -n %{name}-%{version}/qtmultimedia
cp %{SOURCE1001} .

%build
export QTDIR=/usr/share/qt5
touch .git

qmake -qt=5
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%qmake5_install

# Fix wrong path in pkgconfig files
find %{buildroot}%{_libdir}/pkgconfig -type f -name '*.pc' \
-exec perl -pi -e "s, -L%{_builddir}/?\S+,,g" {} \;
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;



%fdupes %{buildroot}/%{_includedir}




#### Pre/Post section

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%post gsttools
/sbin/ldconfig
%postun gsttools
/sbin/ldconfig



#### File section


%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/libQt5Multimedia.so.5
%{_libdir}/libQt5Multimedia.so.5.*
%{_libdir}/libQt5MultimediaWidgets.so.5
%{_libdir}/libQt5MultimediaWidgets.so.5.*
%{_libdir}/libQt5MultimediaQuick_p.so.5
%{_libdir}/libQt5MultimediaQuick_p.so.5.*

%files devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/libQt5Multimedia.so
%{_libdir}/libQt5MultimediaWidgets.so
%{_libdir}/libQt5MultimediaQuick_p.so
%{_libdir}/libqgsttools_p.so
%{_libdir}/libQt5Multimedia.prl
%{_libdir}/libQt5Multimedia.la
%{_libdir}/libQt5MultimediaWidgets.prl
%{_libdir}/libQt5MultimediaWidgets.la
%{_libdir}/libQt5MultimediaQuick_p.prl
%{_libdir}/libQt5MultimediaQuick_p.la
%{_libdir}/libqgsttools_p.prl
%{_libdir}/pkgconfig/*
%{_includedir}/qt5/*
%{_datadir}/qt5/mkspecs/*
%{_libdir}/cmake/*


%files -n qt5-qtdeclarative-import-multimedia
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/qt5/qml/QtMultimedia/*

%files gsttools
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/libqgsttools_p.so.1
%{_libdir}/libqgsttools_p.so.1.*

%files plugin-mediaservice-gstaudiodecoder
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/qt5/plugins/mediaservice/libgstaudiodecoder.so

%files plugin-mediaservice-gstcamerabin
%defattr(-,root,root,-)
%manifest %{name}.manifest
%if ! ("%{profile}" == "common" || "%{profile}" == "ivi" || "%{profile}" == "generic" || "%{profile}" == "mobile" )
#commented out until the work on gstreamer-1.0 will be finished in Qt
#%{_libdir}/qt5/plugins/mediaservice/libgstcamerabin.so
%endif

%files plugin-mediaservice-gstmediacapture
%defattr(-,root,root,-)
%manifest %{name}.manifest
%if ! ("%{profile}" == "common" || "%{profile}" == "ivi" || "%{profile}" == "generic" || "%{profile}" == "mobile" )
#commented out until the work on gstreamer-1.0 will be finished in Qt
#%{_libdir}/qt5/plugins/mediaservice/libgstmediacapture.so
%endif

%files plugin-mediaservice-gstmediaplayer
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/qt5/plugins/mediaservice/libgstmediaplayer.so

%files plugin-playlistformats-m3u
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/qt5/plugins/playlistformats/libqtmultimedia_m3u.so

# %files plugin-audio-pulseaudio
# %defattr(-,root,root,-)
%manifest %{name}.manifest
# %{_libdir}/qt5/plugins/audio/libqtmedia_pulse.so

%files plugin-audio-alsa
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/qt5/plugins/audio/libqtaudio_alsa.so

#### No changelog section, separate $pkg.changelog contains the history
