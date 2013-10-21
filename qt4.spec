#
# TODO:
#	- more cleanups
#	- check if translations are available
#	- check Qt ui tool
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_with	nas		# NAS audio support
%bcond_without	gtk		# GTK+ theme integration
%bcond_without	pch		# pch (pre-compiled headers) in qmake
%bcond_without	system_phonon	# phonon libraries from phonon.spec intead of qt4.spec
%bcond_with	wkhtml		# WKHTMLTOPDF patch (affects QtGui ABI)
# -- databases
%bcond_without	mysql		# MySQL plugin
%bcond_without	odbc		# unixODBC plugin
%bcond_without	pgsql		# PostgreSQL plugin
%bcond_without	sqlite3		# SQLite3 plugin
%bcond_without	sqlite		# SQLite2 plugin
%bcond_without	ibase		# ibase (InterBase/Firebird) plugin
# -- SIMD CPU instructions
%bcond_with	mmx		# use MMX instructions
%bcond_with	3dnow		# use 3Dnow instructions
%bcond_with	sse		# use SSE instructions in gui/painting module
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions (since: Intel middle Pentium4, AMD Athlon64)
%bcond_with	ssse3		# use SSSE3 instructions (Intel since Core2, Via Nano)
%bcond_with	sse41		# use SSE4.1 instructions (Intel since middle Core2)
%bcond_with	sse42		# use SSE4.2 instructions (the same)
%bcond_with	avx		# use AVX instructions (future Intel x86 CPUs only)

%ifnarch %{ix86} %{x8664} sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%ifarch	athlon
%define		with_3dnow	1
%endif
%ifarch athlon pentium3 pentium4 %{x8664}
%define		with_mmx	1
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

%define		icu_abi		52
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

Summary:	The Qt GUI application framework
Summary(es.UTF-8):	Biblioteca para ejecutar aplicaciones GUI Qt
Summary(pl.UTF-8):	Biblioteka Qt do tworzenia GUI
Summary(pt_BR.UTF-8):	Estrutura para rodar aplicações GUI Qt
Name:		qt4
Version:	4.8.5
Release:	2
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/4.8/%{version}/qt-everywhere-opensource-src-%{version}.tar.gz
# Source0-md5:	1864987bdbb2f58f8ae8b350dfdbe133
Source2:	%{name}-qtconfig.desktop
Source3:	%{name}-designer.desktop
Source4:	%{name}-assistant.desktop
Source5:	%{name}-linguist.desktop

# git clone git://gitorious.org/+kde-developers/qt/kde-qt.git
# git checkout -b 4.7.1-patched origin/4.7.1-patched
# git diff v4.7.1..4.7.1-patched > ~/rpm/packages/qt4/qt4-kde-git.patch
Patch100:	%{name}-kde-git.patch

Patch0:		%{name}-tools.patch
Patch1:		%{name}-qt_copy.patch
Patch2:		%{name}-buildsystem.patch
Patch3:		%{name}-locale.patch
Patch5:		%{name}-support-cflags-with-commas.patch
Patch6:		%{name}-build-lib-static.patch
Patch7:		%{name}-x11_fonts.patch
Patch8:		%{name}-ibase.patch
Patch9:		qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch
Patch10:	webkit-no_Werror.patch
Patch11:	%{name}-wkhtml.patch
Patch12:	fix-crash-in-assistant.patch
Patch13:	improve-cups-support.patch
# backported from Qt5 (essentially)
# http://bugzilla.redhat.com/702493
# https://bugreports.qt-project.org/browse/QTBUG-5545
Patch15:	qt-everywhere-opensource-src-4.8.4-qgtkstyle_disable_gtk_theme_check.patch
Patch16:	qt-everywhere-opensource-src-4.8.3-QTBUG-4862.patch
URL:		http://qt-project.org/
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	Mesa-libOpenVG-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	dbus-devel >= 0.93
BuildRequires:	fontconfig-devel
BuildRequires:	freetds-devel
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gstreamer0.10-plugins-base-devel
%{?with_gtk:BuildRequires:	gtk+2-devel >= 2:2.10}
# see dependency on libicu version below
BuildRequires:	libicu-devel >= %{icu_abi}
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel >= 1.0.0
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-backend-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	pulseaudio-devel >= 0.9.10
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	rsync
BuildRequires:	sed >= 4.0
%{?with_sqlite:BuildRequires:	sqlite-devel}
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.3.0}
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	zlib-devel
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
Summary:	Qt core classes used by other modules
Summary(pl.UTF-8):	Podstawowe klasy Qt używane przez inne moduły
Group:		X11/Libraries
%requires_eq_to	libicu libicu-devel
# be sure to depend on proper arch.
%ifarch %{x8664} ppc64 sparc64 s390x
Requires:	libicui18n.so.%{icu_abi}()(64bit)
%else
Requires:	libicui18n.so.%{icu_abi}
%endif
Obsoletes:	QtAssistant

%description -n QtCore
Qt core classes used by other modules.

%description -n QtCore -l pl.UTF-8
Podstawowe klasy Qt używane przez inne moduły.

%package -n QtCore-devel
Summary:	Qt core classes used by other modules - development files
Summary(pl.UTF-8):	Podstawowe klasy Qt używane przez inne moduły - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	glib2-devel
Requires:	libstdc++-devel
Requires:	zlib-devel
Obsoletes:	QtAssistant-devel

%description -n QtCore-devel
Qt core classes used by other modules - development files.

%description -n QtCore-devel -l pl.UTF-8
Podstawowe klasy Qt używane przez inne moduły - pliki programistyczne.

%package -n QtCore-static
Summary:	Qt core classes used by other modules - static libraries
Summary(pl.UTF-8):	Podstawowe klasy Qt używane przez inne moduły - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Obsoletes:	QtAssistant-static

%description -n QtCore-static
Qt core classes used by other modules - static libraries.

%description -n QtCore-static -l pl.UTF-8
Podstawowe klasy Qt używane przez inne moduły - biblioteki statyczne.

%package -n QtDBus
Summary:	Qt classes for D-BUS support
Summary(pl.UTF-8):	Klasy Qt do obsługi D-BUS
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}
# only for libqtscriptdbus plugin
Requires:	QtGui = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}

%description -n QtDBus
This module provides Qt classes for D-BUS support. D-BUS is an
Inter-Process Communication (IPC) and Remote Procedure Calling (RPC)
mechanism originally developed for Linux to replace existing and
competing IPC solutions with one unified protocol.

%description -n QtDBus -l pl.UTF-8
Ten moduł udostępnia klasy Qt do obsługi D-BUS. D-BUS to mechanizm
komunikacji między procesowej (IPC - Inter-Process Communication) i
zdalnego wywoływania procedur (RPC - Remote Procedure Calling)
stworzony początkowo dla Linuksa, aby zastąpić istniejące i
konkurujące ze sobą rozwiązania IPC jednym, ujednoliconym protokołem.

