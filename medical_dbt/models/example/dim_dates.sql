{{ config(materialized='table') }}

SELECT DISTINCT
    DATE(message_date) AS date,
    EXTRACT(YEAR FROM message_date) AS year,
    EXTRACT(MONTH FROM message_date) AS month,
    EXTRACT(DAY FROM message_date) AS day
FROM {{ ref('stg_telegram_messages') }}
