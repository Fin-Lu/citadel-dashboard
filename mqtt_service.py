import asyncio
import json
import aiomqtt
from state import state

class MQTTService:
    def __init__(self, broker_ip: str = "127.0.0.1", port: int = 1883):
        self.broker_ip = broker_ip
        self.port = port
        self.client = None

    async def start(self):
        while True:
            try:
                async with aiomqtt.Client(self.broker_ip, port=self.port) as client:
                    self.client = client
                    await client.subscribe("citadel/nodes/+/+/telemetry")
                    await client.subscribe("citadel/system/security_status")

                    async for message in client.messages:
                        self._handle_message(message)
            except aiomqtt.MqttError:
                await asyncio.sleep(5)

    def _handle_message(self, message):
        try:
            payload_str = message.payload.decode()
            data = json.loads(payload_str)
            
            if "scd40" in data:
                state.current_temp = data["scd40"].get("temperature", state.current_temp)
                state.humidity = data["scd40"].get("humidity", state.humidity)
                state.co2_ppm = data["scd40"].get("co2", state.co2_ppm)
            if "ld2410" in data:
                state.radar_presence = data["ld2410"].get("target_state", 0) > 0
                
            state.notify()
        except Exception as e:
            print(f"Fehler beim Parsen der MQTT-Nachricht: {e}")

    async def publish_actuator(self, topic: str, value: str):
        if self.client:
            try:
                await self.client.publish(f"citadel/actuators/{topic}", value)
            except Exception as e:
                print(f"Fehler beim Senden: {e}")

mqtt_service = MQTTService()
