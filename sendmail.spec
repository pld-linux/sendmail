#
# Conditional build:
%bcond_without	db3	# use db instead of db3 package
%bcond_without	ldap	# without LDAP support
%bcond_without	tls	# without TLS (SSL) support
%bcond_with	pgsql	# with PostgreSQL support (bluelabs)
#
Summary:	A widely used Mail Transport Agent (MTA)
Summary(de):	sendmail-Mail-Übertragungsagent
Summary(es):	Sendmail - agente de transporte de mail
Summary(fr):	Agent de transport de courrier sendmail
Summary(ko):	SMTP_AUTH¿Í TLS¸¦ Áö¿øÇÏ´Â Mail Àü¼Û ÇÁ·Î±×·¥(MTA)
Summary(pl):	Sendmail - serwer poczty elektronicznej
Summary(pt_BR):	Sendmail - agente de transporte de mail
Summary(ru):	ğÏŞÔÏ×ÙÊ ÔÒÁÎÓĞÏÒÔÎÙÊ ÁÇÅÎÔ sendmail
Summary(tr):	Elektronik posta hizmetleri sunucusu
Summary(uk):	ğÏÛÔÏ×ÉÊ ÔÒÁÎÓĞÏÒÔÎÉÊ ÁÇÅÎÔ sendmail
Name:		sendmail
Version:	8.12.11
Release:	7.1
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
# Source0-md5:	fafda7f8043f0c34b9aa295618aa598c
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
Patch0:		%{name}-makemapman.patch
Patch1:		%{name}-smrsh-paths.patch
Patch2:		%{name}-rmail.patch
Patch3:		%{name}-os-paths.patch
Patch4:		%{name}-m4path.patch
Patch5:		%{name}-redirect.patch
Patch6:		%{name}-hprescan-dos.patch
Patch7:		http://blue-labs.org/clue/bluelabs.patch-8.12.3
BuildRequires:	cyrus-sasl-devel
%{?with_db3:BuildRequires:	db3-devel}
%{!?with_db3:BuildRequires:	db-devel >= 4.1.25}
BuildRequires:	man
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_tls:BuildRequires:	openssl-devel >= 0.9.6m}
%{?with_pgsql:BuildRequires:	postgresql-devel}
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post):	awk
Requires(post):	textutils
Requires(post,preun):/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
%{!?with_db3:Requires:	db >= 4.1.25}
Requires:	m4
Requires:	procmail
Requires:	pam >= 0.77.3
Provides:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	courier
Obsoletes:	exim
Obsoletes:	masqmail
Obsoletes:	nullmailer
Obsoletes:	omta
Obsoletes:	postfix
Obsoletes:	qmail
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smail
Obsoletes:	smtpdaemon
Obsoletes:	ssmtp
Obsoletes:	zmailer

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

%description -l es
sendmail es un agente de transporte de correo electrónico, que mueve
mensajes entre máquinas. Implementa facilidades de internetwork y
rutado, caracterizando cambio de nombres (aliases) y envío a nuevas
direcciones ( forwarding ), rutado automático para gateways de la red
y configuración flexible. Necesitarás del sendmail si deseas enviar y
recibir mensajes a través de la Internet.

%description -l fr
Sendmail est un agent de transport de courrier, qui est le programme
transférent le courrier d'une machine à l'autre. Sendmail implémente
une facilité générale de routage de courrier entre les réseaux, permet
l'\"aliasing\" et le \"forwarding\", un routage automatique sur les
passerelles du réseau, et une configuration flexible.

%description -l ko
SendamilÀº ¸Å¿ì ³Î¸® »ç¿ëµÇ´Â Mail Àü¼Û ÇÁ·Î±×·¥ÀÌ´Ù(MTA). Mail Àü¼Û
ÇÁ·Î±×·¥µé(MTA)Àº ¾î¶°ÇÑ machine¿¡¼­ ´Ù¸¥ machineÀ¸·Î ¸ŞÀÏÀ» º¸³»¸ç
SendmailÀº e-mailÀ» ÀĞ±âÀ§ÇØ »ç¿ëÇÏ´Â client programÀº ¾Æ´Ï´Ù.
SendamilÀº ¿øÇÏ´Â °÷À¸·Î InternetÀÌ³ª Network¸¦ ÅëÇØ e-mailÀ» º¸³»´Â
¿ªÇÒÀ» ÇÏ´Â backgrond¿¡¼­ ÀÛ¾÷À» ÇÏ´Â ÇÁ·Î±×·¥ÀÌ´Ù.

