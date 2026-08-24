-- Farmer Table DDL
CREATE TABLE farmers (
    farmer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    aadhaar_hash VARCHAR(64) UNIQUE NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    land_holding_hectares FLOAT NOT NULL,
    village_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staff Table DDL
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    mandi_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(15) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'MANDI_ADMIN',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);