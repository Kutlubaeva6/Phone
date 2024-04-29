import sqlite3 as sl

def menu(conn):
    while True:
        print('Меню')
        user_choice = input('1 - Импортировать данные\n2 - Найти контакт\n3 - Добавить контакт\n\
4 - Изменить контакт\n5 - Удалить контакт\n6 - Список контактов\n0 - Выход\n')
        print()
        if user_choice == '1':
            file_to_add = input('Введите название файла: ')
            import_data(file_to_add, conn)
        elif user_choice == '2':
            find(conn)
        elif user_choice == '3':
            add(conn)
        elif user_choice == '4':
            change(conn)
        elif user_choice == '5':
            delete(conn)
        elif user_choice == '6':
            show(conn)
        elif user_choice == '0':
            print('Выход')
            break
        else:
            print('Неправильно выбрана команда')
            print()
            continue
        conn.commit()


def import_data(file_to_add, conn):
    try:
        with open(file_to_add, 'r', encoding='utf-8') as new_contacts:

            contacts_to_add = new_contacts.readlines()
            for line in contacts_to_add:
                c = conn.cursor()
                c.execute(f'INSERT INTO phone(фамилия, имя, номер) VALUES(?, ?, ?);', line.split())
    except FileNotFoundError:
        print(f'{file_to_add} не найден')

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    headers = ['Фамилия', 'Имя', 'Номер телефона']
    contact_list = []
    for line in lines:
        line = line.strip().split()
        contact_list.append(dict(zip(headers, line)))
    return contact_list


def search_parameters():
    print('Поиск')
    search_field = input('1 - фамилия\n2 - имя\n3 - телефон\n')
    print()
    search_value = None
    if search_field == '1':
        search_value = input('Введите фамилию: ')
        print()
    elif search_field == '2':
        search_value = input('Введите имя: ')
        print()
    elif search_field == '3':
        search_value = int(input('Введите номер: '))
        print()
    return search_field, search_value


def find(conn):
    search_field, search_value = search_parameters()
    search_fields_dict = {'1': 'фамилия', '2': 'имя', '3': 'номер'}
    found_contacts = []
    c = conn.cursor()
    c.execute(f'SELECT фамилия, имя, номер FROM phone WHERE {search_fields_dict[search_field]} = "{search_value}";')
    for line in c.fetchall():
        found_contacts.append({key: value for key, value in zip(['Фамилия', 'Имя', 'Номер'], line)})
    if len(found_contacts) == 0:
        print('Контакт не найден!')
    else:
        print_contacts(found_contacts)
    print()


def get_new():
    last_name = input('Фамилия: ')
    first_name = input('Имя: ')
    phone_number = int(input('Телефон: '))
    return last_name, first_name, phone_number


def add(conn):
    c = conn.cursor()
    c.execute(f'INSERT INTO phone(фамилия, имя, номер) VALUES(?, ?, ?);', get_new())
    conn.commit()


def show(conn):
    print(f'Фамилия{" " * (20 - len("Фамилия"))}Имя{" " * (20 - len("Имя"))}Номер')
    c = conn.cursor()
    c.execute('SELECT * FROM phone ORDER BY фамилия')
    for line in c.fetchall():
        print(f'{line[0]:20}{line[1]:20}{line[2]:12}')
    print()


def search_to_modify(conn):
    search_field, search_value = search_parameters()
    search_fields_dict = {'1': 'фамилия', '2': 'имя', '3': 'номер'}
    search_result = []
    c = conn.execute(f'SELECT * FROM phone WHERE {search_fields_dict[search_field]} = "{search_value}";')
    for line in c.fetchall():
        search_result.append({key: value for key, value in zip(['Фамилия', 'Имя', 'Номер'], line)})
    if len(search_result) == 1:
        return search_result[0]
    elif len(search_result) > 1:
        print('Какой из контактов?')
        for i in range(len(search_result)):
            print(f'{i + 1} - {search_result[i]}')
        num_count = int(input('Выберите контакт, который нужно изменить/удалить: '))
        return search_result[num_count - 1]
    else:
        print('Контакт не найден')
    print()


def change(conn):
    number_to_change = search_to_modify(conn)
    number_to_change_old = number_to_change.copy()
    print('Что изменить?')
    field = input('1 - Фамилия\n2 - Имя\n3 - Номер телефона\n')
    if field == '1':
        number_to_change['Фамилия'] = input('Новая фамилия: ')
    elif field == '2':
        number_to_change['Имя'] = input('Новое имя: ')
    elif field == '3':
        number_to_change['Номер'] = input('Новый номер телефона: ')
    c = conn.cursor()
    c.execute(f'''UPDATE phone 
              SET имя = '{number_to_change['Имя']}', фамилия = '{number_to_change['Фамилия']}', номер = '{number_to_change['Номер']}'
              WHERE имя = '{number_to_change_old['Имя']}' 
                    AND фамилия = '{number_to_change_old['Фамилия']}' 
                    AND номер = '{number_to_change_old['Номер']}'
              
                    ''')


def delete(conn):
    number_to_change = search_to_modify(conn)
    c = conn.cursor()
    c.execute(f'''DELETE FROM phone WHERE
                        имя = '{number_to_change['Имя']}' AND фамилия = '{number_to_change['Фамилия']}' AND номер = '{number_to_change['Номер']}'
                ''')


def print_contacts(contact_list: list):
    for contact in contact_list:
        for key, value in contact.items():
            print(f'{key}: {value:12}', end='')
        print()


if __name__ == '__main__':

    conn = sl.connect(r'C:\Users\kutlu\OneDrive\Рабочий стол\python_att\proba.db', timeout=10)
    menu(conn)