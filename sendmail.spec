Summary:	A widely used Mail Transport Agent (MTA).
Summary(pl):	Sendmail -- aplikacja do obs³ugi poczty elektronicznej
Name:		sendmail
Version:	8.10.1
Release:	1
License:	BSD
Group:		System Environment/Daemons
Group(pl):	Sieciowe/Serwery
Provides:	smtpdaemon
Source0:	ftp://ftp.cs.berkeley.edu/ucb/sendmail/%{name}.%{version}.tar.gz
Source1:	sendmail.init
Source2:	http://www.informatik.uni-kiel.de/%7Eca/email/rules/check.tar
Source3:	aliases
Source4:	sendmail.sysconfig
Source5:	sendmail-8.9.3-etc-mail-Makefile
Source6:	sendmail-redhat.mc
Patch0:		sendmail-8.10.0-redhat.patch
Patch1:		sendmail-8.10.0-makemapman.patch
Patch2:		sendmail-8.10.0-smrsh-paths.patch
Patch3:		sendmail-8.8.7-rmail.patch
#Patch4:	sendmail-8.10.0-aliasesDoS.patch
#Patch5:	sendmail-8.10.0-movefiles.patch
#Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		/sbin/chkconfig
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
Obsoletes:	zmail
Obsoletes:	qmail
Obsoletes:	smail


%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your e-mail. Sendmail is a
behind-the-scenes program which actually moves your e-mail over
networks or the Internet to where you want it to go.

If you ever need to reconfigure Sendmail, you'll also need to have the
sendmail.cf package installed. If you need documentation on Sendmail,
you can install the sendmail-doc package.


%description -l pl
Sendmail jest programem umo¿liwiaj±cym wymianê poczty elektronicznej
miêdzy komputerami w sieci internet. Zajmuje siê przekazywaniem poczty
elektronicznej miêdzy bramkami pocztowymi i dostarczaniem przesy³ek na
konta docelowe. Bardzo dobrze obs³uguje aliasy pocztowe a jego
dodatkowym atutem jest prosta konfiguracja. Dziêki rozbudowanym
mo¿liwo¶ciom konfiguracyjnym jest w stanie dostarczaæ przesy³ki za
po¶rednictwem protoko³ów: SMTP, ESMTP, UUCP, X.400 i innych.

Je¿eli masz zamiar korzystaæ z poczty elektronicznej w sieci internet
oraz 6bone to zainstaluj ten pakiet

%package doc
Summary:	Documentation about the Sendmail Mail Transport Agent program.
Summary(pl):	Dokumentacja do Sendmaila.
Group(pl):	Serwery
Group:		Documentation
######		/home/lukasz/rpm/groups: no such file

%description doc
The sendmail-doc package contains documentation about the Sendmail
Mail Transport Agent (MTA) program, including release notes, the
Sendmail FAQ and a few papers written about Sendmail. The papers are
provided in PostScript(TM) and troff formats.

Install the sendmail-doc package if you need documentation about
Sendmail.

%description -l pl
Ten pakiet zawiera dokumentacjê do programu Sendmail Mail Transport
Agent (MTA). Dokumentacja zwawiera informacje o zmianach w bie¿±cej
wersji, FAQ - najczêsciej zadawane pytania. Dokumentacja dostêpna jest
w formacie PostScript(TM) oraz troff. Je¿eli potrzebujesz dokumntacji
- zainstaluj ten pakiet.

%package cf
Summary:	The files needed to reconfigure Sendmail.
Summary(pl):	Pliki konfiguracyjne oraz makra m4 dla sendmaila
Group:		System Environment/Daemons
######		/home/lukasz/rpm/groups: no such file
Group(pl):	Serwery
Requires:	%{name} = %{version}


%description cf
This package includes the configuration files which you'd need to
generate the sendmail.cf file distributed with the sendmail package.
You'll need the sendmail-cf package if you ever need to reconfigure
and rebuild your sendmail.cf file. For example, the default
sendmail.cf file is not configured for UUCP. If someday you needed to
send and receive mail over UUCP, you'd need to install the sendmail-cf
package to help you reconfigure Sendmail.

Install the sendmail-cf package if you need to reconfigure your
sendmail.cf file.

%description -l pl cf
Pakiet ten zawiera wszystkie pliki konfiguracyjne u¿ywane do gene-
rowania pliku sendmail.cf, znajduj±cego siê w pakiecie bazowym.
Bêdziesz potrzebowa³ tego pakietu je¿eli chcesz zmieniæ i przebudowaæ
konfiguracjê swojego sendmaila. Na przyk³ad, standardowy plik konfigu-
racyjny nie zawiera wspomagania dla poczty po UUCP. Je¿eli chcesz wy-
sy³aæ i odbieraæ pocztê po UUCP bêdziesz potrzebowa³ tego pakietu.

%prep
%setup -q
%patch0 -p1 -b .redhat
%patch1 -p1 -b .makemapman
%patch2 -p1 -b .smrsh
%patch3 -p1 -b .rmail
#%patch4 -p1 -b .aliases
#%patch5 -p1 -b .movestuff

# XXX REVERTING
#tar xf $RPM_SOURCE_DIR/check.tar -C cf
#chown root.root cf/hack/* cf/README.check


sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/redhat.mc

%build
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DUSE_VENDOR_CF_PATH=1"

cd sendmail
sh Build -f ../redhat.config.m4
cd ..

cd mailstats
sh Build -f ../redhat.config.m4
cd ..

cd rmail
sh Build -f ../redhat.config.m4
cd ..

cd makemap
sh Build -f ../redhat.config.m4
cd ..

cd praliases
sh Build -f ../redhat.config.m4
cd ..

