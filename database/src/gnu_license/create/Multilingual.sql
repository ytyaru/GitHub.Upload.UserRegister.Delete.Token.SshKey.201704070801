drop table Multilingual;
create table Multilingual(
    Id              integer primary key,
    LicenseId       integer,
    LanguageCode    text,
    Name            text unique not null,
    Description     text,
    foreign key(LicenseId) references Licenses(Id)
);
