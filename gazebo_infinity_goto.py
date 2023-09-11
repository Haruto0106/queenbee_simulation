#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from queenbee.bee import Bee
from queenbee.logger import logger_info, log_file_r
from queenbee.plotter import df_lidar, plot_lidar, df_GPS, plot_GPS, plot_position, map_GPS
SYSTEMADDRESS = "udp://:14540"
altitude_hover=1.5
counter = 0
# latitude_start=35.7963106###松戸の橋の座標
# longitude_start=139.89165

# latitude_start=35.796174###松戸の橋近くの座標
# longitude_start=139.891552

# latitude_goal = 35.796907
# longitude_goal = 139.892006
altitude_goto = 3
latitude_goto = 0.0003
longitude_goto = 0.0003



async def run():
    # global drone

    # global dist,lat,lon,abs_alt,rel_alt
    # dist,lat,lon,abs_alt,rel_alt = 0,0,0,0,0
    # await drone.connect(system_address="udp://:14540")
    await drone.Connect(system_address=SYSTEMADDRESS)
    await drone.Catch_GPS()
    await drone.Loop_hold_wait(system_address=SYSTEMADDRESS)
    await drone.Arm()

    
    coroutines = [
        main_run(),
        drone.Get_flight_mode(),
        drone.Get_position(),
        drone.Get_lidar(),
        drone.Get_mission_progress(),
        drone.Loop_log(),
        drone.Loop_status_text(),
        drone.Loop_mission_progress(),
        # df_lidar(),
        # df_GPS(),
        # # plot_lidar(),
        # # plot_GPS(),
        # plot_position(),
        # map_GPS()
        
        # get_distance(),
        # loop_print()
        # get_GPS(),
        # loop_print_GPS()
    ]
    await asyncio.gather(*coroutines)

async def main_run():
    counter = 0
    await asyncio.sleep(2)
    latitude_start = drone.Latitude_deg
    longitude_start = drone.Longitude_deg
    altitude_home = drone.Absolute_altitude_m

    altitude_goal = altitude_home + altitude_goto
    latitude_goal = latitude_start + latitude_goto
    longitude_goal = longitude_start + longitude_goto
    await drone.Takeoff()
    await asyncio.sleep(5)
    altitude_goal = altitude_home + altitude_hover
    while True:
        await drone.Goto_location(latitude_start,
                                longitude_start,
                                altitude_goal,0)#行き
        while abs(latitude_start - drone.Latitude_deg) > 1.0e-5 and abs(longitude_start - drone.Longitude_deg) > 1.0e-5 :
            await asyncio.sleep(1)
        counter += + 1#片道の回数
        logger_info.info("The number of one-way trip:" + str(counter))
        await drone.Goto_location(latitude_goal,
                                longitude_goal,
                                altitude_goal,0)#帰り
        while abs(latitude_goal - drone.Latitude_deg) > 1.0e-5 and abs(longitude_goal - drone.Longitude_deg) > 1.0e-5 :
            await asyncio.sleep(1)    
        counter = counter + 1#片道の回数
        logger_info.info("The number of one-way trip:" + str(counter))

        
if __name__ == "__main__":
    drone = Bee()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
