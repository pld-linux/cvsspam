Summary:	CVSspam emails you diffs when someone commits a change to your CVS repository
Summary(pl):	CVSspam - wysy³anie ró¿nic po wykonaniu zmiany w repozytorium CVS
Name:		cvsspam
Version:	0.2.11
Release:	7
Epoch:		0
License:	GPL
Group:		Applications/System
Source0:	http://www.badgers-in-foil.co.uk/projects/cvsspam/%{name}-%{version}.tar.gz
# Source0-md5:	e2fe350b845ad1d2ff935f623a0f543a
Patch0:		%{name}-users-quote.patch
Patch1:		%{name}-charset-arg.patch
Patch2:		%{name}-filenr.patch
Patch3:		%{name}-trailing-cvsinfo-slash.patch
Patch4:		%{name}-optkb_binary_hint.patch
Patch5:		%{name}-encode_email_personal_name.patch
Patch6:		%{name}-cvsroot_trailing_slash.patch
Patch7:		%{name}-mail_threading.patch
Patch8:		%{name}-comment-ws.patch
URL:		http://www.badgers-in-foil.co.uk/projects/cvsspam/
BuildRequires:	rpmbuild(macros) >= 1.177
Requires:	cvs
Requires:	ruby
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_datadir	%{_prefix}/share/%{name}

%description
CVSspam sends email when a change is committed to the CVS repository.
Syntax-highlighted diffs describe the changes made, and links to Web
frontends on CVS and bug tracking systems are generated where
possible.

%description -l pl
CVSspam wysy³a wiadomo¶æ po wykonaniu zmiany w repozytorium CVS.
Ró¿nice z pod¶wietlaniem sk³adni opisuj± wykonane zmiany, a je¶li to
mo¿liwe, generowane s± odno¶niki do frontendów WWW do CVS i systemów
¶ledzenia b³êdów.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p0
%patch7 -p0
%patch8 -p1

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
NOTE: The cvsspam programs have been moved to %{_datadir}.
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
