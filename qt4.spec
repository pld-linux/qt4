#
# TODO:
#		- better descriptions
#
# Conditional build:
%bcond_with	nas		# enable NAS audio support
# static libs disabled for now
%bcond_with	static_libs	# don't build static libraries
%bcond_without	cups		# disable CUPS support
%bcond_without	mysql		# don't build MySQL plugin
%bcond_without	odbc		# don't build unixODBC plugin
%bcond_without	pgsql		# don't build PostgreSQL plugin
%bcond_without	designer	# don't build designer (it takes long)
%bcond_without	sqlite3		# don't build SQLite3 plugin
%bcond_without	sqlite		# don't build SQLite2 plugin
%bcond_without	ibase		# build ibase (InterBase/Firebird) plugin
%bcond_without	pch		# enable pch in qmake
%bcond_with	dont_enable	# blocks translations, they are not yeat available

%undefine	with_dont_enable

%ifnarch %{ix86} %{x8664} sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%define		_withsql	1
%{!?with_sqlite3:%{!?with_sqlite:%{!?with_ibase:%{!?with_mysql:%{!?with_pgsql:%{!?with_odbc:%undefine _withsql}}}}}}

%define		_snap		050513
%define		_ver		4.0.0
%define		_packager	djurban

Summary:	The Qt GUI application framework
Summary(es):	Biblioteca para ejecutar aplicaciones GUI Qt
Summary(pl):	Biblioteka Qt do tworzenia GUI
Summary(pt_BR):	Estrutura para rodar aplicações GUI Qt
Name:		qt4
Version:	%{_ver}
Release:	1.%{_snap}.0.1
License:	GPL/QPL
Group:		X11/Libraries
Source0:	http://ep09.pld-linux.org/~%{_packager}/kde/qt-copy-%{_snap}.tar.bz2
#Source0:	http://wftp.tu-chemnitz.de/pub/Qt/source//%{_name}-x11-opensource-%{version}-b1.tar.bz2
# Source0-md5:	df41290b627b28dc00991bf1e0f7a440
#Source1:	http://ep09.pld-linux.org/~%{_packager}/kde/%{_name}-copy-patches-040531.tar.bz2
#Source1-md5	2e38e44b6ef26bfb8a7f3b6900ee53c0
Source2:	qtconfig.desktop
Source3:	designer.desktop
Source4:	assistant.desktop
Source5:	linguist.desktop
Patch0:		%{name}-tools.patch
%if %{with dont_enable}
Patch1:		qt-FHS.patch
# no tutorials exist
Patch3:		qt-disable_tutorials.patch
%endif
Patch2:		%{name}-buildsystem.patch
Patch4:		%{name}-locale.patch
Patch8:		%{name}-antialias.patch
URL:		http://www.trolltech.com/products/qt/
Icon:		qt.xpm
%{?with_ibase:BuildRequires:	Firebird-devel}
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
BuildRequires:	OpenGL-devel
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
# uncomment this in rel. 1 - no time to upgrade rpm
#BuildRequires:	rpmbuild(macros) >= 1.213
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
%define         _noautostrip    '.*_debug\\.so*'

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

%description -l es
Contiene las bibliotecas compartidas necesarias para ejecutar
aplicaciones Qt, bien como los archivos README.

%description -l pl
Qt oferuje kompletny system do tworzenia i rozwijania aplikacji w
jêzyku C++, w którego sk³ad wchodzi biblioteka z klasami oraz
wieloplatformowymi narzêdziami do rozwijania i t³umaczenia aplikacji.
Z pomoc± Qt jeden kod ¼ród³owy mo¿e byæ natywnie uruchamiany na
ró¿nych platformach (Windows, Unix/Linux, Mac OS X).

Qt ma bogaty zbiór standardowych elementów interfejsu graficznego, ale
pozwala równie¿ na pisanie w³asnych elementów. £±czy w sposób
niewidoczny dla programisty interfejsy programowania ró¿nych systemów,
tworz±c w ten sposób jeden interfejs dla obs³ugi plików, sieci,
procesów, w±tków, baz danych itp. Umo¿liwia tak¿e ³atwe przenoszenie
na Qt aplikacji korzystaj±cych z Motif oraz pisanie wtyczek z
wykorzystaniem Netscape LiveConnect.

