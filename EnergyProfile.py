from classes import*
import pandas as pd
import numpy as np

class EnergyProfile:
    def __init__(self) -> None:
        pass
    def __init__(self, summer_season: Season, winter_season: Season, df: pd.DataFrame):
        self.summer_season = summer_season
        self.winter_season = winter_season
        self.df = df

        self.summer_energy_usage = []
        self.winter_energy_usage = []
        self.create_season_energy()
        self.cooling_energy_simple = []
        self.get_all_cooling()
        
        self.winter_weekday_energy_usage = [] # Previously winter_weekday_dataset
        self.winter_weekend_energy_usage = []
        self.summer_weekday_energy_usage = []
        self.summer_weekend_energy_usage = []
        self.cooling_weekday_energy_usage = []
        self.cooling_weekend_energy_usage = []
        self.get_interval_average_datasets()

        self.summer_interval_average_energy_usage = []
        self.summer_weekday_average_energy_usage = []
        self.summer_weekend_average_energy_usage = []

        self.winter_interval_average_energy_usage = []
        self.winter_weekday_average_energy_usage = []
        self.winter_weekend_average_energy_usage = []
        self.get_season_daily_averages()

        #list_compiled_energy ? Not needed

        self.cooling_interval_average = []
        self.weekend_cooling_interval_average = []
        self.weekday_cooling_interval_average = []
        self.get_interval_cooling()

        self.winter_day_of_the_week_average_energy_usage = []
        self.get_day_of_the_week_averages() # Only needed for winter?
        self.winter_day_of_week_seperated_interval_average_data = []
        self.get_day_of_the_week_seperated_interval_average_data() # Also only needed for winter?

        self.cooling_day_of_the_week_data = []
        self.winter_day_of_the_week_data = []
        self.summer_day_of_the_week_data = []
        self.create_cooling_energy()

        self.cooling_season_energy_typical_winter_intervals = []
        self.create_cooling_data_by_interval(1) # Arbitrary starting day

        self.compiled_energy = [self.summer_energy_usage[self.summer_season.year.year],self.winter_energy_usage[self.summer_season.year.year],self.cooling_energy_simple[self.summer_season.year.year]]


        return
    
    def break_range(self, break_starting_day: int, break_ending_day: int) -> list:
        """Generates an interval range for the days to exclude from the data

        Args:
            break_starting_day (int): The first day to be excluded
            break_ending_day (int): The last day to be exluded

        Returns:
            int list: Contains the first and last interval index for the specified break
        """    
        break_starting_interval = int(number_of_intervals_to_day(break_starting_day, 15))
        break_ending_interval = int(number_of_intervals_to_day(break_ending_day, 15))
        break_range_set = [break_starting_interval, break_ending_interval]
        return break_range_set
    
    def create_season_energy(self) ->list:
        """ Creates a 2 dimensional list with each index holding the energy use in Watts of the Mines campus for the given season each year.
            The season is stored in the season object

        Args:
            season (Season): A season object for the desired season
            df (DataFrame): The dataframe which contains the energy data of the Mines campus in Watts in 15 minute intervals

        Returns:
            list: A list containing the energy use in 15 minute intervals for the desired time frames. The last 7 items contains the list of 
            averages for each day of the week. The 8th to last row contains the list of overall averages for each time of day.
        """
                
        # Initializes a nested array for each year + avg 
        #MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
        #month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
        list_summer_season_energy = []
        list_winter_season_energy = []
        year_num = 2008 # Beginning in 2008
        cols = self.df.columns # Columns store the year
        for i in range(0,len(cols)):
            # Initialize a Year object with the current year
            year = Year(year_num)
            year_num +=1 # Increment the year
            
            # Find the interval range for winter break (Dec 15 to Jan 10)
            break_range_set = self.break_range(number_of_days_to_month(11, year.month_days)+15,10)
            # Get a single year of seasonal energy data
            list_summer_season_row = self.season_energy(self.summer_season.list_interval_range, year.int_end_of_year, break_range_set, self.df, i)
            list_winter_season_row = self.season_energy(self.winter_season.list_interval_range, year.int_end_of_year, break_range_set, self.df, i)
            # Add the single year of seasonal energy data to a list containing all the years of seasonal energy data
            list_summer_season_energy.append(list_summer_season_row)
            list_winter_season_energy.append(list_winter_season_row)
            

        list_summer_season_energy = self.season_averages(list_summer_season_energy)
        list_summer_season_energy = self.season_weekday_averages(list_summer_season_energy, True)
        list_winter_season_energy = self.season_averages(list_winter_season_energy)
        list_winter_season_energy = self.season_weekday_averages(list_winter_season_energy, False)

        self.summer_energy_usage = list_summer_season_energy
        self.winter_energy_usage = list_winter_season_energy
        return 

    def season_energy(self, list_season_range: list, end_of_year: int, time_to_exclude: list, df,  i: int):
        """ Creates a list containing all of the intervals for the given season in order while exluding all breaks.

        Args:
            list_season_range (list): A e element int list contatining the first and last interval of the season
            end_of_year (int): The interval corresponding to the last day of the year
            time_to_exclude (list): A 2 element int list containing the first and last interval of the break
            df (DataFrame): The dataframe to extract data from
            i (int): Integer corresponding to a column (year) in the dataframe

        Returns:
            _type_: _description_
        """

        cols = df.columns # Columns store the year from 2008 to 2019
        
        bool_exclude_time = False
        list_season_row = []

        # Not sure what this is for
        if(bool_exclude_time != 0):
            bool_exclude_time = True

        # Check if the year changes between the first and last month i.e. December 2018 to January 2019
        if(list_season_range[0] > list_season_range[1]):
            # Iterate from the start of the season to the end of the year
            for j in range(list_season_range[0], end_of_year):
                # If we are exluding a break and the current interval is greater than the beginning of the break
                if( bool_exclude_time == True and j >time_to_exclude[0]):
                    # Append the row with the data from the same interval on the previous day to make sure data is similar
                    # Improve this by skipping this section of data entirely
                    list_season_row.append(list_season_row[j-96])
                    continue
                # If it is not part of the break
                else:
                    list_season_row.append(df.at[j,cols[i]]) 
            for j in range(0, list_season_range[1]):
                if( bool_exclude_time == True and j < time_to_exclude[1]):
                    list_season_row.append(list_season_row[j-96])
                    continue
                else:
                    list_season_row.append(df.at[j,cols[i]])
        else:
            for k in range(list_season_range[0],list_season_range[1]):
                list_season_row.append(df.at[k, cols[i]])
        return list_season_row

    def cooling_energy(self, list_season_range: list, end_of_year: int, time_to_exclude: list, df: pd.DataFrame,  i: int, list_winter_day_of_week_seperated_interval_average_data: list):
        """ Creates a list containing all of the intervals for the given season in order while exluding all breaks.

        Args:
            list_season_range (list): A e element int list contatining the first and last interval of the season
            end_of_year (int): The interval corresponding to the last day of the year
            time_to_exclude (list): A 2 element int list containing the first and last interval of the break
            df (DataFrame): The dataframe to extract data from
            i (int): Integer corresponding to a column (year) in the dataframe

        Returns:
            _type_: _description_
        """

        cols = self.df.columns # Columns store the year from 2008 to 2019
        
        bool_exclude_time = False
        list_season_row = []
        list_winter_row = []
        list_summer_row = []

        # Not sure what this is for
        if(bool_exclude_time != 0):
            bool_exclude_time = True
        #print(len(list_winter_day_of_week_seperated_interval_average_data))
        #print(len(list_winter_day_of_week_seperated_interval_average_data[0]))
        # Check if the year changes between the first and last month i.e. December 2018 to January 2019
        if(list_season_range[0] > list_season_range[1]):
            # Iterate from the start of the season to the end of the year
            for j in range(list_season_range[0], end_of_year):
                day = 0
                if j%672 < 96:
                    day = 0
                elif j%672 < 96*2:
                    day = 1
                elif j%672 < 96*3:
                    day = 2
                elif j%672 < 96*4:
                    day = 3
                elif j%672 < 96*5:
                    day = 4
                elif j%672 < 96*6:
                    day = 5
                else:
                    day = 6
                # If we are exluding a break and the current interval is greater than the beginning of the break
                if( bool_exclude_time == True and j >time_to_exclude[0]):
                    # Append the row with the data from the same interval on the previous day to make sure data is similar
                    # Improve this by skipping this section of data entirely
                    list_season_row.append(list_season_row[j-96])
                    continue
                # If it is not part of the break
                else:
                    
                    list_season_row.append(df.at[j,cols[i]] - list_winter_day_of_week_seperated_interval_average_data[day, j%95]) 
                    list_winter_row.append(list_winter_day_of_week_seperated_interval_average_data[day][j%95])
            for j in range(0, list_season_range[1]):
                if( bool_exclude_time == True and j < time_to_exclude[1]):
                    list_season_row.append(list_season_row[j-96])
                    continue
                else:
                    list_season_row.append(df.at[j,cols[i]]- list_winter_day_of_week_seperated_interval_average_data[day][ j%95])
                    list_winter_row.append(list_winter_day_of_week_seperated_interval_average_data[day][ j%95])
                    
        else:
            for k in range(list_season_range[0],list_season_range[1]):
                #print(k)
                #print(k%96)
                #list_winter_day_of_week_seperated_interval_average_data[k%96]
                
                day = 0
                if k%665 < 95:
                    day = 4
                elif k%665 < 95*2:
                    day = 5
                elif k%665 < 95*3:
                    day = 6
                elif k%665 < 95*4:
                    day = 0
                elif k%665 < 95*5:
                    day = 1
                elif k%665 < 95*6:
                    day = 2
                else:
                    day = 3
                # k%96 is the interval in the day
                # day is the day of the week to get data from
                list_season_row.append(df.at[k, cols[i]] - list_winter_day_of_week_seperated_interval_average_data[day][k%95]) 
                list_winter_row.append(list_winter_day_of_week_seperated_interval_average_data[day][k%95])
                list_summer_row.append(df.at[k, cols[i]])
        return list_season_row,  list_winter_row, list_summer_row
    def season_averages(self, list_season_energy: list) -> list:
        """ Appends the list of season energy with the average at each time of day

        Args:
            list_season_energy (list): The list containing the energy use (Watts) of the Mines campus in 15 minute interval for a given season

        Returns:
            list: An appended list of season energy
        """
        list_average_row = []
        for interval in range(0,len(list_season_energy[1])-1):
            sum_of_season =0
            for year in range(0,len(list_season_energy)):
                sum_of_season += list_season_energy[year][interval]
            average_season = sum_of_season/len(list_season_energy)
            list_average_row.append(average_season)
        list_season_energy.append(list_average_row)
        return list_season_energy
