.headers on
.tables
select * from sqlite_master where type = 'table';
select * from Colors;
select * from Licenses;
select * from Multilingual;
select Licenses.Id,Licenses.HeaderId,Colors.Key from Licenses left join Colors on Licenses.ColorId = Colors.Id;
select Licenses.Id,Licenses.HeaderId,Multilingual.LanguageCode,Multilingual.Name from Licenses left join Multilingual on Licenses.Id = Multilingual.LicenseId;
vacuum;
