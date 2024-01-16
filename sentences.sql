drop database if exists body_fitness;


create database if not exists body_fitness; 

use body_fitness;

create table if not exists users(
    id int not null primary key auto_increment,
    nombre varchar(50) not null,
    apellido varchar(50) not null,
    edad int not null,
    cedula varchar(20) not null unique,
    correo varchar(50) not null unique,
    celular varchar(20) not null unique,
    direccion varchar(100),
    created_at datetime default current_timestamp
);

create table if not exists plans(
    id int not null primary key auto_increment,
    plan_name varchar(50) not null
);


insert into plans(plan_name) values('1 Mes');
insert into plans(plan_name) values('2 Meses');
insert into plans(plan_name) values('3 Meses');
insert into plans(plan_name) values('6 Meses');
insert into plans(plan_name) values('10 dias');
insert into plans(plan_name) values('12 dias');
insert into plans(plan_name) values('15 dias');
insert into plans(plan_name) values('otro');
