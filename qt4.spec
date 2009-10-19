#
# TODO:
#	- figure out why it tries to link with system qt (fix and drop BuildConflicts Qt)
#	- better descriptions
#	- more cleanups
#	- check if translations are available
#	- check Qt ui tool
# - QtDBus (and maybe others) not multilib compatible (split pkgs or drop symlinks)
#   file /usr/bin/qdbus from install of QtDBus-4.5.0-7.i686 conflicts with file from package QtDBus-4.5.0-7.x86_64
#   file /usr/bin/qdbusviewer from install of QtDBus-4.5.0-7.i686 conflicts with file from package QtDBus-4.5.0-7.x86_64
#   $ rpm -q QtDBus --filecolor|less
#   /usr/bin/qdbus  0
#   /usr/bin/qdbusviewer    0
#   $ file /usr/bin/qdbus /usr/bin/qdbusviewer
#   /usr/bin/qdbus:       symbolic link to `../lib/qt4/bin/qdbus'
#   /usr/bin/qdbusviewer: symbolic link to `../lib/qt4/bin/qdbusviewer'
#   MORAL: it would be ok if the files were marked as multilib (colors 1 or 2), not symlinks (color 0)
#   I personally would moved binaries to %{_bindir}
# - solve dep loops:
#error: LOOP:
#error: removing QtGui-4.4.3-1.athlon "Requires(auto): libQtSvg.so.4" from tsort relations.
#error:     QtGui-4.4.3-1.athlon                     Requires(auto): libQtSvg.so.4
#error: removing QtSvg-4.4.3-1.athlon "Requires(auto): libQtGui.so.4" from tsort relations.
#error:     QtSvg-4.4.3-1.athlon                     Requires(auto): libQtGui.so.4
#
#error: LOOP:
#error: removing QtGui-4.3.4-2.athlon "Requires(auto): libQtGui.so.4" from tsort relations.
#error:     QtGui-4.3.4-2.athlon                     Requires(auto): libQtGui.so.4
#error: removing QtSvg-4.3.4-2.athlon "Requires(auto): libQtSvg.so.4" from tsort relations.
#error:     QtSvg-4.3.4-2.athlon                     Requires(auto): libQtSvg.so.4
#
#error: LOOP:
#error: removing Qt3Support-4.4.3-1.athlon "Requires: QtGui = 4.4.3-1" from tsort relations.
#error:     Qt3Support-4.4.3-1.athlon                Requires: QtGui = 4.4.3-1
#error: removing QtGui-4.4.3-1.athlon "Requires: Qt3Support = 4.4.3-1" from tsort relations.
#error:     QtGui-4.4.3-1.athlon                     Requires: Qt3Support = 4.4.3-1
#
#error: LOOP:
#error: removing QtGui-4.3.4-2.athlon "Requires: QtGui = 4.3.4-2" from tsort relations.
#error:     QtGui-4.3.4-2.athlon                     Requires: QtGui = 4.3.4-2
#error: removing Qt3Support-4.3.4-2.athlon "Requires: Qt3Support = 4.3.4-2" from tsort relations.
#error:     Qt3Support-4.3.4-2.athlon                Requires: Qt3Support = 4.3.4-2
#
# Package those files:
#   /usr/lib64/libphonon.a
#   /usr/lib64/qt4/bin/qttracereplay
#   /usr/lib64/qt4/bin/xmlpatternsvalidator
#
# Conditional build:
%bcond_with	nas		# enable NAS audio support
%bcond_without	static_libs	# build static libraries
%bcond_without	cups		# disable CUPS support
%bcond_without	mysql		# don't build MySQL plugin
%bcond_without	odbc		# don't build unixODBC plugin
%bcond_without	pgsql		# don't build PostgreSQL plugin
%bcond_without	sqlite3		# don't build SQLite3 plugin
%bcond_without	sqlite		# don't build SQLite2 plugin
%bcond_without	ibase		# don't build ibase (InterBase/Firebird) plugin
%bcond_without	pch		# disable pch in qmake
%bcond_without	gtk		# don't build GTK theme integration
%bcond_without	system_phonon
%bcond_with	sse		# use SSE instructions in gui/painting module
%bcond_with	sse2		# use SSE2 instructions
#
%define		state	beta1
#
%ifnarch %{ix86} %{x8664} sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%ifarch pentium3 pentium4 %{x8664}
%define		with_sse	1
%endif
%ifarch pentium4 %{x8664}
%define		with_sse2	1
%endif
# any SQL
%define		_withsql	1
%{!?with_sqlite3:%{!?with_sqlite:%{!?with_ibase:%{!?with_mysql:%{!?with_pgsql:%{!?with_odbc:%undefine _withsql}}}}}}
#
Summary:	The Qt GUI application framework
Summary(es.UTF-8):	Biblioteca para ejecutar aplicaciones GUI Qt
Summary(pl.UTF-8):	Biblioteka Qt do tworzenia GUI
Summary(pt_BR.UTF-8):	Estrutura para rodar aplicações GUI Qt
Name:		qt4
Version:	4.6.0
Release:	0.%{state}.1
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://get.qt.nokia.com/qt/source/qt-everywhere-opensource-src-%{version}-%{state}.tar.gz
# Source0-md5:	60d136f17491ce0e56bb317ea7300aef
Source2:	%{name}-qtconfig.desktop
Source3:	%{name}-designer.desktop
Source4:	%{name}-assistant.desktop
Source5:	%{name}-linguist.desktop

# git clone git://gitorious.org/+kde-developers/qt/kde-qt.git
# git checkout -b 4.5.3-patched origin/4.5.3-patched
# git diff v4.5.3..4.5.3-patched > qt4-kde-git.patch
Patch100:	%{name}-kde-git.patch

Patch0:		%{name}-tools.patch
Patch1:		%{name}-qt_copy.patch
Patch2:		%{name}-buildsystem.patch
Patch3:		%{name}-locale.patch
Patch4:		%{name}-antialias.patch
Patch5:		%{name}-support-cflags-with-commas.patch
Patch6:		%{name}-build-lib-static.patch
Patch7:		%{name}-x11_fonts.patch
Patch8:		%{name}-pl-update.patch
Patch9:		%{name}-ibase.patch
# svn://anonsvn.kde.org/home/kde/trunk/qt-copy/patches
URL:		http://www.qtsoftware.com/
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	OpenGL-GLU-devel
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
# incompatible with bison
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	dbus-devel >= 0.62
BuildRequires:	fontconfig-devel
BuildRequires:	freetds-devel
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	giflib-devel
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gstreamer-plugins-base-devel
%{?with_gtk:BuildRequires:	gtk+2-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel >= 1.0.0
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-backend-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_pgsql:BuildRequires:	postgresql-static}
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
%{?with_sqlite:BuildRequires:	sqlite-devel}
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.2.12-2}
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	zlib-devel
# when building it tries to link with system qt instead of buit one
BuildConflicts:	QtCore-devel <= %{version}
BuildConflicts:	QtScript-devel <= %{version}
Obsoletes:	qt-extensions
Obsoletes:	qt-utils
Conflicts:	kdelibs <= 8:3.2-0.030602.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_noautostrip	'.*_debug\\.so*'

%define		specflags	-fno-strict-aliasing

%define		_qtdir		%{_libdir}/qt4

%description
Qt is a complete C++ application development framework, which includes
a class library and tools for multiplatform development and
internationalization. Using Qt, a single source code tree can build
applications that run natively on different platforms (Windows,
Unix/Linux, Mac OS X, embedded Linux).

Qt has a rich set of standard widgets, and lets you write custom
controls. It encapsulates four different platform-specific APIs, and
the APIs for file-handling, networking, process-handling, threading,
database access, etc. Qt now also has Motif migration oraz Netscape
LiveConnect plugin.

%description -l es.UTF-8
Contiene las bibliotecas compartidas necesarias para ejecutar
aplicaciones Qt, bien como los archivos README.

%description -l pl.UTF-8
Qt oferuje kompletny system do tworzenia i rozwijania aplikacji w
języku C++, w którego skład wchodzi biblioteka z klasami oraz
wieloplatformowymi narzędziami do rozwijania i tłumaczenia aplikacji.
Z pomocą Qt jeden kod źródłowy może być natywnie uruchamiany na
różnych platformach (Windows, Unix/Linux, Mac OS X).

Qt ma bogaty zbiór standardowych elementów interfejsu graficznego, ale
pozwala również na pisanie własnych elementów. Łączy w sposób
niewidoczny dla programisty interfejsy programowania różnych systemów,
tworząc w ten sposób jeden interfejs dla obsługi plików, sieci,
procesów, wątków, baz danych itp. Umożliwia także łatwe przenoszenie
na Qt aplikacji korzystających z Motif oraz pisanie wtyczek z
wykorzystaniem Netscape LiveConnect.

%package -n Qt3Support
Summary:	Qt3 compatibility library
Summary(pl.UTF-8):	Biblioteka kompatybilności z Qt3
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n Qt3Support
Qt3 compatibility library.

%description -n Qt3Support -l pl.UTF-8
Biblioteka kompatybilności z Qt3.

%package -n Qt3Support-devel
Summary:	Qt3 compatibility library - development files
Summary(pl.UTF-8):	Biblioteka kompatybilności z Qt3 - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtNetwork-devel = %{version}-%{release}
Requires:	QtSql-devel = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

%description -n Qt3Support-devel
Qt3 compatibility library - development files.

%description -n Qt3Support-devel -l pl.UTF-8
Biblioteka kompatybilności z Qt3 - pliki programistyczne.

