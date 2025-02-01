-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default",
    email text COLLATE pg_catalog."default",
    email_verified timestamp(3) without time zone,
    password text COLLATE pg_catalog."default",
    image text COLLATE pg_catalog."default",
    created_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    feature_flags text[] COLLATE pg_catalog."default" DEFAULT ARRAY[]::text[],
    admin boolean NOT NULL DEFAULT false,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to test;
-- Index: users_email_key

-- DROP INDEX IF EXISTS public.users_email_key;

CREATE UNIQUE INDEX IF NOT EXISTS users_email_key
    ON public.users USING btree
    (email COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;