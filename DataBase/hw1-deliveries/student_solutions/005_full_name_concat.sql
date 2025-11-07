-- Задание: Вывести полное имя клиента в формате 'Фамилия Имя' в поле full_name 
SELECT last_name || ' ' || first_name AS full_name FROM clients