%package -n QtDBus-devel
Summary:	Qt classes for D-BUS support - development files
Summary(pl.UTF-8):	Klasy Qt do obsługi D-BUS - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtDBus = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtDBus-devel
Qt classes for D-BUS support - development files.

%description -n QtDBus-devel -l pl.UTF-8
Klasy Qt do obsługi D-BUS - pliki programistyczne.

%package -n QtDBus-static
Summary:	Qt classes for D-BUS support - static libraries
Summary(pl.UTF-8):	Klasy Qt do obsługi D-BUS - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtDBus-devel = %{version}-%{release}

%description -n QtDBus-static
Qt classes for D-BUS support - static libraries.

%description -n QtDBus-static -l pl.UTF-8
Klasy Qt do obsługi D-BUS - biblioteki statyczne.

%package -n QtDeclarative
Summary:	QtDeclarative - QML language engine library
Summary(pl.UTF-8):	QtDeclarative - biblioteka języka QML
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtSvg = %{version}-%{release}
Requires:	QtXmlPatterns = %{version}-%{release}
# for qmlwebkitplugin plugin
Requires:	QtWebKit = %{version}-%{release}

%description -n QtDeclarative
QtDeclarative is the QML language engine library. QML is a declarative
language oriented on JavaScript.

%description -n QtDeclarative -l pl.UTF-8
QtDeclarative to biblioteka języka QML. QML jest deklaratywnym
językiem zorientowanym na JavaScript.

%package -n QtDeclarative-devel
Summary:	Development files for QtDeclarative - QML language engine library
Summary(pl.UTF-8):	Pliki programistyczne QtDeclarative - biblioteki języka QML
Group:		X11/Development/Libraries
Requires:	QtDeclarative = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtNetwork-devel = %{version}-%{release}
Requires:	QtScript-devel = %{version}-%{release}

%description -n QtDeclarative-devel
Development files for QtDeclarative - QML language engine library.

%description -n QtDeclarative-devel -l pl.UTF-8
Pliki programistyczne QtDeclarative - biblioteki języka QML.

%package -n QtDeclarative-static
Summary:	Static version of QtDeclarative - QML language engine library
Summary(pl.UTF-8):	Statycza wersja QtDeclarative - biblioteki języka QML
Group:		X11/Development/Libraries
Requires:	QtDeclarative-devel = %{version}-%{release}

%description -n QtDeclarative-static
Static version of QtDeclarative - QML language engine library.

%description -n QtDeclarative-static -l pl.UTF-8
Statycza wersja QtDeclarative - biblioteki języka QML.

%package -n QtDesigner
Summary:	Classes for extending Qt Designer
Summary(pl.UTF-8):	Klasy do rozbudowy Qt Designera
Group:		X11/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}
# for plugins
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtDBus = %{version}-%{release}
Requires:	QtDeclarative = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtSvg = %{version}-%{release}
Requires:	QtWebKit = %{version}-%{release}
Requires:	QtXmlPatterns = %{version}-%{release}
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
Summary:	Qt Graphical User Interface components
Summary(pl.UTF-8):	Komponenty graficznego interfejsu użytkownika Qt
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
# for qtracegraphicssystem plugin
Requires:	QtNetwork = %{version}-%{release}

%description -n QtGui
Qt Graphical User Interface components.

%description -n QtGui -l pl.UTF-8
Komponenty graficznego interfejsu użytkownika Qt.

%package -n QtGui-devel
Summary:	Qt Graphical User Interface components - development files
Summary(pl.UTF-8):	Komponenty graficznego interfejsu użytkownika Qt - pliki programistyczne
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
Qt Graphical User Interface components - development files.

%description -n QtGui-devel -l pl.UTF-8
Komponenty graficznego interfejsu użytkownika Qt - pliki
programistyczne.

%package -n QtGui-static
Summary:	Qt Graphical User Interface components - static libraries
Summary(pl.UTF-8):	Komponenty graficznego interfejsu użytkownika Qt - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}

%description -n QtGui-static
Qt Graphical User Interface components - static libraries.

%description -n QtGui-static -l pl.UTF-8
Komponenty graficznego interfejsu użytkownika Qt - biblioteki
statyczne.

%package -n QtHelp
Summary:	Qt classes for integrating online documentation in applications
Summary(pl.UTF-8):	Klasy Qt do integracji dokumentacji w aplikacjach
Group:		X11/Libraries
Requires:	QtCLucene = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

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
Summary:	Qt classes for integrating online documentation in applications - development files
Summary(pl.UTF-8):	Klasy Qt do integracji dokumentacji w aplikacjach - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCLucene-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtHelp = %{version}-%{release}
Requires:	QtSql-devel = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtHelp-devel
Qt classes for integrating online documentation in applications -
development files.

%description -n QtHelp-devel -l pl.UTF-8
Klasy Qt do integracji dokumentacji w aplikacjach - pliki
programistyczne.

%package -n QtHelp-static
Summary:	Qt classes for integrating online documentation in applications - static library
Summary(pl.UTF-8):	Klasy Qt do integracji dokumentacji w aplikacjach - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtHelp-devel = %{version}-%{release}

%description -n QtHelp-static
Qt classes for integrating online documentation in applications -
static library.

%description -n QtHelp-static -l pl.UTF-8
Klasy Qt do integracji dokumentacji w aplikacjach - biblioteka
statyczna.

%package -n QtMultimedia
Summary:	Qt classes for multimedia programming
Summary(pl.UTF-8):	Klasy Qt do programowania multimediów
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}

%description -n QtMultimedia
Qt classes for multimedia programming.

%description -n QtMultimedia -l pl.UTF-8
Klasy Qt do programowania multimediów.

%package -n QtMultimedia-devel
Summary:	Qt classes for multimedia programming - development files
Summary(pl.UTF-8):	Klasy Qt do programowania multimediów - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtMultimedia = %{version}-%{release}

%description -n QtMultimedia-devel
Qt classes for multimedia programming - development files.

%description -n QtMultimedia-devel -l pl.UTF-8
Klasy Qt do programowania multimediów - pliki programistyczne.

%package -n QtMultimedia-static
Summary:	Qt classes for multimedia programming - static libraries
Summary(pl.UTF-8):	Klasy Qt do programowania multimediów - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtMultimedia-devel = %{version}-%{release}

%description -n QtMultimedia-static
Qt classes for multimedia programming - static libraries.

%description -n QtMultimedia-static -l pl.UTF-8
Klasy Qt do programowania multimediów - biblioteki statyczne.