%package -n Qt3Support-static
Summary:	Qt3 compatibility library - static libraries
Summary(pl.UTF-8):	Biblioteka kompatybilności z Qt3 - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	Qt3Support-devel = %{version}-%{release}

%description -n Qt3Support-static
Qt3 compatibility library - static libraries.

%description -n Qt3Support-static -l pl.UTF-8
Biblioteka kompatybilności z Qt3 - biblioteki statyczne.

%package -n QtAssistant
Summary:	Qt Assistant client library
Summary(pl.UTF-8):	Biblioteka kliencka Qt Assistant
Group:		X11/Development/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}

%description -n QtAssistant
This library allows to use Qt Assistant as an application's help tool.

%description -n QtAssistant -l pl.UTF-8
Ta biblioteka umożliwia wykorzystanie Qt Assistanta jako narzędzie
pomocy w aplikacjach.

%package -n QtAssistant-devel
Summary:	Qt Assistant client library - development files
Summary(pl.UTF-8):	Biblioteka kliencka Qt Assistant - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtNetwork-devel = %{version}-%{release}

%description -n QtAssistant-devel
Development files for Qt Assistant client library.

%description -n QtAssistant-devel -l pl.UTF-8
Pliki programistyczne biblioteki klienckiej Qt Assistant.

%package -n QtAssistant-static
Summary:	Static Qt Assistant client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka Qt Assistant
Group:		X11/Development/Libraries
Requires:	QtAssistant-devel = %{version}-%{release}

%description -n QtAssistant-static
Static Qt Assistant client library.

%description -n QtAssistant-static -l pl.UTF-8
Statyczna biblioteka kliencka Qt Assistant.

%package -n QtCLucene
Summary:	QtCLucene full text search library wrapper
Summary(pl.UTF-8):	Interfejs QtCLucene do biblioteki wyszukiwania pełnotekstowego
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtCLucene
QtCLucene full text search library wrapper.

%description -n QtCLucene -l pl.UTF-8
Interfejs QtCLucene do biblioteki wyszukiwania pełnotekstowego.

%package -n QtCLucene-devel
Summary:	QtCLucene full text search library wrapper - development files
Summary(pl.UTF-8):	Interfejs QtCLucene do biblioteki wyszukiwania pełnotekstowego - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCLucene = %{version}-%{release}
Requires:	QtCore-devel = %{version}-%{release}

%description -n QtCLucene-devel
QtCLucene full text search library wrapper - development files.

%description -n QtCLucene-devel -l pl.UTF-8
Interfejs QtCLucene do biblioteki wyszukiwania pełnotekstowego - pliki
programistyczne.

%package -n QtCLucene-static
Summary:	QtCLucene full text search library wrapper - static library
Summary(pl.UTF-8):	Interfejs QtCLucene do biblioteki wyszukiwania pełnotekstowego - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtCLucene-devel = %{version}-%{release}

%description -n QtCLucene-static
QtCLucene full text search library wrapper - static library.

%description -n QtCLucene-static -l pl.UTF-8
Interfejs QtCLucene do biblioteki wyszukiwania pełnotekstowego -
biblioteka statyczna.

%package -n QtCore
Summary:	Core classes used by other modules
Summary(pl.UTF-8):	Podstawowe klasy używane przez inne moduły
Group:		X11/Libraries
Requires(post):	/sbin/ldconfig

%description -n QtCore
Core classes used by other modules.

%description -n QtCore -l pl.UTF-8
Podstawowe klasy używane przez inne moduły.

%package -n QtCore-devel
Summary:	Core classes used by other modules - development files
Summary(pl.UTF-8):	Podstawowe klasy używane przez inne moduły - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	glib2-devel
Requires:	libstdc++-devel
Requires:	zlib-devel

%description -n QtCore-devel
Core classes used by other modules - development files.

%description -n QtCore-devel -l pl.UTF-8
Podstawowe klasy używane przez inne moduły - pliki programistyczne.

%package -n QtCore-static
Summary:	Core classes used by other modules - static libraries
Summary(pl.UTF-8):	Podstawowe klasy używane przez inne moduły - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}

%description -n QtCore-static
Core classes used by other modules - static libraries.

%description -n QtCore-static -l pl.UTF-8
Podstawowe klasy używane przez inne moduły - biblioteki statyczne.

%package -n QtDBus
Summary:	Classes for D-BUS support
Summary(pl.UTF-8):	Klasy do obsługi D-BUS
Group:		X11/Libraries
Requires:	QtXml = %{version}-%{release}

%description -n QtDBus
This module provides classes for D-BUS support. D-BUS is an
Inter-Process Communication (IPC) and Remote Procedure Calling (RPC)
mechanism originally developed for Linux to replace existing and
competing IPC solutions with one unified protocol.

%description -n QtDBus -l pl.UTF-8
Ten moduł udostępnia klasy do obsługi D-BUS. D-BUS to mechanizm
komunikacji między procesowej (IPC - Inter-Process Communication) i
zdalnego wywoływania procedur (RPC - Remote Procedure Calling)
stworzony początkowo dla Linuksa, aby zastąpić istniejące i
konkurujące ze sobą rozwiązania IPC jednym, ujednoliconym protokołem.

%package -n QtDBus-devel
Summary:	Classes for D-BUS support - development files
Summary(pl.UTF-8):	Klasy do obsługi D-BUS - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtDBus = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}
Requires:	dbus-devel
Requires:	glib2-devel >= 2.0.0

%description -n QtDBus-devel
Classes for D-BUS support - development files.

%description -n QtDBus-devel -l pl.UTF-8
Klasy do obsługi D-BUS - pliki programistyczne.

%package -n QtDBus-static
Summary:	Classes for D-BUS support - static libraries
Summary(pl.UTF-8):	Klasy do obsługi D-BUS - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtDBus-devel = %{version}-%{release}

%description -n QtDBus-static
Classes for D-BUS support - static libraries.

%description -n QtDBus-static -l pl.UTF-8
Klasy do obsługi D-BUS - biblioteki statyczne.

%package -n QtDesigner
Summary:	Classes for extending Qt Designer
Summary(pl.UTF-8):	Klasy do rozbudowy Qt Designera
Group:		X11/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}
Obsoletes:	qt4-designer-libs

%description -n QtDesigner
This module provides classes that allow you to create your own custom
widget plugins for Qt Designer, and classes that enable you to access
Qt Designer's components.

%description -n QtDesigner -l pl.UTF-8
Ten moduł dostarcza klasy, które pozwalają tworzyć własne wtyczki dla
Qt Designera oraz klasy, które umożliwiają dostęp do jego komponentów.

%package -n QtDesigner-devel
Summary:	Classes for extending Qt Designer - development files
Summary(pl.UTF-8):	Klasy do rozbudowy Qt Designera - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtDesigner = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtScript-devel = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtDesigner-devel
Classes for extending Qt Designer - development files.

%description -n QtDesigner-devel -l pl.UTF-8
Klasy do rozbudowy Qt Designera - pliki programistyczne.

%package -n QtDesigner-static
Summary:	Classes for extending Qt Designer - static libraries
Summary(pl.UTF-8):	Klasy do rozbudowy Qt Designera - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtDesigner-devel = %{version}-%{release}

%description -n QtDesigner-static
Classes for extending Qt Designer - static libraries.

%description -n QtDesigner-static -l pl.UTF-8
Klasy do rozbudowy Qt Designera - biblioteki statyczne.

%package -n QtGui
Summary:	Graphical User Interface components
Summary(pl.UTF-8):	Komponenty graficznego interfejsu użytkownika
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
# two following because of some plugins
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}

%description -n QtGui
Graphical User Interface components.

%description -n QtGui -l pl.UTF-8
Komponenty graficznego interfejsu użytkownika.

%package -n QtGui-devel
Summary:	Graphical User Interface components - development files
Summary(pl.UTF-8):	Komponenty graficznego interfejsu użytkownika - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	fontconfig-devel
Requires:	freetype-devel >= 1:2.0.0
Requires:	libpng-devel >= 2:1.0.8
Requires:	xorg-lib-libSM-devel
Requires:	xorg-lib-libXcursor-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXfixes-devel
Requires:	xorg-lib-libXi-devel
Requires:	xorg-lib-libXinerama-devel
Requires:	xorg-lib-libXrandr-devel
Requires:	xorg-lib-libXrender-devel

%description -n QtGui-devel
Graphical User Interface components - development files.

%description -n QtGui-devel -l pl.UTF-8
Komponenty graficznego interfejsu użytkownika - pliki programistyczne.

%package -n QtGui-static
Summary:	Graphical User Interface components - static libraries
Summary(pl.UTF-8):	Komponenty graficznego interfejsu użytkownika - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}

%description -n QtGui-static
Graphical User Interface components - static libraries.

%description -n QtGui-static -l pl.UTF-8
Komponenty graficznego interfejsu użytkownika - biblioteki statyczne.

%package -n QtHelp
Summary:	Classes for integrating online documentation in applications
Summary(pl.UTF-8):	Klasy do integracji dokumentacji w aplikacjach
Group:		X11/Libraries
Requires:	QtGui = %{version}-%{release}

%description -n QtHelp
QtHelp module includes tools for generating and viewing Qt help files.
In addition it provides classes for accessing help contents
programatically to be able to integrate online help into Qt
applications.

%description -n QtHelp -l pl.UTF-8
Moduł QtHelp zawiera narzędzia do generowania i przeglądania plików
pomocy Qt. Oprócz tego udostępnia klasy pozwalające na programowy
dostęp do zawartości dokumentacji w celu integracji pomocy w
aplikacjach Qt.

