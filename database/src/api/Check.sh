PATH_DB=$1
echo ${PATH_DB}
PATH_THIS=$(cd $(dirname $0) && pwd)
echo ${PATH_THIS}
PATH_SUB=res/sql/check
echo ${PATH_SUB}
PATH_SCRIPT=${PATH_THIS}${PATH_SUB}
echo ${PATH_SCRIPT}
echo ${PATH_SCRIPT}/check.sql
echo "${PATH_SCRIPT}/check.sql"
sqlite3 "${PATH_DB}" < ${PATH_SCRIPT}/check.sql

# なぜか文字列結合がおかしくなる。意図したパスが作成できない。bashのバグかもしれない。原因不明。
# 実行パスと参照ファイルパスが異なる階層にあるときに生じるのかもしれない。
#
# `/tmp/GitHub.Database.Create.Auto.Add.Accounts.2017032221454/src/account/res/sql/check`というパスにしたいのに、
# `res/sql/checkatabase.Create.Auto.Add.Accounts.2017032221454/src/account/`という文字列になってしまう。
# 前方の文字を上書きしたような結果になっている。謎。
# ----------------------------------------------------
#/tmp/GitHub.Database.Create.Auto.Add.Accounts.2017032221454/res/db/GitHub.Accounts.sqlite3
#/tmp/GitHub.Database.Create.Auto.Add.Accounts.2017032221454/src/account
#res/sql/check
#res/sql/checkatabase.Create.Auto.Add.Accounts.2017032221454/src/account
#/check.sqleckatabase.Create.Auto.Add.Accounts.2017032221454/src/account
#/check.sqleckatabase.Create.Auto.Add.Accounts.2017032221454/src/account
#/tmp/GitHub.Database.Create.Auto.Add.Accounts.2017032221454/src/account/Check.sh: 行 11: /tmp/#GitHub.Database.Create.Auto.Add.Accounts.201703222: そのようなファイルやディレクトリはありません
# ----------------------------------------------------

