-- Table: public.api_keys

-- DROP TABLE IF EXISTS public.api_keys;

CREATE TABLE IF NOT EXISTS public.api_keys
(
    id text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    note text COLLATE pg_catalog."default",
    public_key text COLLATE pg_catalog."default" NOT NULL,
    hashed_secret_key text COLLATE pg_catalog."default" NOT NULL,
    display_secret_key text COLLATE pg_catalog."default" NOT NULL,
    last_used_at timestamp(3) without time zone,
    expires_at timestamp(3) without time zone,
    project_id text COLLATE pg_catalog."default" NOT NULL,
    fast_hashed_secret_key text COLLATE pg_catalog."default",
    CONSTRAINT api_keys_pkey PRIMARY KEY (id),
    CONSTRAINT api_keys_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.projects (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.api_keys
    OWNER to test;
-- Index: api_keys_fast_hashed_secret_key_idx

-- DROP INDEX IF EXISTS public.api_keys_fast_hashed_secret_key_idx;

CREATE INDEX IF NOT EXISTS api_keys_fast_hashed_secret_key_idx
    ON public.api_keys USING btree
    (fast_hashed_secret_key COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_keys_fast_hashed_secret_key_key

-- DROP INDEX IF EXISTS public.api_keys_fast_hashed_secret_key_key;

CREATE UNIQUE INDEX IF NOT EXISTS api_keys_fast_hashed_secret_key_key
    ON public.api_keys USING btree
    (fast_hashed_secret_key COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_keys_hashed_secret_key_idx

-- DROP INDEX IF EXISTS public.api_keys_hashed_secret_key_idx;

CREATE INDEX IF NOT EXISTS api_keys_hashed_secret_key_idx
    ON public.api_keys USING btree
    (hashed_secret_key COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_keys_hashed_secret_key_key

-- DROP INDEX IF EXISTS public.api_keys_hashed_secret_key_key;

CREATE UNIQUE INDEX IF NOT EXISTS api_keys_hashed_secret_key_key
    ON public.api_keys USING btree
    (hashed_secret_key COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_keys_id_key

-- DROP INDEX IF EXISTS public.api_keys_id_key;

CREATE UNIQUE INDEX IF NOT EXISTS api_keys_id_key
    ON public.api_keys USING btree
    (id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_keys_project_id_idx

-- DROP INDEX IF EXISTS public.api_keys_project_id_idx;

CREATE INDEX IF NOT EXISTS api_keys_project_id_idx
    ON public.api_keys USING btree
    (project_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_keys_public_key_idx

-- DROP INDEX IF EXISTS public.api_keys_public_key_idx;

CREATE INDEX IF NOT EXISTS api_keys_public_key_idx
    ON public.api_keys USING btree
    (public_key COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_keys_public_key_key

-- DROP INDEX IF EXISTS public.api_keys_public_key_key;

CREATE UNIQUE INDEX IF NOT EXISTS api_keys_public_key_key
    ON public.api_keys USING btree
    (public_key COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;