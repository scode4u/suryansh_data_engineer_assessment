SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS rehab;
DROP TABLE IF EXISTS hoa;
DROP TABLE IF EXISTS valuation;
DROP TABLE IF EXISTS properties;

SET FOREIGN_KEY_CHECKS = 1;


--  Main properties table
CREATE TABLE properties (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    zip_code VARCHAR(20),
    sqft_total INT,
    bedrooms INT,
    bathrooms INT,
    year_built INT,
    latitude DOUBLE,
    longitude DOUBLE
);

-- Valuation table (multiple rows per property)
CREATE TABLE valuation (
    valuation_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    list_price DECIMAL(12,2),
    zestimate DECIMAL(12,2),
    arv DECIMAL(12,2),
    expected_rent DECIMAL(12,2),
    rent_zestimate DECIMAL(12,2),
    low_fmr DECIMAL(12,2),
    high_fmr DECIMAL(12,2),
    redfin_value DECIMAL(12,2),
    previous_rent DECIMAL(12,2),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

-- HOA table (multiple rows per property)
CREATE TABLE hoa (
    hoa_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa_fee DECIMAL(12,2),
    hoa_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

-- Rehab table (multiple rows per property)
CREATE TABLE rehab (
    rehab_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab DECIMAL(12,2),
    rehab_calculation DECIMAL(12,2),
    flooring_flag VARCHAR(10),
    foundation_flag VARCHAR(10),
    roof_flag VARCHAR(10),
    hvac_flag VARCHAR(10),
    kitchen_flag VARCHAR(10),
    bathroom_flag VARCHAR(10),
    appliances_flag VARCHAR(10),
    windows_flag VARCHAR(10),
    landscaping_flag VARCHAR(10),
    trashout_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);
