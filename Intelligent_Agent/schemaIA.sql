create table components (
    component text primary key,  
    manufacturer1 text,
    capacity1 int,
    manufacturer2 text,
    capacity2 int, 
    manufacturer3 text,
    capacity3 int,
    manufacturer4 text,
    capacity4 int,
    manufacturer5 text,
    capacity5 int 
);

create table courier (
    dayReq int primary key, 
    courier1 text,
    capacity1 int,
    courier2 text,
    capacity2 int,
    courier3 text,
    capacity3 int,
    courier4 text,
    capacity4 int,
    courier5 text,
    capacity5 int
);

create table requirements (
    dayReq int primary key,
    component1 text,
    quantity1 int,
    component2 text, 
    quantity2 int
);

create table history (
    component text,
    dayReq int,
    quantity int, 
    manufacturer text,
    courier text 
);