cd smrsh
sh Build -f ../redhat.config.m4
cd ..

cd cf/cf
m4 redhat.mc > redhat.cf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT
install -d etc/rc.d/init.d etc/rc.d/rc{0,1,2,3,4,5,6}.d etc/sysconfig
install -d usr/bin usr/lib usr/man/man{1,5,8} usr/sbin var/log var/spool usr/lib/sendmail-cf
cd -

OBJDIR=obj.$(uname -s).$(uname -r).$(arch)

make DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/sendmail
make DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/mailstats
make DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/praliases
make DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 force-install -C $OBJDIR/rmail
make DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/makemap
ln -sf ../sbin/makemap $RPM_BUILD_ROOT%{_bindir}/makemap
make DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/smrsh

# install docs by hand
install -d $RPM_BUILD_ROOT%{_prefix}/doc/sendmail
cp -ar FAQ LICENSE KNOWNBUGS README RELEASE_NOTES doc $RPM_BUILD_ROOT%{_prefix}/doc/sendmail
cp smrsh/README $RPM_BUILD_ROOT%{_prefix}/doc/sendmail/README.smrsh
cp cf/README $RPM_BUILD_ROOT%{_prefix}/doc/sendmail/README.cf

# install the cf files
cd cf
cp -ar * $RPM_BUILD_ROOT%{_libdir}/sendmail-cf
cd -

install -d $RPM_BUILD_ROOT/etc/mail


install cf/cf/redhat.cf $RPM_BUILD_ROOT/etc/sendmail.cf
sed -e 's|@@PATH@@|%{_libdir}/sendmail-cf|' < %{SOURCE6} > $RPM_BUILD_ROOT/etc/mail/sendmail.mc
echo "# local-host-names - include all aliases for your machine here." > $RPM_BUILD_ROOT/etc/mail/local-host-names

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail
install -d -m755 $RPM_BUILD_ROOT/var/spool/mqueue

# dangling symlinks
for f in hoststat mailq newaliases purgestat
  do
    ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/${f}
  done
install -d $RPM_BUILD_ROOT/etc/smrsh

cat <<EOF > $RPM_BUILD_ROOT/etc/mail/access
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
for map in virtusertable access domaintable mailertable
  do
    touch $RPM_BUILD_ROOT/etc/mail/${map}
    makemap hash $RPM_BUILD_ROOT/etc/mail/${map}.db < $RPM_BUILD_ROOT/etc/mail/${map}
  done
install %{SOURCE3} $RPM_BUILD_ROOT/etc/aliases
makemap hash $RPM_BUILD_ROOT/etc/aliases.db < %{SOURCE3}

install %SOURCE4 $RPM_BUILD_ROOT/etc/sysconfig/sendmail
install -m755 %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail

install %{SOURCE5} $RPM_BUILD_ROOT/etc/mail/Makefile

chmod u+w $RPM_BUILD_ROOT%{_sbindir}/{mailstats,praliases}
chmod u+w $RPM_BUILD_ROOT%{_bindir}/rmail

strip $RPM_BUILD_ROOT%{_sbindir}/{mailstats,praliases,sendmail}
strip $RPM_BUILD_ROOT%{_bindir}/rmail

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

%preun
if [ $1 = 0 ]; then
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
%config				/etc/sendmail.cf
%attr(0644,root,root) %config	/etc/mail/sendmail.mc
%config(noreplace)		/etc/mail/local-host-names
%config(noreplace)		/etc/aliases
%attr(0644,root,mail) %ghost	/etc/aliases.db
%attr(0755,root,mail) %dir	/var/spool/mqueue
%dir /etc/smrsh
%dir /etc/mail

%config /etc/mail/Makefile
%attr(0644,root,root) %ghost			/etc/mail/virtusertable.db
%attr(0644,root,root) %config(noreplace)	/etc/mail/virtusertable

%attr(0644,root,root) %ghost			/etc/mail/access.db
%attr(0644,root,root) %config(noreplace)	/etc/mail/access

%attr(0644,root,root) %ghost			/etc/mail/domaintable.db
%attr(0644,root,root) %config(noreplace)	/etc/mail/domaintable

%attr(0644,root,root) %ghost			/etc/mail/mailertable.db
%attr(0644,root,root) %config(noreplace)	/etc/mail/mailertable

%attr(0644,root,root) %config(noreplace)	/etc/mail/helpfile

%config /etc/sysconfig/sendmail

%config /etc/rc.d/init.d/sendmail

%files cf
%defattr(644,root,root,755)
%{_libdir}/sendmail-cf

%files doc
%defattr(644,root,root,755)
%{_prefix}/doc/sendmail

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- fixed virtusertable patch
- make smrsh look into /etc/smrsh

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- remove noreplace attr from sednmail.cf.

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- provide a more sane /etc/mail/access default config file
- use makemap to initializa the empty databases, not touch
- added a small, but helpful /etc/mail/Makefile

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- correxct dangling symlinks.
- check for map file existence in %post.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 3)
* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- improved 8.9.3 config from Mike McHenry <mmchen@minn.net>

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- version 8.9.3

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- use the libdb1 stuff correctly

* Mon Sep 21 1998 Michael K. Johnson <johnsonm@redhat.com>
- Allow empty QUEUE in /etc/sysconfig/sendmail for those who
  want to run sendmail in daemon mode without processing the
  queue regularly.

* Thu Sep 17 1998 Michael K. Johnson <johnsonm@redhat.com>
- /etc/sysconfig/sendmail

* Fri Aug 28 1998 Jeff Johnson <jbj@redhat.com>
- recompile statically linked binary for 5.2/sparc

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
