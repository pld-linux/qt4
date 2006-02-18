#
# TODO:
#	- QtUiTools to subpackage
#         (headers in %{_includedir}/qt4/QtUiTools, but (static-only) lib is not installed)
#       - qt4-designer-libs vs QtDesigner-{devel,static} naming inconsistency 
#	- better descriptions
#	- more cleanups
#	- check if translations are available
#
# Conditional build:
%bcond_with	nas		# enable NAS audio support
%bcond_without	static_libs	# build static libraries
%bcond_without	cups		# disable CUPS support
%bcond_without	mysql		# don't build MySQL plugin
%bcond_without	odbc		# don't build unixODBC plugin
%bcond_without	pgsql		# don't build PostgreSQL plugin
%bcond_without	designer	# don't build designer (it takes long)
%bcond_without	sqlite3		# don't build SQLite3 plugin
%bcond_without	sqlite		# don't build SQLite2 plugin
%bcond_without	ibase		# don't build ibase (InterBase/Firebird) plugin
%bcond_without	pch		# disable pch in qmake
%bcond_with	sse		# use SSE instructions in gui/painting module
%bcond_with	dont_enable	# blocks translations, they are not yet available

%undefine	with_dont_enable

%ifnarch %{ix86} %{x8664} sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif

%ifarch pentium3 pentium4 %{x8664}
%define		with_sse	1
%endif

%define		_withsql	1
%{!?with_sqlite3:%{!?with_sqlite:%{!?with_ibase:%{!?with_mysql:%{!?with_pgsql:%{!?with_odbc:%undefine _withsql}}}}}}

Summary:	The Qt GUI application framework
Summary(es):	Biblioteca para ejecutar aplicaciones GUI Qt
Summary(pl):	Biblioteka Qt do tworzenia GUI
Summary(pt_BR):	Estrutura para rodar aplicações GUI Qt
Name:		qt4
Version:	4.1.0
Release:	1.9
License:	GPL/QPL
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-src-%{version}.tar.gz
# Source0-md5:	0e3982a54f56b6420d3062b20524410a
Source2:	qtconfig.desktop
Source3:	designer.desktop
Source4:	assistant.desktop
Source5:	linguist.desktop
Patch0:		%{name}-tools.patch
Patch1:		%{name}-alpha.patch
Patch2:		%{name}-buildsystem.patch
Patch3:		%{name}-locale.patch
Patch4:		%{name}-debug-and-release.patch
Patch5:		%{name}-sse.patch
Patch6:		%{name}-antialias.patch
Patch7:		%{name}-support-cflags-with-commas.patch
Patch8:		%{name}-build-lib-static.patch
%if %{with dont_enable}
Patch9:		qt-FHS.patch
# no tutorials exist
Patch10:	qt-disable_tutorials.patch
%endif
URL:		http://www.trolltech.com/products/qt/
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	OpenGL-devel
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
# incompatible with bison
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_pch:BuildRequires:	gcc >= 5:3.4.0}
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel >= 1.0.0
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	libungif-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	perl-base
%{?with_pgsql:BuildRequires:	postgresql-backend-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
%{?with_sqlite:BuildRequires:	sqlite-devel}
%{?with_odbc:BuildRequires:	unixODBC-devel}
BuildRequires:	xcursor-devel
BuildRequires:	xft-devel
BuildRequires:	xrender-devel
BuildRequires:	zlib-devel
Requires:	OpenGL
Obsoletes:	qt-extensions
Obsoletes:	qt-utils
Conflicts:	kdelibs <= 8:3.2-0.030602.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define         _noautostrip    '.*_debug\\.so*'

%define		specflags	-fno-strict-aliasing

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
Requires:	QtCore = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	zlib-devel

%description -n QtCore-devel
Core classes used by other modules - development files.

%description -n QtCore-devel -l pl
Podstawowe klasy u¿ywane przez inne modu³y - pliki programistyczne.

%package -n QtCore-static
Summary:	Core classes used by other modules - static libraries
Summary(pl):	Podstawowe klasy u¿ywane przez inne modu³y - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}

