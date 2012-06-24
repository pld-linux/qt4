#
# TODO:
#	- better descriptions
#	- more cleanups
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
%bcond_with	pch		# enable pch in qmake
%bcond_with	sse		# use SSE instructions in gui/painting module

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
Summary(pt_BR):	Estrutura para rodar aplica��es GUI Qt
Name:		qt4
Version:	4.2.2
Release:	1
License:	GPL/QPL
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-src-%{version}.tar.gz
# Source0-md5:	19f6374fe7924e33775cb87ee02669cb
Source2:	%{name}-qtconfig.desktop
Source3:	%{name}-designer.desktop
Source4:	%{name}-assistant.desktop
Source5:	%{name}-linguist.desktop
Source6:	%{name}_pl.ts
Patch0:		%{name}-tools.patch
Patch2:		%{name}-buildsystem.patch
Patch3:		%{name}-locale.patch
Patch5:		%{name}-sse.patch
Patch6:		%{name}-antialias.patch
Patch7:		%{name}-support-cflags-with-commas.patch
Patch8:		%{name}-build-lib-static.patch
Patch9:		%{name}-x11_fonts.patch
URL:		http://www.trolltech.com/products/qt/
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	OpenGL-devel
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
# incompatible with bison
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	dbus-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	giflib-devel
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel >= 1.0.0
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
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
BuildConflicts:	QtCore-devel < %{version}
BuildConflicts:	QtCore < %{version}
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

%package -n QtCore
Summary:	Core classes used by other modules
Summary(pl):	Podstawowe klasy u�ywane przez inne modu�y
Group:		X11/Libraries

%description -n QtCore
Core classes used by other modules.

%description -n QtCore -l pl
Podstawowe klasy u�ywane przez inne modu�y.

%package -n QtCore-devel
Summary:	Core classes used by other modules - development files
Summary(pl):	Podstawowe klasy u�ywane przez inne modu�y - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	glib2-devel
Requires:	libstdc++-devel
Requires:	zlib-devel

%description -n QtCore-devel
Core classes used by other modules - development files.

%description -n QtCore-devel -l pl
Podstawowe klasy u�ywane przez inne modu�y - pliki programistyczne.

%package -n QtCore-static
Summary:	Core classes used by other modules - static libraries
Summary(pl):	Podstawowe klasy u�ywane przez inne modu�y - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}

%description -n QtCore-static
Core classes used by other modules - static libraries.

%description -n QtCore-static -l pl
Podstawowe klasy u�ywane przez inne modu�y - biblioteki statyczne.

%package -n QtGui
Summary:	Graphical User Interface components
Summary(pl):	Komponenty graficznego interfejsu u�ytkownika
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
# two following because of some plugins
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}

%description -n QtGui
Graphical User Interface components.

%description -n QtGui -l pl
Komponenty graficznego interfejsu u�ytkownika.

%package -n QtGui-devel
Summary:	Graphical User Interface components - development files
Summary(pl):	Komponenty graficznego interfejsu u�ytkownika - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	fontconfig-devel
Requires:	freetype-devel >= 1:2.0.0
Requires:	libpng-devel >= 2:1.0.8
Requires:	xcursor-devel
Requires:	xrender-devel

%description -n QtGui-devel
Graphical User Interface components - development files.

%description -n QtGui-devel -l pl
Komponenty graficznego interfejsu u�ytkownika - pliki programistyczne.

%package -n QtGui-static
Summary:	Graphical User Interface components - static libraries
Summary(pl):	Komponenty graficznego interfejsu u�ytkownika - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtGui-devel = %{version}-%{release}

%description -n QtGui-static
Graphical User Interface components - static libraries.

%description -n QtGui-static -l pl
Komponenty graficznego interfejsu u�ytkownika - biblioteki statyczne.

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
Summary(pl):	Klasy wspomagaj�ce OpenGL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtOpenGL
OpenGL support classes.

%description -n QtOpenGL -l pl
Klasy wspomagaj�ce OpenGL.

