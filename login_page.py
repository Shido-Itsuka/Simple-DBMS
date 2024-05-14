import flet as ft
import json
import sqlite3

from main_page import _view_ as main_view


def main(page: ft.Page):
    page.theme = ft.Theme(ft.colors.GREEN)

    page.title = "Login Page"
    page.window_focused = True
    page.theme_mode = ft.ThemeMode.DARK

    page.window_minimizable = True
    page.window_maximizable = False
    page.window_resizable = False

    page.window_height = 800
    page.window_width = 1200
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.window_center()

    def login(e):
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
            with open('users.json', 'r') as f:
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

    login_body = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    'Sign In',
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
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
                                )
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
                    ),
                    on_click=login,


                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            # spacing=20
        ),
        bgcolor="#272b25",
        width=400,
        height=500,
        border=ft.border.all(2, '#363a34'),
        border_radius=ft.border_radius.all(10),
        padding=30,
        alignment=ft.alignment.center,
    )

    page_body = ft.Column(
        [
            login_body
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(page_body)

    page.update()

    def route_change(route):
        page.views.clear()
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

        match page.route:
            case "/main_page_admin":
                page.views.append(main_view('admin')),
                page.title = "DataBase Management System - Admin"
            case "/main_page_user":
                page.views.append(main_view('user')),
                page.title = "DataBase Management System - User"
            case "/main_page_guest":
                page.views.append(main_view())
                page.title = "DataBase Management System - Guest"

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
