-- Table: public.projects

-- DROP TABLE IF EXISTS public.projects;

CREATE TABLE IF NOT EXISTS public.projects
(
    id text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name text COLLATE pg_catalog."default" NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    org_id text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT projects_pkey PRIMARY KEY (id),
    CONSTRAINT projects_org_id_fkey FOREIGN KEY (org_id)
        REFERENCES public.organizations (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.projects
    OWNER to test;
-- Index: projects_org_id_idx

-- DROP INDEX IF EXISTS public.projects_org_id_idx;

CREATE INDEX IF NOT EXISTS projects_org_id_idx
    ON public.projects USING btree
    (org_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;