
-- 1. Overall customer and churn metrics
SELECT
    COUNT(*) AS total_customers,
    SUM(Churn_Flag) AS churned_customers,
    COUNT(*) - SUM(Churn_Flag) AS retained_customers,
    ROUND(100.0 * SUM(Churn_Flag) / COUNT(*), 2) AS churn_rate
FROM customers;

-- 2. Churn by contract type
SELECT
    Contract,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * AVG(Churn_Flag), 2) AS churn_rate
FROM customers
GROUP BY Contract
ORDER BY churn_rate DESC;

-- 3. Churn by payment method
SELECT
    PaymentMethod,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * AVG(Churn_Flag), 2) AS churn_rate
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate DESC;

-- 4. Customer segmentation using a CTE
WITH customer_segments AS (
    SELECT
        CASE
            WHEN tenure <= 12 THEN 'New Customers'
            WHEN tenure <= 48 THEN 'Mid-Tenure Customers'
            ELSE 'Long-Tenure Customers'
        END AS customer_segment,
        Churn_Flag
    FROM customers
)
SELECT
    customer_segment,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * AVG(Churn_Flag), 2) AS churn_rate
FROM customer_segments
GROUP BY customer_segment
ORDER BY churn_rate DESC;

-- 5. Rank customer segments by churn risk using a window function
WITH segment_metrics AS (
    SELECT
        Contract,
        Tenure_Group,
        COUNT(*) AS customers,
        ROUND(100.0 * AVG(Churn_Flag), 2) AS churn_rate
    FROM customers
    GROUP BY Contract, Tenure_Group
)
SELECT
    Contract,
    Tenure_Group,
    customers,
    churn_rate,
    RANK() OVER (ORDER BY churn_rate DESC) AS risk_rank
FROM segment_metrics
ORDER BY risk_rank;
