.headers on
.tables
select * from sqlite_master where type = 'table';
select * from Languages;
select * from Aliases;
select * from Extensions;
select * from Interpreters;
select * from FileNames;
select * from Languages left join Aliases on Languages.Id = Aliases.LanguageId;
select * from Languages left join Extensions on Languages.Id = Extensions.LanguageId;
select * from Languages left join Interpreters on Languages.Id = Interpreters.LanguageId;
select * from Languages left join FileNames on Languages.Id = FileNames.LanguageId;
vacuum;
