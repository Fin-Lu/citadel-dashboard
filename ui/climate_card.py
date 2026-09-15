import asyncio
import flet as ft
from state import state
from mqtt_service import mqtt_service

class ClimateCard(ft.Card):
    def __init__(self):
        super().__init__()
        self.current_text = ft.Text(f"{state.current_temp} °C", size=24, weight=ft.FontWeight.BOLD)
        self.target_text = ft.Text(f"{state.target_temp} °C", size=18, color=ft.Colors.ORANGE_ACCENT)
        self.dew_text = ft.Text(f"Taupunkt: {state.dew_point} °C | CO2: {state.co2_ppm} ppm", size=12, color=ft.Colors.GREY_400)
        
        self.slider = ft.Slider(
            min=16.0,
            max=26.0,
            divisions=20,
            value=state.target_temp,
            label="{value} °C",
            on_change=self._on_slider_change
        )
        
        self.content = ft.Container(
            padding=15,
            content=ft.Column(
                controls=[
                    ft.Row([ft.Icon(ft.Icons.THERMOSTAT, color=ft.Colors.ORANGE_ACCENT), ft.Text("Klimasteuerung", size=18, weight=ft.FontWeight.BOLD)]),
                    ft.Row([ft.Text("Ist:"), self.current_text, ft.Text("Soll:"), self.target_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.slider,
                    self.dew_text
                ]
            )
        )

    def _on_slider_change(self, e):
        state.target_temp = round(e.control.value, 1)
        self.target_text.value = f"{state.target_temp} °C"
        self.update()
        asyncio.create_task(mqtt_service.publish_actuator("living_room/temp/set", str(state.target_temp)))

    def refresh_ui(self):
        self.current_text.value = f"{state.current_temp} °C"
        self.dew_text.value = f"Taupunkt: {state.dew_point} °C | CO2: {state.co2_ppm} ppm"
        self.update()
