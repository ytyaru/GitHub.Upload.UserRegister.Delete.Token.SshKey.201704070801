#!/bin/bash
#HatenaId = $1
#BlogId = $2
sqlite=sqlite3
#PATH_DB=${THIS_DIR}/GNU.Licenses.sqlite3
PATH_DB=$1
THIS_DIR=`dirname $0`
# Create Table
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Colors.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Licenses.sql
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Multilingual.sql
# Insert
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Colors.Insert.sql

# tsvの相対パスの基準がpython実行パスになっているため参照できない。
#.mode tabs
#.import ./Colors.tsv Colors

# Check
${sqlite} "${PATH_DB}" < ${THIS_DIR}/Check.sql

