
# Very much like site.Linux.m4, but:
#  Uses $(RPM_OPT_FLAGS) for OPTIMIZE
#  Uses the default cc
#  SBINGRP already defaults to mail
#  Adds -lnsl to LIBS for NIS support

define(`confMAPDEF', `-DMAP_REGEX -DNIS')
APPENDDEF(`confLIBS', `-lnsl')
define(`confSTDIR', `/var/run')
define(`confHFDIR',`/etc/mail')
define(`confDEPEND_TYPE', `CC-M')
define(`confMANROOT', `/usr/share/man/man')
define(`confOPTIMIZE', `$(RPM_OPT_FLAGS)')
define(`confLDOPTS', `-s')

