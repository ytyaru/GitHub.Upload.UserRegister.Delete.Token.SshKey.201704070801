drop table Licenses;
create table Licenses(
    Id          integer primary key,
    HeaderId    text,
    ColorId     integer,
    Target      text check(Target='software' or Target='document' or Target='other' or Target='other.font' or Target='other.opinion' or Target='other.design'),
    Url         text,
    foreign key(ColorId) references Colors(Id)
);
