
  
    

  create  table "pgdb"."churn"."stg_services__dbt_tmp"
  
  
    as
  
  (
    with stg_services as (
    
    select
        id,
        tenure_months,
        phone_service, 
        multiple_lines, 
        internet_service, 
        online_security, 
        online_backup, 
        device_protection, 
        tech_support, 
        streaming_tv, 
        streaming_movies,
        CURRENT_TIMESTAMP as insert_datetime

    from "pgdb"."churn"."customers"
)

select * from stg_services
  );
  