%package -n QtNetwork
Summary:	Qt classes for network programming
Summary(pl.UTF-8):	Klasy Qt do programowania sieciowego
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
# the rest for qnmbearer plugin
Requires:	QtDBus = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n QtNetwork
Qt classes for network programming.

%description -n QtNetwork -l pl.UTF-8
Klasy Qt do programowania sieciowego.

%package -n QtNetwork-devel
Summary:	Qt classes for network programming - development files
Summary(pl.UTF-8):	Klasy Qt do programowania sieciowego - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}

%description -n QtNetwork-devel
Qt classes for network programming - development files.

%description -n QtNetwork-devel -l pl.UTF-8
Klasy Qt do programowania sieciowego - pliki programistyczne.

%package -n QtNetwork-static
Summary:	Qt classes for network programming - static libraries
Summary(pl.UTF-8):	Klasy Qt do programowania sieciowego - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtNetwork-devel = %{version}-%{release}

%description -n QtNetwork-static
Qt classes for network programming - static libraries.

%description -n QtNetwork-static -l pl.UTF-8
Klasy Qt do programowania sieciowego - biblioteki statyczne.

%package -n QtOpenGL
Summary:	Qt OpenGL support classes
Summary(pl.UTF-8):	Klasy Qt wspomagające OpenGL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}

%description -n QtOpenGL
Qt OpenGL support classes.

%description -n QtOpenGL -l pl.UTF-8
Klasy Qt wspomagające OpenGL.

%package -n QtOpenGL-devel
Summary:	Qt OpenGL support classes - development files
Summary(pl.UTF-8):	Klasy Qt wspomagające OpenGL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-GLU-devel
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}

%description -n QtOpenGL-devel
Qt OpenGL support classes - development files.

%description -n QtOpenGL-devel -l pl.UTF-8
Klasy Qt wspomagające OpenGL - pliki programistyczne.

%package -n QtOpenGL-static
Summary:	Qt OpenGL support classes - static libraries
Summary(pl.UTF-8):	Klasy Qt wspomagające OpenGL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtOpenGL-devel = %{version}-%{release}

%description -n QtOpenGL-static
Qt OpenGL support classes - static libraries.

%description -n QtOpenGL-static -l pl.UTF-8
Klasy Qt wspomagające OpenGL - biblioteki statyczne.

%package -n QtOpenVG
Summary:	Qt OpenVG support classes
Summary(pl.UTF-8):	Klasy Qt wspomagające OpenVG
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}

%description -n QtOpenVG
Qt OpenVG support classes.

%description -n QtOpenVG -l pl.UTF-8
Klasy Qt wspomagające OpenVG.

%package -n QtOpenVG-devel
Summary:	Qt OpenVG support classes - development files
Summary(pl.UTF-8):	Klasy Qt wspomagające OpenVG - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Mesa-libOpenVG-devel
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}

%description -n QtOpenVG-devel
Qt OpenVG support classes - development files.

%description -n QtOpenVG-devel -l pl.UTF-8
Klasy Qt wspomagające OpenVG - pliki programistyczne.

%package -n QtOpenVG-static
Summary:	Qt OpenVG support classes - static libraries
Summary(pl.UTF-8):	Klasy Qt wspomagające OpenVG - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtOpenVG-devel = %{version}-%{release}

%description -n QtOpenVG-static
Qt OpenVG support classes - static libraries.

%description -n QtOpenVG-static -l pl.UTF-8
Klasy Qt wspomagające OpenVG - biblioteki statyczne.

%package -n QtScript
Summary:	Qt classes for scripting applications
Summary(pl.UTF-8):	Klasy Qt pozwalające dodać obsługę skryptów w aplikacjach
Group:		X11/Development/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtScript
The QtScript module provides Qt classes to handle scripts inside
applications.

%description -n QtScript -l pl.UTF-8
Ten moduł dostarcza klasy Qt obsługujące języki skryptowe wewnątrz
aplikacji.

%package -n QtScript-devel
Summary:	Qt classes for scripting applications - development files
Summary(pl.UTF-8):	Klasy Qt do obsługi skryptów wewnątrz aplikacji - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}

%description -n QtScript-devel
Qt classes for scriptin applications - development files.

%description -n QtScript-devel -l pl.UTF-8
Klasy Qt do obsługi skryptów wewnątrz aplikacji - pliki
programistyczne.

%package -n QtScript-static
Summary:	Qt classes for scripting applications - static library
Summary(pl.UTF-8):	Klasy Qt pozwalające dodać obsługę skryptów w aplikacjach - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtScript-devel = %{version}-%{release}

%description -n QtScript-static
Qt classes for scripting applications - static library.

%description -n QtScript-static -l pl.UTF-8
Klasy Qt pozwalające dodać obsługę skryptów w aplikacjach - biblioteka
statyczna.

%package -n QtScriptTools
Summary:	QtScriptTools - additional components for applications that use QtScript
Summary(pl.UTF-8):	QtScriptTools - dodatkowe komponenty dla aplikacji wykorzystujących QtScript
Group:		X11/Development/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}

%description -n QtScriptTools
The QtScriptTools module provides additional components for
applications that use QtScript.

%description -n QtScriptTools -l pl.UTF-8
Moduł QtScriptTools dostarcza dodatkowe komponenty dla aplikacji
wykorzystujących QtScript.

%package -n QtScriptTools-devel
Summary:	Development files for QtScriptTools components
Summary(pl.UTF-8):	Pliki programistyczne komponentów QtScriptTools
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtScript-devel = %{version}-%{release}
Requires:	QtScriptTools = %{version}-%{release}

%description -n QtScriptTools-devel
Development files for QtScriptTools components.

%description -n QtScriptTools-devel -l pl.UTF-8
Pliki programistyczne komponentów QtScriptTools.

%package -n QtScriptTools-static
Summary:	QtScriptTools components - static library
Summary(pl.UTF-8):	Komponenty QtScriptTools - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtScriptTools-devel = %{version}-%{release}

%description -n QtScriptTools-static
Static version of QtScriptTools library, providing additional
components for applications that use QtScript.

%description -n QtScriptTools-static -l pl.UTF-8
Statyczna biblioteka QtScriptTools, dostarczająca dodatkowe komponenty
dla aplikacji wykorzystujących QtScript.

%package -n QtSql
Summary:	Qt classes for database integration using SQL
Summary(pl.UTF-8):	Klasy Qt do integracji z bazami danych przy użyciu SQL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtSql
Qt classes for database integration using SQL.

%description -n QtSql -l pl.UTF-8
Klasy Qt do integracji z bazami danych przy użyciu SQL.

%package -n QtSql-devel
Summary:	Qt classes for database integration using SQL - development files
Summary(pl.UTF-8):	Klasy Qt do integracji z bazami danych przy użyciu SQL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}

