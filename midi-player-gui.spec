Summary:        MIDI-Player-GUI client and server package
Name:           MIDI-Player-GUI
Version:        1.2.0el
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Base
URL:            https://github.com/Mormacill/MIDI-Player-GUI

Source0:        MIDI-Player-GUI-%{version}.tar.gz
# Later referring to github source https://github.com/Mormacill/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:      noarch

%description
MIDI-Player-GUI All-in-One package including midi files, GUI-dependencies like .xinitrc file and a plymouth splash screen

%package        client
Summary:        MIDI-Player-GUI client package

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
Requires:       systemd-udev

%description    client
MIDI-Player-GUI client package including midi files, GUI-dependencies like .xinitrc file and a plymouth splash screen and stuff for sending midi messages

%package        server
Summary:        MIDI-Player-GUI server package

Requires:       python-devel
Requires:       python-unversioned-command
Requires:       python-pip
Requires:       python-tkinter
Requires:       alsa-lib-devel
Requires:       gcc-c++
Requires:       xorg-x11-server-Xorg
Requires:       xorg-x11-xinit
Requires:       net-tools

%description    server
MIDI-Player-GUI server package including midi files, GUI-dependencies like .xinitrc file and stuff for receiving midi messages

%define themedir     %{_datadir}/plymouth/themes/mpg-organ
%define plymouthconf %{_sysconfdir}/plymouth/plymouthd.conf
%define optdir       /opt

%prep
%autosetup

%install
#Client
install -d %{buildroot}/%{themedir}
install -m 644 -p Client/plymouth/mpg-organ.plymouth -t %{buildroot}/%{themedir}
install -m 644 -p Client/plymouth/mpg-organ.script -t %{buildroot}/%{themedir}
install -m 644 -p Client/plymouth/mpg-splash.png -t %{buildroot}/%{themedir}

install -d %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Client/Source/midi.py -t %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Client/Source/mido-getDevice.py -t %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Client/midi-start-client.sh -t %{buildroot}/%{optdir}/%{name}

install -d %{buildroot}/%{optdir}/%{name}/Config
install -m 644 -p Config/xinitrc-client -t %{buildroot}/%{optdir}/%{name}/Config
install -m 644 -p Config/bashrc-client -t %{buildroot}/%{optdir}/%{name}/Config
install -m 644 -p README.md -t %{buildroot}/%{optdir}/%{name}

install -d %{buildroot}/%{optdir}/%{name}/Config/openbox
install -m 644 -p Config/openbox/autostart -t %{buildroot}/%{optdir}/%{name}/Config/openbox
install -m 644 -p Config/openbox/environment -t %{buildroot}/%{optdir}/%{name}/Config/openbox
install -m 644 -p Config/openbox/menu.xml -t %{buildroot}/%{optdir}/%{name}/Config/openbox
install -m 644 -p Config/openbox/rc.xml -t %{buildroot}/%{optdir}/%{name}/Config/openbox
install -m 644 -p Config/openbox/terminals.menu -t %{buildroot}/%{optdir}/%{name}/Config/openbox

install -d %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 644 -p Config/90-usb-automount.rules -t %{buildroot}/%{_sysconfdir}/udev/rules.d

#Server
install -d %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Server/Source/midi-receive.py -t %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Server/Source/midi-receive-GUI.py -t %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Server/Source/mido-getDevice.py -t %{buildroot}/%{optdir}/%{name}/Source
install -m 644 -p Server/midi-start-server.sh -t %{buildroot}/%{optdir}/%{name}

%files client
#Plymouth theme
%{themedir}/mpg-organ.plymouth
%{themedir}/mpg-organ.script
%{themedir}/mpg-splash.png

#Midi files
%{optdir}/%{name}/Source/midi.py
%{optdir}/%{name}/Source/mido-getDevice.py
%{optdir}/%{name}/midi-start-client.sh

#X files
%{optdir}/%{name}/Config/xinitrc-client
%{optdir}/%{name}/Config/bashrc-client
%{optdir}/%{name}/README.md

%{optdir}/%{name}/Config/openbox/autostart
%{optdir}/%{name}/Config/openbox/environment
%{optdir}/%{name}/Config/openbox/menu.xml
%{optdir}/%{name}/Config/openbox/rc.xml
%{optdir}/%{name}/Config/openbox/terminals.menu

#USB mount
%{_sysconfdir}/udev/rules.d/90-usb-automount.rules

%post client

%files server
#Midi files
%{optdir}/%{name}/Source/midi-receive.py
%{optdir}/%{name}/Source/midi-receive-GUI.py
%{optdir}/%{name}/Source/mido-getDevice.py
%{optdir}/%{name}/midi-start-server.sh

%post server

%changelog
* Wed Feb 11 2026 Morma Cill <> - 1.2.0el
- Created theme and other client stuff
