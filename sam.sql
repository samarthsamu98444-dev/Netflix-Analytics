-- 1. Total Titles
SELECT COUNT(*) AS total_titles
FROM netflix;

-- 2. Movies vs TV Shows
SELECT type,
       COUNT(*) AS total
FROM netflix
GROUP BY type;

-- 3. Top Countries
SELECT country,
       COUNT(*) AS total
FROM netflix
GROUP BY country
ORDER BY total DESC;

-- 4. Top Genres
SELECT genre,
       COUNT(*) AS total
FROM netflix
GROUP BY genre
ORDER BY total DESC;

-- 5. Rating Distribution
SELECT rating,
       COUNT(*) AS total
FROM netflix
GROUP BY rating
ORDER BY total DESC;

-- 6. Content By Year
SELECT release_year,
       COUNT(*) AS total
FROM netflix
GROUP BY release_year
ORDER BY release_year;

-- 7. Top Directors
SELECT director,
       COUNT(*) AS total
FROM netflix
GROUP BY director
ORDER BY total DESC;

-- 8. Movies Only
SELECT *
FROM netflix
WHERE type='Movie';

-- 9. TV Shows Only
SELECT *
FROM netflix
WHERE type='TV Show';

-- 10. Content Released After 2015
SELECT *
FROM netflix
WHERE release_year > 2015;

-- 11. Countries Above Average Content
SELECT country,
       COUNT(*) AS total
FROM netflix
GROUP BY country
HAVING COUNT(*) >
(
    SELECT AVG(cnt)
    FROM
    (
        SELECT COUNT(*) AS cnt
        FROM netflix
        GROUP BY country
    ) t
);

-- 12. Directors Above Average Titles
SELECT director,
       COUNT(*) AS total
FROM netflix
GROUP BY director
HAVING COUNT(*) >
(
    SELECT AVG(cnt)
    FROM
    (
        SELECT COUNT(*) AS cnt
        FROM netflix
        GROUP BY director
    ) t
);

-- 13. Latest Content From Each Country
SELECT *
FROM
(
    SELECT country,
           title,
           release_year,

           ROW_NUMBER() OVER(
               PARTITION BY country
               ORDER BY release_year DESC
           ) AS rn

    FROM netflix
) t

WHERE rn = 1;

-- 14. Rank Directors By Number Of Titles
SELECT director,
       COUNT(*) AS total,

       DENSE_RANK() OVER(
           ORDER BY COUNT(*) DESC
       ) AS ranking

FROM netflix

GROUP BY director;

-- 15. Running Content Growth
SELECT release_year,
       total_titles,

       SUM(total_titles) OVER(
           ORDER BY release_year
       ) AS running_total

FROM
(
    SELECT release_year,
           COUNT(*) AS total_titles

    FROM netflix

    GROUP BY release_year
) t;

-- 16. Top Genre In Each Country
SELECT *
FROM
(
    SELECT country,
           genre,
           COUNT(*) AS total,

           RANK() OVER(
               PARTITION BY country
               ORDER BY COUNT(*) DESC
           ) AS rnk

    FROM netflix

    GROUP BY country, genre
) t

WHERE rnk = 1;

-- 17. Earliest Content
SELECT *
FROM netflix
ORDER BY release_year
LIMIT 1;

-- 18. Latest Content
SELECT *
FROM netflix
ORDER BY release_year DESC
LIMIT 1;

-- 19. Count Content Per Director
SELECT director,
       COUNT(*) AS total_titles
FROM netflix
GROUP BY director
ORDER BY total_titles DESC;

-- 20. Country Wise Movies vs TV Shows
SELECT country,
       type,
       COUNT(*) AS total
FROM netflix
GROUP BY country, type
ORDER BY country;
