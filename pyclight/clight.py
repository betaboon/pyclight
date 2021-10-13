import logging
import os

from dbus_next import BusType
from dbus_next.aio import MessageBus, ProxyObject, ProxyInterface

logger = logging.getLogger(__name__)


class Clight:
    def __init__(self):
        self._session_bus: MessageBus = MessageBus(bus_type=BusType.SESSION)
        self._system_bus = MessageBus(bus_type=BusType.SYSTEM)

    async def get_session_bus(self) -> MessageBus:
        if not self._session_bus.connected:
            await self._session_bus.connect()
        return self._session_bus

    async def get_system_bus(self) -> MessageBus:
        if not self._system_bus.connected:
            await self._system_bus.connect()
        return self._system_bus

    async def get_interface(
        self,
        bus: MessageBus,
        bus_name: str,
        path: str,
        interface_name: str,
    ) -> ProxyInterface:
        introspection = await bus.introspect(bus_name, path)
        obj = bus.get_proxy_object(bus_name, path, introspection)
        interface = obj.get_interface(interface_name)
        return interface

    async def get_clight_interface(self) -> ProxyInterface:
        bus = await self.get_session_bus()
        return await self.get_interface(
            bus=bus,
            bus_name="org.clight.clight",
            path="/org/clight/clight",
            interface_name="org.clight.clight",
        )

    async def increase_backlight(self, value: int) -> None:
        i = await self.get_clight_interface()
        v = float(value / 100)
        await i.call_inc_bl(v)

    async def decrease_backlight(self, value: int) -> None:
        i = await self.get_clight_interface()
        v = float(value / 100)
        await i.call_dec_bl(v)

    async def get_backlight(self) -> int:
        i = await self.get_clight_interface()
        v = await i.get_bl_pct()
        return int(v * 100)

    async def set_backlight(self, value: int) -> None:
        session_bus = await self.get_session_bus()
        backlight_conf = await self.get_interface(
            bus=session_bus,
            bus_name="org.clight.clight",
            path="/org/clight/clight/Conf/Backlight",
            interface_name="org.clight.clight.Conf.Backlight",
        )
        is_smooth = await backlight_conf.get_no_smooth() == False
        smooth_step = await backlight_conf.get_trans_step()
        smooth_timeout = await backlight_conf.get_trans_duration()

        smooth_step = 0.05
        smooth_timeout = 1

        logger.debug(f"{is_smooth=}")
        logger.debug(f"{smooth_step=}")
        logger.debug(f"{smooth_timeout=}")

        system_bus = await self.get_system_bus()
        backlight = await self.get_interface(
            bus=system_bus,
            bus_name="org.clightd.clightd",
            path="/org/clightd/clightd/Backlight",
            interface_name="org.clightd.clightd.Backlight",
        )
        v = float(value / 100)
        await backlight.call_set_all(v, [is_smooth, smooth_step, smooth_timeout], "")
