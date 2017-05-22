drop table Interpreters;
create table Interpreters(
    Id                  integer primary key,
    LanguageId          integer not null,
    Interpreter         text not null,
    foreign key(LanguageId) references Languages(Id)
);
