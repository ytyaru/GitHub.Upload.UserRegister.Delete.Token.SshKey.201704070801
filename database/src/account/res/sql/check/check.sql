.tables
.headers on
select * from sqlite_master where type = 'table';
select * from Accounts;
select * from TwoFactors;
select * from AccessTokens;
select * from AccessTokens where (',' || Scopes || ',') LIKE '%,repo,%';
