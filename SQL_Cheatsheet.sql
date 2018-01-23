/////* SQL cheatsheets */////
-- MySQL		Date-time functions		Where conditions: Logic, Math		Partition over
-- Standard		Count, Aggregations		Regexp & String manipulation		Case statement
-- BigQuery		Math functions			Joins & Unions
-- Database management: Create, Insert, Load, Update, Delete, Alter. 
-- Optimising speed, costs of query

/////* COMMAND ORDER */////

  SELECT
  FROM
  WHERE
  GROUP BY 
  ORDER BY [ASC / DESC]
  HAVING 
  LIMIT   --SQL ONLY

/////* DATE-TIME FUNCTIONS */////

  SECOND      HOUR         WEEK          MONTH        YEAR
  MINUTE      DAY          DAYOFWEEK     QUARTER      TIMESTAMPDIFF
    
  SELECT 
  EXTRACT (month FROM saledate) AS month,
  EXTRACT (year FROM saledate) AS year,
  COUNT (DISTINCT EXTRACT (day FROM saledate)) AS days_in_month,
  FROM data

  SELECT TIMESTAMPDIFF(MONTH,'2009-05-18','2009-07-29');
  SELECT TIMESTAMPDIFF(MONTH, time_1, time_2) AS churn_time; 
  FROM table_name;
  
-- TIMESTAMPDIFF(hour/minute/second, var1, var2) which calculates the difference between 2 variables in the specified format.
-- DAYOFWEEK(datevar), where the day of the week will be returned as an integer from 1 - 7 where 1 = Sunday, 2 = Monday, etc.

/////* COUNTING & AGGREGATION *///// 