%package -n QtOpenGL-devel
Summary:	OpenGL support classes - development files
Summary(pl):	Klasy wspomagaj�ce OpenGL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}

%description -n QtOpenGL-devel
OpenGL support classes - development files.

%description -n QtOpenGL-devel -l pl
Klasy wspomagaj�ce OpenGL - pliki programistyczne.

%package -n QtOpenGL-static
Summary:	OpenGL support classes - static libraries
Summary(pl):	Klasy wspomagaj�ce OpenGL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtOpenGL-devel = %{version}-%{release}

%description -n QtOpenGL-static
OpenGL support classes - static libraries.

%description -n QtOpenGL-devel -l pl
Klasy wspomagaj�ce OpenGL - biblioteki statyczne.

%package -n QtSql
Summary:	Classes for database integration using SQL
Summary(pl):	Klasy do integracji z bazami danych przy u�yciu SQL
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtSql
Classes for database integration using SQL.

%description -n QtSql -l pl
Klasy do integracji z bazami danych przy u�yciu SQL.

%package -n QtSql-devel
Summary:	Classes for database integration using SQL - development files
Summary(pl):	Klasy do integracji z bazami danych przy u�yciu SQL - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}

%description -n QtSql-devel
Classes for database integration using SQL - development files.

%description -n QtSql-devel -l pl
Klasy do integracji z bazami danych przy u�yciu SQL - pliki
programistyczne.

%package -n QtSql-static
Summary:	Classes for database integration using SQL - static libraries
Summary(pl):	Klasy do integracji z bazami danych przy u�yciu SQL - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtSql-devel = %{version}-%{release}

%description -n QtSql-static
Classes for database integration using SQL - static libraries.

%description -n QtSql-static -l pl
Klasy do integracji z bazami danych przy u�yciu SQL - biblioteki
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
Ten pakiet zawiera wtyczki do Qt umo�liwiaj�ce korzystanie z baz
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
Ten pakiet zawiera wtyczki do Qt umo�liwiaj�ce korzystanie z baz
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
Ten pakiet zawiera wtyczki do Qt umo�liwiaj�ce korzystanie z us�ug
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
Ten pakiet zawiera wtyczki do Qt umo�liwiaj�ce korzystanie z baz
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
Ten pakiet zawiera wtyczki do Qt umo�liwiaj�ce korzystanie z baz
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
Ten pakiet zawiera wtyczki do Qt umo�liwiaj�ce korzystanie z baz
danych SQLite3 poprzez klasy QSql.

%description -n QtSql-sqlite3 -l pt_BR
Plugin de suporte a SQLite3 para Qt.

%package -n QtSvg
Summary:	SVG support
Summary(pl):	Wsparcie dla SVG
Group:		X11/Libraries
Requires:	QtXml = %{version}-%{release}

%description -n QtSvg
SVG support.

%description -n QtSvg -l pl
Wsparcie dla SVG.

%package -n QtSvg-devel
Summary:	SVG support - development files
Summary(pl):	Wsparcie dla SVG - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtSvg = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

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
Summary(pl):	Szkielet test�w
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtTest
Test framework.

%description -n QtTest -l pl
Szkielet test�w.

%package -n QtTest-devel
Summary:	Test framework - development files
Summary(pl):	Szkielet test�w - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtTest = %{version}-%{release}

%description -n QtTest-devel
Test framework - development files.

%description -n QtTest-devel -l pl
Szkielet test�w - pliki programistyczne.

%package -n QtXml
Summary:	Classes for handling XML
Summary(pl):	Klasy do obs�ugi XML-a
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}

%description -n QtXml
Classes for handling XML.

%description -n QtXml -l pl
Klasy do obs�ugi XML-a.

%package -n QtXml-devel
Summary:	Classes for handling XML - development files
Summary(pl):	Klasy do obs�ugi XML-a - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n QtXml-devel
Classes for handling XML - development files.

