Summary:	A widely used Mail Transport Agent (MTA)
Summary(pl):	Sendmail -- aplikacja do obs³ugi poczty elektronicznej
Name:		sendmail
Version:	8.11.0
Release:	1
License:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Provides:	smtpdaemon
Source0:	ftp://ftp.cs.berkeley.edu/ucb/sendmail/%{name}.%{version}.tar.gz
Source1:	sendmail.init
Source2:	http://www.informatik.uni-kiel.de/~ca/email/rules/check.tar
Source3:	aliases
Source4:	sendmail.sysconfig
Source5:	sendmail-etc-mail-Makefile
Source6:	sendmail.mc
Source7:	sendmail-config.m4
Patch0:		sendmail-redhat.patch
Patch1:		sendmail-makemapman.patch
Patch2:		sendmail-smrsh-paths.patch
Patch3:		sendmail-rmail.patch
Patch4:		sendmail-manpath.patch
Patch5:		sendmail-m4path.patch
Patch6:		sendmail-dtelnet.patch
Patch7:		sendmail-pld.mc.patch
Patch8:		sendmail-redirect.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db3-devel
BuildRequires:	gdbm-devel
BuildRequires:	pam-devel
Prereq:		/sbin/chkconfig
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
Obsoletes:	zmailer
Obsoletes:	qmail
Obsoletes:	smail
Obsoletes:	exim
Obsoletes:	postfix
#Obsoletes:	sendmail-cf

%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your e-mail. Sendmail is a
behind-the-scenes program which actually moves your e-mail over
networks or the Internet to where you want it to go.

If you need documentation on Sendmail, you can install the sendmail-doc
package.

%description -l pl
Sendmail jest programem umo¿liwiaj±cym wymianê poczty elektronicznej
miêdzy komputerami w sieci internet. Zajmuje siê przekazywaniem poczty
elektronicznej miêdzy bramkami pocztowymi i dostarczaniem przesy³ek na
konta docelowe. Bardzo dobrze obs³uguje aliasy pocztowe a jego
dodatkowym atutem jest prosta konfiguracja. Dziêki rozbudowanym
mo¿liwo¶ciom konfiguracyjnym jest w stanie dostarczaæ przesy³ki za
po¶rednictwem protoko³ów: SMTP, ESMTP, UUCP, X.400 i innych.

dokumentacja do programu sendmail znajduje siê w pakiecie sendmail-doc.

%package cf
Summary:	The files needed to reconfigure Sendmail
Summary(pl):	Pliki potrzebne do rekonfiguracji Sendmaila
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}
Requires:	m4

%description cf
This package includes the configuration files which you'd need to
generate the sendmail.cf file distributed with the sendmail package.
You'll need the sendmail-cf package if you ever need to reconfigure
and rebuild your sendmail.cf file.  For example, the default
sendmail.cf file is not configured for UUCP.  If someday you needed to
send and receive mail over UUCP, you'd need to install the sendmail-cf
package to help you reconfigure Sendmail.

Install the sendmail-cf package if you need to reconfigure your
sendmail.cf file.

%description -l pl cf
Ten pakiet zawiera pliki konfiguracyjne, których bêdziesz potrzebowa³,
by wygenerowaæ plik sendmail.cf, zawarty w pakiecie sendmail.
Bêdziesz potrzebowa³ pakietu sendmail-cf je¿eli potrzebujesz
zrekonfigurowaæ i przebudowaæ plik sendmail.cf. Na przyk³ad, domy¶lny
sendmail.cf nie jest skonfigurowany dla UUCP. Je¿eli kiedy¶ bêdziesz
potrzebowa³ wysy³aæ i odbieraæ porztê po UUCP, bêdziesz musia³
zainstalowaæ pakiet sendmail-cf, który pomo¿e ci zrekonfigurowaæ Sendmaila.

%package doc
Summary:	Documentation about the Sendmail Mail Transport Agent program
Summary(pl):	Dokumentacja do Sendmaila
Group:		Documentation
Group(pl):	Dokumentacja
Requires:	%{name} = %{version}

%description doc
The sendmail-doc package contains documentation about the Sendmail
Mail Transport Agent (MTA) program, including release notes, the
Sendmail FAQ and a few papers written about Sendmail. The papers are
provided in PostScript(TM) and troff formats.

Install the sendmail-doc package if you need documentation about
Sendmail.

