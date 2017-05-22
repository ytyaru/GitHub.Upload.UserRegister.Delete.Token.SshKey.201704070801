create table Counts(
    Id              integer primary key,
    RepositoryId    integer not null,
    Forks           integer not null,
    Stargazers      integer not null,
    Watchers        integer not null,
    Issues          integer not null,
    foreign key(RepositoryId) references Repositories(Id)
);
