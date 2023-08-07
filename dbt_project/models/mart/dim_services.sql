with dim_services as (
    
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
        insert_datetime

    from {{ ref('stg_services') }}
)

select * from dim_services