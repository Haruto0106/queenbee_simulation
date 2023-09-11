#!/usr/bin/env python3
#松戸で地面でガチャってたやつ 多分失敗する

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from queenbee.bee import Bee
from queenbee.logger import logger_info, log_file_r
from queenbee.plotter import df_lidar, plot_lidar, df_GPS, plot_GPS, plot_position, map_GPS
SYSTEMADDRESS = "udp://:14540"
altitude_hover=3
altitude_goto = 3


async def run():
    await drone.Connect(system_address=SYSTEMADDRESS)
    await drone.Catch_GPS()
    await drone.Loop_hold_wait(system_address=SYSTEMADDRESS)
    

    
    coroutines = [
        main_run(),
        drone.Loop_flight_mode(),
        drone.Loop_position(),
        drone.Loop_lidar(),
        drone.Loop_mission_progress(),
        drone.Loop_log(),
        drone.Loop_status_text(),
        drone.Loop_mission_progress()
        ]
    await asyncio.gather(*coroutines)

async def main_run():
    await asyncio.sleep(2)
    await drone.Arm()
    latitude_start = drone.Latitude_deg
    longitude_start = drone.Longitude_deg
    altitude_home = drone.Absolute_altitude_m
    altitude_goal = altitude_home + altitude_goto
    await drone.Goto_location(latitude_start,
                              longitude_start,
                              altitude_goal,0)
    while abs(altitude_goal - drone.Absolute_altitude_m) > 0.3:
        await asyncio.sleep(0.01)
    await drone.Land()
    await asyncio.sleep(2)
    return

        
if __name__ == "__main__":
    drone = Bee()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
