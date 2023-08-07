
  
    

  create  table "pgdb"."churn"."stg_demographics__dbt_tmp"
  
  
    as
  
  (
    with stg_demographics as (
    
    select
        id,
        gender, 
        senior_citizen, 
        partner, 
        dependents,
        CURRENT_TIMESTAMP as insert_datetime

    from "pgdb"."churn"."customers"
)

select * from stg_demographics
  );
  