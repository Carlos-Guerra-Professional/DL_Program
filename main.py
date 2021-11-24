# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import csv
import datetime

import pandas as pd
import math
from datetime import date, datetime, time, timedelta

from Modules import Truck
from Modules import Package
from Modules import ChainingHashTable


# User interface to lookup the status of packages at time given.
# Time: O(n), Space: O(n)
def user_interface(final_total_distance, package_hash, package_table):
    print("\n")
    print("WELCOME TO THE WGUPS DELIVERY AND LOGISTICS APPLICATION.")
    print("\n")
    print("Total Distance Traveled: ", final_total_distance)
    print("\n")

    user_input = ''
    while user_input != 'q' and user_input != 'Q':
        print(" Please select an option:", "\n",
              "1. To see the status of all packages at a particular time, type the number "'1'", then press ENTER.",
              "\n",
              "2. To exit the application type the letter 'Q' or 'q', then press ENTER.", "\n")
        user_menu_input = input()
        if user_menu_input == 'q' or user_menu_input == 'Q':
            print("Goodbye.")
            exit()

        if user_menu_input != 'q' and user_menu_input != 'Q' and user_menu_input != '1':
            print(" Invalid entry.", "\n", "Please follow instruction options and try again.", "\n")

        if user_menu_input == '1':
            while user_menu_input != 'q' and user_menu_input != 'Q':
                print(" Please enter a time to see the status of all packages at that given time.", "\n",
                      "Enter time in the following format for hour and minute, HH:MM, 24 Hr Time/Military Time.", "\n",
                      "Any time from 00:00 to 23:59 can be entered for a 24 hour period to view status... "
                      "OR... Press 'Q' or 'q' to exit application.")
                print("\n")
                user_time_input = input()
                if user_time_input == 'q' or user_time_input == 'Q':
                    print("Goodbye.")
                    exit()
                try:
                    if user_time_input != 'q' and user_time_input != 'Q':
                        (hrs, mins) = user_time_input.split(':')
                        today_date = date.today()
                        user_time = time(int(hrs), int(mins))
                        search_time = datetime.combine(today_date, user_time)
                        print("Status of packages at selected time of: ", user_time_input)
                        print("ID | Address | City | State | Zip Code | Deliver By | Weight | "
                              "Note | Depart Time | Delivered Time | Package Status")
                        print("---------------------------------------------------------------------------------------"
                              "--------------------------------------------------------------------------------------")
                        i = 1
                        while i < len(package_table):
                            item = package_hash.search(i)
                            package_id = item.get_package_id()
                            depart_time = item.get_depart_time()
                            delivered_time_prior = item.get_delivered_time()
                            if search_time <= depart_time:
                                item.set_package_status("At hub.")
                            if depart_time <= search_time < delivered_time_prior:
                                item.set_package_status("En route.")
                            if search_time >= delivered_time_prior:
                                item.set_package_status("Delivered.")
                            address = item.get_address()
                            city = item.get_city()
                            state = item.get_state()
                            zip_code = item.get_zip_code()
                            deliver_by = item.get_deliver_by()
                            weight = item.get_weight()
                            note = item.get_note()
                            delivered_time_former = item.get_delivered_time()
                            package_status = item.get_package_status()

                            print(package_id, "|", address, "|",  city, "|", state, "|", zip_code, "|", deliver_by, "|",
                                  weight, "|", note, "|", depart_time, "|", delivered_time_former, "|", package_status)

                            i += 1

                        print("\n")

                except ValueError:
                    print(" Invalid entry.", "\n", "Please follow instruction options and try again.", "\n")

        user_input = user_menu_input

    print("Goodbye.")


