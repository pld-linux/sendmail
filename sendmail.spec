Summary:	A widely used Mail Transport Agent (MTA)
Summary(pl):	Sendmail -- aplikacja do obs³ugi poczty elektronicznej
Name:		sendmail
Version:	8.10.1
Release:	5
License:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Provides:	smtpdaemon
Source0:	ftp://ftp.cs.berkeley.edu/ucb/sendmail/%{name}.%{version}.tar.gz
Source1:	sendmail.init
Source2:	http://www.informatik.uni-kiel.de/%7Eca/email/rules/check.tar
Source3:	aliases
Source4:	sendmail.sysconfig
Source5:	sendmail-8.9.3-etc-mail-Makefile
Source6:	sendmail.mc
Source7:	sendmail-config.m4
Patch0:		sendmail-8.10.0-redhat.patch
Patch1:		sendmail-8.10.0-makemapman.patch
Patch2:		sendmail-8.10.0-smrsh-paths.patch
Patch3:		sendmail-8.8.7-rmail.patch
Buildrequires:	cyrus-sasl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		/sbin/chkconfig
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
Obsoletes:	zmail
Obsoletes:	qmail
Obsoletes:	smail
Obsoletes:	sendmail-cf

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

%description -l pl
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

# XXX REVERTING[B
#tar xf $RPM_SOURCE_DIR/check.tar -C cf
#chown root.root cf/hack/* cf/README.check

sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/redhat.mc

install %{SOURCE7} config.m4

%build
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DUSE_VENDOR_CF_PATH=1"

cd sendmail
sh Build -f ../config.m4
cd ..

cd mailstats
sh Build -f ../config.m4
cd ..

cd rmail
sh Build -f ../config.m4
cd ..

cd makemap
sh Build -f ../config.m4
cd ..

cd praliases
sh Build -f ../config.m4
cd ..

cd smrsh
sh Build -f ../config.m4
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

%{__make} DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/sendmail
%{__make} DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/mailstats
%{__make} DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/praliases
%{__make} DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 force-install -C $OBJDIR/rmail
%{__make} DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
 install -C $OBJDIR/makemap
ln -sf ../sbin/makemap $RPM_BUILD_ROOT%{_bindir}/makemap
%{__make} DESTDIR=$RPM_BUILD_ROOT SBINOWN=`id -nu` UBINOWN=`id -nu` SBINGRP=`id -ng` UBINGRP=`id -ng` MANOWN=`id -nu` MANGRP=`id -ng` \
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
install %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/sendmail

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
%{_libdir}/sendmail-cf

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

%files doc
%defattr(644,root,root,755)
%{_prefix}/doc/sendmail