%description -n QtSql-devel
Qt classes for database integration using SQL - development files.

%description -n QtSql-devel -l pl.UTF-8
Klasy Qt do integracji z bazami danych przy użyciu SQL - pliki
programistyczne.

%package -n QtSql-static
Summary:	Qt classes for database integration using SQL - static libraries
Summary(pl.UTF-8):	Klasy Qt do integracji z bazami danych przy użyciu SQL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtSql-devel = %{version}-%{release}

%description -n QtSql-static
Qt classes for database integration using SQL - static libraries.

%description -n QtSql-static -l pl.UTF-8
Klasy Qt do integracji z bazami danych przy użyciu SQL - biblioteki
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
Summary:	Qt SVG support
Summary(pl.UTF-8):	Wsparcie Qt dla SVG
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
# for svg plugins
Requires:	QtXml = %{version}-%{release}

%description -n QtSvg
Qt SVG support.

%description -n QtSvg -l pl.UTF-8
Wsparcie Qt dla SVG.

%package -n QtSvg-devel
Summary:	Qt SVG support - development files
Summary(pl.UTF-8):	Wsparcie Qt dla SVG - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtSvg = %{version}-%{release}

%description -n QtSvg-devel
Qt SVG support - development files.

%description -n QtSvg-devel -l pl.UTF-8
Wsparcie Qt dla SVG - pliki programistyczne.

%package -n QtSvg-static
Summary:	Qt SVG support - static libraries
Summary(pl.UTF-8):	Wsparcie Qt dla SVG - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtSvg-devel = %{version}-%{release}

%description -n QtSvg-static
Qt SVG support - static libraries.

%description -n QtSvg-static -l pl.UTF-8
Wsparcie Qt dla SVG - biblioteki statyczne.

%package -n QtTest
Summary:	Qt test framework
Summary(pl.UTF-8):	Szkielet testów Qt
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtTest
Qt test framework.

%description -n QtTest -l pl.UTF-8
Szkielet testów Qt.

%package -n QtTest-devel
Summary:	Qt test framework - development files
Summary(pl.UTF-8):	Szkielet testów Qt - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtTest = %{version}-%{release}

%description -n QtTest-devel
Qt test framework - development files.

%description -n QtTest-devel -l pl.UTF-8
Szkielet testów Qt - pliki programistyczne.

%package -n QtTest-static
Summary:	Qt test framework - static libraries
Summary(pl.UTF-8):	Szkielet testów Qt - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtTest-devel = %{version}-%{release}

%description -n QtTest-static
Qt test framework - static libraries.

%description -n QtTest-static -l pl.UTF-8
Szkielet testów Qt - biblioteki statyczne.

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
Summary:	Qt classes for rendering HTML, XHTML and SVG documents
Summary(pl.UTF-8):	Klasy Qt do renderowania dokumentów HTML, XHTML i SVG
Group:		X11/Libraries
Requires:	QtDBus = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

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
Summary:	Qt classes for rendering HTML, XHTML and SVG documents - development files
Summary(pl.UTF-8):	Klasy Qt do renderowania dokumentów HTML, XHTML i SVG - pliki programistyczne
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
Qt classes for rendering HTML, XHTML and SVG documents - development
files.

%description -n QtWebKit-devel -l pl.UTF-8
Klasy Qt do renderowania dokumentów HTML, XHTML i SVG - pliki
programistyczne.

%package -n QtWebKit-static
Summary:	Qt classes for rendering HTML, XHTML and SVG documents - static library
Summary(pl.UTF-8):	Klasy Qt do renderowania dokumentów HTML, XHTML i SVG - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtWebKit-devel = %{version}-%{release}

%description -n QtWebKit-static
Qt classes for rendering HTML, XHTML and SVG documents - static
library.

%description -n QtWebKit-static -l pl.UTF-8
Klasy Qt do renderowania dokumentów HTML, XHTML i SVG - biblioteka
statyczna.

%package -n QtXml
Summary:	Qt classes for handling XML
Summary(pl.UTF-8):	Klasy Qt do obsługi XML-a
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtXml
Qt classes for handling XML.

%description -n QtXml -l pl.UTF-8
Klasy Qt do obsługi XML-a.

%package -n QtXml-devel
Summary:	Qt classes for handling XML - development files
Summary(pl.UTF-8):	Klasy Qt do obsługi XML-a - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n QtXml-devel
Qt classes for handling XML - development files.

%description -n QtXml-devel -l pl.UTF-8
Klasy Qt do obsługi XML-a - pliki programistyczne.

%package -n QtXml-static
Summary:	Qt classes for handling XML - static libraries
Summary(pl.UTF-8):	Klasy Qt do obsługi XML-a - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtXml-static
Qt classes for handling XML - static libraries.

%description -n QtXml-static -l pl.UTF-8
Klasy Qt do obsługi XML-a - biblioteki statyczne.

%package -n QtXmlPatterns
Summary:	QtXmlPatterns XQuery engine
Summary(pl.UTF-8):	Silnik zapytań XQuery QtXmlPatterns
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}

%description -n QtXmlPatterns
QtXmlPatterns XQuery engine.

%description -n QtXmlPatterns -l pl.UTF-8
Silnik zapytań XQuery QtXmlPatterns.

%package -n QtXmlPatterns-devel
Summary:	QtXmlPatterns XQuery engine - development files
Summary(pl.UTF-8):	Silnik zapytań XQuery QtXmlPatterns - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtNetwork-devel = %{version}-%{release}
Requires:	QtXmlPatterns = %{version}-%{release}

%description -n QtXmlPatterns-devel
QtXmlPatterns XQuery engine - development files.

%description -n QtXmlPatterns-devel -l pl.UTF-8
Silnik zapytań XQuery QtXmlPatterns - pliki programistyczne.

%package -n QtXmlPatterns-static
Summary:	QtXmlPatterns XQuery engine - static library
Summary(pl.UTF-8):	Silnik zapytań XQuery QtXmlPatterns - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtXmlPatterns-devel = %{version}-%{release}

%description -n QtXmlPatterns-static
QtXmlPatterns XQuery engine - static library.

%description -n QtXmlPatterns-static -l pl.UTF-8
Silnik zapytań XQuery QtXmlPatterns - biblioteka statyczna.

%package assistant
Summary:	Qt documentation browser
Summary(pl.UTF-8):	Przeglądarka dokumentacji Qt
Group:		X11/Development/Tools
Requires:	QtGui = %{version}-%{release}
Requires:	QtHelp = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtSql-sqlite3 = %{version}-%{release}
Requires:	QtWebKit = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}
Requires:	hicolor-icon-theme

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
Requires:	QtGui = %{version}-%{release}
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
Requires:	QtDesigner = %{version}-%{release}

