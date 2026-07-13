select id as user_id,
    name,
    username,
    lower(email) as email
from {{ source('raw', 'users') }}