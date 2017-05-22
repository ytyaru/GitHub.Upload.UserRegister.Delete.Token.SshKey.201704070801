create table Users(
    Id              integer primary key,
    AccountId       integer unique not null,
    Blog            text,
    Company         text,
    Location        text,
    Hireable        integer check(Hireable=0 or Hireable=1),
    Bio             text,
    foreign key(AccountId) references Accounts(Id)
);
