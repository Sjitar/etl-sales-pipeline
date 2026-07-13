select id as post_id,
    user_id,
    title,
    body,
    length(title) as title_length,
    length(body) as body_length
from {{ source('raw', 'posts') }}