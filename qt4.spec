#
# TODO:
# - build system recheck (most make -C are to be changed)
# - redo subpackages (qt-core,qt-xml,qt-network,qt-opengl, etc.)
# - bconds for IBM db2, oracle and tds sql drivers
# - fix install
# - remove obsolete patches

# Conditional build:
%bcond_with	nas		# enable NAS audio support
%bcond_with	nvidia		# prelink Qt/KDE and depend on NVIDIA binaries
%bcond_without	static_libs	# don't build static libraries
%bcond_without	cups		# disable CUPS support
%bcond_without	mysql		# don't build MySQL plugin
%bcond_without	odbc		# don't build unixODBC plugin
%bcond_without	pgsql		# don't build PostgreSQL plugin
%bcond_without	designer	# don't build designer (it takes long)
%bcond_without	sqlite		# don't build SQLite plugin
%bcond_without	ibase		# build ibase (InterBase/Firebird) plugin
%bcond_with	pch		# enable pch in qmake
%bcond_with	dont_enable	# a bcond for missing features

%undefine	with_dont_enable

%ifnarch %{ix86} %{x8664} sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%define		_withsql	1
%{!?with_sqlite:%{!?with_ibase:%{!?with_mysql:%{!?with_pgsql:%{!?with_odbc:%undefine _withsql}}}}}

#define		_snap		040422
%define		_ver		4.0.0
%define		_packager	djurban
%define		_name		qt

