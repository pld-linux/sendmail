divert(-1)
dnl This is the macro config file used to generate the /etc/mail/sendmail.cf
dnl file. If you modify thei file you will have to regenerate the
dnl /etc/mail/sendmail.cf by running this macro config through the m4
dnl preprocessor:
dnl
dnl        m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf
dnl
dnl You will need to have the sendmail-cf package installed for this to
dnl work.
include(`@@PATH@@/m4/cf.m4')
define(`confDEF_USER_ID',``8:12'')
OSTYPE(`linux')
undefine(`UUCP_RELAY')
undefine(`BITNET_RELAY')
define(`confTO_CONNECT', `1m')
define(`confTRY_NULL_MX_LIST',true)
define(`confDONT_PROBE_INTERFACES',true)
define(`PROCMAIL_MAILER_PATH',`/usr/bin/procmail')
define('ALIAS_FILE','/etc/mail/aliases')
define(`confPRIVACY_FLAGS',`authwarnings,novrfy,noexpn,noetrn')
TRUST_AUTH_MECH(`LOGIN PLAIN GSSAPI KERBEROS_V4 DIGEST-MD5 CRAM-MD5')
define(`confAUTH_MECHANISMS',`LOGIN PLAIN GSSAPI KERBEROS_V4 DIGEST-MD5 CRAM-MD5')
dnl	Define maximum message size here if you want:
dnl	define(`confMAX_MESSAGE_SIZE', `10000000')
FEATURE(`smrsh',`/usr/sbin/smrsh')
FEATURE(`mailertable',`hash -o /etc/mail/mailertable')
FEATURE(`virtusertable',`hash -o /etc/mail/virtusertable')
FEATURE(`genericstable',`hash -o /etc/mail/genericstable')
FEATURE(redirect)
dnl tun off Message Submission Agent (MSA)
dnl FEATURE(`no_default_msa')
FEATURE(always_add_domain)
FEATURE(use_cw_file)
FEATURE(local_procmail)
FEATURE(`access_db')
FEATURE(`blacklist_recipients')

dnl define(`confCACERT_PATH',`/usr/share/ssl')
dnl define(`confCACERT',`/usr/share/ssl/ca-bundle.crt')
dnl define(`confSERVER_CERT',`/var/lib/openssl/certs/sendmail.pem')
dnl define(`confSERVER_KEY',`/var/lib/openssl/certs/sendmail.pem')
dnl DAEMON_OPTIONS(`Port=smtp, Name=MTA')dnl
dnl DAEMON_OPTIONS(`Family=inet, Port=smtps, Name=MTA-SSL, M=s')dnl

dnl define(`MILTER', 1)
dnl INPUT_MAIL_FILTER(`milter-amavis', `S=local:/var/run/clamav/clamav-milter.sock, F=T, T=S:10m; R:10m;E:10m')

dnl We strongly recommend to comment this one out if you want to protect
dnl yourself from spam. However, the laptop and users on computers that do
dnl not hav 24x7 DNS do need this.
dnl FEATURE(`accept_unresolvable_domains')
dnl FEATURE(`relay_based_on_MX')
MAILER(smtp)
MAILER(procmail)
