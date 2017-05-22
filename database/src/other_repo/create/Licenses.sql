drop table Licenses;
create table Licenses(
    Id                  integer primary key,
    RepositoryId        integer not null,
    LicenseId           integer,
    foreign key(RepositoryId) references Repositories(Id)
); 