%description -l pl
Sendmail jest programem umo¿liwiaj±cym wymianê poczty elektronicznej
miêdzy komputerami w sieci (MTA). Zajmuje siê przekazywaniem poczty
elektronicznej miêdzy bramkami pocztowymi i dostarczaniem przesy³ek na
konta docelowe. Bardzo dobrze obs³uguje aliasy pocztowe a jego
dodatkowym atutem jest prosta konfiguracja. Dziêki rozbudowanym
mo¿liwo¶ciom konfiguracyjnym jest w stanie dostarczaæ przesy³ki za
po¶rednictwem protoko³ów: SMTP, ESMTP, UUCP, X.400 i innych.

%description -l pt_BR
O sendmail é um agente de transporte de correio eletrônico, que move
mensagens entre máquinas. Ele implementa facilidades de internetwork e
roteamento, caracterizando troca de nomes (aliases) e remessa a novos
endereços ( forwarding ), roteamento automático para gateways da rede
e configuração flexível.

%description -l ru
Sendmail - ÜÔÏ Mail Transport Agent, ĞÒÏÇÒÁÍÍÁ ĞÅÒÅÓÙÌÁÀİÁÑ ĞÏŞÔÕ Ó
ÍÁÛÉÎÙ ÎÁ ÍÁÛÉÎÕ. Sendmail ĞÒÅÄÏÓÔÁ×ÌÑÅÔ ÓÔÁÎÄÁÒÔÎÙÅ ÓÒÅÄÓÔ×Á
ÍÅÖÓÅÔÅ×ÏÊ ÍÁÒÛÒÕÔÉÚÁÃÉÉ ĞÏŞÔÙ, aliasing, forwarding, Á×ÔÏÍÁÔÉŞÅÓËÕÀ
ÍÁÒÛÒÕÔÉÚÁÃÉÀ ÄÌÑ ÓÅÔÅ×ÙÈ ÛÌÀÚÏ× É ÇÉÂËÉÊ ÍÅÈÁÎÉÚÍ ËÏÎÆÉÇÕÒÁÃÉÉ.

%description -l tr
Sendmail, bir mektubu bir makineden diğerine taşır. Pek çok davranışı
ayarlanabilir. Internet üzerinden mektup almak veya göndermek
istiyorsanız bu pakete gereksiniminiz olacaktır.

%description -l uk
Sendmail - ÃÅ Mail Transport Agent, ĞÒÏÇÒÁÍÁ İÏ ĞÅÒÅÓÉÌÁ¤ ĞÏÛÔÕ Ú
ÍÁÛÉÎÉ ÎÁ ÍÁÛÉÎÕ. Sendmail ÎÁÄÁ¤ ÓÔÁÎÄÁÒÔÎ¦ ÚÁÓÏÂÉ Í¦ÖÍÅÒÅÖÅ×Ï§
ÍÁÒÛÒÕÔÉÚÁÃ¦§ ĞÏÛÔÉ, aliasing, forwarding, Á×ÔÏÍÁÔÉŞÎÕ ÍÁÒÛÒÕÔÉÚÁÃ¦À
ÄÌÑ ÍÅÒÅÖÅ×ÉÈ ÛÌÀÚ¦× ÔÁ ÇÎÕŞËÉÊ ÍÅÈÁÎ¦ÚÍ ÍÁÒÛÒÕÔÉÚÁÃ¦§.

%package devel
Summary:	Header files and static libmilter library
Summary(pl):	Pliki nag³ówkowe i statyczna biblioteka libmilter
Group:		Development/Libraries

%description devel
Header files and static libmilter library.