# Create package object and insert into hash table.
# Time: O(n), Space: O(n)
def create_package_object_and_insert_into_hash():
    package_hash = ChainingHashTable.ChainingHashTable()

    with open('Files\WGUPS Package Table.csv') as package_csv_file:
        package_table = pd.read_csv(package_csv_file)

        for package_item in package_table.itertuples():
            package_id = package_item[1]
            address = package_item[2]
            city = package_item[3]
            state = package_item[4]
            zip_code = int(package_item[5])
            deliver_by = package_item[6]
            weight = package_item[7]
            note = package_item[8]
            depart_time = package_item[9]
            delivered_time = package_item[10]
            package_status = package_item[11]

            package = Package.Package(package_id, address, city, state, str(zip_code), deliver_by, weight, note,
                                      depart_time, delivered_time, package_status)

            package_hash.insert(package_id, package)

        package_loading(package_table, package_hash)


# Look up the index for both addresses in the address table, which is just a single list, to use each index to map their
# location in the distance table. The distance table is a 2D Array/Matrix.
# Time: O(n), Space: O(n)
def lookup_coordinates(address1, address2):
    with open('Files\WGUPS address Table.csv') as address_csv_file:
        coordinates = []
        address_table = csv.reader(address_csv_file)
        for address_row in address_table:
            if address1 in address_row:
                index1 = address_row.index(address1)
            if address2 in address_row:
                index2 = address_row.index(address2)
        coordinates.append(index1)
        coordinates.append(index2)
        return coordinates


# Find distance between address by using their index location in address table list to find their matching location in
# (2D Array/Matrix). Then return the value located at the cross section of those row and column indexes.
# Time: O(n), Space: O(n^2)
def find_distance(start_address_id, next_address_id, package_hash):
    with open('Files\WGUPS Distance Table.csv') as distance_csv_file:
        distance_table = csv.reader(distance_csv_file)
        two_d_array = []
        for distance_row in distance_table:
            two_d_array.append(distance_row)
        item1 = package_hash.search(start_address_id)
        start_address = item1.get_address()
        item2 = package_hash.search(next_address_id)
        next_address = item2.get_address()
        dist_coord = lookup_coordinates(start_address, next_address)
        return two_d_array[dist_coord[0]][dist_coord[1]]


# Take each truck package list and deliver each package to the next closest address, starting from hub, and then back
# to hub after final package is delivered. Nearest Neighbor Algorithm used.
# Time: O(n^3), Space: O(n)
def find_closest_address(truck_list, package_hash, truck_depart_time):
    distance_list = []
    start_address_id = 41
    total_distance = 0.0
    hub_depart_time = truck_depart_time

    for id_num in truck_list:
        next_address_id = id_num
        distance_list.append(float(find_distance(start_address_id, next_address_id, package_hash)))

    shortest_distance = min(distance_list)
    shortest_index = distance_list.index(shortest_distance)
    next_address_id = truck_list[shortest_index]
    portion_of_hour = shortest_distance / 18
    deliver_time = portion_of_hour * 60
    deliver_minutes = math.floor(deliver_time)
    deliver_seconds = math.floor((deliver_time - deliver_minutes) * 60)
    time_delivered = hub_depart_time + timedelta(minutes=deliver_minutes, seconds=deliver_seconds)
    total_distance = total_distance + shortest_distance

    item = package_hash.search(next_address_id)
    item.set_depart_time(hub_depart_time)
    item.set_delivered_time(time_delivered)
    start_address_id = next_address_id

    while len(truck_list) > 0:
        distance_list = []
        truck_list.remove(start_address_id)
        next_depart_time = time_delivered

        for id_num in truck_list:
            next_address_id = id_num
            distance_list.append(float(find_distance(start_address_id, next_address_id, package_hash)))

        if len(distance_list) != 0:
            shortest_distance = min(distance_list)
            shortest_index = distance_list.index(shortest_distance)
            next_address_id = truck_list[shortest_index]
            portion_of_hour = shortest_distance / 18
            deliver_time = portion_of_hour * 60
            deliver_minutes = math.floor(deliver_time)
            deliver_seconds = math.floor((deliver_time - deliver_minutes) * 60)
            time_delivered = next_depart_time + timedelta(minutes=deliver_minutes, seconds=deliver_seconds)
            total_distance = total_distance + shortest_distance

            item = package_hash.search(next_address_id)
            item.set_depart_time(hub_depart_time)
            item.set_delivered_time(time_delivered)
            start_address_id = next_address_id

    next_address_id = 41
    distance_back_to_hub = float(find_distance(start_address_id, next_address_id, package_hash))
    total_distance = total_distance + distance_back_to_hub
    portion_of_hour = distance_back_to_hub / 18
    deliver_time = portion_of_hour * 60
    deliver_minutes = math.floor(deliver_time)
    deliver_seconds = math.floor((deliver_time - deliver_minutes) * 60)
    time_arrived = next_depart_time + timedelta(minutes=deliver_minutes, seconds= deliver_seconds)

    return total_distance