%package -n QtCore
Summary:	Core classes used by other modules
Group:		X11/Development/Libraries

%description -n QtCore
Core classes used by other modules.

%package -n QtCore-devel
Summary:	Core classes used by other modules
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}

%description -n QtCore-devel
Core classes used by other modules.

%package -n QtGui
Summary:	Graphical User Interface components
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}

%description -n QtGui
Graphical User Interface components.

%package -n QtGui-devel
Summary:	Graphical User Interface components
Group:		X11/Development/Libraries
Requires:	QtCore-devel >= %{epoch}:%{version}-%{release}

%description -n QtGui-devel
Graphical User Interface components.

%package -n QtNetwork
Summary:	Classes for network programming
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}

%description -n QtNetwork
Classes for network programming.

%package -n QtNetwork-devel
Summary:	Classes for network programming
Group:		X11/Development/Libraries
Requires:	QtCore-devel >= %{epoch}:%{version}-%{release}

%description -n QtNetwork-devel
Classes for network programming.

%package -n QtOpenGL
Summary:	OpenGL support classes
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}

%description -n QtOpenGL
OpenGL support classes.

%package -n QtOpenGL-devel
Summary:	OpenGL support classes
Group:		X11/Development/Libraries
Requires:	QtCore-devel >= %{epoch}:%{version}-%{release}

%description -n QtOpenGL-devel
OpenGL support classes.

%package -n QtSql
Summary:	Classes for database integration using SQL
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}

%description -n QtSql
Classes for database integration using SQL.

%package -n QtSql-devel
Summary:	Classes for database integration using SQL
Group:		X11/Development/Libraries
Requires:	QtCore-devel >= %{epoch}:%{version}-%{release}

%description -n QtSql-devel
Classes for database integration using SQL.

%package -n QtSql-ibase
Summary:	Database plugin for InterBase/Firebird Qt support
Summary(pl):	Wtyczka InterBase/Firebird do Qt
Summary(pt_BR):	Plugin de suporte a InterBase/Firebird para Qt
Group:		X11/Development/Libraries
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}
Requires:	QtSql >= %{epoch}:%{version}-%{release}

%description -n QtSql-ibase
This package contains a plugin for accessing Interbase/Firebird
database via the QSql classes.

%description -n QtSql-ibase -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych Interbase/Firebird poprzez klasy QSql.

%description -n QtSql-ibase -l pt_BR
Plugin de suporte a InterBase/Firebird para Qt.

%package -n QtSql-mysql
Summary:	Database plugin for MySQL Qt support
Summary(pl):	Wtyczka MySQL do Qt
Summary(pt_BR):	Plugin de suporte a MySQL para Qt
Group:		X11/Development/Libraries
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}
Requires:	QtSql >= %{epoch}:%{version}-%{release}

%description -n QtSql-mysql
This package contains a plugin for accessing MySQL database via the
QSql classes.

%description -n QtSql-mysql -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych MySQL poprzez klasy QSql.

%description -n QtSql-mysql -l pt_BR
Plugin de suporte a MySQL para Qt.

%package -n QtSql-odbc
Summary:	Database plugin for ODBC Qt support
Summary(pl):	Wtyczka ODBC do Qt
Summary(pt_BR):	Plugin de suporte a ODBC para Qt
Group:		X11/Development/Libraries
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}
Requires:	QtSql >= %{epoch}:%{version}-%{release}

%description -n QtSql-odbc
This package contains a plugin for accessing unixODBC services via the
QSql classes.

%description -n QtSql-odbc -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z us³ug
unixODBC poprzez klasy QSql.

%description -n QtSql-odbc -l pt_BR
Plugin de suporte a ODBC para Qt.

%package -n QtSql-pgsql
Summary:	Database plugin for PostgreSQL Qt support
Summary(pl):	Wtyczka PostgreSQL do Qt
Summary(pt_BR):	Plugin de suporte a PostgreSQL para Qt
Group:		X11/Development/Libraries
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}
Requires:	QtSql >= %{epoch}:%{version}-%{release}

%description -n QtSql-pgsql
This package contains a plugin for accessing PostgreSQL database via
the QSql classes.

%description -n QtSql-pgsql -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych PostgreSQL poprzez klasy QSql.

