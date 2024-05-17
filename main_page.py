import flet as ft
import sqlite3
import json

tables = ['Марки_и_модели', 'Характеристики_автомобилей', 'Дополнительные_опции_и_особенности']

new_records = {}


def delete_record_by_id(table_name, record_id):
    conn = sqlite3.connect('car_catalog.db')
    cur = conn.cursor()
    # Выполнение запроса на удаление записи
    cur.execute("DELETE FROM {} WHERE ID = ?".format(table_name), (record_id,))
    # Подтверждение изменений в базе данных
    conn.commit()
    # Закрытие соединения с базой данных
    conn.close()


def get_all_ids(table_name):
    conn = sqlite3.connect('car_catalog.db')
    cur = conn.cursor()
    # Выполнение запроса для выбора всех ID из таблицы
    cur.execute("SELECT ID FROM {}".format(table_name))
    # Получение результатов запроса
    ids = cur.fetchall()
    # Закрытие соединения с базой данных
    conn.close()
    # Возвращение списка ID
    return ids


def get_all_ids_pro(table):
    print(table)
    return 14


def add_record(table_name, data):
    conn = sqlite3.connect('car_catalog.db')
    cur = conn.cursor()
    # Выполнение запроса на добавление записи
    questions = ', '.join(['?'] * len(data))
    print(questions)
    cur.execute(f"INSERT INTO {table_name} VALUES ({questions})", data)
    # Подтверждение изменений в базе данных
    conn.commit()
    # Закрытие соединения с базой данных
    conn.close()


def update_record(table_name, record_id, new_data):
    conn = sqlite3.connect('car_catalog.db')
    cur = conn.cursor()
    # Выполнение запроса на обновление записи
    cur.execute("UPDATE {} SET Марка = ?, Модель = ? WHERE ID = ?".format(table_name), (*new_data, record_id))
    # Подтверждение изменений в базе данных
    conn.commit()
    # Закрытие соединения с базой данных
    conn.close()


def get_column_count(table_name):
    conn = sqlite3.connect('car_catalog.db')
    cur = conn.cursor()
    # Выполнение запроса на получение информации о столбцах таблицы
    cur.execute("PRAGMA table_info({})".format(table_name))
    # Получение результатов запроса и подсчет количества строк
    column_count = len(cur.fetchall())
    # Закрытие соединения с базой данных
    conn.close()
    # Возвращение количества столбцов
    return column_count


# Функция для чтения настроек
def read_settings():
    with open('settings.json', 'r') as f:
        settings_file = json.load(f)
        return settings_file


# Функция для записи настроек
def write_settings(id, new_value):
    with open('settings.json', 'r') as f:
        settings_file = json.load(f)
        settings_file[id] = new_value
        with open('settings.json', 'w') as w:
            json.dump(settings_file, w, indent=4, ensure_ascii=False)


# Функция для получения названий столбцов
def get_column_names(table_name):
    conn = sqlite3.connect('car_catalog.db')
    cur = conn.cursor()
    cur.execute("PRAGMA table_info({})".format(table_name))
    columns = [row[1] for row in cur.fetchall()]
    conn.close()
    return columns


