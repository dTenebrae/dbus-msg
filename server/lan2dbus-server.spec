Name:           lan2dbus-server
Version:        0.1
Release:        1%{?dist}
Summary:        Simple broadcasting app written in Python

License:        GPL
URL:            https://github.com/dtenebrae/dbus-msg

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
lan2dbus is a small messaging app written in Python 3, using dbus for showing message as popup window.

%build
pyinstaller --onefile %{_sourcedir}/lan2dbus-server.py

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 dist/lan2dbus-server %{buildroot}%{_bindir}/lan2dbus-server

%files
%{_bindir}/lan2dbus-server

%changelog
* Sat Jun 25 2022 Artem Chernyshev <dtenebrae@gmail.com> - 0.1-1
- Initial package

