import calendar
from datetime import datetime, timedelta

# Constants for calculation
WEEKS_PER_YEAR = 52
MONTHS_PER_YEAR = 12
HOURS_PER_WEEK = 40


# Function to determine if it's a leap year
def is_leap_year(year):
    return calendar.isleap(year)


# Function to calculate pay intervals based on frequency
def get_pay_frequency_delta(pay_frequency, latest_pay_date, is_leap):
    if pay_frequency == 'weekly':
        return timedelta(weeks=1)
    elif pay_frequency == 'bi-weekly':
        return timedelta(weeks=2)
    elif pay_frequency == 'monthly':
        return timedelta(days=29) if is_leap and latest_pay_date.month == 2 else timedelta(days=30)
    else:
        raise ValueError("Invalid pay frequency. Choose 'weekly', 'bi-weekly', or 'monthly'.")


## Function to calculate earnings per payday
def calculate_earnings(pay_frequency, pay_rate, salary_mode):
    if salary_mode == 'hourly':
        weekly_pay = pay_rate * HOURS_PER_WEEK
        if pay_frequency == 'weekly':
            return weekly_pay
        elif pay_frequency == 'bi-weekly':
            return weekly_pay * 2  # For bi-weekly, pay for two weeks
        elif pay_frequency == 'monthly':
            return weekly_pay * (WEEKS_PER_YEAR / MONTHS_PER_YEAR)  # Average weeks per month
        else:
            raise ValueError("Invalid pay frequency. Choose 'weekly', 'bi-weekly', or 'monthly'.")
    elif salary_mode == 'salary':
        # If salary mode, pay_rate is annual salary
        if pay_frequency == 'weekly':
            pay_periods = WEEKS_PER_YEAR
        elif pay_frequency == 'bi-weekly':
            pay_periods = WEEKS_PER_YEAR / 2
        elif pay_frequency == 'monthly':
            pay_periods = MONTHS_PER_YEAR
        else:
            raise ValueError("Invalid pay frequency. Choose 'weekly', 'bi-weekly', or 'monthly'.")
        return pay_rate / pay_periods  # This calculation remains correct for salary mode
    else:
        raise ValueError("Invalid salary mode. Choose 'hourly' or 'salary'.")


# Function to organize and print future paydays with earnings and calculate year-end total
def organize_and_print_future_paydays_with_year_end_total(paid_dates, pay_frequency, pay_rate, salary_mode):
    current_year = datetime.now().year
    is_leap = is_leap_year(current_year)
    paydays_by_month = {datetime(current_year, month, 1).strftime("%b"): [] for month in range(1, 13)}
    earnings_per_payday = calculate_earnings(pay_frequency, pay_rate, salary_mode)
    total_earnings = 0

    # Calculate future paydays
    for date_str in paid_dates:
        # Strip any leading or trailing whitespace from the date string
        clean_date_str = date_str.strip()
        # Now parse the cleaned date string
        payday = datetime.strptime(clean_date_str, "%m/%d/%Y")
        delta = get_pay_frequency_delta(pay_frequency, payday, is_leap)
        while payday.year == current_year:
            paydays_by_month[payday.strftime("%b")].append((payday.strftime("%d"), earnings_per_payday))
            payday += delta

    # Print out the results in SQL-like format and calculate total earnings
    print("| {:<5} | {:<15} | {:<15} |".format("Month", "Paydays", "Earnings ($)"))
    print("-" * 50)
    for month, days in paydays_by_month.items():
        if days:
            earnings_str = ', '.join(["{} (${:.2f})".format(day, earnings) for day, earnings in days])
            print("| {:<5} | {:<15} | {:<15} |".format(month, earnings_str, ''))
            total_earnings += sum(earnings for _, earnings in days)
    print("-" * 50)
    print(f"Year-End Total Earnings: ${total_earnings:.2f}")


# Main program to handle user input and integrate with the payroll logic
def main():
    # User input section
    print("Enter your salary mode ('hourly' or 'salary'): ")
    salary_mode = input().strip().lower()
    print("Enter your hourly rate or annual salary: ")
    pay_rate = float(input().strip())

    # Pay frequency selection
    print("Select your pay frequency by entering the corresponding number:")
    print("1. Weekly\n2. Bi-weekly\n3. Monthly")
    frequency_options = {'1': 'weekly', '2': 'bi-weekly', '3': 'monthly'}
    frequency_choice = input("Your choice (1, 2, or 3): ").strip()
    pay_frequency = frequency_options.get(frequency_choice, 'bi-weekly')  # Default to bi-weekly

    # Last pay dates input
    print("Enter your last 3-4 pay dates in the format MM/DD/YYYY, separated by commas:")
    last_pay_dates_str = input().strip()
    last_pay_dates = last_pay_dates_str.split(',')

    # Process and output future paydays and total earnings
    organize_and_print_future_paydays_with_year_end_total(last_pay_dates, pay_frequency, pay_rate, salary_mode)


if __name__ == "__main__":
    main()
