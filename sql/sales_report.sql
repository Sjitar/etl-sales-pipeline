SELECT
    category,
    SUM(total) AS revenue,
    SUM(quantity) AS items_sold,
    COUNT(*) AS orders_count
FROM sales
GROUP BY category
ORDER BY revenue DESC
