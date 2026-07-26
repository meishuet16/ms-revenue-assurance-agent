CREATE OR REPLACE TABLE approval_documents (
    document_id STRING,
    customer_name STRING,
    document_text STRING
);

INSERT INTO approval_documents VALUES
('DOC-0001','Kensington Labs','J. Tan approves a retention concession of USD 2,000 per month for Kensington Labs for the full Q3 2026 period.'),
('DOC-0044','BrightFarm Co','The July concession is approved. The August and September extension is approved in principle, subject to CFO final approval. Please do not apply it to billing yet.'),
('PT-0142','Nova Retail','Nova Retail monthly platform fee increases from USD 18,000 to USD 21,000 effective 2026-01-01. The amendment is approved.');

