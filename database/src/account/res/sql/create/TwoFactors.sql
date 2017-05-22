create table TwoFactors(
    Id                          integer primary key,
    AccountId                   integer not null,
    Secret                      text not null,
    RecoveryCodes               text,
    RecoveryCodesExpirationDate text,
    foreign key(AccountId) references Accounts(Id)
);
