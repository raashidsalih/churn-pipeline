
  
    

  create  table "pgdb"."churn"."stg_location__dbt_tmp"
  
  
    as
  
  (
    with stg_location as (
    
    select
        id, 
        country, 
        state, 
        city, 
        zip_code, 
        lat_long, 
        latitude, 
        longitude,
        CURRENT_TIMESTAMP as insert_datetime

    from "pgdb"."churn"."customers"
)

select * from stg_location
  );
  