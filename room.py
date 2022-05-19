#The program simulates a booking system of hotels for its rooms.
#Ziwei Hu 260889365
import doctest
import datetime


MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Room:
    """ Represents a room

    Instance attributes: room_type(str), room_num(int), price(float), availability(dict)
    Class attribute: TYPES_OF_ROOMS_AVAILABLE """
    
    TYPES_OF_ROOMS_AVAILABLE = ['twin', 'double', 'queen', 'king']
    
    def __init__(self, room_type, room_num, price):
        #raise AssertionError if the type of any of the inputs does not match as expected
        if type(room_type) != str or type(room_num) != int or type(price) != float:
            raise AssertionError("The type of input is not correct.")
        
        #raise AssertionError if the room type does not match one of the available types
        type_of_room = room_type.lower()
        if type_of_room not in Room.TYPES_OF_ROOMS_AVAILABLE:
            raise AssertionError("The type of room is not available.")
        
        #raise AssertionError if the room number is not positive
        if room_num <= 0:
            raise AssertionError("The room number is not positive.")
        
        #raise AssertionError if the price is negative
        if price < 0:
            raise AssertionError("The price is not a non-negative number.")
        
        #creates instance attributes that store data that is specific to an object
        self.room_type = room_type
        self.room_num = room_num
        self.price = price
        self.availability = {}
        
        
        
    def __str__(self):
        """ Returns a string representation of a room.

        >>> my_room = Room('Double', 237, 99.99)
        >>> str(my_room)
        'Room 237,Double,99.99'
        
        >>> a_room = Room('Twin', 1, 0.0)
        >>> print(a_room)
        Room 1,Twin,0.0
        
        >>> room_b = Room('king', 1229, 1206.0)
        >>> str(room_b)
        'Room 1229,king,1206.0'
        """
        room = "Room " + str(self.room_num)
        type_room = self.room_type
        price_room = str(self.price)
        return room + "," + type_room + "," + price_room
        
        
        
    def set_up_room_availability(self, months_list, year):
        """ (list,int) -> None
        Updates the availability attribute of the room.
        
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> len(r.availability)
        2
        >>> len(r.availability[(2021, 6)])
        31
        >>> r.availability[(2021, 5)][5]
        True
        >>> print(r.availability[(2021, 5)][0])
        None
        
        >>> r.set_up_room_availability(['Feb'], 2000)
        >>> len(r.availability)
        3
        >>> len(r.availability[(2000, 2)])
        30
        >>> r.availability[(2000, 2)][29]
        True
        
        >>> r.set_up_room_availability(['Feb'], 1700)
        >>> len(r.availability)
        4
        >>> len(r.availability[(1700, 2)])
        29
        """
        #iterate through the months_list, add a new item in availablity dict each time
        for month in months_list:
            #create a tuple of integers represents year and month for the key
            key = (year, MONTHS.index(month) + 1)
            
            #create a list of booleans for the value of the new item
            value = [None]
            #get the number of days of specific month
            days_specific_month = DAYS_PER_MONTH[MONTHS.index(month)]
            
            #if leap year, change the days of February to 29
            if month == 'Feb':
                if year % 4 == 0:
                    days_specific_month = 29
                    if year % 100 == 0 and year % 400 != 0:
                        days_specific_month = 28
            
            #Add True to value for days_specific_month times
            for i in range(days_specific_month):
                value.append(True)
            
            #add a new item in availablity dictionary 
            self.availability[key] = value
         
         
           
    def reserve_room(self, reserve_date):
        """ (date) -> None
        Updates the availability of the room accordingly.
        
        >>> r = Room('Queen', 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.reserve_room(date1)
        >>> r.availability[(2021, 6)][20]
        False
        >>> r.availability[(2021, 5)][15] = False
        >>> date2 = datetime.date(2021, 5, 15)
        >>> r.reserve_room(date2)
        Traceback (most recent call last):
        AssertionError: The room is not available at the given date
        
        >>> date3 = datetime.date(2021, 6, 1)
        >>> r.reserve_room(date3)
        >>> r.availability[(2021, 6)][1]
        False
        >>> r.availability[(2021, 6)][2]
        True
        """
        #retrieve the year, month and day from the date object input
        year = reserve_date.year
        month = reserve_date.month
        day = reserve_date.day
        
        #raise AssertionError if the room is not available at the given date
        if self.availability[(year, month)][day] == False:
            raise AssertionError("The room is not available at the given date")
        
        #update the availability of the room for the given date, change to False
        self.availability[(year, month)][day] = False
        
        
        
    def make_available(self, available_date):
        """ (date) -> None
        Updates the availability of the room at the given date to be True.
        
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.make_available(date1)
        >>> r.availability[(2021, 6)][20]
        True
        >>> r.availability[(2021, 5)][3] = False
        >>> date2 = datetime.date(2021, 5, 3)
        >>> r.make_available(date2)
        >>> r.availability[(2021, 5)][3]
        True
        >>> date3 = datetime.date(2021, 5, 9)
        >>> r.reserve_room(date3)
        >>> r.make_available(date3)
        >>> r.availability[(2021, 5)][9]
        True
        >>> date4 = datetime.date(2021, 6, 1)
        >>> r.make_available(date4)
        >>> r.availability[(2021, 6)][1]
        True
        """
        #retrieve the year, month and day from the date object input
        year = available_date.year
        month = available_date.month
        day = available_date.day
        
        #update the availability of the room for the given date, change to True
        self.availability[(year, month)][day] = True
        
    
    
    def is_available(self, first_date, second_date):
        """ (date,date) -> bool
        Returns True if the room is available every night from the first date(included),\
        to the second date(excluded), returns False otherwise.
        
        >>> r = Room("King", 203, 100.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 5, 25)
        >>> date2 = datetime.date(2021, 6, 10)
        >>> r.is_available(date1, date2)
        True
        >>> r.availability[(2021, 5)][28] = False
        >>> r.is_available(date1, date2)
        False
        
        >>> date3 = datetime.date(2021, 7, 21)
        >>> r.is_available(date1, date3)
        False
        
        >>> r.is_available(date2, date1)
        Traceback (most recent call last):
        AssertionError: The first date is not earlier than the second date
        """
        #raise AssertionError if the first date is not earlier than the second date
        if first_date >= second_date:
            raise AssertionError("The first date is not earlier than the second date")
        
        #get a timedelta object from the two given days
        difference_day = second_date - first_date
        #calculate the difference of days
        num_days = difference_day.days
        #generate a timedelta object represents one day
        one_day = datetime.timedelta(days = 1)

        date = first_date
        date_list = []
        
        #create a list contains all date between first_date and second_date
        for i in range(num_days):
            date_list.append(date)
            date += one_day
            
        #check whether the availability of the room has been set up
        for date in date_list:
            try:
                self.availability[(date.year, date.month)][date.day]
            except KeyError:
                return False
            
        #check whether the room is available every night from the first_date to the second
        for date in date_list:
            if self.availability[(date.year, date.month)][date.day] == False:
                return False
        
        return True
        
        
    
    @staticmethod
    def find_available_room(room_list, type_input, date1, date2):
        """ (list,str,date,date) -> Room
        Returns the first Room from the input list which happens to be available for\
        the specific dates and is of the correct room type. Returns None if no such room.
        
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> r2.set_up_room_availability(['May'], 2021)
        >>> r3.set_up_room_availability(['May'], 2021)
        >>> r1.availability[(2021, 5)][8] = False
        >>> r = [r1, r2, r3]
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> my_room == r3
        True
        >>> r3.availability[(2021, 5)][3] = False
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> print(my_room)
        None
        
        >>> r = Room("King", 110, 120.0)
        >>> r.set_up_room_availability(['Dec'], 2021)
        >>> r.set_up_room_availability(['Jan'], 2022)
        >>> date1 = datetime.date(2021, 12, 20)
        >>> date2 = datetime.date(2022, 1, 8)
        >>> my_room = Room.find_available_room([r], 'Queen', date1, date2)
        >>> print(my_room)
        None
        >>> my_room = Room.find_available_room([r], 'King', date1, date2)
        >>> my_room == r
        True
        """
        #raise an AssertionError if date1 is not earlier than date2
        if date1 >= date2:
            raise AssertionError("The check in date does not happen to be earlier than "+
                                  "the check out date.")
        
        #iterate through each room in the input list to check availabiliy
        for room in room_list:
            if room.is_available(date1, date2) and room.room_type == type_input:
                return room
        
        #if there is no such room, return None
        return None
            
    
        
        
if __name__ == "__main__":
    doctest.testmod()
        
        