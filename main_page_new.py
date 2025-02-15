import flet as ft
import settings_module as sem
# from db_interact import *
import db_interact as dbi
import json
from encrypted_storage import EncryptedStorage
import sqlite3

from main_page import NavRail

print('Запуск main_page_new.py')
storage = EncryptedStorage()
db_manager = dbi.DatabaseManager(storage.load_data()['db_info']['db_path'])

new_records = {}
edited_records = {}


# datatables = [ft.Control()]  # временное решение до заполнения списка


def db_manager_create():
    global db_manager
    db_manager = dbi.DatabaseManager(storage.load_data()['db_info']['db_path'])
    print(db_manager.get_table_names())


def datacell_on_change(e):
    print('value:', e.control.value)
    print('data:', e.control.data)
    column = db_manager.get_column_names(e.control.data["table"])[int(e.control.data["column"])]

    if e.control.value != e.control.data["verified_value"]:
        new_value = e.control.value
        if edited_records.get(e.control.data["ID"]):
            edited_records[e.control.data["ID"]]["new_value"][column] = new_value
            print('Значения изменились')
        else:
            edited_records[e.control.data["ID"]] = {
                # "ID": e.control.data["ID"],
                "table": e.control.data["table"],
                "new_value": {
                    column: new_value,
                }
            }
            print('Запись создана')
    else:
        edited_records[e.control.data["ID"]]["new_value"].pop(column)
        print('Значения не изменились')
    if edited_records[e.control.data["ID"]]["new_value"] == {}:
        edited_records.pop(e.control.data["ID"])
    print('\nТекущие измененные значения:', edited_records, end='\n')


def datatable_column_fill(table_name):
    columns = db_manager.get_column_names(table_name)
    return [ft.DataColumn(ft.Text(columns[i])) for i in range(len(columns))]


# Функция для заполнения строк таблиц
def datatable_row_fill(table_name):
    rows = db_manager.get_table_rows(table_name)
    return [ft.DataRow(cells=[ft.DataCell(
        ft.TextField(
            value=str(row[i]),
            read_only=True,
            border=ft.InputBorder.NONE,
            expand=True,
            on_change=datacell_on_change,
            data={
                "ID": str(row[0]),
                "column": str(i),
                "row": row,
                "table": str(table_name),
                "verified_value": str(row[i])
            },
            key=str(row[0]) if i == 0 else None
        ),
    )
        for i in range(len(row))]) for row in rows]


def create_datatables():
    temp_datatables = []
    table_names = db_manager.get_table_names()
    for i in range(len(table_names)):
        temp_datatables.append(
            ft.DataTable(
                columns=datatable_column_fill(table_names[i]),
                rows=datatable_row_fill(table_names[i]),
                width=1300,
                vertical_lines=ft.BorderSide(width=1, color=ft.colors.OUTLINE_VARIANT),
                # data=f'table_{i + 1}',
                data={
                    'data': None,
                    'table_name': table_names[i]
                }
            )
        )
    return temp_datatables


datatables = create_datatables()
for i in datatables:
    print(i.data['table_name'])


def create_table_select():
    temp_list = []
    table_names = db_manager.get_table_names()
    for i in range(len(table_names)):
        temp_list.append(
            ft.Segment(
                value=f'{i}',
                label=ft.Text(
                    f'{table_names[i]}',
                    weight=ft.FontWeight.NORMAL,
                    size=16
                )
            )
        )
    return temp_list


def table_select_on_change(e):
    datatable_container.content.controls[0] = datatables[int(str(e.control.selected)[2:3])]
    datatable_container.update()


def update_button_on_click(e):
    print('update_button_on_click')
    # refresh_db(number=int(str(table_select.selected)[2:3]))
    refresh_db(everything=True)
    if edit_row_switch.value is True:
        allow_rows_editing(True)
    else:
        allow_rows_editing(False)
    e.page.update()


