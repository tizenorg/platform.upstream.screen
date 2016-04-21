#
# spec file for package screen
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Url:            http://www.gnu.org/software/screen/

Name:           screen
BuildRequires:  makeinfo
BuildRequires:  ncurses-devel
BuildRequires:  utempter-devel
Requires(pre):  coreutils
Version:        4.2.0
Release:        0
Summary:        A program to allow multiple screens on a VT100/ANSI Terminal
License:        GPL-3.0
Group:          System/Utilities
Source:         %{name}-%{version}.tar.gz
Source1:        screen.conf
Source1001:     screen.manifest

%if ! %{?license:0}
%define license %doc
%endif


%description
With this program you can take advantage of the multitasking abilities
of your Linux system by opening several sessions over one terminal. The
sessions can also be detached and resumed from another login terminal.

Documentation: man page

%prep
%setup
cp %{SOURCE1001} .

%build
CFLAGS="-DMAXWIN=1000 $RPM_OPT_FLAGS" %reconfigure --prefix=/usr --infodir=%{_infodir} \
                --mandir=%{_mandir} \
                --with-socket-dir='(eff_uid ? "/var/run/uscreens" : "/var/run/screens")' \
                --with-sys-screenrc=/etc/screenrc \
                --with-pty-group=5 \
                --enable-use-locale \
                --enable-colors256 \
                --verbose
%__make -j1

%install
%make_install
rm -f $RPM_BUILD_ROOT/usr/bin/screen
mv $RPM_BUILD_ROOT/usr/bin/screen-%version $RPM_BUILD_ROOT/usr/bin/screen
chmod 755 $RPM_BUILD_ROOT/usr/bin/screen
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/usr/lib/tmpfiles.d
mkdir -p $RPM_BUILD_ROOT/var/run/screens
chmod 755 $RPM_BUILD_ROOT/var/run/screens
mkdir -p $RPM_BUILD_ROOT/var/run/uscreens
chmod 1777 $RPM_BUILD_ROOT/var/run/uscreens
install -m 644 screenrc $RPM_BUILD_ROOT/etc/screenrc
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%post
# Create our dirs immediatly, after a manual package install.
# After a reboot systemd/aaa_base will take care.
test -d /var/run/screens || mkdir -m 755 /var/run/screens
test -d /var/run/uscreens || mkdir -m 1777 /var/run/uscreens


%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%config %{_sysconfdir}/screenrc
%attr(555,root,root) %{_bindir}/screen
%dir /usr/share/screen
%dir /usr/lib/tmpfiles.d
/%{_prefix}/lib/tmpfiles.d/screen.conf
%{_datadir}/%{name}/utf8encodings
# Created via aaa_base or systemd on system boot
%ghost %dir /var/run/screens
%ghost %dir /var/run/uscreens
%doc %{_infodir}/screen.info*.gz
%doc %{_mandir}/man1/screen.1.gz
