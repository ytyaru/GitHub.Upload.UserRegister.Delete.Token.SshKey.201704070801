drop table Aliases;
create table Aliases(
    Id                  integer primary key,
    LanguageId          integer not null,
    Aliase              text not null,
    foreign key(LanguageId) references Languages(Id)
);