# Функция для получения всех строк таблицы
def get_table_rows(table_name):
    conn = sqlite3.connect('car_catalog.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(table_name))
    rows = cur.fetchall()
    conn.close()
    return rows


# Функция для заполнения заголовков таблиц
def datatable_column_fill(table_name):
    columns = get_column_names(table_name)
    return [ft.DataColumn(ft.Text(columns[i])) for i in range(len(columns))]


# Функция для заполнения строк таблиц
def datatable_row_fill(table_name):
    rows = get_table_rows(table_name)
    return [ft.DataRow(cells=[ft.DataCell(
        ft.TextField(
            value=str(row[i]),
            read_only=True,
            border=ft.InputBorder.NONE,
            expand=True,
        ),
    )
        for i in range(len(row))]) for row in rows]


table_1 = ft.DataTable(
    columns=datatable_column_fill('Марки_и_модели'),
    rows=datatable_row_fill('Марки_и_модели'),
    width=1300,
    vertical_lines=ft.BorderSide(width=1, color=ft.colors.OUTLINE_VARIANT),
    show_checkbox_column=True,
    data=None,
)

table_2 = ft.DataTable(
    columns=datatable_column_fill('Характеристики_автомобилей'),
    rows=datatable_row_fill('Характеристики_автомобилей'),
    width=1800,
    vertical_lines=ft.BorderSide(width=1, color=ft.colors.OUTLINE_VARIANT),
    data=None,
)

table_3 = ft.DataTable(
    columns=datatable_column_fill('Дополнительные_опции_и_особенности'),
    rows=datatable_row_fill('Дополнительные_опции_и_особенности'),
    width=1300,
    vertical_lines=ft.BorderSide(width=1, color=ft.colors.OUTLINE_VARIANT),
    data=None,
)


def table_select_on_change(e):
    match int(str(e.control.selected)[2:3]):
        case 0:
            datatable_container.content.controls[0] = table_1
        case 1:
            datatable_container.content.controls[0] = table_2
            if AutoExpandSwitch.value is True:
                e.page.window_width = 1800
                e.page.window_center()
                page_update(e.page)
        case 2:
            datatable_container.content.controls[0] = table_3
    datatable_container.update()
    if int(str(e.control.selected)[2:3]) != 1 and AutoExpandSwitch.value is True:
        e.page.window_width = 1300
        e.page.window_center()
        page_update(e.page)


def add_record_on_click(e):
    current_table = [table_1, table_2, table_3][int(str(table_select.selected)[2:3])]
    match int(str(table_select.selected)[2:3]):
        case 0:
            print('Марки и модели')
        case 1:
            print('Характеристики автомобилей')
        case 2:
            print('Дополнительные опции')

    print(current_table)

    table = get_all_ids(tables[int(str(table_select.selected)[2:3])])
    if current_table.data is None:
        fixed = max([int(str(x)[1:-2]) for x in table])
        current_table.data = fixed + 1
    else:
        fixed = current_table.data
        current_table.data = fixed + 1
    # another_max_id = get_all_ids_pro(current_table)

    new_row = ft.DataRow(cells=[])
    number_of_colums = get_column_count(tables[int(str(table_select.selected)[2:3])])
    for i in range(number_of_colums):
        new_cell = ft.DataCell(
            ft.TextField(
                value=str(fixed + 1) if i == 0 else '',
                read_only=False,
                border=ft.InputBorder.NONE,
                expand=True,

            ),
        )
        new_row.cells.append(new_cell)
    # current_table.rows.append(new_row)
    [table_1, table_2, table_3][int(str(table_select.selected)[2:3])].rows.append(new_row)
    e.page.update()

    global new_records
    new_records[tables[int(str(table_select.selected)[2:3])]] = \
        ([table_1, table_2, table_3][int(str(table_select.selected)[2:3])].rows[-1])
    # [print(new_records[-1].cells[_].content, sep='\n') for _ in range(number_of_colums)]
    # print('__' * 20)


def save_records(e):
    global new_records
    if new_records:
        for key, value in new_records.items():
            data = []
            for i in range(len(value.cells)):
                print(value.cells[i].content.value)
                data.append(f'{value.cells[i].content.value}')
            print(20*'-')
            print(tuple(data))
            print(key)
            add_record(key, tuple(data))
    e.page.update()
    new_records = {}
    refresh_db(first=True, second=True, third=True)


def switch_on_change(e):
    if e.control.value is True:
        e.page.window_width = 1800
    else:
        e.page.window_width = 1300
    e.page.window_center()
    page_update(e.page)


def textfield_delete_on_change(e):
    if e.control.value != '':
        table = get_all_ids(tables[int(str(table_select.selected)[2:3])])
        fixed = [int(str(x)[1:-2]) for x in table]
        print(fixed, int(e.control.value), table_select.selected)
        if min(fixed) <= int(e.control.value) <= max(fixed):
            delete_row_button.disabled = False
            delete_row_button.mouse_cursor = ft.MouseCursor.CLICK
        else:
            delete_row_button.disabled = True
            delete_row_button.mouse_cursor = ft.MouseCursor.NO_DROP
    else:
        delete_row_button.disabled = True
        delete_row_button.mouse_cursor = ft.MouseCursor.NO_DROP
    e.page.update()


def delete_row(e):
    delete_record_by_id(tables[int(str(table_select.selected)[2:3])], textfield_delete.value)
    refresh_db(int(str(table_select.selected)[2:3]))
    textfield_delete.value = ''
    page_update(e.page)


dbpage = ft.Container(
    content=ft.Column(
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    table_select := ft.SegmentedButton(
                        segments=[
                            ft.Segment(
                                value='0',
                                label=ft.Text(
                                    'Марки и модели',
                                    weight=ft.FontWeight.NORMAL,
                                    size=16
                                )
                            ),
                            ft.Segment(
                                value='1',
                                label=ft.Text(
                                    'Характеристики автомобилей',
                                    weight=ft.FontWeight.NORMAL,
                                    size=16
                                )
                            ),
                            ft.Segment(
                                value='2',
                                label=ft.Text(
                                    'Дополнительные опции',
                                    weight=ft.FontWeight.NORMAL,
                                    size=16
                                )
                            )
                        ],
                        selected={'0'},
                        show_selected_icon=False,
                        on_change=table_select_on_change
                    ),
                    save_button := ft.FilledButton(
                        'Сохранить',
                        icon=ft.icons.SAVE_ROUNDED,
                        on_click=save_records
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
            ft.Divider(
                height=10,
                thickness=1,
                color=ft.colors.TRANSPARENT
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                'Добавить запись',
                                icon=ft.icons.ADD_ROUNDED,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(
                                        radius=10,
                                    ),
                                ),
                                on_click=add_record_on_click
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Text('Введите ID:', style=ft.TextThemeStyle.LABEL_MEDIUM, size=16),
                                        ft.VerticalDivider(width=10, color=ft.colors.TRANSPARENT),
                                        textfield_delete := ft.TextField(
                                            # hint_text='Введите ID',
                                            border=ft.InputBorder.NONE,
                                            width=50,
                                            on_change=textfield_delete_on_change,
                                            input_filter=ft.NumbersOnlyInputFilter()
                                        ),
                                        delete_row_button := ft.IconButton(
                                            icon=ft.icons.DELETE_ROUNDED,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=10,
                                                ),
                                                color=ft.colors.ERROR,
                                            ),
                                            disabled=True,
                                            on_click=delete_row,
                                            mouse_cursor=ft.MouseCursor.NO_DROP
                                        )
                                    ],
                                    spacing=0,

                                ),
                                border=ft.border.only(bottom=ft.BorderSide(2, ft.colors.OUTLINE_VARIANT)),
                                padding=ft.padding.only(left=1),
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        'Разрешить редактирование:',
                                        size=16,
                                        style=ft.TextThemeStyle.LABEL_MEDIUM
                                    ),
                                    ft.Switch(
                                        value=False
                                    )
                                ]
                            )

                        ],
                        spacing=60,
                    ),
                    ft.Row(
                        controls=[
                            window_extension_switch_text := ft.Text(
                                'Расширить окно:',
                                size=16,
                                style=ft.TextThemeStyle.LABEL_MEDIUM,
                                color=ft.colors.ON_SURFACE
                            ),
                            window_extension_switch := ft.Switch(
                                on_change=switch_on_change,
                            ),
                        ]
                    )

                ],
                spacing=20
            ),
            ft.Divider(
                height=10,
                thickness=1,
                color=ft.colors.TRANSPARENT
            ),
            datatable_container := ft.Container(
                padding=0,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        table_1
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True,
                    # width=99999
                ),
                expand=True,
                alignment=ft.alignment.top_center,
                # border=ft.border.all(2, ft.colors.BLACK)
            )
        ],
        expand=True,
        # scroll=ft.ScrollMode.HIDDEN
    ),
    padding=20,
    expand=True,
)


