%define major		0
%define libname		%mklibname %name %major
%define libnamedev	%mklibname %name -d

%define cvs	0
%define rel	1

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
Version: 	0.16
Release: 	%{release}
Source0:	http://ovh.dl.sourceforge.net/sourceforge/barry/%{distname}
# (austin) I made this icon (photo) myself.  I hope it's legal.
Source1:	bb128.png
# (fc) 0.16-1mdv fix build (GIT)
Patch0:		barry-0.16-fixbuild.patch
# (fc) 0.16-1mdv fix udev ACL (GIT) (Mdv bug #56664)
Patch1:		barry-0.16-udevacl.patch
URL:		http://www.netdirect.ca/software/packages/barry/
License:	GPLv2+
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	imagemagick
BuildRequires:	libusb-devel
BuildRequires:	boost-devel
BuildRequires:	gtkmm2.4-devel
BuildRequires:	libglademm2.4-devel
BuildRequires:  gettext-devel
%if %build_opensync
BuildRequires:	libopensync-devel
%endif
BuildRequires:	libtar-devel
BuildRequires:	fuse-devel

%description
Barry is a GPL C++ library for interfacing with the RIM BlackBerry Handheld.

It comes with a command line tool for exploring the device and a GUI for
making quick backups and udev rules which allow the device to be charged
via a USB port.

%package -n 	%{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries
Requires:	%{name}-common >= %{version}

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n 	%{libnamedev}
Summary: 	Header files and static libraries from %{name}
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%{name}-devel

%description -n %{libnamedev}
Libraries and includes files for developing programs based on %{name}.

%package tools
Summary:	BlackBerry(tm) Tools
Group:		Communications

%description tools
Barry is a desktop toolset for managing your BlackBerry(tm) device.
(BlackBerry is a registered trademark of Research in Motion Limited.)

This package contains the commandline tools btool, breset and others.

%package common
Summary:	BlackBerry(tm) common files
Group:		Communications

%description common
Common files used by Barry.

%package charge
Summary:	BlackBerry(tm) Charging Scripts
Group:		Communications

%description charge
This package installs special handshake and udev scripts which allow
a BlackBerry device to be charged via USB at 500mA.

%package gui
Summary:	BlackBerry(tm) Backup Tool
Group:		Communications

%description gui
This package contains a graphical applications to backup and restore data
from a BlackBerry device.

%if %build_opensync
%package opensync
Summary:	BlackBerry(tm) opensync plugin
Group:		Communications

%description opensync
Barry is a desktop toolset for managing your BlackBerry(tm) device.
(BlackBerry is a registered trademark of Research in Motion Limited.)

This package contains the opensync plugin to synchronize a BlackBerry with
other devices and applications.
%endif

%package ppp
Summary:	BlackBerry(tm) PPP support utility and example scripts
Group:		Communications

%description ppp
This package contains a utility which enables the use of BlackBerry
devices as cellular data modems, and also contains example PPP scripts
for this purpose.

%prep
%setup -q 
%patch0 -p1 -b .fixbuild
%patch1 -p1 -b .udevacl

#needed by patch0
autoreconf -i

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
cp udev/{10,69}-blackberry.rules %{buildroot}%{_sysconfdir}/udev/rules.d/

mkdir -p %{buildroot}%{_sysconfdir}/ppp/peers
for i in o2ireland rogers sprint tmobileus verizon; do \
	install -m 0644 ppp/barry-$i %{buildroot}%{_sysconfdir}/ppp/peers/barry-$i; \
	install -m 0644 ppp/barry-$i.chat %{buildroot}%{_sysconfdir}/ppp/chat-barry-$i; \
done
# I know this is ugly, but I don't know how to use $i within a sed
# command. If you do, just do the obvious to do this all in one sed
# command in the loop above - AdamW 2008/09
sed -i -e 's,chatscripts/barry-,ppp/chat-barry-,g' %{buildroot}%{_sysconfdir}/ppp/peers/barry-*
sed -i -e 's,\.chat,,g' %{buildroot}%{_sysconfdir}/ppp/peers/barry-*

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
%{_libdir}/*.*a
%{_libdir}/pkgconfig/*.pc

%files tools
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%{_sbindir}/breset
%{_bindir}/btool
%{_bindir}/brecsum
%{_bindir}/upldif
%{_bindir}/bktrans
%{_bindir}/btranslate
%{_bindir}/bidentify
%{_bindir}/bfuse
%{_bindir}/bdptest
%{_bindir}/bjavaloader
%{_bindir}/bjdwp
%{_bindir}/brimtrans
%{_bindir}/bs11nread
%{_bindir}/bjvmdebug
%{_mandir}/man1/btool*
%{_mandir}/man1/bidentify*
%{_mandir}/man1/bs11nread*
%{_mandir}/man1/brecsum*
%{_mandir}/man1/breset*
%{_mandir}/man1/upldif*
%{_mandir}/man1/bfuse*
%{_mandir}/man1/bjavaloader*
%{_mandir}/man1/bjdwp*

%files charge
%defattr(-,root,root)
%{_sbindir}/bcharge
%{_sysconfdir}/udev/rules.d/10-blackberry.rules
%{_mandir}/man1/bcharge*

%files gui
%defattr(-,root,root)
%doc gui/AUTHORS gui/ChangeLog gui/README gui/NEWS gui/TODO
%{_bindir}/barrybackup
%{_datadir}/barry/glade/*.glade
%{_datadir}/applications/*
%{_mandir}/man1/barrybackup*
%{_iconsdir}/*

%if %{build_opensync}
%files opensync
%defattr(-,root,root)
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*
%endif

%files ppp
%defattr(-,root,root)
%doc ppp/README
%{_sbindir}/pppob
%{_mandir}/man1/pppob*
%{_sysconfdir}/ppp/chat-*
%{_sysconfdir}/ppp/peers/barry-*

%files common
%defattr(-,root,root)
%{_sysconfdir}/udev/rules.d/69-blackberry.rules