%package -n QtHelp-devel
Summary:	Classes for integrating online documentation in applications - development files
Summary(pl.UTF-8):	Klasy do integracji dokumentacji w aplikacjach - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCLucene-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtHelp = %{version}-%{release}
Requires:	QtSql-devel = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtHelp-devel
Classes for integrating online documentation in applications -
development files.

%description -n QtHelp-devel -l pl.UTF-8
Klasy do integracji dokumentacji w aplikacjach - pliki
programistyczne.

%package -n QtHelp-static
Summary:	Classes for integrating online documentation in applications - static library
Summary(pl.UTF-8):	Klasy do integracji dokumentacji w aplikacjach - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtHelp-devel = %{version}-%{release}

%description -n QtHelp-static
Classes for integrating online documentation in applications - static
library.

%description -n QtHelp-static -l pl.UTF-8
Klasy do integracji dokumentacji w aplikacjach - biblioteka statyczna.

%package -n QtMultimedia
Summary:	Classes for multimedia programming
Summary(pl.UTF-8):	Klasy do programowania multimediów
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtMultimedia
Classes for multimedia programming.

%description -n QtMultimedia -l pl.UTF-8
Klasy do programowania multimediów.

%package -n QtMultimedia-devel
Summary:	Classes for multimedia programming - development files
Summary(pl.UTF-8):	Klasy do programowania multimediów - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}

%description -n QtMultimedia-devel
Classes for multimedia programming - development files.

%description -n QtMultimedia-devel -l pl.UTF-8
Klasy do programowania multimediów - pliki programistyczne.

%package -n QtMultimedia-static
Summary:       Classes for multimedia programming - static libraries
Summary(pl.UTF-8):     Klasy do programowania multimediów - biblioteki statyczne
Group:         X11/Development/Libraries
Requires:      QtNetwork-devel = %{version}-%{release}

%description -n QtMultimedia-static
Classes for multimedia programming - static libraries.

%description -n QtMultimedia-static -l pl.UTF-8
Klasy do programowania multimediów - biblioteki statyczne.

%package -n QtNetwork
Summary:	Classes for network programming
Summary(pl.UTF-8):	Klasy do programowania sieciowego
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtNetwork
Classes for network programming.

%description -n QtNetwork -l pl.UTF-8
Klasy do programowania sieciowego.

%package -n QtNetwork-devel
Summary:	Classes for network programming - development files
Summary(pl.UTF-8):	Klasy do programowania sieciowego - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}

%description -n QtNetwork-devel
Classes for network programming - development files.

%description -n QtNetwork-devel -l pl.UTF-8
Klasy do programowania sieciowego - pliki programistyczne.

%package -n QtNetwork-static
Summary:	Classes for network programming - static libraries
Summary(pl.UTF-8):	Klasy do programowania sieciowego - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtNetwork-devel = %{version}-%{release}

%description -n QtNetwork-static
Classes for network programming - static libraries.

%description -n QtNetwork-static -l pl.UTF-8
Klasy do programowania sieciowego - biblioteki statyczne.

%package -n QtOpenGL
Summary:	OpenGL support classes
Summary(pl.UTF-8):	Klasy wspomagające OpenGL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtOpenGL
OpenGL support classes.

%description -n QtOpenGL -l pl.UTF-8
Klasy wspomagające OpenGL.

%package -n QtOpenGL-devel
Summary:	OpenGL support classes - development files
Summary(pl.UTF-8):	Klasy wspomagające OpenGL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-GLU-devel
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}

%description -n QtOpenGL-devel
OpenGL support classes - development files.

%description -n QtOpenGL-devel -l pl.UTF-8
Klasy wspomagające OpenGL - pliki programistyczne.

%package -n QtOpenGL-static
Summary:	OpenGL support classes - static libraries
Summary(pl.UTF-8):	Klasy wspomagające OpenGL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtOpenGL-devel = %{version}-%{release}

%description -n QtOpenGL-static
OpenGL support classes - static libraries.

%description -n QtOpenGL-static -l pl.UTF-8
Klasy wspomagające OpenGL - biblioteki statyczne.

%package -n QtScript
Summary:	Classes for scripting applications
Summary(pl.UTF-8):	Klasy pozwalające dodać obsługę skryptów w aplikacjach
Group:		X11/Development/Libraries

%description -n QtScript
The QtScript module provides classes to handle scripts inside
applications.

%description -n QtScript -l pl.UTF-8
Ten moduł dostarcza klasy obsługujące języki skryptowe wewnątrz
aplikacji.

%package -n QtScript-devel
Summary:	Classes for scripting applications - development files
Summary(pl.UTF-8):	Klasy do obsługi skryptów wewnątrz aplikacji - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}

%description -n QtScript-devel
Classes for scriptin applications - development files.

%description -n QtScript-devel -l pl.UTF-8
Klasy do obsługi skryptów wewnątrz aplikacji - pliki programistyczne.

%package -n QtScript-static
Summary:	Classes for scripting applications - static library
Summary(pl.UTF-8):	Klasy pozwalające dodać obsługę skryptów w aplikacjach - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtScript-devel = %{version}-%{release}

%description -n QtScript-static
Classes for scripting applications - static library.

%description -n QtScript-static -l pl.UTF-8
Klasy pozwalające dodać obsługę skryptów w aplikacjach - biblioteka
statyczna.

%package -n QtScriptTools
Summary:	Classes for scripting applications
Summary(pl.UTF-8):	Klasy pozwalające dodać obsługę skryptów w aplikacjach
Group:		X11/Development/Libraries

%description -n QtScriptTools
The QtScriptTools module provides classes to handle scripts inside
applications.

%description -n QtScriptTools -l pl.UTF-8
Ten moduł dostarcza klasy obsługujące języki skryptowe wewnątrz
aplikacji.

%package -n QtScriptTools-devel
Summary:	Classes for scripting applications - development files
Summary(pl.UTF-8):	Klasy do obsługi skryptów wewnątrz aplikacji - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtScript-devel = %{version}-%{release}
Requires:	QtScriptTools = %{version}-%{release}

%description -n QtScriptTools-devel
Classes for scriptin applications - development files.

%description -n QtScriptTools-devel -l pl.UTF-8
Klasy do obsługi skryptów wewnątrz aplikacji - pliki programistyczne.

%package -n QtScriptTools-static
Summary:	Classes for scripting applications - static library
Summary(pl.UTF-8):	Klasy pozwalające dodać obsługę skryptów w aplikacjach - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtScriptTools-devel = %{version}-%{release}

%description -n QtScriptTools-static
Classes for scripting applications - static library.

%description -n QtScriptTools-static -l pl.UTF-8
Klasy pozwalające dodać obsługę skryptów w aplikacjach - biblioteka
statyczna.

%package -n QtSql
Summary:	Classes for database integration using SQL
Summary(pl.UTF-8):	Klasy do integracji z bazami danych przy użyciu SQL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtSql
Classes for database integration using SQL.

%description -n QtSql -l pl.UTF-8
Klasy do integracji z bazami danych przy użyciu SQL.

%package -n QtSql-devel
Summary:	Classes for database integration using SQL - development files
Summary(pl.UTF-8):	Klasy do integracji z bazami danych przy użyciu SQL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}

%description -n QtSql-devel
Classes for database integration using SQL - development files.

%description -n QtSql-devel -l pl.UTF-8
Klasy do integracji z bazami danych przy użyciu SQL - pliki
programistyczne.

%package -n QtSql-static
Summary:	Classes for database integration using SQL - static libraries
Summary(pl.UTF-8):	Klasy do integracji z bazami danych przy użyciu SQL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtSql-devel = %{version}-%{release}

%description -n QtSql-static
Classes for database integration using SQL - static libraries.

%description -n QtSql-static -l pl.UTF-8
Klasy do integracji z bazami danych przy użyciu SQL - biblioteki
statyczne. programistyczne.

%package -n QtSql-ibase
Summary:	Database plugin for InterBase/Firebird Qt support
Summary(pl.UTF-8):	Wtyczka InterBase/Firebird do Qt
Summary(pt_BR.UTF-8):	Plugin de suporte a InterBase/Firebird para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-ibase
This package contains a plugin for accessing Interbase/Firebird
database via the QSql classes.

%description -n QtSql-ibase -l pl.UTF-8
Ten pakiet zawiera wtyczki do Qt umożliwiające korzystanie z baz
danych Interbase/Firebird poprzez klasy QSql.

%description -n QtSql-ibase -l pt_BR.UTF-8
Plugin de suporte a InterBase/Firebird para Qt.

%package -n QtSql-mysql
Summary:	Database plugin for MySQL Qt support
Summary(pl.UTF-8):	Wtyczka MySQL do Qt
Summary(pt_BR.UTF-8):	Plugin de suporte a MySQL para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-mysql
This package contains a plugin for accessing MySQL database via the
QSql classes.

%description -n QtSql-mysql -l pl.UTF-8
Ten pakiet zawiera wtyczki do Qt umożliwiające korzystanie z baz
danych MySQL poprzez klasy QSql.

%description -n QtSql-mysql -l pt_BR.UTF-8
Plugin de suporte a MySQL para Qt.

%package -n QtSql-odbc
Summary:	Database plugin for ODBC Qt support
Summary(pl.UTF-8):	Wtyczka ODBC do Qt
Summary(pt_BR.UTF-8):	Plugin de suporte a ODBC para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-odbc
This package contains a plugin for accessing unixODBC services via the
QSql classes.

