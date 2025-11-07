-- Задание 010: Выбрать имя клиента и вес его депозитов

-- Напишите ваше решение ниже:

SELECT clients.full_name, weight_g FROM gold_deposits JOIN clients ON clients.id = client_id;