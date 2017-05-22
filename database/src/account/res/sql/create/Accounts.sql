create table Accounts(
    Id          integer primary key,
    Username    text not null,
    MailAddress text unique not null,
    Password    text not null,
    CreateAt    text
);
