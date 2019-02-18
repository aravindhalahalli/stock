create database Stocks;
use Stocks;
create table Users(email varchar(50) primary key , password varchar(12) , phoneno int);
create table Company( ID varchar(10) primary key ,Cname varchar(100) , found_date date , domain varchar(20), high double , low double);
create table History( ID varchar(10) , year_ date , stock_price  double, Turn_over double , primary key(ID ,year_ ) , foreign key(ID) references Company(ID));
create table Prediction(ID varchar(10) , year_ date  , stock_price  double , primary key(ID , year_ ),foreign key(ID) refernces Company(ID) );
create table market(ID varchar(10),year_ date, GDP float , sensex float, primary key(year_ ) ,foreign key(ID) references History(ID));