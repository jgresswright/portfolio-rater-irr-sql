WITH rating_distances AS (
	SELECT
		evaluation_id,
		MAX(r.rating) - MIN(r.rating) AS rating_distance
	FROM ratings r
	GROUP BY evaluation_id
)
SELECT
	AVG(rd.rating_distance) AS avg_distance,
	e.domain
FROM rating_distances rd
LEFT JOIN evaluations e ON rd.evaluation_id = e.evaluation_id
GROUP BY e.domain
ORDER BY avg_distance DESC
