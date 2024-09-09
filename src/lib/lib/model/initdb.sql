CREATE SCHEMA IF NOT EXISTS osint;

DO $$ BEGIN
    CREATE TYPE osint.page_status AS ENUM ('ready', 'crawling', 'finished', 'failed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE osint.pages
(
  id           bigserial PRIMARY KEY,
  site         TEXT NOT NULL,
  url          TEXT UNIQUE NOT NULL,
  release_date TIMESTAMP WITH TIME ZONE,
  meta         jsonb,
  created_at   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP WITH TIME ZONE,
  status       osint.page_status
);

CREATE INDEX pages_site_key ON osint.pages (site);

ALTER TABLE IF EXISTS osint.pages
    OWNER to postgres;

CREATE INDEX site
    ON osint.pages USING btree
    (site ASC NULLS LAST)
    WITH (deduplicate_items=True)
;
CREATE INDEX status
    ON osint.pages USING btree
    (status ASC NULLS LAST)
    WITH (deduplicate_items=True)
;
CREATE INDEX url
    ON osint.pages USING btree
    (url ASC NULLS LAST)
    WITH (deduplicate_items=True)
;

DO $$ BEGIN
    CREATE TYPE osint.ioc_type AS ENUM ('url', 'ip', 'hash', 'yara_rule', 'cve_id', 'mitre_attack_technique_id');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE osint.iocs
(
  id           bigserial PRIMARY KEY,
  type         osint.ioc_type,
  key          TEXT UNIQUE NOT NULL
);

CREATE TABLE osint.relations
(
    id           bigserial PRIMARY KEY,
    iocs_id      integer references osint.iocs,
    pages_id     integer references osint.pages,
    created_at   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);