def refresh_db(number=None, first=False, second=False, third=False):
    match number:
        case 0:
            table_1.rows = datatable_row_fill('Марки_и_модели')
            return True
        case 1:
            table_2.rows = datatable_row_fill('Характеристики_автомобилей')
            return True
        case 2:
            table_3.rows = datatable_row_fill('Дополнительные_опции_и_особенности')
            return True

    if first:
        table_1.rows = datatable_row_fill('Марки_и_модели')
    if second:
        table_2.rows = datatable_row_fill('Характеристики_автомобилей')
    if third:
        table_3.rows = datatable_row_fill('Дополнительные_опции_и_особенности')


queries = ft.Container(
    content=ft.Text('Запросы')
)


def change_theme(e):
    e.page.theme_mode = e.page.theme_mode.LIGHT \
        if e.page.theme_mode == e.page.theme_mode.DARK \
        else e.page.theme_mode.DARK
    e.control.selected = True if e.control.selected is False else False
    page_update(e.page)


def auto_expand_switch_on_change(e):
    if e.control.value is True:
        write_settings("AutoWindowExtension", True)
        window_extension_switch.disabled = True
        window_extension_switch_text.color = ft.colors.ON_SURFACE_VARIANT
    else:
        write_settings("AutoWindowExtension", False)
        window_extension_switch.disabled = False
        window_extension_switch_text.color = ft.colors.ON_SURFACE
    page_update(e.page)