def save_records(e):
    global new_records
    if new_records:
        for key, value in new_records.items():
            data = []
            for i in range(len(value.cells)):
                print(value.cells[i].content.value)
                data.append(f'{value.cells[i].content.value}')
            print(20 * '-')
            print(tuple(data))
            print(f'key: {key}')
            db_manager.add_record(key, tuple(data))
    if edited_records:
        for key, value in edited_records.items():
            print(key, value)
            db_manager.update_record(
                value["table"],
                int(key),
                value["new_value"]
            )

    e.page.update()
    new_records.clear()
    edited_records.clear()
    refresh_db(everything=True)
    if edit_row_switch.value is True:
        allow_rows_editing(True)
    else:
        allow_rows_editing(False)

    e.page.update()


def add_record_on_click(e):
    current_table = datatables[int(str(table_select.selected)[2:3])]
    # match int(str(table_select.selected)[2:3]):
    #     case 0:
    #         print('Марки и модели')
    #     case 1:
    #         print('Характеристики автомобилей')
    #     case 2:
    #         print('Дополнительные опции')

    print(f'{current_table}')

    table = db_manager.get_all_ids(db_manager.get_table_names()[int(str(table_select.selected)[2:3])])
    print(f'\ntable: {table}\n')
    print(max([int(str(x)[1:-2]) for x in table]))
    if current_table.data['data'] is None:
        fixed = max([int(str(x)[1:-2]) for x in table])
        print(fixed)
        current_table.data['data'] = int(fixed) + 1
    else:
        fixed = current_table.data['data']
        print(fixed)  # <table_1> as example
        current_table.data['data'] = int(fixed) + 1
    # another_max_id = get_all_ids_pro(current_table)

    new_row = ft.DataRow(cells=[])
    number_of_colums = db_manager.get_column_count(db_manager.get_table_names()[int(str(table_select.selected)[2:3])])
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
    datatables[int(str(table_select.selected)[2:3])].rows.append(new_row)
    datatable_container.content.scroll_to(offset=-1, duration=1000)
    e.page.update()

    global new_records
    new_records[current_table.data['table_name']] = \
        (datatables[int(str(table_select.selected)[2:3])].rows[-1])
    print(f'\nnew_records: \n{new_records}\n')
    print(table_select.selected)
    # [print(new_records[-1].cells[_].content, sep='\n') for _ in range(number_of_colums)]
    # print('__' * 20)


def textfield_delete_on_change(e):
    if e.control.value != '':
        table = db_manager.get_all_ids(db_manager.get_table_names()[int(str(table_select.selected)[2:3])])
        fixed = [int(str(x)[1:-2]) for x in table]
        # print(fixed, int(e.control.value), table_select.selected)
        if int(e.control.value) in fixed:
            delete_row_button.disabled = False
            delete_row_button.mouse_cursor = ft.MouseCursor.CLICK
            datatable_container.content.scroll_to(key=e.control.value, duration=1000)
        else:
            delete_row_button.disabled = True
            delete_row_button.mouse_cursor = ft.MouseCursor.NO_DROP
            if int(e.control.value) > max(fixed):
                datatable_container.content.scroll_to(offset=-1, duration=1000)
    else:
        delete_row_button.disabled = True
        delete_row_button.mouse_cursor = ft.MouseCursor.NO_DROP
        datatable_container.content.scroll_to(offset=0, duration=1000)
    e.page.update()


def delete_row(e):
    db_manager.delete_record_by_id(db_manager.get_table_names()[int(str(table_select.selected)[2:3])], int(textfield_delete.value))
    refresh_db(int(str(table_select.selected)[2:3]))
    textfield_delete.value = ''
    page_update(e.page)


def allow_rows_editing(status=False):
    if status is True:
        for _ in datatables:
            for i in range(len(_.rows)):
                for j in range(len(_.rows[i].cells)):
                    _.rows[i].cells[j].content.read_only = False
    else:
        for _ in datatables:
            for i in range(len(_.rows)):
                for j in range(len(_.rows[i].cells)):
                    _.rows[i].cells[j].content.read_only = True


def edit_switch_on_change(e):
    if e.control.value is True:
        allow_rows_editing(True)
    else:
        allow_rows_editing(False)
    e.page.update()


