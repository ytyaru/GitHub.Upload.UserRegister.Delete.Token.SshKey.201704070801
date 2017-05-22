# $1=GitHub.Accounts.sqlite3のパス
PATH_THIS=`dirname $0`
echo ${PATH_THIS}
echo "---------CreateTable.sh"
bash ${PATH_THIS}/CreateTable.sh "$1"
echo "---------Insert.sh"
#bash ${PATH_THIS}/Insert.sh $1
echo "---------Check.sh"
bash ${PATH_THIS}/Check.sh "$1"
