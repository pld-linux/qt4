#
# TODO:
#	- better descriptions
#	- more cleanups
#	- check if translations are avilable
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
%bcond_with	dont_enable	# blocks translations, they are not yet available

%undefine	with_dont_enable

%ifnarch %{ix86} %{x8664} sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%define		_withsql	1
%{!?with_sqlite3:%{!?with_sqlite:%{!?with_ibase:%{!?with_mysql:%{!?with_pgsql:%{!?with_odbc:%undefine _withsql}}}}}}

%define		_packager	djurban

Summary:	The Qt GUI application framework
Summary(es):	Biblioteca para ejecutar aplicaciones GUI Qt
Summary(pl):	Biblioteka Qt do tworzenia GUI
Summary(pt_BR):	Estrutura para rodar aplicações GUI Qt
Name:		qt4
Version:	4.0.0
#Release:	1.%{_snap}.0.1
Release:	0.1
License:	GPL/QPL
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-desktop-%{version}.tar.bz2
# Source0-md5:	a6183269fab293282daf2da9ac940577
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
Patch9:		%{name}rc1-build.patch
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
Summary(pl):	Podstawowe klasy u¿ywane przez inne modu³y
Group:		X11/Libraries

%description -n QtCore
Core classes used by other modules.

%description -n QtCore -l pl
Podstawowe klasy u¿ywane przez inne modu³y.

%package -n QtCore-devel
Summary:	Core classes used by other modules - development files
Summary(pl):	Podstawowe klasy u¿ywane przez inne modu³y - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}

%description -n QtCore-devel
Core classes used by other modules - development files.

%description -n QtCore-devel -l pl
Podstawowe klasy u¿ywane przez inne modu³y - pliki programistyczne.

%package -n QtGui
Summary:	Graphical User Interface components
Summary(pl):	Komponenty graficznego interfejsu u¿ytkownika
Group:		X11/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}

%description -n QtGui
Graphical User Interface components.

%description -n QtGui -l pl
Komponenty graficznego interfejsu u¿ytkownika.

%package -n QtGui-devel
Summary:	Graphical User Interface components - development files
Summary(pl):	Komponenty graficznego interfejsu u¿ytkownika - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{epoch}:%{version}-%{release}
Requires:	QtGui = %{epoch}:%{version}-%{release}

%description -n QtGui-devel
Graphical User Interface components - development files.

%description -n QtGui-devel -l pl
Komponenty graficznego interfejsu u¿ytkownika - pliki programistyczne.

%package -n QtNetwork
Summary:	Classes for network programming
Summary(pl):	Klasy do programowania sieciowego
Group:		X11/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}

%description -n QtNetwork
Classes for network programming.

%description -n QtNetwork -l pl
Klasy do programowania sieciowego.

%package -n QtNetwork-devel
Summary:	Classes for network programming - development files
Summary(pl):	Klasy do programowania sieciowego - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{epoch}:%{version}-%{release}
Requires:	QtNetwork = %{epoch}:%{version}-%{release}

%description -n QtNetwork-devel
Classes for network programming - development files.

%description -n QtNetwork-devel -l pl
Klasy do programowania sieciowego - pliki programistyczne.

%package -n QtOpenGL
Summary:	OpenGL support classes
Summary(pl):	Klasy wspomagaj±ce OpenGL
Group:		X11/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}

%description -n QtOpenGL
OpenGL support classes.

%description -n QtOpenGL -l pl
Klasy wspomagaj±ce OpenGL.

%package -n QtOpenGL-devel
Summary:	OpenGL support classes - development files
Summary(pl):	Klasy wspomagaj±ce OpenGL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{epoch}:%{version}-%{release}
Requires:	QtOpenGL = %{epoch}:%{version}-%{release}

%description -n QtOpenGL-devel
OpenGL support classes - development files.

%description -n QtOpenGL-devel -l pl
Klasy wspomagaj±ce OpenGL - pliki programistyczne.

%package -n QtSql
Summary:	Classes for database integration using SQL
Summary(pl):	Klasy do integracji z bazami danych przy u¿yciu SQL
Group:		X11/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}

%description -n QtSql
Classes for database integration using SQL.

%description -n QtSql -l pl
Klasy do integracji z bazami danych przy u¿yciu SQL.

%package -n QtSql-devel
Summary:	Classes for database integration using SQL - development files
Summary(pl):	Klasy do integracji z bazami danych przy u¿yciu SQL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{epoch}:%{version}-%{release}
Requires:	QtSql = %{epoch}:%{version}-%{release}

%description -n QtSql-devel
Classes for database integration using SQL - development files.

