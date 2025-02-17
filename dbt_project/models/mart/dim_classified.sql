with dim_classified as (
    
    select
        id, 
        model_version, 
        predicted_churn_label, 
        confidence, 
        inference_datetime, 
        insert_datetime

    from {{ ref('stg_classified') }}
)

select * from dim_classified