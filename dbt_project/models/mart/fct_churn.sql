with
contract as (

    select
        id

    from {{ ref('dim_contract') }}
),


classified as (
    
    select
        id, 
        churn_label, 
        confidence

    from {{ ref('dim_classified') }}
),


final as (

    select
        contract.id,
        classified.churn_label,
        classified.confidence,
        CURRENT_TIMESTAMP as insert_datetime

    from contract join classified using (id)
)

select * from final