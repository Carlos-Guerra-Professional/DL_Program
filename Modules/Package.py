class Package:  # Built Package Class

    def __init__(self, package_id, address, city, state, zip_code, deliver_by, weight, note, depart_time,
                 delivered_time, package_status = 'At hub.'):     # Built Package Constructor
        self._package_id = package_id
        self._address = address
        self._city = city
        self._state = state
        self._zip_code = zip_code
        self._deliver_by = deliver_by
        self._weight = weight
        self._note = note
        self._depart_time = depart_time
        self._delivered_time = delivered_time
        self._package_status = package_status

    # Setters
    def set_package_id(self, package_id):
        self._package_id = package_id

    def set_address(self, address):
        self._address = address

    def set_city(self, city):
        self._city = city

    def set_state(self, state):
        self._state = state

    def set_zip(self, zip_code):
        self._zip_code = zip_code

    def set_deliver_by(self, deliver_by):
        self._deliver_by = deliver_by

    def set_weight(self, weight):
        self._weight = weight

    def set_notes(self, note):
        self._note = note

    def set_depart_time(self, depart_time):
        self._depart_time = depart_time

    def set_delivered_time(self, delivered_time):
        self._delivered_time = delivered_time

    def set_package_status(self, package_status):
        self._package_status = package_status

    # Getters
    def get_package_id(self):
        return self._package_id

    def get_address(self):
        return self._address

    def get_city(self):
        return self._city

    def get_state(self):
        return self._state

    def get_zip_code(self):
        return self._zip_code

    def get_deliver_by(self):
        return self._deliver_by

    def get_weight(self):
        return self._weight

    def get_note(self):
        return self._note

    def get_depart_time(self):
        return self._depart_time

    def get_delivered_time(self):
        return self._delivered_time

    def get_package_status(self):
        return self._package_status
