-- models/stg_telegram_messages.sql

{{ config(materialized='view') }}

SELECT
    message_id,
    channel_name,
    CAST(message_date AS TIMESTAMP) AS message_date,
    message_text,
    has_media,
    LENGTH(COALESCE(message_text, '')) AS message_length
FROM raw.telegram_messages

