# TODO:
# - make sid-milter support:
#   http://sourceforge.net/projects/sid-milter/
#   http://www.sendmail.net/
# - http://blue-labs.org/clue/bluelabs.patch-8.12.3 has been updated upstream
# - move compilation from install to build section, fix re-entrancy of install
# - add tests bcond and/or disable tests tha fail on (AC-)builders
#
# Conditional build:
%bcond_without	ldap	# without LDAP support
%bcond_without	tls	# without TLS (SSL) support
%bcond_with	pgsql	# with PostgreSQL support (bluelabs)
#
Summary:	A widely used Mail Transport Agent (MTA)
Summary(de.UTF-8):	sendmail-Mail-Übertragungsagent
Summary(es.UTF-8):	Sendmail - agente de transporte de mail
Summary(fr.UTF-8):	Agent de transport de courrier sendmail
Summary(ko.UTF-8):	SMTP_AUTH와 TLS를 지원하는 Mail 전송 프로그램(MTA)
Summary(pl.UTF-8):	Sendmail - serwer poczty elektronicznej
Summary(pt_BR.UTF-8):	Sendmail - agente de transporte de mail
Summary(ru.UTF-8):	Почтовый транспортный агент sendmail
Summary(tr.UTF-8):	Elektronik posta hizmetleri sunucusu
Summary(uk.UTF-8):	Поштовий транспортний агент sendmail
Name:		sendmail
Version:	8.13.8
Release:	10
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
# Source0-md5:	5f29c94b42e0bb74d546b2ae84203a1e
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.aliases
# From http://doc.phpauction.org/sendmail/examples/
Source4:	%{name}-examples.tar.bz2
# Source4-md5:	d00d817cd456a947a7fc6c04072a7d68
Source5:	%{name}-etc-mail-Makefile
Source6:	%{name}.mc
Source7:	%{name}-config.m4
Source8:	%{name}.sasl
Source9:	%{name}.access
Source10:	%{name}.mailertable
Source11:	%{name}.virtusertable
Source12:	%{name}.domaintable
Source13:	%{name}-smtp.pamd
Source14:	%{name}.monitrc
Patch0:		%{name}-makemapman.patch
Patch1:		%{name}-smrsh-paths.patch
Patch2:		%{name}-rmail.patch
Patch3:		%{name}-os-paths.patch
Patch4:		%{name}-m4path.patch
Patch5:		%{name}-redirect.patch
Patch6:		%{name}-hprescan-dos.patch
Patch7:		http://blue-labs.org/clue/bluelabs.patch-8.12.3
URL:		http://www.sendmail.org/
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db-devel >= 4.1.25
BuildRequires:	man
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
%{?with_tls:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.310
BuildRequires:	sed >= 4.0
%ifarch sparc
BuildRequires:	sparc32
%endif
Requires(post):	awk
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts >= 0.4.0.20
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	db >= 4.1.25
Requires:	m4
Requires:	pam >= 0.79.0
Requires:	procmail
Provides:	group(smmsp)
Provides:	smtpdaemon
Provides:	user(smmsp)
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/mail
%define		specflags	-fPIC

%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your e-mail. Sendmail is a
behind-the-scenes program which actually moves your e-mail over
networks or the Internet to where you want it to go.

%description -l de.UTF-8
Sendmail überträgt Mails zwischen Rechnern. Es implementiert eine
allgemeine Mail-Routing-Funktion über das Netzwerk mit Aliasing und
Weiterleiten von Nachrichten, automatischem Routing an
Netzwerk-Gateways und flexible Konfiguration. Wenn Sie E-Mails über
das Internet senden und empfangen möchten, brauchen Sie sendmail.

%description -l es.UTF-8
sendmail es un agente de transporte de correo electrónico, que mueve
mensajes entre máquinas. Implementa facilidades de internetwork y
rutado, caracterizando cambio de nombres (aliases) y envío a nuevas
direcciones ( forwarding ), rutado automático para gateways de la red
y configuración flexible. Necesitarás del sendmail si deseas enviar y
recibir mensajes a través de la Internet.

%description -l fr.UTF-8
Sendmail est un agent de transport de courrier, qui est le programme
transférent le courrier d'une machine à l'autre. Sendmail implémente
une facilité générale de routage de courrier entre les réseaux, permet
l'"aliasing" et le "forwarding", un routage automatique sur les
passerelles du réseau, et une configuration flexible.

%description -l ko.UTF-8
Sendamil은 매우 널리 사용되는 Mail 전송 프로그램이다(MTA). Mail 전송
프로그램들(MTA)은 어떠한 machine에서 다른 machine으로 메일을 보내며
Sendmail은 e-mail을 읽기위해 사용하는 client program은 아니다.
Sendamil은 원하는 곳으로 Internet이나 Network를 통해 e-mail을 보내는
역할을 하는 backgrond에서 작업을 하는 프로그램이다.

%description -l pl.UTF-8
Sendmail jest programem umożliwiającym wymianę poczty elektronicznej
między komputerami w sieci (MTA). Zajmuje się przekazywaniem poczty
elektronicznej między bramkami pocztowymi i dostarczaniem przesyłek na
konta docelowe. Bardzo dobrze obsługuje aliasy pocztowe a jego
dodatkowym atutem jest prosta konfiguracja. Dzięki rozbudowanym
możliwościom konfiguracyjnym jest w stanie dostarczać przesyłki za
pośrednictwem protokołów: SMTP, ESMTP, UUCP, X.400 i innych.

%description -l pt_BR.UTF-8
O sendmail é um agente de transporte de correio eletrônico, que move
mensagens entre máquinas. Ele implementa facilidades de internetwork e
roteamento, caracterizando troca de nomes (aliases) e remessa a novos
endereços ( forwarding ), roteamento automático para gateways da rede
e configuração flexível.

%description -l ru.UTF-8
Sendmail - это Mail Transport Agent, программа пересылающая почту с
машины на машину. Sendmail предоставляет стандартные средства
межсетевой маршрутизации почты, aliasing, forwarding, автоматическую
маршрутизацию для сетевых шлюзов и гибкий механизм конфигурации.

%description -l tr.UTF-8
Sendmail, bir mektubu bir makineden diğerine taşır. Pek çok davranışı
ayarlanabilir. Internet üzerinden mektup almak veya göndermek
istiyorsanız bu pakete gereksiniminiz olacaktır.

%description -l uk.UTF-8
Sendmail - це Mail Transport Agent, програма що пересилає пошту з
машини на машину. Sendmail надає стандартні засоби міжмережевої
маршрутизації пошти, aliasing, forwarding, автоматичну маршрутизацію
для мережевих шлюзів та гнучкий механізм маршрутизації.

%package -n libmilter-devel
Summary:	Header files and static libmilter library
Summary(pl.UTF-8):	Pliki nagłówkowe i statyczna biblioteka libmilter
Group:		Development/Libraries
Provides:	sendmail-devel
Obsoletes:	sendmail-devel

%description -n libmilter-devel
Header files and static libmilter library.

%description -n libmilter-devel -l pl.UTF-8
Pliki nagłówkowe i statyczna biblioteka libmilter.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%{?with_pgsql:%patch7 -p1}

sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/pld.mc

install %{SOURCE7} config.m4

# Ac-specific hack:
# It's problem with _simultanous_ building when builders are on the same
# machine. These are anonymous SHM tests (AFAIR) which must fail when called
# simultanously...
#
# send on builders requests only for some arch - it won't fail.
#- blues
%ifarch i386 i586 athlon
%{__sed} -i -e 's/^\(smtest.*t-shm\)/dnl \1/' libsm/Makefile.m4
%{__sed} -i -e 's/^\(smtest.*t-sem\)/dnl \1/' libsm/Makefile.m4
%endif

%build
echo "define(\`confCC', \`%{__cc}')" >> config.m4
%ifarch sparc sparc64
echo "define(\`confOPTIMIZE', \`%{rpmcflags} -DUSE_VENDOR_CF_PATH=1 -DSM_CONF_SEM=0 -DNETINET6')" >> config.m4
%else
echo "define(\`confOPTIMIZE', \`%{rpmcflags} -DUSE_VENDOR_CF_PATH=1 -DNETINET6')" >> config.m4
%endif
echo "APPENDDEF(\`confINCDIRS', \`-I/usr/include/sasl')" >> config.m4
echo "define(\`confLIBSEARCHPATH', \`/%{_lib} %{_prefix}/%{_lib}')" >> config.m4
echo "define(\`confLIBSEARCH', \`db resolv')" >> config.m4
%if 0%{!?debug:1}
echo "define(\`confLDOPTS', \`-s')" >> config.m4
%endif
%if %{with ldap}
echo "APPENDDEF(\`confMAPDEF', \`-DLDAPMAP')" >> config.m4
echo "APPENDDEF(\`confLIBS', \`-lldap -llber')" >> config.m4
%endif
%if %{with pgsql}
echo "APPENDDEF(\`confENVDEF', \`-DSASL')" >> config.m4
echo "APPENDDEF(\`confMAPDEF', \`-DPGSQLMAP')" >> config.m4
echo "APPENDDEF(\`confLIBS', \`-lpq -lresolv')" >> config.m4
echo "APPENDDEF(\`confLIBS', \`-lsasl -lcrypto')" >> config.m4
%endif
%if %{with tls}
echo "APPENDDEF(\`confENVDEF', \`-DSTARTTLS')" >> config.m4
echo "APPENDDEF(\`confENVDEF', \`-D_FFR_DEAL_WITH_ERROR_SSL')" >> config.m4
echo "APPENDDEF(\`confLIBS', \`-lssl -lcrypto')" >> config.m4
echo "APPENDDEF(\`confENVDEF', \`-D_FFR_SMTP_SSL')" >> config.m4
%endif

echo "APPENDDEF(\`confENVDEF', \`-DMILTER')" >> config.m4

%ifarch sparc
%define		Build		sparc32 sh Build
%else
%define		Build		sh Build
%endif

cd sendmail	&& %{Build} -f ../config.m4
cd ../mailstats	&& %{Build} -f ../config.m4
cd ../rmail	&& %{Build} -f ../config.m4
cd ../makemap	&& %{Build} -f ../config.m4
cd ../praliases	&& %{Build} -f ../config.m4
cd ../smrsh	&& %{Build} -f ../config.m4
cd ../libmilter	&& %{Build} -f ../config.m4
cd ../cf/cf
m4 pld.mc > pld.cf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5,8} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,pam.d,monit,sysconfig,sasl,smrsh,security} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_prefix}/lib} \
	$RPM_BUILD_ROOT{%{_datadir}/sendmail-cf,%{_libdir}} \
	$RPM_BUILD_ROOT/var/{log,spool/mqueue} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_includedir}}

