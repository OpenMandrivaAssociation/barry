%define major 18
%define libname %mklibname %{name} %major
%define devname %mklibname %{name} -d

%define build_opensync 1

Summary:	Linux interface to RIM BlackBerry devices
Name:		barry
Version:	0.18.4
Release:	1
License:	GPLv2+
Group:		Communications
URL:		http://www.netdirect.ca/software/packages/barry/
Source0:	http://ovh.dl.sourceforge.net/sourceforge/barry/%{name}-%{version}.tar.bz2
# (austin) I made this icon (photo) myself.  I hope it's legal.
Source1:	bb128.png

BuildRequires:	imagemagick
BuildRequires:	pkgconfig(libusb)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	libglademm2.4-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libxml++-2.6)
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

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Requires:	%{name}-common >= %{version}

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n %{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%{name}-devel < %{version}-%{release} 

%description -n %{devname}
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

%build
%configure2_5x \
	--disable-static \
	--enable-gui \
	--enable-boost \
%if %{build_opensync}
	--enable-opensync-plugin
%else
	--disable-opensync-plugin
%endif
%make
										
%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
cp udev/{10,99}-blackberry*.rules %{buildroot}%{_sysconfdir}/udev/rules.d/

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

%find_lang %{name}-backup
%find_lang %{name}

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tools -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README
%{_sbindir}/breset
%{_bindir}/btool
%{_bindir}/brecsum
%{_bindir}/upldif
#%{_bindir}/bktrans
#%{_bindir}/btranslate
#%{_bindir}/brimtrans
%{_bindir}/btarcmp
#{_bindir}/bwatch
%{_bindir}/bidentify
%{_bindir}/bfuse
%{_bindir}/bdptest
%{_bindir}/bjavaloader
%{_bindir}/bjdwp
%{_bindir}/bs11nread
%{_bindir}/bjvmdebug
%{_bindir}/balxparse
%{_bindir}/bio
%{_bindir}/brawchannel
%{_bindir}/btardump
%{_mandir}/man1/btool*
%{_mandir}/man1/bidentify*
%{_mandir}/man1/bs11nread*
%{_mandir}/man1/brecsum*
%{_mandir}/man1/breset*
%{_mandir}/man1/upldif*
%{_mandir}/man1/bfuse*
%{_mandir}/man1/bjavaloader*
%{_mandir}/man1/bjdwp*
%{_mandir}/man1/balxparse*
%{_mandir}/man1/bio*
%{_mandir}/man1/brawchannel*
%{_mandir}/man1/btardump*
%{_mandir}/man1/bwatch*
%{_mandir}/man1/btarcmp*

%files charge
%{_sbindir}/bcharge
%{_sysconfdir}/udev/rules.d/*-blackberry*.rules
%{_mandir}/man1/bcharge*

%files gui -f %{name}-backup.lang
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
%doc ppp/README
%{_sbindir}/pppob
%{_mandir}/man1/pppob*
%{_sysconfdir}/ppp/chat-*
%{_sysconfdir}/ppp/peers/barry-*

%files common
%{_sysconfdir}/udev/rules.d/69-blackberry.rules
