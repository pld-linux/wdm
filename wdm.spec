Summary:	WINGs Display Manager
Summary(pl):	Display Manager bazuj�cy na WING
Name:		wdm
Version:	1.19
Release:	2
License:	GPL
Group:		X11/XFree86
Source0:	http://www.tcscs.com/wdm/wdm/%{name}-%{version}.tar.gz
Source1:	xdm-3331.tar.gz
Source2:	%{name}.init
Source3:	%{name}.pamd
Source4:	%{name}-Xclients.in
Patch0:		%{name}-errmsg.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-wraster.patch
Patch3:		%{name}-pam.patch
Patch4:		%{name}-xdm3331.patch
URL:		http://www.tcscs.com/wdm/
BuildRequires:	autoconf
BuildRequires:	XFree86-devel >= 3.3.2
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
wdm is a modification/enhancement of XFree86's xdm which provides a
more flexible login panel while maintaining the basic xdm code to
interface with pam, etc.

The basic code uses XFree86 xdm with RedHat patches to implement pam.

This package is automake/autoconf based rather than Imake.

Xdm manages one more more X displays, which may be on the local host
or remote servers. wdm is an enhancement of the xdm distributed as
part of XFree86. It replaces the logon panel with an external "greet"
module (that is, a separate binary executable file). This separate
executable file has been implemented using the WindowMaker WINGs
widget library and the WindowMaker wraster graphics library.

The interface to the external routine supports passing a parameter to
the Xsession script (such as failsafe which just starts an xterm
window). This interface can be used (with a modified Xsession) to
specify the window manager to start.

Except for the pam configuration file which is /etc/pam.d/wdm, the
install location prefix of /usr/X11R6 is used. wdm's configuration
directory is /etc/X11/wdm.

Note: This rpm has been compiled assuming that the path for the wmaker
program is %{_bindir}/wmaker and the path for the afterstep program is
/usr/X11R6/bin/afterstep. If this is incorrect for your system, then
the file /etc/X11/wdm/Xclients must be modified to reflect the correct
locations.

Note: Additional window managers can be added by modifying the wdmWm
Xresources in the /etc/X11/wdm/wdm-config file and changing the
/etc/X11/wdm/Xclients file to start the added window managers.

Note: The rpm binary install process runs a post install script to
find window managers on the install system and update the wdm-config
and Xclients files. Although this shell script can do a reasonable
job, there is nothing like editing these files to tailor them to a
particular system. This script can be run manually if new window
managers are installed.

%description -l pl
wdm jest modyfikacj�/rozszerzeniem xdm dodaj�cym panel logowania o
wi�kszych mo�liwo�ciach. Panel jest oddzielnym programem
zaimplementowanym z u�yciem biblioteki widget�w WING z WindowMakera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1
cp -f %{PATCH3} patches/
cp -f %{SOURCE1} .
cp -f %{SOURCE4} src/config/Xclients.in

%build
autoconf
%configure \
	--enable-pam \
--with-wdmdir=%{_sysconfdir}/X11/wdm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,security}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/wdm
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/wdm
touch $RPM_BUILD_ROOT/etc/security/blacklist.wdm

gzip -9nf AUTHORS ChangeLog NEWS README README.pam TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
/etc/X11/wdm/wdmReconfig

%files
%defattr(644,root,root,755)
%doc {AUTHORS,ChangeLog,NEWS,README,README.pam,TODO}.gz
%attr(755,root,root) %{_bindir}/wdm
%attr(755,root,root) %{_bindir}/wdmLogin
%{_mandir}/man1/*

%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/wdm
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.wdm
%attr(754,root,root) /etc/rc.d/init.d/wdm

%dir %{_sysconfdir}/X11/wdm
%dir %{_sysconfdir}/X11/wdm/authdir
%config %{_sysconfdir}/X11/wdm/pixmaps
%config %{_sysconfdir}/X11/wdm/wdm-config
%config %{_sysconfdir}/X11/wdm/wdm-config.in
%config %{_sysconfdir}/X11/wdm/Xservers
%config %{_sysconfdir}/X11/wdm/Xresources
%config %{_sysconfdir}/X11/wdm/Xaccess
%attr(755,root,root) %config %{_sysconfdir}/X11/wdm/Xsetup_0
%attr(755,root,root) %config %{_sysconfdir}/X11/wdm/Xsession
%attr(755,root,root) %config %{_sysconfdir}/X11/wdm/Xclients
%attr(755,root,root) %config %{_sysconfdir}/X11/wdm/Xclients.in
%attr(755,root,root) %config %{_sysconfdir}/X11/wdm/TakeConsole
%attr(755,root,root) %config %{_sysconfdir}/X11/wdm/GiveConsole
%attr(755,root,root) %config %{_sysconfdir}/X11/wdm/wdmReconfig