OBJDIR=obj.$(uname -s).$(uname -r).$(\
%ifarch sparc
sparc32 \
%endif
uname -m)

IDNU=`id -nu`
IDNG=`id -ng`
SMINSTOPT="DESTDIR=$RPM_BUILD_ROOT SBINOWN=$IDNU SBINGRP=$IDNG \
	UBINOWN=$IDNU UBINGRP=$IDNG MANOWN=$IDNU MANGRP=$IDNG \
	CFOWN=$IDNU CFGRP=$IDNG MSPQOWN=$IDNU GBINGRP=$IDNG GBINOWN=$IDNU \
	BINOWN=$IDNU BINGRP=$IDNG LIBOWN=$IDNU LIBGRP=$IDNG INCOWN=$IDNU INCGRP=$IDNG"

%{__make} -C $OBJDIR/sendmail install \
	$SMINSTOPT
%{__make} -C $OBJDIR/mailstats install \
	$SMINSTOPT
%{__make} -C $OBJDIR/praliases install \
	$SMINSTOPT
%{__make} -C $OBJDIR/rmail force-install \
	$SMINSTOPT
%{__make} -C $OBJDIR/makemap install \
	$SMINSTOPT
%{__make} -C $OBJDIR/smrsh install \
	$SMINSTOPT
