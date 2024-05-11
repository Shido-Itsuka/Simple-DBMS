import flet as ft

dbpage = ft.Container(
    content=ft.Text('Database Page')
)

queries = ft.Container(
    content=ft.Text('Queries')
)

settings = ft.Container(
    content=ft.Text('Settings')
)

baseform = ft.Container(
    padding=0,
    content=dbpage
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


NavRail = ft.Container(
    content=ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(
                    'База данных',
                )
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    ),
    width=200,
    expand=True
)

navbar = ft.Container(
    content=NavRail,
    expand=True
)

main_container = ft.Container(
    content=ft.Row(
        [
            navbar,
            baseform
        ],
        alignment=ft.MainAxisAlignment.START
    ),
    padding=0
)


def _view_(login_type='guest') -> ft.View:
    if login_type == 'admin':
        return ft.View(
            "/main_page_admin",
            [
                main_container
            ],
            padding=0
        )
    if ligin_type == 'user':
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
