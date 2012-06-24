#
# Conditional build:
# _without_ldap		without LDAP support
# _without_tls		without TLS (SSL) support

Summary:	A widely used Mail Transport Agent (MTA)
Summary(de):	sendmail-Mail-�bertragungsagent
Summary(fr):	Agent de transport de courrier sendmail
Summary(pl):	Sendmail - serwer poczty elektronicznej
Summary(ru):	�������� ������������ ����� sendmail
Summary(tr):	Elektronik posta hizmetleri sunucusu
Summary(uk):	�������� ������������ ����� sendmail
Name:		sendmail
Version:	8.12.3
Release:	3
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
Source1:	%{name}.init
Source2:	http://www.informatik.uni-kiel.de/~ca/email/rules/check.tar
Source3:	aliases
Source4:	%{name}.sysconfig
Source5:	%{name}-etc-mail-Makefile
Source6:	%{name}.mc
Source7:	%{name}-config.m4
Source8:	%{name}.sasl
Source9:	%{name}-access-sample
Source10:	%{name}-mailertable-sample
Source11:	%{name}-virtusertable-sample
Source12:	%{name}-domaintable-sample
Source13:	%{name}-pam-d-smtp
Patch0:		%{name}-makemapman.patch
Patch1:		%{name}-smrsh-paths.patch
Patch2:		%{name}-rmail.patch
Patch3:		%{name}-os-paths.patch
Patch4:		%{name}-m4path.patch
Patch5:		%{name}-redirect.patch
Patch6:		%{name}-hprescan-dos.patch
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db3-devel
%{!?_without_ldap:BuildRequires:	openldap-devel}
%{!?_without_tls:BuildRequires:	openssl-devel}
Requires:	m4
Requires:	procmail
PreReq:		/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post):	awk
Requires(post):	textutils
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	smtpdaemon
Obsoletes:	exim
Obsoletes:	masqmail
Obsoletes:	omta
Obsoletes:	postfix
Obsoletes:	qmail
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smail
Obsoletes:	zmailer

%define		_sysconfdir	/etc/mail

%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your e-mail. Sendmail is a
behind-the-scenes program which actually moves your e-mail over
networks or the Internet to where you want it to go.

%description -l de
Sendmail �bertr�gt Mails zwischen Rechnern. Es implementiert eine
allgemeine Mail-Routing-Funktion �ber das Netzwerk mit Aliasing und
Weiterleiten von Nachrichten, automatischem Routing an
Netzwerk-Gateways und flexible Konfiguration. Wenn Sie E-Mails �ber
das Internet senden und empfangen m�chten, brauchen Sie sendmail.

%description -l fr
Sendmail est un agent de transport de courrier, qui est le programme
transf�rent le courrier d'une machine � l'autre. Sendmail impl�mente
une facilit� g�n�rale de routage de courrier entre les r�seaux, permet
l'\"aliasing\" et le \"forwarding\", un routage automatique sur les
passerelles du r�seau, et une configuration flexible.

%description -l pl
Sendmail jest programem umo�liwiaj�cym wymian� poczty elektronicznej
mi�dzy komputerami w sieci (MTA). Zajmuje si� przekazywaniem poczty
elektronicznej mi�dzy bramkami pocztowymi i dostarczaniem przesy�ek na
konta docelowe. Bardzo dobrze obs�uguje aliasy pocztowe a jego
dodatkowym atutem jest prosta konfiguracja. Dzi�ki rozbudowanym
mo�liwo�ciom konfiguracyjnym jest w stanie dostarcza� przesy�ki za
po�rednictwem protoko��w: SMTP, ESMTP, UUCP, X.400 i innych.

%description -l ru
Sendmail - ��� Mail Transport Agent, ��������� ������������ ����� �
������ �� ������. Sendmail ������������� ����������� ��������
���������� ������������� �����, aliasing, forwarding, ��������������
������������� ��� ������� ������ � ������ �������� ������������.

