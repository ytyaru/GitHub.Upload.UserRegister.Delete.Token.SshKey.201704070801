create table Languages(
    Id              integer primary key,
    RepositoryId    integer not null,
    Language        text not null,
    Size            integer not null,
    foreign key(RepositoryId) references Repositories(Id)
);