Summary:	The Qt GUI application framework
Summary(es):	Biblioteca para ejecutar aplicaciones GUI Qt
Summary(pl):	Biblioteka Qt do tworzenia GUI
Summary(pt_BR):	Estrutura para rodar aplica��es GUI Qt
Name:		qt4
Version:	%{_ver}
Release:	0.tp1.1
Epoch:		6
License:	GPL/QPL
Group:		X11/Libraries
#Source0:	http://ep09.pld-linux.org/~%{_packager}/kde/%{_name}-copy-%{_snap}.tar.bz2
#Source0:	ftp://ftp.trolltech.com/qt/source/%{_name}-x11-opensource-%{version}-b1.tar.bz2
Source0:	http://wftp.tu-chemnitz.de/pub/Qt/source//%{_name}-x11-opensource-%{version}-b1.tar.bz2
# Source0-md5:	4e7432f9bf5f3333429b490e33568573
#Source1:	http://ep09.pld-linux.org/~%{_packager}/kde/%{_name}-copy-patches-040531.tar.bz2
#Source1-md5	2e38e44b6ef26bfb8a7f3b6900ee53c0
Source2:	%{_name}config.desktop
Source3:	designer.desktop
Source4:	assistant.desktop
Source5:	linguist.desktop
%if %{with dont_enable}
Patch0:		%{_name}-tools.patch
Patch1:		%{_name}-FHS.patch
Patch3:		%{_name}-disable_tutorials.patch
%endif
Patch2:		%{name}-buildsystem.patch
Patch4:		%{name}-locale.patch
Patch6:		%{name}-licence_check.patch
Patch7:		%{name}-xcursor_version.patch
Patch8:		%{name}-antialias.patch
Patch9:		%{name}-hotfixes.patch
URL:		http://www.trolltech.com/products/qt/
Icon:		qt.xpm
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	OpenGL-devel
%{?with_nvidia:BuildRequires:	XFree86-driver-nvidia-devel < 1.0.4620}
# incompatible with bison
BuildRequires:	byacc
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.0.0
%{?with_pch:BuildRequires:	gcc >= 5:3.4.0}
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel >= 1.0.0
BuildRequires:	libpng-devel >= 1.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	libungif-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	perl-base
%{?with_pgsql:BuildRequires:	postgresql-backend-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
%{?with_odbc:BuildRequires:	unixODBC-devel}
%{?with_sqlite:BuildRequires:	sqlite-devel}
BuildRequires:	xcursor-devel
BuildRequires:	xft-devel
BuildRequires:	xrender-devel
BuildRequires:	zlib-devel
Requires:	OpenGL
Conflicts:	kdelibs <= 8:3.2-0.030602.1
Obsoletes:	qt-extensions
Obsoletes:	qt-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

# <begin main library description>

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

This package contains the shared, multi-threaded, linux version of the
Qt library, the style plugins and translation files for Qt.

%description -l es
Contiene las bibliotecas compartidas necesarias para ejecutar
aplicaciones Qt, bien como los archivos README.

%description -l pl
Qt oferuje kompletny system do tworzenia i rozwijania aplikacji w
j�zyku C++, w kt�rego sk�ad wchodzi biblioteka z klasami oraz
wieloplatformowymi narz�dziami do rozwijania i t�umaczenia aplikacji.
Z pomoc� Qt jeden kod �r�d�owy mo�e by� natywnie uruchamiany na
r�nych platformach (Windows, Unix/Linux, Mac OS X).

Qt ma bogaty zbi�r standardowych element�w interfejsu graficznego, ale
pozwala r�wnie� na pisanie w�asnych element�w. ��czy w spos�b
niewidoczny dla programisty interfejsy programowania r�nych system�w,
tworz�c w ten spos�b jeden interfejs dla obs�ugi plik�w, sieci,
proces�w, w�tk�w, baz danych itp. Umo�liwia tak�e �atwe przenoszenie
na Qt aplikacji korzystaj�cych z Motif oraz pisanie wtyczek z
wykorzystaniem Netscape LiveConnect.

Ten pakiet zawiera wsp�dzielon�, wielow�tkow�, linuksow� wersj�
biblioteki Qt, wtyczki ze stylami oraz pliki t�umacze� Qt.

%description -l pt_BR
Cont�m as bibliotecas compartilhadas necess�rias para rodar aplica��es
Qt, bem como os arquivos README.

%package devel
Summary:	Development files for the Qt GUI toolkit
Summary(es):	Archivos de inclusi�n necesaria para compilar aplicaciones Qt
Summary(pl):	Pliki nag��wkowe, przyk�ady i dokumentacja do biblioteki
Summary(pt_BR):	Arquivos de inclus�o necess�ria para compilar aplica��es Qt
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	freetype-devel
Requires:	libjpeg-devel
Requires:	libmng-devel
Requires:	libpng-devel
Requires:	libstdc++-devel
Requires:	%{_name} = %{epoch}:%{version}-%{release}
Conflicts:	qt2-devel

%description devel
This package contains the Qt development tools: the metaobjects
compiler (moc) and the user interface compiler (uic); Qt include
files, pkgconfig helpers and tools for preserving compatibility
between versions of Qt.


%description devel -l pl
Ten pakiet zawiera narz�dzia programistyczne Qt: kompilator
metaobiekt�w (moc), kompilator interfejsu u�ytkownika (uic); pliki
nag��wkowe, wsparcie dla pkgconfig oraz narz�dzia u�atwiaj�ce
zachowanie kompatybilno�ci niezale�nie od wersji Qt.


%package static
Summary:	Qt static library
Summary(pl):	Biblioteka statyczna Qt
Group:		X11/Development/Libraries
Requires:	%{_name}-devel = %{epoch}:%{version}-%{release}

%description static
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

This package contains the static, multi-threaded, linux version of the
Qt library.


%description static -l pl
Qt oferuje kompletny system do tworzenia i rozwijania aplikacji w
j�zyku C++, w kt�rego sk�ad wchodzi biblioteka z klasami oraz
wieloplatformowymi narz�dziami do rozwijania i t�umaczenia aplikacji.
Z pomoc� Qt jeden kod �r�d�owy mo�e by� natywnie uruchamiany na
r�nych platformach (Windows, Unix/Linux, Mac OS X).

Qt ma bogaty zbi�r standardowych element�w interfejsu graficznego, ale
pozwala r�wnie� na pisanie w�asnych element�w. ��czy w spos�b
niewidoczny dla programisty interfejsy programowania r�nych system�w,
tworz�c w ten spos�b jeden interfejs dla obs�ugi plik�w, sieci,
proces�w, w�tk�w, baz danych itp. Umo�liwia tak�e �atwe przenoszenie
na Qt aplikacji korzystaj�cych z Motif oraz pisanie wtyczek z
wykorzystaniem Netscape LiveConnect.

Ten pakiet zawiera statyczn�, wielow�tkow�, linuksow� wersj�
biblioteki Qt.

%package doc
Summary:	Qt Documentation in HTML format
Summary(pl):	Dokumentacja Qt w formacie HTML
Group:		X11/Development/Libraries
Obsoletes:	qt-doc-html

%description doc
Qt documentation in HTML format.

%description doc -l pl
Dokumentacja qt w formacie HTML.

%package man
Summary:	Qt man pages
Summary(pl):	Qt - strony man
Group:		X11/Development/Libraries
Obsoletes:	qt-doc-man

%description man
Qt documentation in man pages format.

%description man -l pl
Dokumentacja qt w formacie stron man.

%package examples
Summary:	Example programs bundled with Qt
Summary(pl):	�wiczenia i przyk�ady do Qt
Summary(pt_BR):	Programas exemplo desenvolvidos com o Qt
Group:		X11/Development/Libraries
Requires:	%{_name}-devel = %{epoch}:%{version}-%{release}

%description examples
Example programs bundled with Qt version.

%description examples -l pl
�wiczenia/przyk�ady do��czone do Qt.

%description examples -l pt_BR
Programas exemplo para o Qt vers�o.

# <end main library desc>

# <start multithreaded plugins desc>

%package plugin-ibase
Summary:	Database plugin for InterBase/Firebird Qt support
Summary(pl):	Wtyczka InterBase/Firebird do Qt
Summary(pt_BR):	Plugin de suporte a InterBase/Firebird para Qt
Group:		X11/Libraries
Requires:	%{_name} = %{epoch}:%{version}-%{release}
Provides:	%{_name}-plugin-sql = %{epoch}:%{version}-%{release}

%description plugin-ibase
This package contains a multi-thread enabled plugin for accessing
Interbase/Firebird database via the QSql classes.

%description plugin-ibase -l pl
Ten pakiet zawiera wielow�tkow� wersj� wtyczki do Qt umo�liwiaj�cej
korzystanie z baz danych Interbase/Firebird poprzez klasy QSql.

%description plugin-ibase -l pt_BR
Plugin de suporte a InterBase/Firebird para Qt.

%package plugin-mysql
Summary:	Database plugin for MySQL Qt support
Summary(pl):	Wtyczka MySQL do Qt
Summary(pt_BR):	Plugin de suporte a MySQL para Qt
Group:		X11/Libraries
Requires:	%{_name} = %{epoch}:%{version}-%{release}
Provides:	%{_name}-plugin-sql = %{epoch}:%{version}-%{release}
Obsoletes:	qt-plugins-mysql

%description plugin-mysql
This package contains a multi-thread enabled plugin for accessing
MySQL database via the QSql classes.

%description plugin-mysql -l pl
Ten pakiet zawiera wielow�tkow� wersj� wtyczki do Qt umo�liwiaj�cej
korzystanie z baz danych MySQL poprzez klasy QSql.

%description plugin-mysql -l pt_BR
Plugin de suporte a MySQL para Qt.

%package plugin-odbc
Summary:	Database plugin for ODBC Qt support
Summary(pl):	Wtyczka ODBC do Qt
Summary(pt_BR):	Plugin de suporte a ODBC para Qt
Group:		X11/Libraries
Requires:	%{_name} = %{epoch}:%{version}-%{release}
Provides:	%{_name}-plugin-sql = %{epoch}:%{version}-%{release}
Obsoletes:	qt-plugins-odbc

%description plugin-odbc
This package contains a multi-thread enabled plugin for accessing
unixODBC services via the QSql classes.

%description plugin-odbc -l pl
Ten pakiet zawiera wielow�tkow� wersj� wtyczki do Qt umo�liwiaj�cej
korzystanie z us�ug unixODBC poprzez klasy QSql.

%description plugin-odbc -l pt_BR
Plugin de suporte a ODBC para Qt.

%package plugin-psql
Summary:	Database plugin for PostgreSQL Qt support
Summary(pl):	Wtyczka PostgreSQL do Qt
Summary(pt_BR):	Plugin de suporte a PostgreSQL para Qt
Group:		X11/Libraries
Requires:	%{_name} = %{epoch}:%{version}-%{release}
Provides:	%{_name}-plugin-sql = %{epoch}:%{version}-%{release}
Obsoletes:	qt-plugins-psql

%description plugin-psql
This package contains a multi-thread enabled plugin for accessing
PostgreSQL database via the QSql classes.


%description plugin-psql -l pl
Ten pakiet zawiera wielow�tkow� wersj� wtyczki do Qt umo�liwiaj�cej
korzystanie z baz danych PostgreSQL poprzez klasy QSql.

%description plugin-psql -l es
Plugin de suporte a PostgreSQL para Qt.

%package plugin-sqlite
Summary:	Database plugin for SQLite Qt support
Summary(pl):	Wtyczka SQLite do Qt
Summary(pt_BR):	Plugin de suporte a SQLite para Qt
Group:		X11/Libraries
Requires:	%{_name} = %{epoch}:%{version}-%{release}
Provides:	%{_name}-plugin-sql = %{epoch}:%{version}-%{release}

%description plugin-sqlite
This package contains a multi-thread enabled plugin for using the
SQLite library (which allows to acces virtually any SQL database) via
the QSql classes.

%description plugin-sqlite -l pl
Ten pakiet zawiera wielow�tkow� wersj� wtyczki do Qt umo�liwiaj�cej
korzystanie z baz danych PostgreSQL poprzez klasy QSql.

%description plugin-sqlite -l pt_BR
Plugin de suporte a SQLite para Qt. # <end multithreaded plugins desc>

%package linguist
Summary:	Translation helper for Qt
Summary(pl):	Aplikacja u�atwiaj�ca t�umaczenie aplikacji oparty o Qt
Group:		X11/Development/Tools
Conflicts:	%{_name}-devel < 6:3.3.2-3

%description linguist
This program provides an interface that shortens and helps systematize
the process of translating GUIs. Qt Linguist takes all of the text of
a UI that will be shown to the user, and presents it to a human
translator in a simple window. When one UI text is translated, the
program automatically progresses to the next, until they are all
completed.

%description linguist -l pl
Ten program oferuje interfejs znacznie przy�pieszaj�cy proces
t�umaczenia interfejsu u�ytkownika. Zbiera wszystkie teksty
przeznaczone do t�umaczenia i przedstawia w �atwym w obs�udze oknie.
Gdy jeden z nich jest ju� przet�umaczony, automatycznie przechodzi do
nast�pnego, a� wszystkie b�d� przet�umaczone.

%package assistant
Summary:	Qt documentation browser
Summary(pl):	Przegl�darka dokumentacji Qt
Group:		X11/Development/Tools
Requires:	%{_name}-doc
Conflicts:	%{_name}-devel < 6:3.3.2-3

%description assistant
Qt Assistant is a tool for browsing on-line documentation with
indexing, bookmarks and full-text search.

%description assistant -l pl
Qt Assistant to narz�dzie do przegl�dania dokumentacji z mo�liwo�ci�
indeksowania, dodawania zak�adek i pe�notekstowego wyszukiwania.

%package -n qmake
Summary:	Qt makefile generator
Summary(pl):	Generator plik�w makefile dla aplikacji Qt
Group:		X11/Development/Tools
Conflicts:	%{_name}-devel < 6:3.3.2-3

%description -n qmake
A powerful makefile generator. It can create makefiles on any platform
from a simple .pro definitions file.

%description -n qmake -l pl
Rozbudowany generator plik�w makefile. Potrafi tworzy� pliki makefile
na ka�dej platformi na podstawie �atwego w przygotowaniu pliku .pro.

%package -n qtconfig
Summary:	Qt widgets configuration tool
Summary(pl):	Narz�dzie do konfigurowania widget�w Qt
Group:		X11/Applications
Requires:	%{_name} = %{epoch}:%{version}-%{release}

%description -n qtconfig
A tool for configuring look and behavior of Qt widgets.

%description -n qtconfig -l pl
Narz�die do konfiguracji wygl�du i zachowania widget�w Qt.

%package designer
Summary:	IDE used for GUI designing with Qt library
Summary(pl):	IDE s�u��ce do projektowania GUI za pomoc� biblioteki Qt
Group:		X11/Applications
Requires:	%{_name}-designer-libs = %{epoch}:%{version}-%{release}

%description designer
An advanced tool used for GUI designing with Qt library.

%description designer -l pl
Zaawansowane narz�dzie s�u��ce do projektowania interfejsu graficznego
za pomoc� biblioteki Qt.

%package designer-libs
Summary:	Libraries IDE used for GUI designing with Qt library
Summary(pl):	Biblioteki do IDE s�u��cego do projektowania GUI za pomoc� biblioteki Qt
Group:		X11/Applications
Requires:	%{_name} >= %{epoch}:%{version}-%{release}

%description designer-libs
Libraries used by the Qt GUI Designer.

%description designer-libs -l pl
Biblioteki wykorzystywane przez narz�dzie projektowania interfejsu
graficznego - Qt Designer.

%prep
#setup -q -n %{_name}-copy-%{_snap}
%setup -q -n %{_name}-x11-opensource-%{version}-b1
%if %{with dont_enable}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%endif
#patch2 -p1 -b .niedakh
#patch4 -p1 -b .niedakh
#patch6 -p1 -b .niedakh
#patch7 -p1 -b .niedakh
#patch8 -p1 -b .niedakh
#patch9 -p1

#cat >> patches/DISABLED <<EOF
#0005
#0039
#0042
#0043
#0047
#EOF
#./apply_patches

# change QMAKE_CFLAGS_RELEASE to build
# properly optimized libs
plik="mkspecs/linux-g++/qmake.conf"

perl -pi -e "
	s|/usr/X11R6/lib|/usr/X11R6/%{_lib}|;
	s|/usr/lib|%{_libdir}|;
	s|\\(QTDIR\\)/lib|\\(QTDIR\\)/%{_lib}|;
	" $plik

cat $plik \
	|grep -v QMAKE_CFLAGS_RELEASE \
	|grep -v QMAKE_CXXFLAGS_RELEASE \
	|grep -v QMAKE_CFLAGS_DEBUG \
	|grep -v QMAKE_CXXFLAGS_DEBUG \
	> $plik.1

mv $plik.1 $plik
echo >> $plik
echo -e "QMAKE_CFLAGS_RELEASE\t=\t%{rpmcflags}" >> $plik
echo -e "QMAKE_CXXFLAGS_RELEASE\t=\t%{rpmcflags}" >> $plik
echo -e "QMAKE_CFLAGS_DEBUG\t=\t%{debugcflags}" >> $plik
echo -e "QMAKE_CXXFLAGS_DEBUG\t=\t%{debugcflags}" >> $plik

%build
export QTDIR=`/bin/pwd`
export YACC='byacc -d'
export PATH=$QTDIR/bin:$PATH
export LD_LIBRARY_PATH=$QTDIR/%{_lib}:$LD_LIBRARY_PATH
export QMAKESPEC=$QTDIR/mkspecs/linux-g++

if [ "%{_lib}" != "lib" ] ; then
	ln -s lib "%{_lib}"
fi

# pass OPTFLAGS to build qmake itself with optimization
export OPTFLAGS="%{rpmcflags}"

#%{__make} -f Makefile.cvs

##################################
# DEFAULT OPTIONS FOR ALL BUILDS #
##################################

DEFAULTOPT=" \
	-DQT_CLEAN_NAMESPACE \
	-verbose \
	-prefix %{_prefix} \
	-libdir %{_libdir} \
	-headerdir %{_includedir}/qt \
	-datadir %{_datadir}/qt \
	-docdir %{_docdir}/%{_name}-doc \
	-sysconfdir %{_sysconfdir}/qt \
	-translationdir %{_datadir}/locale/ \
	-fast \
	-qt-gif \
	-system-libjpeg \
	-system-libmng \
	-system-libpng \
	-system-zlib \
	-no-exceptions \
	-I%{_includedir}/postgresql/server \
	-I%{_includedir}/mysql \
	%{!?with_cups:-no-cups} \
	%{?with_nas:-system-nas-sound} \
	%{?with_nvidia:-dlopen-opengl} \
	%{?with_pch:-pch} \
	%{?debug:-debug} \
	-xcursor"

##################################
#      STATIC MULTI-THREAD       #
##################################

%if %{with static_libs}
STATICOPT=" \
	-qt-imgfmt-jpeg \
	-qt-imgfmt-mng \
	-qt-imgfmt-png \
	%{?with_mysql:-qt-sql-mysql} \
	%{?with_odbc:-qt-sql-odbc} \
	%{?with_pgsql:-qt-sql-psql} \
	%{?with_sqlite:-qt-sql-sqlite} \
	%{?with_ibase:-qt-sql-ibase} \
	-static"

./configure \
	$DEFAULTOPT \
	$STATICOPT \
	<<_EOF_
q
yes
_EOF_

# Do not build tutorial and examples. Provide them as sources.
%{__make} sub-qmake sub-src 

# This will not remove previously compiled libraries.
%{__make} clean
%endif

##################################
#      SHARED MULTI-THREAD       #
##################################

SHAREDOPT=" \
	-plugin-imgfmt-jpeg \
	-plugin-imgfmt-mng \
	-plugin-imgfmt-png \
	%{?with_mysql:-plugin-sql-mysql} \
	%{?with_odbc:-plugin-sql-odbc} \
	%{?with_pgsql:-plugin-sql-psql} \
	%{?with_sqlite:-plugin-sql-sqlite} \
	%{?with_ibase:-plugin-sql-ibase} \
	-plugin-style-cde \
	-plugin-style-compact \
	-plugin-style-motif \
	-plugin-style-motifplus \
	-plugin-style-platinum \
	-plugin-style-sgi \
	-plugin-style-windows"

./configure \
	$DEFAULTOPT \
	$SHAREDOPT \
	-plugindir %{_libdir}/qt/plugins-mt \
	<<_EOF_
q
yes
_EOF_

%if %{with dont_enable}
%if %{without designer}
grep -v designer tools/tools.pro > tools/tools.pro.1
mv tools/tools.pro{.1,}
%{__make} -C tools/designer/uic \
	UIC="LD_PRELOAD=$QTDIR/%{_lib}/libqt-mt.so.3 $QTDIR/bin/uic -L $QTDIR/plugins"
%endif
%endif
# Do not build tutorial and examples. Provide them as sources.
%{__make} sub-qmake 
%{__make} -C src sub-moc
$QTDIR/bin/moc src/gui/image/qmovie.cpp > src/gui/image/qmovie.moc
$QTDIR/bin/moc src/gui/image/qpixmapcache.cpp > src/gui/image/qpixmapcache.moc
$QTDIR/bin/moc src/gui/widgets/qdockwindow.cpp > src/gui/widgets/qdockwindow.moc
$QTDIR/bin/moc src/gui/widgets/qeffects.cpp > src/gui/widgets/qeffects.moc
$QTDIR/bin/moc src/gui/widgets/qmenu.cpp > src/gui/widgets/qmenu.moc
$QTDIR/bin/moc src/gui/widgets/qmenudata.cpp > src/gui/widgets/qmenudata.moc
$QTDIR/bin/moc src/gui/widgets/qsplitter.cpp > src/gui/widgets/qsplitter.moc
$QTDIR/bin/moc src/gui/widgets/qworkspace.cpp > src/gui/widgets/qworkspace.moc
$QTDIR/bin/moc src/gui/dialogs/qcolordialog.cpp > src/gui/dialogs/qcolordialog.moc
$QTDIR/bin/moc src/gui/dialogs/qfontdialog.cpp > src/gui/dialogs/qfontdialog.moc
$QTDIR/bin/moc src/gui/dialogs/qprintdialog_unix.cpp > src/gui/dialogs/qprintdialog_unix.moc
$QTDIR/bin/moc src/opengl/qgl_x11.cpp > src/opengl/qgl_x11.moc
$QTDIR/bin/moc src/network/qftp.cpp > src/network/qftp.moc
$QTDIR/bin/moc src/compat/dialogs/q3filedialog.cpp > src/compat/dialogs/q3filedialog.moc
$QTDIR/bin/moc src/compat/other/qnetworkprotocol.cpp > src/compat/other/qnetworkprotocol.moc
$QTDIR/bin/moc src/compat/itemviews/qtable.cpp > src/compat/itemviews/qtable.moc
$QTDIR/bin/moc src/compat/widgets/q3dockwindow.cpp > src/compat/widgets/q3dockwindow.moc
$QTDIR/bin/moc src/compat/widgets/q3mainwindow.cpp > src/compat/widgets/q3mainwindow.moc
$QTDIR/bin/moc src/compat/widgets/qscrollview.cpp > src/compat/widgets/qscrollview.moc
$QTDIR/bin/moc src/compat/widgets/q3datetimeedit.cpp > src/compat/widgets/q3datetimeedit.moc
$QTDIR/bin/moc src/compat/widgets/q3toolbar.cpp > src/compat/widgets/q3toolbar.moc

%{__make} sub-src sub-tools sub-demos

%if %{with dont_enable}
%if %{with designer}
cd tools/designer/designer
lrelease designer_de.ts
lrelease designer_fr.ts
%endif
cd $QTDIR/tools/assistant
lrelease assistant_de.ts
lrelease assistant_fr.ts
cd $QTDIR/tools/linguist/linguist
lrelease linguist_de.ts
lrelease linguist_fr.ts
cd $QTDIR
%endif

##make -C extensions/nsplugin/src

%install
rm -rf $RPM_BUILD_ROOT

export QTDIR=`/bin/pwd`

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/qt \
	$RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/{crypto,network} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{_name}/lib \
	$RPM_BUILD_ROOT%{_mandir}/man{1,3} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install bin/{findtr,qt20fix,qtrename140} \
	$RPM_BUILD_ROOT%{_bindir}

#tools/{msg2qm/msg2qm,mergetr/mergetr}
#	$RPM_BUILD_ROOT%{_bindir}

%if %{with static_libs}
install %{_lib}/libqt*.a		$RPM_BUILD_ROOT%{_libdir}
%endif

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

%if %{with dont_enable}
%if %{with designer}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/designer.desktop
%endif

install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}