%description -n QtSql-pgsql -l es
Plugin de suporte a PostgreSQL para Qt.

%package -n QtSql-sqlite
Summary:	QtSql sqlite plugin
Summary:	Database plugin for SQLite Qt support
Summary(pl):	Wtyczka SQLite do Qt
Summary(pt_BR):	Plugin de suporte a SQLite para Qt
Group:		X11/Development/Libraries
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}
Requires:	QtSql >= %{epoch}:%{version}-%{release}

%description -n QtSql-sqlite
This package contains a plugin for using the SQLite library (which
allows to acces virtually any SQL database) via the QSql classes.

%description -n QtSql-sqlite -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych SQLite poprzez klasy QSql.

%description -n QtSql-sqlite -l pt_BR
Plugin de suporte a SQLite para Qt.

%package -n QtSql-sqlite3
Summary:	Database plugin for SQLite3 Qt support
Summary(pl):	Wtyczka SQLite3 do Qt
Summary(pt_BR):	Plugin de suporte a SQLite3 para Qt
Group:		X11/Development/Libraries
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}
Requires:	QtSql >= %{epoch}:%{version}-%{release}

%description -n QtSql-sqlite3
This package contains a plugin for using the SQLite3 library (which
allows to acces virtually any SQL database) via the QSql classes.

%description -n QtSql-sqlite3 -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych SQLite3 poprzez klasy QSql.

%description -n QtSql-sqlite3 -l pt_BR
Plugin de suporte a SQLite3 para Qt.

%package -n QtXml
Summary:	Classes for handling XML
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}

%description -n QtXml
Classes for handling XML.

%package -n QtXml-devel
Summary:	Classes for handling XML
Group:		X11/Development/Libraries
Requires:	QtCore-devel >= %{epoch}:%{version}-%{release}

%description -n QtXml-devel
Classes for handling XML.

%package -n Qt3Support
Summary:	Qt3 compat library
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}

%description -n Qt3Support
Qt3 compat library.

%package -n Qt3Support-devel
Summary:	Qt3 compat library
Group:		X11/Development/Libraries
Requires:	QtCore-devel >= %{epoch}:%{version}-%{release}

%description -n Qt3Support-devel
Qt3 compat library.

%package assistant
Summary:	Qt documentation browser
Summary(pl):	Przegl±darka dokumentacji Qt
Group:		X11/Development/Tools
Requires:	%{name}-doc

%description assistant
Qt Assistant is a tool for browsing on-line documentation with
indexing, bookmarks and full-text search.

%description assistant -l pl
Qt Assistant to narzêdzie do przegl±dania dokumentacji z mo¿liwo¶ci±
indeksowania, dodawania zak³adek i pe³notekstowego wyszukiwania.

%package build
Summary:	Build tools for Qt4
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}
Requires:	QtXml >= %{epoch}:%{version}-%{release}

%description build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) and qt3to4 include names
converter.

%package designer
Summary:	IDE used for GUI designing with Qt library
Summary(pl):	IDE s³u¿±ce do projektowania GUI za pomoc± biblioteki Qt
Group:		X11/Applications
Requires:	%{name}-designer-libs = %{epoch}:%{version}-%{release}

%description designer
An advanced tool used for GUI designing with Qt library.

%description designer -l pl
Zaawansowane narzêdzie s³u¿±ce do projektowania interfejsu graficznego
za pomoc± biblioteki Qt.

%package designer-libs
Summary:	Libraries IDE used for GUI designing with Qt library
Summary(pl):	Biblioteki do IDE s³u¿±cego do projektowania GUI za pomoc± biblioteki Qt
Group:		X11/Applications

%description designer-libs
Libraries used by the Qt GUI Designer.

%description designer-libs -l pl
Biblioteki wykorzystywane przez narzêdzie projektowania interfejsu
graficznego - Qt Designer.

%package linguist
Summary:	Translation helper for Qt
Summary(pl):	Aplikacja u³atwiaj±ca t³umaczenie aplikacji oparty o Qt
Group:		X11/Development/Tools

%description linguist
This program provides an interface that shortens and helps systematize
the process of translating GUIs. Qt Linguist takes all of the text of
a UI that will be shown to the user, and presents it to a human
translator in a simple window. When one UI text is translated, the
program automatically progresses to the next, until they are all
completed.

