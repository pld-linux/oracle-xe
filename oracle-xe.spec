# TODO:
# - read the license. Can we redistribute it?

%define	oracle_rel	1.0
%define	oracle_ver	10.2.0
%define	oracle_home	/usr/lib/oracle/xe/app/oracle/product/%{oracle_ver}/server

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
Source3:	%{name}-sgapga.awk
NoSource:	0
URL:		-
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Provides:	group(dba)
Provides:	user(oracle)
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0
%define		no_install_post_strip	1
%define		no_install_post_chrpath	1


%description
Oracle XE.

%description -l pl.UTF-8
Wyrocznia XE.

%prep
%setup -q -c -T
rpm2cpio %{SOURCE0} | cpio -dimu
sed -e 's#^ORACLE_HOME=$#ORACLE_HOME=%{oracle_home}#' < %{SOURCE2} > oracle-xe.sysconfig

mv usr/share/doc/oracle_xe doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/oracle-xe
install oracle-xe.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/oracle-xe

install -d $RPM_BUILD_ROOT%{oracle_home}
cp -a usr/lib/oracle/xe/app/oracle/product/%{oracle_ver}/server/* $RPM_BUILD_ROOT%{oracle_home}

mv $RPM_BUILD_ROOT%{oracle_home}/dbs/init{,XE}.ora

install -d $RPM_BUILD_ROOT/var/lib/oracle/network/admin
install -d $RPM_BUILD_ROOT/var/log/oracle

# move directories that needs to be writable out of /usr, and create symlinks
# in their original paths
%define	mvln() \
install -d $(dirname $RPM_BUILD_ROOT%{2}/%{1}); \
mv $RPM_BUILD_ROOT%{oracle_home}/%{1} $RPM_BUILD_ROOT%{2}/%{1}; \
ln -s %{2}/%{1} $RPM_BUILD_ROOT%{oracle_home}/%{1}; \
%{nil}

%mvln dbs /var/lib/oracle
#%%mvln log /var/log/oracle
%mvln rdbms/log /var/log/oracle
%mvln network/log /var/log/oracle
%mvln config/log /var/log/oracle/config
%mvln rdbms /var/lib/oracle
%mvln network/admin /var/lib/oracle
ln -s /var/lib/oracle/admin $RPM_BUILD_ROOT%{_sysconfdir}/oracle-xe

install -d $RPM_BUILD_ROOT%{_datadir}/oracle/scripts
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/oracle/scripts/sgapga.awk

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 236 -r -f dba
%useradd -u 236 -r -d /usr/lib/oracle/xe -s /bin/false -c "Oracle" -g dba oracle

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove oracle
	%groupremove dba
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%dir %{_sysconfdir}/oracle-xe
%attr(754,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/rc.d/init.d/oracle-xe
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/oracle-xe

%dir %{oracle_home}
%{oracle_home}/dbs
%{oracle_home}/demo
%{oracle_home}/jlib
%{oracle_home}/ldap
%{oracle_home}/nls
%{oracle_home}/opmn
%{oracle_home}/oracore
%{oracle_home}/plsql
%{oracle_home}/precomp
%{oracle_home}/rdbms
%{oracle_home}/slax
%{oracle_home}/sqlplus
%{oracle_home}/xdk

%attr(755,root,root) %{oracle_home}/bin/*

%{oracle_home}/config/log
%{oracle_home}/config/scripts/*.menu
%{oracle_home}/config/scripts/*.ora
%{oracle_home}/config/scripts/*.sql
# XXX integrate into initscript and rm?
%{oracle_home}/config/scripts/oracle-xe
%attr(755,root,root) %{oracle_home}/config/scripts/*.sh
%{oracle_home}/config/seeddb

%dir %{oracle_home}/ctx
%{oracle_home}/ctx/admin
%{oracle_home}/ctx/config
%{oracle_home}/ctx/data
%dir %{oracle_home}/ctx/bin/ctxhx
%attr(755,root,root) %{oracle_home}/ctx/bin/ctxhx
%dir %{oracle_home}/ctx/lib
%{oracle_home}/ctx/lib/*.ini
%{oracle_home}/ctx/lib/*.lic
%{oracle_home}/ctx/lib/*.map
%{oracle_home}/ctx/lib/*.mk
%{oracle_home}/ctx/lib/*.res
%{oracle_home}/ctx/lib/*.ux
%attr(755,root,root) %{oracle_home}/ctx/lib/*.so*
%{oracle_home}/ctx/mesg
%{oracle_home}/ctx/migrate

%dir %{oracle_home}/hs
%dir %{oracle_home}/hs/admin
%{oracle_home}/hs/admin/*.ora
# XXX? rm?
%{oracle_home}/hs/admin/*.ora.sample
%dir %{oracle_home}/hs/bin
%attr(755,root,root)  %{oracle_home}/hs/bin/brand.bin

%dir %{oracle_home}/jdbc
%dir %{oracle_home}/jdbc/bin
%attr(755,root,root) %{oracle_home}/jdbc/bin/fixJDBC-tm4ldaps.sh
%{oracle_home}/jdbc/lib/*.jar
%{oracle_home}/jdbc/Readme.txt

%dir %{oracle_home}/lib
%{oracle_home}/lib/*.a
%{oracle_home}/lib/*.so*
%{oracle_home}/lib/*.lis
%{oracle_home}/lib/*.zip
%{oracle_home}/lib/sysliblist

%{oracle_home}/network/admin
%dir %{oracle_home}/network
%dir %{oracle_home}/network/install
%dir %{oracle_home}/network/install/sqlnet
%{oracle_home}/network/install/sqlnet/setowner.sh
%dir %{oracle_home}/network/lib
%attr(755,root,root) %{oracle_home}/network/lib/lib*.so

%{oracle_home}/network/log
%{oracle_home}/network/mesg

%dir %{oracle_home}/odbc
%{oracle_home}/odbc/html
%{oracle_home}/odbc/mesg
%dir %{oracle_home}/odbc/utl
%attr(755,root,root) %{oracle_home}/odbc/utl/odbc_update_ini.sh

# TODO: -devel?
#%{oracle_home}/plsql/include

%attr(755,root,root) %{_datadir}/oracle/scripts
%dir /var/log/oracle
%dir %attr(750,oracle,dba) /var/log/oracle/network
%dir %attr(750,oracle,dba) /var/log/oracle/network/log
%dir %attr(750,oracle,dba) /var/log/oracle/rdbms
%dir %attr(750,oracle,dba) /var/log/oracle/rdbms/log

%dir /var/lib/oracle
# XXX Directories should be 750, but files 640.
# XXX: list them here (i still don't have the tarball)
%attr(750,oracle,dba) /var/lib/oracle/*
