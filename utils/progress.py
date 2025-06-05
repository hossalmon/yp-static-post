from datetime import date

def get_year_progress(given_date=None):
    today = given_date or date.today()
    start = date(today.year, 1, 1)
    end = date(today.year + 1, 1, 1)
    days_passed = (today - start).days + 1  # include today
    days_in_year = (end - start).days
    progress = days_passed / days_in_year
    return today, progress, days_passed, days_in_year
