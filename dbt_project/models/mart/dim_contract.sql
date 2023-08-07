with dim_contract as (
    
    select
        id,
        contract, 
        paperless_billing, 
        payment_method, 
        monthly_charges, 
        total_charges, 
        insert_datetime

    from {{ ref('stg_contract') }}
)

select * from dim_contract