%description -n QtXml-devel -l pl
Klasy do obs�ugi XML-a - pliki programistyczne.

%package -n QtXml-static
Summary:	Classes for handling XML - static libraries
Summary(pl):	Klasy do obs�ugi XML-a - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtXml-devel = %{version}-%{release}

%description -n QtXml-static
Classes for handling XML - static libraries.

%description -n QtXml-static -l pl
Klasy do obs�ugi XML-a - biblioteki statyczne.

%package -n Qt3Support
Summary:	Qt3 compatibility library
Summary(pl):	Biblioteka kompatybilno�ci z Qt3
Group:		X11/Libraries
Requires:	QtCore = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n Qt3Support
Qt3 compatibility library.

%description -n Qt3Support -l pl
Biblioteka kompatybilno�ci z Qt3.

%package -n Qt3Support-devel
Summary:	Qt3 compatibility library - development files
Summary(pl):	Biblioteka kompatybilno�ci z Qt3 - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}
Requires:	QtNetwork-devel = %{version}-%{release}
Requires:	QtSql-devel = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}

%description -n Qt3Support-devel
Qt3 compatibility library - development files.

%description -n Qt3Support-devel -l pl
Biblioteka kompatybilno�ci z Qt3 - pliki programistyczne.

%package -n Qt3Support-static
Summary:	Qt3 compatibility library - static libraries
Summary(pl):	Biblioteka kompatybilno�ci z Qt3 - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	Qt3Support-devel = %{version}-%{release}

%description -n Qt3Support-static
Qt3 compatibility library - static libraries.

%description -n Qt3Support-static -l pl
Biblioteka kompatybilno�ci z Qt3 - biblioteki statyczne.

%package -n QtAssistant
Summary:	Qt Assistant client library
Summary(pl):	Biblioteka kliencka Qt Assistant
Group:		X11/Development/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}

%description -n QtAssistant
This library allows to use Qt Assistant as an application's help tool.

%description -n QtAssistant -l pl
Ta biblioteka umo�liwia wykorzystanie Qt Assistanta jako narz�dzie
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

%package -n QtDBus
Summary:	Classes for D-BUS support
Summary(pl):	Klasy do obs�ugi D-BUS
Group:		X11/Libraries
Requires:	QtXml = %{version}-%{release}
# is it really required? libs should need just libs, not service
#Requires:	dbus

%description -n QtDBus
This module provides classes for D-BUS support. D-BUS is an
Inter-Process Communication (IPC) and Remote Procedure Calling (RPC)
mechanism originally developed for Linux to replace existing and
competing IPC solutions with one unified protocol. 

%description -n QtDBus -l pl
Ten modu� udost�pnia klasy do obs�ugi D-BUS. D-BUS to mechanizm
komunikacji mi�dzy procesowej (IPC - Inter-Process Communication) i
zdalnego wywo�ywania procedur (RPC - Remote Procedure Calling)
stworzony pocz�tkowo dla Linuksa, aby zast�pi� istniej�ce i
konkuruj�ce ze sob� rozwi�zania IPC jednym, ujednoliconym protoko�em.

%package -n QtDBus-devel
Summary:	Classes for D-BUS support - development files
Summary(pl):	Klasy do obs�ugi D-BUS - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtDBus = %{version}-%{release}
Requires:	QtXml-devel = %{version}-%{release}
Requires:	dbus-devel
Requires:	glib2-devel >= 2.0.0

%description -n QtDBus-devel
Classes for D-BUS support - development files.

%description -n QtDBus-devel -l pl
Klasy do obs�ugi D-BUS - pliki programistyczne.

%package -n QtDBus-static
Summary:	Classes for D-BUS support - static libraries
Summary(pl):	Klasy do obs�ugi D-BUS - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtDBus-devel = %{version}-%{release}

%description -n QtDBus-static
Classes for D-BUS support - static libraries.

%description -n QtDBus-static -l pl
Klasy do obs�ugi D-BUS - biblioteki statyczne.