%description designer
An advanced tool used for GUI designing with Qt library.

%description designer -l pl.UTF-8
Zaawansowane narzędzie służące do projektowania interfejsu graficznego
za pomocą biblioteki Qt.

%package devel-private
Summary:	Private Qt headers files
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtDeclarative-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtScript-devel = %{version}-%{release}

%description devel-private
Private Qt headers files - for calibre

%package linguist
Summary:	Translation helper for Qt
Summary(pl.UTF-8):	Aplikacja ułatwiająca tłumaczenie aplikacji opartych o Qt
Group:		X11/Development/Tools
Requires:	QtUiTools = %{version}-%{release}
Requires:	hicolor-icon-theme

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
Requires:	QtDBus = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}
Requires:	desktop-file-utils

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
Requires:	QtDeclarative = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtHelp = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}
Requires:	QtScript = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtSvg = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}
Requires:	QtXmlPatterns = %{version}-%{release}

%description demos
Demos are spiders that fly.

%description demos -l pl.UTF-8
Dema to latające pająki.

%package doc
Summary:	Qt Documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja Qt w formacie HTML
Group:		X11/Development/Libraries
Suggests:	%{name}-assistant = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja qt w formacie HTML.

%package examples
Summary:	Example programs bundled with Qt
Summary(pl.UTF-8):	Ćwiczenia i przykłady do Qt
Summary(pt_BR.UTF-8):	Programas exemplo desenvolvidos com o Qt
Group:		X11/Development/Libraries
# no *-devel deps, allow to look at the examples without compiling

%description examples
Example programs bundled with Qt version.

%description examples -l pl.UTF-8
Ćwiczenia/przykłady dołączone do Qt.

%description examples -l pt_BR.UTF-8
Programas exemplo para o Qt versão.

%prep
%setup -q -n qt-everywhere-opensource-src-%{version}

%patch100 -p1

%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%{?with_wkhtml:%patch11 -p1}
%patch12 -p1
%patch13 -p1

%patch15 -p1
%patch16 -p1

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
	' mkspecs/common/g++-base.conf

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

# disable webkit tests, broken build
rm -r src/3rdparty/webkit/Source/WebKit/qt/tests

%build
# pass OPTFLAGS to build qmake itself with optimization
export OPTFLAGS="%{rpmcflags}"
export PATH=$PWD/bin:$PATH

##################################
# DEFAULT OPTIONS FOR ALL BUILDS #
##################################

COMMONOPT=" \
	-confirm-license \
	-opensource \
	-buildkey pld \
	-verbose \
	-prefix %{_qtdir} \
	-bindir %{_qtdir}/bin \
	-docdir %{_docdir}/%{name}-doc \
	-headerdir %{_includedir}/qt4 \
	-libdir %{_libdir} \
	-plugindir %{_qtdir}/plugins \
	-datadir %{_datadir}/qt4 \
	-translationdir %{_localedir}/ \
	-sysconfdir %{_sysconfdir}/qt4 \
	-examplesdir %{_examplesdir}/qt4 \
	-demosdir %{_examplesdir}/qt4-demos \
	-optimized-qmake \
	-fast \
	-glib \
	%{!?with_gtk:-no-gtkstyle} \
	-%{!?with_pch:no-}pch \
	-no-rpath \
	%{!?with_mmx:-no-mmx} \
	%{!?with_3dnow:-no-3dnow} \
	%{!?with_sse:-no-sse} \
	%{!?with_sse2:-no-sse2} \
	%{!?with_sse3:-no-sse3} \
	%{!?with_ssse3:-no-ssse3} \
	%{!?with_sse41:-no-sse4.1} \
	%{!?with_sse42:-no-sse4.2} \
	%{!?with_avx:-no-avx} \
	-qdbus \
	-dbus-linked \
	-reduce-relocations \
	-system-libjpeg \
	-system-libmng \
	-system-libpng \
	-system-libtiff \
	-system-zlib \
	-openssl-linked \
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
	-largefile \
	-iconv \
	-icu \
	-no-separate-debug-info \
	-xfixes \
	-nis \
	-sm \
	-stl \
	-xcursor \
	-xinput \
	-xinerama \
	-xrandr \
	-xkb \
	-xrender \
	-xshape \
	-xmlpatterns \
	-continue"

##################################
#       STATIC MULTI-THREAD      #
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

./configure $COMMONOPT $OPT

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
#       SHARED MULTI-THREAD      #
##################################

OPT=" \
	-%{!?with_mysql:no}%{?with_mysql:plugin}-sql-mysql \
	-%{!?with_odbc:no}%{?with_odbc:plugin}-sql-odbc \
	-%{!?with_pgsql:no}%{?with_pgsql:plugin}-sql-psql \
	-%{!?with_sqlite3:no}%{?with_sqlite3:plugin}-sql-sqlite \
	-%{!?with_sqlite:no}%{?with_sqlite:plugin}-sql-sqlite2 \
	-%{!?with_ibase:no}%{?with_ibase:plugin}-sql-ibase \
	-shared"

./configure $COMMONOPT $OPT

%{__make}
%{__make} \
	sub-tools-all-ordered \
	sub-demos-all-ordered \
	sub-examples-all-ordered

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{env.d,qt4},%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_pkgconfigdir}}
install -d $RPM_BUILD_ROOT%{_qtdir}/plugins/{crypto,network}

echo '#QT_GRAPHICSSYSTEM=raster' > $RPM_BUILD_ROOT/etc/env.d/QT_GRAPHICSSYSTEM

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# for qt-creator sth is messed up in the Makefile, nothing for make install
install bin/qdoc3 $RPM_BUILD_ROOT%{_qtdir}/bin/qdoc3

