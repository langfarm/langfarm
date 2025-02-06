-- Type: Role

-- DROP TYPE IF EXISTS public."Role";

CREATE TYPE public."Role" AS ENUM
    ('OWNER', 'ADMIN', 'MEMBER', 'VIEWER', 'NONE');

ALTER TYPE public."Role"
    OWNER TO test;

-- Table: public.organization_memberships

-- DROP TABLE IF EXISTS public.organization_memberships;

CREATE TABLE IF NOT EXISTS public.organization_memberships
(
    id text COLLATE pg_catalog."default" NOT NULL,
    org_id text COLLATE pg_catalog."default" NOT NULL,
    user_id text COLLATE pg_catalog."default" NOT NULL,
    role "Role" NOT NULL,
    created_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT organization_memberships_pkey PRIMARY KEY (id),
    CONSTRAINT organization_memberships_org_id_fkey FOREIGN KEY (org_id)
        REFERENCES public.organizations (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT organization_memberships_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.organization_memberships
    OWNER to test;
-- Index: organization_memberships_org_id_user_id_key

-- DROP INDEX IF EXISTS public.organization_memberships_org_id_user_id_key;

CREATE UNIQUE INDEX IF NOT EXISTS organization_memberships_org_id_user_id_key
    ON public.organization_memberships USING btree
    (org_id COLLATE pg_catalog."default" ASC NULLS LAST, user_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: organization_memberships_user_id_idx

-- DROP INDEX IF EXISTS public.organization_memberships_user_id_idx;

CREATE INDEX IF NOT EXISTS organization_memberships_user_id_idx
    ON public.organization_memberships USING btree
    (user_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;