%description -n QtSql-odbc -l pl.UTF-8
Ten pakiet zawiera wtyczki do Qt umożliwiające korzystanie z usług
unixODBC poprzez klasy QSql.

%description -n QtSql-odbc -l pt_BR.UTF-8
Plugin de suporte a ODBC para Qt.

%package -n QtSql-pgsql
Summary:	Database plugin for PostgreSQL Qt support
Summary(pl.UTF-8):	Wtyczka PostgreSQL do Qt
Summary(pt_BR.UTF-8):	Plugin de suporte a PostgreSQL para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-pgsql
This package contains a plugin for accessing PostgreSQL database via
the QSql classes.

%description -n QtSql-pgsql -l pl.UTF-8
Ten pakiet zawiera wtyczki do Qt umożliwiające korzystanie z baz
danych PostgreSQL poprzez klasy QSql.

%description -n QtSql-pgsql -l es.UTF-8
Plugin de suporte a PostgreSQL para Qt.

%package -n QtSql-sqlite
Summary:	Database plugin for SQLite 2.x Qt support
Summary(pl.UTF-8):	Wtyczka SQLite 2.x do Qt
Summary(pt_BR.UTF-8):	Plugin de suporte a SQLite 2.x para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-sqlite
This package contains a plugin for using the SQLite 2.x library (which
allows to acces virtually any SQL database) via the QSql classes.

%description -n QtSql-sqlite -l pl.UTF-8
Ten pakiet zawiera wtyczki do Qt umożliwiające korzystanie z baz
danych SQLite 2.x poprzez klasy QSql.

%description -n QtSql-sqlite -l pt_BR.UTF-8
Plugin de suporte a SQLite 2.x para Qt.

%package -n QtSql-sqlite3
Summary:	Database plugin for SQLite3 Qt support
Summary(pl.UTF-8):	Wtyczka SQLite3 do Qt
Summary(pt_BR.UTF-8):	Plugin de suporte a SQLite3 para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-sqlite3
This package contains a plugin for using the SQLite3 library (which
allows to acces virtually any SQL database) via the QSql classes.

%description -n QtSql-sqlite3 -l pl.UTF-8
Ten pakiet zawiera wtyczki do Qt umożliwiające korzystanie z baz
danych SQLite3 poprzez klasy QSql.

%description -n QtSql-sqlite3 -l pt_BR.UTF-8
Plugin de suporte a SQLite3 para Qt.

%package -n QtSql-tds
Summary:	Database plugin for TDS Qt support
Summary(pl.UTF-8):	Wtyczka TDS do Qt
Summary(pt_BR.UTF-8):	Plugin de suporte a TDS para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-tds
This package contains a plugin for accessing TDS database via the QSql
classes.

%description -n QtSql-tds -l pl.UTF-8
Ten pakiet zawiera wtyczki do Qt umożliwiające korzystanie z baz
danych TDS poprzez klasy QSql.

%description -n QtSql-tds -l pt_BR.UTF-8
Plugin de suporte a TDS para Qt.

%package -n QtSvg
Summary:	SVG support
Summary(pl.UTF-8):	Wsparcie dla SVG
Group:		X11/Libraries
Requires:	QtXml = %{version}-%{release}

%description -n QtSvg
SVG support.

%description -n QtSvg -l pl.UTF-8
Wsparcie dla SVG.

%package -n QtSvg-devel
Summary:	SVG support - development files
Summary(pl.UTF-8):	Wsparcie dla SVG - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtSvg = %{version}-%{release}

%description -n QtSvg-devel
SVG support - development files.

%description -n QtSvg-devel -l pl.UTF-8
Wsparcie dla SVG - pliki programistyczne.

%package -n QtSvg-static
Summary:	SVG support - static libraries
Summary(pl.UTF-8):	Wsparcie dla SVG - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtSvg-devel = %{version}-%{release}

%description -n QtSvg-static
SVG support - static libraries.

%description -n QtSvg-static -l pl.UTF-8
Wsparcie dla SVG - biblioteki statyczne.

%package -n QtTest
Summary:	Test framework
Summary(pl.UTF-8):	Szkielet testów
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtTest
Test framework.

%description -n QtTest -l pl.UTF-8
Szkielet testów.

%package -n QtTest-devel
Summary:	Test framework - development files
Summary(pl.UTF-8):	Szkielet testów - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtTest = %{version}-%{release}

%description -n QtTest-devel
Test framework - development files.

%description -n QtTest-devel -l pl.UTF-8
Szkielet testów - pliki programistyczne.

%package -n QtTest-static
Summary:	Test framework - static libraries
Summary(pl.UTF-8):	Szkielet testów - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtTest-devel = %{version}-%{release}

%description -n QtTest-static
Test framework - static libraries.

%description -n QtTest-static -l pl.UTF-8
Szkielet testów - biblioteki statyczne.

%package -n QtUiTools
Summary:	Classes for handling Qt Designer forms in applications
Summary(pl.UTF-8):	Klasy do obsługi formularzy Qt Designera w aplikacjach
Group:		X11/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n QtUiTools
The QtUiTools module provides classes to handle forms created with Qt
Designer.

%description -n QtUiTools -l pl.UTF-8
Moduł QtUiTools udostępnia klasy do obsługi formularzy tworzonych przy
użyciu Qt Designera.

%package -n QtUiTools-devel
Summary:	Classes for handling Qt Designer forms in applications - development files
Summary(pl.UTF-8):	Klasy do obsługi formularzy Qt Designera w aplikacjach - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtUiTools = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtUiTools-devel
Classes for handling Qt Designer forms in applications - development
files.

%description -n QtUiTools-devel -l pl.UTF-8
Klasy do obsługi formularzy Qt Designera w aplikacjach - pliki
programistyczne.

%package -n QtUiTools-static
Summary:	Classes for handling Qt Designer forms in applications - static library
Summary(pl.UTF-8):	Klasy do obsługi formularzy Qt Designera w aplikacjach - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtUiTools-devel = %{version}-%{release}

%description -n QtUiTools-static
Classes for handling Qt Designer forms in applications - static
library.

%description -n QtUiTools-static -l pl.UTF-8
Klasy do obsługi formularzy Qt Designera w aplikacjach - biblioteka
statyczna.

%package -n QtWebKit
Summary:	Classes for rendering HTML, XHTML and SVG documents
Summary(pl.UTF-8):	Klasy do renderowania dokumentów HTML, XHTML i SVG
Group:		X11/Libraries
Requires:	QtGui = %{version}-%{release}

%description -n QtWebKit
QtWebKit provides a Web browser engine that makes it easy to embed
content from the World Wide Web into your Qt application. At the same
time Web content can be enhanced with native controls. QtWebKit
provides facilities for rendering of HyperText Markup Language (HTML),
Extensible HyperText Markup Language (XHTML) and Scalable Vector
Graphics (SVG) documents, styled using Cascading Style Sheets (CSS)
and scripted with JavaScript.

%description -n QtWebKit -l pl.UTF-8
QtWebKit udostępnia silnik przeglądarki WWW ułatwiający osadzanie
treści ze stron WWW w aplikacjach Qt. Jednocześnie treść WWW może być
rozszerzana o natywne kontrolki. QtWebKit zapewnia renderowanie
dokumentów w językach HTML (HyperText Markup Language), XHTML
(Extensible HyperText Markup Language) i SVG (Scalable Vector
Graphics) z obsługą styli CSS (Cascading Style Sheets) i skryptów w
języku JavaScript.

%package -n QtWebKit-devel
Summary:	Classes for rendering HTML, XHTML and SVG documents - development files
Summary(pl.UTF-8):	Klasy do renderowania dokumentów HTML, XHTML i SVG - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtNetwork-devel = %{version}-%{release}
Requires:	QtScript-devel = %{version}-%{release}
Requires:	QtWebKit = %{version}-%{release}
%if %{with system_phonon}
Requires:	phonon-devel
%else
Requires:	qt4-phonon-devel = %{version}-%{release}
%endif

%description -n QtWebKit-devel
Classes for rendering HTML, XHTML and SVG documents - development
files.

%description -n QtWebKit-devel -l pl.UTF-8
Klasy do renderowania dokumentów HTML, XHTML i SVG - pliki
programistyczne.

%package -n QtWebKit-static
Summary:	Classes for rendering HTML, XHTML and SVG documents - static library
Summary(pl.UTF-8):	Klasy do renderowania dokumentów HTML, XHTML i SVG - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtWebKit-devel = %{version}-%{release}

%description -n QtWebKit-static
Classes for rendering HTML, XHTML and SVG documents - static library.

%description -n QtWebKit-static -l pl.UTF-8
Klasy do renderowania dokumentów HTML, XHTML i SVG - biblioteka
statyczna.

%package -n QtXml
Summary:	Classes for handling XML
Summary(pl.UTF-8):	Klasy do obsługi XML-a
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtXml
Classes for handling XML.

%description -n QtXml -l pl.UTF-8
Klasy do obsługi XML-a.

%package -n QtXml-devel
Summary:	Classes for handling XML - development files
Summary(pl.UTF-8):	Klasy do obsługi XML-a - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n QtXml-devel
Classes for handling XML - development files.

%description -n QtXml-devel -l pl.UTF-8
Klasy do obsługi XML-a - pliki programistyczne.

%package -n QtXml-static
Summary:	Classes for handling XML - static libraries
Summary(pl.UTF-8):	Klasy do obsługi XML-a - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtXml-static
Classes for handling XML - static libraries.

%description -n QtXml-static -l pl.UTF-8
Klasy do obsługi XML-a - biblioteki statyczne.