# Load each package by taking into account their "deliver_by" times, note/requirements, package capacity limits and
# package availability time.
# Time: O(n), Space: 0(n)
def package_loading(package_table, package_hash):
    truck1_list = []
    truck2_list = []
    truck3_list = []
    need_to_be_loaded = []
    i = 1
    while i <= len(package_table):
        item = package_hash.search(i)
        package_id = item.get_package_id()
        deliver_by = item.get_deliver_by()
        note = item.get_note()
        need_to_be_loaded.append(package_id)
        if item is not None:
            if len(truck1_list) < 16:
                if package_id != 41:
                    if deliver_by != 'EOD' and (note != 'Delayed on flight---will not arrive to depot until 9:05 am' or
                                                note == 'Must be delivered with 13, 15' or
                                                note == 'Must be delivered with 13, 19' or
                                                note == 'Must be delivered with 15, 19'):
                        Truck.T1.set_truck1_list(package_id)
                        truck1_list = Truck.T1.get_truck1_list()

                        need_to_be_loaded.remove(package_id)

            if note == 'Delayed on flight---will not arrive to depot until 9:05 am' or \
                    note == 'Can only be on truck 2':
                if len(truck2_list) < 16:
                    if package_id != 41:
                        Truck.T2.set_truck2_list(package_id)
                        truck2_list = Truck.T2.get_truck2_list()

                        need_to_be_loaded.remove(package_id)

            if len(truck3_list) < 16:
                if package_id != 41:
                    if deliver_by == 'EOD' and (note != 'Delayed on flight---will not arrive to depot until 9:05 am'
                                                and note != 'Can only be on truck 2'):
                        Truck.T3.set_truck3_list(package_id)
                        truck3_list = Truck.T3.get_truck3_list()

                        need_to_be_loaded.remove(package_id)

            if len(need_to_be_loaded) != 0:
                for id_num in need_to_be_loaded:
                    if len(truck1_list) < 16:
                        if int(id_num) != 41:
                            Truck.T1.set_truck1_list(id_num)
                            truck1_list = Truck.T1.get_truck1_list()

                            need_to_be_loaded.remove(id_num)

        today_date = date.today()
        depart_time_1 = time(hour=8, minute=0)
        depart_time_2 = time(hour=9, minute=5)
        depart_time_3 = time(hour=10, minute=30)

        truck1_depart_time = datetime.combine(today_date, depart_time_1)
        truck2_depart_time = datetime.combine(today_date, depart_time_2)
        truck3_depart_time = datetime.combine(today_date, depart_time_3)

        if package_id in truck1_list:
            item = package_hash.search(package_id)
            item.set_depart_time(truck1_depart_time)

        if package_id in truck2_list:
            item = package_hash.search(package_id)
            item.set_depart_time(truck2_depart_time)

        if package_id in truck3_list:
            item = package_hash.search(package_id)
            item.set_depart_time(truck3_depart_time)

        i += 1

    truck1_total_distance = find_closest_address(truck1_list, package_hash, truck1_depart_time)
    truck2_total_distance = find_closest_address(truck2_list, package_hash, truck2_depart_time)
    truck3_total_distance = find_closest_address(truck3_list, package_hash, truck3_depart_time)

    final_total_distance = truck1_total_distance + truck2_total_distance + truck3_total_distance

    user_interface(final_total_distance, package_hash, package_table)


create_package_object_and_insert_into_hash()
