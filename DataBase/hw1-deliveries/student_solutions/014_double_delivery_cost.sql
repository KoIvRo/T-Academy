-- Задание: Вывести имена клиентов и удвоенную стоимость их доставок
SELECT clients.first_name, deliveries.delivery_cost * 2 FROM deliveries JOIN clients ON clients.id=deliveries.client_id