# kill -L/inside/builddir from *.la and *.pc (bug #77152)
%{__sed} -i -e "s,-L$PWD/lib,,g" $RPM_BUILD_ROOT%{_libdir}/*.{la,prl}
%{__sed} -i -e "s,-L$PWD/lib,,g" $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc
%{__sed} -i -e '
	s|moc_location=.*|moc_location=%{_bindir}/moc-qt4|;
	s|uic_location=.*|uic_location=%{_bindir}/uic-qt4|;
	' $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# libQtWebKit.la contains '-ljscore' and '-lwebcore', they come
# from src/3rdparty/webkit/{JavaScriptCore,WebCore}} but those libs aren't installed
%{__sed} -i -e "s,-lwebcore,,g;s,-ljscore,,g;" $RPM_BUILD_ROOT%{_libdir}/libQtWebKit.la

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
ln -sf ../%{_lib}/qt4/bin/qdoc3 .
ln -sf ../%{_lib}/qt4/bin/qt3to4 .
ln -sf ../%{_lib}/qt4/bin/rcc .
ln -sf ../%{_lib}/qt4/bin/uic3 .
ln -sf ../%{_lib}/qt4/bin/pixeltool .
ln -sf ../%{_lib}/qt4/bin/qcollectiongenerator .
ln -sf ../%{_lib}/qt4/bin/qdbuscpp2xml .
ln -sf ../%{_lib}/qt4/bin/qdbusxml2cpp .
ln -sf ../%{_lib}/qt4/bin/qhelpconverter .
ln -sf ../%{_lib}/qt4/bin/qhelpgenerator .
ln -sf ../%{_lib}/qt4/bin/qmlviewer .
ln -sf ../%{_lib}/qt4/bin/qmlplugindump .
ln -sf ../%{_lib}/qt4/bin/qttracereplay .
ln -sf ../%{_lib}/qt4/bin/qvfb .
ln -sf ../%{_lib}/qt4/bin/xmlpatternsvalidator .
cd -

# multilib
mv $RPM_BUILD_ROOT%{_qtdir}/bin/{qdbus,qdbusviewer} $RPM_BUILD_ROOT%{_bindir}
ln -sf %{_bindir}/qdbus $RPM_BUILD_ROOT%{_qtdir}/bin/qdbus
ln -sf %{_bindir}/qdbusviewer $RPM_BUILD_ROOT%{_qtdir}/bin/qdbusviewer

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/qtconfig-qt4.desktop
install tools/qtconfig/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qtconfig-qt4.png

install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}/linguist-qt4.desktop
for f in tools/linguist/linguist/images/icons/linguist-*-32.png; do
	size=$(echo $(basename ${f}) | cut -d- -f2)
	install -D $f $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${size}x${size}/apps/linguist-qt4.png
done

install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/assistant-qt4.desktop
install -D tools/assistant/tools/assistant/images/assistant.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/assistant-qt4.png
install -D tools/assistant/tools/assistant/images/assistant-128.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/128x128/apps/assistant-qt4.png

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

%{__rm} $RPM_BUILD_ROOT%{_localedir}/*.qm
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
	install	-d $RPM_BUILD_ROOT%{_localedir}/$lang/LC_MESSAGES
	cp $file $RPM_BUILD_ROOT%{_localedir}/$lang/LC_MESSAGES/$MOD.qm
done

cd $RPM_BUILD_ROOT%{_includedir}/qt4/Qt
# QtCore must be the last
for f in ../Qt{3Support,DBus,Declarative,Designer,Gui,Help,Network,OpenGL,Script,Sql,Svg,Test,UiTools,WebKit,Xml,XmlPatterns,Core}/*; do
	if [ ! -d $f ]; then
		ln -sf $f `basename $f`
	fi
done
cd -

# Ship doc & qmake stuff
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

# Ship private headers - ugly hack to build calibre
install -d $RPM_BUILD_ROOT%{_includedir}/qt4/private
rsync -aR include/QtCore/private \
	  include/QtDeclarative/private \
	  include/QtGui/private \
	  include/QtScript/private \
	  $RPM_BUILD_ROOT%{_includedir}/qt4/private
rsync -aR src/corelib/*/*_p.h \
          src/declarative/*/*_p.h \
          src/gui/*/*_p.h \
          src/script/*/*_p.h \
	  $RPM_BUILD_ROOT%{_includedir}/qt4/private


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
mkdevfl	QtDeclarative
mkdevfl QtGui
mkdevfl QtMultimedia
mkdevfl QtNetwork
mkdevfl QtOpenGL
mkdevfl QtOpenVG
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
mkdevfl QtDesigner || /bin/true
mkdevfl QtUiTools || /bin/true

# without glob (exclude QtScriptTools* QtXmlPatterns*)
%{__sed} -i 's,QtScript\*,QtScript,g' QtScript-devel.files
%{__sed} -i 's,QtXml\*,QtXml,g' QtXml-devel.files
# no duplication between QtCore-devel and QtXml-devel
%{__sed} -i 's,%{_includedir}/qt4/Qt/QXmlStream.*,,g' QtCore-devel.files
%{__sed} -i 's,%{_includedir}/qt4/Qt/qxmlstream\.h,,g' QtCore-devel.files

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
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libphonon.so* \
	$RPM_BUILD_ROOT%{_libdir}/libphonon.{la,prl} \
	$RPM_BUILD_ROOT%{_libdir}/qt4/plugins/phonon_backend/libphonon_gstreamer.so \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/phonon.pc
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/qt4/phonon
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libphonon.a
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt3Support	-p /sbin/ldconfig
%postun	-n Qt3Support	-p /sbin/ldconfig

%post	-n QtCLucene	-p /sbin/ldconfig
%postun	-n QtCLucene	-p /sbin/ldconfig

%post	-n QtCore	-p /sbin/ldconfig
%postun	-n QtCore	-p /sbin/ldconfig

%post	-n QtDBus	-p /sbin/ldconfig
%postun	-n QtDBus	-p /sbin/ldconfig

%post	-n QtDeclarative	-p /sbin/ldconfig
%postun	-n QtDeclarative	-p /sbin/ldconfig

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

%post	-n QtOpenVG	-p /sbin/ldconfig
%postun	-n QtOpenVG	-p /sbin/ldconfig

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

%post assistant
%update_icon_cache hicolor

%postun assistant
%update_icon_cache hicolor

%post linguist
%update_icon_cache hicolor

%postun linguist
%update_icon_cache hicolor

%post	phonon		-p /sbin/ldconfig
%postun	phonon		-p /sbin/ldconfig

%post qtconfig
%update_desktop_database

%files -n Qt3Support
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt3Support.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt3Support.so.4
%attr(755,root,root) %{_qtdir}/plugins/accessible/libqtaccessiblecompatwidgets.so

%files -n QtCLucene
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtCLucene.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtCLucene.so.4

%files -n QtCore
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtCore.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtCore.so.4
%dir /etc/qt4
%dir %{_qtdir}
%dir %{_qtdir}/bin
%dir %{_qtdir}/plugins
%dir %{_qtdir}/plugins/codecs
%attr(755,root,root) %{_qtdir}/plugins/codecs/*.so
# two following are used only by foreign packages, not QtCore
%dir %{_qtdir}/plugins/crypto
%dir %{_qtdir}/plugins/network
%dir %{_datadir}/qt4
%lang(ar) %{_localedir}/ar/LC_MESSAGES/qt4.qm
%lang(cs) %{_localedir}/cs/LC_MESSAGES/qt4.qm
%lang(da) %{_localedir}/da/LC_MESSAGES/qt4.qm
%lang(de) %{_localedir}/de/LC_MESSAGES/qt4.qm
%lang(es) %{_localedir}/es/LC_MESSAGES/qt4.qm
%lang(fa) %{_localedir}/fa/LC_MESSAGES/qt4.qm
%lang(fr) %{_localedir}/fr/LC_MESSAGES/qt4.qm
%lang(gl) %{_localedir}/gl/LC_MESSAGES/qt4.qm
%lang(he) %{_localedir}/he/LC_MESSAGES/qt4.qm
%lang(hu) %{_localedir}/hu/LC_MESSAGES/qt4.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4.qm
%lang(ko) %{_localedir}/ko/LC_MESSAGES/qt4.qm
%lang(lt) %{_localedir}/lt/LC_MESSAGES/qt4.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4.qm
%lang(pt) %{_localedir}/pt/LC_MESSAGES/qt4.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4.qm
%lang(sk) %{_localedir}/sk/LC_MESSAGES/qt4.qm
%lang(sl) %{_localedir}/sl/LC_MESSAGES/qt4.qm
%lang(sv) %{_localedir}/sv/LC_MESSAGES/qt4.qm
%lang(uk) %{_localedir}/uk/LC_MESSAGES/qt4.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4.qm

%files -n QtDBus
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qdbus
%attr(755,root,root) %{_bindir}/qdbusviewer
%attr(755,root,root) %{_libdir}/libQtDBus.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtDBus.so.4
%attr(755,root,root) %{_qtdir}/bin/qdbus
%attr(755,root,root) %{_qtdir}/bin/qdbusviewer
# ?? is this the proper place?
%attr(755,root,root) %{_qtdir}/plugins/script/libqtscriptdbus.so

%files -n QtDeclarative
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmlviewer
%attr(755,root,root) %{_bindir}/qmlplugindump
%attr(755,root,root) %{_qtdir}/bin/qmlviewer
%attr(755,root,root) %{_qtdir}/bin/qmlplugindump
%attr(755,root,root) %{_libdir}/libQtDeclarative.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtDeclarative.so.4
%dir %{_qtdir}/imports
%dir %{_qtdir}/imports/Qt
%dir %{_qtdir}/imports/Qt/labs
%dir %{_qtdir}/imports/Qt/labs/folderlistmodel
%dir %{_qtdir}/imports/Qt/labs/gestures
%dir %{_qtdir}/imports/Qt/labs/particles
%dir %{_qtdir}/imports/Qt/labs/shaders
%attr(755,root,root) %{_qtdir}/imports/Qt/labs/*/*.so
%{_qtdir}/imports/Qt/labs/*/qmldir
%dir %{_qtdir}/imports/QtWebKit
%attr(755,root,root) %{_qtdir}/imports/QtWebKit/*.so
%{_qtdir}/imports/QtWebKit/qmldir
%dir %{_qtdir}/plugins/qmltooling
%attr(755,root,root) %{_qtdir}/plugins/qmltooling/libqmldbg_tcp.so
%attr(755,root,root) %{_qtdir}/plugins/qmltooling/libqmldbg_inspector.so

%files -n QtDesigner
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtDesigner.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtDesigner.so.4
%attr(755,root,root) %{_libdir}/libQtDesignerComponents.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtDesignerComponents.so.4
%dir %{_qtdir}/plugins/designer
%attr(755,root,root) %{_qtdir}/plugins/designer/*.so

%files -n QtGui
%defattr(644,root,root,755)
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/QT_GRAPHICSSYSTEM
%attr(755,root,root) %{_libdir}/libQtGui.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtGui.so.4
%dir %{_qtdir}/plugins/accessible
%attr(755,root,root) %{_qtdir}/plugins/accessible/libqtaccessiblewidgets.so
%dir %{_qtdir}/plugins/graphicssystems
%attr(755,root,root) %{_qtdir}/plugins/graphicssystems/libqtracegraphicssystem.so
%dir %{_qtdir}/plugins/iconengines
%dir %{_qtdir}/plugins/imageformats
%attr(755,root,root) %{_qtdir}/plugins/imageformats/libqgif.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/libqico.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/libqjpeg.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/libqmng.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/libqtga.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/libqtiff.so
%dir %{_qtdir}/plugins/inputmethods
%attr(755,root,root) %{_qtdir}/plugins/inputmethods/*.so

%files -n QtHelp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qhelpconverter
%attr(755,root,root) %{_bindir}/qhelpgenerator
%attr(755,root,root) %{_libdir}/libQtHelp.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtHelp.so.4
%attr(755,root,root) %{_qtdir}/bin/qhelpconverter
%attr(755,root,root) %{_qtdir}/bin/qhelpgenerator
%lang(cs) %{_localedir}/cs/LC_MESSAGES/qt4-qt_help.qm
%lang(da) %{_localedir}/da/LC_MESSAGES/qt4-qt_help.qm
%lang(de) %{_localedir}/de/LC_MESSAGES/qt4-qt_help.qm
%lang(fr) %{_localedir}/fr/LC_MESSAGES/qt4-qt_help.qm
%lang(gl) %{_localedir}/gl/LC_MESSAGES/qt4-qt_help.qm
%lang(hu) %{_localedir}/hu/LC_MESSAGES/qt4-qt_help.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4-qt_help.qm
%lang(ko) %{_localedir}/ko/LC_MESSAGES/qt4-qt_help.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4-qt_help.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4-qt_help.qm
%lang(sl) %{_localedir}/sl/LC_MESSAGES/qt4-qt_help.qm
%lang(uk) %{_localedir}/uk/LC_MESSAGES/qt4-qt_help.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4-qt_help.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4-qt_help.qm

%files -n QtMultimedia
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtMultimedia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtMultimedia.so.4

%files -n QtNetwork
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtNetwork.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtNetwork.so.4
%dir %{_qtdir}/plugins/bearer
%attr(755,root,root) %{_qtdir}/plugins/bearer/*.so

%files -n QtOpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtOpenGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtOpenGL.so.4
%attr(755,root,root) %{_qtdir}/plugins/graphicssystems/libqglgraphicssystem.so

%files -n QtOpenVG
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtOpenVG.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtOpenVG.so.4

%files -n QtScript
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtScript.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtScript.so.4
%dir %{_qtdir}/plugins/script

%files -n QtScriptTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtScriptTools.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtScriptTools.so.4

%files -n QtSql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSql.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSql.so.4
%dir %{_qtdir}/plugins/sqldrivers

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
%attr(755,root,root) %ghost %{_libdir}/libQtSvg.so.4
%attr(755,root,root) %{_qtdir}/plugins/iconengines/libqsvgicon.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/libqsvg.so

%files -n QtTest
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtTest.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtTest.so.4

%files -n QtUiTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtUiTools.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtUiTools.so.4

%files -n QtWebKit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtWebKit.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtWebKit.so.4

%files -n QtXml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtXml.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtXml.so.4

%files -n QtXmlPatterns
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/bin/xmlpatterns
%attr(755,root,root) %{_qtdir}/bin/xmlpatternsvalidator
%attr(755,root,root) %{_bindir}/xmlpatternsvalidator
%attr(755,root,root) %{_libdir}/libQtXmlPatterns.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtXmlPatterns.so.4

%files assistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/assistant-qt4
%attr(755,root,root) %{_bindir}/pixeltool
%attr(755,root,root) %{_bindir}/qcollectiongenerator
%attr(755,root,root) %{_qtdir}/bin/assistant
%attr(755,root,root) %{_qtdir}/bin/pixeltool
%attr(755,root,root) %{_qtdir}/bin/qcollectiongenerator
%lang(cs) %{_localedir}/cs/LC_MESSAGES/qt4-assistant.qm
%lang(da) %{_localedir}/da/LC_MESSAGES/qt4-assistant.qm
%lang(de) %{_localedir}/de/LC_MESSAGES/qt4-assistant.qm
%lang(fr) %{_localedir}/fr/LC_MESSAGES/qt4-assistant.qm
%lang(hu) %{_localedir}/hu/LC_MESSAGES/qt4-assistant.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4-assistant.qm
%lang(ko) %{_localedir}/ko/LC_MESSAGES/qt4-assistant.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4-assistant.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4-assistant.qm
%lang(sl) %{_localedir}/sl/LC_MESSAGES/qt4-assistant.qm
%lang(uk) %{_localedir}/uk/LC_MESSAGES/qt4-assistant.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4-assistant.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4-assistant.qm
%{_desktopdir}/assistant-qt4.desktop
%{_iconsdir}/hicolor/*/apps/assistant-qt4.png

