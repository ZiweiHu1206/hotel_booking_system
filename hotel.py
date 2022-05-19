#This program simulates a booking system of hotels for a hotel.
#Ziwei Hu 260889365
import doctest, datetime, random, copy, os, csv
from room import Room, MONTHS, DAYS_PER_MONTH
from reservation import Reservation


class Hotel:
    """ Represents a hotel

    Instance attributes: name(str), rooms(list), reservations(dict)"""
    
    def __init__(self, name, rooms = [], reservations = {}):
        self.name = name
        self.rooms = copy.deepcopy(rooms)
        self.reservations = copy.deepcopy(reservations)
        
        
    def make_reservation(self, name_person, type_room_desired, date1, date2):
        """ (str,str,date,date) -> int
        Creates a reservation for the first available room of that type,\
        returns the booking number of the reservation. Update the attribute.
        
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        1953400675629
        >>> print(h.reservations[1953400675629])
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        #if a room of the specified type is available, creates a reservation 
        if Room.find_available_room(self.rooms, type_room_desired, date1, date2) != None:
            room = Room.find_available_room(self.rooms, type_room_desired, date1, date2)
            a_reservation = Reservation(name_person, room, date1, date2)
        
        #raise an AssertionError if no room of the given type is available
        else:
            raise AssertionError("No room of the given type is available.")
        
        #updates the attribute storing all the hotel reservations
        self.reservations[a_reservation.booking_number] = a_reservation
            
        return a_reservation.booking_number
    
    
    
    def get_receipt(self, booking_num_list):
        """ (list) -> float
        Returns a float indicating the amount of money a user should pay for reservations.
        
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Negget Hotel", [r1, r2, r3])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.get_receipt([num1])
        560.0
        
        >>> date3 = datetime.date(2021, 6, 5)
        >>> num2 = h.make_reservation("Mrs. Santos", "Twin", date1, date3)
        >>> h.get_receipt([num1, num2])
        2375.0
        
        >>> h.get_receipt([123])
        0.0
        """
        payment = 0.0
        
        #iterate through each booking number in the list, add to the price to pay
        for booking_num in booking_num_list:
            if booking_num in self.reservations:
                reservation_object = self.reservations[booking_num]
                
                #gets the number of days for the reservation
                diff = reservation_object.check_out - reservation_object.check_in
                num_days = diff.days
                
                #generates the payment for the reservation
                payment += reservation_object.room_reserved.price * num_days
                
            else:
                continue
            
        return payment
    
    
    
    def get_reservation_for_booking_number(self, booking_num):
        """ (int) -> Reservation
        Returns the reservation object with the given booking number,
        returns None if such a reservation cannot be found.
        
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> rsv = h.get_reservation_for_booking_number(num1)
        >>> print(rsv)
        Booking number: 4191471513010
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        #returns the reservation object with the booking_num
        if booking_num in self.reservations:
            return self.reservations[booking_num]
        else:
            return None
        
    
    
    def cancel_reservation(self, booking_num):
        """ (int) -> None
        Cancels the reservation with the specified booking number.
        
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.cancel_reservation(num1)
        >>> num1 in h.reservations
        False
        >>> r1.availability[(2021, 5)][4]
        True
        """
        #returns the reservation object with the booking_num
        reservation_object = self.get_reservation_for_booking_number(booking_num)
        
        #retrieves the check-in date and check-out date
        check_in_date = reservation_object.check_in
        check_out_date = reservation_object.check_out
        
        #remove the reservation from reservations of the hotel
        del self.reservations[booking_num]
        
        #gets the number of days for the reservation
        diff = check_out_date - check_in_date
        num_days = diff.days
        one_day = datetime.timedelta(days = 1) 
        
        #make available for the room originally reserved
        for date in range(num_days):
            reservation_object.room_reserved.make_available(check_in_date)
            check_in_date += one_day
            
            
            
    def get_available_room_types(self):
        """ (None) -> list
        Returns a list of strings representing the room types available at the hotel.
        
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> types = h.get_available_room_types()
        >>> types.sort()
        >>> types
        ['Queen', 'Twin']
        """
        room_type_available = []
        
        #generates a list of room type available at the hotel
        for a_room in self.rooms:
            if a_room.room_type not in room_type_available:
                room_type_available.append(a_room.room_type)
            else:
                continue
        
        return room_type_available
        
        
    
    @staticmethod
    def load_hotel_info_file(info_file):
        """ (str) -> str,list
        Read in the file at that path and return a 2-tuple of the hotel's name and a\
        list of Room objects.
        
        >>> hotel_name,rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> hotel_name
        'Overlook Hotel'
        >>> print(len(rooms))
        500
        >>> print(rooms[236])
        Room 237,Twin,99.99
        """
        #open the file
        file_object = open(info_file, "r")
        
        #read the file line by line
        line_num = 1
        list_rooms = []
        for line in file_object:
            #get the hotel name when reading the first line of the file
            if line_num == 1:
                hotel_name = line.strip()
            
            #create a Room object each time, append to the list_rooms
            else:
                room_element = line.split(',')
                
                #remove any whitespace in case of one
                for element in room_element:
                    element = element.strip()
                    
                room_object = Room(room_element[1], int(room_element[0][5:]),\
                                   float(room_element[2]))
                list_rooms.append(room_object)
            
            line_num += 1
        
        file_object.close()      
        return hotel_name, list_rooms
                    
    
    
    def save_hotel_info_file(self):
        """ (None) -> None
        Saves the hotel's name and room information into a file hotel_info_txt.
        
        >>> r1 = Room("Double", 101, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> h.save_hotel_info_file()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 101,Double,99.99\\n'
        >>> fobj.close()
        """
        #generate the name of a folder for a hotel
        hotel_name = self.name
        folder_name = ""
        for char in hotel_name:
            if char == " ":
                folder_name += "_"
            else:
                folder_name += char.lower()
        
        #open a new file to write the hotel's name and room information
        file_object = open("hotels/" + folder_name + "/hotel_info.txt", "w")
        file_object.write(self.name + "\n")
        
        for element in self.rooms:
            file_object.write(str(element) + "\n")
        
        file_object.close()
        
        
    
    @staticmethod
    def load_reservation_strings_for_month(folder_name, month, year):
        """ (str,str,int) -> dict
        Loads the CSV file named after the given month and year in the given folder name,
        returns a dictionary, each key is a room number, each value is a list of tuples.
        
        >>> name,rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> h = Hotel(name, rooms, {})
        >>> rsvs = h.load_reservation_strings_for_month('overlook_hotel', 'Oct', 1975)
        >>> print(rsvs[237])
        [(1975, 'Oct', 1, ''), (1975, 'Oct', 2, ''), (1975, 'Oct', 3, ''), (1975, 'Oct', 4, ''), (1975, 'Oct', 5, ''), (1975, 'Oct', 6, ''), (1975, 'Oct', 7, ''), (1975, 'Oct', 8, ''), (1975, 'Oct', 9, ''), (1975, 'Oct', 10, ''), (1975, 'Oct', 11, ''), (1975, 'Oct', 12, ''), (1975, 'Oct', 13, ''), (1975, 'Oct', 14, ''), (1975, 'Oct', 15, ''), (1975, 'Oct', 16, ''), (1975, 'Oct', 17, ''), (1975, 'Oct', 18, ''), (1975, 'Oct', 19, ''), (1975, 'Oct', 20, ''), (1975, 'Oct', 21, ''), (1975, 'Oct', 22, ''), (1975, 'Oct', 23, ''), (1975, 'Oct', 24, ''), (1975, 'Oct', 25, ''), (1975, 'Oct', 26, ''), (1975, 'Oct', 27, ''), (1975, 'Oct', 28, ''), (1975, 'Oct', 29, ''), (1975, 'Oct', 30, '9998701091820--Jack'), (1975, 'Oct', 31, '9998701091820--Jack')]
        """
        #loads the csv file named after the given month and year in the given folder name
        filename = str(year) + "_" + month + ".csv"
        file_object = open("hotels/" + folder_name + "/" + filename, "r")
        file_content = csv.reader(file_object)
        content_list = list(file_content)
       
        #create a dictionary to store value
        reservation_dict = dict()
        
        #read line by line, append the new item to the dictionary
        for r in range(len(content_list)):
            
            rsv_list = []
            for c in range(len(content_list[r])):
                #generate a list of tuples corresponding to the reservation data
                if c == 0:
                    key = int(content_list[r][c])
                elif content_list[r][c] == "":
                    rsv_list.append((year, month, c, ""))
                else:
                    rsv_list.append((year, month, c, content_list[r][c]))
            
            #add a new item with key and value to reservation_dict
            reservation_dict[key] = rsv_list
        
        file_object.close()
        
        return reservation_dict
     
     
    
    def save_reservations_for_month(self, month, year):
        """ (str,int) -> None
        Create a new CSV file named after the given month, contains one row per room
        
        >>> random.seed(987)
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> Reservation.booking_numbers = []
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> num = h.make_reservation("Jack", "Double", date1, date2)
        >>> h.save_reservations_for_month('Oct', 2021)
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        #generate the folder name in hotels folder
        hotel_name = self.name
        folder_name = ""
        for char in hotel_name:
            if char == " ":
                folder_name += "_"
            else:
                folder_name += char.lower()
                
        #generate the filename
        filename = str(year) + "_" + month + ".csv"
        
        #create a new csv file to write
        file_object = open("hotels/" + folder_name + "/" + filename, "w")
        
        #get the first day of the given month for further looping
        first_date = datetime.date(year, MONTHS.index(month) + 1, 1)
        one_day = datetime.timedelta(days = 1) 
        
        #iterate through rooms in the hotel
        for room_obj in self.rooms:
            room_number = room_obj.room_num
            row = str(room_number) + ','
            
            #iterate through each day of the month to check its availability
            for i in range(DAYS_PER_MONTH[MONTHS.index(month)]):
                if not room_obj.is_available(first_date, first_date + one_day):
                    
                    #find the reservation object for this room at given date
                    for booking_num in self.reservations:
                        rsv_obj = self.reservations[booking_num]
                        room_testing = rsv_obj.room_reserved
                        room_num_testing = room_testing.room_num
                        
                        #if the two rooms are the same, generate the short string 
                        if not room_testing.is_available(first_date, first_date + one_day):
                            if room_num_testing == room_number:
                                short_string = rsv_obj.to_short_string()
                                row += short_string + ','
                #if no reservation, add a comma for seperation                
                else:
                    row += ','
                #increase the date by one day
                first_date += one_day
                
            #write to the csv file for each room in the hotel
            file_object.write(row[:-1] + "\n")
        
        file_object.close()
        
    
    
    def save_hotel(self):
        """ (None) -> None
        Saves a file hotel_info.txt with the hotel's name and room information,
        CSV files containing the reservation data. If the folders do not exist, then
        create them.
        
        >>> random.seed(987)
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> Reservation.booking_numbers = []
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> h.make_reservation("Jack", "Double", date1, date2)
        1953400675629
        >>> h.save_hotel()
        
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 237,Double,99.99\\n'
        >>> fobj.close()
        
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        #generate the folder name in hotels folder
        hotel_name = self.name
        folder_name = ""
        for char in hotel_name:
            if char == " ":
                folder_name += "_"
            else:
                folder_name += char.lower()
                
        #check whether the folder exists, if not, create a folder
        if not os.path.exists('hotels/' + folder_name):
            os.makedirs('hotels/' + folder_name)
            
        #save a file hotel_info.txt
        self.save_hotel_info_file()
        
        #if no rooms in a hotel, no CSV files should be created
        if len(self.rooms) == 0:
            return
        
        #retrieve all available months
        availability_dict = self.rooms[0].availability
        
        #save CSV files one for each month in which there are rooms available
        for year, month in availability_dict:
            self.save_reservations_for_month(MONTHS[month - 1], year)
        
        
        
    @classmethod
    def load_hotel(cls, folder_name):
        """ (str) -> Hotel
        Loads the hotel info file and reservation CSV files from folder_name,
        creates and returns an object of type Hotel with the loaded name, rooms, and
        reservation information. Creates Reservation objects first.
        
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> hotel = Hotel.load_hotel('overlook_hotel')
        >>> hotel.name
        'Overlook Hotel'
        >>> str(hotel.rooms[236])
        'Room 237,Twin,99.99'
        >>> print(hotel.reservations[9998701091820])
        Booking number: 9998701091820
        Name: Jack
        Room reserved: Room 237,Twin,99.99
        Check-in date: 1975-10-30
        Check-out date: 1975-12-24
        """
        #get access to all the files in the given folder
        files_list = os.listdir('hotels/' + folder_name)
        
        #iterate through every file in the files_list
        for file in files_list:
            #if the file is the hotel_info.txt, load the hotel info
            if file[-3:] == 'txt':
                hotel_name, list_rooms = Hotel.load_hotel_info_file('hotels/'+folder_name+'/'+file)
                hotel_name.strip()
        
        #create a Hotel object with empty reservations dictionary
        reservations_hotel = {}
        
        hotel_obj = Hotel(hotel_name, list_rooms)
        list_rooms = hotel_obj.rooms
        reservations_hotel = hotel_obj.reservations
            
        #if the file is a CSV file, get all the month and year exist into months_list
        months_list = []
        for file in files_list:
            if file[-3:] == 'csv':
                #get the year and month for this CSV file
                year = int(file[:4])
                month = file[5:8]
                
                #append year and month as a tuple into month_list
                months_list.append((month, year))
                
                
        #set up availability for all the rooms listed in CSV file for that month
        for room in list_rooms:
            for month, year in months_list:
                room.set_up_room_availability([month], year)
                
        #store all reservation strings of one room into rsv_dict,  key is room number   
        rsv_dict = {}
        for month, year in months_list:
            #load the CSV file to get the rsv_dict for each month
            rsv_dict_month = Hotel.load_reservation_strings_for_month(folder_name, month, year)
            
            #iterate through the new dict created to check whether is in rsv_dict
            for room_number in rsv_dict_month:
                if room_number in rsv_dict:
                    rsv_dict[room_number] = rsv_dict_month[room_number] + rsv_dict[room_number]
                else:
                    rsv_dict[room_number] = rsv_dict_month[room_number]
        
        
        #generate a dictionay that key is booking number, value is room object
        for room_num in rsv_dict:
            for room_obj in list_rooms:
                
                if room_obj.room_num == room_num:
                    #get a dictionary that key is a booking number and value is a reservation object
                    rsv_obj_dict = Reservation.get_reservations_from_row(room_obj, rsv_dict[room_num])
        
                    for booking_num in rsv_obj_dict:
                        reservations_hotel[booking_num] = rsv_obj_dict[booking_num] 
        
        return hotel_obj
        
                
    
    
if __name__ == "__main__":
    doctest.testmod()
        
