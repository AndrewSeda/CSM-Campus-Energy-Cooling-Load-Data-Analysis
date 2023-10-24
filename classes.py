
#Returns the interval for the first day of summer assuming 15 min intervals
#Parameters:
#Month
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
class Year:
    month_days = []
    end_of_year_int = 0
    def __init__(self) -> None:
        pass
    def __init__(self, year):
        if (year%4 == 0):
            self.month_days = [31,29,31,30,31,30,31,31,30,31,30,31]
        else:
            self.month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
        #Stores a value for the last interval in the year
        self.end_of_year_int = number_of_intervals_to_start_of_month(11, self.month_days) + number_of_intervals_to_day(31, 15)
        return


        
    
def number_of_days_to_month(months: list, month_days: list) -> int:
    """Returns the number of days before the specified month

    Args:
        months (int): The number of months before the target month (Ex: 3 for April)
        month_days (int list): A list containing the number of days in each month

    Returns:
        int: Total number of days before specified month
    """
    
    
    days = sum(month_days[i] for i in range(0,months))
    return int(days)

def number_of_intervals_to_day(day: int, minute_interval: list) -> int:
    """Calculates the interval index corresponding to the desired day

    Args:
        day (int): The day to  convert to an interval
        minute_interval (int): The number of minutes per interval

    Returns:
        int: The interval index for the input day
    """
    multiplier = 24*60/minute_interval
    starting_interval = multiplier*day
    return int(starting_interval)

def number_of_intervals_to_start_of_month(month: int, month_days: list) -> int:
    """Finds the number of days to the start of a month

    Args:
        month (int): The month to find the number of intervals before
        month_days (int list): The number of days in each month

    Returns:
       Int: The interval index corresponding to the first day in the month
    """
    month_starting_day = number_of_days_to_month(month, month_days)
    month_starting_interval = number_of_intervals_to_day(month_starting_day,15)
    return month_starting_interval

INTERVALS_PER_DAY = number_of_intervals_to_day(1,15)  


def check_leap(year: int) -> list:
    """Checks whether the current year is a leap year and adjusts the days per month accordingly

    Args:
        year (int): The year to check leap for

    Returns:
        int list: The number of days in each month
    """    
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if year%4 == 0:
        Leap = True
    else:
         Leap = False
    if Leap == True:
        month_days[1] = 29
    return month_days







