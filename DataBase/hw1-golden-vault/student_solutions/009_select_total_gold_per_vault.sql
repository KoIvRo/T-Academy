-- Задание 009: Посчитать общий вес золота в каждом хранилище

-- Напишите ваше решение ниже:

SELECT vault_id, SUM(weight_g) AS total_weight FROM gold_deposits GROUP BY vault_id;