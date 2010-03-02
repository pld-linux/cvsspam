Summary:	CVSspam emails you diffs when someone commits a change to your CVS repository
Summary(pl.UTF-8):	CVSspam - wysyłanie różnic po wykonaniu zmiany w repozytorium CVS
Name:		cvsspam
Version:	0.2.12
Release:	12
License:	GPL
Group:		Applications/System
Source0:	http://www.badgers-in-foil.co.uk/projects/cvsspam/releases/%{name}-%{version}.tar.gz
# Source0-md5:	0afa4fbaf1c9edb27385e46337f80f4b
Source1:	%{name}-branch.sh
Patch100:	%{name}-branch.diff
Patch0:		%{name}-textdiff.patch
Patch1:		%{name}-tracfunc.patch
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
rm svn_post_commit_hook.rb
%patch100 -p0
%patch0 -p0
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_datadir},%{_sysconfdir}}
install -p {collect_diffs,cvsspam,record_lastdir}.rb $RPM_BUILD_ROOT%{_datadir}
cp -a cvsspam.conf $RPM_BUILD_ROOT%{_sysconfdir}

# svn part
install -p svn_post_commit_hook.rb $RPM_BUILD_ROOT%{_datadir}

# compat
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
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cvsspam.conf
%dir %{_datadir}
%attr(755,root,root) %{_datadir}/*.rb

%ghost %{_libdir}/%{name}
