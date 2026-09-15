import asyncio
import flet as ft
from state import state
from mqtt_service import mqtt_service

class LightingCard(ft.Card):
    def __init__(self):
        super().__init__()
        self.presence_badge = ft.Container(
            content=ft.Text("Präsenz erkannt" if state.radar_presence else "Raum leer", size=11),
            bgcolor=ft.Colors.GREEN_900 if state.radar_presence else ft.Colors.GREY_800,
            border_radius=5,
            padding=4
        )
        
        self.switch_light = ft.Switch(label="Hauptbeleuchtung", value=state.light_living_room, on_change=self._on_toggle)
        self.dimmer = ft.Slider(min=0, max=100, divisions=10, value=state.light_brightness, label="{value}%", on_change=self._on_dim)

        self.content = ft.Container(
            padding=15,
            content=ft.Column(
                controls=[
                    ft.Row([
                        ft.Row([ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.YELLOW_ACCENT), ft.Text("Beleuchtung", size=18, weight=ft.FontWeight.BOLD)]),
                        self.presence_badge
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.switch_light,
                    ft.Text("Dimmwert:", size=12),
                    self.dimmer
                ]
            )
        )

    def _on_toggle(self, e):
        state.light_living_room = e.control.value
        asyncio.create_task(mqtt_service.publish_actuator("living_room/light/state", "ON" if e.control.value else "OFF"))

    def _on_dim(self, e):
        state.light_brightness = int(e.control.value)
        asyncio.create_task(mqtt_service.publish_actuator("living_room/light/brightness", str(state.light_brightness)))

    def refresh_ui(self):
        self.presence_badge.content.value = "Präsenz erkannt" if state.radar_presence else "Raum leer"
        self.presence_badge.bgcolor = ft.Colors.GREEN_900 if state.radar_presence else ft.Colors.GREY_800
        self.update()