%files build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/moc-qt4
%attr(755,root,root) %{_bindir}/qdoc3
%attr(755,root,root) %{_bindir}/qt3to4
%attr(755,root,root) %{_bindir}/rcc
%attr(755,root,root) %{_bindir}/uic-qt4
%attr(755,root,root) %{_qtdir}/bin/moc
%attr(755,root,root) %{_qtdir}/bin/qdoc3
%attr(755,root,root) %{_qtdir}/bin/qt3to4
%attr(755,root,root) %{_qtdir}/bin/rcc
%attr(755,root,root) %{_qtdir}/bin/uic
#find better place?
%attr(755,root,root) %{_bindir}/qttracereplay
%attr(755,root,root) %{_qtdir}/bin/qttracereplay
%{_datadir}/qt4/q3porting.xml

%files designer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/designer-qt4
%attr(755,root,root) %{_qtdir}/bin/designer
%lang(cs) %{_localedir}/cs/LC_MESSAGES/qt4-designer.qm
%lang(de) %{_localedir}/de/LC_MESSAGES/qt4-designer.qm
%lang(fr) %{_localedir}/fr/LC_MESSAGES/qt4-designer.qm
%lang(hu) %{_localedir}/hu/LC_MESSAGES/qt4-designer.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4-designer.qm
%lang(ko) %{_localedir}/ko/LC_MESSAGES/qt4-designer.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4-designer.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4-designer.qm
%lang(sl) %{_localedir}/sl/LC_MESSAGES/qt4-designer.qm
%lang(uk) %{_localedir}/uk/LC_MESSAGES/qt4-designer.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4-designer.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4-designer.qm
%{_desktopdir}/designer-qt4.desktop
%{_pixmapsdir}/designer-qt4.png

