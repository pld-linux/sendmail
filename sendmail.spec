#
# Conditional build:
# _without_ldap - without LDAP
#
Summary:	A widely used Mail Transport Agent (MTA)
Summary(de):	sendmail-Mail-Übertragungsagent
Summary(fr):	Agent de transport de courrier sendmail
Summary(pl):	Sendmail -- aplikacja do obs³ugi poczty elektronicznej
Summary(tr):	Elektronik posta hizmetleri sunucusu
Name:		sendmail
Version:	8.11.4
Release:	5
License:	BSD
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Provides:	smtpdaemon
Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
Source1:	%{name}.init
Source2:	http://www.informatik.uni-kiel.de/~ca/email/rules/check.tar
Source3:	aliases
Source4:	%{name}.sysconfig
Source5:	%{name}-etc-mail-Makefile
Source6:	%{name}.mc
Source7:	%{name}-config.m4
Source8:	%{name}.sasl
Patch0:		%{name}-redhat.patch
Patch1:		%{name}-makemapman.patch
Patch2:		%{name}-smrsh-paths.patch
Patch3:		%{name}-rmail.patch
Patch4:		%{name}-manpath.patch
Patch5:		%{name}-m4path.patch
Patch6:		%{name}-dtelnet.patch
Patch7:		%{name}-pld.mc.patch
Patch8:		%{name}-redirect.patch
Patch9:		%{name}-hprescan-dos.patch
Patch10:	%{name}-aliasesDoS.patch
Patch11:	%{name}-fix.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db3-devel
%{!?_without_ldap:BuildRequires:	openldap-devel}
BuildRequires:	pam-devel
Requires:	m4
Prereq:		/sbin/chkconfig
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
Obsoletes:	zmailer
Obsoletes:	qmail
Obsoletes:	smail
Obsoletes:	exim
Obsoletes:	postfix
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc

%define		_sysconfdir	/etc/mail

%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your e-mail. Sendmail is a
behind-the-scenes program which actually moves your e-mail over
networks or the Internet to where you want it to go.

%description -l de
Sendmail überträgt Mails zwischen Rechnern. Es implementiert eine
allgemeine Mail-Routing-Funktion über das Netzwerk mit Aliasing und
Weiterleiten von Nachrichten, automatischem Routing an
Netzwerk-Gateways und flexible Konfiguration. Wenn Sie E-Mails über
das Internet senden und empfangen möchten, brauchen Sie sendmail.

%description -l fr
Sendmail est un agent de transport de courrier, qui est le programme
transférent le courrier d'une machine à l'autre. Sendmail implémente
une facilité générale de routage de courrier entre les réseaux, permet
l'\"aliasing\" et le \"forwarding\", un routage automatique sur les
passerelles du réseau, et une configuration flexible.

%description -l pl
Sendmail jest programem umo¿liwiaj±cym wymianê poczty elektronicznej
miêdzy komputerami w sieci internet. Zajmuje siê przekazywaniem poczty
elektronicznej miêdzy bramkami pocztowymi i dostarczaniem przesy³ek na
konta docelowe. Bardzo dobrze obs³uguje aliasy pocztowe a jego
dodatkowym atutem jest prosta konfiguracja. Dziêki rozbudowanym
mo¿liwo¶ciom konfiguracyjnym jest w stanie dostarczaæ przesy³ki za
po¶rednictwem protoko³ów: SMTP, ESMTP, UUCP, X.400 i innych.

%description -l tr
Sendmail, bir mektubu bir makineden diðerine taþýr. Pek çok davranýþý
ayarlanabilir. Internet üzerinden mektup almak veya göndermek
istiyorsanýz bu pakete gereksiniminiz olacaktýr.

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
%patch9 -p1
%patch10 -p1
%patch11 -p1

# seems to be obsoleted...
#tar xf %{SOURCE2} -C cf

sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/redhat.mc

install %{SOURCE7} config.m4

%build

%if %{?debug:0}%{!?debug:1}
echo "define(\`confLDOPTS\', \`-s\')" >> config.m4
%endif
%if %{?_without_ldap:0}%{!?_without_ldap:1}
echo "APPENDDEF(\`confMAPDEF\', \`-DLDAPMAP\')" >> config.m4
echo "APPENDDEF(\`confLIBS\', \`-lldap -llber\')" >> config.m4
%endif