%package -n QtXmlPatterns
Summary:	QtXmlPatterns XQuery engine
Summary(pl.UTF-8):	Silnik zapytan XQuery QtXmlPatterns
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtXmlPatterns
QtXmlPatterns XQuery engine.

%description -n QtXmlPatterns -l pl.UTF-8
Silnik zapytan XQuery QtXmlPatterns.

%package -n QtXmlPatterns-devel
Summary:	QtXmlPatterns XQuery engine - development files
Summary(pl.UTF-8):	Silnik zapytan XQuery QtXmlPatterns - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtNetwork-devel = %{version}-%{release}
Requires:	QtXmlPatterns = %{version}-%{release}

%description -n QtXmlPatterns-devel
QtXmlPatterns XQuery engine - development files.

%description -n QtXmlPatterns-devel -l pl.UTF-8
Silnik zapytan XQuery QtXmlPatterns - pliki programistyczne.

%package -n QtXmlPatterns-static
Summary:	QtXmlPatterns XQuery engine - static library
Summary(pl.UTF-8):	Silnik zapytan XQuery QtXmlPatterns - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtXmlPatterns-devel = %{version}-%{release}

%description -n QtXmlPatterns-static
QtXmlPatterns XQuery engine - static library.

%description -n QtXmlPatterns-static -l pl.UTF-8
Silnik zapytan XQuery QtXmlPatterns - biblioteka statyczna.

%package assistant
Summary:	Qt documentation browser
Summary(pl.UTF-8):	Przeglądarka dokumentacji Qt
Group:		X11/Development/Tools
Requires:	%{name}-doc = %{version}-%{release}
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtDBus = %{version}-%{release}

%description assistant
Qt Assistant is a tool for browsing on-line documentation with
indexing, bookmarks and full-text search.

%description assistant -l pl.UTF-8
Qt Assistant to narzędzie do przeglądania dokumentacji z możliwością
indeksowania, dodawania zakładek i pełnotekstowego wyszukiwania.

%package build
Summary:	Build tools for Qt4
Summary(pl.UTF-8):	Narzędzia do budowania dla Qt4
Group:		X11/Development/Tools
Requires:	QtCore = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) and qt3to4 include names
converter.

%description build -l pl.UTF-8
Ten pakiet zawiera kompilator zasobów Qt (rcc), kompilator
metaobiektów (moc), kompilator interfejsów użytkownika (uic) oraz
konwerter nazw plików nagłówkowych qt3to4.

%package designer
Summary:	IDE used for GUI designing with Qt library
Summary(pl.UTF-8):	IDE służące do projektowania GUI za pomocą biblioteki Qt
Group:		X11/Applications
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtDesigner = %{version}-%{release}

%description designer
An advanced tool used for GUI designing with Qt library.

%description designer -l pl.UTF-8
Zaawansowane narzędzie służące do projektowania interfejsu graficznego
za pomocą biblioteki Qt.

%package linguist
Summary:	Translation helper for Qt
Summary(pl.UTF-8):	Aplikacja ułatwiająca tłumaczenie aplikacji oparty o Qt
Group:		X11/Development/Tools
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtUiTools = %{version}-%{release}

%description linguist
This program provides an interface that shortens and helps systematize
the process of translating GUIs. Qt Linguist takes all of the text of
a UI that will be shown to the user, and presents it to a human
translator in a simple window. When one UI text is translated, the
program automatically progresses to the next, until they are all
completed.

%description linguist -l pl.UTF-8
Ten program oferuje interfejs znacznie przyśpieszający proces
tłumaczenia interfejsu użytkownika. Zbiera wszystkie teksty
przeznaczone do tłumaczenia i przedstawia w łatwym w obsłudze oknie.
Gdy jeden z nich jest już przetłumaczony, automatycznie przechodzi do
następnego, aż wszystkie będą przetłumaczone.

%package phonon
Summary:	Cross-platform multimedia framework
Summary(pl.UTF-8):	Wieloplatformowy szkielet multimedialny
Group:		X11/Development/Tools
Obsoletes:	phonon

%description phonon
Phonon is a cross-platform multimedia framework that enables the use
of audio and video content in Qt applications.

%description phonon -l pl.UTF-8
Phonon to wieloplatformowy szkielet multimedialny pozwalający na
wykorzystywanie treści dźwiękowych i filmowych w aplikacjach Qt.

%package phonon-devel
Summary:	Cross-platform multimedia framework - development files
Summary(pl.UTF-8):	Wieloplatformowy szkielet multimedialny - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtDBus-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	qt4-phonon = %{version}-%{release}
Obsoletes:	phonon-devel

%description phonon-devel
Cross-platform multimedia framework - development files.

%description phonon-devel -l pl.UTF-8
Wieloplatformowy szkielet multimedialny - pliki programistyczne.

%package qmake
Summary:	Qt makefile generator
Summary(pl.UTF-8):	Generator plików makefile dla aplikacji Qt
Group:		X11/Development/Tools

%description qmake
A powerful makefile generator. It can create makefiles on any platform
from a simple .pro definitions file.

%description qmake -l pl.UTF-8
Rozbudowany generator plików makefile. Potrafi tworzyć pliki makefile
na każdej platformi na podstawie łatwego w przygotowaniu pliku .pro.

%package qtconfig
Summary:	Qt widgets configuration tool
Summary(pl.UTF-8):	Narzędzie do konfigurowania widgetów Qt
Group:		X11/Applications
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description qtconfig
A tool for configuring look and behavior of Qt widgets.

%description qtconfig -l pl.UTF-8
Narzędie do konfiguracji wyglądu i zachowania widgetów Qt.

%package -n qvfb
Summary:	Qt Virtual framebuffer
Summary(pl.UTF-8):	Wirtualny framebuffer dla Qt
Group:		X11/Development/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}

%description -n qvfb
Qt Virtual framebuffer allows you to run Qt/Embedded applications in X
window.

%description -n qvfb -l pl.UTF-8
Qt Virtual framebuffer pozwala na uruchamianie aplikacji Qt/Embedded w
okienku X.

%package demos
Summary:	Demos of new Qt4 features
Summary(pl.UTF-8):	Programy demonstrujące nowe możliwości Qt4
Group:		X11/Development/Libraries
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description demos
Demos are spiders that fly.

%description demos -l pl.UTF-8
Dema to latające pająki.

%package doc
Summary:	Qt Documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja Qt w formacie HTML
Group:		X11/Development/Libraries

%description doc
Qt documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja qt w formacie HTML.

%package examples
Summary:	Example programs bundled with Qt
Summary(pl.UTF-8):	Ćwiczenia i przykłady do Qt
Summary(pt_BR.UTF-8):	Programas exemplo desenvolvidos com o Qt
Group:		X11/Development/Libraries
# no it does not , we cant be sure the user wants to compile them right?
# he might just want to take a look, anwyay no single devel package now
#Requires:	%{name}-devel = %{version}-%{release}

%description examples
Example programs bundled with Qt version.

%description examples -l pl.UTF-8
Ćwiczenia/przykłady dołączone do Qt.

%description examples -l pt_BR.UTF-8
Programas exemplo para o Qt versão.

%prep
%setup -q -n qt-everywhere-opensource-src-%{version}-%{state}

%patch100 -p1

%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
#%patch8 -p1
%patch9 -p1

%{__sed} -i -e 's,usr/X11R6/,usr/g,' mkspecs/linux-g++-64/qmake.conf \
	mkspecs/common/linux.conf

# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|QMAKE_CC.*=.*gcc|QMAKE_CC\t\t= %{__cc}|;
	s|QMAKE_CXX.*=.*g++|QMAKE_CXX\t\t= %{__cxx}|;
	s|QMAKE_LINK.*=.*g++|QMAKE_LINK\t\t= %{__cxx}|;
	s|QMAKE_LINK_SHLIB.*=.*g++|QMAKE_LINK_SHLIB\t= %{__cxx}|;
	s|QMAKE_CFLAGS_RELEASE.*|QMAKE_CFLAGS_RELEASE\t+= %{rpmcppflags} %{rpmcflags}|;
	s|QMAKE_CXXFLAGS_RELEASE.*|QMAKE_CXXFLAGS_RELEASE\t+= %{rpmcppflags} %{rpmcxxflags}|;
	s|QMAKE_CFLAGS_DEBUG.*|QMAKE_CFLAGS_DEBUG\t+= %{debugcflags}|;
	s|QMAKE_CXXFLAGS_DEBUG.*|QMAKE_CXXFLAGS_DEBUG\t+= %{debugcflags}|;
	' mkspecs/common/g++.conf

%{__sed} -i -e '
	s|QMAKE_INCDIR_QT.*|QMAKE_INCDIR_QT       = %{_includedir}/qt4|;
	' mkspecs/common/linux.conf

# No -L/usr/lib.
%{__sed} -i -e '
	s|^QMAKE_LIBDIR_QT.*=.*|QMAKE_LIBDIR_QT       =|;
	' mkspecs/common/linux.conf

# undefine QMAKE_STRIP, so we get useful -debuginfo pkgs
%{__sed} -i -e '
	s|^QMAKE_STRIP.*=.*|QMAKE_STRIP             =|;
	' mkspecs/common/linux.conf

%build
# pass OPTFLAGS to build qmake itself with optimization
export OPTFLAGS="%{rpmcflags}"
export PATH=$PWD/bin:$PATH

##################################
# DEFAULT OPTIONS FOR ALL BUILDS #
##################################

