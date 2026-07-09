SELECT u.id AS user_id,
    u.name,
    u.username,
    u.email,
    COUNT(p.id) AS posts_count
FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id,
    u.name,
    u.username,
    u.email
ORDER BY posts_count DESC