def switch_on_change(e):
    if e.control.value is True:
        e.page.window.width = 1800
    else:
        e.page.window.width = 1300
    e.page.window.center()
    page_update(e.page)


# -----------------------------------------------------------------------------------

dbpage = ft.Container(
    content=ft.Column(
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.icons.REFRESH_ROUNDED,
                        tooltip='Обновить таблицу',
                        on_click=update_button_on_click
                    ),
                    table_select := ft.SegmentedButton(
                        segments=[
                            *create_table_select()
                        ],
                        selected={'0'},
                        show_selected_icon=False,
                        on_change=table_select_on_change,
                        style=ft.ButtonStyle(
                            padding=15
                        ),

                    ),
                    save_button := ft.FilledButton(
                        'Сохранить',
                        icon=ft.icons.SAVE_ROUNDED,
                        on_click=save_records,
                        style=ft.ButtonStyle(
                            padding=16
                        )
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
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
                            add_record_button := ft.ElevatedButton(
                                'Добавить запись',
                                icon=ft.icons.ADD_ROUNDED,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(
                                        radius=10,
                                    ),
                                    padding=15
                                ),
                                on_click=add_record_on_click
                            ),
                            delete_con := ft.Container(
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
                            edit_row := ft.Row(
                                controls=[
                                    ft.Text(
                                        'Разрешить редактирование:',
                                        size=16,
                                        style=ft.TextThemeStyle.LABEL_MEDIUM
                                    ),
                                    edit_row_switch := ft.Switch(
                                        value=False,
                                        on_change=edit_switch_on_change
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
                        datatables[0]
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True,
                    auto_scroll=False
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


def refresh_db(number=None, everything=False):
    def update_table(num):
        try:
            datatables[num].update()
        except AssertionError as e:
            print('Cannot update table:', e)

    if number:
        datatables[number].rows = datatable_row_fill(db_manager.get_table_names()[number])
        update_table(number)
        return True

    if everything:
        table_names = db_manager.get_table_names()
        for i in range(len(table_names)):
            datatables[i].rows = datatable_row_fill(table_names[i])
            update_table(i)


# -----------------------------------------------------------------------------------

def read_queries():
    with open(f'{storage.load_data()["db_info"]["folder_path"]}queries.json', 'r', encoding='utf-8') as f:
        queries_file = json.load(f)
        return queries_file


def queries_dropdown_on_change(e):
    print('query changed')
    all_queries = read_queries()
    e.page.session.set('query', all_queries[queries_dropdown.value]['query'])
    e.page.session.set('query_full_info', all_queries[queries_dropdown.value])
    query_title.text = all_queries[queries_dropdown.value]['name']
    query_description.text = all_queries[queries_dropdown.value]['description']
    query_name.visible = True
    show_query_result_button.disabled = False
    parameter_input.value = ''
    show_query_info_button.disabled = False

    if all_queries[queries_dropdown.value]['type'] == 'with_input':
        parameter_input_container.visible = True
    else:
        parameter_input_container.visible = False

    # if queries_dropdown.value is not None:
    #     space_for_query_result.controls = [ft.Text(all_queries[queries_dropdown.value]['query'])]
    # else:
    #     space_for_query_result.controls = [ft.Text('Здесь будет результат запроса')]
    space_for_query_result.controls = [ft.Text('Здесь будет результат запроса')]

    queries.update()


def clear_queries_dropdown(e):
    queries_dropdown.value = None
    parameter_input.value = ''
    # query_name.visible = False
    query_title.text = 'Название запроса'
    query_description.text = 'Описание запроса'
    parameter_input.error_text = ''
    show_query_result_button.disabled = True
    parameter_input_container.visible = False
    show_query_info_button.disabled = True

    space_for_query_result.controls = [ft.Text('Здесь будет результат запроса')]
    queries.update()


def show_query_result(e):
    parameter_input.update()
    temp_query = e.page.session.get('query')
    # print('\nSelected query:', e.page.session.get('query'))
    if parameter_input.value != '':
        if '[INPUT]' in e.page.session.get('query'):
            # e.page.session.set('query', e.page.session.get('query').replace('[INPUT]', parameter_input.value))
            temp_query = e.page.session.get('query').replace('[INPUT]', parameter_input.value)
    else:
        parameter_input.error_text = 'Поле не может быть пустым'
    query_result = db_manager.execute_query(temp_query)
    print(f'\n{query_result}\n')
    columns = e.page.session.get('query_full_info')['columns']
    query_result_table.columns = [ft.DataColumn(ft.Text(columns[i])) for i in range(len(columns))]
    query_result_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(query_result[i][j]))
                                                 for j in range(len(columns))]) for i in range(len(query_result))]

    if len(columns) < 6:
        query_result_table.width = e.page.session.get('window_parameters')['width'] - 280
    else:
        # query_result_table.width = sum(len(i) for i in columns) * 15
        query_result_table.width = None

    space_for_query_result.controls = [
        query_result_table,
        ft.Divider(
            height=5,
        )
    ]
    queries.update()


query_result_table = ft.DataTable(
    columns=[],
    rows=[],
    # width=1300,
    vertical_lines=ft.BorderSide(width=1, color=ft.colors.OUTLINE_VARIANT),
    # show_checkbox_column=True,
    data=None,
)


def open_show_query_dialog(e):
    fill_query_info(e)
    e.page.dialog = show_query_info
    show_query_info.open = True
    e.page.update()


def close_show_query_dialog(e):
    show_query_info.open = False
    e.page.update()
    # query_help_name.value = 'data'
    # query_help_description.value = 'data'
    # query_help_query.value = 'data'
    # query_help_type.value = 'data'


def fill_query_info(e):
    query_full_info = e.page.session.get('query_full_info')
    query_keys = list(query_full_info.keys())
    query_values = list(query_full_info.values())
    print('\n', query_keys, '\n', query_values, '\n')
    if query_keys == ['query', 'name', 'description', 'type', 'columns']:
        localized_query_labels = ['Запрос', 'Название', 'Описание', 'Тип', 'Столбцы']
        new_query_full_info = {}
        for i in range(len(query_full_info.keys())):
            new_query_full_info[localized_query_labels[i]] = query_values[i]
        query_full_info = new_query_full_info
    print(query_full_info)
    info_list = []
    for key, value in query_full_info.items():
        if len(info_list) > 0:
            info_list.append(
                ft.Divider(
                    height=25,
                    thickness=1,
                    # color=ft.colors.TRANSPARENT
                )
            )
        info_list.append(
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Text(
                            key,
                            size=18,
                            style=ft.TextThemeStyle.LABEL_MEDIUM
                        ),
                        ft.Text(
                            value,
                            size=16,
                            # style=ft.TextThemeStyle.TITLE_MEDIUM,
                            selectable=True
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=0
            ),

        )

    show_query_info.content.controls = info_list


def copy_query(e):
    e.page.set_clipboard(
        str(e.page.session.get('query_full_info'))
    )
    e.page.update()


show_query_info = ft.AlertDialog(
    title=ft.Row(
        controls=[
            ft.Text('Информация о запросе'),
            ft.IconButton(ft.icons.CLOSE, on_click=close_show_query_dialog)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    ),
    content=ft.Column(
        controls=[

        ],
        spacing=50,
        width=400,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        height=500,
        scroll=ft.ScrollMode.ADAPTIVE,
    ),
    actions=[
        ft.TextButton(
            'Скопировать',
            on_click=copy_query,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    radius=ft.border_radius.all(10)
                )
            )
        )
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    # actions_overflow_button_spacing=0,
    shape=ft.RoundedRectangleBorder(
        radius=ft.border_radius.all(10)
    ),
    scrollable=True

)


def parameter_input_on_change(e):
    if parameter_input.value == '':
        parameter_input.error_text = 'Поле не может быть пустым'
    else:
        parameter_input.error_text = ''
    e.control.update()


# -----------------------------------------------------------------------------------

queries = ft.Container(
    content=ft.Column(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            'Запросы:',
                                            size=18,
                                            style=ft.TextThemeStyle.TITLE_MEDIUM
                                        ),
                                        queries_dropdown := ft.Dropdown(
                                            options=[
                                                ft.dropdown.Option(key='1', text='Запрос 1'),
                                                ft.dropdown.Option(key='2', text='Запрос 2'),
                                                ft.dropdown.Option(key='3', text='Запрос 3'),
                                                ft.dropdown.Option(key='4', text='Запрос 4'),
                                                ft.dropdown.Option(key='5', text='Запрос 5'),
                                                ft.dropdown.Option(key='6', text='Запрос 6'),
                                                ft.dropdown.Option(key='7', text='Запрос 7'),
                                                ft.dropdown.Option(key='8', text='Запрос 8'),
                                                ft.dropdown.Option(key='9', text='Запрос 9'),
                                                ft.dropdown.Option(key='10', text='Запрос 10'),
                                            ],
                                            hint_text='Выберите запрос',
                                            on_change=queries_dropdown_on_change
                                        ),
                                        clear_queries_dropdown_button := ft.IconButton(
                                            icon=ft.icons.CLEAR_ROUNDED,
                                            on_click=clear_queries_dropdown
                                        ),
                                        ft.VerticalDivider(
                                            thickness=1,
                                            width=20
                                        ),
                                        show_query_result_button := ft.ElevatedButton(
                                            text='Показать результат',
                                            icon=ft.icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=10
                                                )
                                            ),
                                            on_click=show_query_result,
                                            disabled=True
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.START
                                ),
                                ft.Row(
                                    controls=[
                                        show_query_info_button := ft.IconButton(
                                            icon=ft.icons.QUESTION_MARK_ROUNDED,
                                            tooltip='Информация о запросе',
                                            on_click=open_show_query_dialog,
                                            disabled=True
                                        )
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    query_name := ft.Text(
                                        expand=True,
                                        spans=[
                                            query_title := ft.TextSpan(
                                                text='Название запроса',
                                            ),
                                            ft.TextSpan(
                                                text=' — ',
                                            ),
                                            query_description := ft.TextSpan(
                                                text='Описание запроса',
                                            ),
                                        ]
                                    ),
                                ],
                                expand=False,
                            )
                        ),
                        parameter_input_container := ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        'Параметр запроса:',
                                        size=16,
                                        style=ft.TextThemeStyle.TITLE_MEDIUM,
                                    ),
                                    ft.VerticalDivider(
                                        thickness=1,
                                        width=20,
                                        color=ft.colors.OUTLINE_VARIANT
                                    ),
                                    parameter_input := ft.TextField(
                                        hint_text='Значение параметра',
                                        border=ft.InputBorder.NONE,
                                        # disabled=True,
                                        expand=True,
                                        text_size=14,
                                        hint_style=ft.TextStyle(
                                            weight=ft.FontWeight.NORMAL
                                        ),
                                        on_change=parameter_input_on_change,
                                        on_submit=show_query_result
                                    ),
                                ],
                                expand=False,
                            ),
                            border=ft.border.only(
                                bottom=ft.border.BorderSide(width=2, color=ft.colors.OUTLINE_VARIANT)
                            ),
                            width=420,
                            visible=False
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                border_radius=10,
                bgcolor=ft.colors.TRANSPARENT,
                padding=ft.padding.all(10),
            ),
            queries_container := ft.Container(
                padding=0,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        space_for_query_resulta := ft.Row(
                            controls=[
                                space_for_query_result := ft.Column(
                                    controls=[
                                        ft.Text(
                                            'Здесь будет результат запроса:',
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    # adaptive=True,

                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            # adaptive=True,

                        )
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True,
                    auto_scroll=False
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


def change_theme(e):
    if e.page.theme_mode == e.page.theme_mode.DARK:
        e.page.theme_mode = e.page.theme_mode.LIGHT
        e.control.selected = True
        sem.write_settings("PageTheme", "LIGHT")
    else:
        e.page.theme_mode = e.page.theme_mode.DARK
        sem.write_settings("PageTheme", "DARK")
        e.control.selected = False
    page_update(e.page)


def auto_expand_switch_on_change(e):
    if e.control.value is True:
        sem.write_settings("AutoWindowExtension", True)
        window_extension_switch.disabled = True
        window_extension_switch_text.color = ft.colors.ON_SURFACE_VARIANT
    else:
        sem.write_settings("AutoWindowExtension", False)
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
    content=ft.Column(
        controls=[
            ft.Text(
                'Простая СУБД | Simple DBMS',
                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                # size=22
            ),
            ft.Text(
                'Версия | Version 0.8.0',
                style=ft.TextThemeStyle.TITLE_MEDIUM,
                size=18
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        'Ссылка на GitHub | GitHub link',
                        style=ft.TextStyle(
                            color=ft.colors.BLUE,
                            size=18
                        ),
                        url='https://github.com/Shido-Itsuka/Simple-DBMS'
                    )
                ]
            ),
            ft.Divider(
                thickness=2,
                height=25,
                # color=ft.colors.TRANSPARENT,
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text='Copyright © 2024 | ',
                        style=ft.TextStyle(
                            size=16
                        )
                    ),
                    ft.TextSpan(
                        text='Shido-Itsuka',
                        style=ft.TextStyle(
                            color=ft.colors.BLUE,
                            size=16
                        ),
                        url='https://github.com/Shido-Itsuka'
                    ),
                    ft.TextSpan(
                        text=' | All rights reserved.',
                        style=ft.TextStyle(
                            size=16
                        )
                    )
                ],
                style=ft.TextThemeStyle.LABEL_LARGE
            )
        ],
        # expand=False,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=20
    ),
    padding=50,
)

