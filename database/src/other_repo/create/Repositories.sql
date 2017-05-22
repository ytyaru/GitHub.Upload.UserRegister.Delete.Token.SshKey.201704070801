create table Repositories(
    Id          integer primary key,
    IdOnGitHub  integer unique not null,
    Owner       text not null,
    Name        text not null,
    Description text,
    Homepage    text,
    CreatedAt   text not null,
    PushedAt    text not null,
    UpdatedAt   text not null,
    CheckedAt   text not null
);
