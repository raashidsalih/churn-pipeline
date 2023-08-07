with stg_demographics as (
    
    select
        id,
        gender, 
        senior_citizen, 
        partner, 
        dependents,
        CURRENT_TIMESTAMP as insert_datetime

    from {{ source('churn', 'customers') }}
)

select * from stg_demographics