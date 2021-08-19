--Question set 1
SELECT f.title,
	   c.name,
       COUNT(*)
  FROM category c
  JOIN film_category fc
  ON c.category_id = fc.category_id
  JOIN film f
  ON f.film_id = fc.film_id
  JOIN inventory i
  ON i.film_id = f.film_id
  JOIN rental r
  ON r.inventory_id = i.inventory_id
  WHERE c.name IN
 ('Animation','Children','Classics','Comedy','Family','Music')
  GROUP BY 1,2
  ORDER BY 2;

-- PROJECT Question 1
WITH rental_counts AS(
  SELECT f.title,
  	   c.name,
         COUNT(*) rental_counts_movie
    FROM category c
    JOIN film_category fc
    ON c.category_id = fc.category_id
    JOIN film f
    ON f.film_id = fc.film_id
    JOIN inventory i
    ON i.film_id = f.film_id
    JOIN rental r
    ON r.inventory_id = i.inventory_id
    WHERE c.name IN
   ('Animation','Children','Classics','Comedy','Family','Music')
    GROUP BY 1,2
    ORDER BY 2
)

SELECT name,
       SUM(rental_counts_movie)
FROM rental_counts
GROUP BY 1

--Question 2
WITH rental_counts AS(
  SELECT f.title,
  	   c.name,
         COUNT(*) rental_counts_movie
    FROM category c
    JOIN film_category fc
    ON c.category_id = fc.category_id
    JOIN film f
    ON f.film_id = fc.film_id
    JOIN inventory i
    ON i.film_id = f.film_id
    JOIN rental r
    ON r.inventory_id = i.inventory_id
    WHERE c.name IN
   ('Animation','Children','Classics','Comedy','Family','Music')
    GROUP BY 1,2
    ORDER BY 2
)

--Question set 2

--PROJECT Question 3
SELECT DATE_PART('month',r.rental_date) rental_month,
       DATE_PART('year',r.rental_date) rental_year,
       i.store_id store_ID,
       COUNT(*) rental_counts
FROM inventory i
JOIN rental r
ON r.inventory_id = i.inventory_id
GROUP BY 1,2,3
ORDER BY 4 DESC;

--Question 3
WITH top_paying_customers AS (
  SELECT c.customer_id,
	      CONCAT(c.first_name,' ',c.last_name) full_name,
        SUM(amount) total_payment
  FROM customer c
  JOIN payment p
  ON c.customer_id = p.customer_id
  GROUP BY 1,2
  ORDER BY 3 DESC
  LIMIT 10
)

SELECT tpc.full_name,
       DATE_TRUNC('month',payment_date),
       COUNT (*) num_transactions,
       SUM(amount) monthly_sum
FROM payment p
JOIN top_paying_customers tpc
ON tpc.customer_id = p.customer_id
GROUP BY 1,2
ORDER BY 1;

-- PROJECT Question 4
WITH top_paying_customers AS (
  SELECT c.customer_id,
	      CONCAT(c.first_name,' ',c.last_name) full_name,
        SUM(amount) total_payment
  FROM customer c
  JOIN payment p
  ON c.customer_id = p.customer_id
  GROUP BY 1,2
  ORDER BY 3 DESC
  LIMIT 10
),
monthly_payments_of_tpc AS (
  SELECT tpc.full_name,
       DATE_TRUNC('month',payment_date) the_date,
       COUNT (*) num_transactions,
       SUM(amount) monthly_sum
FROM payment p
JOIN top_paying_customers tpc
ON tpc.customer_id = p.customer_id
GROUP BY 1,2
ORDER BY 1
)
SELECT full_name,
	   the_date,
	   mptpc.monthly_sum,
       LAG(mptpc.monthly_sum) OVER (PARTITION BY full_name) lag,
	   monthly_sum - LAG(mptpc.monthly_sum) OVER (PARTITION BY full_name) monthly_difference
FROM monthly_payments_of_tpc mptpc











WITH actor_movies AS(
  SELECT fa.actor_id,
         r.rental_id,
         CONCAT(a.first_name,' ',a.last_name) full_name
  FROM film f
  JOIN film_actor fa
  ON fa.film_id = f.film_id
  JOIN inventory i
  ON fa.film_id = i.film_id
  JOIN rental r
  ON r.inventory_id = i.inventory_id
  JOIN actor a
  ON a.actor_id = fa.actor_id
)
SELECT actor_id,full_name,
       COUNT(*) rental_counts,
       NTILE(4) OVER (ORDER BY COUNT(*)) perctle
FROM actor_movies
GROUP BY 1,2
ORDER BY 3 DESC

WITH actor_movies AS(
  SELECT fa.actor_id,
         r.rental_id,
         CONCAT(a.first_name,' ',a.last_name) full_name
  FROM film f
  JOIN film_actor fa
  ON fa.film_id = f.film_id
  JOIN inventory i
  ON fa.film_id = i.film_id
  JOIN rental r
  ON r.inventory_id = i.inventory_id
  JOIN actor a
  ON a.actor_id = fa.actor_id
),
ordered_actors AS (
  SELECT actor_id,full_name,
        COUNT(*) rental_counts,
        NTILE(4) OVER (ORDER BY COUNT(*)) perctle
  FROM actor_movies
  GROUP BY 1,2
  ORDER BY 3 DESC
  LIMIT 10
)

SELECT oa.actor_id,
       oa.full_name
FROM ordered_actors oa
JOIN film_actor fa
ON fa.actor_id = oa.actor_id
JOIN film f
ON f.film_id = fa.film_id










--PROJECT Question 2

--Additional query
SELECT film_id,
	   title,
       length,
       NTILE(4) OVER (ORDER BY length)
FROM film
ORDER BY 2

--The main query for this question
SELECT f.film_id,
       f.title,
       f.length,
       t1.count,
       NTILE(4) OVER (ORDER BY length)
FROM(
    SELECT f.film_id,
          f.title,
          COUNT(*)
    FROM film f
    JOIN inventory i
    ON f.film_id = i.film_id
    JOIN rental r
    ON r.inventory_id = i.inventory_id
    GROUP BY 1,2
    ORDER BY 3 DESC
    LIMIT 10
  ) t1
JOIN film f
ON t1.film_id = f.film_id
ORDER BY 2
