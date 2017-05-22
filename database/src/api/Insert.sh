PATH_DB=$1
PATH_THIS=$(cd $(dirname $0) && pwd)
echo ${PATH_THIS}
PATH_SCRIPT_SUB=res/sql/insert
#PATH_SCRIPT="${PATH_SCRIPT}/res/sql/insert"
echo ${PATH_SCRIPT_SUB}
PATH_SCRIPT=${PATH_THIS}/${PATH_SCRIPT_SUB}
echo ${PATH_SCRIPT}
PATH_SCRIPT=/tmp/GitHub.Database.Create.Auto.Add.Accounts.2017032221454/src/account/res/sql/insert
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/Accounts.sql
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/TwoFactors.sql
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/AccessTokens.sql
