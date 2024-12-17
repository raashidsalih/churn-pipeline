
  
    

  create  table "pgdb"."churn"."fct_churn__dbt_tmp"
  
  
    as
  
  (
    with
contract as (

    select
        id,
        actual_churn_label

    from "pgdb"."churn"."dim_contract"
),


classified as (
    
    select
        id, 
        predicted_churn_label, 
        confidence

    from "pgdb"."churn"."dim_classified"
),


final as (

    select
        contract.id,
        contract.actual_churn_label,
        classified.predicted_churn_label,
        classified.confidence,
        CURRENT_TIMESTAMP as insert_datetime

    from contract join classified using (id)
)

select * from final
  );
  