%description -l pl doc
Ten pakiet zawiera dokumentacjê do programu Sendmail Mail Transport
Agent (MTA). Dokumentacja zwawiera informacje o zmianach w bie¿±cej
wersji i FAQ - najczêsciej zadawane pytania. Dokumentacja dostêpna jest
w formacie PostScript(TM) oraz troff. Je¿eli potrzebujesz dokumentacji
- zainstaluj ten pakiet.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# seems to be obsoleted...
#tar xf %{SOURCE2} -C cf

sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/redhat.mc

install %{SOURCE7} config.m4

%build

#RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DUSE_VENDOR_CF_PATH=1 -DNETINET6"
# won't compile with -DNETINET6 on glibc-2.2 - resolver problems

RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DUSE_VENDOR_CF_PATH=1"
export RPM_OPT_FLAGS

cd sendmail	&& sh Build -f ../config.m4
cd ../mailstats	&& sh Build -f ../config.m4
cd ../rmail	&& sh Build -f ../config.m4
cd ../makemap	&& sh Build -f ../config.m4
cd ../praliases	&& sh Build -f ../config.m4
cd ../smrsh	&& sh Build -f ../config.m4
cd ../cf/cf
m4 redhat.mc > redhat.cf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{mail,smrsh}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d $RPM_BUILD_ROOT/etc/sysconfig
install -d $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}
install -d $RPM_BUILD_ROOT/var/log $RPM_BUILD_ROOT/var/spool/mqueue
install -d $RPM_BUILD_ROOT%{_libdir}/sendmail-cf

OBJDIR=obj.$(uname -s).$(uname -r).$(arch)

IDNU=`id -nu`
IDNG=`id -ng`
SMINSTOPT="DESTDIR=$RPM_BUILD_ROOT SBINOWN=$IDNU SBINGRP=$IDNG \
	UBINOWN=$IDNU UBINGRP=$IDNG MANOWN=$IDNU MANGRP=$IDNG"
%{__make} $SMINSTOPT install -C $OBJDIR/sendmail
%{__make} $SMINSTOPT install -C $OBJDIR/mailstats
%{__make} $SMINSTOPT install -C $OBJDIR/praliases
%{__make} $SMINSTOPT force-install -C $OBJDIR/rmail
%{__make} $SMINSTOPT install -C $OBJDIR/makemap
ln -sf ../sbin/makemap $RPM_BUILD_ROOT%{_bindir}/makemap
%{__make} $SMINSTOPT install -C $OBJDIR/smrsh

# install docs by hand
install -d $RPM_BUILD_ROOT%{_docdir}/sendmail
cp -ar FAQ LICENSE KNOWNBUGS README RELEASE_NOTES doc $RPM_BUILD_ROOT%{_docdir}/sendmail
cp smrsh/README $RPM_BUILD_ROOT%{_docdir}/sendmail/README.smrsh
cp cf/README $RPM_BUILD_ROOT%{_docdir}/sendmail/README.cf