baseform = ft.Container(
    padding=ft.padding.only(right=10),
    content=dbpage,
    expand=True
)


def page_update(p: ft.Page):
    p.update()


def logout(e):
    print('Logout')
    e.page.clean()
    e.page.go('/')
    # e.page.views.pop()
    e.page.update()


usertab = ft.Column(
    [
        # ft.Divider(),
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
            expand=True,
            # bgcolor=ft.Colors.DEEP_ORANGE_ACCENT
        )
    ],
    height=150,
    width=200
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
    trailing=ft.Divider(),
    width=200,
    expand=True,
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

NavRailContainer = ft.Container(
    content=ft.Column(
        controls=[
            NavRail,
            ft.Divider(
                thickness=1,

            ),
            usertab
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        # spacing=0
    ),
)

main_container = ft.Container(
    content=ft.Row(
        [
            NavRailContainer,
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
    all_settings = sem.read_settings()
    if all_settings["AutoWindowExtension"] is True:
        AutoExpandSwitch.value = True
        window_extension_switch.disabled = True
        window_extension_switch_text.color = ft.colors.ON_SURFACE_VARIANT
    else:
        AutoExpandSwitch.value = False
        window_extension_switch.disabled = False
        window_extension_switch_text.color = ft.colors.ON_SURFACE

    if all_settings["PageTheme"] == "LIGHT":
        theme_button.selected = True
    else:
        theme_button.selected = False


# -----------------------------------------------------------------------------------

def _view_(login_type='guest') -> ft.View:
    global datatables
    global storage
    execute_settings()
    storage = EncryptedStorage()
    db_manager_create()
    datatables = create_datatables()
    create_table_select()
    user_type_text.value = {'guest': 'Гость', 'admin': 'Админ', 'user': 'Пользователь'}[
        login_type]
    NavRail.selected_index = 0
    baseform.content = dbpage
    table_select.selected = {'0'}
    datatable_container.content.controls[0] = datatables[0]
    textfield_delete.value = ''
    edit_row_switch.value = False
    allow_rows_editing(False)
    refresh_db(everything=True)
    print('login_type:', login_type)
    match login_type:
        case 'admin':
            add_record_button.visible = True
            delete_con.visible = True
            edit_row.visible = True
            save_button.visible = True
            print('admin')
        case 'user':
            add_record_button.visible = True
            save_button.visible = True
            edit_row.visible = False
            delete_con.visible = False
            print('user')
        case 'guest':
            add_record_button.visible = False
            delete_con.visible = False
            edit_row.visible = False
            save_button.visible = False
            print('guest')

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
        padding=0,

    )