%description linguist -l pl
Ten program oferuje interfejs znacznie przy¶pieszaj±cy proces
t³umaczenia interfejsu u¿ytkownika. Zbiera wszystkie teksty
przeznaczone do t³umaczenia i przedstawia w ³atwym w obs³udze oknie.
Gdy jeden z nich jest ju¿ przet³umaczony, automatycznie przechodzi do
nastêpnego, a¿ wszystkie bêd± przet³umaczone.

%package -n qmake
Summary:	Qt makefile generator
Summary(pl):	Generator plików makefile dla aplikacji Qt
Group:		X11/Development/Tools

%description -n qmake
A powerful makefile generator. It can create makefiles on any platform
from a simple .pro definitions file.

%description -n qmake -l pl
Rozbudowany generator plików makefile. Potrafi tworzyæ pliki makefile
na ka¿dej platformi na podstawie ³atwego w przygotowaniu pliku .pro.

%package -n qtconfig
Summary:	Qt widgets configuration tool
Summary(pl):	Narzêdzie do konfigurowania widgetów Qt
Group:		X11/Applications

%description -n qtconfig
A tool for configuring look and behavior of Qt widgets.

%description -n qtconfig -l pl
Narzêdie do konfiguracji wygl±du i zachowania widgetów Qt.

%package -n qvfb
Summary:	Qt Virtual framebuffer
Group:		X11/Development/Libraries

%description -n qvfb
Qt Virtual framebuffer alllows you to run Qt/Embedded applications in
XWindow.

%package demos
Summary:	Demos of new qt4 features
Group:		X11/Development/Libraries
Requires:	QtCore >= %{epoch}:%{version}-%{release}
Requires:	QtXml >= %{epoch}:%{version}-%{release}

%description demos
Demos are spiders that fly.

%package doc
Summary:	Qt Documentation in HTML format
Summary(pl):	Dokumentacja Qt w formacie HTML
Group:		X11/Development/Libraries

%description doc
Qt documentation in HTML format.

%description doc -l pl
Dokumentacja qt w formacie HTML.

%package man
Summary:	Qt man pages
Summary(pl):	Qt - strony man
Group:		X11/Development/Libraries

%description man
Qt documentation in man pages format.

%description man -l pl
Dokumentacja qt w formacie stron man.

%package examples
Summary:	Example programs bundled with Qt
Summary(pl):	Æwiczenia i przyk³ady do Qt
Summary(pt_BR):	Programas exemplo desenvolvidos com o Qt
Group:		X11/Development/Libraries
# no it does not , we cant be sure the user wants to compile them right?
# he might just want to take a look, anwyay no single devel package now
#Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description examples
Example programs bundled with Qt version.

%description examples -l pl
Æwiczenia/przyk³ady do³±czone do Qt.

%description examples -l pt_BR
Programas exemplo para o Qt versão.

%prep
#setup -q -n %{_name}-copy-%{_snap}
%setup -q -n qt-copy
%patch0 -p1
%if %{with dont_enable}
%patch1 -p1
%patch3 -p1
%endif
%patch2 -p1 -b .niedakh
%patch4 -p1 -b .niedakh
#patch7 -p1 -b .niedakh
%patch8 -p1 -b .niedakh

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
if test -n "$LD_LIBRARY_PATH"; then
export LD_LIBRARY_PATH=$QTDIR/%{_lib}:$LD_LIBRARY_PATH
else
export LD_LIBRARY_PATH=$QTDIR/lib
fi

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
	-DQT_COMPAT \
	-verbose \
	-prefix %{_prefix} \
	-libdir %{_libdir} \
	-headerdir %{_includedir}/qt \
	-datadir %{_datadir}/qt \
	-docdir %{_docdir}/%{name}-doc \
	-sysconfdir %{_sysconfdir}/qt \
	-translationdir %{_datadir}/locale/ \
	-fast \
	-%{!?with_pch:no-}pch \
	-qt-gif \
	-system-libjpeg \
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
	-xcursor \
	-xshape \
	-xrender \
	-fontconfig \
	-xkb \
	-sm \
	-nis"

##################################
#      STATIC MULTI-THREAD       #
##################################

