Summary:	CVSspam emails you diffs when someone commits a change to your CVS repository
Summary(pl.UTF-8):	CVSspam - wysyłanie różnic po wykonaniu zmiany w repozytorium CVS
Name:		cvsspam
Version:	0.2.12
Release:	10
License:	GPL
Group:		Applications/System
Source0:	http://www.badgers-in-foil.co.uk/projects/cvsspam/releases/%{name}-%{version}.tar.gz
# Source0-md5:	0afa4fbaf1c9edb27385e46337f80f4b
Patch100:	%{name}-branch.diff
Patch0:		%{name}-multibyte_enc_disables_highlight-patch1.diff
Patch1:		%{name}-textdiff.patch
URL:		http://www.badgers-in-foil.co.uk/projects/cvsspam/
BuildRequires:	rpmbuild(macros) >= 1.277
Requires:	cvs-client
%{?ruby_mod_ver_requires_eq}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_datadir	%{_prefix}/share/%{name}
%define		_libdir		%{_prefix}/lib

%description
CVSspam sends email when a change is committed to the CVS repository.
Syntax-highlighted diffs describe the changes made, and links to Web
frontends on CVS and bug tracking systems are generated where
possible.

%description -l pl.UTF-8
CVSspam wysyła wiadomość po wykonaniu zmiany w repozytorium CVS.
Różnice z podświetlaniem składni opisują wykonane zmiany, a jeśli to
możliwe, generowane są odnośniki do frontendów WWW do CVS i systemów
śledzenia błędów.

%prep
%setup -q
%patch100 -p0
%patch0 -p0
%patch1 -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_datadir},%{_sysconfdir}}

install {collect_diffs,cvsspam,record_lastdir}.rb $RPM_BUILD_ROOT%{_datadir}
install cvsspam.conf $RPM_BUILD_ROOT%{_sysconfdir}

ln -s %{_datadir} $RPM_BUILD_ROOT%{_libdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

# make compat symlink, the symlink is discarded using %ghost on package uninstall
%triggerpostun -- cvsspam < 0.2.11-5.3
# need rmdir, because the path belongs to new package (is %ghosted) and therefore is not removed by rpm
rmdir %{_libdir}/%{name} 2>/dev/null || mv -v %{_libdir}/%{name}{,.rpmsave}
ln -s %{_datadir} %{_libdir}/%{name}
%banner %{name} -e <<EOF
NOTE:
The cvsspam programs have been moved to %{_datadir}.
I've created compat symlink so you don't feel so much pain of that.

EOF

%files
%defattr(644,root,root,755)
%doc CREDITS TODO cvsspam-doc.pdf cvsspam-doc.html
%dir %{_datadir}
%attr(755,root,root) %{_datadir}/*
%ghost %{_libdir}/%{name}
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
