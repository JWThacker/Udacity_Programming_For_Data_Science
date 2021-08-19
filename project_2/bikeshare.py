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
    months = ['january','february','march','april','may','june','all']
    cities = CITY_DATA.keys()
    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
    print('Hello! Let\'s explore some US bikeshare data!')
    #Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Which city's data would you like to view/analyze (Chicago, New York City, or Washington)?").lower()
            if city not in cities:
                print("That's not a valid city name: Chicago, New York City, Washington.")
            else:
                break
        except KeyboardInterrupt:
            print('Program terminated.')
            exit()
    #Get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Would you like to view the data from a certain month(January, February,..., June, all)?").lower()
            if month not in months:
                print("Please enter a valid month: only January through June or enter 'all' for no filter.")
            else:
                break
        except KeyboardInterrupt:
            print("Program terminated")
            exit()
            
    #Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Would you like to view data from a certain day(monday, tuesday,...,sunday, all)?").lower()
            if day not in days:
                print("Please enter the name of a valid day: Sunday through Monday or enter 'all' for no filter.")
            else:
                break
        except KeyboardInterrupt:
            print('Program terminated.')
            exit()
            
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
    
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    
    
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
        
    if day != 'all':
        df = df[df['Day'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['January','February','March','April','May','June']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    monthMode = df['Month'].mode()[0]
    print('Most common month: ',months[monthMode - 1])
    #Display the most common day of week
    print('Most common day of the week: ',df['Day'].mode()[0])

    #Display the most common start hour
    print('Most common start hour: ',df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    print('Most commonly used start station:',df['Start Station'].mode()[0])

    #Display most commonly used end station
    print('Most commonly used end station:',df['End Station'].mode()[0])


    #Display most frequent combination of start station and end station trip
    df['Start/End Combination'] = df['Start Station'] + ' and ' + df['End Station']
    print('Most commonly used trip (starting and end stations together):',df['Start/End Combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    print('Total travel time across all travelers:',df['Trip Duration'].sum())
    
    #Display mean travel time
    print('Average travel time:',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    labels = df['User Type'].value_counts().keys().tolist()
    n_labels = range(len(labels))
    value_counts = df['User Type'].value_counts()
    for i in n_labels:
        print('The number of ',labels[i]+'s',' is ',value_counts[labels[i]])
    
    print('\n')
    if city == 'washington':
        print("Washington has neither a 'gender' nor 'birth year' attribute. ")
    else:
    #Display counts of gender
        gender_labels = df['Gender'].value_counts().keys().tolist()
        n_gender_labels = range(len(gender_labels))
        gender_value_counts = df['Gender'].value_counts()
        for i in n_gender_labels:
            print('The number of ',gender_labels[i] + 's is ',gender_value_counts[gender_labels[i]])

        print('\n')
        
    #Display earliest, most recent, and most common year of birth
        print('The earliest birth year is:',df['Birth Year'].min())
        print('The most recent birth year is:',df['Birth Year'].max())
        print('The most common birth year is:',df['Birth Year'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        user_input = True
        while user_input:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            try:
                answer = input("Would you like to see a 5 line preview of the data?").lower()
                if answer == 'yes':
                    print(df.head())
                else:
                    break
            except KeyboardInterrupt:
                print('Program terminated')
                exit()
              
            try:
                answer = input("Would you like to apply a different filter an see more lines of the data (type: Yes or No)?").lower()
                if answer == 'yes':
                    user_input = True
                else:
                    user_input = False
            except KeyboardInterrupt:
                Print('Program terminated')
                exit()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