%description -n QtCore-static
Core classes used by other modules - static libraries.

%description -n QtCore-static -l pl
Podstawowe klasy u¿ywane przez inne modu³y - biblioteki statyczne.

%package -n QtGui
Summary:	Graphical User Interface components
Summary(pl):	Komponenty graficznego interfejsu u¿ytkownika
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
# two following because of some plugins
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}

%description -n QtGui
Graphical User Interface components.

%description -n QtGui -l pl
Komponenty graficznego interfejsu u¿ytkownika.

%package -n QtGui-devel
Summary:	Graphical User Interface components - development files
Summary(pl):	Komponenty graficznego interfejsu u¿ytkownika - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	freetype-devel >= 1:2.0.0
Requires:	fontconfig-devel
Requires:	libpng-devel >= 2:1.0.8
Requires:	xcursor-devel
Requires:	xrender-devel

%description -n QtGui-devel
Graphical User Interface components - development files.

%description -n QtGui-devel -l pl
Komponenty graficznego interfejsu u¿ytkownika - pliki programistyczne.

%package -n QtGui-static
Summary:	Graphical User Interface components - static libraries
Summary(pl):	Komponenty graficznego interfejsu u¿ytkownika - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}

%description -n QtGui-static
Graphical User Interface components - static libraries.

%description -n QtGui-static -l pl
Komponenty graficznego interfejsu u¿ytkownika - biblioteki statyczne.

%package -n QtNetwork
Summary:	Classes for network programming
Summary(pl):	Klasy do programowania sieciowego
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtNetwork
Classes for network programming.

%description -n QtNetwork -l pl
Klasy do programowania sieciowego.

%package -n QtNetwork-devel
Summary:	Classes for network programming - development files
Summary(pl):	Klasy do programowania sieciowego - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}

%description -n QtNetwork-devel
Classes for network programming - development files.

%description -n QtNetwork-devel -l pl
Klasy do programowania sieciowego - pliki programistyczne.

%package -n QtNetwork-static
Summary:	Classes for network programming - static libraries
Summary(pl):	Klasy do programowania sieciowego - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtNetwork-devel = %{version}-%{release}

%description -n QtNetwork-static
Classes for network programming - static libraries.

%description -n QtNetwork-static -l pl
Klasy do programowania sieciowego - biblioteki statyczne.

%package -n QtOpenGL
Summary:	OpenGL support classes
Summary(pl):	Klasy wspomagaj±ce OpenGL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtOpenGL
OpenGL support classes.

%description -n QtOpenGL -l pl
Klasy wspomagaj±ce OpenGL.

%package -n QtOpenGL-devel
Summary:	OpenGL support classes - development files
Summary(pl):	Klasy wspomagaj±ce OpenGL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}

%description -n QtOpenGL-devel
OpenGL support classes - development files.

%description -n QtOpenGL-devel -l pl
Klasy wspomagaj±ce OpenGL - pliki programistyczne.

%package -n QtOpenGL-static
Summary:	OpenGL support classes - static libraries
Summary(pl):	Klasy wspomagaj±ce OpenGL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtOpenGL-devel = %{version}-%{release}

%description -n QtOpenGL-static
OpenGL support classes - static libraries.

%description -n QtOpenGL-devel -l pl
Klasy wspomagaj±ce OpenGL - biblioteki statyczne.

%package -n QtSql
Summary:	Classes for database integration using SQL
Summary(pl):	Klasy do integracji z bazami danych przy u¿yciu SQL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtSql
Classes for database integration using SQL.

%description -n QtSql -l pl
Klasy do integracji z bazami danych przy u¿yciu SQL.

