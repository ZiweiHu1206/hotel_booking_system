#This program simulates a booking system of hotels for the booking.
#Ziwei Hu 260889365
import doctest, datetime, random, matplotlib, os
from hotel import Hotel


class Booking:
    """ Represents a booking for the booking system.

    Instance attribute: hotels(list)  """
    
    def __init__(self, hotels):
        """ (list) -> Booking
        Initializes an instance attribute of the same name(hotels) accordingly
        """
        self.hotels = hotels
        
        
    @classmethod
    def load_system(cls):
        """ (None) -> Booking
        Loads in all the hotels in the hotels folder and creates,
        and returns an object of type Booking with said list of hotels.
        
        >>> system = Booking.load_system()
        >>> len(system.hotels)
        3
        >>> system.hotels[0].name
        'The Great Northern Hotel'
        >>> print(system.hotels[0].rooms[314])
        Room 315,Queen,129.99
        """
        #get access to all the folders in the hotels folder
        folder_list = os.listdir('hotels')
        
        #create a list to add Hotel object in
        hotels = []
        
        #iterate through each folder to load each hotel
        for folder in folder_list:
            #skip .DS_Store folder for Mac
            if folder[0] == ".":
                continue
            
            #generate a Hotel object for each folder
            a_hotel = Hotel.load_hotel(folder)
            hotels.append(a_hotel)
            
        return cls(hotels)
        
    
    
    def menu(self):
        """ (None) -> None
        Welcomes the user to the booking system, asks them to select\
        which operation they would like to perform.
        
        >>> booking = Booking.load_system()
        >>> booking.menu()
        Welcome to Booking System
        What would you like to do?
        1        Make a reservation
        2        Cancel a reservation
        3        Look up a reservation
        """
        #display the welcoming message
        print("Welcome to Booking System")
        print("What would you like to do?")
        print("1        Make a reservation")
        print("2        Cancel a reservation")
        print("3        Look up a reservation")
        
        #retrieve input from the user
        user_input = input()
        
        #perform different operation of different selection
        if user_input == "1":
            self.create_reservation()
        elif user_input == "2":
            self.cancel_reservation()
        elif user_input == "3":
            self.lookup_reservation()
        elif user_input == "xyzzy":
            self.delete_reservations_at_random()
            
    
    
    def create_reservation(self):
        """ (None) -> None
        Prompt the user for their name, then display a list\
        of hotels to choose, then a list of room types at the hotel.
        Prompt them for a check-in and check-out date.
        Make the reservation with the given information.
        Print out their booking number and total amount owing.
        
        >> random.seed(137)
        >> booking = Booking.load_system()
        >> booking.create_reservation()
        Please enter your name: Judy
        Hi Judy! Which hotel would you like to book?
        1        The Great Northern Hotel
        2        Overlook Hotel
        1
        Which type of room would you like?
        1        Double
        2        Twin
        3        King
        4        Queen
        1
        Enter check-in date(YYYY-MM-DD): 1989-01-01
        Enter check-out date(YYYY-MM-DD): 1989-01-04
        Ok. Making your reservation for a Double room.
        Your reservation number is: 4191471513010
        Your total amount due is: $459.84.
        Thank you!
        """
        #prompt the user for their name
        user_name = input("Please enter your name: ")
        
        #display a list of hotels for them to choose from
        print("Hi " + user_name + "! Which hotel would you like to book?")
        for i in range(len(self.hotels)):
            print(str(i+1) + "        " + self.hotels[i].name)
            
        hotel_chosen = int(input())
        
        #get the available room types for the hotel chosen
        for i in range(len(self.hotels)):
            if hotel_chosen == i+1:
                room_types = self.hotels[i].get_available_room_types()
                
        #display a list of room types at the hotel
        print("Which type of room would you like?")
        for i in range(len(room_types)):
            print(str(i+1), "        " + room_types[i])
            
        #get the type of room desired from the user
        type_chosen = int(input())
        for i in range(len(room_types)):
            if type_chosen == i+1:
                type_chosen = room_types[i]
                
                
        #prompt the user for check-in and check-out date
        check_in = input("Enter check-in date (YYYY-MM-DD): ")
        check_out = input("Enter check-out date(YYYY-MM-DD): ")
        check_in = check_in.split("-")
        check_out = check_out.split("-")
        
        for element in check_in:
            if element[0] == "0":
                element = element[1:]
        for element in check_out:
            if element[0] == "0":
                element = element[1:]
                
        check_in_date = datetime.date(int(check_in[0]),int(check_in[1]),int(check_in[2]))
        check_out_date = datetime.date(int(check_out[0]),int(check_out[1]),int(check_out[2]))
                
                
        #make the reservation with the given information
        for i in range(len(self.hotels)):
            if hotel_chosen == i+1:
                booking_num = self.hotels[i].make_reservation(user_name,type_chosen,check_in_date,check_out_date)
            
               
        #print out the booking number
        print("Ok. Making your reservation for a " + str(type_chosen) + " room.")
        print("Your reservation number is: " + str(booking_num))
        
        #get the total amount owing and print it
        for i in range(len(self.hotels)):
            if hotel_chosen == i+1:
                total_amount = round(self.hotels[i].get_receipt([booking_num]), 2)
            
        print("Your total amount due is: $" + str(total_amount) + ".")
        print("Thank you!")
        
    
    
    def cancel_reservation(self):
        """ (None) -> None
        Prompts the user to enter a booking number, and tries to\
        cancel the reservation with that booking number(at any hotel).
        If the reservation could not be found, inform the user.
        
        >> booking = Booking.load_system()
        >> booking.cancel_reservation()
        Please enter your booking number: 9998701091820
        Cancelled successfully.
        >> booking.cancel_reservation()
        Please enter your booking number: 9998701091820
        Could not find a reservation with that booking number.
        """
        #prompts the user to enter a booking number
        booking_num = int(input("Please enter your booking number: "))
                          
        #iterate through the hotels to check whether contain the booking number
        cancel_times = 0
        for i in range(len(self.hotels)):
            if booking_num in self.hotels[i].reservations:
                #cancel the reservation if be found
                self.hotels[i].cancel_reservation(booking_num)
                cancel_times += 1
                print("Cancelled successfully.")
        
        #display message if cannot be found
        if cancel_times == 0:
            print("Could not find a reservation with that booking number.")
        
    
    
    def lookup_reservation(self):
        """ (None) -> None
        Lookup the reservation from the booking number enter by user,
        or user's name, hotel name, room number, etc, to find a reservation
        If cannot find one, inform the user.
        
        >> booking = Booking.load_system()
        >> booking.lookup_reservation()
        Do you have your booking number(s)? yes
        Please enter a booking number (or 'end'): 9998701091820
        Please enter a booking number (or 'end'): end
        Reservation found at hotel Overlook Hotel:
        Booking number: 9998701091820
        Name: Jack
        Room reserved: Room 237,Twin,99.99
        Check-in date: 1975-10-30
        Check-out date: 1975-12-24
        Total amount due: $5499.45
        
        >> booking = Booking.load_system()
        >> booking.lookup_reservation()
        Do you have your booking number(s)? no
        Please enter your name: Judy
        Please enter the hotel you are booked at: The Great Northern Hotel
        Enter the reserved room number: 315
        Enter the check-in date (YYYY-MM-DD): 1989-01-01
        Enter the check-out date (YYYY-MM-DD): 1990-01-01
        Reservation found under booking number 3020747285952.
        Here are the details:
        Booking number: 3020747285952
        Name: Judy
        Room reserved: Room 315,Queen,129.99
        Check-in date: 1989-01-01
        Check-out date: 1990-01-01
        Total amount due: $47446.35
        """
        #asks the user if they have their booking number(s)
        have_booking_num = input("Do you have your booking number(s)? ")
        
        
        #if they do, asks them to enter them
        if have_booking_num == "yes":
            booking_num_list = []
            
            booking_num = input("Please enter a booking number (or 'end'): ")
            if len(booking_num) == 13:
                booking_num_list.append(int(booking_num))
            #asks the user to enter booking number until type 'end'
            while booking_num != "end":
                booking_num = input("Please enter a booking number (or 'end'): ")
                if len(booking_num) == 13:
                    booking_num_list.append(int(booking_num))
                
                
            #iterate through each booking number entered to find such a reservation
            for booking_number in booking_num_list:
                found_times = 0
                
                #find the booking number in all hotels
                for i in range(len(self.hotels)):
                    if booking_number in self.hotels[i].reservations:
                        found_times += 1
                        total_amount = round(self.hotels[i].get_receipt([booking_number]),2)
                        
                        #prints the reservation to the screen
                        print("Reservation found at hotel " + self.hotels[i].name + ":")
                        print(self.hotels[i].reservations[booking_number])
                        print("Total amount due: $" + str(total_amount))
                        
                if found_times == 0:
                    print("The booking number is invalid.")
             
             
        #if they do not have their booking number         
        if have_booking_num == "no":
            #asks them to enter their name, hotel name, room number,etc
            name_user = input("Please enter your name: ")
            hotel_name = input("Please enter the hotel you are booked at: ")
            room_number = int(input("Enter the reserved room number: "))
            check_in_date = input("Enter the check-in date (YYYY-MM-DD): ")
            check_out_date = input("Enter the check-out date (YYYY-MM-DD): ")
            
            #get the date object from the user's input date
            check_in = check_in_date.split("-")
            check_out = check_out_date.split("-")
        
            for element in check_in:
                if element[0] == "0":
                    element = element[1:]
            for element in check_out:
                if element[0] == "0":
                    element = element[1:]
                    
            check_in_date = datetime.date(int(check_in[0]),int(check_in[1]),int(check_in[2]))
            check_out_date = datetime.date(int(check_out[0]),int(check_out[1]),int(check_out[2]))
            
            found_times = 0
            #iterate through each hotel to find such a reservation
            for i in range(len(self.hotels)):
                #get the hotel object of the same name as input
                if hotel_name == self.hotels[i].name:
                    
                    #iterate through all booking number of the reservations
                    for booking_number in self.hotels[i].reservations:
                        #check each Reservation object of the booking_number
                        if name_user == self.hotels[i].reservations[booking_number].name:
                            if room_number == self.hotels[i].reservations[booking_number].room_reserved.room_num:
                                if check_in_date == self.hotels[i].reservations[booking_number].check_in:
                                    if check_out_date == self.hotels[i].reservations[booking_number].check_out:
                                        found_times += 1
                                        total_amount = round(self.hotels[i].get_receipt([booking_number]),2)
                                        
                                        #prints the reservation to the screen
                                        print("Reservation found at hotel " + self.hotels[i].name + ":")
                                        print(self.hotels[i].reservations[booking_number])
                                        print("Total amount due: $" + str(total_amount))
            if found_times == 0:
                print("The booking number is invalid.")
                    
            
            
    def delete_reservations_at_random(self):
        """ (None) -> None
        Chooses a hotel at random and delete all of its reservations.
        
        >>> random.seed(1338)
        >>> booking = Booking.load_system()
        >>> booking.delete_reservations_at_random()
        You said the magic word!
        >>> len(booking.hotels[1].reservations)
        0
        >>> len(booking.hotels[0].reservations)
        1
        """
        print("You said the magic word!")
        
        #choose a random hotel
        num_hotels = len(self.hotels)
        random_index = random.randint(0, num_hotels - 1)
        
        #delete all of its reservation
        self.hotels[random_index].reservations = {}
        




    
