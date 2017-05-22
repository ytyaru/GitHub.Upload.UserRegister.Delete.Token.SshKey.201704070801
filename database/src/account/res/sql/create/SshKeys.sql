create table SshKeys(
    Id              integer primary key,
    AccountId       integer unique not null,
    IdOnGitHub      integer not null,
    Title           text,
    Key             text,
    Verified        integer check(Verified=0 or Verified=1),
    ReadOnly        integer check(ReadOnly=0 or ReadOnly=1),
    CreatedAt       text,
    foreign key(AccountId) references Accounts(Id)
);