%package -n QtSql-devel
Summary:	Classes for database integration using SQL - development files
Summary(pl):	Klasy do integracji z bazami danych przy u¿yciu SQL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}

%description -n QtSql-devel
Classes for database integration using SQL - development files.

%description -n QtSql-devel -l pl
Klasy do integracji z bazami danych przy u¿yciu SQL - pliki
programistyczne.

%package -n QtSql-static
Summary:	Classes for database integration using SQL - static libraries
Summary(pl):	Klasy do integracji z bazami danych przy u¿yciu SQL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtSql-devel = %{version}-%{release}

%description -n QtSql-static
Classes for database integration using SQL - static libraries.

%description -n QtSql-static -l pl
Klasy do integracji z bazami danych przy u¿yciu SQL - biblioteki
statyczne. programistyczne.

%package -n QtSql-ibase
Summary:	Database plugin for InterBase/Firebird Qt support
Summary(pl):	Wtyczka InterBase/Firebird do Qt
Summary(pt_BR):	Plugin de suporte a InterBase/Firebird para Qt
Group:		X11/Libraries
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

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
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

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
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

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
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

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
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

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
Requires:	QtSql = %{version}-%{release}
Provides:	QtSql-backend = %{version}-%{release}

%description -n QtSql-sqlite3
This package contains a plugin for using the SQLite3 library (which
allows to acces virtually any SQL database) via the QSql classes.

%description -n QtSql-sqlite3 -l pl
Ten pakiet zawiera wtyczki do Qt umo¿liwiaj±ce korzystanie z baz
danych SQLite3 poprzez klasy QSql.

%description -n QtSql-sqlite3 -l pt_BR
Plugin de suporte a SQLite3 para Qt.

%package -n QtSvg
Summary:	SVG support
Summary(pl):	Wsparcie dla SVG
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtSvg
SVG support.

%description -n QtSvg -l pl
Wsparcie dla SVG.

%package -n QtSvg-devel
Summary:	SVG support - development files
Summary(pl):	Wsparcie dla SVG - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtSvg = %{version}-%{release}

%description -n QtSvg-devel
SVG support - development files.

%description -n QtSvg-devel -l pl
Wsparcie dla SVG - pliki programistyczne.

%package -n QtSvg-static
Summary:	SVG support - static libraries
Summary(pl):	Wsparcie dla SVG - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtSvg-devel = %{version}-%{release}

%description -n QtSvg-static
SVG support - static libraries.

%description -n QtSvg-static -l pl
Wsparcie dla SVG - biblioteki statyczne.

%package -n QtTest
Summary:	Test framework
Summary(pl):	Szkielet testów
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtTest
Test framework.

%description -n QtTest -l pl
Szkielet testów.

%package -n QtTest-devel
Summary:	Test framework - development files
Summary(pl):	Szkielet testów - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtTest = %{version}-%{release}

%description -n QtTest-devel
Test framework - development files.

%description -n QtTest-devel -l pl
Szkielet testów - pliki programistyczne.

%package -n QtXml
Summary:	Classes for handling XML
Summary(pl):	Klasy do obs³ugi XML-a
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtXml
Classes for handling XML.

%description -n QtXml -l pl
Klasy do obs³ugi XML-a.

%package -n QtXml-devel
Summary:	Classes for handling XML - development files
Summary(pl):	Klasy do obs³ugi XML-a - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n QtXml-devel
Classes for handling XML - development files.

%description -n QtXml-devel -l pl
Klasy do obs³ugi XML-a - pliki programistyczne.

%package -n QtXml-static
Summary:	Classes for handling XML - static libraries
Summary(pl):	Klasy do obs³ugi XML-a - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtXml-static
Classes for handling XML - static libraries.

%description -n QtXml-static -l pl
Klasy do obs³ugi XML-a - biblioteki statyczne.

%package -n Qt3Support
Summary:	Qt3 compatibility library
Summary(pl):	Biblioteka kompatybilno¶ci z Qt3
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n Qt3Support
Qt3 compatibility library.

