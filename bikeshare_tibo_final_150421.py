import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs. I used following simple example to help me:
    # https://www.includehelp.com/python/asking-the-user-for-input-until-a-valid-response-in-python.aspx
    while True:
     try:
      city = input('Enter the city of your choice(chicago, new york city, washington):')
      if city == 'washington' or city == 'chicago' or city == 'new york city':
        print('city entered successfully...')
        break;
      else:
        print('City should be only one of these: chicago, new york city, washington: ')
        continue
     except:
      continue
    #get user input for filter by month or day
    while True:
     try:
      user_filter = input('would you like to filter by month or day? if yes, type month or day. If no, type anything!')
      if user_filter == 'month':
        print('data will be filtered by month')
    # get user input for month (all, january, february, ... , june)
        month = input('Enter a specific month from january untill june:')
        if month in ['january', 'february', 'march', 'april', 'may', 'june']:
          day = 'all'
          break;
        # handle case if user writes non conform input:
        else:
          month = 'all'
          day = 'all'
          print ('no filter was set because your answer was not clear!')
          break;
      elif user_filter == 'day':
    # get user input for day of week (all, monday, tuesday, ... sunday)
        print ('data will be filtered by day')
        day = input('Enter a day in the week:')
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
          month = 'all'
          break;
        # handle case if user writes non conform input:
        else:
          month = 'all'
          day = 'all'
          print ('no filter was set because your answer was not clear!')
          break;
        month = 'all'
        break;
      #if the user does not choose to filter by month or day, then no matter what asnwer is,
      #there will be no filter:
      else:
        print ('no filter because your answer was not clear!')
        day = 'all'
        month = 'all'
        break;
     except:
      continue

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Import the csv file of the city chosen by the user
    df = pd.read_csv(CITY_DATA[city])
    # Convert  the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day given by the user
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['dummy','january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]
    print('The most common month is: ', months[popular_month])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ', popular_end_station)
    #display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('most frequent combination of start station and end station trip: ', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time, 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].describe()[1]
    print('Mean travel time: ', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Name and number of different user types: ', user_types)
    # Display counts of gender and create an exception for cities with
    #no gender info like washington!'
    while True:
     try:
      gender_types = df['Gender'].value_counts()
      break;
     except:
      gender_types = 'There is no info for gender types for this city'
      break;

    print('Gender informations: ', gender_types)
    # Display earliest, most recent, and most common year of birth
    while True:
     try:
      earliest_birth_year = df['Birth Year'].describe()[3].astype(int)
      most_recent_birth_year = df['Birth Year'].describe()[7].astype(int)
      most_common_birth_year = df['Birth Year'].describe()[1].astype(int)
      break;
     #display an exception for washington that has no birth year info
     except:
      earliest_birth_year = 'There is no info for birth years for this city'
      most_recent_birth_year = 'There is no info for birth years for this city'
      most_common_birth_year = 'There is no info for birth years for this city'
      break;

    print('The earliest birth year is: ', earliest_birth_year)
    print('The most recent birth year is: ', most_recent_birth_year)
    print('The most common birth year is: ', most_common_birth_year)

    #Get first five lines on user request:
    #while True
    #try print(df.head())
    #view_raw_data = input('Do you wanna see 5 more lines: yes or no?')
    # If answer is yes:
    # PROBLEM: I wanted to delete the rows of my df and show head again... 
    #Except: break


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
