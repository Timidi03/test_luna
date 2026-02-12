BEGIN;

INSERT INTO activities (id, name, path) VALUES
(1, 'Services', '1.'),
(2, 'Healthcare', '1.1.'),
(3, 'Dentistry', '1.1.1.'),
(4, 'Clinic', '1.1.2.'),
(5, 'Private Clinic', '1.1.3.'),

(6, 'Education', '1.2.'),
(7, 'School', '1.2.1.'),
(8, 'University', '1.2.2.'),
(9, 'Training Center', '1.2.3.'),

(10, 'IT', '1.3.'),
(11, 'Software Development', '1.3.1.'),
(12, 'Web Development', '1.3.1.1.'),
(13, 'System Integration', '1.3.2.'),

(14, 'Trade', '2.'),
(15, 'Supermarket', '2.1.');

INSERT INTO buildings (id, address, latitude, longitude, created_at)
SELECT
    gs,
    CASE (gs % 10)
        WHEN 1 THEN 'Moscow, Tverskaya St., bld. ' || (5 + gs)
        WHEN 2 THEN 'Moscow, Leninsky Prospekt, bld. ' || (10 + gs)
        WHEN 3 THEN 'Moscow, Arbat St., bld. ' || (3 + gs)
        WHEN 4 THEN 'Moscow, Kutuzovsky Prospekt, bld. ' || (15 + gs)
        WHEN 5 THEN 'Moscow, Prospekt Mira, bld. ' || (20 + gs)
        WHEN 6 THEN 'Moscow, Profsoyuznaya St., bld. ' || (7 + gs)
        WHEN 7 THEN 'Moscow, Baumanskaya St., bld. ' || (12 + gs)
        WHEN 8 THEN 'Moscow, Varshavskoe Shosse, bld. ' || (30 + gs)
        WHEN 9 THEN 'Moscow, Maroseyka St., bld. ' || (2 + gs)
        ELSE 'Moscow, Dmitrovskoye Shosse, bld. ' || (40 + gs)
    END,

    55.70 + (random() * 0.2),
    37.50 + (random() * 0.3),
    now()
FROM generate_series(1, 30) AS gs;

INSERT INTO organizations (id, name, building_id)
SELECT
    gs,
    CASE (gs % 10)
        WHEN 1 THEN 'City Clinic #' || gs
        WHEN 2 THEN 'Dental Clinic "Dental+' || gs || '"'
        WHEN 3 THEN 'Private Clinic "MedCenter ' || gs || '"'
        WHEN 4 THEN 'School #' || (100 + gs)
        WHEN 5 THEN 'University Center #' || gs
        WHEN 6 THEN 'Training Center "Profi ' || gs || '"'
        WHEN 7 THEN 'IT Company "TechSoft' || gs || '"'
        WHEN 8 THEN 'Web Studio "WebPro' || gs || '"'
        WHEN 9 THEN 'System Integrator "SysInt' || gs || '"'
        ELSE 'Supermarket "Market ' || gs || '"'
    END,

    (1 + (gs % 30))
FROM generate_series(1, 50) AS gs;

INSERT INTO organization_activities (organization_id, activity_id)
SELECT
    id,
    CASE
        WHEN name ILIKE '%Clinic%' THEN 4
        WHEN name ILIKE '%Dental%' THEN 3
        WHEN name ILIKE '%MedCenter%' THEN 5
        WHEN name ILIKE '%School%' THEN 7
        WHEN name ILIKE '%University%' THEN 8
        WHEN name ILIKE '%Training Center%' THEN 9
        WHEN name ILIKE '%TechSoft%' THEN 11
        WHEN name ILIKE '%WebPro%' THEN 12
        WHEN name ILIKE '%SysInt%' THEN 13
        WHEN name ILIKE '%Market%' THEN 15
    END

FROM organizations;

INSERT INTO phones (id, organization_id, phone_number)
SELECT
    row_number() OVER (),
    o.id,
    CASE
        WHEN (random() < 0.5)
            THEN '79' || floor(100000000 + random()*899999999)::bigint
        ELSE '7-495-' || lpad(floor(100 + random()*899)::text, 3, '0')
    END
FROM organizations o
JOIN generate_series(1,3) gs ON random() < 0.7;
COMMIT;
