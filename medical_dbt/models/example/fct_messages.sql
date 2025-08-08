{{ config(materialized='table') }}

SELECT
    msg.message_id,
    ch.channel_id,
    dt.date,
    msg.has_media,
    msg.message_length
FROM {{ ref('stg_telegram_messages') }} msg
LEFT JOIN {{ ref('dim_channels') }} ch
    ON msg.channel_name = ch.channel_name
LEFT JOIN {{ ref('dim_dates') }} dt
    ON DATE(msg.message_date) = dt.date
