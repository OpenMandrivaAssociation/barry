%define name	barry
%define version	0.8
%define release %mkrel 1

%define major	0
%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d

Name: 	 	%{name}
Summary: 	Linux interface to RIM BlackBerry devices
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
# (austin) I made this icon (photo) myself.  I hope it's legal.
Source1:	bb128.png
Patch:		barry-compile.patch
URL:		http://www.netdirect.ca/software/packages/barry/
License:	GPL
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	ImageMagick
BuildRequires:	libusb-devel boost-devel openssl-devel
BuildRequires:	gtkmm2.4-devel libglademm2.4-devel
BuildRequires:	opensync-devel
BuildRequires:	libtar-devel

%description
Barry is a GPL C++ library for interfacing with the RIM BlackBerry Handheld.

It comes with a command line tool for exploring the device and a GUI for
making quick backups and udev rules which allow the device to be charged
via a USB port.

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %name.

%package -n 	%{libnamedev}
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libnamedev}
Libraries and includes files for developing programs based on %name.

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

%package opensync
Summary: BlackBerry(tm) opensync plugin
Group:   Communications

%description opensync
Barry is a desktop toolset for managing your BlackBerry(tm) device.
(BlackBerry is a registered trademark of Research in Motion Limited.)

This package contains the opensync plugin to synchronize a BlackBerry with
other devices and applications.

%prep
%setup -q
cd gui/src
%patch

%build
%configure2_5x
%make
cd gui
%configure2_5x  PKG_CONFIG_PATH="..:$PKG_CONFIG_PATH" CXXFLAGS="-I../.." LDFLAGS="-L../../src"
%make
cd ../opensync-plugin
%configure2_5x  PKG_CONFIG_PATH="..:$PKG_CONFIG_PATH" CXXFLAGS="-I../.." LDFLAGS="-L../../src"
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
cp udev/10-blackberry.rules %{buildroot}%{_sysconfdir}/udev/rules.d/
mkdir -p %{buildroot}%{_sysconfdir}/security/console.perms.d
cp udev/10-blackberry.perms %{buildroot}%{_sysconfdir}/security/console.perms.d/
cd gui
%makeinstall_std
cd ../opensync-plugin
%makeinstall_std

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Barry Backup
Comment=Backup for BlackBerry devices
Exec=%{_bindir}/%{name}backup
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Utility;Office;PDA;X-MandrivaLinux-Office-Communications-Phone;
EOF

# old icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 %SOURCE1 $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 %SOURCE1 $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 %SOURCE1 $RPM_BUILD_ROOT/%_miconsdir/%name.png

mkdir -p %buildroot/%_iconsdir/hicolor/16x16/apps
convert %SOURCE1 $RPM_BUILD_ROOT/%_iconsdir/hicolor/16x16/apps/%name.png
mkdir -p %buildroot/%_iconsdir/hicolor/32x32/apps
convert %SOURCE1 $RPM_BUILD_ROOT/%_iconsdir/hicolor/32x32/apps/%name.png
mkdir -p %buildroot/%_iconsdir/hicolor/48x48/apps
convert %SOURCE1 $RPM_BUILD_ROOT/%_iconsdir/hicolor/48x48/apps/%name.png
mkdir -p %buildroot/%_iconsdir/hicolor/64x64/apps
convert %SOURCE1 $RPM_BUILD_ROOT/%_iconsdir/hicolor/64x64/apps/%name.png
mkdir -p %buildroot/%_iconsdir/hicolor/128x128/apps
cp %SOURCE1 $RPM_BUILD_ROOT/%_iconsdir/hicolor/128x128/apps/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

%files tools
%doc AUTHORS ChangeLog COPYING NEWS README
%{_sbindir}/breset
%{_sbindir}/pppob
%{_bindir}/btool
%{_bindir}/upldif
%{_bindir}/ktrans
%{_bindir}/translate
%{_mandir}/man1/btool*

%files charge
%{_sbindir}/bcharge
%{_sysconfdir}/udev/rules.d/*
%{_sysconfdir}/security/console.perms.d/*
%{_mandir}/man1/bcharge*

%files gui
%doc gui/AUTHORS gui/ChangeLog gui/COPYING gui/README gui/NEWS gui/TODO
%{_bindir}/barrybackup
%{_datadir}/barry/glade/*.glade
%{_datadir}/applications/*
%{_iconsdir}/*

%files opensync
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*
