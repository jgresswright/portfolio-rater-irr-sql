WITH deltas AS (
	SELECT
		ABS(LAG(rating, 1) OVER (PARTITION BY rater_id ORDER BY rated_at) - rating) AS delta,
		rater_id
	FROM ratings
)
SELECT
	rater_id,
	AVG(delta) AS avg_delta
FROM deltas
GROUP BY rater_id
ORDER BY avg_delta DESC
