%define major		0
%define libname		%mklibname %name %major
%define libnamedev	%mklibname %name -d

%define cvs	20080814
%define rel	2

%if %cvs
%define release		%mkrel 0.%cvs.%rel
%define distname	%name-%cvs.tar.lzma
%define dirname		%name
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.bz2
%define dirname		%name-%version
%endif

%define build_opensync	1

Name: 	 	barry
Summary: 	Linux interface to RIM BlackBerry devices
Version: 	0.14
Release: 	%{release}
Source0:	http://ovh.dl.sourceforge.net/sourceforge/barry/%{distname}
# (austin) I made this icon (photo) myself.  I hope it's legal.
Source1:	bb128.png
Patch0:		barry-compile.patch
URL:		http://www.netdirect.ca/software/packages/barry/
License:	GPLv2+
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	ImageMagick
BuildRequires:	libusb-devel boost-devel openssl-devel
BuildRequires:	gtkmm2.4-devel libglademm2.4-devel
%if %build_opensync
BuildRequires:	libopensync-devel
%endif
BuildRequires:	libtar-devel

%description
Barry is a GPL C++ library for interfacing with the RIM BlackBerry Handheld.

It comes with a command line tool for exploring the device and a GUI for
making quick backups and udev rules which allow the device to be charged
via a USB port.

%package -n 	%{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n 	%{libnamedev}
Summary: 	Header files and static libraries from %{name}
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%{name}-devel

%description -n %{libnamedev}
Libraries and includes files for developing programs based on %{name}.

%package tools
Summary: BlackBerry(tm) Tools
Group: 	 Communications

%description tools
Barry is a desktop toolset for managing your BlackBerry(tm) device.
(BlackBerry is a registered trademark of Research in Motion Limited.)

This package contains the commandline tools btool, breset and others.

%package charge
Summary: BlackBerry(tm) Charging Scripts
Group:	 Communications

%description charge
This package installs special handshake and udev scripts which allow
a BlackBerry device to be charged via USB at 500mA.

%package gui
Summary: BlackBerry(tm) Backup Tool
Group: 	 Communications

%description gui
This package contains a graphical applications to backup and restore data
from a BlackBerry device.

%if %build_opensync
%package opensync
Summary: BlackBerry(tm) opensync plugin
Group:   Communications

%description opensync
Barry is a desktop toolset for managing your BlackBerry(tm) device.
(BlackBerry is a registered trademark of Research in Motion Limited.)

This package contains the opensync plugin to synchronize a BlackBerry with
other devices and applications.
%endif

%package ppp
Summary: BlackBerry(tm) PPP support utility and example scripts
Group: 	 Communications

%description ppp
This package contains a utility which enables the use of BlackBerry
devices as cellular data modems, and also contains example PPP scripts
for this purpose.

%prep
%setup -q -n %{dirname}
pushd gui/src
%patch0
popd

%build
%if %cvs
./buildgen.sh
%endif
%configure2_5x --enable-gui \
	--enable-boost \
%if %{build_opensync}
	--enable-opensync-plugin
%else
	--disable-opensync-plugin
%endif
%make
										
%install
rm -rf %{buildroot}
%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
cp udev/10-blackberry.rules %{buildroot}%{_sysconfdir}/udev/rules.d/
mkdir -p %{buildroot}%{_sysconfdir}/security/console.perms.d
cp udev/10-blackberry.perms %{buildroot}%{_sysconfdir}/security/console.perms.d/

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Barry Backup
Comment=Backup for BlackBerry devices
Exec=%{_bindir}/%{name}backup
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Utility;Office;PDA;
EOF

mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps
convert -scale 16 %{SOURCE1} %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 32 %{SOURCE1} %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 48 %{SOURCE1} %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 64 %{SOURCE1} %{buildroot}/%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -m 0644 %{SOURCE1} %{buildroot}/%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif
		
%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

%files tools
%doc AUTHORS ChangeLog NEWS README
%{_sbindir}/breset
%{_bindir}/btool
%{_bindir}/brecsum
%{_bindir}/upldif
%{_bindir}/bktrans
%{_bindir}/btranslate
%{_bindir}/bidentify
%{_mandir}/man1/btool*
%{_mandir}/man1/bidentify*
%{_mandir}/man1/bs11nread*
%{_mandir}/man1/brecsum*
%{_mandir}/man1/breset*
%{_mandir}/man1/upldif*

%files charge
%{_sbindir}/bcharge
%{_sysconfdir}/udev/rules.d/*
%{_sysconfdir}/security/console.perms.d/*
%{_mandir}/man1/bcharge*

%files gui
%doc gui/AUTHORS gui/ChangeLog gui/README gui/NEWS gui/TODO
%{_bindir}/barrybackup
%{_datadir}/barry/glade/*.glade
%{_datadir}/applications/*
%{_mandir}/man1/barrybackup*
%{_iconsdir}/*

%if %{build_opensync}
%files opensync
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*
%endif

%files ppp
%doc ppp/{README,barry-*}
%{_sbindir}/pppob
%{_mandir}/man1/pppob*