settings = ft.Container(
    content=ft.Column(
        controls=[
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    'Сменить тему:',
                                    size=18
                                ),
                                theme_button := ft.IconButton(
                                    icon=ft.icons.DARK_MODE_ROUNDED,
                                    selected_icon=ft.icons.LIGHT_MODE_ROUNDED,
                                    on_click=change_theme,
                                )
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=10
                    ),
                    variant=ft.CardVariant.ELEVATED,
                    show_border_on_foreground=True,
                    is_semantic_container=True,
                    scale=1,
                ),
                width=200
            ),
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    'Автоматическое расширение окна при открытии 2-ой (широкой) таблицы:\n',
                                    spans=[
                                        ft.TextSpan(
                                            'P.S. При этом, переключатель ручного расширения окна будет отключен',
                                            style=ft.TextStyle(size=16, color=ft.colors.ON_SURFACE_VARIANT)
                                        )
                                    ],
                                    size=18
                                ),
                                AutoExpandSwitch := ft.Switch(
                                    on_change=auto_expand_switch_on_change
                                )
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=10
                    ),
                    variant=ft.CardVariant.ELEVATED,
                    show_border_on_foreground=True,
                    is_semantic_container=True,
                    scale=1,
                ),
                width=750
            )
        ]
    ),
    padding=20
)

helppage = ft.Container(
    content=ft.Text('Помощь')
)

baseform = ft.Container(
    padding=ft.padding.only(right=10),
    content=dbpage,
    expand=True
)


def page_update(p: ft.Page):
    p.update()


def logout(e):
    if e.page.window_width != 1300:
        e.page.window_width = 1300
        e.page.window_center()
        window_extension_switch.value = False
        page_update(e.page)
    print('Logout')
    e.page.clean()
    e.page.go('/')


usertab = ft.Column(
    [
        ft.Divider(),
        ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            user_type_text := ft.Text(
                                'User Type',
                                style=ft.TextThemeStyle.TITLE_SMALL,
                                size=18
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.icons.LOGOUT_ROUNDED,
                        icon_color=ft.colors.RED_700,
                        on_click=logout
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=20
            ),
            padding=ft.padding.only(
                left=15,
                # top=30,
                right=10
            ),
            expand=True
        )
    ],
    height=150,

)


