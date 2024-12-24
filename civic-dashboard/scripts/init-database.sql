-- Drop the table if it exists (Optional, for testing purposes)
DROP TABLE IF EXISTS city_council_meetings;

-- Create the city_council_meetings table
CREATE TABLE city_council_meetings (
    id VARCHAR PRIMARY KEY,
    term_id INTEGER,
    agenda_item_id INTEGER,
    council_agenda_item_id INTEGER,
    decision_body_id INTEGER,
    meeting_id INTEGER,
    item_process_id INTEGER,
    decision_body_name VARCHAR,
    meeting_date TIMESTAMP,
    reference VARCHAR,
    term_year VARCHAR,
    agenda_cd VARCHAR,
    meeting_number VARCHAR,
    item_status VARCHAR,
    agenda_item_title TEXT,
    agenda_item_summary TEXT,
    agenda_item_recommendation TEXT,
    decision_recommendations TEXT,
    decision_advice TEXT,
    subject_terms TEXT,
    background_attachment_ids JSONB,
    agenda_item_address JSONB,
    addresses JSONB,
    geo_locations JSONB,
    ward_ids JSONB
);
