.headers on
.tables
select * from sqlite_master where type='table';
select * from Licenses;
select * from Gnu;
select Licenses.Id,Licenses.Name,Gnu.GnuLicenseId from Licenses inner join Gnu on Licenses.Id=Gnu.LicenseId;

.database
ATTACH "GNU.Licenses.sqlite3" AS GNU;
.database
select main.Licenses.Id,main.Licenses.Key,GNU.Licenses.HeaderId,main.Licenses.Name
 from main.Licenses
  inner join main.Gnu on main.Licenses.Id=main.Gnu.LicenseId
  inner join GNU.Licenses on main.Gnu.LicenseId=GNU.Licenses.Id
;

select main.Licenses.Id,main.Licenses.Key,GNU.Licenses.HeaderId,main.Licenses.Name,GNU.Multilingual.Name
 from main.Licenses
  inner join main.Gnu on main.Licenses.Id=main.Gnu.LicenseId
  inner join GNU.Licenses on main.Gnu.GnuLicenseId=GNU.Licenses.Id
  inner join GNU.Multilingual on GNU.Licenses.Id=GNU.Multilingual.LicenseId
 where GNU.Multilingual.LanguageCode='ja'
;

vacuum;
