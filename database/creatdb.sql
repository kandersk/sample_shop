-- CREATE DATABASE IF NOT EXSISTS 'store';
-- USE 'store';

CREATE TABLE IF NOT EXISTS store(
  item int not null primary key,
  price  numeric(9,2) not null,
  title text not null,
  imageurl text,
  qty int not null,
  descrip text,
  shp numeric(9,2) not null
);
