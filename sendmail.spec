Summary:	Sendmail -- mail transport agent
Summary(pl):	Sendmail -- aplikacja do obs³ugi poczty elektronicznej
Name:		sendmail
Version:	8.9.3
Release:	3
Copyright:	distributable (similar to, but not quite BSD)
Group:		Daemons
Group(pl):	Serwery
Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
Source1:	site.Linux.m4
Source2:	aliases
Source3:	%{name}.init
Source4:	site.Linux.ppc.m4
Source5:	%{name}.sysconfig
Patch0:		%{name}-ipv6.patch
Patch1:		%{name}-dtelnet.patch
Patch2:		%{name}-path.patch
Patch3:		%{name}-rmail.patch
Patch4:		%{name}-pld.mc.patch
Patch5:		%{name}-redirect.patch
Patch6:		%{name}-smrsh.patch
Patch7:		%{name}-release.patch
BuildRoot:	/tmp/%{name}-%{version}-root
URL:		http://www.sendmail.org
Prereq:		/sbin/chkconfig
Obsoletes:	zmail
Obsoletes:	qmail
Obsoletes:	smail

%description 
Sendmail is a Mail Transport Agent, which is the program
that moves mail from one machine to another.  Sendmail implements a
general internetwork mail routing facility, featuring aliasing and
forwarding, automatic routing to network gateways, and flexible
configuration.

If you need the ability to send and receive mail via the internet
you'll need sendmail.

%description -l pl
Sendmail jest programem umo¿liwiaj±cym wymianê poczty elektronicznej
miêdzy komputerami w sieci internet. Zajmuje siê przekazywaniem poczty
elektronicznej miêdzy bramkami pocztowymi i dostarczaniem przesy³ek na 
konta docelowe. Bardzo dobrze obs³uguje aliasy pocztowe a jego dodatkowym 
atutem jest prosta konfiguracja. Dziêki rozbudowanym mo¿liwo¶ciom 
konfiguracyjnym jest w stanie dostarczaæ przesy³ki za po¶rednictwem 
protoko³ów: SMTP, ESMTP, UUCP, X.400 i innych.

Je¿eli masz zamiar korzystaæ z poczty elektronicznej w sieci internet
oraz 6bone to zainstaluj ten pakiet.

%package	cf
Summary:	Sendmail configuration files and m4 macros
Summary(pl):	Pliki konfiguracyjne oraz makra m4 dla sendmaila
Group:		Daemons
Group(pl):	Serwery
Requires:	%{name} = %{version}

%description cf
This package contains all the configuration files used to generate
the sendmail.cf file distributed with the base sendmail package.
You'll want this package if you need to reconfigure and rebuild
your sendmail.cf file.  For example, the default sendmail.cf is
not configured for UUCP.  If you need to send and receive mail
over UUCP, you may need this package to help you reconfigure sendmail.

%description -l pl cf
Pakiet ten zawiera wszystkie pliki konfiguracyjne u¿ywane do gene-
rowania pliku sendmail.cf, znajduj±cego siê w pakiecie bazowym.
Bêdziesz potrzebowa³ tego pakietu je¿eli chcesz zmieniæ i przebudowaæ
konfiguracjê swojego sendmaila. Na przyk³ad, standardowy plik konfigu-
racyjny nie zawiera wspomagania dla poczty po UUCP. Je¿eli chcesz wy-
sy³aæ i odbieraæ pocztê po UUCP bêdziesz potrzebowa³ tego pakietu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7	-p1

%build
ID="`id -u`"
GID="`id -g`"
OPT=$RPM_OPT_FLAGS

cat %{SOURCE1} |sed s/gid/"$GID"/g | sort | sed s/id/"$ID"/g | sort | \
sed s/opt/"$OPT"/g > BuildTools/Site/site.Linux.m4

