Summary:	A widely used Mail Transport Agent (MTA)
Summary(de):	sendmail-Mail-�bertragungsagent
Summary(fr):	Agent de transport de courrier sendmail
Summary(pl):	Sendmail -- aplikacja do obs�ugi poczty elektronicznej
Summary(tr):	Elektronik posta hizmetleri sunucusu
Name:		sendmail
Version:	8.11.2
Release:	1
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
Patch0:		%{name}-redhat.patch
Patch1:		%{name}-makemapman.patch
Patch2:		%{name}-smrsh-paths.patch
Patch3:		%{name}-rmail.patch
Patch4:		%{name}-manpath.patch
Patch5:		%{name}-m4path.patch
Patch6:		%{name}-dtelnet.patch
Patch7:		%{name}-pld.mc.patch
Patch8:		%{name}-redirect.patch
Patch9:		%{name}-ipv6-glibc-2.2.patch
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
mi�dzy komputerami w sieci internet. Zajmuje si� przekazywaniem poczty
elektronicznej mi�dzy bramkami pocztowymi i dostarczaniem przesy�ek na
konta docelowe. Bardzo dobrze obs�uguje aliasy pocztowe a jego
dodatkowym atutem jest prosta konfiguracja. Dzi�ki rozbudowanym
mo�liwo�ciom konfiguracyjnym jest w stanie dostarcza� przesy�ki za
po�rednictwem protoko��w: SMTP, ESMTP, UUCP, X.400 i innych.

%description -l tr
Sendmail, bir mektubu bir makineden di�erine ta��r. Pek �ok davran���
ayarlanabilir. Internet �zerinden mektup almak veya g�ndermek
istiyorsan�z bu pakete gereksiniminiz olacakt�r.

%package cf
Summary:	The files needed to reconfigure Sendmail
Summary(de):	sendmail-Konfigurationsdateien und m4-Makros 
Summary(fr):	fichiers de configuration sendmail et macros m4
Summary(pl):	Pliki potrzebne do rekonfiguracji Sendmaila
Summary(tr):	sendmail ayar dosyalar� ve makrolar�
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}
Requires:	m4

%description cf
This package includes the configuration files which you'd need to
generate the sendmail.cf file distributed with the sendmail package.
You'll need the sendmail-cf package if you ever need to reconfigure
and rebuild your sendmail.cf file. For example, the default
sendmail.cf file is not configured for UUCP. If someday you needed to
send and receive mail over UUCP, you'd need to install the sendmail-cf
package to help you reconfigure Sendmail.

%description -l de cf
Dieses Paket enth�lt alle Konfigurationsdateien, die zum Erzeugen der
Sendmail.cf-Datei erforderlich sind, die mit dem Basis- Sendmail-Paket
geliefert wird. Sie werden darauf nicht verzichten wollen, wenn Sie
Ihre Sendmail-cf-Datei neu konfigurieren und bauen wollen. Die
Standard-Sendmail.cf.-Datei ist z.B. nicht f�r UUCP konfiguriert. Wenn
Sie also Post �ber UUCP versenden und empfangen wollen, brauchen Sie
es f�r eine Neukonfiguration.

%description -l fr cf
Ce package contient tous les fichiers de configuration utilis�s pour
g�n�rer le fichier sendmail.cf distribu� avec le package de base
sendmail. Vous n'aurez besoin de ce package que pour reconfigurer et
reconstruire votre fichier sendmail.cf. Par exemple Le sendmail.cf par
d�faut n'est pas configur� pour UUCP. Si vous devez recevoir des mails
avec UUCP, vous aurez besoin de ce package pour reconfigurer sendmail.

%description -l pl cf
Ten pakiet zawiera pliki konfiguracyjne, kt�rych b�dziesz potrzebowa�,
by wygenerowa� plik sendmail.cf, zawarty w pakiecie sendmail. B�dziesz
potrzebowa� pakietu sendmail-cf je�eli potrzebujesz zrekonfigurowa� i
przebudowa� plik sendmail.cf. Na przyk�ad, domy�lny sendmail.cf nie
jest skonfigurowany dla UUCP. Je�eli kiedy� b�dziesz potrzebowa�
wysy�a� i odbiera� porzt� po UUCP, b�dziesz musia� zainstalowa� pakiet
sendmail-cf, kt�ry pomo�e ci zrekonfigurowa� Sendmaila.

%description -l tr cf
Bu paket, sendmail paketi ile da��t�lan sendmail.cf dosyas�n�
olu�turmak i�in kullan�lan t�m ayar dosyalar�n� i�erir. sendmail.cf
dosyas�n� ba�tan ayarlay�p kurmak i�in kullan�l�r.

%package doc
Summary:	Documentation about the Sendmail Mail Transport Agent program
Summary(de):	Sendmail-Dokumentation 
Summary(fr):	Documentation de sendmail
Summary(pl):	Dokumentacja do Sendmaila
Summary(tr):	sendmail belgeleri
Group:		Documentation
Group(de):	Dokumentation
Group(pl):	Dokumentacja
Requires:	%{name} = %{version}

%description doc
The sendmail-doc package contains documentation about the Sendmail
Mail Transport Agent (MTA) program, including release notes, the
Sendmail FAQ and a few papers written about Sendmail. The papers are
provided in PostScript(TM) and troff formats.

%description -l de doc
Dieses Paket beinhaltet Release-Notes, die h�ufigsten Fragen und
Antworten (FAQ) zu Sendmail sowie ein paar Artikel �ber Sendmail. Die
letzteren sind sowohl in PostScript als auch in troff verf�gbar.

%description -l fr doc
Paquetage contenant les remarques sur la version, la FAQ sendmail et
quelques articles sur sendmail. Ces articles sont au format PostScript
et troff.

%description -l pl doc
Ten pakiet zawiera dokumentacj� do programu Sendmail Mail Transport
Agent (MTA). Dokumentacja zwawiera informacje o zmianach w bie��cej
wersji i FAQ - najcz�sciej zadawane pytania. Dokumentacja dost�pna
jest w formacie PostScript(TM) oraz troff.

%description -l tr doc
Bu paket, sendmail ile ilgili �ok�a sorulan sorular� ve sendmail
hakk�nda yaz�lm�� makalelerin bir k�sm�n� i�ermektedir.

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

# seems to be obsoleted...
#tar xf %{SOURCE2} -C cf

sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/redhat.mc

install %{SOURCE7} config.m4

%build

RPM_OPT_FLAGS="%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS} \
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
