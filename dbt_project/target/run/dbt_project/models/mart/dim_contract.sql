
  
    

  create  table "pgdb"."churn"."dim_contract__dbt_tmp"
  
  
    as
  
  (
    with dim_contract as (
    
    select
        id,
        contract, 
        paperless_billing, 
        payment_method, 
        monthly_charges, 
        total_charges, 
        actual_churn_label, 
        insert_datetime

    from "pgdb"."churn"."stg_contract"
)

select * from dim_contract
  );
  