%description -n Qt3Support -l pl
Biblioteka kompatybilno¶ci z Qt3.

%package -n Qt3Support-devel
Summary:	Qt3 compatibility library - development files
Summary(pl):	Biblioteka kompatybilno¶ci z Qt3 - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtCore-devel = %{version}-%{release}

%description -n Qt3Support-devel
Qt3 compatibility library - development files.

%description -n Qt3Support-devel -l pl
Biblioteka kompatybilno¶ci z Qt3 - pliki programistyczne.

%package -n Qt3Support-static
Summary:	Qt3 compatibility library - static libraries
Summary(pl):	Biblioteka kompatybilno¶ci z Qt3 - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	Qt3Support-devel = %{version}-%{release}

%description -n Qt3Support-static
Qt3 compatibility library - static libraries.

%description -n Qt3Support-static -l pl
Biblioteka kompatybilno¶ci z Qt3 - biblioteki statyczne.

%package -n QtAssistant
Summary:	Qt Assistant client library
Summary(pl):	Biblioteka kliencka Qt Assistant
Group:		X11/Development/Libraries

%description -n QtAssistant
This library allows to use Qt Assistant as an application's help tool.

%description -n QtAssistant -l pl
Ta biblioteka umo¿liwia wykorzystanie Qt Assistanta jako narzêdzie
pomocy w aplikacjach.

%package -n QtAssistant-devel
Summary:	Qt Assistant client library - development files
Summary(pl):	Biblioteka kliencka Qt Assistant - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtNetwork-devel = %{version}-%{release}

%description -n QtAssistant-devel
Development files for Qt Assistant client library.

%description -n QtAssistant-devel -l pl
Pliki programistyczne biblioteki klienckiej Qt Assistant.

%package -n QtAssistant-static
Summary:	Static Qt Assistant client library
Summary(pl):	Statyczna biblioteka kliencka Qt Assistant
Group:		X11/Development/Libraries
Requires:	QtAssistant-devel = %{version}-%{release}

%description -n QtAssistant-static
Static Qt Assistant client library.

%description -n QtAssistant-static -l pl
Statyczna biblioteka kliencka Qt Assistant.

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
Requires:	QtCore = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) and qt3to4 include names
converter.

%description build -l pl
Ten pakiet zawiera kompilator zasobów Qt (rcc), kompilator
metaobiektów (moc), kompilator interfejsów u¿ytkownika (uic) oraz
konwerter nazw plików nag³ówkowych qt3to4.

%package designer
Summary:	IDE used for GUI designing with Qt library
Summary(pl):	IDE s³u¿±ce do projektowania GUI za pomoc± biblioteki Qt
Group:		X11/Applications
Requires:	%{name}-designer-libs = %{version}-%{release}

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

%package -n QtDesigner-devel
Summary:	IDE used for GUI designing with Qt library - development files
Summary(pl):	IDE s³u¿±ce do projektowania GUI za pomoc± biblioteki Qt - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	%{name}-designer-libs = %{version}-%{release}
Requires:	QtCore-devel = %{version}-%{release}

%description -n QtDesigner-devel
IDE used for GUI designing with Qt library - development files.

%description -n QtDesigner-devel -l pl
IDE s³u¿±ce do projektowania GUI za pomoc± biblioteki Qt - pliki
programistyczne.

%package -n QtDesigner-static
Summary:	IDE used for GUI designing with Qt library - static libraries
Summary(pl):	IDE s³u¿±ce do projektowania GUI za pomoc± biblioteki Qt - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtDesigner-devel = %{version}-%{release}

%description -n QtDesigner-static
IDE used for GUI designing with Qt library - static libraries.

%description -n QtDesigner-static -l pl
IDE s³u¿±ce do projektowania GUI za pomoc± biblioteki Qt - biblioteki
statyczne.

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