COMMONOPT=" \
	-DQT_CLEAN_NAMESPACE \
	-buildkey pld \
	-verbose \
	-prefix %{_qtdir} \
	-bindir %{_qtdir}/bin \
	-docdir %{_docdir}/%{name}-doc \
	-headerdir %{_includedir}/qt4 \
	-libdir %{_libdir} \
	-L%{_libdir} \
	-plugindir %{_qtdir}/plugins \
	-datadir %{_datadir}/qt4 \
	-translationdir %{_datadir}/locale/ \
	-sysconfdir %{_sysconfdir}/qt4 \
	-examplesdir %{_examplesdir}/qt4 \
	-demosdir %{_examplesdir}/qt4-demos \
	-fast \
	-glib \
	%{!?with_gtk:-no-gtkstyle} \
	-%{!?with_pch:no-}pch \
	-no-rpath \
	%{!?with_sse:-no-sse} \
	%{!?with_sse2:-no-sse2} \
	-qdbus \
	-qt-gif \
	-reduce-relocations \
	-system-libjpeg \
	-system-libmng \
	-system-libpng \
	-system-zlib \
	-exceptions \
	-largefile \
	-I/usr/include/postgresql/server \
	-I/usr/include/mysql \
	%{?with_cups:-cups} \
	%{?with_nas:-system-nas-sound} \
	%{?debug:-debug} \
	%{!?debug:-release} \
	-qt3support \
	-fontconfig \
	-iconv \
	-no-separate-debug-info \
	-xfixes \
	-nis \
	-sm \
	-xcursor \
	-xinput \
	-xkb \
	-xrender \
	-xshape \
	-xmlpatterns \
	-continue"

##################################
#	  STATIC MULTI-THREAD	   #
##################################

%if %{with static_libs}
OPT=" \
	-%{!?with_mysql:no}%{?with_mysql:qt}-sql-mysql \
	-%{!?with_odbc:no}%{?with_odbc:qt}-sql-odbc \
	-%{!?with_pgsql:no}%{?with_pgsql:qt}-sql-psql \
	-%{!?with_sqlite3:no}%{?with_sqlite3:qt}-sql-sqlite \
	-%{!?with_sqlite:no}%{?with_sqlite:qt}-sql-sqlite2 \
	-%{!?with_ibase:no}%{?with_ibase:qt}-sql-ibase \
	-static"

echo "o
yes" | ./configure $COMMONOPT $OPT

%{__make} -C src
%{__make} -C tools/assistant/lib
%{__make} -C tools/designer
if [ ! -d staticlib ]; then
	mkdir staticlib
	cp -a lib/*.a staticlib
fi
%{__make} distclean
%endif

##################################
#	  SHARED MULTI-THREAD	   #
##################################

OPT=" \
	-%{!?with_mysql:no}%{?with_mysql:plugin}-sql-mysql \
	-%{!?with_odbc:no}%{?with_odbc:plugin}-sql-odbc \
	-%{!?with_pgsql:no}%{?with_pgsql:plugin}-sql-psql \
	-%{!?with_sqlite3:no}%{?with_sqlite3:plugin}-sql-sqlite \
	-%{!?with_sqlite:no}%{?with_sqlite:plugin}-sql-sqlite2 \
	-%{!?with_ibase:no}%{?with_ibase:plugin}-sql-ibase \
	-shared"

echo "o
yes" | ./configure $COMMONOPT $OPT

%{__make}
%{__make} \
	sub-tools-all-ordered \
	sub-demos-all-ordered \
	sub-examples-all-ordered

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_pkgconfigdir},%{_libdir}/qt4/tools/qdoc3}
install -d $RPM_BUILD_ROOT%{_qtdir}/plugins/{crypto,network}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# for qt-creator sth is messed up in the Makefile, nothing for make install
#install tools/qdoc3/qdoc3 $RPM_BUILD_ROOT%{_libdir}/qt4/tools/qdoc3

# kill -L/inside/builddir from *.la and *.pc (bug #77152)
%{__sed} -i -e "s,-L$PWD/lib,,g" $RPM_BUILD_ROOT%{_libdir}/*.{la,prl}
%{__sed} -i -e "s,-L$PWD/lib,,g" $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc
%{__sed} -i -e '
	s|moc_location=.*|moc_location=%{_bindir}/moc-qt4|;
	s|uic_location=.*|uic_location=%{_bindir}/uic-qt4|;
	' $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# install tools
install bin/findtr	$RPM_BUILD_ROOT%{_qtdir}/bin

cd $RPM_BUILD_ROOT%{_bindir}
ln -sf ../%{_lib}/qt4/bin/assistant assistant-qt4
ln -sf ../%{_lib}/qt4/bin/designer designer-qt4
ln -sf ../%{_lib}/qt4/bin/findtr findtr-qt4
ln -sf ../%{_lib}/qt4/bin/linguist linguist-qt4
ln -sf ../%{_lib}/qt4/bin/lrelease lrelease-qt4
ln -sf ../%{_lib}/qt4/bin/lupdate lupdate-qt4
ln -sf ../%{_lib}/qt4/bin/moc moc-qt4
ln -sf ../%{_lib}/qt4/bin/qmake qmake-qt4
ln -sf ../%{_lib}/qt4/bin/qtconfig qtconfig-qt4
ln -sf ../%{_lib}/qt4/bin/uic uic-qt4
ln -sf ../%{_lib}/qt4/bin/qt3to4 .
ln -sf ../%{_lib}/qt4/bin/rcc .
ln -sf ../%{_lib}/qt4/bin/uic3 .
ln -sf ../%{_lib}/qt4/bin/pixeltool .
ln -sf ../%{_lib}/qt4/bin/qdbus .
ln -sf ../%{_lib}/qt4/bin/qdbuscpp2xml .
ln -sf ../%{_lib}/qt4/bin/qdbusxml2cpp .
ln -sf ../%{_lib}/qt4/bin/qdbusviewer .
ln -sf ../%{_lib}/qt4/bin/qhelpconverter .
ln -sf ../%{_lib}/qt4/bin/qhelpgenerator .
ln -sf ../%{_lib}/qt4/bin/qvfb .
cd -

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/qtconfig-qt4.desktop
install tools/qtconfig/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qtconfig-qt4.png

install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}/linguist-qt4.desktop
install tools/linguist/linguist/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/linguist-qt4.png

install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/assistant-qt4.desktop

install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/designer-qt4.desktop
install tools/designer/src/designer/images/designer.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/designer-qt4.png

%if %{with static_libs}
install staticlib/*.a $RPM_BUILD_ROOT%{_libdir}
%endif

#
# Locale
#
for f in translations/*.ts ; do
	LD_LIBRARY_PATH=lib bin/lrelease $f -qm translations/$(basename $f .ts).qm
done

rm -f $RPM_BUILD_ROOT%{_datadir}/locale/*.qm
for file in translations/*.qm tools/assistant/*.qm tools/designer/designer/*.qm tools/linguist/linguist/*.qm; do
	[ ! -f $file ] && continue
	case "$file" in
		*untranslated*)
			continue;
			;;
	esac
	eval "`echo $file | sed -r 's:.*/([a-zA-Z]+(_[a-zA-Z]{3,}){0,1})_(((ja)_jp)|([a-z]{2}_[A-Z]{2,})|([a-z]{2}))\.qm$:MOD=\1 ; lang=\5\6\7:'`"
	[ "$lang" == "iw" ] && lang=he
	MOD=qt4-$MOD
	[ "$MOD" == "qt4-qt" ] && MOD=qt4
	install	-d $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES
	cp $file $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES/$MOD.qm
done