%if %{with static_libs}
STATICOPT=" \
	%{?with_mysql:-qt-sql-mysql} \
	%{?with_odbc:-qt-sql-odbc} \
	%{?with_pgsql:-qt-sql-psql} \
	%{?with_sqlite3:-qt-sql-sqlite} \
	%{?with_sqlite:-qt-sql-sqlite2} \
	%{?with_ibase:-qt-sql-ibase} \
	-static"

./configure \
	$DEFAULTOPT \
	$STATICOPT \
	<<_EOF_
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
	%{?with_mysql:-plugin-sql-mysql} \
	%{?with_odbc:-plugin-sql-odbc} \
	%{?with_pgsql:-plugin-sql-psql} \
	%{?with_sqlite3:-plugin-sql-sqlite} \
	%{?with_sqlite:-plugin-sql-sqlite2} \
	%{?with_ibase:-plugin-sql-ibase}"

./configure \
	$DEFAULTOPT \
	$SHAREDOPT \
	-plugindir %{_libdir}/qt4/plugins \
	<<_EOF_
yes
_EOF_

%if 0
%if %{with dont_enable}
%if %{without designer}
grep -v designer tools/tools.pro > tools/tools.pro.1
mv tools/tools.pro{.1,}
%{__make} -C tools/designer/uic \
	UIC="LD_PRELOAD=$QTDIR/%{_lib}/libqt-mt.so.3 $QTDIR/bin/uic -L $QTDIR/plugins"
%endif
%endif

# Do not build tutorial and examples. Provide them as sources.
%{__make} sub-src-all-ordered

cd tools/qtconfig
$QTDIR/bin/uic previewwidgetbase.ui -o ui_previewwidgetbase.h
cd -
%{__make} sub-tools-all-ordered sub-demos-all-ordered
%endif
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

%install
rm -rf $RPM_BUILD_ROOT

export QTDIR=`/bin/pwd`

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/qt \
	$RPM_BUILD_ROOT%{_libdir}/qt4/plugins/{crypto,network} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}/lib \
	$RPM_BUILD_ROOT%{_mandir}/man{1,3} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install bin/findtr \
	tools/qvfb/qvfb \
	$RPM_BUILD_ROOT%{_bindir}

mv -f $RPM_BUILD_ROOT{%{_prefix}/qt.conf,%{_sysconfdir}/qt}

# we fix qmakespecs. from now QMAKE_INCDIR_QT becomes %{_includedir}/qt4
perl -pi -e "
	s|(QMAKE_INCDIR_QT\\s*=\\s*\\\$\\(QTDIR\\)/include)|\$1/qt4|
	" $RPM_BUILD_ROOT/%{_datadir}/qt4/mkspecs/linux-g++/qmake.conf

#tools/{msg2qm/msg2qm,mergetr/mergetr}
#	$RPM_BUILD_ROOT%{_bindir}

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

install tools/qtconfig/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qtconfig.png

install tools/linguist/linguist/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/linguist.png

install tools/assistant/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/assistant.png

%if %{with designer}
install tools/designer/src/designer/images/designer.png \
$RPM_BUILD_ROOT%{_pixmapsdir}/designer.png
%endif

%if %{with static_libs}
install %{_lib}/libqt*.a $RPM_BUILD_ROOT%{_libdir}
%endif

%if %{with designer}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/designer.desktop
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install bin/uic $RPM_BUILD_ROOT%{_bindir}
%endif

install tools/linguist/{qm2ts,lrelease,lupdate}/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# not yet available
#install doc/man/man1/*.1	$RPM_BUILD_ROOT%{_mandir}/man1
#install doc/man/man3/*.3qt	$RPM_BUILD_ROOT%{_mandir}/man3

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

install tools/assistant/assistant_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/assistant.qm
install tools/assistant/assistant_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/assistant.qm

install tools/linguist/linguist/linguist_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/linguist.qm
install tools/linguist/linguist/linguist_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/linguist.qm
%endif

