create table SshConfigures(
    Id                  integer primary key,
    AccountId           integer unique not null,
    HostName            text, -- github.com.{username}
    PrivateKeyFilePath  text, -- ~/.ssh/rsa_4096_{username}
    PublicKeyFilePath   text, -- ~/.ssh/rsa_4096_{username}.pub
    Type                text, -- check(Type='rsa' or Type='dsa' or Type='ecdsa' or Type='ed25519') 新しい暗号方式ができるかもしれない
    Bits                integer, -- 2048, 4096, ...
    Passphrase          text,
    foreign key(AccountId) references Accounts(Id)
);
