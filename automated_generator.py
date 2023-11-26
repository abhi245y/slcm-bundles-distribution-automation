import yaml
import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
from datetime import datetime, timedelta
from main import get_details
import json
from datasheetmaker import fillDetails as generateDatasheet

def date_range(start, end, holidays):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    # print(start_date, end_date)
    delta = end_date - start_date 
    days = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    return list(set(list(map(lambda n: n.strftime("%d") if n.day >= 10 else str(n.day), days)))-set(holidays))

def convetFullDateToMonthAndYear(date):
    format_str = '%Y-%m-%d'
    datetime_obj = datetime.strptime(date, format_str)
    return datetime_obj.strftime("%B ") + str(datetime_obj.year)

def getSundays(year, period_start, period_end):
    format_str = '%Y-%m-%d'
    lastmonth = datetime.strptime(period_start, format_str).month
    currentmonth = datetime.strptime(period_end, format_str).month
    before=datetime(year,lastmonth,20)
    after=datetime(year,currentmonth,21)
    rr = rrule.rrule(rrule.WEEKLY,byweekday=relativedelta.SU,dtstart=before)
    return [r.day for r in rr.between(before,after,inc=True)]
       

def main():
    with open('autometa.yaml', 'r') as file:
        autodata = yaml.safe_load(file)
    
    with open('casula_employee_details.json', 'r') as f:
        employee_data = json.load(f)
    
    sunday = getSundays(datetime.now().year, autodata['period_start'], autodata['period_end'])

    holidays = sunday+autodata['public_holidays']+autodata['public_holidays']+autodata['second_sat']
    holidays.sort(reverse=True)

    present_days = set(autodata['present_days'])-set(holidays)

    datasheet_check = input("Do you want to generate Datasheets (y/n)")

    for employee in employee_data:
        print("Generating Attendance for", employee['name'])
        absent_days = autodata['absentees'].get(employee['name']) or []
        employee_present_days = list(set(present_days)-set(absent_days))
        print("Present Days:", employee_present_days, " Absent Days:", absent_days, "\nTotal Present Days:",len(employee_present_days))
        get_details(employee['name'],employee['period_from'], employee['period_to'], convetFullDateToMonthAndYear(autodata['period_start']), convetFullDateToMonthAndYear(autodata['period_end']),
        employee_present_days,absent_days,holidays,[],autodata['special_holiday_certificate'],autodata['quarantine_certificate'],[],[],[],autodata['period_start'], autodata['period_end'],autodata['nonWorkingDays'])
        if datasheet_check=='y' and employee['name'] != "Unnikrishnan Nair B":
            if employee['post'] == 'Labourer':
                print("Generating Datasheet")
                generateDatasheet(employee)
        print("*********************GENERATED*******************************")

if __name__ == '__main__':
    main()