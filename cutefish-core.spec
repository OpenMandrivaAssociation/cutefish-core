%define oname core

Name:           cutefish-core
Version:        0.7
Release:        1
Summary:        System backend and start session for Cutefish
License:        GPL-3.0-or-later
Group:          System/X11/Other
URL:            https://github.com/cutefishos/core
Source:         https://github.com/cutefishos/core/archive/refs/tags/%{version}/%{oname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  cmake(KF5CoreAddons)
BuildRequires:  cmake(KF5GlobalAccel)
BuildRequires:  cmake(KF5WindowSystem)
BuildRequires:	cmake(KF5IdleTime)
BuildRequires:  cmake(FishUI)
BuildRequires:  cmake(PolkitQt5-1)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(ECM)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5QuickControls2)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:	pkgconfig(xcb-cursor)
BuildRequires:  pkgconfig(xcb-damage)
BuildRequires:	pkgconfig(xcb-ewmh)
BuildRequires:	pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:	pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xorg-libinput)
BuildRequires:  pkgconfig(xorg-server)
BuildRequires:  pkgconfig(xorg-synaptics)
BuildRequires:  pkgconfig(xtst)

Requires:       cutefish-kwin-plugins
Requires:       cutefish-qt-plugins
Requires:       fishui
Requires:       kwin
Recommends:     kscreen5
Recommends:     cutefish-wallpapers

%description
Cutefish WorkSpace - System backend and start session and more.


%prep
%autosetup -n %{oname}-%{version} -p1
#ed -i 's/\(QHotkey \)QHotkey/\1qhotkey/' hotkeys/CMakeLists.txt
sed -i 's/^\(Type=\).*$/\1XSession/' session/cutefish-xsession.desktop

%build
%cmake
%make_build

%install
%make_install -C build

install -dm 0755 %{buildroot}%{_sysconfdir}/xdg/cutefishos

%find_lang %{name} --with-qt --all-name

# xsession default selector
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
touch %{buildroot}%{_sysconfdir}/alternatives/default-xsession.desktop
ln -s %{_sysconfdir}/alternatives/default-xsession.desktop %{buildroot}%{_datadir}/xsessions/default.desktop

%post
%{_sbindir}/update-alternatives --install %{_datadir}/xsessions/default.desktop \
  default-xsession.desktop %{_datadir}/xsessions/cutefish-xsession.desktop 20

%postun
[ -f %{_datadir}/xsessions/cutefish-xsession.desktop ] || %{_sbindir}/update-alternatives \
  --remove default-xsession.desktop %{_datadir}/xsessions/cutefish-xsession.desktop

%files -f %{name}.lang
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/xdg/cutefishos
#config(noreplace) #{_sysconfdir}/xdg/cutefishos/theme.conf
%config %{_sysconfdir}/cutefish
%{_bindir}/chotkeys
%{_bindir}/cupdatecursor
%{_bindir}/cutefish-cpufreq
%{_bindir}/cutefish-gmenuproxy
%{_bindir}/cutefish-notificationd
%{_bindir}/cutefish-polkit-agent
%{_bindir}/cutefish-powerman
%{_bindir}/cutefish-screen-brightness
%{_bindir}/cutefish-sddm-helper
%{_bindir}/cutefish-session
%{_bindir}/cutefish-settings-daemon
%{_bindir}/cutefish-shutdown
%{_bindir}/cutefish-xembedsniproxy
%{_sysconfdir}/xdg/autostart/cutefish-polkit-agent.desktop
#_sysconfdir}/xdg/autostart/cutefish-settings-daemon.desktop
%{_datadir}/polkit-1/actions/com.cutefish.brightness.pkexec.policy
%ghost %{_sysconfdir}/alternatives/default-xsession.desktop
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/com.cutefish.cpufreq.pkexec.policy
%{_datadir}/polkit-1/actions/com.cutefish.sddm.helper.pkexec.policy
%{_datadir}/xsessions/default.desktop
%{_datadir}/xsessions/cutefish-xsession.desktop
%{_userunitdir}/cutefish-gmenuproxy.service
