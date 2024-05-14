import flet as ft

dbpage = ft.Container(
    content=ft.Text('Database Page')
)

queries = ft.Container(
    content=ft.Text('Запросы')
)

settings = ft.Container(
    content=ft.Text('Настройки')
)

baseform = ft.Container(
    padding=0,
    content=dbpage
)


def page_update(p: ft.Page):
    p.update()


def on_change_rail(e):
    match e.control.data:
        case 0:
            baseform.content = dbpage
            print('Выбрана база данных')
        case 1:
            baseform.content = queries
            print('Выбраны запросы')
        case 2:
            baseform.content = settings
            print('Выбраны настройки')
    page_update(e.page)


NavRail = ft.Container(
    content=ft.Column(
        controls=[
            ft.ExpansionTile(
                title=ft.Text(
                    'База Данных',
                ),
                controls=[
                    ft.ListTile(
                        title=ft.Text(
                            'Главная таблица',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=0.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Первая таблица',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=0.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Вторая таблица',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=0.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Третья таблица',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=0.1
                    )
                ],
                affinity=ft.TileAffinity.LEADING,
                controls_padding=ft.padding.only(left=10),

            ),
            ft.ExpansionTile(
                title=ft.Text(
                    'Запросы',
                ),
                controls=[
                    ft.ListTile(
                        title=ft.Text(
                            'Первый запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Второй запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Третий запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Четвертый запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Пятый запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Шестой запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Седьмой запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Восьмой запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Девятый запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                    ft.ListTile(
                        title=ft.Text(
                            'Десятый запрос',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=1.1
                    ),
                ],
                affinity=ft.TileAffinity.LEADING,
                controls_padding=ft.padding.only(left=10),

            ),
            ft.ExpansionTile(
                title=ft.Text(
                    'Настройки',
                ),
                controls=[
                    ft.ListTile(
                        title=ft.Text(
                            '---',
                            style=ft.TextThemeStyle.BODY_MEDIUM
                        ),
                        on_click=on_change_rail,
                        data=2.1
                    )
                ],
                affinity=ft.TileAffinity.LEADING,
                controls_padding=ft.padding.only(left=10),

            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        scroll=ft.ScrollMode.HIDDEN
    ),
    width=200,
)


def logout(e):
    print('Logout')
    e.page.clean()
    e.page.go('/')


usertab = ft.Container(
    content=ft.Row(
        [
            ft.Text(
                'User Type',
                style=ft.TextThemeStyle.BODY_LARGE
            ),
            ft.IconButton(
                icon=ft.icons.LOGOUT_ROUNDED,
                icon_color=ft.colors.RED_700,
                on_click=logout
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    ),
    padding=20,
    bgcolor=ft.colors.SECONDARY_CONTAINER,
    # expand=True,
    height=80

)

navbar = ft.Container(
    content=ft.Column(
        controls=[
            NavRail
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.HIDDEN
    ),
    padding=0,
    width=200,
    alignment=ft.alignment.top_center
)

left_panel = ft.Column(
    controls=[
        navbar,
        usertab
    ],
    alignment=ft.MainAxisAlignment.END,
    width=200,
)


main_container = ft.Container(
    content=ft.Row(
        [
            left_panel,
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


# global user_type


def _view_(login_type='guest') -> ft.View:
    # global user_type
    # user_type = login_type
    usertab.content.controls[0].value = {'guest': 'Гость', 'admin': 'Админ', 'user': 'Пользователь'}[login_type]

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
