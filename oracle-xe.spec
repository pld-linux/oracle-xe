
%define         _enable_debug_packages                  0
%define         no_install_post_strip                   1
%define         no_install_post_chrpath                 1

%define		oracle_rel 1.0
%define		oracle_ver 10.2.0
%define		oracle_home /usr/lib/oracle/xe/app/oracle/product/%{oracle_ver}
Summary:	Oracle XE
Summary(pl.UTF-8):	Wyrocznia XE
Name:		oracle-xe
Version:	%{oracle_ver}.1
Release:	0.1
License:	Proprietary (not distributable)
Group:		Applications
Source0:	%{name}-%{version}-%{oracle_rel}.i386.rpm
# NoSource0-md5:	707641df1e51320607ba9b0a7b19fb3d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
NoSource:       0
URL:		-
%if %{with initscript}
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
%endif
#BuildRequires:	-
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
Provides:	group(dba)
Provides:	user(oracle)
#Obsoletes:	-
#Conflicts:	-
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Oracle XE.

%description -l pl.UTF-8
Wyrocznia XE.

%prep
%setup -c -T

rpm2cpio %{SOURCE0} | cpio -dimu

cp %{SOURCE2} .
sed -i 's#^ORACLE_HOME=$#ORACLE_HOME=%{oracle_home}#'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{init.d,sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/oracle-xe
install oracle.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/oracle-xe

install -d $RPM_BUILD_ROOT%{oracle_home}
cp -a usr/lib/oracle/xe/app/oracle/product/%{oracle_ver} $RPM_BUILD_ROOT%{oracle_home} 

mv $RPM_BUILD_ROOT%{oracle_home}/network/admin $RPM_BUILD_ROOT%{sysconfdir}/oracle-xe
ln -s $RPM_BUILD_ROOT%{sysconfdir}/oracle-xe $RPM_BUILD_ROOT%{oracle_home}/network/admin

mv $RPM_BUILD_ROOT/server/dbs/init{,XE}.ora

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 234 -r -f dba
%useradd -u 234 -r -d /usr/lib/oracle/xe -s /bin/false -c "Oracle" -g dba oracle

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun

%files
%defattr(644,root,root,755)
%{oracle_home}
%dir %{sysconfdir}/oracle-xe
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) listener.ora
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) tnsnames.ora

%doc usr/share/doc/oracle_xe/*