class Season:
    #int_first_month = 0
    #int_last_month = 0
    #int_first_day = 0
    #int_last_day = 0
    #list_day_intervals = []
    #list_offset_day_intervals = []
    #list_day_names = []
    #bool_summer = True
    #year = Year(2019)
    #list_interval_range = []
    #list_month_range = []
    #list_month_names = []
    #list_month_interval = []
    #list_month_days = []

    def __init__(self) -> None:
        pass
    def __init__(self, starting_month: int, ending_month: int, starting_day: int, ending_day: int, is_summer: bool, year: Year):
        self.int_first_month = starting_month
        self.int_last_month = ending_month
        self.int_first_day = starting_day
        self.int_last_day = ending_day
        self.year = year
        #Stores a value for the last interval in the year
        self.create_day_array()
        self.bool_summer = is_summer
        self.list_month_range = [starting_month, ending_month]
        self.create_season_set()
        self.season_interval_range()
        return
    def season_interval_range(self) -> list:
        """Generates a list containing the first and last interval index for a range of months

        Args:
            list_season_range (int list): Contains the first and last month to find an interval range for
            month_days (int list): the number of days in a month

        Returns:
            int list: The first and last interval index for a range of months
        """    
        list_starting_interval = number_of_intervals_to_start_of_month(self.int_first_month, self.year.month_days)
        list_starting_interval = list_starting_interval+number_of_intervals_to_day(self.int_first_day,15)
        list_ending_interval = number_of_intervals_to_start_of_month(self.int_last_month, self.year.month_days)
        list_ending_interval = list_ending_interval+number_of_intervals_to_day(self.int_last_day,15)
        self.list_interval_range = []
        self.list_interval_range.append(list_starting_interval)
        self.list_interval_range.append(list_ending_interval)
        #print(len(self.list_interval_range))
        #print(self.list_interval_range)
        return 
    
    
    def create_day_array(self):
        season_day_set = []
        name_set = [] # stores month and day as a set Ex. August 10th is 9/10
        interval_set = [] # Stores the interval that begins each day
        int_day_interval = number_of_intervals_to_start_of_month(self.int_first_month, self.year.month_days) + number_of_intervals_to_day(self.int_first_day,15)
    # If the year changes (i.e. December 2019  to January 2020)
        if(self.int_last_month > self.int_first_month):
            # Iterate through each month in the given range
            for int_month in range(self.int_first_month, self.int_last_month+1):
                # Store the number of month (i.e. April is 4)
                str_month = str(int_month+1)
                # Get the number of days in the month
                int_days_in_month = self.year.month_days[int_month]
                # If it is the first month, need to start on the designated start date
                if int_month == self.int_first_month:
                    # For each day in the month
                    for day in range(self.int_first_day,int_days_in_month):
                        name_set.append(str_month + "/" + str(day+1))
                        # Begin the set of 15 minute intervals at the number of intervals to the first of the month + the number of intervals to the day of the month
                        interval_set.append(int_day_interval) 
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY # Go to the interval that begins the next day
                elif int_month == self.int_last_month:
                    for day in range(0,self.int_last_day):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval)
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY
                else:
                    for day in range(0,int_days_in_month):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval)
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY
            list_offset_intervals = interval_set # Create a new list to store the list of intervals shifted to start at zero
            offset = interval_set[0] # The offset of each interval is equal to the offset of the first interval

            for i in range (0,len(list_offset_intervals)):
                list_offset_intervals[i] = list_offset_intervals[i] - offset
            self.list_offset_day_intervals = list_offset_intervals
        else:
            for int_month in range(self.int_first_month, 12):
                str_month = str(int_month+1)
                int_days_in_month = self.year.month_days[int_month]
                if int_month == self.int_first_month:
                    for day in range(self.int_first_day,int_days_in_month):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval)
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY
                elif int_month == self.int_last_month:
                    for day in range(0,self.int_last_day):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval)
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY
                else:
                    for day in range(0,int_days_in_month):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval)
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY

            list_offset_intervals = interval_set # Create a new list to store the list of intervals shifted to start at zero
            offset = interval_set[0] # The offset of each interval is equal to the offset of the first interval

            for i in range (0,len(list_offset_intervals)):
                list_offset_intervals[i] = list_offset_intervals[i] - offset

            for int_month in range(0,self.int_last_month+1):
                str_month = str(int_month+1)
                int_days_in_month = self.year.month_days[int_month]
                if int_month == self.int_first_month:
                    for day in range(self.int_first_day,int_days_in_month):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval) # No longer needed?
                        list_offset_intervals.append(int_day_interval) # Since the for loop begins at the beginning of the year, offset = 0
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY
                elif int_month == self.int_last_month:
                    for day in range(0,self.int_last_day):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval) # No longer needed?
                        list_offset_intervals.append(int_day_interval)
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY
                else:
                    for day in range(0,int_days_in_month):
                        name_set.append(str_month + "/" + str(day))
                        interval_set.append(int_day_interval) # No longer needed?
                        list_offset_intervals.append(int_day_interval)
                        int_day_interval = int_day_interval + INTERVALS_PER_DAY
            self.list_offset_day_intervals = list_offset_intervals
        
        
        season_day_set.append(name_set)
        season_day_set.append(interval_set)
        self.list_day_intervals = interval_set
        self.list_day_names = name_set

        return season_day_set # Returns the set of intervals corresponding the start of each day in the range with the corresponding name

    def create_season_set(self) -> None: 
        """Generates lists which contain the month names and interval locations for the specified month ranges

        Args:
            list_season_range (list): A list containing integers corresponding to the first and last month of the desired range
            month_days (list): A list containing the number of days in each month
        """

        month_set = []
        month_intervals = [0]
        j = 0
        if self.int_first_month > self.int_last_month:
            for i in range(self.int_first_month,12):
                month_set.append(MONTH_NAMES[i])
                if j > 0:
                    month_intervals.append(int( number_of_intervals_to_day(self.year.month_days[i],15))+month_intervals[j-1])
                j +=1
            for i in range(0,self.int_last_month+1):
                month_set.append(MONTH_NAMES[i])
                if j > 0:
                    month_intervals.append(int( number_of_intervals_to_day(self.year.month_days[i],15))+month_intervals[j-1])
                j +=1
        else:
            for i in range(self.int_first_month,self.int_last_month+1):
                month_set.append(MONTH_NAMES[i])
                if j > 0:
                    month_intervals.append(int( number_of_intervals_to_day(self.year.month_days[i],15))+month_intervals[j-1])
                j +=1
        self.list_month_names = month_set
        self.list_month_interval = month_intervals
        return 


