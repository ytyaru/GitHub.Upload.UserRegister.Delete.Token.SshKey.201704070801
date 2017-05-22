PATH_DB=$1
PATH_SCRIPT=$(cd $(dirname $0) && pwd)
PATH_SCRIPT=${PATH_SCRIPT}/res/sql/create
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/Accounts.sql
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/TwoFactors.sql
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/AccessTokens.sql
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/SshKeys.sql

