import flet as ft
from typing import List, Dict, Tuple, Optional, Union


def main(page: ft.Page) -> None:
    # Configuração da Janela
    page.title = "Tela Home"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 450
    page.window.height = 750
    page.window.resizable = False

    # Cor de fundo padrão
    background_conecta_recife_color_light: str = "#8eb5ea"
    background_conecta_recife_color_dark: str = "#3b78cc"

    # Cabeçalho com cor de fundo e espaçamento aprimorado
    header_element = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(  # Estilizando o botão "Sair"
                    text="Sair",
                    bgcolor=background_conecta_recife_color_light,
                    color=ft.colors.WHITE,
                    on_click=lambda _: print("Botão sair clicado!"),
                ),
                ft.Icon(ft.icons.ACCOUNT_CIRCLE,
                        size=30, color=ft.colors.WHITE),
                ft.IconButton(
                    icon=ft.icons.MENU,
                    icon_size=30,
                    bgcolor=background_conecta_recife_color_dark,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: print("Menu clicado!")
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        # bgcolor=background_conecta_recife_color,  # Fundo azul escuro
        padding=10,  # Espaçamento interno maior
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[background_conecta_recife_color_light,
                    background_conecta_recife_color_dark]
        )
        # border=ft.border.all(2, ft.colors.RED),  # Borda azul de 2px
    )

    question_element = ft.Container(
        content=ft.Row([ft.Text("O que você gostaria de fazer?",
                                size=17, color=ft.Colors.BLACK, weight=ft.FontWeight.W_700)],
                       alignment=ft.MainAxisAlignment.CENTER
                       ),
        margin=ft.margin.only(top=50)
    )

    
    

    # Adiciona o cabeçalho à interface
    page.add(header_element, question_element)


ft.app(target=main)
