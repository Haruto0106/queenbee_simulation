#!/usr/bin/env python3
#松戸で空中でholdしたまま動かなくなったやつ

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from queenbee.bee import Bee
from queenbee.logger import logger_info, log_file_r
from queenbee.plotter import df_lidar, plot_lidar, df_GPS, plot_GPS, plot_position, map_GPS
SYSTEMADDRESS = "udp://:14540"
altitude_hover=3
altitude_goto = 3
# latitude_start=35.7963106###松戸の橋の座標
# longitude_start=139.89165

# latitude_start=35.796174###松戸の橋近くの座標
# longitude_start=139.891552

# latitude_goal = 35.796723   #ゲートボール場の座標 
# longitude_goal = 139.8918259

latitude_goto = 0.0003
longitude_goto = 0.0003


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
    latitude_goal = latitude_start + latitude_goto
    longitude_goal = longitude_start + longitude_goto
    
    await drone.Takeoff()
    while drone.Lidar <= 3:#1.5mだとテント突き抜けそう、0.3mでもいいかも
        await asyncio.sleep(0.05)

    await drone.Goto_location(latitude_goal,
                              longitude_goal,
                              altitude_goal,0)
    while abs(latitude_goal - drone.Latitude_deg) > 1.0e-5 and abs(longitude_goal - drone.Longitude_deg) > 1.0e-5  and abs(altitude_goal - drone.Absolute_altitude_m)>0.1:
        await asyncio.sleep(0.01)
    await drone.Hold()
    await asyncio.sleep(1)
    await drone.Land()
    await asyncio.sleep(2)
    return

        
if __name__ == "__main__":
    drone = Bee()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
