Summary:	Sendmail -- mail transport agent
Summary(pl):	Sendmail -- aplikacja do obs³ugi poczty elektronicznej
Name:		sendmail
Version:	8.9.2
Release:	3d
Copyright:	distributable (similar to, but not quite BSD)
Group:		Networking/Daemons
Group(pl):	Sieci/Demony
URL:		http://www.sendmail.org
Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
Source1:	site.Linux.m4
Source2:	aliases
Source3:	%{name}.init
Source4:	site.Linux.ppc.m4
Patch0:		%{name}-ip6.patch
Patch1:		%{name}-telnet.patch
Patch2:		%{name}-path.patch
Patch3:		%{name}-rmail.patch
Patch4:		%{name}-pld.mc.patch
Patch5:		%{name}-DoS.patch
Patch6:		%{name}-redirect.patch
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
Prereq:		/sbin/chkconfig
BuildRoot:	/tmp/%{name}-%{version}-root

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
miêdzy komputerami w sieci Internet. Zajmuje siê przekazywaniem poczty
elektronicznej miêdzy bramkami pocztowymi i dostarczaniem przesy³ek na 
konta docelowe. Bardzo dobrze obs³uguje aliasy pocztowe a jego dodatkowym 
atutem jest prosta konfiguracja. Dziêki rozbudowanym mo¿liwo¶ciom 
konfiguracyjnym jest w stanie dostarczaæ przesy³ki za po¶rednictwem 
protoko³ów: SMTP, ESMTP, UUCP, X.400 i innych.

Je¿eli masz zamiar korzystaæ z poczty elektronicznej w sieci Internet
oraz 6bone to zainstaluj ten pakiet.

%package	cf
Summary:	Sendmail configuration files and m4 macros
Summary(pl):	Pliki konfiguracyjne oraz makra m4 dla sendmaila
Group:		Daemons
Group(pl):	Demony
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

ID="`id -u`"
GID="`id -g`"
OPT=$RPM_OPT_FLAGS

cat %{SOURCE1} |sed s/gid/"$GID"/g | sort | sed s/id/"$ID"/g | sort | \
sed s/opt/"$OPT"/g > BuildTools/Site/site.Linux.m4

%build
cd src
./makesendmail
cd ../
make makemap mail.local mailstats praliases rmail 
make smrsh LDOPTS="-s -static" 
(
cd cf/cf
/usr/bin/m4 pld.mc >> ./sendmail.cf
)

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{mail,rc.d/init.d}
install -d $RPM_BUILD_ROOT/usr/{bin,sbin,lib/sendmail-cf,libexec}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}
install -d $RPM_BUILD_ROOT/var/{run,spool/{mqueue,mail}}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/mail/aliases
touch $RPM_BUILD_ROOT/etc/mail/{sendmail.{ct,cw},relay-domains}

for i in aliases access domaintable genericstable mailertable majordomo \
virtusertable
do touch $RPM_BUILD_ROOT/etc/mail/$i{,.db}
done

install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail

make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT OPTIONS=force-install rmail mail.local

for i in hoststat mailq newaliases purgestat
	do ln -sf ../sbin/sendmail  $RPM_BUILD_ROOT/usr/bin/$i
done
ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail

install cf/cf/sendmail.cf $RPM_BUILD_ROOT/etc/mail

cp cf/* $RPM_BUILD_ROOT/usr/lib/sendmail-cf/ -a

cp smrsh/README smrsh/SMRSH.txt

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/{man1/*,man5/*,man8/*}
gzip -9nf README KNOWNBUGS RELEASE_NOTES smrsh/SMRSH.txt

%post
/sbin/chkconfig --add sendmail

%preun
if [ -e /var/lock/sybsys/sendmail ]; then
    /etc/rc.d/init.d/sendmail stop || :
fi

if [ $1 = 0 ]; then
   /sbin/chkconfig --del sendmail
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz KNOWNBUGS.gz RELEASE_NOTES.gz smrsh/SMRSH.txt.gz

%attr(711,root,root) /usr/bin/hoststat
%attr(711,root,root) /usr/bin/mailq
%attr(711,root,root) /usr/bin/newaliases
%attr(711,root,root) /usr/bin/purgestat
%attr(755,root,root) /usr/bin/rmail

%attr(755,root,root) /usr/sbin/mailstats
%attr(755,root,root) /usr/sbin/makemap
%attr(755,root,root) /usr/sbin/praliases

%attr(4711,root,root) /usr/sbin/sendmail

%attr(711,root,root) /usr/lib/sendmail
%attr(755,root,root) /usr/libexec/mail.local
%attr(755,root,root) /usr/libexec/smrsh

%attr(644,root, man) %{_mandir}/man[158]/*

%attr(640,root,root) %config %verify(not size mtime md5) /var/run/sendmail.st

%attr(750,root,mail) %dir /var/spool/mqueue

%attr(700,root,root) %config %verify(not size mtime md5) /etc/rc.d/init.d/*

%files cf
%defattr(644,root,root,755)

/usr/lib/sendmail-cf

%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/mail/*

%changelog
* Thu Feb 10 1999 Micha³ Kuratczyk <kurkens@polbox.com>
  [8.9.2-3d]
- "Obsoletes: smtpdaemon" instead a lot of obsoletes
- simplification in %files
- gzipping instead bzipping

* Fri Jan 22 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
[8.9.2-3d]
- fixed group && owner ELF bineries,
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

* Tue May 05 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscripts

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- added a rmail patch

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- argh!  Fixed some of the db1 handling that had to be added for glibc 2.1

* Fri Oct 24 1997 Donnie Barnes <djb@redhat.com>
- added support for db1 on SPARC

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- added chkconfig support
- various spec file cleanups
- changed group to Networking/Daemons (from Daemons).  Sure, it runs on
  non networked systems, but who really *needs* it then?

* Wed Oct 08 1997 Donnie Barnes <djb@redhat.com>
- made /etc/mail/deny.db a ghost
- removed preun that used to remove deny.db (ghost handles that now)
- NOTE: upgrading from the sendmail packages in 4.8, 4.8.1, and possibly
  4.9 (all Red Hat betas between 4.2 and 5.0) could cause problems.  You
  may need to do a makemap in /etc/mail and a newaliases after upgrading
  from those packages.  Upgrading from 4.2 or prior should be fine.

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- made aliases.db a ghost

* Tue Sep 23 1997 Donnie Barnes <djb@redhat.com>
- fixed preuninstall script to handle aliases.db on upgrades properly

* Mon Sep 15 1997 Donnie Barnes <djb@redhat.com>
- fixed post-install output and changed /var/spool/mqueue to 755

* Thu Sep 11 1997 Donnie Barnes <djb@redhat.com>
- fixed /usr/lib/sendmail-cf paths

* Tue Sep 09 1997 Donnie Barnes <djb@redhat.com>
- updated to 8.8.7
- added some spam filtration
- combined some makefile patches
- added BuildRoot support

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- marked initscript symlinks as missingok
- run newalises after creating /var/spool/mqueue

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc, udated release to -6 (skipped -5!)

* Tue Apr 01 1997 Erik Troan <ewt@redhat.com>
- Added -nsl on the Alpha (for glibc to provide NIS functions).

* Mon Mar 03 1997 Erik Troan <ewt@redhat.com>
- Added nis support.
        
