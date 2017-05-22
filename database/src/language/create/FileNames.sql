drop table FileNames;
create table FileNames(
    Id                  integer primary key,
    LanguageId          integer not null,
    FileName            text not null,
    foreign key(LanguageId) references Languages(Id)
);
