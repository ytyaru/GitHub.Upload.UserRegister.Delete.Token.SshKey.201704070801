#!/bin/bash
#HatenaId = $1
#BlogId = $2
sqlite=sqlite3
#GITHUB_USER_NAME="__other__"
#PATH_DB=${THIS_DIR}/GitHub.Repositories.${GITHUB_USER_NAME}.sqlite3
PATH_DB=$1
THIS_DIR=`dirname $0`
# Create Table
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Repositories.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Counts.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Languages.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Licenses.sql
# Check
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Check.sql