RPM_OPT_FLAGS="%{rpmcflags} \
	-DUSE_VENDOR_CF_PATH=1 -DNETINET6 -D_FFR_TESTMODE_DROP_PRIVS"
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig,sasl,smrsh}} \
	$RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT%{_libdir} \
	$RPM_BUILD_ROOT%{_mandir}/man{1,5,8} \
	$RPM_BUILD_ROOT/var/log $RPM_BUILD_ROOT/var/spool/mqueue \
	$RPM_BUILD_ROOT%{_libdir}/sendmail-cf \

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

install cf/cf/redhat.cf $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf
sed -e 's|@@PATH@@|%{_libdir}/sendmail-cf|' < %{SOURCE6} \
	> $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.mc
echo "# local-host-names - include all aliases for your machine here." \
	> $RPM_BUILD_ROOT%{_sysconfdir}/local-host-names

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail

# dangling symlinks
for f in hoststat mailq newaliases purgestat ; do
  ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/${f}
done

cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/access
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
	touch $RPM_BUILD_ROOT%{_sysconfdir}/${map}
		$RPM_BUILD_ROOT%{_bindir}/makemap -C $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf hash \
		$RPM_BUILD_ROOT%{_sysconfdir}/${map}.db < $RPM_BUILD_ROOT%{_sysconfdir}/${map}
done

install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/aliases
$RPM_BUILD_ROOT%{_bindir}/makemap -C $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf hash \
	$RPM_BUILD_ROOT%{_sysconfdir}/aliases.db < %{SOURCE3}

install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/sendmail
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/Makefile
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sasl/sendmail

mv $RPM_BUILD_ROOT/usr/share/doc/sendmail/{FAQ,KNOWNBUGS,LICENSE,README,README.cf,doc/op/op.me} .

gzip -9nf FAQ KNOWNBUGS README README.cf op.me

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
 for map in virtusertable access domaintable mailertable; do
	if [ -f /etc/mail/${map} ] ; then
		/usr/bin/makemap hash /etc/mail/${map} < /etc/mail/${map}
		sleep 1
	fi
 done
} > /dev/null 2>&1

DESC="sendmail daemon"; %chkconfig_add

%preun
%chkconfig_del

# removal of compatibility links
%triggerpostun -- sendmail < 8.10.1
/sbin/chkconfig --add sendmail

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/mailstats
%attr(755,root,root) %{_sbindir}/praliases
%attr(755,root,root) %{_bindir}/hoststat
%attr(755,root,root) %{_bindir}/purgestat
%attr(755,root,root) %{_bindir}/rmail
%attr(755,root,root) %{_bindir}/makemap
%attr(755,root,root) %{_sbindir}/makemap
%attr(6755,root,mail) %{_sbindir}/sendmail
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
%config(noreplace) %{_sysconfdir}/sendmail.cf
%config(noreplace) %{_sysconfdir}/sendmail.mc
%config(noreplace) %{_sysconfdir}/local-host-names
%config(noreplace) %{_sysconfdir}/aliases
%attr(0644,root,mail) %ghost %{_sysconfdir}/aliases.db
%attr(0770,root,mail) %dir /var/spool/mqueue
%dir /etc/smrsh
%dir %{_sysconfdir}

%config %{_sysconfdir}/Makefile
%ghost %{_sysconfdir}/virtusertable.db
%config(noreplace) %{_sysconfdir}/virtusertable
%ghost %{_sysconfdir}/access.db
%config(noreplace) %{_sysconfdir}/access
%ghost %{_sysconfdir}/domaintable.db
%config(noreplace) %{_sysconfdir}/domaintable
%ghost %{_sysconfdir}/mailertable.db
%config(noreplace) %{_sysconfdir}/mailertable
%config(noreplace) %{_sysconfdir}/helpfile

%attr(754,root,root) /etc/rc.d/init.d/sendmail
%config(noreplace) /etc/sysconfig/sendmail
%config(noreplace) /etc/sasl/sendmail

%dir %{_libdir}/sendmail-cf
%dir %{_libdir}/sendmail-cf/cf
%{_libdir}/sendmail-cf/cf/pld.mc
%{_libdir}/sendmail-cf/feature
%{_libdir}/sendmail-cf/m4
%{_libdir}/sendmail-cf/mailer
%dir %{_libdir}/sendmail-cf/ostype
%{_libdir}/sendmail-cf/ostype/linux.m4
%dir %{_libdir}/sendmail-cf/sh
%{_libdir}/sendmail-cf/sh/makeinfo.sh
%{_libdir}/sendmail-cf/siteconfig