# Generates daily averages across the length of list_season_energy
    def season_weekday_averages(self, list_season_energy, bool_is_summer) ->list:
        """_summary_

        Args:
            list_season_energy (_type_): _description_
            bool_is_summer (_type_): _description_

        Returns:
            list: _description_
        """
        list_average_weekday_row = []
        list_average_weekend_row = []
        interval_tracker = 0
        day_count = 0

        weekday_int_tracker = 0
        # This  loops through each interval in a day
        # The nested loop causes each interval in a day to be averaged for every 
        # occurance of that interval before continuing to the next interval
        for interval in range(0,len(list_season_energy[1])-1):
            sum_weekday_season =0
            sum_weekend_season = 0
            weekday_count = 0
            weekend_count = 0
            
            for year in range(0,len(list_season_energy)):
                if year == 0:
                    if bool_is_summer == True:
                        weekday_int_tracker = 0
                    else:
                        weekday_int_tracker = 96
                elif year == 1:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96
                    else:
                        weekday_int_tracker = 96*2
                elif year == 2:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*2
                    else:
                        weekday_int_tracker = 96*3
                elif year == 3:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*3
                    else:
                        weekday_int_tracker = 96*4
                elif year == 4:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*5
                    else:
                        weekday_int_tracker = 96*6
                elif year == 5:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*6
                    else:
                        weekday_int_tracker = 0
                elif year == 6:
                    if bool_is_summer == True:
                        weekday_int_tracker = 0
                    else:
                        weekday_int_tracker = 96
                elif year == 7:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96
                    else:
                        weekday_int_tracker = 96*2
                elif year == 8:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*3
                    else:
                        weekday_int_tracker = 96*4
                elif year == 9:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*4
                    else:
                        weekday_int_tracker = 96*5
                elif year == 10:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*5
                    else:
                        weekday_int_tracker = 96*6
                elif year == 11:
                    if bool_is_summer == True:
                        weekday_int_tracker = 96*6
                    else:
                        weekday_int_tracker = 0      
                weekday_int_tracker += interval
                weekday_int_tracker = weekday_int_tracker % (96*7)
                if weekday_int_tracker < 96 or weekday_int_tracker >= (96*6):
                    sum_weekend_season += list_season_energy[year][interval]
                    weekend_count +=1
                else:
                    sum_weekday_season += list_season_energy[year][interval]
                    weekday_count +=1
                if interval_tracker == 76:
                    interval_tracker = 0
                    day_count +=1
                #dataSortedByInterval[day_count]
            average_weekend_season = 0
            average_weekday_season = 0
            average_weekend_season = sum_weekend_season/weekend_count
            average_weekday_season = sum_weekday_season/weekday_count
            list_average_weekday_row.append(average_weekday_season)
            list_average_weekend_row.append(average_weekend_season)
        list_season_energy.append(list_average_weekday_row)
        list_season_energy.append(list_average_weekend_row)

        return list_season_energy

    def get_all_cooling(self) -> list:
        """Returns a list containing the continuous difference between the energy uses of two seasons

        Args:
            season_one_energy (_type_): _description_
            season_two_energy (_type_): _description_
            year_selected (_type_): _description_

        Returns:
            list: _description_
        """
        list_cooling_energy=[]
        
        #print(len(season_one_energy), "\n")
        for i in range(0,12):
            list_year_cooling = []
            #i=b+2008
            if(len(self.winter_energy_usage[i]) > len(self.summer_energy_usage[i])):
                for h in range(0,len(self.summer_energy_usage[i])-1):
                    list_year_cooling.append(self.summer_energy_usage[i][h]-self.winter_energy_usage[i][h])
            else:
                for h in range(0,len(self.winter_energy_usage[i])-1):
                    list_year_cooling.append(self.summer_energy_usage[i][h]-self.winter_energy_usage[i][h])
            list_cooling_energy.append(list_year_cooling)
        list_cooling_energy = self.season_averages(list_cooling_energy)
        list_cooling_energy = self.season_weekday_averages(list_cooling_energy, True)
        self.cooling_energy_simple = list_cooling_energy
        return 
    
    def get_interval_average_datasets(self):
        self.winter_weekday_energy_usage =  self.interval_average_dataset(self.winter_energy_usage, 13) # 13 is weekday, 14 is weekend
        self.winter_weekend_energy_usage =  self.interval_average_dataset(self.winter_energy_usage, 14)
        self.summer_weekday_energy_usage =  self.interval_average_dataset(self.summer_energy_usage, 13) # 13 is weekday, 14 is weekend
        self.summer_weekend_energy_usage =  self.interval_average_dataset(self.summer_energy_usage, 14)
        self.cooling_weekday_energy_usage =  self.interval_average_dataset(self.cooling_energy_simple, 13) # 13 is weekday, 14 is weekend
        self.cooling_weekend_energy_usage =  self.interval_average_dataset(self.cooling_energy_simple, 14)

    def interval_average_dataset(self, list_season_energy, year_selected: int) -> list:
        """ Returns a list of the average energy use over the season for each 15 minute interval in a day.

        Args:
            list_season_energy (_type_): _description_
            year_selected (_type_): _description_

        Returns:
            list: _description_
        """
        list_interval_seperated = []
        
        #Loops through all intervals for a 24hour period to construct a list
        # which contains the data seperated by interval
        #First loop goes through the first interval of each day
        # Inner loop goes through all the intervals for the day provided by the first interval
        for k in range(0,INTERVALS_PER_DAY):
            list_daily_set = []
            for i in range(0,len(list_season_energy[year_selected])-INTERVALS_PER_DAY,INTERVALS_PER_DAY):
                list_daily_set.append(list_season_energy[year_selected][k+i])
            list_interval_seperated.append(list_daily_set)
        list_daily_set = []
        # Constructs an array containing the standard deviation 
        for b in range(0,INTERVALS_PER_DAY):
            list_daily_set.append(np.std(list_interval_seperated[b]))
        list_interval_seperated.append(list_daily_set)
    
        return list_interval_seperated
    
    def get_season_daily_averages(self):
        self.summer_interval_average_energy_usage, self.summer_weekday_average_energy_usage , self.summer_weekend_average_energy_usage = self.season_daily_averages(self.summer_energy_usage, self.summer_season.year.year)
        self.winter_interval_average_energy_usage, self.winter_weekday_average_energy_usage , self.winter_weekend_average_energy_usage = self.season_daily_averages(self.winter_energy_usage, self.winter_season.year.year)

    def season_daily_averages(self, list_season_energy, year_selected):
        """_summary_

        Args:
            list_season_energy (_type_): _description_
            year_selected (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        list_seasonal_interval_average = self.interval_average(list_season_energy, year_selected)
        list_seasonal_weekday_interval_average = self.interval_average(list_season_energy,  13)
        list_seasonal_weekend_interval_average = self.interval_average(list_season_energy, 14)
        return list_seasonal_interval_average, list_seasonal_weekday_interval_average, list_seasonal_weekend_interval_average
    
    def interval_average(self, list_season_energy, year_selected) -> list:
        """_summary_

        Args:
            list_season_energy (_type_): _description_
            year_selected (_type_): _description_

        Returns:
            list: _description_
        """
        list_interval_average_per_day = []
        
        
        #Loops through all intervals for a 24hour period to construct a list
        # which contains the data seperated by the day
        #First loop goes through the first interval of each day
        # Inner loop goes through all the intervals for the day provied by the first interval
        
        for k in range(0,INTERVALS_PER_DAY):
            season_day_sum = 0
            season_day_average = 0
            for i in range(0,len(list_season_energy[year_selected])-INTERVALS_PER_DAY,INTERVALS_PER_DAY):
                season_day_sum += list_season_energy[year_selected][k+i]
            season_day_average = season_day_sum/((len(list_season_energy[year_selected])-1)/INTERVALS_PER_DAY)
            list_interval_average_per_day.append(season_day_average)
        #print(len(list_interval_average_per_day))
        return list_interval_average_per_day

    
    def get_interval_cooling(self):
        self.cooling_interval_average = self.interval_cooling(self.summer_interval_average_energy_usage, self.winter_interval_average_energy_usage)
        self.weekend_cooling_interval_average = self.interval_cooling(self.summer_weekend_average_energy_usage, self.winter_weekend_average_energy_usage)
        self.weekday_cooling_interval_average = self.interval_cooling(self.summer_weekday_average_energy_usage, self.winter_weekday_average_energy_usage)

    def interval_cooling(self, summer_energy, winter_energy) ->list: # Formerly get_cooling_day
        """_summary_

        Args:
            list_summer_interval_average (_type_): _description_
            list_winter_interval_average (_type_): _description_

        Returns:
            list: _description_
        """
        list_cooling_interval_average = []
        for i in range(0,len(summer_energy)):
            list_cooling_interval_average.append(summer_energy[i]-winter_energy[i])
        return list_cooling_interval_average
    
    def get_day_of_the_week_averages(self):
        self.winter_day_of_the_week_average_energy_usage = self.season_day_of_the_week_averages(self.winter_energy_usage, self.winter_season.year.year, self.winter_season.bool_summer)

    def season_day_of_the_week_averages(self, list_season_energy, bool_is_summer, year) -> list:
        """_summary_

        Args:
            list_season_energy (_type_): _description_
            bool_is_summer (_type_): _description_

        Returns:
            list: _description_
        """
        list_average_mon_row = []
        list_average_tues_row = []
        list_average_wed_row = []
        list_average_thur_row = []
        list_average_fri_row = []
        list_average_sat_row = []
        list_average_sun_row = []
    

        weekday_int_tracker = 0
        # This  loops through each interval in a day
        # The nested loop causes each interval in a day to be averaged for every 
        # occurance of that interval before continuing to the next interval
        # Year key:
        # 0 = 2008
        # 1 = 2009
        # 2 = 2010
        # 3 = 2011
        # 4 = 2012
        # 5 = 2013
        # 6 = 2014
        # 7 = 2015
        # 8 = 2016
        # 9 = 2017
        # 10 = 2018
        # 11 = 2019
        

        for interval in range(0,len(list_season_energy)-1):
            if year == 0:
                if bool_is_summer == True: # If summer 2008, the first interval is on a monday
                    weekday_int_tracker = 0
                else: # Else it is winter 2008, and the first interval is on a Tuesday
                    weekday_int_tracker = 96
            elif year == 1:
                if bool_is_summer == True:
                    weekday_int_tracker = 96
                else:
                    weekday_int_tracker = 96*2
            elif year == 2:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*2
                else:
                    weekday_int_tracker = 96*3
            elif year == 3:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*3
                else:
                    weekday_int_tracker = 96*4
            elif year == 4:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*5
                else:
                    weekday_int_tracker = 96*6
            elif year == 5:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*6
                else:
                    weekday_int_tracker = 0
            elif year == 6:
                if bool_is_summer == True:
                    weekday_int_tracker = 0
                else:
                    weekday_int_tracker = 96
            elif year == 7:
                if bool_is_summer == True:
                    weekday_int_tracker = 96
                else:
                    weekday_int_tracker = 96*2
            elif year == 8:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*3
                else:
                    weekday_int_tracker = 96*4
            elif year == 9:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*4
                else:
                    weekday_int_tracker = 96*5
            elif year == 10:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*5
                else:
                    weekday_int_tracker = 96*6
            elif year == 11:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*6
                else:
                    weekday_int_tracker = 0      
            weekday_int_tracker += interval
            weekday_int_tracker = weekday_int_tracker % (96*7)
            # weekday_int_tracker details:
                # 0 - 96 = Sunday
                # 96 - 96*2 = Monday
                # 96*2 - 96*3 = Tuesday
                # 96*3 - 96*4 = Wednesday
                # 96*4 - 96*5 = Thursday
                # 96*5 - 96*6 = Friday
                # 96*6 - 96*7 = Saturday
            if weekday_int_tracker < 96:
                list_average_sun_row.append(list_season_energy[interval])
            elif weekday_int_tracker < 96*2:
                list_average_mon_row.append(list_season_energy[interval])
            elif weekday_int_tracker < 96*3:
                list_average_tues_row.append(list_season_energy[interval])
            elif weekday_int_tracker < 96*4:
                list_average_wed_row.append(list_season_energy[interval])
            elif weekday_int_tracker < 96*5:
                list_average_thur_row.append(list_season_energy[interval])
            elif weekday_int_tracker < 96*6:
                list_average_fri_row.append(list_season_energy[interval])
            else:
                list_average_sat_row.append(list_season_energy[interval])
            #dataSortedByInterval[day_count]


        list_day_of_the_week_seperated_interval_data = []
        
        
        list_day_of_the_week_seperated_interval_data.append(list_average_mon_row)
        list_day_of_the_week_seperated_interval_data.append(list_average_tues_row)
        list_day_of_the_week_seperated_interval_data.append(list_average_wed_row)
        list_day_of_the_week_seperated_interval_data.append(list_average_thur_row)
        list_day_of_the_week_seperated_interval_data.append(list_average_fri_row)
        list_day_of_the_week_seperated_interval_data.append(list_average_sat_row)
        list_day_of_the_week_seperated_interval_data.append(list_average_sun_row)

        return list_day_of_the_week_seperated_interval_data
    
    def get_day_of_the_week_seperated_interval_average_data(self):
        self.winter_day_of_week_seperated_interval_average_data = self.create_day_of_the_week_seperated_interval_average_data(self.winter_day_of_the_week_average_energy_usage)

    def create_day_of_the_week_seperated_interval_average_data(self, list_day_of_the_week_seperated_data):
        
        # Does not match season_day_of_the_week_averages
        list_mon_interval_average = self.interval_average(list_day_of_the_week_seperated_data, 0)
        list_tues_interval_average = self.interval_average(list_day_of_the_week_seperated_data, 1)
        list_wed_interval_average = self.interval_average(list_day_of_the_week_seperated_data, 2)
        list_thur_interval_average = self.interval_average(list_day_of_the_week_seperated_data, 3)
        list_fri_interval_average = self.interval_average(list_day_of_the_week_seperated_data, 4)
        list_sat_interval_average = self.interval_average(list_day_of_the_week_seperated_data, 5)
        list_sun_interval_average = self.interval_average(list_day_of_the_week_seperated_data, 6)

        list_day_of_week_seperated_interval_average_data = []
        
        list_day_of_week_seperated_interval_average_data.append(list_mon_interval_average)
        list_day_of_week_seperated_interval_average_data.append(list_tues_interval_average)
        list_day_of_week_seperated_interval_average_data.append(list_wed_interval_average)
        list_day_of_week_seperated_interval_average_data.append(list_thur_interval_average)
        list_day_of_week_seperated_interval_average_data.append(list_fri_interval_average)
        list_day_of_week_seperated_interval_average_data.append(list_sat_interval_average)
        list_day_of_week_seperated_interval_average_data.append(list_sun_interval_average)
        return list_day_of_week_seperated_interval_average_data

    def create_cooling_data_by_interval(self, starting_day: int):
        list_cooling_season_energy = []
        # weekday_int_tracker details:
                # 0 - 96 = Sunday
                # 96 - 96*2 = Monday
                # 96*2 - 96*3 = Tuesday
                # 96*3 - 96*4 = Wednesday
                # 96*4 - 96*5 = Thursday
                # 96*5 - 96*6 = Friday
                # 96*6 - 96*7 = Saturday
        if starting_day == 0:
            start_int =0
        elif starting_day == 1:
            start_int = 96
        elif starting_day == 2:
            start_int = 96*2
        elif starting_day == 3:
            start_int = 96*3
        elif starting_day == 4:
            start_int = 96*4
        elif starting_day == 5:
            start_int = 96*5
        elif starting_day == 6:
            start_int = 96*6

        for interval in range(0,len(self.summer_energy_usage[11])-1):    
            weekday_int_tracker = start_int + interval
            weekday_int_tracker = weekday_int_tracker % (96*7)

            if weekday_int_tracker < 96:
                day_of_week = 0
            elif weekday_int_tracker < 96*2:
                day_of_week = 1
            elif weekday_int_tracker < 96*3:
                day_of_week = 2
            elif weekday_int_tracker < 96*4:
                day_of_week = 3
            elif weekday_int_tracker < 96*5:
                day_of_week = 4
            elif weekday_int_tracker < 96*6:
                day_of_week = 5
            else:
                day_of_week = 6
            #print("Interval: ",interval, "Day of the week: ", day_of_week, "Int Tracker: ", weekday_int_tracker)
            day_interval = weekday_int_tracker % 96
            if day_interval == 95:
                day_interval = 94
            list_cooling_season_energy.append(self.summer_energy_usage[11][interval] - self.winter_day_of_week_seperated_interval_average_data[day_of_week][day_interval])

        return list_cooling_season_energy
                

    def create_average_cooling_data_by_interval(self, list_season_energy, starting_day, list_winter_season_day_seperated_energy):
        list_cooling_season_energy = []
        # weekday_int_tracker details:
                # 0 - 96 = Sunday
                # 96 - 96*2 = Monday
                # 96*2 - 96*3 = Tuesday
                # 96*3 - 96*4 = Wednesday
                # 96*4 - 96*5 = Thursday
                # 96*5 - 96*6 = Friday
                # 96*6 - 96*7 = Saturday
        

        for interval in range(0,len(list_season_energy[11])-1):    
            list_cooling_season_energy.append(list_season_energy[11][interval] - list_winter_season_day_seperated_energy[interval])
        return list_cooling_season_energy
    
    def create_cooling_energy(self) ->list:
        """ Creates a 2 dimensional list with each index holding the cooling load in Watts of the Mines campus for the given season each year

        Args:
            season (Season): A summer season object 
            df (DataFrame): The dataframe which contains the energy data of the Mines campus in Watts in 15 minute intervals
            list_winter_day_of_week_seperated_interval_average_data (list): A list containing the average energy use at each time of day (in 15 min intervals) for each day of the week

        Returns:
            list: A list containing the cooling load in 15 minute intervals for the desired time frames. The last 2 items contains the list of 
            averages the weekday and weekend. The 3rd to last row contains the list of overall averages for each time of day.
        """
            
        # Initializes a nested array for each year + avg 
        #MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
        #month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
        list_cooling_energy = []
        list_winter_energy = []
        list_summer_energy = []
        year_num = 2008 # Beginning in 2008
        cols = self.df.columns # Columns store the year
        for i in range(0,len(cols)):
            # Initialize a Year object with the current year
            year = Year(year_num)
            year_num +=1 # Increment the year
            
            # Find the interval range for winter break (Dec 15 to Jan 10)
            break_range_set = self.break_range(number_of_days_to_month(11, year.month_days)+15,10)
            # Get a single year of seasonal energy data
            list_cooling_row, list_winter_row, list_summer_row = self.cooling_energy(self.summer_season.list_interval_range, year.int_end_of_year, break_range_set, self.df, i, self.winter_day_of_week_seperated_interval_average_data)
            # Add the single year of seasonal energy data to a list containing all the years of seasonal energy data
            list_cooling_energy.append(list_cooling_row)
            list_winter_energy.append(list_winter_row)
            list_summer_energy.append(list_summer_row)

        list_cooling_energy = self.season_averages(list_cooling_energy)
        list_cooling_energy = self.season_weekday_averages(list_cooling_energy, self.summer_season.bool_summer)
        list_winter_energy = self.season_averages(list_winter_energy)
        list_winter_energy = self.season_weekday_averages(list_winter_energy, self.summer_season.bool_summer)
        list_summer_energy = self.season_averages(list_summer_energy)
        list_summer_energy = self.season_weekday_averages(list_summer_energy, self.summer_season.bool_summer)
        self.cooling_day_of_the_week_data = list_cooling_energy
        self.winter_day_of_the_week_data = list_winter_energy
        self.summer_day_of_the_week_data = list_summer_energy
        return 
                