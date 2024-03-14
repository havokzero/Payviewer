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

# Function to calculate earnings per payday
def calculate_earnings(pay_frequency, pay_rate, salary_mode):
    if salary_mode == 'hourly':
        weekly_pay = pay_rate * HOURS_PER_WEEK
    elif salary_mode == 'salary':
        weekly_pay = pay_rate / WEEKS_PER_YEAR
    else:
        raise ValueError("Invalid salary mode. Choose 'hourly' or 'salary'.")

    if pay_frequency == 'weekly':
        return weekly_pay
    elif pay_frequency == 'bi-weekly':
        return weekly_pay * 2
    elif pay_frequency == 'monthly':
        return weekly_pay * WEEKS_PER_YEAR / MONTHS_PER_YEAR
    else:
        raise ValueError("Invalid pay frequency. Choose 'weekly', 'bi-weekly', or 'monthly'.")

# Function to organize and print future paydays with earnings and calculate year-end total
def organize_and_print_future_paydays_with_year_end_total(paid_dates, pay_frequency, pay_rate, salary_mode):
    current_year = datetime.now().year
    is_leap = is_leap_year(current_year)
    paydays_by_month = {datetime(current_year, month, 1).strftime("%b"): [] for month in range(1, 13)}
    earnings_per_payday = calculate_earnings(pay_frequency, pay_rate, salary_mode)
    total_earnings = 0

    # Calculate future paydays
    for date_str in paid_dates:
        payday = datetime.strptime(date_str, "%Y-%m-%d")
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

# Example usage with hypothetical conditions
#user_dates = ['2024-01-14', '2024-01-28', '2024-02-11', '2024-02-25', '2024-03-11', '2024-03-25']  # Initial paid dates
#pay_frequency = 'bi-weekly'  # Assumed pay frequency
#pay_rate = 31  # Assumed hourly rate
#salary_mode = 'hourly'  # Payment mode
#organize_and_print_future_paydays_with_year_end_total(user_dates, pay_frequency, pay_rate, salary_mode)
