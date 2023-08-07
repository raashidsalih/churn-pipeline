
  
    

  create  table "pgdb"."churn"."dim_classified__dbt_tmp"
  
  
    as
  
  (
    with dim_classified as (
    
    select
        id, 
        model_version, 
        churn_label, 
        confidence, 
        inference_datetime, 
        insert_datetime

    from "pgdb"."churn"."stg_classified"
)

select * from dim_classified
  );
  