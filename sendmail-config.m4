define(`confMAPDEF', `-DNEWDB -DNIS')
define(`confENVDEF', `-DXDEBUG=0 -DMILTER')
define(`confLIBS', `-lnsl')
define(`confLIBSEARCH', `db resolv')
define(`confMANOWN', `root')
define(`confMANGRP', `root')
define(`confMANMODE', `644')
define(`confMAN1SRC', `1')
define(`confMAN5SRC', `5')
define(`confMAN8SRC', `8')
define(`confSHAREDLIB_EXT', `.so')
APPENDDEF(`confENVDEF', -DSASL)
APPENDDEF(`conf_sendmail_LIBS', -lsasl)
APPENDDEF(`confINCDIRS', `-I/usr/include/sasl')
