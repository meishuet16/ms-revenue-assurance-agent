INSERT INTO contracts VALUES
('CON-NOVA','CUST-NOVA','Nova Retail','flat','USD','2025-01-01','active'),
('CON-KEN','CUST-KENSINGTON','Kensington Labs','flat','USD','2025-01-01','active'),
('CON-BF','CUST-BRIGHTFARM','BrightFarm Co','flat','USD','2025-01-01','active'),
('CON-SUM','CUST-SUMMIT','Summit Manufacturing','usage_based','USD','2025-01-01','active');

INSERT INTO pricing_terms VALUES
('PT-0142','CON-NOVA','flat_fee',21000,'monthly','2026-01-01',NULL,'approved','PT-0142'),
('PT-KEN-BASE','CON-KEN','flat_fee',12000,'monthly','2026-01-01',NULL,'approved','DOC-0001'),
('PT-BF-BASE','CON-BF','flat_fee',8000,'monthly','2026-01-01',NULL,'approved','DOC-0044'),
('PT-SUM-USAGE','CON-SUM','usage_rate',2.5,'per_unit','2026-01-01',NULL,'approved',NULL);

INSERT INTO invoices VALUES
('INV-NOVA-2026-07','CUST-NOVA','2026-07-01','2026-07-31',18000),
('INV-NOVA-2026-08','CUST-NOVA','2026-08-01','2026-08-31',18000),
('INV-NOVA-2026-09','CUST-NOVA','2026-09-01','2026-09-30',18000),
('INV-KEN-2026-07','CUST-KENSINGTON','2026-07-01','2026-07-31',10000),
('INV-KEN-2026-08','CUST-KENSINGTON','2026-08-01','2026-08-31',10000),
('INV-KEN-2026-09','CUST-KENSINGTON','2026-09-01','2026-09-30',10000),
('INV-BF-2026-07','CUST-BRIGHTFARM','2026-07-01','2026-07-31',7500),
('INV-BF-2026-08','CUST-BRIGHTFARM','2026-08-01','2026-08-31',7500),
('INV-BF-2026-09','CUST-BRIGHTFARM','2026-09-01','2026-09-30',7500);

INSERT INTO invoice_lines
SELECT 'IL-' || invoice_id, invoice_id, 'base_fee', 1, total_amount, total_amount FROM invoices;

INSERT INTO usage_records VALUES
('UR-SUMMIT-SEP-A','CUST-SUMMIT','2026-09-01','2026-09-30',4200),
('UR-SUMMIT-SEP-B','CUST-SUMMIT','2026-09-01','2026-09-30',3850);

INSERT INTO commercial_exceptions VALUES
('EX-KEN-Q3','CUST-KENSINGTON','retention_concession',2000,'2026-07-01','2026-09-30','approved','J. Tan','DOC-0001'),
('EX-BF-JUL','CUST-BRIGHTFARM','retention_concession',500,'2026-07-01','2026-07-31','approved','J. Tan','DOC-0044'),
('EX-BF-AUGSEP','CUST-BRIGHTFARM','retention_concession',500,'2026-08-01','2026-09-30','approved','J. Tan','DOC-0044');