%package -n QtDesigner
Summary:	Classes for extending Qt Designer
Summary(pl):	Klasy do rozbudowy Qt Designera
Group:		X11/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}
Obsoletes:	qt4-designer-libs

%description -n QtDesigner
This module provides classes that allow you to create your own custom
widget plugins for Qt Designer, and classes that enable you to access
Qt Designer's components.

%description -n QtDesigner -l pl
Ten modu� dostarcza klasy, kt�re pozwalaj� tworzy� w�asne wtyczki dla
Qt Designera oraz klasy, kt�re umo�liwiaj� dost�p do jego komponent�w.

%package -n QtDesigner-devel
Summary:	Classes for extending Qt Designer - development files
Summary(pl):	Klasy do rozbudowy Qt Designera - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtDesigner = %{version}-%{release}
Requires:	QtGui-devel = %{version}-%{release}

%description -n QtDesigner-devel
Classes for extending Qt Designer - development files.

%description -n QtDesigner-devel -l pl
Klasy do rozbudowy Qt Designera - pliki programistyczne.

%package -n QtDesigner-static
Summary:	Classes for extending Qt Designer - static libraries
Summary(pl):	Klasy do rozbudowy Qt Designera - biblioteki statyczne
Group:		X11/Development/Libraries
Requires:	QtDesigner-devel = %{version}-%{release}

%description -n QtDesigner-static
Classes for extending Qt Designer - static libraries.

%description -n QtDesigner-static -l pl
Klasy do rozbudowy Qt Designera - biblioteki statyczne.

%package -n QtUiTools
Summary:	Classes for handling Qt Designer forms in applications
Summary(pl):	Klasy do obs�ugi formularzy Qt Designera w aplikacjach
Group:		X11/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description -n QtUiTools
The QtUiTools module provides classes to handle forms created with Qt
Designer.

%description -n QtUiTools -l pl
Modu� QtUiTools udost�pnia klasy do obs�ugi formularzy tworzonych przy
u�yciu Qt Designera.

%package -n QtUiTools-devel
Summary:	Classes for handling Qt Designer forms in applications - development files
Summary(pl):	Klasy do obs�ugi formularzy Qt Designera w aplikacjach - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtCore-devel = %{version}-%{release}
Requires:	QtUiTools = %{version}-%{release}

%description -n QtUiTools-devel
Classes for handling Qt Designer forms in applications - development
files.

%description -n QtUiTools-devel -l pl
Klasy do obs�ugi formularzy Qt Designera w aplikacjach - pliki
programistyczne.

%package -n QtUiTools-static
Summary:	Classes for handling Qt Designer forms in applications - static library
Summary(pl):	Klasy do obs�ugi formularzy Qt Designera w aplikacjach - biblioteka statyczna
Group:		X11/Development/Libraries
Requires:	QtUiTools-devel = %{version}-%{release}

%description -n QtUiTools-static
Classes for handling Qt Designer forms in applications - static
library.

%description -n QtUiTools-static -l pl
Klasy do obs�ugi formularzy Qt Designera w aplikacjach - biblioteka
statyczna.

%package assistant
Summary:	Qt documentation browser
Summary(pl):	Przegl�darka dokumentacji Qt
Group:		X11/Development/Tools
Requires:	%{name}-doc = %{version}-%{release}
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtDBus = %{version}-%{release}

%description assistant
Qt Assistant is a tool for browsing on-line documentation with
indexing, bookmarks and full-text search.

%description assistant -l pl
Qt Assistant to narz�dzie do przegl�dania dokumentacji z mo�liwo�ci�
indeksowania, dodawania zak�adek i pe�notekstowego wyszukiwania.

%package build
Summary:	Build tools for Qt4
Summary(pl):	Narz�dzia do budowania dla Qt4
Group:		X11/Development/Tools
Requires:	QtCore = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) and qt3to4 include names
converter.

