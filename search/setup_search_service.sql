CREATE OR REPLACE CORTEX SEARCH SERVICE search_approval_documents
ON document_text
ATTRIBUTES document_id, customer_name
WAREHOUSE = RA_WH
TARGET_LAG = '1 hour'
AS (
    SELECT document_id, customer_name, document_text
    FROM approval_documents
);