cd src
./makesendmail
cd ../
make makemap mailstats praliases rmail 
make smrsh LDOPTS="-s -static" 
(
cd cf/cf
/usr/bin/m4 pld.mc >> ./sendmail.cf
)

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{mail,rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT/usr/{bin,lib,sbin,share/sendmail-cf,libexec}
install -d $RPM_BUILD_ROOT/usr/share/{man/man{1,5,8},misc}
install -d $RPM_BUILD_ROOT/var/{run,spool/{mqueue,mail}}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/mail/aliases
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/sendmail

touch $RPM_BUILD_ROOT/etc/mail/{sendmail.{ct,cw},relay-domains}

for i in aliases access domaintable genericstable mailertable majordomo \
virtusertable
do touch $RPM_BUILD_ROOT/etc/mail/$i{,.db}
done

install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail

make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT OPTIONS=force-install rmail 

for i in hoststat mailq newaliases purgestat
	do ln -sf ../sbin/sendmail  $RPM_BUILD_ROOT/usr/bin/$i
done
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail

install cf/cf/sendmail.cf $RPM_BUILD_ROOT/etc/mail

cp cf/* $RPM_BUILD_ROOT/usr/share/sendmail-cf/ -a

mv $RPM_BUILD_ROOT/etc/mail/*.hf $RPM_BUILD_ROOT/usr/share/misc

cat $RPM_BUILD_ROOT/etc/mail/sendmail.cf |sed s/DZ8.9.3/DZLinux/g > \
    $RPM_BUILD_ROOT/etc/mail/sendmail.cf.new

mv $RPM_BUILD_ROOT/etc/mail/sendmail.cf.new $RPM_BUILD_ROOT/etc/mail/sendmail.cf    

cp smrsh/README smrsh/SMRSH.txt

gzip -9fn $RPM_BUILD_ROOT/usr/share/man/man[158]/*
gzip -9fn README KNOWNBUGS RELEASE_NOTES smrsh/SMRSH.txt

%post
/sbin/chkconfig --add sendmail
if [ -f /var/lock/subsys/sendmail ]; then
    /etc/rc.d/init.d/sendmail restart >&2
fi

%preun
if [ -e /var/lock/sybsys/sendmail ]; then
    /etc/rc.d/init.d/sendmail stop &>/dev/null
fi

if [ $1 = 0 ]; then
   /sbin/chkconfig --del sendmail
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,KNOWNBUGS,RELEASE_NOTES}.gz 
%doc smrsh/SMRSH.txt.gz

%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/mail/*
%attr(644,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*
%attr(755,root,root) /etc/rc.d/init.d/*

%attr(755,root,root) /usr/bin/*

%attr(755,root,root) /usr/sbin/mailstats
%attr(755,root,root) /usr/sbin/makemap
%attr(755,root,root) /usr/sbin/praliases

%attr(755,root,root) /usr/sbin/sendmail

%attr(755,root,root) /usr/lib/sendmail
%attr(755,root,root) /usr/sbin/smrsh

/usr/share/man/man[158]/*
/usr/share/misc/*.hf

%ghost /var/run/sendmail.st

%files cf
%defattr(644,root,root,755)

%dir /usr/share/sendmail-cf
%attr(-,root,root) /usr/share//sendmail-cf/*

%changelog
* Fri Jan 22 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [8.9.2-3d]
- fixed group && owner ELF binaries,
- fixed init script,
- fixed %preun.

* Sun Jan 17 1999 Wojtek ¦lusarczyk <wojtek@SHADOW.EU.ORG>
  [8.9.2-2d]
- fixed sendmail.init script,
- compressed man pages && documentation,
  by Micha³ Zalewski <lcamtuf@ids.pl>
- added patch against DoS ;)
- added %{name}-redirect.patch

* Thu Sep 10 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [8.9.1-1d]
- updated to 8.9.1a && build for PLD Tornado,
- build with IPv6 support
  (patches was prepared by John Kennedy <jk@csuchico.edu>),
- build with Detect-Telnet support,
- removed subpackage doc.

* Thu Jul 30 1998 Wojtek Slusarczyk <wojtek@shadow.eu.org>
  [8.8.8-1d]
- build against glibc-2.1,
- updated to 8.8.8,
- added IPv6 support,
- translation modified for pl,
- moved configfiles to /etc/mail,
- changed permissions of all binaries to 711,
- moved %changelog at the end of spec,
- build from non root's account.