%description build -l pl
Ten pakiet zawiera kompilator zasob�w Qt (rcc), kompilator
metaobiekt�w (moc), kompilator interfejs�w u�ytkownika (uic) oraz
konwerter nazw plik�w nag��wkowych qt3to4.

%package designer
Summary:	IDE used for GUI designing with Qt library
Summary(pl):	IDE s�u��ce do projektowania GUI za pomoc� biblioteki Qt
Group:		X11/Applications
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtDesigner = %{version}-%{release}

%description designer
An advanced tool used for GUI designing with Qt library.

%description designer -l pl
Zaawansowane narz�dzie s�u��ce do projektowania interfejsu graficznego
za pomoc� biblioteki Qt.

%package linguist
Summary:	Translation helper for Qt
Summary(pl):	Aplikacja u�atwiaj�ca t�umaczenie aplikacji oparty o Qt
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

%description linguist -l pl
Ten program oferuje interfejs znacznie przy�pieszaj�cy proces
t�umaczenia interfejsu u�ytkownika. Zbiera wszystkie teksty
przeznaczone do t�umaczenia i przedstawia w �atwym w obs�udze oknie.
Gdy jeden z nich jest ju� przet�umaczony, automatycznie przechodzi do
nast�pnego, a� wszystkie b�d� przet�umaczone.

%package qmake
Summary:	Qt makefile generator
Summary(pl):	Generator plik�w makefile dla aplikacji Qt
Group:		X11/Development/Tools

%description qmake
A powerful makefile generator. It can create makefiles on any platform
from a simple .pro definitions file.

%description qmake -l pl
Rozbudowany generator plik�w makefile. Potrafi tworzy� pliki makefile
na ka�dej platformi na podstawie �atwego w przygotowaniu pliku .pro.

%package qtconfig
Summary:	Qt widgets configuration tool
Summary(pl):	Narz�dzie do konfigurowania widget�w Qt
Group:		X11/Applications
Requires:	Qt3Support = %{version}-%{release}
Requires:	QtGui = %{version}-%{release}
Requires:	QtNetwork = %{version}-%{release}
Requires:	QtSql = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description qtconfig
A tool for configuring look and behavior of Qt widgets.

%description qtconfig -l pl
Narz�die do konfiguracji wygl�du i zachowania widget�w Qt.

%package -n qvfb
Summary:	Qt Virtual framebuffer
Summary(pl):	Wirtualny framebuffer dla Qt
Group:		X11/Development/Libraries
Requires:	QtGui = %{version}-%{release}
Requires:	QtOpenGL = %{version}-%{release}

%description -n qvfb
Qt Virtual framebuffer allows you to run Qt/Embedded applications in X
window.

%description -n qvfb -l pl
Qt Virtual framebuffer pozwala na uruchamianie aplikacji Qt/Embedded w
okienku X.

%package demos
Summary:	Demos of new Qt4 features
Summary(pl):	Programy demonstruj�ce nowe mo�liwo�ci Qt4
Group:		X11/Development/Libraries
Requires:	QtAssistant = %{version}-%{release}
Requires:	QtXml = %{version}-%{release}

%description demos
Demos are spiders that fly.

%description demos -l pl
Dema to lataj�ce paj�ki.

%package doc
Summary:	Qt Documentation in HTML format
Summary(pl):	Dokumentacja Qt w formacie HTML
Group:		X11/Development/Libraries

%description doc
Qt documentation in HTML format.

%description doc -l pl
Dokumentacja qt w formacie HTML.

%package examples
Summary:	Example programs bundled with Qt
Summary(pl):	�wiczenia i przyk�ady do Qt
Summary(pt_BR):	Programas exemplo desenvolvidos com o Qt
Group:		X11/Development/Libraries
# no it does not , we cant be sure the user wants to compile them right?
# he might just want to take a look, anwyay no single devel package now
#Requires:	%{name}-devel = %{version}-%{release}

%description examples
Example programs bundled with Qt version.

%description examples -l pl
�wiczenia/przyk�ady do��czone do Qt.

