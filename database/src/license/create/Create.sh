#!/bin/bash
#HatenaId = $1
#BlogId = $2
sqlite=sqlite3
#PATH_DB=./GitHub.Licenses.sqlite3
PATH_DB=$1
THIS_DIR=`dirname $0`
# Create Table
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Licenses.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Gnu.sql
# Insert
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Licenses.Insert.sql
#${sqlite} "${PATH_DB}" < ${THIS_DIR}/Gnu.Insert.sql
# Check
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Check.sql