-- GROUP BY (ALL)
-- COUNT DISTINCT (SQL, MYSQL)
-- COUNT DISTINCT (TERADATA): can pipe multiple columns
-- EXACT_COUNT_DISTINCT (BIGQUERY): use CONCAT() to pipe multiple columns too
  
  SELECT store, city, COUNT(DISTINCT(clothes||colour||brand||price) AS num_items
  FROM shopping_data
  GROUP BY store, city
 
-- Use EXACT_COUNT_DISTINCT to perform a group-by:

/* Notes: Using COUNT(DISTINCT x) in BigQuery for values larger than 1,000 returns an approximation.
  You can specify the level of approximation (i.e., COUNT(DISTINCT students, 10,000) which will return
  the exact amount, but this is costly in terms of performance. Hence where possible, use EXACT_COUNT_DISTINCT. */

  SELECT classes, age, 
  EXACT_COUNT_DISTINCT (CONCAT (student, teacher, STRING(date_of_birth))) AS aggregation
  FROM database
  GROUP BY classes, age

/////* MATH FUNCTIONS */////

-- MIN()    AVG()     FLOOR()     STDDEV_POP() population stdev    VAR_POP() population variance
-- MAX()    SUM()     CEILING()   STDDEV_SAMP() sample stdev       VAR_SAMP() sample variance
		    
/////* WHERE CONDITIONS */////

# LOGIC: Use Brackets to separate logical operators. 
# -- AND    OR      NOT 

# MATH:
# -- BETWEEN... AND... 
# -- NULL / NOT NULL
# -- equals = 
# -- not equals <>
# -- comparisons >= / <= / > / <
 
  SELECT students
  FROM database
  WHERE student_age BETWEEN 10 AND 20;
  
  SELECT students
  FROM database
  WHERE (student_age <> 16) AND (student_age >= 10);

# STRING:
# -- LIKE
# -- IN
# -- WILDCARD % (any number of characters)
# -- WILDCARE _ (exact 1 wild character)

/////* REGEX, STRING MANIPULATION */////

-- REGEXP()
-- REGEXP_LIKE()
-- RLIKE()

SELECT target
FROM data 
WHERE REGEXP_LIKE( target, 'pattern')

-- [*][%] any number of characters; 
-- [.][_] just one character
-- [?] one or zero characters
-- [^] START 
-- [$] END
-- [[:alnum:]]+ alphanumeric
-- [[:alpha:]]+ alphabets only
-- [[:space:]] whitespace characters (tab, newline, space, return)
-- Decent documenation: https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp

  SELECT students
  FROM database
  WHERE student_name IN '%jane%'; 
  WHERE REGEXP_LIKE(student_name, '%jane%');
  WHERE REGEXP_LIKE(student_name, 'ben*y'); benny, beny, bey
  
-- LEFT(string, index) 
-- RIGHT(string, index)
-- MID(string, start, length)

  SELECT LEFT("Hello World!", 5) AS HELLO;
  SELECT RIGHT("Hello World!", 6) AS WORLD!;
  SELECT MID("Hello World! It's me!", 1, 5) AS HELLO;
  SELECT MID("Hello World! It's me!", -3, 2) AS ME;
  
/////* JOINS & UNION */////

-- LEFT JOIN ... ON ... 
-- RIGHT JOIN ... ON ... 
-- INNER JOIN ... ON...
-- FULL JOIN... (dont ever do this)
-- SELF JOIN (use alias to mark tables)

-- UNION 
-- UNION ALL 

  SELECT City, Country FROM Customers
  WHERE Country='Germany'
  UNION
  SELECT City, Country FROM Suppliers
  WHERE Country='Germany'
  ORDER BY City;

-- 1. Union only works with similar column names
-- 2. BigQuery has no UNION. Select from multiple tables like so: 

  SELECT City, Country 
  FROM 
  (Customers), 
  (Suppliers)
  WHERE Country='Germany'
  ORDER BY City;
  
/////* PARTITION OVER */////
-- Use partition over to create new columns. Make search faster.

  SELECT 
  store,
	SUM(revenue) AS monthly_revenue,
	SUM(revenue)/SUM(dates) AS avg_daily_revenue,
	ROW_NUMBER() OVER (PARTITION BY store ORDER BY avg_daily_revenue DESC ) AS Row_sum_rev,
	ROW_NUMBER() OVER (PARTITION BY store ORDER BY sum_monthly_revenue DESC ) AS Row_avg_rev
	FROM database;

/////* ROW_NUMBER() */////

-- creates row numbers within each category -- 
	SELECT 
	    @within_category_rank := category as Cat_Number,
	    @row_number:= CASE
	    WHEN @within_category_rank = category THEN @row_number + 1 ELSE 1
	    END AS num,    
	    column2,
	    column3,
	    column4
	FROM
	    table
	ORDER BY Cat_Number, category;

-- method 2 : order by CUSTOMER
-- Note: Wrap this in an outer query to select where row_num = 123 
			    
SELECT @row_num := IF(@prev_value = d.Customer, @row_num+1, 1) AS RowNumber
       ,d.Customer
       ,d.OrderDate
       ,d.Amount
       ,@prev_value := d.Customer -- order by CUSTOMER 
  FROM data d,
      (SELECT @row_num := 1) x,
      (SELECT @prev_value := '') y
  ORDER BY d.Customer, d.OrderDate DESC

/////* CASE */////

-- CASE (SINGULAR) TO REPLACE IF-ELSE STATEMENTS:

  SELECT sale_item,
  SUM (CASE WHEN EXTRACT(month FROM saledate)=6 AND stype='p' THEN amt END) AS rev_june,
  SUM (CASE WHEN EXTRACT(month FROM saledate)=7 AND stype='p' THEN amt END) AS rev_july,
  SUM (CASE WHEN EXTRACT(month FROM saledate)=8 AND stype='p' THEN amt END) AS rev_aug,
  (rev_aug + rev_june + rev_july) AS rev_total_summer
  FROM trnsact

-- CASE (MULTIPLE) TO CREATE BUCKETS:

  SELECT
  (CASE
  WHEN education >=50 AND education <70 THEN 'low'
  WHEN education >=70 AND education <80 THEN 'med'
  WHEN education >=80 THEN 'high'
  END) AS education_levels,
  COUNT (DISTINCT store) AS num_stores
  FROM store_msa
  GROUP BY education_levels

# ---------------------------------------------------------------------------------------------------------- # 

/////* CREATE NEW TABLES */////

  CREATE TABLE Persons (
      PersonID int,
      LastName varchar(255),
      FirstName varchar(255),
      Address varchar(255),
  );
  
  CREATE TABLE new_table_name AS
      SELECT column1, column2,...
      FROM existing_table_name
      WHERE ....;

/////* ADDING & EDITING NEW DATA */////

-- INSERT ROWS FROM OTHER TABLE:

  INSERT INTO table_2 
    SELECT table_1.column_name
    FROM table_1 WHERE table1.column_name > 100;
  
-- INSERT ROWS FROM FILE:

  LOAD DATA 
  LOCAL INFILE '/path/pet.txt' 
  INTO TABLE table_name;
  
-- INSERT ROWS FROM RAW: 

  INSERT INTO table_name
    -> VALUES ('Puffball','Diane','hamster','f','1999-03-30',NULL);

-- UPDATE ROWS:

  UPDATE table_name
  SET Name = 'new person name', City= 'new city'
  WHERE CustomerID = 1; -- selection criteria; leaving this out means ALL ROWS R UPDATED

-- DELETE ROWS:

  DELETE FROM table_name
  WHERE Name = 'Juan';
  
  # all records will be deleted
  DELETE * FROM table_name; 

-- EDIT TABLE STRUCTURE: 

  ALTER TABLE table_name
  ADD column_name datatype;

  ALTER TABLE table_name
  DROP COLUMN column_name;

  ALTER TABLE table_name
  MODIFY* COLUMN column_name datatype; -- *specific to MySQL only

/////* Notes on optimising performance & costs */////
  
  -- On BQ, where possible, use EXACT_COUNT_DISTINCT rather than COUNT(DISTINCT ) 
  -- Use GROUP BY rather than COUNT DISTINCT to save on query costs
  -- Avoid using correlated subqueries where possible. Try to use joins or uncorrelated subqueries. 
  -- Avoid IF-ELSE statements with SQL; teradata & some others dont accept it. Use CASE for consistency.
  
x -------------------------------------------- x -------------------------------------------- x
| Correlated Subquery                          | Left Join / Uncorrelated SubQ                |
| -------------------------------------------- x -------------------------------------------- |
| SELECT article, dealer, price                | SELECT s1.article, dealer, s1.price          |
| FROM   shop s1                               | FROM shop s1                                 |
| WHERE  price=(SELECT MAX(s2.price)           | JOIN (                                       |
|              FROM shop s2                    |   select article, MAX(price) AS price        |
|              WHERE s1.article = s2.article); |   FROM shop                                  |
|                                              |   GROUP BY article) AS s2                    |
|                                              |   ON s1.article = s2.article                 |
|                                              |   AND s1.price = s2.price;                   |
x -------------------------------------------- x -------------------------------------------- x           
  
