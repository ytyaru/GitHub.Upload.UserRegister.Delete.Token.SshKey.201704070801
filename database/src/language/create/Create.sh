#!/bin/bash
#HatenaId = $1
#BlogId = $2
sqlite=sqlite3
#PATH_DB=${THIS_DIR}/GitHub.Languages.sqlite3
PATH_DB=$1
THIS_DIR=`dirname $0`
# Create Table
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Languages.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Aliases.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Extensions.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Interpreters.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/FileNames.sql
# Check
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Check.sql