%description -n QtSql-devel -l pl
Klasy do integracji z bazami danych przy u¿yciu SQL - pliki
programistyczne.

%package -n QtSql-ibase
Summary:	Database plugin for InterBase/Firebird Qt support
Summary(pl):	Wtyczka InterBase/Firebird do Qt
Summary(pt_BR):	Plugin de suporte a InterBase/Firebird para Qt
Group:		X11/Libraries
Requires:	QtSql = %{epoch}:%{version}-%{release}
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}

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
Group:		X11/Libraries
Requires:	QtSql = %{epoch}:%{version}-%{release}
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}

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
Group:		X11/Libraries
Requires:	QtSql = %{epoch}:%{version}-%{release}
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}

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
Group:		X11/Libraries
Requires:	QtSql = %{epoch}:%{version}-%{release}
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}

%description -n QtSql-pgsql
This package contains a plugin for accessing PostgreSQL database via
the QSql classes.

%description -n QtSql-pgsql -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych PostgreSQL poprzez klasy QSql.

%description -n QtSql-pgsql -l es
Plugin de suporte a PostgreSQL para Qt.

%package -n QtSql-sqlite
Summary:	Database plugin for SQLite 2.x Qt support
Summary(pl):	Wtyczka SQLite 2.x do Qt
Summary(pt_BR):	Plugin de suporte a SQLite 2.x para Qt
Group:		X11/Libraries
Requires:	QtSql = %{epoch}:%{version}-%{release}
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}

%description -n QtSql-sqlite
This package contains a plugin for using the SQLite 2.x library (which
allows to acces virtually any SQL database) via the QSql classes.

%description -n QtSql-sqlite -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych SQLite 2.x poprzez klasy QSql.

%description -n QtSql-sqlite -l pt_BR
Plugin de suporte a SQLite 2.x para Qt.

%package -n QtSql-sqlite3
Summary:	Database plugin for SQLite3 Qt support
Summary(pl):	Wtyczka SQLite3 do Qt
Summary(pt_BR):	Plugin de suporte a SQLite3 para Qt
Group:		X11/Libraries
Provides:	QtSql-backend = %{epoch}:%{version}-%{release}
Requires:	QtSql = %{epoch}:%{version}-%{release}

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
Summary(pl):	Klasy do obs³ugi XML-a
Group:		X11/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}

%description -n QtXml
Classes for handling XML.

%description -n QtXml -l pl
Klasy do obs³ugi XML-a.

%package -n QtXml-devel
Summary:	Classes for handling XML - development files
Summary(pl):	Klasy do obs³ugi XML-a - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{epoch}:%{version}-%{release}
Requires:	QtXml = %{epoch}:%{version}-%{release}

%description -n QtXml-devel
Classes for handling XML - development files.

%description -n QtXml-devel -l pl
Klasy do obs³ugi XML-a - pliki programistyczne.

%package -n Qt3Support
Summary:	Qt3 compatibility library
Summary(pl):	Biblioteka kompatybilno¶ci z Qt3
Group:		X11/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}

%description -n Qt3Support
Qt3 compatibility library.

%description -n Qt3Support -l pl
Biblioteka kompatybilno¶ci z Qt3.

%package -n Qt3Support-devel
Summary:	Qt3 compatibility library - development files
Summary(pl):	Biblioteka kompatybilno¶ci z Qt3 - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{epoch}:%{version}-%{release}
Requires:	Qt3Support = %{epoch}:%{version}-%{release}

%description -n Qt3Support-devel
Qt3 compatibility library - development files.

%description -n Qt3Support-devel -l pl
Biblioteka kompatybilno¶ci z Qt3 - pliki programistyczne.

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
Summary(pl):	Narzêdzia do budowania dla Qt4
Group:		X11/Development/Tools
Requires:	QtCore = %{epoch}:%{version}-%{release}
Requires:	QtXml = %{epoch}:%{version}-%{release}

%description build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) and qt3to4 include names
converter.

%description build -l pl
Ten pakiet zawiera komilator zasobów Qt (rcc), kompilator metaobiektów
(moc), kompilator interfejsów u¿ytkownika (uic) oraz konwerter nazw
plików nag³ówkowych qt3to4.

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
Summary(pl):	Wirtualny framebuffer dla Qt
Group:		X11/Development/Libraries

%description -n qvfb
Qt Virtual framebuffer allows you to run Qt/Embedded applications in
X window.

%description -n qvfb -l pl
Qt Virtual framebuffer pozwala na uruchamianie aplikacji Qt/Embedded
w okienku X.