%description -l tr
Sendmail, bir mektubu bir makineden di�erine ta��r. Pek �ok davran���
ayarlanabilir. Internet �zerinden mektup almak veya g�ndermek
istiyorsan�z bu pakete gereksiniminiz olacakt�r.

%description -l uk
Sendmail - �� Mail Transport Agent, �������� �� ��������� ����� �
������ �� ������. Sendmail ����� ��������Φ ������ ͦ��������ϧ
����������æ� �����, aliasing, forwarding, ����������� ����������æ�
��� ��������� ���ڦ� �� ������� ����Φ�� ����������æ�.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# seems to be obsoleted...
#tar xf %{SOURCE2} -C cf

sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/pld.mc

install %{SOURCE7} config.m4

%build
echo "define(\`confCC', \`%{__cc}')" >> config.m4
echo "define(\`confOPTIMIZE', \`%{rpmcflags} -DUSE_VENDOR_CF_PATH=1 -DNETINET6')" >> config.m4
%if %{?debug:0}%{!?debug:1}
echo "define(\`confLDOPTS', \`-s')" >> config.m4
%endif
%if %{?_without_ldap:0}%{!?_without_ldap:1}
echo "APPENDDEF(\`confMAPDEF', \`-DLDAPMAP')" >> config.m4
echo "APPENDDEF(\`confLIBS', \`-lldap -llber')" >> config.m4
%endif
%if %{?_without_tls:0}%{!?_without_tls:1}
echo "APPENDDEF(\`confENVDEF', \`-DSTARTTLS')" >> config.m4
echo "APPENDDEF(\`confLIBS', \`-lssl -lcrypto')" >> config.m4
%endif

cd sendmail	&& sh Build -f ../config.m4
cd ../mailstats	&& sh Build -f ../config.m4
cd ../rmail	&& sh Build -f ../config.m4
cd ../makemap	&& sh Build -f ../config.m4
cd ../praliases	&& sh Build -f ../config.m4
cd ../smrsh	&& sh Build -f ../config.m4
cd ../cf/cf
m4 pld.mc > pld.cf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig,sasl,smrsh}} \
	$RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT%{_libdir} \
	$RPM_BUILD_ROOT%{_mandir}/man{1,5,8} \
	$RPM_BUILD_ROOT/var/log $RPM_BUILD_ROOT/var/spool/mqueue \
	$RPM_BUILD_ROOT%{_libdir}/sendmail-cf \
	$RPM_BUILD_ROOT/etc/pam.d \

OBJDIR=obj.$(uname -s).$(uname -r).$(arch)

IDNU=`id -nu`
IDNG=`id -ng`
SMINSTOPT="DESTDIR=$RPM_BUILD_ROOT SBINOWN=$IDNU SBINGRP=$IDNG \
	UBINOWN=$IDNU UBINGRP=$IDNG MANOWN=$IDNU MANGRP=$IDNG \
	CFOWN=$IDNU CFGRP=$IDNG MSPQOWN=$IDNU GBINGRP=$IDNG GBINOWN=$IDNU \
	BINOWN=$IDNU BINGRP=$IDNG"
%{__make} $SMINSTOPT install -C $OBJDIR/sendmail
%{__make} $SMINSTOPT install -C $OBJDIR/mailstats
%{__make} $SMINSTOPT install -C $OBJDIR/praliases
%{__make} $SMINSTOPT force-install -C $OBJDIR/rmail
%{__make} $SMINSTOPT install -C $OBJDIR/makemap
ln -sf ../sbin/makemap $RPM_BUILD_ROOT%{_bindir}/makemap
%{__make} $SMINSTOPT install -C $OBJDIR/smrsh

