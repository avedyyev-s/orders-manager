from orders_manager import get_all_orders, add_order, get_total_revenue, delete_order_by_id, search_orders, save_backup, load_backup

title_menu = "---Меню---"
show_all_orders = "1. Показать все заказы"
add_new_order = "2. Добавить новый заказ"
show_total_revenue = "3. Показать общую выручку"
delete_order = "4. Удалить заказ по ID"
find_order = "5. Поиск заказа"
create_backup = "6. Создать резервную копию базы"
restore_backup = "7. Восстановить базу из резервной копии"
exit_in_program = "8. Выйти из программы"

while True:
    print(title_menu, show_all_orders, add_new_order, show_total_revenue, delete_order, find_order, create_backup, restore_backup, exit_in_program, sep='\n')
    choice = input("Выберите пункт: ")
    if choice == "1":
        for order in get_all_orders():
            print(f'[ID {order["id"]}] Клиент: {order["client"]} | Сумма заказа: {order["price"]} руб.')
    elif choice == "2":
        name_client = input("Введите имя клиента: ")
        while True:
            try:
                revenue_client = int(input("Введите сумму заказа: "))
                break
            except ValueError:
                print("Ошибка! Нужно ввести именно цифры. Попробуйте еще раз пожалуйста.")
        if add_order(name_client, revenue_client):
            print("Заказ успешно добавлен!")
        else:
            print("Имя не может быть пустым или сумма отрицательным! Попробуйте еще раз!")
    elif choice == "3":
        print(f"Выручка состваляет {get_total_revenue()} руб.")
    elif choice == "4":
        while True:
            try:
                delete_order_id = int(input("Введите ID заказа который хотите удалить: "))
                if delete_order_by_id(delete_order_id):
                    print("Ваш заказ успешно удален!")
                    break
                else:
                    print("Заказ с данным ID не найден")
            except ValueError:
                print("Пожалуйста введите ID цифрами")
    elif choice == "5":
        user_search = input("Поиск по ID или по имени: ")
        result_search = search_orders(user_search)
        if len(result_search) == 0:
            print("Ничего не найдено")
        else:
            for result in result_search:
                print(f"ID: {result['id']} | Клиент: {result['client']} | Сумма заказа: {result['price']} руб.")
    elif choice == "6":
        if save_backup():
            print("Резервная копия успешно создана в файле orders_backup.json!")
        else:
            print("Произошла ошибка! Попробуйте еще раз.")
    elif choice == "7":
        if load_backup():
            print("База данных успешно восстановлена!")
        else:
            print("Ошибка! Файл резервной копии не найден.")
    elif choice == "8":
        print("Успешно вышли из программы!")
        break
    else:
        print("Неверный пункт меню! Попробуйте снова.")