cd $RPM_BUILD_ROOT%{_includedir}/qt4/Qt
# QtCore must be the last
for f in ../Qt{3Support,Assistant,DBus,Designer,Gui,Help,Network,OpenGL,Script,Sql,Svg,Test,UiTools,WebKit,Xml,XmlPatterns,Core}/*; do
	if [ ! -d $f ]; then
		ln -sf $f `basename $f`
	fi
done
cd -

# Ship doc & qmake stuff
ln -s %{_docdir}/%{name}-doc $RPM_BUILD_ROOT%{_qtdir}/doc
ln -s %{_datadir}/qt4/mkspecs $RPM_BUILD_ROOT%{_qtdir}/mkspecs

for f in $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc; do
	HAVEDEBUG=`echo $f | grep _debug | wc -l`
	MODULE=`echo $f | basename $f | cut -d. -f1 | cut -d_ -f1`
	MODULE2=`echo $MODULE | tr a-z A-Z | sed s:QT::`
	DEFS="-D_REENTRANT"

	if [ "$MODULE2" == "3SUPPORT" ]; then
		DEFS="$DEFS -DQT3_SUPPORT -DQT_QT3SUPPORT_LIB"
	else
		DEFS="$DEFS -DQT_"$MODULE2"_LIB"
	fi
	[ "$HAVEDEBUG" -eq 0 ] && DEFS="$DEFS -DQT_NO_DEBUG"

	sed -i -e "s:-DQT_SHARED:-DQT_SHARED $DEFS:" $f
done

# Prepare some files list
ifecho() {
	RESULT=`echo $RPM_BUILD_ROOT$2 2>/dev/null`
	[ "$RESULT" == "" ] && return # XXX this is never true due $RPM_BUILD_ROOT being set
	r=`echo $RESULT | awk '{ print $1 }'`

	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or direcotry!"
		return 1
	fi
}

mkdevfl() {
	set -x
	MODULE=$1; shift
	echo "%%defattr(644,root,root,755)" > $MODULE-devel.files
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.so"
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.la"
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.prl"
	ifecho $MODULE-devel "%{_pkgconfigdir}/$MODULE*.pc"
	if [ -d "$RPM_BUILD_ROOT%{_includedir}/qt4/$MODULE" ]; then
		ifecho $MODULE-devel %{_includedir}/qt4/$MODULE
	fi
	for f in `find $RPM_BUILD_ROOT%{_includedir}/qt4/$MODULE -printf "%%P "`; do
		ifecho $MODULE-devel %{_includedir}/qt4/$MODULE/$f
		if [ -a "$RPM_BUILD_ROOT%{_includedir}/qt4/Qt/$f" ]; then
			ifecho $MODULE-devel %{_includedir}/qt4/Qt/$f
		fi
	done
	for f in $@; do ifecho $MODULE-devel $f; done
}

mkdevfl QtCore %{_includedir}/qt4 %{_includedir}/qt4/Qt
mkdevfl QtDBus %{_qtdir}/bin/qdbuscpp2xml %{_qtdir}/bin/qdbusxml2cpp %{_bindir}/qdbuscpp2xml %{_bindir}/qdbusxml2cpp
mkdevfl QtGui
mkdevfl QtMultimedia
mkdevfl QtNetwork
mkdevfl QtOpenGL
mkdevfl QtScript
mkdevfl QtScriptTools
mkdevfl QtSql
mkdevfl QtSvg
mkdevfl QtTest
mkdevfl QtHelp
mkdevfl QtWebKit
mkdevfl QtCLucene
mkdevfl QtXml
mkdevfl QtXmlPatterns
mkdevfl Qt3Support
mkdevfl phonon

# without *.la *.pc etc.
mkdevfl QtAssistant || /bin/true
mkdevfl QtDesigner || /bin/true
mkdevfl QtUiTools || /bin/true

# without glob (exclude QtScriptTools* QtXmlPatterns*)
%{__sed} -i 's,QtScript\*,QtScript,g' QtScript-devel.files
%{__sed} -i 's,QtXml\*,QtXml,g' QtXml-devel.files

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt4
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt4 -printf "%%P "`; do
	ifecho examples %{_examplesdir}/qt4/$f
done

echo "%defattr(644,root,root,755)" > demos.files
ifecho demos "%{_examplesdir}/qt4-demos"
ifecho demos "%{_qtdir}/bin/qtdemo"
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt4-demos -printf "%%P "`; do
	ifecho demos %{_examplesdir}/qt4-demos/$f
done

%if %{with system_phonon}
for a in $(sed -e '/%defattr/d;s/\(%dir\|%attr[^ ]\+\) //;' < phonon-devel.files); do
	rm -rf $RPM_BUILD_ROOT$a
done
rm -f $RPM_BUILD_ROOT%{_libdir}/libphonon.so.*
rm -f $RPM_BUILD_ROOT%{_libdir}/qt4/plugins/phonon_backend/libphonon_gstreamer.so
%endif

# check whether no other fixes are needed
mv $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP/LC_MESSAGES/*.* \
	$RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES/

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt3Support	-p /sbin/ldconfig
%postun	-n Qt3Support	-p /sbin/ldconfig

%post	-n QtAssistant	-p /sbin/ldconfig
%postun	-n QtAssistant	-p /sbin/ldconfig

%post	-n QtCLucene	-p /sbin/ldconfig
%postun	-n QtCLucene	-p /sbin/ldconfig

%post	-n QtCore	-p /sbin/ldconfig
%postun	-n QtCore	-p /sbin/ldconfig

%post	-n QtDBus	-p /sbin/ldconfig
%postun	-n QtDBus	-p /sbin/ldconfig

%post	-n QtDesigner	-p /sbin/ldconfig
%postun	-n QtDesigner	-p /sbin/ldconfig

%post	-n QtGui	-p /sbin/ldconfig
%postun	-n QtGui	-p /sbin/ldconfig

%post	-n QtHelp	-p /sbin/ldconfig
%postun	-n QtHelp	-p /sbin/ldconfig

%post	-n QtMultimedia	-p /sbin/ldconfig
%postun	-n QtMultimedia	-p /sbin/ldconfig

%post	-n QtNetwork	-p /sbin/ldconfig
%postun	-n QtNetwork	-p /sbin/ldconfig

%post	-n QtOpenGL	-p /sbin/ldconfig
%postun	-n QtOpenGL	-p /sbin/ldconfig

%post   -n QtScript	-p /sbin/ldconfig
%postun -n QtScript	-p /sbin/ldconfig

%post   -n QtScriptTools	-p /sbin/ldconfig
%postun -n QtScriptTools	-p /sbin/ldconfig

%post	-n QtSql	-p /sbin/ldconfig
%postun	-n QtSql	-p /sbin/ldconfig

%post	-n QtSvg	-p /sbin/ldconfig
%postun	-n QtSvg	-p /sbin/ldconfig

%post	-n QtTest	-p /sbin/ldconfig
%postun	-n QtTest	-p /sbin/ldconfig

%post	-n QtUiTools	-p /sbin/ldconfig
%postun	-n QtUiTools	-p /sbin/ldconfig

%post	-n QtWebKit	-p /sbin/ldconfig
%postun	-n QtWebKit	-p /sbin/ldconfig

%post	-n QtXml	-p /sbin/ldconfig
%postun	-n QtXml	-p /sbin/ldconfig

%post   -n QtXmlPatterns	-p /sbin/ldconfig
%postun -n QtXmlPatterns	-p /sbin/ldconfig

%post	phonon		-p /sbin/ldconfig
%postun	phonon		-p /sbin/ldconfig

%files -n Qt3Support
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt3Support.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt3Support.so.?

%files -n QtAssistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtAssistantClient.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtAssistantClient.so.?

%files -n QtCLucene
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtCLucene.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtCLucene.so.?

%files -n QtCore
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtCore.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtCore.so.?
%dir %{_qtdir}
%dir %{_qtdir}/bin
%dir %{_qtdir}/plugins
%dir %{_qtdir}/plugins/accessible
%dir %{_qtdir}/plugins/codecs
%dir %{_qtdir}/plugins/crypto
%dir %{_qtdir}/plugins/graphicssystems
%dir %{_qtdir}/plugins/iconengines
%dir %{_qtdir}/plugins/imageformats
%dir %{_qtdir}/plugins/inputmethods
%dir %{_qtdir}/plugins/network
%dir %{_qtdir}/plugins/sqldrivers
%dir %{_qtdir}/plugins/script
%dir %{_qtdir}/tools
%dir %{_datadir}/qt4
%lang(ar) %{_datadir}/locale/ar/LC_MESSAGES/qt4.qm
%lang(da) %{_datadir}/locale/da/LC_MESSAGES/qt4.qm
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt4.qm
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/qt4.qm
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/qt4.qm
%lang(he) %{_datadir}/locale/he/LC_MESSAGES/qt4.qm
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/qt4.qm
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4.qm
%lang(pt) %{_datadir}/locale/pt/LC_MESSAGES/qt4.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt4.qm
%lang(sk) %{_datadir}/locale/sk/LC_MESSAGES/qt4.qm
%lang(sl) %{_datadir}/locale/sl/LC_MESSAGES/qt4.qm
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/qt4.qm
%lang(uk) %{_datadir}/locale/uk/LC_MESSAGES/qt4.qm
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/qt4.qm
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/qt4.qm

%files -n QtDBus
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qdbus
%attr(755,root,root) %{_bindir}/qdbusviewer
%attr(755,root,root) %{_libdir}/libQtDBus.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtDBus.so.?
%attr(755,root,root) %{_qtdir}/bin/qdbus
%attr(755,root,root) %{_qtdir}/bin/qdbusviewer
# ?? is this the proper place?
%attr(755,root,root) %{_qtdir}/plugins/script/libqtscriptdbus.so

%files -n QtDesigner
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtDesigner.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtDesigner.so.?
%attr(755,root,root) %{_libdir}/libQtDesignerComponents.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtDesignerComponents.so.?
%dir %{_qtdir}/plugins/designer
%attr(755,root,root) %{_qtdir}/plugins/designer/*.so

%files -n QtGui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtGui.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtGui.so.?
%attr(755,root,root) %{_qtdir}/plugins/accessible/*.so
%attr(755,root,root) %{_qtdir}/plugins/codecs/*.so
%attr(755,root,root) %{_qtdir}/plugins/graphicssystems/*.so
%attr(755,root,root) %{_qtdir}/plugins/iconengines/*.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/*.so
%attr(755,root,root) %{_qtdir}/plugins/inputmethods/*.so

%files -n QtHelp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qhelpconverter
%attr(755,root,root) %{_bindir}/qhelpgenerator
%attr(755,root,root) %{_libdir}/libQtHelp.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtHelp.so.?
%attr(755,root,root) %{_qtdir}/bin/qhelpconverter
%attr(755,root,root) %{_qtdir}/bin/qhelpgenerator
%lang(da) %{_datadir}/locale/da/LC_MESSAGES/qt4-qt_help.qm
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt4-qt_help.qm
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/qt4-qt_help.qm
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4-qt_help.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt4-qt_help.qm
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/qt4-qt_help.qm
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/qt4-qt_help.qm

%files -n QtMultimedia
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtMultimedia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtMultimedia.so.?

%files -n QtNetwork
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtNetwork.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtNetwork.so.?

%files -n QtOpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtOpenGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtOpenGL.so.?

%files -n QtScript
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtScript.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtScript.so.?

%files -n QtScriptTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtScriptTools.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtScriptTools.so.?

%files -n QtSql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSql.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSql.so.?

%if %{with mysql}
%files -n QtSql-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlmysql.so
%endif

%if %{with pgsql}
%files -n QtSql-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlpsql.so
%endif

%if %{with sqlite}
%files -n QtSql-sqlite
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlite2.so
%endif

%if %{with sqlite3}
%files -n QtSql-sqlite3
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlite.so
%endif

%if %{with ibase}
%files -n QtSql-ibase
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlibase.so
%endif

%if %{with odbc}
%files -n QtSql-odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlodbc.so
%endif

%files -n QtSql-tds
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqltds.so

%files -n QtSvg
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSvg.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSvg.so.?

%files -n QtTest
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtTest.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtTest.so.?

%files -n QtUiTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtUiTools.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtUiTools.so.?

%files -n QtWebKit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtWebKit.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtWebKit.so.?

%files -n QtXml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtXml.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtXml.so.?

%files -n QtXmlPatterns
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/bin/xmlpatterns
%attr(755,root,root) %{_libdir}/libQtXmlPatterns.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtXmlPatterns.so.?

%files assistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pixeltool
%attr(755,root,root) %{_bindir}/assistant-qt4
%attr(755,root,root) %{_qtdir}/bin/pixeltool
%attr(755,root,root) %{_qtdir}/bin/qcollectiongenerator
%attr(755,root,root) %{_qtdir}/bin/assistant
%attr(755,root,root) %{_qtdir}/bin/assistant_adp
%lang(da) %{_datadir}/locale/da/LC_MESSAGES/qt4-assistant*.qm
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt4-assistant*.qm
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/qt4-assistant*.qm
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4-assistant*.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt4-assistant*.qm
%lang(zh_CN) %{_datadir}/locale/zh_*/LC_MESSAGES/qt4-assistant*.qm
%{_desktopdir}/assistant-qt4.desktop
#%{_pixmapsdir}/assistant-qt4.png

