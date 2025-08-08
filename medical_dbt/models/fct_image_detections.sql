{{ config(materialized='table') }}

SELECT
    detection_id,
    message_id,
    detected_object_class,
    confidence_score
FROM raw.image_detections
