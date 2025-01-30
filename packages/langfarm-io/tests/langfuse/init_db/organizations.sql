-- Table: public.organizations

-- DROP TABLE IF EXISTS public.organizations;

CREATE TABLE IF NOT EXISTS public.organizations
(
    id text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cloud_config jsonb,
    CONSTRAINT organizations_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.organizations
    OWNER to test;