%files build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rcc
%attr(755,root,root) %{_bindir}/moc-qt4
%attr(755,root,root) %{_bindir}/qt3to4
%attr(755,root,root) %{_bindir}/uic-qt4
%attr(755,root,root) %{_qtdir}/bin/rcc
%attr(755,root,root) %{_qtdir}/bin/moc
%attr(755,root,root) %{_qtdir}/bin/qt3to4
%attr(755,root,root) %{_qtdir}/bin/uic
#%dir %{_libdir}/qt4/tools/qdoc3
#%attr(755,root,root) %{_libdir}/qt4/tools/qdoc3/qdoc3
%{_datadir}/qt4/q3porting.xml

%files designer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/designer-qt4
%attr(755,root,root) %{_qtdir}/bin/designer
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt4-designer.qm
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/qt4-designer.qm
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4-designer.qm
%lang(sl) %{_datadir}/locale/sl/LC_MESSAGES/qt4-designer.qm
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/qt4-designer.qm
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/qt4-designer.qm
%{_desktopdir}/designer-qt4.desktop
%{_pixmapsdir}/designer-qt4.png

%files linguist
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/findtr-qt4
%attr(755,root,root) %{_bindir}/linguist-qt4
%attr(755,root,root) %{_bindir}/lrelease-qt4
%attr(755,root,root) %{_bindir}/lupdate-qt4
%attr(755,root,root) %{_qtdir}/bin/findtr
%attr(755,root,root) %{_qtdir}/bin/linguist
%attr(755,root,root) %{_qtdir}/bin/lconvert
%attr(755,root,root) %{_qtdir}/bin/lrelease
%attr(755,root,root) %{_qtdir}/bin/lupdate
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt4-linguist.qm
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/qt4-linguist.qm
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/qt4-linguist.qm
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4-linguist.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt4-linguist.qm
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/qt4-linguist.qm
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/qt4-linguist.qm
%{_datadir}/qt4/phrasebooks
%{_desktopdir}/linguist-qt4.desktop
%{_pixmapsdir}/linguist-qt4.png

%if %{without system_phonon}
%files phonon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libphonon.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libphonon.so.?
%dir %{_qtdir}/plugins/phonon_backend
%attr(755,root,root) %{_qtdir}/plugins/phonon_backend/libphonon_gstreamer.so
%endif

%files qmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmake-qt4
%attr(755,root,root) %{_qtdir}/bin/qmake
%{_datadir}/qt4/mkspecs
%{_qtdir}/mkspecs

%files qtconfig
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qtconfig-qt4
%attr(755,root,root) %{_qtdir}/bin/qtconfig
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4-qtconfig.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt4-qtconfig.qm
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/qt4-qtconfig.qm
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/qt4-qtconfig.qm
%{_desktopdir}/qtconfig-qt4.desktop
%{_pixmapsdir}/qtconfig-qt4.png

%files -n qvfb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qvfb
%attr(755,root,root) %{_qtdir}/bin/qvfb
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4-qvfb.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt4-qvfb.qm
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/qt4-qvfb.qm
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/qt4-qvfb.qm

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc
%{_qtdir}/doc

%files -n QtCLucene-devel -f QtCLucene-devel.files
%defattr(644,root,root,755)

%files -n Qt3Support-devel -f Qt3Support-devel.files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uic3
%attr(755,root,root) %{_qtdir}/bin/uic3

%files -n QtAssistant-devel -f QtAssistant-devel.files
%defattr(644,root,root,755)

%files -n QtCore-devel -f QtCore-devel.files
%defattr(644,root,root,755)

%files -n QtDBus-devel -f QtDBus-devel.files
%defattr(644,root,root,755)

%files -n QtDesigner-devel -f QtDesigner-devel.files
%defattr(644,root,root,755)

%files -n QtGui-devel -f QtGui-devel.files
%defattr(644,root,root,755)

%files -n QtHelp-devel -f QtHelp-devel.files
%defattr(644,root,root,755)

%files -n QtMultimedia-devel -f QtMultimedia-devel.files
%defattr(644,root,root,755)

%files -n QtNetwork-devel -f QtNetwork-devel.files
%defattr(644,root,root,755)

%files -n QtOpenGL-devel -f QtOpenGL-devel.files
%defattr(644,root,root,755)

%files -n QtScript-devel -f QtScript-devel.files
%defattr(644,root,root,755)

%files -n QtScriptTools-devel -f QtScriptTools-devel.files
%defattr(644,root,root,755)

%files -n QtSql-devel -f QtSql-devel.files
%defattr(644,root,root,755)

%files -n QtSvg-devel -f QtSvg-devel.files
%defattr(644,root,root,755)

%files -n QtTest-devel -f QtTest-devel.files
%defattr(644,root,root,755)

%files -n QtUiTools-devel -f QtUiTools-devel.files
%defattr(644,root,root,755)

%files -n QtWebKit-devel -f QtWebKit-devel.files
%defattr(644,root,root,755)

%files -n QtXml-devel -f QtXml-devel.files
%defattr(644,root,root,755)

%files -n QtXmlPatterns-devel -f QtXmlPatterns-devel.files
%defattr(644,root,root,755)

%if %{without system_phonon}
%files phonon-devel -f phonon-devel.files
%defattr(644,root,root,755)
%endif

%if %{with static_libs}
%files -n Qt3Support-static
%defattr(644,root,root,755)
%{_libdir}/libQt3Support.a

#%files -n QtAssistant-static
#%defattr(644,root,root,755)
#%{_libdir}/libQtAssistantClient.a

#%files -n QtCLucene-static
#%defattr(644,root,root,755)
#%{_libdir}/libQtCLucene.a

%files -n QtCore-static
%defattr(644,root,root,755)
%{_libdir}/libQtCore.a

%files -n QtDBus-static
%defattr(644,root,root,755)
%{_libdir}/libQtDBus.a

%files -n QtDesigner-static
%defattr(644,root,root,755)
%{_libdir}/libQtDesigner.a
%{_libdir}/libQtDesignerComponents.a

%files -n QtGui-static
%defattr(644,root,root,755)
%{_libdir}/libQtGui.a

%files -n QtHelp-static
%defattr(644,root,root,755)
%{_libdir}/libQtHelp.a

%files -n QtMultimedia-static
%defattr(644,root,root,755)
%{_libdir}/libQtMultimedia.a

%files -n QtNetwork-static
%defattr(644,root,root,755)
%{_libdir}/libQtNetwork.a

%files -n QtOpenGL-static
%defattr(644,root,root,755)
%{_libdir}/libQtOpenGL.a

%files -n QtScript-static
%defattr(644,root,root,755)
%{_libdir}/libQtScript.a

%files -n QtScriptTools-static
%defattr(644,root,root,755)
%{_libdir}/libQtScriptTools.a

%files -n QtSql-static
%defattr(644,root,root,755)
%{_libdir}/libQtSql.a

%files -n QtSvg-static
%defattr(644,root,root,755)
%{_libdir}/libQtSvg.a

%files -n QtTest-static
%defattr(644,root,root,755)
%{_libdir}/libQtTest.a

%files -n QtUiTools-static
%defattr(644,root,root,755)
%{_libdir}/libQtUiTools.a

%files -n QtWebKit-static
%defattr(644,root,root,755)
%{_libdir}/libQtWebKit.a

%files -n QtXml-static
%defattr(644,root,root,755)
%{_libdir}/libQtXml.a

%files -n QtXmlPatterns-static
%defattr(644,root,root,755)
%{_libdir}/libQtXmlPatterns.a
%endif

%files demos -f demos.files
%defattr(644,root,root,755)

%files examples -f examples.files
%defattr(644,root,root,755)
