with users as (
    select *
    from {{ ref('stg_users') }}
),
posts as (
    select *
    from {{ ref('stg_posts') }}
)
select users.user_id,
    users.name,
    users.username,
    users.email,
    count(posts.post_id) as posts_count,
    round(avg(posts.title_length), 2) as avg_title_length,
    round(avg(posts.body_length), 2) as avg_body_length
from users
    left join posts on users.user_id = posts.user_id
group by users.user_id,
    users.name,
    users.username,
    users.email