with stg_contract as (
    
    select
        id,
        contract, 
        paperless_billing, 
        payment_method, 
        ROUND(monthly_charges::numeric, 2) as monthly_charges, 
        ROUND(total_charges::numeric, 2) as total_charges, 
        actual_churn_label, 
        CURRENT_TIMESTAMP as insert_datetime

    from {{ source('churn', 'customers') }}
)

select * from stg_contract