cp -dpR examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}
mv $RPM_BUILD_ROOT{%{_libdir}/*.prl,%{_examplesdir}/%{name}/lib}

for i in `find $RPM_BUILD_ROOT -name \*.svn`
do
	rm -rf "$i";
done

cd $RPM_BUILD_ROOT%{_examplesdir}/%{name}
for i in `find ./ -name Makefile`;
do

%{__sed} -i -e "s,$RPM_BUILD_DIR,%{_prefix},g" $i
%{__sed} -i -e "s,examples,src/examples/qt4/examples,g" $i

done
cd -

# we will be only packaging modularized qt no need to package the same headers twice
rm -rf $RPM_BUILD_ROOT%{_includedir}/qt4/Qt

#cd $RPM_BUILD_ROOT%{_includedir}/Qt
#rm -rf *.h
#mkdir arch
#for i in `find \`find ../  -maxdepth 1 -type d | egrep -v -w 'Qt|./'\` -name \*.h|cut -c 4-`;
#do
#y=`echo $i|cut -d '/' -f2-`;
#ln -s $y ../$i;
#done
#cd -

install demos/arthur/{affine/affine,deform/deform,gradients/gradients,pathstroke/pathstroke} \
	demos/{downloadwidget/downloadwidget,interview/interview,mainwindow/mainwindow} \
	demos/{textedit/textedit,sqlbrowser/sqlbrowser,spreadsheet/spreadsheet,scrollarea/scrollarea} \
	demos/{plasmatable/plasmatable,pimelim/pimelim} \
	$RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n QtCore
/sbin/ldconfig
cat << EOF
 *******************************************************
 *                                                     *
 *  NOTE:                                              *
 *  With qt 4.0.0 the single threaded version was      *
 *  removed. Also the library is modular now so be     *
 *  sure to check that you have every module you need. *
 *                                                     *
 *******************************************************
EOF
%postun	-n QtCore	-p /sbin/ldconfig

%post	-n QtGui	-p /sbin/ldconfig
%postun	-n QtGui	-p /sbin/ldconfig

%post	-n QtNetwork	-p /sbin/ldconfig
%postun	-n QtNetwork	-p /sbin/ldconfig

%post	-n QtOpenGL	-p /sbin/ldconfig
%postun	-n QtOpenGL	-p /sbin/ldconfig

%post	-n QtSql	-p /sbin/ldconfig
%postun	-n QtSql	-p /sbin/ldconfig

%post	-n QtXml	-p /sbin/ldconfig
%postun	-n QtXml	-p /sbin/ldconfig

%post	-n Qt3Support	-p /sbin/ldconfig
%postun	-n Qt3Support	-p /sbin/ldconfig

%post	assistant	-p /sbin/ldconfig
%postun	assistant	-p /sbin/ldconfig

%post	designer-libs	-p /sbin/ldconfig
%postun	designer-libs	-p /sbin/ldconfig

%files -n QtCore
%defattr(644,root,root,755)
%dir %{_sysconfdir}/qt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qt/qt.conf
%attr(755,root,root) %{_libdir}/libQtCore*.so.*
%dir %{_libdir}/qt4/plugins
%dir %{_libdir}/qt4/plugins/codecs
%dir %{_libdir}/qt4/plugins/imageformats
%dir %{_libdir}/qt4/plugins/sqldrivers
%dir %{_libdir}/qt4/plugins/crypto
%dir %{_libdir}/qt4/plugins/network
%dir %{_datadir}/qt4

%files -n QtCore-devel
%defattr(644,root,root,755)
%dir %{_includedir}/qt4
%attr(755,root,root) %{_libdir}/libQtCore*.so
%{_libdir}/libQtCore*.la
%{_includedir}/qt4/QtCore
%{_pkgconfigdir}/QtCore*.pc

%files -n QtGui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtGui*.so.*
%{_libdir}/qt4/plugins/codecs/*
%{_libdir}/qt4/plugins/imageformats/*

%files -n QtGui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtGui*.so
%{_libdir}/libQtGui*.la
%{_includedir}/qt4/QtGui
%{_pkgconfigdir}/QtGui*.pc

%files -n QtNetwork
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtNetwork*.so.*

%files -n QtNetwork-devel
%defattr(644,root,root,755)
%{_libdir}/libQtNetwork*.la
%attr(755,root,root) %{_libdir}/libQtNetwork*.so
%{_includedir}/qt4/QtNetwork
%{_pkgconfigdir}/QtNetwork*.pc

%files -n QtOpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtOpenGL*.so.*

%files -n QtOpenGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtOpenGL*.so
%{_libdir}/libQtOpenGL*.la
%{_includedir}/qt4/QtOpenGL
%{_pkgconfigdir}/QtOpenGL*.pc

%files -n QtSql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSql*.so.*

%files -n QtSql-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSql*.so
%{_libdir}/libQtSql*.la
%{_includedir}/qt4/QtSql
%{_pkgconfigdir}/QtSql*.pc

%if %{with mysql}
%files -n QtSql-mysql
%defattr(644,root,root,755)
%attr(755,root,root)  %{_libdir}/qt4/plugins/sqldrivers/libqsqlmysql*.so
%endif

%if %{with pgsql}
%files -n QtSql-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt4/plugins/sqldrivers/libqsqlpsql*.so
%endif

%if %{with sqlite}
%files -n QtSql-sqlite
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt4/plugins/sqldrivers/libqsqlite2*.so
%endif

%if %{with sqlite3}
%files -n QtSql-sqlite3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt4/plugins/sqldrivers/libqsqlite*.so
%endif

%if %{with ibase}
%files -n QtSql-ibase
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt4/plugins/sqldrivers/libqsqlibase*.so
%endif

%if %{with odbc}
%files -n QtSql-odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt4/plugins/sqldrivers/libqsqlodbc*.so
%endif

%files -n QtXml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtXml*.so.*

%files -n QtXml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtXml*.so
%{_libdir}/libQtXml*.la
%{_includedir}/qt4/QtXml
%{_pkgconfigdir}/QtXml*.pc

%files -n Qt3Support
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uic3
%attr(755,root,root) %{_libdir}/libQt3Support*.so.*

%files -n Qt3Support-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt3Support*.so
%{_libdir}/libQt3Support*.la
%{_includedir}/qt4/Qt3Support
%{_pkgconfigdir}/Qt3Support*.pc

%files assistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/assistant
%attr(755,root,root) %{_libdir}/libQtAssistantClient*.so*
#%lang(de) %{_datadir}/locale/de/LC_MESSAGES/assistant.qm
#%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/assistant.qm
%{_desktopdir}/assistant.desktop
%{_pixmapsdir}/assistant.png

%files build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rcc
%attr(755,root,root) %{_bindir}/moc
%attr(755,root,root) %{_bindir}/qt3to4
%attr(755,root,root) %{_bindir}/uic
%{_datadir}/qt4/q3porting.xml

%if %{with designer}
%files designer-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtDesigner*.so.*.*.*

%files designer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/designer
#%dir %{_libdir}/%{name}/plugins-?t/designer
#%lang(de) %{_datadir}/locale/de/LC_MESSAGES/designer.qm
#%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/designer.qm
%{_desktopdir}/designer.desktop
%{_pixmapsdir}/designer.png
%endif

%files linguist
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/linguist
%attr(755,root,root) %{_bindir}/findtr
%attr(755,root,root) %{_bindir}/lrelease
%attr(755,root,root) %{_bindir}/lupdate
%attr(755,root,root) %{_bindir}/qm2ts
#%lang(de) %{_datadir}/locale/de/LC_MESSAGES/linguist.qm
#%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/linguist.qm
%{_mandir}/man1/qm2ts.1*
%{_mandir}/man1/lupdate*.1*
%{_mandir}/man1/lrelease*.1*
%{_datadir}/qt4/phrasebooks
%{_desktopdir}/linguist.desktop
%{_pixmapsdir}/linguist.png

%files -n qmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmake
%{_datadir}/qt4/mkspecs

%files -n qtconfig
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qtconfig
%{_desktopdir}/qtconfig.desktop
%{_pixmapsdir}/qtconfig.png

%files -n qvfb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qvfb

%files demos
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/affine
%attr(755,root,root) %{_bindir}/deform
%attr(755,root,root) %{_bindir}/downloadwidget
%attr(755,root,root) %{_bindir}/gradients
%attr(755,root,root) %{_bindir}/interview
%attr(755,root,root) %{_bindir}/mainwindow
%attr(755,root,root) %{_bindir}/pathstroke
%attr(755,root,root) %{_bindir}/pimelim
%attr(755,root,root) %{_bindir}/plasmatable
%attr(755,root,root) %{_bindir}/scrollarea
%attr(755,root,root) %{_bindir}/spreadsheet
%attr(755,root,root) %{_bindir}/sqlbrowser
%attr(755,root,root) %{_bindir}/textedit

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/qt4
