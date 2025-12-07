-- Insert Dummy Users
-- frontend users
INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'alice', 'Alice Doe', 'alice@example.com', NOW(), 'FRONTEND', 'https://discord.com/api/webhooks/1446448448353210409/B9nie_rwl7M44PxqsRnSeMJSaIZbVKlCqggKqCipoZ0FwnGbN9lqwAuZaDtwm3K42dG6', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'alice'
);

INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'jacob', 'Jacob cidar', 'jacob@example.com', NOW(), 'FRONTEND', 'https://discord.com/api/webhooks/1446448675663511625/x4TzgxXGZgp1-9xuUpjJGipPxja7szdM2lr50iz4rodZv_1IVBdZB54mdX5PMs-zSiWq', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'jacob'
);

-- backend users
INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'john', 'John Cap', 'john@example.com', NOW(), 'BACKEND', 'https://discord.com/api/webhooks/1446448806542708737/YWtr63c-K8pkayNR0G3A3fWq2yxE7wwLmTStxipgYpCubOTOWbLRB9XFbkgCtcznGF3D', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'john'
);

INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'henry', 'Henry herald', 'henry@example.com', NOW(), 'BACKEND', 'https://discord.com/api/webhooks/1446448921160454216/QCzjKHhuew74Ce3mo6GvfKAH359SjSYXxdgM6pEoHgdYvWcrhNAFWq6E2K1YaNiD5DiS', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'henry'
);

-- devops users
INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'michael', 'Michael rhodes', 'michael@example.com', NOW(), 'DEVOPS', 'https://discord.com/api/webhooks/1446449034964238440/jUULaeSlj60FD19MupvrOPKqZd6DHd3b80PEwsvgKR4SYeUvSJfysKzShcgLVUgwB3vj', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'michael'
);

INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'nuarte', 'Nuarte atin', 'nuarte@example.com', NOW(), 'DEVOPS', 'https://discord.com/api/webhooks/1446449169538744371/mUVu24mBfs8j6M-ED-0GZXqhOg1w8HfKLBFDYAssag0CqG_6XTgwhCe31dv1g2RrJ_8K', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'nuarte'
);

-- design users
INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'sophie', 'Sophie Andrea', 'sophie@example.com', NOW(), 'DESIGN', 'https://discord.com/api/webhooks/1446449285058007100/9h6qEZtokiwFpTpZ-BtNluBUE_hT5CXyAy2YxHk3nSJAc7FYtYK5ahZ4B68U-iVaJ6TT', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'sophie'
);

INSERT INTO users (username, full_name, email, created_at, domain, discord_webhook, is_active)
SELECT 'bob', 'bob thomas', 'bob@example.com', NOW(), 'DESIGN', 'https://discord.com/api/webhooks/1446449446060560466/YBy7KYNP7eCKpMYOHdjNMsrzGbR5wHpVN63MVMWHbKrRjKLQ_s0p3j7mWc-LZHfyqTWo', TRUE
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'bob'
);