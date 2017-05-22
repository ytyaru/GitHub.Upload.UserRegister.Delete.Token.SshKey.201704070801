drop table Extensions;
create table Extensions(
    Id                  integer primary key,
    LanguageId          integer not null,
    Extension           text not null,
    IsPrimary           integer default 0 check(IsPrimary = 0 or IsPrimary = 1),
    foreign key(LanguageId) references Languages(Id)
);