%description examples -l pt_BR
Programas exemplo para o Qt vers�o.

%prep
%setup -q -n qt-x11-opensource-src-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|QMAKE_CC.*=.*gcc|QMAKE_CC\t\t= %{__cc}|;
	s|QMAKE_CXX.*=.*g++|QMAKE_CXX\t\t= %{__cxx}|;
	s|QMAKE_LINK.*=.*g++|QMAKE_LINK\t\t= %{__cxx}|;
	s|QMAKE_LINK_SHLIB.*=.*g++|QMAKE_LINK_SHLIB\t= %{__cxx}|;
	s|QMAKE_CFLAGS_RELEASE.*|QMAKE_CFLAGS_RELEASE\t+= %{rpmcflags}|;
	s|QMAKE_CXXFLAGS_RELEASE.*|QMAKE_CXXFLAGS_RELEASE\t+= %{rpmcxxflags}|;
	s|QMAKE_CFLAGS_DEBUG.*|QMAKE_CFLAGS_DEBUG\t+= %{debugcflags}|;
	s|QMAKE_CXXFLAGS_DEBUG.*|QMAKE_CXXFLAGS_DEBUG\t+= %{debugcflags}|;
	' mkspecs/common/g++.conf

%{__sed} -i -e '
	s|QMAKE_INCDIR_QT.*|QMAKE_INCDIR_QT       = %{_includedir}/qt4|;
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
	-%{!?with_pch:no-}pch \
	-%{!?with_sse:no-}sse \
	-qdbus \
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
	-iconv \
	-no-separate-debug-info \
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
%{__make} -C tools/designer
%{__make} -C tools/qdbus/src
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_pkgconfigdir}}
install -d $RPM_BUILD_ROOT%{_qtdir}/plugins/{crypto,network}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# kill -L/inside/builddir from *.la and *.pc (bug #77152)
%{__sed} -i -e "s,-L$PWD/lib,,g" $RPM_BUILD_ROOT%{_libdir}/*.{la,pc,prl}
%{__sed} -i -e '
	s|moc_location=.*|moc_location=%{_bindir}/qt4-moc|;
	s|uic_location=.*|uic_location=%{_bindir}/qt4-uic|;
	' $RPM_BUILD_ROOT%{_libdir}/*.pc

# install tools
install bin/findtr	$RPM_BUILD_ROOT%{_qtdir}/bin
install bin/qvfb	$RPM_BUILD_ROOT%{_bindir}
install bin/pixeltool	$RPM_BUILD_ROOT%{_bindir}
install bin/qdbus	$RPM_BUILD_ROOT%{_bindir}
install bin/qdbuscpp2xml	$RPM_BUILD_ROOT%{_bindir}
install bin/qdbusxml2cpp	$RPM_BUILD_ROOT%{_bindir}

cd $RPM_BUILD_ROOT%{_bindir}
ln -sf ../%{_lib}/qt4/bin/assistant qt4-assistant
ln -sf ../%{_lib}/qt4/bin/designer qt4-designer
ln -sf ../%{_lib}/qt4/bin/linguist qt4-linguist
ln -sf ../%{_lib}/qt4/bin/moc qt4-moc
ln -sf ../%{_lib}/qt4/bin/qmake qt4-qmake
ln -sf ../%{_lib}/qt4/bin/qt3to4 .
ln -sf ../%{_lib}/qt4/bin/qtconfig qt4-qtconfig
ln -sf ../%{_lib}/qt4/bin/rcc .
ln -sf ../%{_lib}/qt4/bin/uic qt4-uic
ln -sf ../%{_lib}/qt4/bin/uic3 .
cd -

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}

install tools/qtconfig/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qt4-qtconfig.png

install tools/linguist/linguist/images/appicon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qt4-linguist.png

install tools/assistant/images/assistant.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qt4-assistant.png

install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install tools/designer/src/designer/images/designer.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/qt4-designer.png

%if %{with static_libs}
install staticlib/*.a $RPM_BUILD_ROOT%{_libdir}
%endif

#
# Locale
#
cp %{SOURCE6} translations/qt_pl.ts
LD_LIBRARY_PATH=lib bin/lrelease translations/qt_pl.ts -qm translations/qt_pl.qm

rm -f $RPM_BUILD_ROOT%{_datadir}/locale/*.qm
for file in translations/*.qm tools/assistant/*.qm tools/designer/designer/*.qm tools/linguist/linguist/*.qm
do
    [ ! -f $file ] && continue
    lang=`echo $file | sed -r 's:.*/[a-zA-Z]*_(.*).qm:\1:'`
    MOD=`echo $file | sed -r 's:.*/([a-zA-Z]*)_.*.qm:\1:'`
    [ "$lang" == "iw" ] && lang=he
    MOD=qt4-$MOD
    [ "$MOD" == "qt4-qt" ] && MOD=qt4
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES
    cp $file $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES/$MOD.qm