%if %{without designer}
install bin/uic $RPM_BUILD_ROOT%{_bindir}
%endif
%endif

install tools/qtconfig/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qtconfig.png

install doc/man/man1/*.1	$RPM_BUILD_ROOT%{_mandir}/man1
install doc/man/man3/*.3qt	$RPM_BUILD_ROOT%{_mandir}/man3

cp -dpR examples tutorial $RPM_BUILD_ROOT%{_examplesdir}/%{_name}

mv $RPM_BUILD_ROOT{%{_libdir}/*.prl,%{_examplesdir}/%{_name}/lib}

# From now QMAKE_INCDIR_QT becomes %{_includedir}/qt
perl -pi -e "
	s|(QMAKE_INCDIR_QT\\s*=\\s*\\\$\\(QTDIR\\)/include)|\$1/qt|
	" $RPM_BUILD_ROOT/%{_datadir}/qt/mkspecs/linux-g++/qmake.conf

# We provide qt style classes as plugins,
# so make corresponding changes to the qconfig.h.
chmod 644 $RPM_BUILD_ROOT%{_includedir}/qt/qconfig.h

cat >> $RPM_BUILD_ROOT%{_includedir}/qt/qconfig.h << EOF

/* All of these style classes we provide as plugins */
#define QT_NO_STYLE_CDE
#define QT_NO_STYLE_COMPACT
#define QT_NO_STYLE_MOTIF
#define QT_NO_STYLE_MOTIFPLUS
#define QT_NO_STYLE_PLATINUM
#define QT_NO_STYLE_SGI
#define QT_NO_STYLE_WINDOWS