# install the cf files
cd cf
rm -f cf/{Build,Makefile} feature/*~
cp -ar * $RPM_BUILD_ROOT%{_libdir}/sendmail-cf
cd -

install cf/cf/redhat.cf $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.cf
sed -e 's|@@PATH@@|%{_libdir}/sendmail-cf|' < %{SOURCE6} \
	> $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.mc
echo "# local-host-names - include all aliases for your machine here." \
	> $RPM_BUILD_ROOT%{_sysconfdir}/mail/local-host-names

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail

# dangling symlinks
for f in hoststat mailq newaliases purgestat ; do
  ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/${f}
done

cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/mail/access
# Check the %{_prefix}/doc/sendmail-%{version}/README.cf file for a description
# of the format of this file. (search for access_db in that file)
# The %{_prefix}/doc/sendmail-%{version}/README.cf is part of the sendmail-doc
# package.
#
# by default we allow relaying from localhost...
localhost.localdomain		RELAY
localhost			RELAY
127.0.0.1			RELAY
EOF

for map in virtusertable access domaintable mailertable ; do
  touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}
  $RPM_BUILD_ROOT%{_bindir}/makemap -C $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.cf hash \
	$RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}.db < $RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}
done

install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases
$RPM_BUILD_ROOT%{_bindir}/makemap -C $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.cf hash \
	$RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases.db < %{SOURCE3}

install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/sendmail
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/mail/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

%post
#
# Convert old format to new
#
if [ -f /etc/mail/deny ] ; then
    cat /etc/mail/deny | \
	awk 'BEGIN{ print "# Entries from obsoleted /etc/mail/deny"} \
		  {print $1" REJECT"}' >> /etc/mail/access
    cp /etc/mail/deny /etc/mail/deny.rpmorig
fi
for oldfile in relay_allow ip_allow name_allow ; do
    if [ -f /etc/mail/$oldfile ] ; then
	cat /etc/mail/$oldfile | \
		awk "BEGIN { print \"# Entries from obsoleted /etc/mail/$oldfile\" ;} \
	     { print $1\" RELAY\" }" >> /etc/mail/access
	cp /etc/mail/$oldfile /etc/mail/$oldfile.rpmorig
     fi
done

#
# Oops, these files moved
#
if [ -f /etc/sendmail.cw ] ; then
    cat /etc/sendmail.cw  | \
      awk 'BEGIN { print "# Entries from obsoleted /etc/sendmail.cw" ;} \
           { print $1 }' >> /etc/mail/local-host-names
    cp /etc/sendmail.cw /etc/sendmail.cw.rpmorig
fi
#
# Rebuild maps (next reboot will rebuild also)
#
{ /usr/bin/newaliases
  for map in virtusertable access domaintable mailertable
  do
    if [ -f /etc/mail/${map} ] ; then
      /usr/bin/makemap hash /etc/mail/${map} < /etc/mail/${map}
      sleep 1
    fi
  done
} > /dev/null 2>&1

/sbin/chkconfig --add sendmail
if [ -f /var/lock/subsys/sendmail ]; then
	/etc/rc.d/init.d/sendmail restart >&2
else
	echo "Run \"/etc/rc.d/init.d/sendmail start\" to start sendmail daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/sendmail ]; then
		/etc/rc.d/init.d/sendmail stop >&2
	fi
	/sbin/chkconfig --del sendmail
fi

# removal of compatibility links
%triggerpostun -- sendmail < 8.10.1
/sbin/chkconfig --add sendmail

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mailstats
%attr(755,root,root) %{_sbindir}/praliases
%attr(755,root,root) %{_bindir}/hoststat
%attr(755,root,root) %{_bindir}/purgestat
%attr(755,root,root) %{_bindir}/rmail
%attr(755,root,root) %{_bindir}/makemap
%attr(755,root,root) %{_sbindir}/makemap
%attr(755,root,root) %{_sbindir}/sendmail
%attr(755,root,root) %{_bindir}/newaliases
%attr(755,root,root) %{_bindir}/mailq
%attr(755,root,root) %{_sbindir}/smrsh
%{_libdir}/sendmail

%{_mandir}/man8/rmail.8*
%{_mandir}/man8/praliases.8*
%{_mandir}/man8/mailstats.8*
%{_mandir}/man8/makemap.8*
%{_mandir}/man8/sendmail.8*
%{_mandir}/man5/aliases.5*
%{_mandir}/man1/newaliases.1*
%{_mandir}/man1/mailq.1*

/var/log/statistics
# XXX can't do noreplace here or new sendmail will not deliver.
#%config %{_sysconfdir}/sendmail.cf
%config %{_sysconfdir}/mail/sendmail.cf
%config %{_sysconfdir}/mail/sendmail.mc
%config(noreplace) %{_sysconfdir}/mail/local-host-names
%config(noreplace) %{_sysconfdir}/mail/aliases
%attr(0644,root,mail) %ghost %{_sysconfdir}/mail/aliases.db
%attr(0755,root,mail) %dir /var/spool/mqueue
%dir %{_sysconfdir}/smrsh
%dir %{_sysconfdir}/mail

%config %{_sysconfdir}/mail/Makefile
%ghost %{_sysconfdir}/mail/virtusertable.db
%config(noreplace) %{_sysconfdir}/mail/virtusertable
%ghost %{_sysconfdir}/mail/access.db
%config(noreplace) %{_sysconfdir}/mail/access
%ghost %{_sysconfdir}/mail/domaintable.db
%config(noreplace) %{_sysconfdir}/mail/domaintable
%ghost %{_sysconfdir}/mail/mailertable.db
%config(noreplace) %{_sysconfdir}/mail/mailertable
%config(noreplace) %{_sysconfdir}/mail/helpfile

%attr(754,root,root) /etc/rc.d/init.d/sendmail
%config(noreplace) /etc/sysconfig/sendmail

%files cf
%defattr(644,root,root,755)
%{_libdir}/sendmail-cf

%files doc
%defattr(644,root,root,755)
%{_docdir}/sendmail
