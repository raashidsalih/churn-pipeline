
  
    

  create  table "pgdb"."churn"."dim_demographics__dbt_tmp"
  
  
    as
  
  (
    with dim_demographics as (
    
    select
        id,
        gender, 
        senior_citizen, 
        partner, 
        dependents,
        insert_datetime

    from "pgdb"."churn"."stg_demographics"
)

select * from dim_demographics
  );
  