EOF

%if %{with dont_enable}
install -d $RPM_BUILD_ROOT%{_datadir}/locale/{ar,de,fr,ru,he,cs,sk}/LC_MESSAGES
install translations/qt_ar.qm $RPM_BUILD_ROOT%{_datadir}/locale/ar/LC_MESSAGES/qt.qm
install translations/qt_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/qt.qm
install translations/qt_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/qt.qm
install translations/qt_ru.qm $RPM_BUILD_ROOT%{_datadir}/locale/ru/LC_MESSAGES/qt.qm
install translations/qt_iw.qm $RPM_BUILD_ROOT%{_datadir}/locale/he/LC_MESSAGES/qt.qm
install translations/qt_cs.qm $RPM_BUILD_ROOT%{_datadir}/locale/cs/LC_MESSAGES/qt.qm
install translations/qt_sk.qm $RPM_BUILD_ROOT%{_datadir}/locale/sk/LC_MESSAGES/qt.qm

%if %{with designer}
install tools/designer/designer/designer_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/designer.qm
install tools/designer/designer/designer_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/designer.qm
%endif
%endif

install tools/assistant/assistant_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/assistant.qm
#install tools/assistant/assistant_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/assistant.qm

%if %{with dont_enable}
install tools/linguist/linguist/linguist_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/linguist.qm
install tools/linguist/linguist/linguist_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/linguist.qm

install tools/linguist/qm2ts/qm2ts.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

rm -rf `find $RPM_BUILD_ROOT -name CVS`

cd $RPM_BUILD_ROOT%{_examplesdir}/%{_name}/examples
for i in `find ./ -name Makefile`;
do

%{__sed} -i -e "s,$RPM_BUILD_DIR,/usr,g" $i
%{__sed} -i -e "s,examples,src/examples/qt/examples,g" $i

done

cd $RPM_BUILD_ROOT%{_examplesdir}/%{_name}/tutorial
for i in `find ./ -name Makefile`;
do

%{__sed} -i -e "s,$RPM_BUILD_DIR,/usr,g" $i
%{__sed} -i -e "s,examples,src/examples/qt/tutorial,g" $i

done

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

cat << EOF

 *******************************************************
 *                                                     *
 *  NOTE:                                              *
 *  With qt 4.0.0 the single threaded version was      *
 *  removed.                                           *
 *                                                     *
 *******************************************************

EOF

%postun 	-p /sbin/ldconfig

%post	designer-libs -p /sbin/ldconfig
%postun	designer-libs -p /sbin/ldconfig
