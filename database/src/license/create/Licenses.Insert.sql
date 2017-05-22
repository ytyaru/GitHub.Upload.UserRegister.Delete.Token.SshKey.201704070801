-- https://developer.github.com/v3/licenses/#get-a-repositorys-license
-- ライセンスが設定されていない場合はNULL。
-- "license":null
-- ライセンスが規定以外の場合は`other`。
-- "license":{"key":"other","name":"Other","spdx_id":null,"url":null,"featured":false}
insert into Licenses (Id,Key,Name,Featured) values (0,'other','Other',0);

