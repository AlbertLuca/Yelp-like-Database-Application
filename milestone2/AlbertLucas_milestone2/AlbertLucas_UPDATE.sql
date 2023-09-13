-- "num_checkins" value for a business is updated in the "CheckIn" table
UPDATE Business
SET num_checkins = (
    SELECT SUM(count)
    FROM CheckIn
    WHERE CheckIn.business_id = Business.business_id
)
WHERE Business.business_id IN (
    SELECT business_id
    FROM CheckIn
);


-- "review_rating" value for a business is updated in the "Business" table
UPDATE Business
SET review_rating = (
    SELECT AVG(review_stars)
    FROM Reviews
    WHERE Reviews.business_id = Business.business_id
)
WHERE Business.business_id IN (
    SELECT business_id
    FROM Reviews
);

-- "review_count" value for a business is updated in the "Business" table
UPDATE Business
SET review_count = (
    SELECT COUNT(review_id)
    FROM Reviews
    WHERE Reviews.business_id = Business.business_id
)
WHERE Business.business_id IN (
    SELECT business_id
    FROM Reviews
);