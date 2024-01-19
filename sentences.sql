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
    duration int, 
    plan_name varchar(50) not null
);

create table if not exists user_plans(
    id int not null primary key auto_increment,
    user_id int not null,
    plan_id int not null,
    start_plan_date date not null,
    end_plan_date date not null,
    frequency int, 
    payment_day date,
    payment_status enum('pendiente', 'pagado') default 'pendiente',
    plan_status enum('activo', 'inactivo') default 'activo', 
    foreign key (user_id) references users(id) on delete cascade,
    foreign key (plan_id) references plans(id) on delete cascade
);



insert into plans(plan_name, duration) values('1 Mes', 1);
insert into plans(plan_name, duration) values('2 Meses', 2);
insert into plans(plan_name, duration) values('3 Meses', 3);
insert into plans(plan_name, duration) values('6 Meses', 6);
insert into plans(plan_name, duration) values('10 dias', 15);
insert into plans(plan_name, duration) values('12 dias', 20);
insert into plans(plan_name, duration) values('15 dias', 30);
insert into plans(plan_name, duration) values('otro', null);