done

cd $RPM_BUILD_ROOT%{_includedir}/qt4/Qt
for f in ../Qt{3Support,Assistant,Core,DBus,Designer,Gui,Network,OpenGL,Sql,Svg,Test,UiTools,Xml}/*
do
	if [ ! -d $f ]; then
		ln -sf $f `basename $f`
	fi
done
cd -

# Ship doc & qmake stuff
ln -s %{_docdir}/%{name}-doc $RPM_BUILD_ROOT%{_qtdir}/doc
ln -s %{_datadir}/qt4/mkspecs $RPM_BUILD_ROOT%{_qtdir}/mkspecs

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
mkdevfl QtDBus %{_bindir}/qdbus %{_bindir}/qdbuscpp2xml %{_bindir}/qdbusxml2cpp
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
mkdevfl QtUiTools || /bin/true

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt4
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt4 -printf "%%P "`
do
	ifecho examples %{_examplesdir}/qt4/$f
done

echo "%defattr(644,root,root,755)" > demos.files
ifecho demos "%{_examplesdir}/qt4-demos"
ifecho demos "%{_qtdir}/bin/qtdemo"
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

%post	-n QtDBus	-p /sbin/ldconfig
%postun	-n QtDBus	-p /sbin/ldconfig

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

%post	-n QtDesigner	-p /sbin/ldconfig
%postun	-n QtDesigner	-p /sbin/ldconfig

%post	-n QtUiTools	-p /sbin/ldconfig
%postun	-n QtUiTools	-p /sbin/ldconfig

%files -n QtCore
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtCore.so.*.*
%dir %{_qtdir}
%dir %{_qtdir}/bin
%dir %{_qtdir}/plugins
%dir %{_qtdir}/plugins/accessible
%dir %{_qtdir}/plugins/codecs
%dir %{_qtdir}/plugins/crypto
%dir %{_qtdir}/plugins/iconengines
%dir %{_qtdir}/plugins/imageformats
%dir %{_qtdir}/plugins/inputmethods
%dir %{_qtdir}/plugins/network
%dir %{_qtdir}/plugins/sqldrivers
%dir %{_datadir}/qt4
%lang(ar) %{_datadir}/locale/ar/LC_MESSAGES/qt4.qm
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt4.qm
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/qt4.qm
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/qt4.qm
%lang(he) %{_datadir}/locale/he/LC_MESSAGES/qt4.qm
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/qt4.qm
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/qt4.qm
%lang(sk) %{_datadir}/locale/sk/LC_MESSAGES/qt4.qm
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/qt4.qm

%files -n QtDBus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtDBus.so.*.*

%files -n QtGui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtGui.so.*.*
%attr(755,root,root) %{_qtdir}/plugins/accessible/*.so
%attr(755,root,root) %{_qtdir}/plugins/codecs/*.so
%attr(755,root,root) %{_qtdir}/plugins/iconengines/*.so
%attr(755,root,root) %{_qtdir}/plugins/imageformats/*.so
%attr(755,root,root) %{_qtdir}/plugins/inputmethods/*.so

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
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlmysql*.so
%endif

%if %{with pgsql}
%files -n QtSql-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlpsql*.so
%endif

%if %{with sqlite}
%files -n QtSql-sqlite
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlite2*.so
%endif

%if %{with sqlite3}
%files -n QtSql-sqlite3
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlite*.so
%if %{with sqlite}
%exclude %{_qtdir}/plugins/sqldrivers/libqsqlite2*.so
%endif
%endif

%if %{with ibase}
%files -n QtSql-ibase
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlibase*.so
%endif

%if %{with odbc}
%files -n QtSql-odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_qtdir}/plugins/sqldrivers/libqsqlodbc*.so
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
%attr(755,root,root) %{_qtdir}/bin/uic3
%attr(755,root,root) %{_libdir}/libQt3Support.so.*.*

%files -n QtAssistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtAssistantClient.so.*.*

%files -n QtDesigner
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtDesigner*.so.*.*
%dir %{_qtdir}/plugins/designer
%attr(755,root,root) %{_qtdir}/plugins/designer/*.so

%files -n QtUiTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtUiTools.so.*.*

%files assistant
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pixeltool
%attr(755,root,root) %{_bindir}/qt4-assistant
%attr(755,root,root) %{_qtdir}/bin/assistant
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/qt4-assistant.qm
%{_desktopdir}/qt4-assistant.desktop
%{_pixmapsdir}/qt4-assistant.png

%files build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rcc
%attr(755,root,root) %{_bindir}/qt4-moc
%attr(755,root,root) %{_bindir}/qt3to4
%attr(755,root,root) %{_bindir}/qt4-uic
%attr(755,root,root) %{_qtdir}/bin/rcc
%attr(755,root,root) %{_qtdir}/bin/moc
%attr(755,root,root) %{_qtdir}/bin/qt3to4
%attr(755,root,root) %{_qtdir}/bin/uic
%{_datadir}/qt4/q3porting.xml

%files designer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qt4-designer
%attr(755,root,root) %{_qtdir}/bin/designer
%{_desktopdir}/qt4-designer.desktop
%{_pixmapsdir}/qt4-designer.png

%files linguist
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qt4-linguist
%attr(755,root,root) %{_qtdir}/bin/findtr
%attr(755,root,root) %{_qtdir}/bin/linguist
%attr(755,root,root) %{_qtdir}/bin/lrelease
%attr(755,root,root) %{_qtdir}/bin/lupdate
%{_datadir}/qt4/phrasebooks
%{_desktopdir}/qt4-linguist.desktop
%{_pixmapsdir}/qt4-linguist.png

%files qmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qt4-qmake
%attr(755,root,root) %{_qtdir}/bin/qmake
%{_datadir}/qt4/mkspecs
%{_qtdir}/mkspecs

%files qtconfig
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qt4-qtconfig
%attr(755,root,root) %{_qtdir}/bin/qtconfig
%{_desktopdir}/qt4-qtconfig.desktop
%{_pixmapsdir}/qt4-qtconfig.png

%files -n qvfb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qvfb

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc
%{_qtdir}/doc

%files -n QtCore-devel -f QtCore-devel.files
%files -n QtDBus-devel -f QtDBus-devel.files
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
%files -n QtUiTools-devel -f QtUiTools-devel.files

%if %{with static_libs}
%files -n QtCore-static
%defattr(644,root,root,755)
%{_libdir}/libQtCore*.a

%files -n QtDBus-static
%defattr(644,root,root,755)
%{_libdir}/libQtDBus*.a

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

%files -n QtAssistant-static
%defattr(644,root,root,755)
%{_libdir}/libQtAssistantClient.a

%files -n QtDesigner-static
%defattr(644,root,root,755)
%{_libdir}/libQtDesigner*.a

%files -n QtUiTools-static
%defattr(644,root,root,755)
%{_libdir}/libQtUiTools.a
%endif

%files demos -f demos.files
%files examples -f examples.files
