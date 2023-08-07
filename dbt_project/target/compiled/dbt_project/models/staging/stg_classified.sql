with stg_classified as (
    
    select
        id, 
        model_version, 
        churn_label, 
        ROUND(confidence::numeric,3) as confidence, 
        inference_datetime, 
        CURRENT_TIMESTAMP as insert_datetime

    from "pgdb"."churn"."classified"
)

select * from stg_classified