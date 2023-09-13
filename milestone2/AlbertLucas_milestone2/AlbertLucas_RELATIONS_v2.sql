CREATE TABLE Business(
    business_id CHAR(22),
    name VARCHAR(255) NOT NULL,
    -- number of stars the business has, if null then the business has not been reviewed yet
    stars REAL CHECK (stars >= 0 AND stars <= 5) NOT NULL,
    -- number of reviews the business has, if null then the business has not been reviewed yet
    review_count INTEGER CHECK (review_count >= 0) NOT NULL,
    -- The address of the business
    address VARCHAR(255) NOT NULL,
    -- The city of the business
    city VARCHAR(255) NOT NULL,
    -- The state of the business
    state CHAR(2) NOT NULL,
    -- the address of the business
    postal_code CHAR(5) NOT NULL,
    -- the average review rating of the business
    review_rating DECIMAL DEFAULT 0.0 CHECK (review_rating >= 0 AND review_rating <= 5) NOT NULL,
    -- the number of total checkins for the business
    num_checkins INT DEFAULT 0 NOT NULL CHECK (num_checkins >= 0),
    PRIMARY KEY (business_id)
);

CREATE TABLE zipcodeData(
    zipcode CHAR(5) NOT NULL,
    -- the total population of the zipcode
    population INTEGER CHECK (population >= 0) NOT NULL,
    -- the average income of the zipcode
    medianIncome INTEGER CHECK (medianIncome >= 0) NOT NULL,
    -- The mean income of the zipcode
    meanIncome INTEGER CHECK (meanIncome >= 0) NOT NULL,
    -- the number of businesses of a category in a zipcode
    num_businesses_category INTEGER CHECK (num_businesses_category >= 0) NOT NULL,
);

CREATE TABLE CheckIn(
    business_id CHAR(22) NOT NULL,
    -- day of the week
    day VARCHAR(255) NOT NULL,
    -- time of the day
    hour TIME NOT NULL,
    -- the number of checkins for the business at the given day and hour
    count INTEGER CHECK (count >= 0) NOT NULL,
    FOREIGN KEY (business_id) REFERENCES Business(business_id) ON DELETE CASCADE
);

CREATE TABLE Reviews(
    review_id CHAR(22) NOT NULL,
    -- the business that the review is for
    business_id CHAR(22) NOT NULL,
    -- the number of stars the business has, if null then the business has not been reviewed yet
    review_stars REAL CHECK (stars >= 0 AND stars <= 5) NOT NULL,
    PRIMARY KEY (review_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id) ON DELETE CASCADE
);

CREATE TABLE Business_Category(
    business_id CHAR(22) NOT NULL,
    -- the category of the business
    category VARCHAR(255) NOT NULL,
    PRIMARY KEY (business_id, category),
    FOREIGN KEY (business_id) REFERENCES Business(business_id) ON DELETE CASCADE
);

CREATE TABLE Popular_Business(
    business_id CHAR(22) NOT NULL,
    popular_business_name VARCHAR(255) NOT NULL,
    -- the number of stars the business has, if null then the business has not been reviewed yet
    stars REAL CHECK (stars >= 0 AND stars <= 5) NOT NULL,
    -- the review rating of the business
    review_rating REAL CHECK (review_rating >= 0 AND review_rating <= 5) NOT NULL,
    -- the total number of reviews for the business
    review_count INTEGER CHECK (review_count >= 0) NOT NULL,
    PRIMARY KEY (business_id, stars, review_rating, review_count),
    FOREIGN KEY (business_id) REFERENCES Business(business_id) ON DELETE CASCADE
);

CREATE TABLE Successful_Business(
    business_id CHAR(22) NOT NULL,
    successful_business_name VARCHAR(255) NOT NULL,
    -- the number of reviews the business has, if null then the business has not been reviewed yet
    review_count INTEGER CHECK (review_count >= 0) NOT NULL,
    -- the number of total checkins for the business
    num_checkins INT DEFAULT 0 NOT NULL CHECK (num_checkins >= 0),
    PRIMARY KEY (business_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id) ON DELETE CASCADE
);
