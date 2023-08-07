
  
    

  create  table "pgdb"."churn"."dim_location__dbt_tmp"
  
  
    as
  
  (
    with dim_location as (
    
    select
        id, 
        country, 
        state, 
        city, 
        zip_code, 
        lat_long, 
        latitude, 
        longitude,
        insert_datetime

    from "pgdb"."churn"."stg_location"
)

select * from dim_location
  );
  