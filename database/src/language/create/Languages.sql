drop table Languages;
create table Languages(
    Id                      integer primary key,
    LanguageId              text unique not null,
    Key                     text unique not null,
    Type                    text not null,
    Color                   text,
    TextMateScope           text default NULL,
    AceMode                 text default 'text',
    CodeMirrorMode          text,
    CodeMirrorMimeType      text,
    GroupName               text,
    Wrap                    integer default 0 check(Wrap = 0 or Wrap = 1),
    Searchable              integer default 1 check(Searchable = 0 or Searchable = 1)
);