%package qmake
Summary:	Qt makefile generator
Summary(pl):	Generator plików makefile dla aplikacji Qt
Group:		X11/Development/Tools
Obsoletes:	qmake

%description qmake
A powerful makefile generator. It can create makefiles on any platform
from a simple .pro definitions file.

%description qmake -l pl
Rozbudowany generator plików makefile. Potrafi tworzyæ pliki makefile
na ka¿dej platformi na podstawie ³atwego w przygotowaniu pliku .pro.

%package qtconfig
Summary:	Qt widgets configuration tool
Summary(pl):	Narzêdzie do konfigurowania widgetów Qt
Group:		X11/Applications
Obsoletes:	qtconfig

%description qtconfig
A tool for configuring look and behavior of Qt widgets.

%description qtconfig -l pl
Narzêdie do konfiguracji wygl±du i zachowania widgetów Qt.

%package -n qvfb
Summary:	Qt Virtual framebuffer
Summary(pl):	Wirtualny framebuffer dla Qt
Group:		X11/Development/Libraries

%description -n qvfb
Qt Virtual framebuffer allows you to run Qt/Embedded applications in X
window.

%description -n qvfb -l pl
Qt Virtual framebuffer pozwala na uruchamianie aplikacji Qt/Embedded w
okienku X.

%package demos
Summary:	Demos of new Qt4 features
Summary(pl):	Programy demonstruj±ce nowe mo¿liwo¶ci Qt4
Group:		X11/Development/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

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
#Requires:	%{name}-devel = %{version}-%{release}

%description examples
Example programs bundled with Qt version.

%description examples -l pl
Æwiczenia/przyk³ady do³±czone do Qt.

%description examples -l pt_BR
Programas exemplo para o Qt versão.

%prep
%setup -q -n qt-x11-opensource-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%if %{with dont_enable}
%patch9 -p1
%patch10 -p1
%endif

# change QMAKE_CFLAGS_RELEASE to build
# properly optimized libs

if [ "%{_lib}" != "lib" ] ; then
	cfgf="mkspecs/linux-g++-64/qmake.conf"
else
	cfgf="mkspecs/linux-g++/qmake.conf"
fi

perl -pi -e "
	s|QMAKE_CC.*=.*gcc|QMAKE_CC = %{__cc}|;
	s|QMAKE_CXX.*=.*g\+\+|QMAKE_CXX = %{__cxx}|;
	s|QMAKE_LINK.*=.*g\+\+|QMAKE_LINK = %{__cxx}|;
	s|QMAKE_LINK_SHLIB.*=.*g\+\+|QMAKE_LINK_SHLIB = %{__cxx}|;
	s|QMAKE_INCDIR_QT.*|QMAKE_INCDIR_QT\t\t= %{_includedir}/qt4|;
	" $cfgf

cat $cfgf \
	|grep -v QMAKE_CFLAGS_RELEASE \
	|grep -v QMAKE_CXXFLAGS_RELEASE \
	|grep -v QMAKE_CFLAGS_DEBUG \
	|grep -v QMAKE_CXXFLAGS_DEBUG \
	> $cfgf.1

mv $cfgf.1 $cfgf
echo >> $cfgf
echo -e "QMAKE_CFLAGS_RELEASE\t= %{rpmcflags}" >> $cfgf
echo -e "QMAKE_CXXFLAGS_RELEASE\t= %{rpmcxxflags}" >> $cfgf
echo -e "QMAKE_CFLAGS_DEBUG\t= %{debugcflags}" >> $cfgf
echo -e "QMAKE_CXXFLAGS_DEBUG\t= %{debugcflags}" >> $cfgf

%build
# pass OPTFLAGS to build qmake itself with optimization
export OPTFLAGS="%{rpmcflags}"
export PATH=$PWD/bin:$PATH

##################################
# DEFAULT OPTIONS FOR ALL BUILDS #
##################################

