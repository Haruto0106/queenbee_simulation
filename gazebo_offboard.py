#!/usr/bin/env python3


import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed)
from queenbee.bee import Bee
from queenbee.logger import logger_info, log_file_r
from queenbee.plotter import df_lidar, plot_lidar, df_GPS, plot_GPS, plot_position, map_GPS


async def run():  
    await drone.Connect(system_address="udp://:14540")
    await drone.Catch_GPS()
    await drone.Loop_hold_wait(system_address="udp://:14540")
    await drone.Arm()
    

    coroutines = [
        main_run(),
        drone.Get_flight_mode(),
        drone.Get_position(),
        drone.Get_lidar(),
        drone.Loop_log(),
        drone.Loop_status_text()
    ]
    await asyncio.gather(*coroutines)


async def main_run():
    await asyncio.sleep(3)
    await drone.Takeoff()
    while drone.Lidar <0.3:
        await asyncio.sleep(0.01)
    logger_info.info("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    logger_info.info("-- Starting offboard")
    while True:
        try:
            await drone.offboard.start()
            break
        except OffboardError as error:
            logger_info.error(f"Starting offboard mode failed with error code: \
                {error._result.result}")
            continue


    logger_info.info("-- climb")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, -0.5, 0.0))
    await asyncio.sleep(5)

    logger_info.info("-- forward")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.5, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)

    logger_info.info("-- Wait for a bit")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)

    logger_info.info("-- right")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.5, 0.0, 0.0))
    await asyncio.sleep(5)

    logger_info.info("-- back")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(-0.5, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)

    logger_info.info("-- left")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, -5.0, 0.0, 0.0))
    await asyncio.sleep(5)

    logger_info.info("--turn")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 36))
    await asyncio.sleep(5)
    
    logger_info.info("--down")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.2, 0.0)
    )
    await asyncio.sleep(5)

    logger_info.info("-- Wait for a bit")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)

    logger_info.info("-- Stopping offboard")
    while True:
        try:
            await drone.offboard.stop()
            break
        except OffboardError as error:
            logger_info.error(f"Stopping offboard mode failed with error code: \
                {error._result.result}")
            continue
    
    await drone.Hold()
    await drone.Land()


if __name__ == "__main__":
    drone = Bee()
    # Run the asyncio loop
    asyncio.run(run())