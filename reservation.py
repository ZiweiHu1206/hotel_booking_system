#This program simulates a booking system of hotels for its reservation.
#Ziwei Hu 260889365
import doctest, datetime, random
from room import Room, MONTHS, DAYS_PER_MONTH


class Reservation:
    """ Represents a reservation
    
    Instance attributes: booking_number(int), name(str), room_reserved(Room),\
                         check_in(date), check_out(date)
    Class attributes: booking_numbers(list) """
    
    booking_numbers = []
    
    def __init__(self, name, room, date1, date2, booking_num = None):
        """ (str,Room,date,date,int) -> Reservation
        Initializes a object of type Reservation by the given arguments.
        
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation("Mrs.Santos", r1, date1, date2)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-10
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][9]
        False
        """
        #raise AssertionError if room_input is not available at the specified dates
        if not room.is_available(date1, date2):
            raise AssertionError("The input room is not available at the specified dates.")
        
        #initialize all the instance attributes
        self.name = name
        self.check_in = date1
        self.check_out = date2
        self.booking_number = booking_num
        
        #raise AssertionError if booking_num input had already been used for not 13 digit
        if self.booking_number != None:
            if len(str(self.booking_number)) != 13:
                raise AssertionError("The booking number is invalid.")
            if self.booking_number in Reservation.booking_numbers:
                raise AssertionError("The booking number is invalid.")
            if str(self.booking_number)[0] not in "123456789":
                raise AssertionError("The booking number is invalid.")
        
        #if booking_num is not provided, generates a new random 13 digit number
        if self.booking_number == None:
            self.booking_number = random.randint(1000000000000, 9999999999999)
        while self.booking_number in Reservation.booking_numbers:
            self.booking_number = random.randint(1000000000000, 9999999999999)
            
            
        #updates the class attribute booking_numbers
        Reservation.booking_numbers.append(self.booking_number)
        
        #get a timedelta object from the two given days, calculate the difference of days
        diff = date2 - date1
        num_days = diff.days
        one_day = datetime.timedelta(days = 1) #generate a timedelta object for one day
        
        date = date1
        date_list = []
        
        #create a list contains all date between first_date and second_date
        for i in range(num_days):
            date_list.append(date)
            date += one_day                      
        
        #reserve the specified room for all nights from date1 to date2
        for date in date_list:
            room.reserve_room(date)
           
        #initiates the intance attribute of room_reserved
        self.room_reserved = room
        
    
    
    def __str__(self):
        """ (Reservation) -> None
        Returns a string representation of a reservation containing the booking number,\
        name on the reservation, room reserved and check-in and out dates.
        
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation)
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        #generates the string representation of every piece of information
        booking_num = "Booking number: " + str(self.booking_number) + "\n"
        name_reserved = "Name: " + self.name + "\n"
        room_reserved = "Room reserved: " + str(self.room_reserved) + "\n"
        check_in_date = "Check-in date: " + str(self.check_in) + "\n"
        check_out_date = "Check-out date: " + str(self.check_out)
        
        return booking_num + name_reserved + room_reserved + check_in_date + check_out_date
    
    
    
    def to_short_string(self):
        """ (None) -> str
        Returns a string containing the booking number and name on the reservation.
        
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> my_reservation.to_short_string()
        '1953400675629--Mrs. Santos'
        """
        #generates a short string containing the booking number and name of reservation
        booking_num = str(self.booking_number)
        name_reservation = self.name
        
        return booking_num + "--" + name_reservation 


    
    @classmethod
    def from_short_string(cls, short_string, date1, date2, room):
        """ (str,date,date) -> Reservation
        Creates and returns an object of type Reservation for a stay in the specified room.
        
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 4)
        >>> my_reservation = Reservation.from_short_string('1953400675629--Mrs. Santos',\
                                                            date1, date2, r1)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-04
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][3]
        False
        """
        #Retrieve the booking number and name of reservation
        booking_number = int(short_string[0:13])
        name = short_string[15:]
        
        return cls(name, room, date1, date2, booking_number)
    
    
    
    @staticmethod
    def get_reservations_from_row(room, reservation_strings):
        """ (Room,list) -> dict
        Returns a dictionary where each key is a booking number and each value is the\
        reservation object for that booking number.
        
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(MONTHS, 2021)
        >>> rsv_strs = [(2021, 'May', 4, '1953400675629--Jack'),\
                        (2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 8, '')]
        >>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
        >>> print(rsv_dict[1953400675629])
        Booking number: 1953400675629
        Name: Jack
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-05
        """
        #creates a dictionary, generate a timedelta object for one day
        reservation_dict = dict()
        one_day = datetime.timedelta(days = 1) 
        
        
        #iterates through each tuple in reservation_strings to reserve the room
        for tup in reservation_strings:
            #if the tuple has empty reservation string, skip to the next iteration
            if tup[3] == '':
                continue
            
            booking_num = int(tup[3][0:13])
            #if no reservation for the booking number in the tuple
            if booking_num not in Reservation.booking_numbers:
                min_date = datetime.date(int(tup[0]), MONTHS.index(tup[1]) + 1, int(tup[2]))
                max_date = datetime.date(int(tup[0]), MONTHS.index(tup[1]) + 1, int(tup[2]))
                
                #find the minimum day as the check-in date and maximum day as check_out
                for tup2 in reservation_strings:
                    if tup2[3] == '':
                        continue
                    elif int(tup2[3][0:13]) == booking_num:
                        date = datetime.date(int(tup2[0]), MONTHS.index(tup2[1]) + 1, int(tup2[2]))
                        if date < min_date:
                            min_date = date
                        elif date > max_date:
                            max_date = date
                    
                max_date += one_day
                
                #generate a reservation, add it to the reservation dictionary
                rsv = Reservation.from_short_string(tup[3], min_date, max_date, room)
                reservation_dict[booking_num] = rsv
                
            #if booking number in the tuple already has reservation, skip to next iteration
            if booking_num in Reservation.booking_numbers:
                continue
                
        return reservation_dict



        
if __name__ == "__main__":
    doctest.testmod()
        
        
     