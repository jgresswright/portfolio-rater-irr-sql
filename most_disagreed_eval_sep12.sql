WITH eval_averages AS (
	SELECT
		evaluation_id,
		rater_id,
		batch_id,
		rating,
		AVG(rating) OVER (PARTITION BY evaluation_id) AS evaluation_avg
	FROM ratings	
),
deviations AS (
	SELECT
		evaluation_id,
		rater_id,
		batch_id,
		ABS(rating - evaluation_avg) AS deviation,
		RANK() OVER (PARTITION BY rater_id, batch_id ORDER BY deviation DESC) AS deviation_rank
	FROM eval_averages
)
SELECT
	evaluation_id,
	rater_id,
	batch_id
FROM deviations
WHERE deviation_rank = 1