%description devel -l pl
Pliki nag³ówkowe i statyczna biblioteka libmilter.

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

%build
echo "define(\`confCC', \`%{__cc}')" >> config.m4
echo "define(\`confOPTIMIZE', \`%{rpmcflags} -DUSE_VENDOR_CF_PATH=1 -DNETINET6')" >> config.m4
echo "APPENDDEF(\`confINCDIRS', \`-I/usr/include/sasl')" >> config.m4
echo "define(\`confLIBSEARCHPATH', \`/%{_lib} /usr/%{_lib}')" >> config.m4
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

cd sendmail	&& sh Build -f ../config.m4
cd ../mailstats	&& sh Build -f ../config.m4
cd ../rmail	&& sh Build -f ../config.m4
cd ../makemap	&& sh Build -f ../config.m4
cd ../praliases	&& sh Build -f ../config.m4
cd ../smrsh	&& sh Build -f ../config.m4
cd ../libmilter	&& sh Build -f ../config.m4
cd ../cf/cf
m4 pld.mc > pld.cf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig,sasl,smrsh}} \
	$RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT%{_libdir} \
	$RPM_BUILD_ROOT%{_mandir}/man{1,5,8} \
	$RPM_BUILD_ROOT/var/log $RPM_BUILD_ROOT/var/spool/mqueue \
	$RPM_BUILD_ROOT%{_libdir}/sendmail-cf \
	$RPM_BUILD_ROOT/etc/pam.d $RPM_BUILD_ROOT%{_includedir}\

OBJDIR=obj.$(uname -s).$(uname -r).$(arch)

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
cp -ar * $RPM_BUILD_ROOT%{_libdir}/sendmail-cf
cd -

# sendmail.{cf,mc}
install cf/cf/pld.cf $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf
sed -e 's|@@PATH@@|%{_libdir}/sendmail-cf|' < %{SOURCE6} \
	> $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.mc

%if %{with pgsql}
install bluelabs.mc $RPM_BUILD_ROOT%{_sysconfdir}/bluelabs.mc
%endif

# submit.mc (submit.cf is installed automatically)
install cf/cf/submit.mc $RPM_BUILD_ROOT%{_sysconfdir}

echo "# local-host-names - include all aliases for your machine here." \
	> $RPM_BUILD_ROOT%{_sysconfdir}/local-host-names

ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail

# dangling symlinks
for f in hoststat mailq newaliases purgestat ; do
	ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/${f}
done

for map in virtusertable access domaintable mailertable ; do
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

mv -f smrsh/README README.smrsh
mv -f cf/README README.cf
mv -f doc/op/op.me .

bzip2 -dc %{SOURCE4} | tar xf -

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid smmsp`" ]; then
	if [ "`/usr/bin/getgid smmsp`" != "25" ]; then
		echo "Error: group smmsp doesn't have gid=25. Correct this before installing sendmail." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 25 -r -f smmsp
fi
if [ -n "`/bin/id -u smmsp 2>/dev/null`" ]; then
	if [ "`/bin/id -u smmsp`" != "25" ]; then
		echo "Error: user smmsp doesn't have uid=25. Correct this before installing sendmail." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 25 -r -d /var/spool/clientqueue -s /bin/false -c "Sendmail Message Submission Program" -g smmsp smmsp 1>&2
fi

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
%{_libdir}/sendmail

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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sendmail.cf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sendmail.mc
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/submit.cf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/submit.mc
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/local-host-names
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/aliases
%{?with_pgsql:%{_sysconfdir}/bluelabs.mc}
%attr(644,root,mail) %ghost %{_sysconfdir}/aliases.db
%attr(770,root,smmsp) %dir /var/spool/clientmqueue
%attr(750,root,mail) %dir /var/spool/mqueue

%config %{_sysconfdir}/Makefile
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/access
%ghost %{_sysconfdir}/access.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/domaintable
%ghost %{_sysconfdir}/domaintable.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailertable
%ghost %{_sysconfdir}/mailertable.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/virtusertable
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

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmilter.a
%{_includedir}/libmilter