%{__make} -C $OBJDIR/libmilter install \
	$SMINSTOPT \
	LIBDIR=%{_libdir}

ln -sf %{_sbindir}/makemap $RPM_BUILD_ROOT%{_bindir}/makemap

# install the cf files
cd cf
rm -f cf/{Build,Makefile} feature/*~
cp -a * $RPM_BUILD_ROOT%{_datadir}/sendmail-cf
cd -

# sendmail.{cf,mc}
install cf/cf/pld.cf $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf
sed -e 's|@@PATH@@|%{_datadir}/sendmail-cf|' < %{SOURCE6} \
	> $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.mc

%if %{with pgsql}
install bluelabs.mc $RPM_BUILD_ROOT%{_sysconfdir}/bluelabs.mc
%endif

# submit.mc (submit.cf is installed automatically)
install cf/cf/submit.mc $RPM_BUILD_ROOT%{_sysconfdir}

echo "# local-host-names - include all aliases for your machine here." \
	> $RPM_BUILD_ROOT%{_sysconfdir}/local-host-names
#"vim ruuls

ln -sf %{_sbindir}/sendmail $RPM_BUILD_ROOT%{_prefix}/lib/sendmail

# dangling symlinks
for f in hoststat mailq newaliases purgestat; do
	ln -sf %{_sbindir}/sendmail $RPM_BUILD_ROOT%{_bindir}/${f}
done

for map in virtusertable access domaintable mailertable; do
	touch $RPM_BUILD_ROOT%{_sysconfdir}/${map}
	$RPM_BUILD_ROOT%{_sbindir}/makemap -C $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf hash \
		$RPM_BUILD_ROOT%{_sysconfdir}/${map}.db < $RPM_BUILD_ROOT%{_sysconfdir}/${map}
done

install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/aliases
$RPM_BUILD_ROOT%{_sbindir}/makemap -C $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf hash \
	$RPM_BUILD_ROOT%{_sysconfdir}/aliases.db < %{SOURCE3}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/sendmail
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/Makefile
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sasl/Sendmail.conf
install %{SOURCE13} $RPM_BUILD_ROOT/etc/pam.d/smtp
install %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/access
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/mailertable
install %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/virtusertable
install %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/domaintable
install %{SOURCE14} $RPM_BUILD_ROOT/etc/monit/

touch $RPM_BUILD_ROOT/etc/security/blacklist.smtp

mv -f smrsh/README README.smrsh
mv -f cf/README README.cf
mv -f doc/op/op.me .

bzip2 -dc %{SOURCE4} | tar xf -

# for perl-Sendmail-Milter
install $OBJDIR/libsm/libsm.a $OBJDIR/libsmutil/libsmutil.a \
	$RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 25 smmsp
%useradd -u 25 -d /var/spool/clientqueue -s /bin/false -c "Sendmail Message Submission Program" -g smmsp smmsp

%post
umask 022
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
%service sendmail restart "sendmail daemon"

%preun
if [ "$1" = "0" ]; then
	%service sendmail stop
	/sbin/chkconfig --del sendmail
fi

%postun
if [ "$1" = "0" ]; then
	%userremove smmsp
	%groupremove smmsp
fi

# removal of compatibility links
%triggerpostun -- sendmail < 8.10.1
/sbin/chkconfig --add sendmail

%files
%defattr(644,root,root,755)
%doc FAQ KNOWNBUGS README* op.me RELEASE_NOTES examples/
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
%{_prefix}/lib/sendmail

%{_mandir}/man1/mailq.1*
%{_mandir}/man1/newaliases.1*
%{_mandir}/man5/aliases.5*
%{_mandir}/man8/mailstats.8*
%{_mandir}/man8/makemap.8*
%{_mandir}/man8/praliases.8*
%{_mandir}/man8/rmail.8*
%{_mandir}/man8/sendmail.8*
%{_mandir}/man8/smrsh.8*

%dir /etc/smrsh
%dir %{_sysconfdir}
/var/log/statistics
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sendmail.cf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sendmail.mc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/submit.cf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/submit.mc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/local-host-names
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/aliases
%{?with_pgsql:%{_sysconfdir}/bluelabs.mc}
%attr(644,root,mail) %ghost %{_sysconfdir}/aliases.db
%attr(770,root,smmsp) %dir /var/spool/clientmqueue
%attr(750,root,mail) %dir /var/spool/mqueue

%config %{_sysconfdir}/Makefile
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/access
%ghost %{_sysconfdir}/access.db
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/domaintable
%ghost %{_sysconfdir}/domaintable.db
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mailertable
%ghost %{_sysconfdir}/mailertable.db
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/virtusertable
%ghost %{_sysconfdir}/virtusertable.db
%config(noreplace) %{_sysconfdir}/helpfile

%attr(754,root,root) /etc/rc.d/init.d/sendmail
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sendmail
%config(noreplace) %verify(not md5 mtime size) /etc/sasl/Sendmail.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/smtp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.smtp
%config(noreplace) %verify(not md5 mtime size) /etc/monit/*.monitrc

%dir %{_datadir}/sendmail-cf
%dir %{_datadir}/sendmail-cf/cf
%{_datadir}/sendmail-cf/cf/pld.mc
%{_datadir}/sendmail-cf/feature
%{_datadir}/sendmail-cf/m4
%{_datadir}/sendmail-cf/mailer
%dir %{_datadir}/sendmail-cf/ostype
%{_datadir}/sendmail-cf/ostype/linux.m4
%dir %{_datadir}/sendmail-cf/sh
%{_datadir}/sendmail-cf/sh/makeinfo.sh
%{_datadir}/sendmail-cf/siteconfig

%files -n libmilter-devel
%defattr(644,root,root,755)
%{_libdir}/libmilter.a
%{_libdir}/libsm.a
%{_libdir}/libsmutil.a
%{_includedir}/libmilter