def on_change_rail(e):
    match e.control.selected_index:
        case 0:
            baseform.content = dbpage
            print('Выбрана база данных')
        case 1:
            baseform.content = queries
            print('Выбраны запросы')
        case 2:
            baseform.content = settings
            print('Выбраны настройки')
        case 3:
            baseform.content = helppage
            print('Выбрана помощь')
    page_update(e.page)


NavRail = ft.NavigationRail(
    destinations=[
        ft.NavigationRailDestination(
            label_content=ft.Text(
                'База данных',
                color=ft.colors.ON_BACKGROUND
            ),
            icon=ft.icons.DATASET_OUTLINED,
            selected_icon=ft.icons.DATASET,
            padding=40
        ),
        ft.NavigationRailDestination(
            label_content=ft.Text(
                'Запросы',
                color=ft.colors.ON_BACKGROUND
            ),
            icon=ft.icons.TABLE_ROWS_OUTLINED,
            selected_icon=ft.icons.TABLE_ROWS_ROUNDED,
            padding=40,
        ),
        ft.NavigationRailDestination(
            label_content=ft.Text(
                'Настройки',
                color=ft.colors.ON_BACKGROUND
            ),
            icon=ft.icons.SETTINGS_OUTLINED,
            selected_icon=ft.icons.SETTINGS,
            padding=40
        ),
        ft.NavigationRailDestination(
            label_content=ft.Text(
                'Справка',
                color=ft.colors.ON_BACKGROUND
            ),
            icon=ft.icons.HELP_OUTLINE_ROUNDED,
            selected_icon=ft.icons.HELP_ROUNDED,
            padding=40
        )
    ],
    selected_index=0,
    label_type=ft.NavigationRailLabelType.SELECTED,
    bgcolor=ft.colors.TRANSPARENT,
    trailing=usertab,
    width=200,
    on_change=on_change_rail,
    unselected_label_text_style=ft.TextStyle(
        size=18
    ),
    selected_label_text_style=ft.TextStyle(
        size=18
    ),
    # indicator_color=ft.colors.TRANSPARENT,
    leading=ft.Column(
        [
            ft.Container(
                # height=70,
                content=ft.Text(
                    'Простая СУБД',
                    # style=ft.TextThemeStyle.TITLE_LARGE,
                    size=20
                ),
                alignment=ft.alignment.center,
                expand=True
            ),
            ft.Divider()
        ],
        height=70
    )
)

main_container = ft.Container(
    content=ft.Row(
        [
            NavRail,
            ft.VerticalDivider(
                width=0,
                thickness=1,

            ),
            ft.VerticalDivider(
                width=10,
                color=ft.colors.TRANSPARENT
            ),
            baseform
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=0
    ),
    expand=True,
)


def execute_settings():
    all_settings = read_settings()
    if all_settings["AutoWindowExtension"] is True:
        AutoExpandSwitch.value = True
        window_extension_switch.disabled = True
        window_extension_switch_text.color = ft.colors.ON_SURFACE_VARIANT
    else:
        AutoExpandSwitch.value = False
        window_extension_switch.disabled = False
        window_extension_switch_text.color = ft.colors.ON_SURFACE


def _view_(login_type='guest') -> ft.View:
    execute_settings()
    user_type_text.value = {'guest': 'Гость', 'admin': 'Админ', 'user': 'Пользователь'}[
        login_type]
    NavRail.selected_index = 0
    baseform.content = dbpage
    table_select.selected = {'0'}
    refresh_db(True, True, True)

    if login_type == 'admin':
        return ft.View(
            "/main_page_admin",
            [
                main_container
            ],
            padding=0
        )
    if login_type == 'user':
        return ft.View(
            "/main_page_user",
            [
                main_container
            ],
            padding=0
        )
    return ft.View(
        "/main_page_guest",
        [
            main_container
        ],
        padding=0
    )
