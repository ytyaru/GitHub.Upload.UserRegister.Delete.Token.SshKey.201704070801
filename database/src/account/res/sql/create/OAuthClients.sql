create table AccessTokens(
    Id              integer primary key,
    AccountId       integer not null,
    IdOnGitHub      integer unique not null,
    Note            text,
    NoteUrl         text,
    ClientId        text,
    ClientSecret    text,
    Fingerprint     text,
    AccessToken     text not null,
    HashedToken     text,
    Scopes          text,
    AppName         text,
    AppUrl          text,
    CreatedAt       text,
    UpdatedAt       text,
    foreign key(AccountId) references Accounts(Id)
);
