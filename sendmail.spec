Summary:	A widely used Mail Transport Agent (MTA).
Summary(pl):	Sendmail -- aplikacja do obs³ugi poczty elektronicznej
Name:		sendmail
Version:	8.10.1
Release:	1
License:	BSD
Group:		System Environment/Daemons
######		Unknown group!
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

install -d $RPM_BUILD_ROOT%{_sysconfdir}/mail


install cf/cf/redhat.cf $RPM_BUILD_ROOT%{_sysconfdir}/sendmail.cf
sed -e 's|@@PATH@@|%{_libdir}/sendmail-cf|' < %{SOURCE6} > $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.mc
echo "# local-host-names - include all aliases for your machine here." > $RPM_BUILD_ROOT%{_sysconfdir}/mail/local-host-names

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail
install -d -m755 $RPM_BUILD_ROOT/var/spool/mqueue

# dangling symlinks
for f in hoststat mailq newaliases purgestat
  do
    ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/${f}
  done
install -d $RPM_BUILD_ROOT%{_sysconfdir}/smrsh

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
for map in virtusertable access domaintable mailertable
  do
touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}
makemap hash $RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}.db < $RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}
  done
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/aliases
makemap hash $RPM_BUILD_ROOT%{_sysconfdir}/aliases.db < %{SOURCE3}

install %SOURCE4 $RPM_BUILD_ROOT/etc/sysconfig/sendmail
install -m755 %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail

install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/mail/Makefile

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
%config %{_sysconfdir}/sendmail.cf
%attr(0644,root,root) %config %{_sysconfdir}/mail/sendmail.mc
%config(noreplace) %{_sysconfdir}/mail/local-host-names
%config(noreplace) %{_sysconfdir}/aliases
%attr(0644,root,mail) %ghost %{_sysconfdir}/aliases.db
%attr(0755,root,mail) %dir	/var/spool/mqueue
%dir %{_sysconfdir}/smrsh
%dir %{_sysconfdir}/mail

%config %{_sysconfdir}/mail/Makefile
%attr(0644,root,root) %ghost %{_sysconfdir}/mail/virtusertable.db
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/virtusertable

%attr(0644,root,root) %ghost %{_sysconfdir}/mail/access.db
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/access

%attr(0644,root,root) %ghost %{_sysconfdir}/mail/domaintable.db
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/domaintable

%attr(0644,root,root) %ghost %{_sysconfdir}/mail/mailertable.db
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/mailertable

%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/helpfile

%config /etc/sysconfig/sendmail

%config /etc/rc.d/init.d/sendmail

%files cf
%defattr(644,root,root,755)
%{_libdir}/sendmail-cf

%files doc
%defattr(644,root,root,755)
%{_prefix}/doc/sendmail