COMMONOPT=" \
	-DQT_CLEAN_NAMESPACE \
	-verbose \
	-prefix %{_prefix} \
	-docdir %{_docdir}/%{name}-doc \
	-headerdir %{_includedir}/qt4 \
	-libdir %{_libdir} \
	-L%{_libdir} \
	-bindir %{_bindir} \
	-plugindir %{_libdir}/qt4/plugins \
	-datadir %{_datadir}/qt4 \
	-translationdir %{_datadir}/locale/ \
	-sysconfdir %{_sysconfdir}/qt4 \
	-examplesdir %{_examplesdir}/qt4 \
	-demosdir %{_examplesdir}/qt4-demos \
	-fast \
	-%{!?with_pch:no-}pch \
	-%{!?with_sse:no-}sse \
	-qt-gif \
	-system-libjpeg \
	-system-libpng \
	-system-zlib \
	-no-exceptions \
	-I%{_includedir}/postgresql/server \
	-I%{_includedir}/mysql \
	%{?with_cups:-cups} \
	%{?with_nas:-system-nas-sound} \
	%{?debug:-debug} \
	%{!?debug:-release} \
	-qt3support \
	-fontconfig \
	-nis \
	-sm \
	-tablet \
	-xcursor \
	-xkb \
	-xrender \
	-xshape"

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

echo "yes" | ./configure $COMMONOPT $OPT