%package demos
Summary:	Demos of new Qt4 features
Summary(pl):	Programy demonstruj±ce nowe mo¿liwo¶ci Qt4
Group:		X11/Development/Libraries
Requires:	QtCore = %{epoch}:%{version}-%{release}
Requires:	QtXml = %{epoch}:%{version}-%{release}

%description demos
Demos are spiders that fly.

%description demos -l pl
Dema to lataj±ce paj±ki.

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
Dokumentacja Qt w formacie stron man.

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
%setup -q -n qt-x11-opensource-desktop-%{version}
%patch0 -p1
%if %{with dont_enable}
%patch1 -p1
%patch3 -p1
%endif
%patch2 -p1 -b .niedakh
%patch4 -p1 -b .niedakh
%patch8 -p1 -b .niedakh
%patch9 -p1

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
echo -e "QMAKE_CXXFLAGS_RELEASE\t=\t%{rpmcxxflags}" >> $plik
echo -e "QMAKE_CFLAGS_DEBUG\t=\t%{debugcflags}" >> $plik
echo -e "QMAKE_CXXFLAGS_DEBUG\t=\t%{debugcflags}" >> $plik

%build
QTDIR=`/bin/pwd`

if test -n "$LD_LIBRARY_PATH"; then
    LD_LIBRARY_PATH=$QTDIR/%{_lib}:$LD_LIBRARY_PATH
else
    LD_LIBRARY_PATH=$QTDIR/lib
fi

if [ "%{_lib}" != "lib" ] ; then
	ln -s lib "%{_lib}"
fi

# pass OPTFLAGS to build qmake itself with optimization
OPTFLAGS="%{rpmcflags}"
PATH=$QTDIR/bin:$PATH
QMAKESPEC=$QTDIR/mkspecs/linux-g++
YACC='byacc -d'

export QTDIR YACC PATH LD_LIBRARY_PATH QMAKESPEC OPTFLAGS

BuildLib() {
# $1 - aditional params

##################################
# DEFAULT OPTIONS FOR ALL BUILDS #
##################################

DEFAULTOPT=" \
	-DQT_CLEAN_NAMESPACE \
	-DQT_COMPAT \
	-verbose \
	-prefix %{_prefix} \
	-docdir %{_docdir}/%{name}-doc \
	-headerdir %{_includedir}/qt4 \
	-libdir %{_libdir} \
	-bindir %{_bindir} \
	-plugindir %{_libdir}/qt4/plugins \
	-datadir %{_datadir}/qt4 \
	-translationdir %{_datadir}/locale/ \
	-sysconfdir %{_sysconfdir}/qt4 \
	-examplesdir %{_examplesdir}/qt4 \
	-demosdir %{_examplesdir}/qt4-demos \
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

./configure \
	$DEFAULTOPT \
	$1 \
	<<_EOF_
yes
_EOF_

%{__make} sub-src-all-ordered

}

##################################
#      STATIC MULTI-THREAD       #
##################################

%if %{with static_libs}
OPT=" \
	%{?with_mysql:-qt-sql-mysql} \
	%{?with_odbc:-qt-sql-odbc} \
	%{?with_pgsql:-qt-sql-psql} \
	%{?with_sqlite3:-qt-sql-sqlite} \
	%{?with_sqlite:-qt-sql-sqlite2} \
	%{?with_ibase:-qt-sql-ibase} \
	-static"
BuildLib $OPT
%{__make} clean
%endif

##################################
#      SHARED MULTI-THREAD       #
##################################

OPT=" \
	%{?with_mysql:-plugin-sql-mysql} \
	%{?with_odbc:-plugin-sql-odbc} \
	%{?with_pgsql:-plugin-sql-psql} \
	%{?with_sqlite3:-plugin-sql-sqlite} \
	%{?with_sqlite:-plugin-sql-sqlite2} \
	%{?with_ibase:-plugin-sql-ibase}"
BuildLib $OPT

%{__make} \
	sub-tools-all-ordered \
	sub-demos-all-ordered \
	sub-examples-all-ordered

#
# TODO: 
#	Check for "with" conditions befor build
# OR
#	Find out why and fix the reason of building only mysql sqldriver
#	(it is not installed either)
#
for dir in src/plugins/sqldrivers/{ibase,odbc,psql,sqlite,sqlite2}
do
	cd $dir
	%{__make}
	cd -
done

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
QTDIR=`/bin/pwd`

export QTDIR

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_libdir}/qt4/plugins/{crypto,network}
	
