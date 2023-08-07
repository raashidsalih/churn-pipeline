with stg_synthesized as (
    
    select
        id, 
        model_version, 
        synthesis_datetime, 
        CURRENT_TIMESTAMP as insert_datetime

    from {{ source('churn', 'synthesized') }}
)

select * from stg_synthesized