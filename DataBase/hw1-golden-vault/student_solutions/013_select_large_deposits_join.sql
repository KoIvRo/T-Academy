-- Задание 013: Выбрать имена клиентов и вес депозитов больше 500 грамм

-- Напишите ваше решение ниже:

SELECT clients.full_name, weight_g FROM gold_deposits JOIN clients ON clients.id = client_id WHERE weight_g > 500;