install plugins/sqldrivers/* $RPM_BUILD_ROOT%{_libdir}/qt4/plugins/sqldrivers
install bin/findtr tools/qvfb/qvfb $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

install tools/qtconfig/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qtconfig.png

install tools/linguist/linguist/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/linguist.png

install tools/assistant/images/assistant.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/assistant.png

%if %{with designer}
install tools/designer/src/designer/images/designer.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/designer.png
%endif

%if %{with static_libs}
install %{_lib}/*Qt*.a $RPM_BUILD_ROOT%{_libdir}
%endif

%if %{with designer}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/designer.desktop
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
%endif

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

cd $RPM_BUILD_ROOT%{_includedir}/qt4/Qt
for f in ../Qt{3Support,Core,Gui,Network,OpenGL,Sql,Xml}/*
do
	if [ ! -d $f ]; then
		ln -sf $f `basename $f`
	fi
done
ln -sf ../../QtCore/arch/qatomic.h arch/qatomic.h
cd -

for f in $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc
do
	sed -i -e s:-L$RPM_BUILD_DIR/qt-x11-opensource-desktop-%{version}/lib::g $f
done

# Prepare some files list
ifecho () {
	RESULT=`echo $RPM_BUILD_ROOT$2 2>/dev/null`
	[ "$RESULT" == "" ] && return
	r=`echo $RESULT | awk '{ print $1 }'`

	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation devel files list!"
		echo "$r: no such file or direcotry!"
		exit 1
	fi
}

mkdevfl () {
	MODULE=$1; shift
	echo "%%defattr(644,root,root,755)" > $MODULE-devel.files
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.so"
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.la" 
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.prl"
	ifecho $MODULE-devel "%{_pkgconfigdir}/$MODULE*.pc"
	for f in `find $RPM_BUILD_ROOT%{_includedir}/qt4/$MODULE -printf "%%P "`
	do
		ifecho $MODULE-devel %{_includedir}/qt4/$MODULE/$f
		ifecho $MODULE-devel %{_includedir}/qt4/Qt/$f
	done
	for f in $@; do ifecho $MODULE-devel $f; done
}

mkdevfl QtCore 	%{_includedir}/qt4 %{_includedir}/qt4/Qt \
	%{_libdir}/libQtAssistantClient{.prl,_debug.prl} \
	%{_libdir}/libQtDesigner{.prl,_debug.prl,Components{.prl,_debug.prl}}
mkdevfl QtGui
mkdevfl QtNetwork
mkdevfl QtOpenGL
mkdevfl QtSql
mkdevfl QtXml
mkdevfl Qt3Support

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt4
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt4 -printf "%%P "`
do
	ifecho examples %{_examplesdir}/qt4/$f
done

echo "%defattr(644,root,root,755)" > demos.files
ifecho demos "%{_examplesdir}/qt4-demos"
ifecho demos "%{_bindir}/qtdemo" >> demos.files
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt4-demos -printf "%%P "`
do
	ifecho demos %{_examplesdir}/qt4-demos/$f
done

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) 
%attr(755,root,root) %{_libdir}/libQtCore*.so.*
%dir %{_libdir}/qt4/plugins
%dir %{_libdir}/qt4/plugins/codecs
%dir %{_libdir}/qt4/plugins/crypto
%dir %{_libdir}/qt4/plugins/imageformats
%dir %{_libdir}/qt4/plugins/network
%dir %{_libdir}/qt4/plugins/sqldrivers
%dir %{_datadir}/qt4

%files -n QtGui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtGui*.so.*
%{_libdir}/qt4/plugins/codecs/*
%{_libdir}/qt4/plugins/imageformats/*

%files -n QtNetwork
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtNetwork*.so.*

%files -n QtOpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtOpenGL*.so.*

%files -n QtSql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSql*.so.*

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


%files -n Qt3Support
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uic3
%attr(755,root,root) %{_libdir}/libQt3Support*.so.*

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
%attr(755,root,root) %{_libdir}/qt4/plugins/designer/*.so

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
#%{_mandir}/man1/qm2ts.1*
#%{_mandir}/man1/lupdate*.1*
#%{_mandir}/man1/lrelease*.1*
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

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc

%files -n QtCore-devel -f QtCore-devel.files
%files -n QtGui-devel -f QtGui-devel.files
%files -n QtNetwork-devel -f QtNetwork-devel.files
%files -n QtOpenGL-devel -f QtOpenGL-devel.files
%files -n QtSql-devel -f QtSql-devel.files
%files -n QtXml-devel -f QtXml-devel.files
%files -n Qt3Support-devel -f Qt3Support-devel.files

%files demos -f demos.files
%files examples -f examples.files
