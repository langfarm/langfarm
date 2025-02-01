-- Table: public.models

-- DROP TABLE IF EXISTS public.models;

CREATE TABLE IF NOT EXISTS public.models
(
    id text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(3) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    project_id text COLLATE pg_catalog."default",
    model_name text COLLATE pg_catalog."default" NOT NULL,
    match_pattern text COLLATE pg_catalog."default" NOT NULL,
    start_date timestamp(3) without time zone,
    input_price numeric(65,30),
    output_price numeric(65,30),
    total_price numeric(65,30),
    unit text COLLATE pg_catalog."default",
    tokenizer_config jsonb,
    tokenizer_id text COLLATE pg_catalog."default",
    CONSTRAINT models_pkey PRIMARY KEY (id),
    CONSTRAINT models_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.projects (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.models
    OWNER to test;
-- Index: models_model_name_idx

-- DROP INDEX IF EXISTS public.models_model_name_idx;

CREATE INDEX IF NOT EXISTS models_model_name_idx
    ON public.models USING btree
    (model_name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: models_project_id_model_name_start_date_unit_key

-- DROP INDEX IF EXISTS public.models_project_id_model_name_start_date_unit_key;

CREATE UNIQUE INDEX IF NOT EXISTS models_project_id_model_name_start_date_unit_key
    ON public.models USING btree
    (project_id COLLATE pg_catalog."default" ASC NULLS LAST, model_name COLLATE pg_catalog."default" ASC NULLS LAST, start_date ASC NULLS LAST, unit COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;