%files devel-private
%defattr(644,root,root,755)
%{_includedir}/qt4/private

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
%lang(cs) %{_localedir}/cs/LC_MESSAGES/qt4-linguist.qm
%lang(de) %{_localedir}/de/LC_MESSAGES/qt4-linguist.qm
%lang(fr) %{_localedir}/fr/LC_MESSAGES/qt4-linguist.qm
%lang(hu) %{_localedir}/hu/LC_MESSAGES/qt4-linguist.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4-linguist.qm
%lang(ko) %{_localedir}/ko/LC_MESSAGES/qt4-linguist.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4-linguist.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4-linguist.qm
%lang(sl) %{_localedir}/sl/LC_MESSAGES/qt4-linguist.qm
%lang(uk) %{_localedir}/uk/LC_MESSAGES/qt4-linguist.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4-linguist.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4-linguist.qm
%{_datadir}/qt4/phrasebooks
%{_desktopdir}/linguist-qt4.desktop
%{_iconsdir}/hicolor/*/apps/linguist-qt4.png

%if %{without system_phonon}
%files phonon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libphonon.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libphonon.so.4
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
%lang(hu) %{_localedir}/hu/LC_MESSAGES/qt4-qtconfig.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4-qtconfig.qm
%lang(ko) %{_localedir}/ko/LC_MESSAGES/qt4-qtconfig.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4-qtconfig.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4-qtconfig.qm
%lang(sl) %{_localedir}/sl/LC_MESSAGES/qt4-qtconfig.qm
%lang(uk) %{_localedir}/uk/LC_MESSAGES/qt4-qtconfig.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4-qtconfig.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4-qtconfig.qm
%{_desktopdir}/qtconfig-qt4.desktop
%{_pixmapsdir}/qtconfig-qt4.png

%files -n qvfb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qvfb
%attr(755,root,root) %{_qtdir}/bin/qvfb
%lang(hu) %{_localedir}/hu/LC_MESSAGES/qt4-qvfb.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4-qvfb.qm
%lang(ko) %{_localedir}/ko/LC_MESSAGES/qt4-qvfb.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4-qvfb.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4-qvfb.qm
%lang(sl) %{_localedir}/sl/LC_MESSAGES/qt4-qvfb.qm
%lang(uk) %{_localedir}/uk/LC_MESSAGES/qt4-qvfb.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4-qvfb.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4-qvfb.qm

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc

%files -n QtCLucene-devel -f QtCLucene-devel.files
%defattr(644,root,root,755)

%files -n Qt3Support-devel -f Qt3Support-devel.files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uic3
%attr(755,root,root) %{_qtdir}/bin/uic3

%files -n QtCore-devel -f QtCore-devel.files
%defattr(644,root,root,755)

%files -n QtDBus-devel -f QtDBus-devel.files
%defattr(644,root,root,755)

%files -n QtDeclarative-devel -f QtDeclarative-devel.files
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

%files -n QtOpenVG-devel -f QtOpenVG-devel.files
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

%files -n QtOpenVG-static
%defattr(644,root,root,755)
%{_libdir}/libQtOpenVG.a

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

%files -n QtDeclarative-static
%defattr(644,root,root,755)
%{_libdir}/libQtDeclarative.a

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
