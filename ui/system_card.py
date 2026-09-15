import asyncio
import flet as ft
from state import state
from mqtt_service import mqtt_service

class SystemCard(ft.Card):
    def __init__(self):
        super().__init__()
        self.security_dot = ft.Icon(ft.Icons.SHIELD, color=ft.Colors.GREEN_ACCENT, size=20)
        
        # Dropdown ohne on_change im Konstruktor initialisieren
        self.dropdown_mode = ft.Dropdown(
            label="Sicherheits- & Raummodus",
            value=state.system_mode,
            options=[
                ft.dropdown.Option("HOME_ACTIVE", "🏠 Anwesend (Automatik)"),
                ft.dropdown.Option("SLEEP", "🌙 Schlafen (Radar aktiv)"),
                ft.dropdown.Option("AWAY", "🔒 Abwesend (Voller Alarm)"),
                ft.dropdown.Option("CINEMA", "🎬 Kino (Licht gedimmt)"),
            ],
        )
        # Event-Handler als Eigenschaft zuweisen
        self.dropdown_mode.on_change = self._on_mode_change
        
        self.content = ft.Container(
            padding=15,
            content=ft.Column(
                controls=[
                    ft.Row([
                        ft.Text("Citadel Security & Mode", size=18, weight=ft.FontWeight.BOLD),
                        self.security_dot
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.dropdown_mode
                ]
            )
        )

    def _on_mode_change(self, e):
        state.system_mode = e.control.value
        asyncio.create_task(mqtt_service.publish_actuator("system/mode/set", state.system_mode))
