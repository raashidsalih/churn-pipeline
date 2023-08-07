with dim_synthesized as (
    
    select
        id, 
        model_version, 
        synthesis_datetime, 
        insert_datetime

    from {{ ref('stg_synthesized') }}
)

select * from dim_synthesized