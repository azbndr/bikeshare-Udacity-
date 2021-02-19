import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

month_lst = ["January", "February", "March", "April", "May", "June", "All"]
day_lst = ["Saturday", "Sunday", "Monday", "Tuesday",
           "Wednesday", "Thursday", "Friday", "All"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            "Please select a city to explore (chicago, new york city, washington)\n").lower()
        if city not in CITY_DATA:
            print("The name of the city you entered doesn't match!!\n")
            continue
        break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Please select a month filter (January, February, March, April, May, June, all)\n").title()
        if month not in month_lst:
            print("The name of the month you entered doesn't match!!\n")
            continue
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Please select a day filter (Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, all)\n").title()
        if day not in day_lst:
            print("The name of the day you entered doesn't match!!\n")
            continue
        break

    print('-'*40)
    return city, month, day


print("\n")


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
    print("Loading Data!!\n")
    df = pd.read_csv(CITY_DATA.get(city), parse_dates=[
                     'Start Time', 'End Time'])
    # Extracting date parts and creating new columns
    df["Start Month"], df["Start Day"], df["Start Hour"] = (df["Start Time"].dt.month_name(),
                                                            df["Start Time"].dt.day_name(), df["Start Time"].dt.hour)

    # Filter by month
    if month != "All":
        df = df[df["Start Month"] == month]
    # Filter by day
    if day != "All":
        df = df[df["Start Day"] == day]
    return df


print("\n")


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "All":
        common_month = df["Start Month"].dropna()
        if common_month.empty:
            print("No common month found!\n")
        else:
            common_month = common_month.mode()[0]
            print("The most common month is: {}\n".format(common_month))
    else:
        print("No common month. You selected a specific month filter!!\n")

    # display the most common day of week
    if day == "All":
        common_day = df["Start Day"].dropna()
        if common_day.empty:
            print("No common day found!\n")
        else:
            common_day = common_day.mode()[0]
            print("The most common day is: {}\n".format(common_day))
    else:
        print("No common day. You selected a specific day filter!!\n")

    # display the most common start hour
    common_hour = df["Start Hour"].dropna()
    if common_hour.empty:
        print("No common hour found")
    else:
        common_hour = common_hour.mode()[0]
        print("The most common hour is: {}\n".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


print("\n")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_station = df["Start Station"]
    if common_station.empty:
        print("No common start station found!\n")
    else:
        common_station = common_station.mode()[0]
        print("The most common start station is: {}\n".format(common_station))

    # display most commonly used end station
    common_end = df["End Station"]
    if common_end.empty:
        print("No common end station found!\n")
    else:
        common_end = common_end.mode()[0]
        print("The most common end station is: {}\n".format(common_end))

    # display most frequent combination of start station and end station trip
    common_start_end = df[["Start Station", "End Station"]].dropna()
    if common_start_end.empty:
        print("No common station found!\n")
    else:
        common_start_end = (common_start_end.groupby(
            ["Start Station", "End Station"]).size().sort_values(ascending=False))

        trip_count = common_start_end.iloc[0]

        stations = common_start_end[common_start_end == trip_count].index[0]
        start_station, end_station = stations

        print("The most common start station is: {} and the most end station is: {} which had {} trips.\n".format(
            start_station, end_station, trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


print("\n")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    valid_time = df["Trip Duration"].dropna()
    if valid_time.empty:
        print("No data found! please choose another filter!!\n")
    else:
        total_time = valid_time.sum()
        print("Total travel time {} seconds or {} hours\n".format(
            total_time, total_time//60))

        # display mean travel time
        avg_time = valid_time.mean()
        print("Average travel time {} seconds or {} hours\n".format(
            avg_time, avg_time//60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


print("\n")


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df["User Type"].dropna()

    if user_type.empty:
        print("No data found! please select another filter!!\n")
    else:
        user_type = user_type.value_counts()
        print("User type info:\n{}\n".format(user_type))
    # Display counts of gender
    if "Gender" in df:
        user_gender = df["Gender"].dropna()
        if user_gender.empty:
            print("No data found! please select another filter!!\n")
        else:
            user_gender_count = user_gender.value_counts()
            print("User gender info:\n{}\n".format(user_gender_count))
    else:
        print("No gender information in this city!!\n")
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        byear = df["Birth Year"].dropna()
        if byear.empty:
            print("No data found! please select another filter!!\n")
        else:
            earliest_byear = df["Birth Year"].max()
            recent_byear = df["Birth Year"].min()
            common_byear = df["Birth Year"].mode()[0]
            print("The earliest birth year is: {}\nThe most recent birth year is: {}\nThe common birth year is: {}\n".format(
                int(earliest_byear), int(recent_byear), int(common_byear)))
    else:
        print("No birth year information in this city!!\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


print("\n")


def main():
    while True:
        city, month, day = get_filters()
        print("Filters => City: {}, Month: {}, Day: {}\n".format(city, month, day))
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
