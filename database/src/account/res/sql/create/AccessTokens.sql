create table AccessTokens(
    Id              integer primary key,
    AccountId       integer not null,
    IdOnGitHub      integer unique not null,
    Note            text,
    AccessToken     text not null,
    Scopes          text,
    SshKeyId        integer, -- GitHubAPIでSSH鍵を設定した場合、その鍵idを保存する
    foreign key(AccountId) references Accounts(Id),
    foreign key(SshKeyId) references SshKeys(IdOnGitHub)
);
