delimiter $$
CREATE TRIGGER average
before  INSERT
   ON history FOR EACH ROW

BEGIN

DECLARE avgs INT;
Declare times date;
Declare id varchar(10);

declare turn int;
   
    set avgs = (select avg(stock_price) from history where year_ = new.year_);
    set times = (select year_ from history where month(new.year_) = '01' or month(new.year_) = '05' or month(new.year_) = '09');
    set turn = (select Turn_over from history where month(new.year_) = '01' or month(new.year_) = '05' or month(new.year_) = '09');
    set id = new.ID;  
    insert into history( ID, year_, stock_price, Turn_over) values(id ,times , avgs, turn);
END;
$$
delimiter ;




delimiter $$
CREATE TRIGGER change_turn
before  INSERT
   ON history FOR EACH ROW

BEGIN

   
    set new.Turn_over = new.Turn_over/4;
END;
$$
delimiter ;


delimiter $$
CREATE TRIGGER same_
before  INSERT
   ON history FOR EACH ROW

BEGIN
if new.year_ in (select year_ from history where new.ID = ID)
 then
signal sqlstate '45000';

END IF;   
END;
$$
delimiter ;


