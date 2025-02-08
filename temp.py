import flet as ft
import logging


def main(page: ft.Page):

    c = ft.Container(
        width=400,
        height=200,
        bgcolor="red",
        animate=ft.animation.Animation(500, ft.AnimationCurve.DECELERATE),
    )

    def animate_container(e):
        c.width = 200 if c.width == 400 else 400
        c.height = 400 if c.height == 200 else 200
        c.bgcolor = "blue" if c.bgcolor == "red" else "red"
        c.update()

    page.add(c, ft.ElevatedButton("Animate container", on_click=animate_container))


logging.basicConfig(level=logging.DEBUG)
ft.app(main)
