#!/usr/bin/env python3

import asyncio
from mavsdk import System
from queenbee.bee import Bee
from queenbee.logger_drone import logger_info, log_file_r
from queenbee.plotter import df_lidar, plot_lidar, df_GPS, plot_GPS, plot_position, map_GPS
from queenbee.lora_queenbee import Lora

async def run():
    await drone.Connect(system_address="serial:///dev/ttyACM0:115200")
    await drone.Catch_GPS()
    await drone.Loop_hold_wait(system_address="serial:///dev/ttyACM0:115200")
    await lora.power_on()

    coroutines = [
        main_run(),
        drone.Loop_flight_mode(),
        drone.Loop_position(),
        drone.Loop_lidar(),
        drone.Loop_log(),
        drone.Loop_status_text(),
        lora.cycle_send_position(drone)
        ]
    await asyncio.gather(*coroutines)

async def main_run():
    await asyncio.sleep(3)
    await drone.Arm()
    await drone.Takeoff()
    while drone.Lidar <= 0.3:
        await asyncio.sleep(0.05)
    await drone.Hold()
    await asyncio.sleep(15)
    await drone.Land()  

if __name__ == "__main__":
    drone = Bee()
    lora = Lora()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())