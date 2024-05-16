import flet as ft

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
                        show_selected_icon=False
                    )
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ],
        expand=True,

    ),
    padding=20,
    expand=True,
)

queries = ft.Container(
    content=ft.Text('Запросы')
)


def change_theme(e):
    e.page.theme_mode = e.page.theme_mode.LIGHT \
        if e.page.theme_mode == e.page.theme_mode.DARK \
        else e.page.theme_mode.DARK
    e.control.selected = True if e.control.selected is False else False
    page_update(e.page)


change_theme_content = ft.Container(
    content=ft.Row(
        [
            ft.Text(
                'Сменить тему:'
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
)

settings = ft.Container(
    content=ft.Column(
        controls=[
            ft.Container(
                content=ft.Card(
                    content=change_theme_content,
                    variant=ft.CardVariant.ELEVATED,
                    show_border_on_foreground=True,
                    is_semantic_container=True,
                    scale=1.2,
                ),
                width=180
            )
        ]
    ),
    padding=20
)

helppage = ft.Container(
    content=ft.Text('Помощь')
)

baseform = ft.Container(
    padding=0,
    content=dbpage,
    expand=True
)


def page_update(p: ft.Page):
    p.update()


def logout(e):
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
            selected_icon=ft.icons.TABLE_ROWS,
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
                'Помощь',
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


# global user_type


def _view_(login_type='guest') -> ft.View:
    # global user_type
    # user_type = login_type
    user_type_text.value = {'guest': 'Гость', 'admin': 'Админ', 'user': 'Пользователь'}[
        login_type]
    NavRail.selected_index = 0
    baseform.content = dbpage
    table_select.selected = {'0'}

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
