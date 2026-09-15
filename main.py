import asyncio
import random
import flet as ft

async def main(page: ft.Page):
    page.title = "CITADEL // OS Core Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0E14"
    page.padding = 16
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window.width = 420
    page.window.height = 880

    state = {
        "security_mode": "HOME_ACTIVE",
        "power_total_w": 285.0,
        "power_daily_kwh": 3.42,
        "server_w": 38.0,
        "printer1_w": 120.0,
        "workstation_w": 110.0,
        "target_temp": 21.5,
        "current_temp": 21.8,
        "humidity": 48.0,
        "co2_ppm": 640,
        "dew_point": 10.4,
        "presence": True,
        "presence_zone": "Couch / Living",
        "light_power": True,
        "light_brightness": 75,
        "light_hue": "#00E5FF",
        "smart_plugs_active": True,
        "printer1_active": True,
        "workstation_active": True,
    }

    # 1. Header & Status
    status_dot = ft.Container(width=10, height=10, border_radius=5, bgcolor=ft.Colors.GREEN_ACCENT)
    status_text = ft.Text("SYSTEM ONLINE // ZERO-TRUST ACTIVE", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT)

    header = ft.Container(
        padding=8,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text("CITADEL CORE", size=22, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE),
                        ft.Row([status_dot, status_text], spacing=6),
                    ]
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.SHIELD_ROUNDED, color=ft.Colors.CYAN_ACCENT, size=24),
                    padding=8,
                    bgcolor="#161B22",
                    border_radius=10,
                )
            ]
        )
    )

    # 2. Live Power & Energy Studio
    total_power_val = ft.Text(f"{int(state['power_total_w'])} W", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_ACCENT)
    daily_kwh_val = ft.Text(f"{state['power_daily_kwh']:.2f} kWh heute", size=12, color=ft.Colors.GREY_400)
    
    server_bar = ft.ProgressBar(value=0.15, color=ft.Colors.CYAN_ACCENT, bgcolor="#21262D", height=6)
    printer_bar = ft.ProgressBar(value=0.45, color=ft.Colors.ORANGE_ACCENT, bgcolor="#21262D", height=6)
    workstation_bar = ft.ProgressBar(value=0.40, color=ft.Colors.PURPLE_ACCENT, bgcolor="#21262D", height=6)

    server_val_txt = ft.Text(f"{state['server_w']:.0f} W", size=11, weight=ft.FontWeight.BOLD)
    printer_val_txt = ft.Text(f"{state['printer1_w']:.0f} W", size=11, weight=ft.FontWeight.BOLD)
    workstation_val_txt = ft.Text(f"{state['workstation_w']:.0f} W", size=11, weight=ft.FontWeight.BOLD)

    def toggle_zero_standby(e):
        state["smart_plugs_active"] = e.control.value
        state["printer1_active"] = e.control.value
        state["workstation_active"] = e.control.value
        plug_switch_p1.value = e.control.value
        plug_switch_ws.value = e.control.value
        page.open(ft.SnackBar(ft.Text("Zero-Standby: Standby-Lasten getrennt!" if not e.control.value else "Zero-Standby: Reaktiviert!"), duration=1200))
        page.update()

    power_card = ft.Container(
        bgcolor="#161B22",
        border_radius=16,
        padding=16,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.BOLT_ROUNDED, color=ft.Colors.AMBER_ACCENT), ft.Text("Live Stromverbrauch", size=16, weight=ft.FontWeight.BOLD)]),
                        ft.Container(
                            content=ft.Text("30 ct / kWh", size=10, color=ft.Colors.AMBER_200),
                            padding=6,
                            bgcolor="#2A2111",
                            border_radius=8,
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=[total_power_val, daily_kwh_val]
                ),
                ft.Divider(height=1, color="#30363D"),
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Row([ft.Text("Citadel Server (24/7):", size=11, color=ft.Colors.GREY_400), server_val_txt], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        server_bar,
                        ft.Row([ft.Text("3D-Drucker Bank (Active):", size=11, color=ft.Colors.GREY_400), printer_val_txt], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        printer_bar,
                        ft.Row([ft.Text("Workstation Desk:", size=11, color=ft.Colors.GREY_400), workstation_val_txt], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        workstation_bar,
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Zero-Standby Master-Cut", size=12, weight=ft.FontWeight.W_600),
                        ft.Switch(value=state["smart_plugs_active"], active_color=ft.Colors.AMBER_ACCENT, on_change=toggle_zero_standby)
                    ]
                )
            ]
        )
    )

    # 3. Quick Scene Chips
    def select_scene(scene_key):
        state["security_mode"] = scene_key
        for key, btn in scene_buttons.items():
            btn.bgcolor = "#00E5FF" if key == scene_key else "#21262D"
            btn.content.color = ft.Colors.BLACK if key == scene_key else ft.Colors.WHITE
        page.update()

    scenes = [
        ("HOME_ACTIVE", "🏠 Anwesend"),
        ("CINEMA", "🎬 Kino"),
        ("SLEEP", "🌙 Schlafen"),
        ("AWAY", "🔒 Abwesend"),
    ]
    
    scene_buttons = {}
    scene_controls = []

    for key, label in scenes:
        is_active = key == state["security_mode"]
        b = ft.Container(
            content=ft.Text(label, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK if is_active else ft.Colors.WHITE),
            bgcolor="#00E5FF" if is_active else "#21262D",
            border_radius=10,
            padding=10,
            on_click=lambda e, k=key: select_scene(k),
            animate=200,
        )
        scene_buttons[key] = b
        scene_controls.append(b)

    scene_row = ft.Row(controls=scene_controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # 4. Climate & Sensor Matrix
    cur_temp_txt = ft.Text(f"{state['current_temp']:.1f}°C", size=26, weight=ft.FontWeight.BOLD)
    target_temp_txt = ft.Text(f"{state['target_temp']:.1f}°C", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_ACCENT)
    dew_point_txt = ft.Text(f"Taupunkt: {state['dew_point']:.1f}°C", size=12, color=ft.Colors.CYAN_200)
    co2_badge = ft.Container(
        content=ft.Text(f"{state['co2_ppm']} ppm CO2", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT),
        padding=6,
        bgcolor="#0E2A1A",
        border_radius=6,
    )

    def on_temp_slider(e):
        state["target_temp"] = round(e.control.value, 1)
        target_temp_txt.value = f"{state['target_temp']:.1f}°C"
        page.update()

    climate_card = ft.Container(
        bgcolor="#161B22",
        border_radius=16,
        padding=16,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.THERMOSTAT_ROUNDED, color=ft.Colors.ORANGE_ACCENT), ft.Text("Klima & Umwelt", size=16, weight=ft.FontWeight.BOLD)]),
                        co2_badge
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([ft.Text("Ist-Temperatur", size=11, color=ft.Colors.GREY_400), cur_temp_txt]),
                        ft.Column([ft.Text("Soll-Vorgabe", size=11, color=ft.Colors.GREY_400), target_temp_txt], horizontal_alignment=ft.CrossAxisAlignment.END),
                    ]
                ),
                ft.Slider(
                    min=16.0,
                    max=26.0,
                    divisions=20,
                    value=state["target_temp"],
                    active_color=ft.Colors.ORANGE_ACCENT,
                    on_change=on_temp_slider
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        dew_point_txt,
                        ft.Text(f"Feuchte: {state['humidity']:.0f}%", size=12, color=ft.Colors.GREY_400)
                    ]
                )
            ]
        )
    )

    # 5. Lighting & mmWave Radar
    radar_badge = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.RADAR_ROUNDED, color=ft.Colors.GREEN_ACCENT, size=16),
            ft.Text(state["presence_zone"], size=11, color=ft.Colors.GREEN_ACCENT, weight=ft.FontWeight.W_600)
        ], spacing=4),
        padding=6,
        bgcolor="#0E2A1A",
        border_radius=6,
    )

    light_bulb_icon = ft.Icon(ft.Icons.LIGHTBULB_ROUNDED, color=ft.Colors.CYAN_ACCENT, size=28)
    brightness_txt = ft.Text(f"{state['light_brightness']}%", size=14, weight=ft.FontWeight.BOLD)

    def toggle_light(e):
        state["light_power"] = e.control.value
        light_bulb_icon.color = ft.Colors.CYAN_ACCENT if e.control.value else ft.Colors.GREY_600
        page.update()

    def on_brightness_slider(e):
        state["light_brightness"] = int(e.control.value)
        brightness_txt.value = f"{state['light_brightness']}%"
        page.update()

    def set_light_color(color_hex):
        state["light_hue"] = color_hex
        light_bulb_icon.color = color_hex
        page.update()

    lighting_card = ft.Container(
        bgcolor="#161B22",
        border_radius=16,
        padding=16,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([light_bulb_icon, ft.Text("Licht & Präsenz", size=16, weight=ft.FontWeight.BOLD)]),
                        radar_badge
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Hauptbeleuchtung Wohnbereich", size=13),
                        ft.Switch(value=state["light_power"], active_color=ft.Colors.CYAN_ACCENT, on_change=toggle_light)
                    ]
                ),
                ft.Row([ft.Text("Helligkeit", size=12, color=ft.Colors.GREY_400), brightness_txt], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Slider(min=0, max=100, divisions=20, value=state["light_brightness"], active_color=ft.Colors.CYAN_ACCENT, on_change=on_brightness_slider),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        ft.IconButton(ft.Icons.CIRCLE, icon_color="#00E5FF", on_click=lambda _: set_light_color("#00E5FF")),
                        ft.IconButton(ft.Icons.CIRCLE, icon_color="#FFB300", on_click=lambda _: set_light_color("#FFB300")),
                        ft.IconButton(ft.Icons.CIRCLE, icon_color="#FF2A6D", on_click=lambda _: set_light_color("#FF2A6D")),
                        ft.IconButton(ft.Icons.CIRCLE, icon_color="#05FFA1", on_click=lambda _: set_light_color("#05FFA1")),
                    ]
                )
            ]
        )
    )

    # 6. Smart Plugs
    def on_plug_toggle(plug_name, e):
        state[plug_name] = e.control.value
        page.update()

    plug_switch_p1 = ft.Switch(value=state["printer1_active"], active_color=ft.Colors.ORANGE_ACCENT, on_change=lambda e: on_plug_toggle("printer1_active", e))
    plug_switch_ws = ft.Switch(value=state["workstation_active"], active_color=ft.Colors.PURPLE_ACCENT, on_change=lambda e: on_plug_toggle("workstation_active", e))

    plugs_card = ft.Container(
        bgcolor="#161B22",
        border_radius=16,
        padding=16,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row([ft.Icon(ft.Icons.POWER_ROUNDED, color=ft.Colors.GREEN_ACCENT), ft.Text("Aktorik & Steckdosen", size=16, weight=ft.FontWeight.BOLD)]),
                ft.Row([ft.Text("3D-Drucker Bank (120 W)", size=13), plug_switch_p1], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("Workstation Desk (110 W)", size=13), plug_switch_ws], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]
        )
    )

    # 7. Asynchroner Background Telemetrie Stream
    async def telemetry_loop():
        while True:
            await asyncio.sleep(2.0)
            if state["smart_plugs_active"]:
                base_w = state["server_w"]
                if state["printer1_active"]:
                    base_w += 115.0 + random.uniform(-10, 15)
                if state["workstation_active"]:
                    base_w += 105.0 + random.uniform(-8, 12)
                state["power_total_w"] = base_w
            else:
                state["power_total_w"] = state["server_w"]

            total_power_val.value = f"{int(state['power_total_w'])} W"
            page.update()

    # 8. Render UI
    page.add(
        header,
        scene_row,
        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
        power_card,
        climate_card,
        lighting_card,
        plugs_card
    )

    asyncio.create_task(telemetry_loop())

if __name__ == "__main__":
    ft.run(main)
