Summary:        MIDI-Player-GUI All-in-One package
Name:           MIDI-Player-GUI
Version:        1.2.0el
Release:        1%{?dist}
License:        GPLv2+
Group:          System Environment/Base
URL:            https://github.com/Mormacill/MIDI-Player-GUI

Source0:        MIDI-Player-GUI-%{version}.tar.gz
# Later referring to github source https://github.com/Mormacill/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:      noarch

Requires:       python-devel
Requires:       python-unversioned-command
Requires:       python-pip
Requires:       python-tkinter
Requires:       alsa-lib-devel
Requires:       gcc-c++
Requires:       xorg-x11-server-Xorg
Requires:       xorg-x11-xinit
Requires:       openbox
Requires:       plymouth
Requires:       plymouth-plugin-script
Requires:       plymouth-graphics-libs
Requires:       net-tools
#BuildRequires:

%define themedir     %{_datadir}/plymouth/themes/mpg-organ
%define plymouthconf %{_sysconfdir}/plymouth/plymouthd.conf
%define optdir       /opt

%description
MIDI-Player-GUI All-in-One package including midi files, GUI-dependencies like .xinitrc file and a plymouth splash screen

%prep
%autosetup

%install

install -d %{buildroot}/%{themedir}
install -m 644 -p Client/plymouth/mpg-organ.plymouth -t %{buildroot}/%{themedir}
install -m 644 -p Client/plymouth/mpg-organ.script -t %{buildroot}/%{themedir}
install -m 644 -p Client/plymouth/mpg-splash.png -t %{buildroot}/%{themedir}

install -d %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Client/Source/midi.py -t %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Client/Source/mido-getDevice.py -t %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Client/midi-start.sh -t %{buildroot}/%{optdir}/%{name}

%files
#Plymouth theme
%{themedir}/mpg-organ.plymouth
%{themedir}/mpg-organ.script
%{themedir}/mpg-splash.png

#Midi files
%{optdir}/%{name}/Source/midi.py
%{optdir}/%{name}/Source/mido-getDevice.py
%{optdir}/%{name}/midi-start.sh

%post
%{_bindir}/plymouth-set-default-theme mpg-organ

%{_bindir}/pip install mido python-rtmidi

%changelog
* Wed Mar 06 2024 Klemen Klemar <klemen.klemar@hotmail.com> - 1.0.0
- Created the theme
