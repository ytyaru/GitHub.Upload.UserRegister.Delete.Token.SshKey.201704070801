drop table Licenses;
create table Licenses(
    Id                  integer primary key,
    Key                 text unique not null,
    Name                text not null,
    SpdxId              text,
    Url                 text,
    HtmlUrl             text,
    Featured            integer default 0 check(Featured = 0 or Featured = 1),
    Description         text,
    Implementation      text,
    Permissions         text,
    Conditions          text,
    Limitations         text,
    Body                text
); 
