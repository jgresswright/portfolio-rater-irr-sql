WITH rating_distances AS (
	SELECT
		evaluation_id,
		MAX(rating) - MIN(rating) AS rating_distance
	FROM ratings
	GROUP BY evaluation_id
)
SELECT
	CASE
		WHEN e.batch_id IN ('B1', 'B2') THEN 'early'
		WHEN e.batch_id IN ('B4', 'B5', 'B6') THEN 'late'
	END AS batch_cohort,
	AVG(r.rating_distance) AS avg_distance
FROM evaluations e
INNER JOIN rating_distances r ON e.evaluation_id = r.evaluation_id
GROUP BY batch_cohort
ORDER BY avg_distance DESC
