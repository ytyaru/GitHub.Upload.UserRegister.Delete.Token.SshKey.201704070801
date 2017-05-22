.headers on
.tables
select * from sqlite_master where type = 'table';
select * from Repositories;
select * from Counts;
select * from Languages;
select * from Licenses;
vacuum;
