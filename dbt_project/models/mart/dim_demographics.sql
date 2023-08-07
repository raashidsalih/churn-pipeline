with dim_demographics as (
    
    select
        id,
        gender, 
        senior_citizen, 
        partner, 
        dependents,
        insert_datetime

    from {{ ref('stg_demographics') }}
)

select * from dim_demographics