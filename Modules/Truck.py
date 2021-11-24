class Truck:  # Built Truck Class
    i = 0

    def __init__(self, truck_id, truck1_list = [], truck2_list = [], truck3_list = []):  # Built Truck Constructor
        self._truck_id = truck_id
        self._truck1_list = truck1_list
        self._truck2_list = truck2_list
        self._truck3_list = truck3_list

    # Setters
    def set_truck_id(self, truck_id):
        self._truck_id = truck_id

    def set_truck1_list(self, truck1_list):
        self._truck1_list.append(truck1_list)

    def set_truck2_list(self, truck2_list):
        self._truck2_list.append(truck2_list)

    def set_truck3_list(self, truck3_list):
        self._truck3_list.append(truck3_list)

    # Getters
    def get_truck_id(self):
        return self._truck_id

    def get_truck1_list(self):
        return self._truck1_list

    def get_truck2_list(self):
        return self._truck2_list

    def get_truck3_list(self):
        return self._truck3_list


T1 = Truck(1)
T2 = Truck(2)
T3 = Truck(3)
