from dataclasses import dataclass, field
from typing import Callable, List

@dataclass
class AppState:
    current_temp: float = 21.4
    target_temp: float = 22.0
    humidity: float = 54.0
    co2_ppm: int = 620
    dew_point: float = 11.8
    
    light_living_room: bool = True
    light_brightness: int = 70
    radar_presence: bool = True
    system_mode: str = "HOME_ACTIVE"
    security_level: str = "GREEN"
    
    _listeners: List[Callable[[], None]] = field(default_factory=list)

    def subscribe(self, callback: Callable[[], None]):
        self._listeners.append(callback)

    def notify(self):
        for callback in self._listeners:
            callback()

state = AppState()
