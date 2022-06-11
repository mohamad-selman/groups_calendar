from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # Days as columns: <td>DAY</td>
    def formatday(self, day, events):

        # filter events by day
        day_events = events.filter(start_time__day = day)

        events_list = ''
        for event in day_events:
            events_list += f'''
                <li>
                    {event.get_url}
                </li>
            '''

        if day != 0:
            return f'''
                <td>
                    <span class='date'>{day}</span>
                    <ul>{events_list}</ul>
                </td>
            '''
        return '<td></td>'

    # Weeks as rows: <tr>COLUMNS</tr>
    def formatweek(self, week, events):
        week_row = ''
        for day, weekday in week:
            week_row += self.formatday(day, events)

        return f'''
            <tr>
                {week_row}
            </tr>
        '''

    # Month as table: <table>ROWS</table>
    def formatmonth(self, withyear=True):

        # filter events by year and month
        events = Event.objects.filter(
            start_time__year = self.year,
            start_time__month = self.month
        )

        month_table = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        month_table += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        month_table += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            month_table += f'{self.formatweek(week, events)}\n'

        month_table += '</table>'
        return month_table
