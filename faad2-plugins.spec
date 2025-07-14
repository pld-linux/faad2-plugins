#
# Conditional build:
%bcond_with	mpeg4ip		# MPEG4IP plugin
%bcond_without	xmms		# XMMS plugin

Summary:	Freeware Advanced Audio Decoder 2 plugins
Summary(pl.UTF-8):	Wtyczki kodeka Freeware Advanced Audio Decoder 2
Name:		faad2-plugins
Version:	2.10.1
Release:	2
License:	GPL v2+
Group:		Applications/Sound
#Source0:	http://downloads.sourceforge.net/faac/%{name}-%{version}.tar.gz
#Source0Download: https://github.com/knik0/faad2/releases
Source0:	https://github.com/knik0/faad2/archive/%{version}/faad2-%{version}.tar.gz
# Source0-md5:	62a0427c6ff3a273aa720e27da166758
Patch0:		faad2-make.patch
Patch1:		faad2-mpeg4ip.patch
Patch3:		faad2-backward_compat.patch
Patch4:		faad2-mp4ff.patch
Patch5:		faad2-mp4v2.patch
URL:		https://www.audiocoding.com/
%{?with_mpeg4ip:BuildRequires:	SDL-devel}
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_xmms:BuildRequires:	id3lib-devel >= 3.8.2}
BuildRequires:	libtool >= 2:1.4d-3
%{?with_xmms:BuildRequires:	mp4ff-devel}
%if %{with mpeg4ip}
BuildRequires:	mp4v2-devel
BuildRequires:	mpeg4ip-devel >= 1:1.6
%endif
BuildRequires:	rpmbuild(macros) >= 1.721
%{?with_xmms:BuildRequires:	xmms-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.

%description -l pl.UTF-8
FAAD 2 to napisany całkowicie od początku dekoder MPEG2 i MPEG-4
obsługujący profile LC, MAIN i LTP.

%package -n mpeg4ip-plugin-faad2
Summary:	MPEG4IP plugin for AAC files
Summary(pl.UTF-8):	Wtyczka MPEG4IP do plików AAC
Group:		Applications/Sound
Requires:	faad2-libs >= %{version}
Requires:	mpeg4ip

%description -n mpeg4ip-plugin-faad2
MPEG4IP plugin for AAC files.

%description -n mpeg4ip-plugin-faad2 -l pl.UTF-8
Wtyczka MPEG4IP do plików AAC.

%package -n xmms-input-faad2
Summary:	XMMS plugin for AAC files
Summary(pl.UTF-8):	Wtyczka XMMS do plików AAC
Group:		X11/Applications/Sound
Requires:	faad2-libs >= %{version}
Requires:	xmms

%description -n xmms-input-faad2
XMMS plugin for AAC files.

%description -n xmms-input-faad2 -l pl.UTF-8
Wtyczka XMMS do plików AAC.

%prep
%setup -q -n faad2-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--with-xmms%{!?with_xmms:=no} \
	--with-mpeg4ip%{!?with_mpeg4ip:=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/faad
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfaad*
%{__rm} $RPM_BUILD_ROOT%{_includedir}/*.h
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/faad2.pc
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/faad.1

%if %{with xmms}
%{__rm} $RPM_BUILD_ROOT%{xmms_input_plugindir}/*.la
%endif
%if %{with mpeg4ip}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mp4player_plugin/*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with xmms}
%files -n xmms-input-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/libmp4.so
%endif

%if %{with mpeg4ip}
%files -n mpeg4ip-plugin-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mp4player_plugin/faad2_plugin.so*
%endif
