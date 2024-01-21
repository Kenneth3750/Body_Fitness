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



insert into users(nombre, apellido, edad, cedula, correo, celular, direccion) values('Juan', 'Perez', 20, '123456789', 'juanperez@example.com', '1234567890', '123 Main St');   
insert into users(nombre, apellido, edad, cedula, correo, celular, direccion) values('Maria', 'Lopez', 25, '987654321', 'marialopez@example.com', '0987654321', '456 Elm St'); 
insert into users(nombre, apellido, edad, cedula, correo, celular, direccion) values('Carlos', 'Gomez', 30, '456789123', 'carlosgomez@example.com', '4567891230', '789 Oak St'); 
insert into users(nombre, apellido, edad, cedula, correo, celular, direccion) values('Laura', 'Rodriguez', 35, '321654987', 'laurarodriguez@example.com', '0321654987', '789 Maple St'); 

insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(1, 1, '2023-01-01', '2023-03-03', NULL, '2023-01-01');
insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(1, 1, '2023-04-01', '2023-05-31', NULL, '2023-04-01');
insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(1, 6, '2023-06-01', '2023-07-31', 0, '2023-04-01');
insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(1, 1, '2023-12-20', '2024-01-20', NULL, '2023-12-20');
insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(2, 1, '2023-11-01', '2024-01-01', NULL, '2023-11-01');
insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(3, 5, '2024-01-03', '2024-01-18', 1, '2023-12-01');
insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(3, 1, '2024-01-20', '2024-02-20', NULL, '2023-12-01');
insert into user_plans(user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) values(4, 7, '2024-01-03', '2024-02-03', 0, '2023-12-01');



