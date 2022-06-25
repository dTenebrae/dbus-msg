Name:           lan2dbus-client
Version:        0.1
Release:        1%{?dist}
Summary:        Simple broadcasting app written in Python

License:        GPL
URL:            https://github.com/dtenebrae/dbus-msg

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  dbus-devel
BuildRequires:  glib2-devel
Requires:       systemd

%description
lan2dbus is a small messaging app written in Python 3, using dbus for showing message as popup window.

%build
pyinstaller --onefile %{_sourcedir}/lan2dbus-client.py

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
install -m 755 dist/lan2dbus-client %{buildroot}%{_bindir}/lan2dbus-client
install -m 755 %{_sourcedir}/l2dbclient.service %{buildroot}%{_unitdir}/l2dbclient.service
install -m 755 %{_sourcedir}/l2dbclient.timer %{buildroot}%{_unitdir}/l2dbclient.timer

%files
%{_bindir}/lan2dbus-client
%{_unitdir}/l2dbclient.service
%{_unitdir}/l2dbclient.timer

%changelog
* Sat Jun 25 2022 Artem Chernyshev <dtenebrae@gmail.com> - 0.1-1
- Initial package