# install the cf files
cd cf
rm -f cf/{Build,Makefile} feature/*~
cp -ar * $RPM_BUILD_ROOT%{_libdir}/sendmail-cf
cd -

# sendmail.{cf,mc}
install cf/cf/pld.cf $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf
sed -e 's|@@PATH@@|%{_libdir}/sendmail-cf|' < %{SOURCE6} \
	> $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.mc

# submit.mc (submit.cf is installed automatically)
install cf/cf/submit.mc $RPM_BUILD_ROOT%{_sysconfdir}

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
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sasl/Sendmail.conf
install %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/access.sample
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/mailertable.sample
install %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/virtusertable.sample
install %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/domaintable.sample
install %{SOURCE13} $RPM_BUILD_ROOT/etc/pam.d/smtp

mv -f smrsh/README README.smrsh
mv -f cf/README README.cf
mv -f doc/op/op.me .

gzip -9nf FAQ KNOWNBUGS README* op.me RELEASE_NOTES

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid smmsp`" ]; then
	if [ "`/usr/bin/getgid smmsp`" != "25" ]; then
		echo "Warning: group smmsp haven't gid=25. Correct this before installing sendmail." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 25 -r -f smmsp
fi
if [ -n "`/bin/id -u smmsp 2>/dev/null`" ]; then
	if [ "`/bin/id -u smmsp`" != "25" ]; then
		echo "Warning: user smmsp haven't uid=25. Correct this before installing sendmail." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 25 -r -d /var/spool/clientqueue -s /bin/false -c "Sendmail Message Submission Program" -g smmsp smmsp 1>&2
fi

%post
#
# Convert old format to new
#
if [ -f /etc/mail/deny ] ; then
	cat /etc/mail/deny | \
		awk 'BEGIN{ print "# Entries from obsoleted /etc/mail/deny"} \
		{print $1" REJECT"}' >> /etc/mail/access
	mv -f /etc/mail/deny /etc/mail/deny.rpmorig
fi
for oldfile in relay_allow ip_allow name_allow ; do
	if [ -f /etc/mail/$oldfile ] ; then
		cat /etc/mail/$oldfile | \
			awk "BEGIN { print \"# Entries from obsoleted /etc/mail/$oldfile\" ;} \
			{ print $1\" RELAY\" }" >> /etc/mail/access
		mv -f /etc/mail/$oldfile /etc/mail/$oldfile.rpmorig
	fi
done

#
# Oops, these files moved
#
if [ -f /etc/sendmail.cw ] ; then
	cat /etc/sendmail.cw | \
		awk 'BEGIN { print "# Entries from obsoleted /etc/sendmail.cw" ;} \
		{ print $1 }' >> /etc/mail/local-host-names
	mv -f /etc/sendmail.cw /etc/sendmail.cw.rpmorig
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

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel smmsp 2>/dev/null
	/usr/sbin/groupdel smmsp 2>/dev/null
fi

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
%attr(2755,root,smmsp) %{_sbindir}/sendmail
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

%dir /etc/smrsh
%dir %{_sysconfdir}
/var/log/statistics
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sendmail.cf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sendmail.mc
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/submit.cf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/submit.mc
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/local-host-names
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/aliases
%attr(0644,root,mail) %ghost %{_sysconfdir}/aliases.db
%attr(0770,root,smmsp) %dir /var/spool/clientmqueue
%attr(0750,root,mail) %dir /var/spool/mqueue
%attr(0755,root,root) %dir /etc/pam.d

%config %{_sysconfdir}/Makefile
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/access
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/access.sample
%ghost %{_sysconfdir}/access.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/domaintable
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/domaintable.sample
%ghost %{_sysconfdir}/domaintable.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailertable
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailertable.sample
%ghost %{_sysconfdir}/mailertable.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/virtusertable
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/virtusertable.sample
%ghost %{_sysconfdir}/virtusertable.db
%config(noreplace) %{_sysconfdir}/helpfile

%attr(754,root,root) /etc/rc.d/init.d/sendmail
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/sendmail
%config(noreplace) %verify(not md5 size mtime) /etc/sasl/Sendmail.conf
%config(noreplace) %verify(not md5 size mtime) /etc/pam.d/smtp

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