%{__make} -C src
%{__make} -C tools/assistant/lib
%{__make} -C tools/designer/src/lib
if [ ! -d staticlib ]; then
	mkdir staticlib
	cp -a lib/*.a staticlib
fi
%{__make} confclean
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

echo "yes" | ./configure $COMMONOPT $OPT

%{__make}
%{__make} \
	sub-tools-all-ordered \
	sub-demos-all-ordered \
	sub-examples-all-ordered

%if %{with dont_enable}
%if %{with designer}
cd tools/designer/designer
lrelease designer_de.ts
lrelease designer_fr.ts
cd -
%endif
cd tools/assistant
lrelease assistant_de.ts
lrelease assistant_fr.ts
cd -
cd tools/linguist/linguist
lrelease linguist_de.ts
lrelease linguist_fr.ts
cd -
%endif

# kill -L/inside/builddir from *.la and *.pc (bug #77152)
%{__sed} -i -e "s,-L$PWD/lib,,g" lib/*.{la,pc,prl}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_libdir}/qt4/plugins/{crypto,network}

install plugins/sqldrivers/* $RPM_BUILD_ROOT%{_libdir}/qt4/plugins/sqldrivers
install bin/findtr tools/qvfb/qvfb $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}

install tools/qtconfig/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qtconfig.png

install tools/linguist/linguist/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/linguist.png

install tools/assistant/images/assistant.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/assistant.png

%if %{with designer}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install tools/designer/src/designer/images/designer.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/designer.png
%endif

%if %{with static_libs}
install staticlib/*.a $RPM_BUILD_ROOT%{_libdir}
%endif

install -d $RPM_BUILD_ROOT%{_datadir}/locale/{ar,cs,de,fr,ru,sk}/LC_MESSAGES
install translations/qt_ar.qm $RPM_BUILD_ROOT%{_datadir}/locale/ar/LC_MESSAGES/qt.qm
install translations/qt_cs.qm $RPM_BUILD_ROOT%{_datadir}/locale/cs/LC_MESSAGES/qt.qm
install translations/qt_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/qt.qm
install translations/qt_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/qt.qm
install translations/qt_ru.qm $RPM_BUILD_ROOT%{_datadir}/locale/ru/LC_MESSAGES/qt.qm
install translations/qt_sk.qm $RPM_BUILD_ROOT%{_datadir}/locale/sk/LC_MESSAGES/qt.qm
install tools/assistant/assistant_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/assistant.qm

%if %{with dont_enable}
%if %{with designer}
install tools/designer/designer/designer_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/designer.qm
install tools/designer/designer/designer_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/designer.qm
%endif

install tools/assistant/assistant_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/assistant.qm

install tools/linguist/linguist/linguist_de.qm $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/linguist.qm
install tools/linguist/linguist/linguist_fr.qm $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/linguist.qm
%endif

cd $RPM_BUILD_ROOT%{_includedir}/qt4/Qt
for f in ../Qt{3Support,Assistant,Core,Designer,Gui,Network,OpenGL,Sql,Svg,Test,Xml}/*
do
	if [ ! -d $f ]; then
		ln -sf $f `basename $f`
	fi
done
ln -sf ../../QtCore/arch/qatomic.h arch/qatomic.h
cd -

mv $RPM_BUILD_ROOT%{_libdir}/*.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
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
		return 1
	fi
}

mkdevfl () {
	MODULE=$1; shift
	echo "%%defattr(644,root,root,755)" > $MODULE-devel.files
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.so"
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.la"
	ifecho $MODULE-devel "%{_libdir}/lib$MODULE*.prl"
	ifecho $MODULE-devel "%{_pkgconfigdir}/$MODULE*.pc"
	if [ -d "$RPM_BUILD_ROOT%{_includedir}/qt4/$MODULE" ]; then
		ifecho $MODULE-devel %{_includedir}/qt4/$MODULE
	fi
	for f in `find $RPM_BUILD_ROOT%{_includedir}/qt4/$MODULE -printf "%%P "`
	do
		ifecho $MODULE-devel %{_includedir}/qt4/$MODULE/$f
		ifecho $MODULE-devel %{_includedir}/qt4/Qt/$f
	done
	for f in $@; do ifecho $MODULE-devel $f; done
}

mkdevfl QtCore %{_includedir}/qt4 %{_includedir}/qt4/Qt
mkdevfl QtGui
mkdevfl QtNetwork
mkdevfl QtOpenGL
mkdevfl QtSql
mkdevfl QtSvg
mkdevfl QtTest
mkdevfl QtXml
mkdevfl Qt3Support

# without *.la *.pc etc.
mkdevfl QtAssistant || /bin/true
mkdevfl QtDesigner || /bin/true

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt4
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt4 -printf "%%P "`
do
	ifecho examples %{_examplesdir}/qt4/$f
done

echo "%defattr(644,root,root,755)" > demos.files
ifecho demos "%{_examplesdir}/qt4-demos"
ifecho demos "%{_bindir}/qtdemo"
ifecho demos "%{_libdir}/qt4/plugins/arthurplugin/libarthurplugin.so"
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

%post	-n QtSvg	-p /sbin/ldconfig
%postun	-n QtSvg	-p /sbin/ldconfig

%post	-n QtTest	-p /sbin/ldconfig
%postun	-n QtTest	-p /sbin/ldconfig

%post	-n QtXml	-p /sbin/ldconfig
%postun	-n QtXml	-p /sbin/ldconfig

%post	-n Qt3Support	-p /sbin/ldconfig
%postun	-n Qt3Support	-p /sbin/ldconfig

%post	-n QtAssistant	-p /sbin/ldconfig
%postun	-n QtAssistant	-p /sbin/ldconfig

%post	designer-libs	-p /sbin/ldconfig
%postun	designer-libs	-p /sbin/ldconfig

%files -n QtCore
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtCore.so.*.*
%dir %{_libdir}/qt4
%dir %{_libdir}/qt4/plugins
%dir %{_libdir}/qt4/plugins/accessible
%dir %{_libdir}/qt4/plugins/codecs
%dir %{_libdir}/qt4/plugins/crypto
%dir %{_libdir}/qt4/plugins/imageformats
%dir %{_libdir}/qt4/plugins/network
%dir %{_libdir}/qt4/plugins/sqldrivers
%dir %{_datadir}/qt4
%lang(ar) %{_datadir}/locale/ar/LC_MESSAGES/qt.qm
%lang(cs) %{_datadir}/locale/cs/LC_MESSAGES/qt.qm
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt.qm
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/qt.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt.qm
%lang(sk) %{_datadir}/locale/sk/LC_MESSAGES/qt.qm

%files -n QtGui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtGui.so.*.*
%{_libdir}/qt4/plugins/accessible/*
%{_libdir}/qt4/plugins/codecs/*
%{_libdir}/qt4/plugins/imageformats/*

%files -n QtNetwork
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtNetwork.so.*.*

%files -n QtOpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtOpenGL.so.*.*

%files -n QtSql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSql.so.*.*

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
%exclude %{_libdir}/qt4/plugins/sqldrivers/libqsqlite2*.so
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

%files -n QtSvg
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtSvg.so.*.*

%files -n QtTest
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtTest.so.*.*

%files -n QtXml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtXml.so.*.*

%files -n Qt3Support
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uic3
%attr(755,root,root) %{_libdir}/libQt3Support.so.*.*

%files -n QtAssistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtAssistantClient.so.*.*

%files assistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/assistant
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/assistant.qm
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
%files designer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/designer
%{_desktopdir}/designer.desktop
%{_pixmapsdir}/designer.png

%files designer-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtDesigner*.so.*.*
%dir %{_libdir}/qt4/plugins/designer
%attr(755,root,root) %{_libdir}/qt4/plugins/designer/*.so
%endif

%files linguist
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/linguist
%attr(755,root,root) %{_bindir}/findtr
%attr(755,root,root) %{_bindir}/lrelease
%attr(755,root,root) %{_bindir}/lupdate
%attr(755,root,root) %{_bindir}/qm2ts
%{_datadir}/qt4/phrasebooks
%{_desktopdir}/linguist.desktop
%{_pixmapsdir}/linguist.png

%files qmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmake
%{_datadir}/qt4/mkspecs

%files qtconfig
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
%files -n QtDesigner-devel -f QtDesigner-devel.files
%files -n QtGui-devel -f QtGui-devel.files
%files -n QtNetwork-devel -f QtNetwork-devel.files
%files -n QtOpenGL-devel -f QtOpenGL-devel.files
%files -n QtSql-devel -f QtSql-devel.files
%files -n QtSvg-devel -f QtSvg-devel.files
%files -n QtTest-devel -f QtTest-devel.files
%files -n QtXml-devel -f QtXml-devel.files
%files -n Qt3Support-devel -f Qt3Support-devel.files
%files -n QtAssistant-devel -f QtAssistant-devel.files

%if %{with static_libs}
%files -n QtCore-static
%defattr(644,root,root,755)
%{_libdir}/libQtCore*.a

%files -n QtGui-static
%defattr(644,root,root,755)
%{_libdir}/libQtGui*.a

%files -n QtNetwork-static
%defattr(644,root,root,755)
%{_libdir}/libQtNetwork*.a

%files -n QtOpenGL-static
%defattr(644,root,root,755)
%{_libdir}/libQtOpenGL*.a

%files -n QtSql-static
%defattr(644,root,root,755)
%{_libdir}/libQtSql*.a

%files -n QtSvg-static
%defattr(644,root,root,755)
%{_libdir}/libQtSvg*.a

%files -n QtXml-static
%defattr(644,root,root,755)
%{_libdir}/libQtXml*.a

%files -n Qt3Support-static
%defattr(644,root,root,755)
%{_libdir}/libQt3Support*.a

%files -n QtDesigner-static
%defattr(644,root,root,755)
%{_libdir}/libQtDesigner.a

%files -n QtAssistant-static
%defattr(644,root,root,755)
%{_libdir}/libQtAssistantClient.a
%endif

%files demos -f demos.files
%files examples -f examples.files
