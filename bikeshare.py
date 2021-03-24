# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 14:00:55 2021
Udacity Data Science with Python--Second Project
@author: Adriana Garcia LA MAGA
"""

import time
import pandas as pd
import numpy as np


#FILTERING OPTIONS --User defined
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington dc': 'washington.csv' }

    city_name={'CH': 'Chicago',
               'NY': 'New York City',
               'DC': 'Washington DC' }

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("------- WELCOME TO THE US BIKESHARE DATA SYSTEM -------")
    hi='Hello {}! Let\'s explore some US bikeshare data!'
    user_name=input('Hello. What is your name? ')
    print(hi.format(user_name))

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_in=input('We currently have information available for the following cities:\
            \n (CH) Chicago \n (NY) New York City \n (DC) Washington DC \n So enter an option: CH - NY - DC \n').upper()

    while city_in not in ['CH','NY','DC']:
        print('Please check spelling the city selection, remember availble options are: CH , NY , DC \n')
        city_in=input().upper()

    city=city_name[city_in]

    # TO DO: get user input for month (all, january, february, ... , june
    month=input('There is available information for: \n January, February, March, April, May and June.\
                \nEnter the name of the month to filter by, or "all" to apply no month filter \n ').title()

    while month not in ['January', 'February','March', 'April', 'May','June','All']:
        print('Please check the month selection, system is not case sensitive, remember availble options are:\
            \n January, February, March, April, May and June, all \n')
        month=input().title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Weekday information is avaible for: .\
            \n Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. \
            \nEnter the weekday name to filter by, or "all" to apply no weekday filter \n').title()

    while day not in ['Monday', 'Tuesday','Wednesday', 'Thrusday', 'Friday','Saturday','Sunday','All']:
            day=input('Please check your weekday selection. Remember Weekday information is avaible for: \
            \n Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. \
            \nEnter the weekday name to filter by, or "all" to apply no weekday filter\n ').title()

    #Get the final names for the case when all options are selected in month or day
    if month=='All':
        month='No'

    if day=='All':
        day='No'

    print("\n\nYou have selected information for: \n " + city + 
        "\n Filtered by month: " + month+ 
        "\n Filtered by weekday: " + day)
    
    return city,month,day

#LOADING THE DATA
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "No" to apply no month filter
        (str) day - name of the day of week to filter by, No "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city=city.lower()
    CITY_DATA = { 'chicago': 'chicago.csv',
                  'new york city': 'new_york_city.csv',
                  'washington dc': 'washington.csv' }
    
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'No':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    if day != 'No':
        # Filter by the selected day user selected
        df = df[df['day_of_week'] == day.title()]
        
    return df


def display_raw_data(df,city,month,day):
    """ Displaying raw data from the selected city-month-day combination selected by user """
    i = 0
    max_rows=len(df)+1 #thiis is used to control the printing on raw data, in case user keep saying yes!
    
    #Ask user selection on printing raw data, non case sentive input chck by lower. :)
    raw = input("\n Do you want me to see display raw data for your selection? Enter: yes or no \n").lower()
    #Set nice view on pd dataframe
    pd.set_option('display.max_columns',200)
    
    df['month']=df['Start Time'].dt.month_name()
    while True:            
        if raw == 'no':
            print('\nOK. Let\'s then dive into some bikeshare statiscs for '+  city.upper() 
                  + '---Month Filtered: '+ month.upper() +  "--Weekday Filtered: " + day.upper())
            break
            
        elif raw == 'yes':
            if i==0:
                print('------BIKESHARE US DATA FOR ' + city + '--Filtered by month: '+ month.upper() + ' - Filtered by day: ' +  day.upper() +' -----')
            
            slicer_1=min(i,max_rows)
            slicer_2=min(i+5,max_rows)
            
            #Here is a check in case user just keep asking for more and more data!
            if df[slicer_1:slicer_2].empty == False:
                print(df[slicer_1:slicer_2]) # TO DO: appropriately subset/slice your dataframe to display next five rows
                raw = input("Want to get 5 more trips raw data info? Enter: yes or no.\n").lower() # TO DO: convert the user input to lower case using lower() function
                i += 5
            else:
                raw = 'no'
                print('no more raw data available-----------------------------')
            
        else:
            raw = input("\nPlease check your spelling. Remember avaible choices are: 'yes' or 'no'\n").lower()



#DESCRIPTIVE STATISTICS
## 1. Popular traveling times
def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('\n-- POPULAR TRAVELING TIMES STAISTICS (for selected city,month,day) --\n')
    # TO DO: display the most common month
    if month=='No':
        df['month_name'] = df['Start Time'].dt.month_name()
        popular_month=df['month_name'].mode()[0]
        print('Most popular month is: ' + popular_month.title())
    else:
        print('Your selected month was: '+ month)

    # TO DO: display the most common day of week
    if day=='No':
        df['day_of_week'] = df['Start Time'].dt.day_name()
        popular_day=df['day_of_week'].mode()[0]
        print('Most popoular day is: ' + popular_day.title())
    else:
        print('Your selected day was: '+ day)
    
    # TO DO: display the most common start hour
    df['hour'] =df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour,'h')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



## 2.Popular Station and trip
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    #Print ComputingStats
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    print('\n --POPULAR STATIONS STATISTICS  (for selected city,month,day) --')
    # TO DO: display most commonly used start station
    try:
        start_station_mode=df['Start Station'].mode()[0]
        print('Most popular Start Station is: \n',start_station_mode)
    except Exception as NotCalculation:
        print('Not able to compute statistics on most common Start Station')

    # TO DO: display most commonly used end station
    try:
        end_station_mode=df['End Station'].mode()[0]
        print('Most popular End Station is:\n ',end_station_mode)
    except Exception as NotCalculation:
        print('Not able to compute statistics on most common End Station')

    # TO DO: display most frequent combination of start station and end station trip
    try:
        #Computing the most popular start-end trip
        df['Start_End']='from '+df['Start Station']+' to '+df['End Station']
        start_end_mode=df['Start_End'].mode()[0]
        message='Most frequent combination Start to End Station trip is: \n {}'
        print(message.format(start_end_mode))
    except Exception as NotCalculation:
        print('Not able to compute statistics on Start-End Station')
    
    #Computing time message
    print("\nThis computations took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
## 3.Trip Duration
def trip_duration_stats(df):
    """Displays statistics on the trip duration."""
    
    print('Computing Traveling Time Statistics ....\n\n')
    start_time= time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Trip Duration']=df['End Time']-df['Start Time']
    df.head()

     # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_travel_time=df['Trip Duration'].mean(skipna=True)

    #Other Statistics on Traveling Time
    total_trips=df['Trip Duration'].count()
    min_travel_time=df['Trip Duration'].min()
    max_travel_time=df['Trip Duration'].max()
    median_travel_time=df['Trip Duration'].median()


    message = "--TRAVELING TIME STATISTICS  (for selected city,month,day )-- \
    \nThe total traveling time of bikeshare users was {}.\
    \nMean traveling time was {}. \
    \n\nOther cool Insights: \n The longest trip took: {} \n The shortest trip took: {} \
    \n Half of trips took no longer than: {} \
    \n\nThis statistics where computed for a total of: {} trips \nComputing them took about {} seconds.\n"

    s=time.time() - start_time
    print(message.format(total_travel_time, mean_travel_time, max_travel_time, min_travel_time, median_travel_time,total_trips,s))
    print("\nThis computations took %s seconds." % (time.time() - start_time))
    print('-'*50)  



## 4.User info
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(' --USER TYPE STATISTICS  (for selected city,month,day)) --')
    print(df['User Type'].value_counts(dropna=False))
    
    # TO DO: Display counts of gender --(Information not available for washington)
    print('\n --USER GENDER STATISTICS  (for selected city,month,day) --')
    try:    
        print(df['Gender'].value_counts(dropna=False))
    
    except Exception as NotAvailableVariable:
       print("This city has no available data on users gender")
    
    # TO DO: Display earliest, most recent, and most common year of birth  --(Information not available for washington)
    print('\n--USER AGE STATISTICS  (for selected city,month,day) --')
    try:    
        earliest_year=df['Birth Year'].min()
        recent_year=df['Birth Year'].max()
        mode_year=df['Birth Year'].mode()[0]

        message_birth='\n Oldest customer born was born in: {} (aprox. age {} years)\
        \n Youngest customer was born in: {}  (aprox. age {} years ) \
        \n Most of our customers were born in: {} (aprox. age {} years)'

        print(message_birth.format(int(earliest_year),2020-int(earliest_year), 
                                   int(recent_year),2020-int(recent_year), 
                                   int(mode_year),2020-int(mode_year)))
    except Exception as NotAvailableVariable:
       print("This city has no available data on users birth year")

    print("\nComputing this statistics took %s seconds." % (time.time() - start_time))
    print('-'*50)


    
    
#MAIN FUNCTION
def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            
           #diplaying raw data
            display_raw_data(df,city,month,day)
           #displaying statistics 
            time_stats(df,month,day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except Exception as ExecutingError:
            print('There was a program error')
            
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in ['yes','no']:
            restart=input('Please check yout spelling, Would you like to restart? Enter yes or no \n').lower()
            
        if restart.lower() != 'yes':
            print('\n Thanks for accesing the bikeshre US data system. Have a nice day!')
            break

if __name__ == "__main__":
	main()

