Summary:	CVSspam emails you diffs when someone commits a change to your CVS repository.
Name:		cvsspam
Version:	0.2.11
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/System
Source0:	http://www.badgers-in-foil.co.uk/projects/cvsspam/%{name}-%{version}.tar.gz
# Source0-md5:	e2fe350b845ad1d2ff935f623a0f543a
URL:		http://www.badgers-in-foil.co.uk/projects/cvsspam/
Requires:	ruby
Requires:	cvs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_sysconfdir	/etc/%{name}

%description
CVSspam sends email when a change is committed to the CVS repository.
Syntax-highlighted diffs describe the changes made, and links to Web
frontends on CVS and bug tracking systems are generated where
possible.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}}

install collect_diffs.rb cvsspam.rb record_lastdir.rb $RPM_BUILD_ROOT%{_bindir}
install cvsspam.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS TODO cvsspam-doc.pdf cvsspam-doc.html
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
