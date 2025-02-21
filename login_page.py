import flet as ft
import json
import logging
import os
import sys
import time
import importlib

import settings_module as sem
import db_checker as dbc
from encrypted_storage import EncryptedStorage

# from main_page import _view_ as main_view


# ---------------------------------------------------------------------------------------------------------

base_path = os.path.dirname(os.path.abspath(__file__))
storage_folder = os.path.join(base_path, '.secure_data')
if os.path.exists(storage_folder):
    storage = EncryptedStorage()
    storage.delete_storage()
    del storage

storage = EncryptedStorage()


# ---------------------------------------------------------------------------------------------------------


def main(page: ft.Page):
    page.theme = ft.Theme(
        ft.Colors.GREEN,
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.CUPERTINO,
            ios=ft.PageTransitionTheme.CUPERTINO,
            macos=ft.PageTransitionTheme.CUPERTINO,
            linux=ft.PageTransitionTheme.CUPERTINO,
            windows=ft.PageTransitionTheme.CUPERTINO,
        ),
    )

    page.title = "Login Page"
    page.window.focused = True

    match sem.read_settings()["PageTheme"]:
        case "LIGHT":
            page.theme_mode = ft.ThemeMode.LIGHT
        case "DARK":
            page.theme_mode = ft.ThemeMode.DARK

    page.window.minimizable = True
    # page.window.maximizable = False
    # page.window.resizable = False

    page.window.height = 800
    page.window.width = 1300
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.session.set("window_parameters", {'width': page.window.width, 'height': page.window.height})

    page.window.maximized = True
    page.window.center()

    # ---------------------------------------------------------------------------------------------------------

    def handle_window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)

    page.window.prevent_close = True
    page.window.on_event = handle_window_event

    def yes_click(e):
        page.window.visible = False
        print('page.window.visible = False')
        page.window.destroy()
        print('page.window.destroy()')
        storage.delete_storage()
        print('storage.delete_storage()')

    def no_click(e):
        page.close(confirm_dialog)

    confirm_dialog = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=10),
        modal=True,
        title=ft.Text("Подтвердите Выход"),
        content=ft.Text("Вы уверены, что хотите выйти?"),
        actions=[
            ft.ElevatedButton("Да",
                              on_click=yes_click,
                              style=ft.ButtonStyle(
                                  shape=ft.RoundedRectangleBorder(radius=10)
                              ),
                              ),
            ft.OutlinedButton("Нет",
                              on_click=no_click,
                              style=ft.ButtonStyle(
                                  shape=ft.RoundedRectangleBorder(radius=10)
                              ),
                              ),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    # ---------------------------------------------------------------------------------------------------------

    def login(e):
        users_file = storage.load_data()['db_info']['folder_path'] + r'\users.json'
        print(users_file)
        if username.value == '':
            username.error_text = 'Username cannot be empty'
            page.update()
        if password.value == '':
            password.error_text = 'Password cannot be empty'
            page.update()
        else:
            username.error_text = ''
            password.error_text = ''
            page.update()
            with open(users_file, 'r') as f:
                users = json.load(f)
                if username.value not in users:
                    print('User does not exist')
                    username.error_text = 'Username does not exist'
                    page.update()
                elif users[username.value] == password.value:
                    print('Login successful')
                    print(f'Username: {username.value} Password: {password.value}')
                    match username.value:
                        case 'admin':
                            page.go('/main_page_admin')
                        case 'user':
                            page.go('/main_page_user')
                    password.value = ''
                    username.value = ''
                else:
                    print('Password incorrect')
                    print(f'Username: {username.value} Password: {password.value}')
                    password.error_text = 'Password incorrect'
                    page.update()

    def auth_fields_on_change(e):
        if e.control.value == '':
            e.control.error_text = f'{e.control.data} cannot be empty'
            page.update()
        else:
            e.control.error_text = ''
            page.update()

    def db_check():
        try:
            databases = dbc.get_databases()
            print("\nНайдены базы данных:")
            for name, path in databases.items():
                print(f"{name}: {path}")
            print('\n')

            dropdown_options = []
            for name, path in databases.items():
                dropdown_options.append(ft.dropdown.Option(text=name, key=path))
            return dropdown_options
        except Exception as e:
            print(f"Ошибка: {e}")
            try:
                db_picker.error_text = f"Ошибка: {e}"
                page.update()
            except Exception as e2:
                print(f"Ошибка: {e2} | db_check function")

    def db_picker_on_change(e):
        if pick_db_button.disabled:
            pick_db_button.disabled = False
        page.update()

    def animate_body(e):
        body.content = ft.AnimatedSwitcher(
            content=login_body.content if body.data == 'welcome_body' else welcome_body.content,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=500,
        )
        body.data = 'login_body' if body.data == 'welcome_body' else 'welcome_body'
        body.width = 400 if body.data == 'login_body' else 500
        body.height = 500 if body.data == 'login_body' else 400

        page.update()

    def pick_db(e):
        # print(db_picker.value)
        # page.session.set('db_info', {
        #     'folder_path': os.path.dirname(db_picker.value),
        #     'db_path': db_picker.value
        # }
        #                  )
        storage.save_data({
            'db_info': {
                'folder_path': os.path.dirname(db_picker.value),
                'db_path': db_picker.value
            }
        })
        # print(f"\n{page.session.get('db_info')}\n")
        print(f"\n{storage.load_data()['db_info']}")
        animate_body(e)

    def back_button_on_click(e):
        username.value = ''
        password.value = ''
        username.error_text = ''
        password.error_text = ''
        animate_body(e)

    welcome_body = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    'Выберите базу данных',
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(),
                db_picker := ft.Dropdown(
                    options=[
                        *db_check()
                    ],
                    on_change=db_picker_on_change
                ),
                ft.Divider(
                    height=30,
                    opacity=0
                ),
                ft.Row(
                    controls=[
                        pick_db_button := ft.FilledButton(
                            text='Далее',
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=10
                                ),
                                padding=20
                            ),
                            on_click=pick_db,
                            disabled=True
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        bgcolor="#272b25",
        width=500,
        height=400,
        border=ft.border.all(
            2,
            color='#363a34'
        ),
        border_radius=ft.border_radius.all(10),
        padding=30,
        alignment=ft.alignment.center,
    )

    login_body = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                        on_click=back_button_on_click
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            ft.Text(
                                'Sign In',
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    )
                ),
                # ft.Divider(
                #     opacity=0,
                #     height=10
                # ),
                ft.Column(
                    controls=[
                        username := ft.TextField(
                            label='Username',
                            icon=ft.icons.PERSON_ROUNDED,
                            autofocus=True,
                            border=ft.InputBorder.UNDERLINE,
                            on_change=auth_fields_on_change,
                            data='Username'
                        ),
                        password := ft.TextField(
                            label='Password',
                            icon=ft.icons.LOCK_OUTLINE_ROUNDED,
                            border=ft.InputBorder.UNDERLINE,
                            password=True,
                            can_reveal_password=True,
                            on_change=auth_fields_on_change,
                            data='Password',

                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    'Login as guest',
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=10
                                        ),
                                        padding=20
                                    ),
                                    on_click=lambda _: page.go('/main_page_guest')
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.FilledButton(
                            'Login',
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=10
                                ),
                                padding=20
                            ),
                            on_click=login,

                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            # spacing=20
        ),
        bgcolor="#272b25",
        width=400,
        height=500,
        border=ft.border.all(
            2,
            color='#363a34'
        ),
        border_radius=ft.border_radius.all(10),
        padding=30,
        alignment=ft.alignment.center,
    )

    body = ft.Container(
        content=welcome_body.content,
        data='welcome_body',
        bgcolor="#272b25",
        width=500,
        height=400,
        border=ft.border.all(
            2,
            color='#363a34'
        ),
        border_radius=ft.border_radius.all(10),
        padding=30,
        alignment=ft.alignment.center,
        animate=ft.animation.Animation(500, ft.AnimationCurve.DECELERATE)
    )

    page_body = ft.Column(
        [
            body
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(page_body)

    page.update()

    # def route_change(route):
    #     if page.theme_mode == ft.ThemeMode.DARK:
    #         welcome_body.bgcolor = "#272b25"
    #     else:
    #         welcome_body.bgcolor = ft.colors.SECONDARY_CONTAINER

    def route_change(route):
        page.views.clear()
        if page.theme_mode == ft.ThemeMode.DARK:
            body.bgcolor = "#272b25"
        else:
            body.bgcolor = ft.colors.SECONDARY_CONTAINER

        page.views.append(
            ft.View(
                "/",
                [
                    page_body
                ],
                padding=0,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.title = 'Authentication'

        # from main_page_new import _view_ as main_view
        if "/main_page" in page.route:
            if "main_page_new" in sys.modules:
                importlib.reload(sys.modules["main_page_new"])

            from main_page import _view_ as main_view
            match page.route:
                case "/main_page_admin":
                    page.views.append(main_view(login_type='admin'))
                    page.title = "DataBase Management System - Admin"
                case "/main_page_user":
                    page.views.append(main_view(login_type='user'))
                    page.title = "DataBase Management System - User"
                case "/main_page_guest":
                    page.views.append(main_view())
                    page.title = "DataBase Management System - Guest"
            # ----------------------------------------------------------------
            username.value = ''
            password.value = ''
            username.error_text = ''
            password.error_text = ''
            # ----------------------------------------------------------------

        # print(e.page.views)
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ft.app(target=main)
