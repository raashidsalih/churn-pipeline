
  
    

  create  table "pgdb"."churn"."stg_synthesized__dbt_tmp"
  
  
    as
  
  (
    with stg_synthesized as (
    
    select
        id, 
        model_version, 
        synthesis_datetime, 
        CURRENT_TIMESTAMP as insert_datetime

    from "pgdb"."churn"."synthesized"
)

select * from stg_synthesized
  );
  