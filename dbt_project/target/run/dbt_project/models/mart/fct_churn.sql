
  
    

  create  table "pgdb"."churn"."fct_churn__dbt_tmp"
  
  
    as
  
  (
    with
contract as (

    select
        id

    from "pgdb"."churn"."dim_contract"
),


classified as (
    
    select
        id, 
        churn_label, 
        confidence

    from "pgdb"."churn"."dim_classified"
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
  );
  