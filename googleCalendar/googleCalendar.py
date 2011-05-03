try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree


from pylabs import q
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import gdata.calendar.client
import atom
import time
import datetime
import re


class retry(object):
    def __init__(self, retries):
        self.retries = retries

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            
            for i in range(1, self.retries+1):
                try:
                    f(*args, **kwargs)
                except gdata.service.RequestError as ex:
                    q.logger.log('trying to %s - trial %s of %s'%(f.__name__, i, self.retries), 2)
                    q.logger.log(ex)
                else:
                    q.logger.log('%s carried out successfully in %s tries'%(f.__name__, i), 5)
                    return
            q.logger.log('failed to %s after %s tries'%(f.__name__, self.retries), 2)
        wrapped_f.__name__ = f.__name__
        wrapped_f.__doc__ = f.__doc__
        return wrapped_f



class GoogleCalendar(object):
    def getConnection(self, email, password=None, saveCredentials=False):
        """
        Creates a connection to the given user's Google Calendar.
        
        @param email: the user's email
        @param password: the user's password, if not given then it is retrieved from the stored users' info, if available
        @param saveCredentials: boolean to determine whether or not to save the user's credentials locally to be used later
        """
        return GoogleCalConnection(email, password, saveCredentials)



class GoogleCalConnection(object):
    def __init__(self, username, password=None, saveCredentials=False):
        self._client = gdata.calendar.service.CalendarService()
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'clients', 'googleCalendar', 'googleCalendar.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        
        
        if password:
            self._client.password = password
            if saveCredentials:
                cfgfile.addSection(username)
                params = {'email':username, 'password':password}
                for k, v in params.items():
                    cfgfile.addParam(username, k, v)
        else:
            if cfgfile.checkSection(username):
                credentials = cfgfile.getSectionAsDict(username)
                self._client.password = credentials['password']
            else:
                raise RuntimeError('Credentials not stored, please enter full credentials')
            
            
        self._client.email = username
        self._client.source = "pylabs"
        self._client.ProgrammaticLogin()
        
        self._initialized = False
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            attrs.append('calendars')
        return attrs
    
    def _reload(self):
        q.logger.log('reloading connection', 5)
        email = self._client.email
        password = self._client.password
        self.__init__(email, password)


    def __getattribute__(self, name):
        if name == 'calendars' and not object.__getattribute__(self, '_initialized'):
            self.calendars = Calendars(self, object.__getattribute__(self, '_client'))
            self._initialized = True
            return object.__getattribute__(self, 'calendars')
        elif name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)
    
    @retry(10)
    def _getOwnCalFeed(self):
        self._ownCalFeed = self._client.GetOwnCalendarsFeed()
        q.logger.log('Calendars initialized', 2)
        self.calendars = Calendars(object.__getattribute__(self, '_client'), object.__getattribute__(self, '_ownCalFeed').entry)
        self._initialized = True
    
    @retry(10)        
    def new(self, title='New Calendar', summary='New Calendar', place='A-Server', color='#2952A3', timezone='Africa/Cairo', hidden='false'):
        """
        Creates a new calendar using the given parameters in the user's calendars.
        
        @param title: string for the title of the new calendar to be created, default is "New Calendar"
        @param summary: string for the summary of the new calendar to be created, default is "New Calendar"
        @param place: string for the default location of the new calendar
        @param color: string for the color in hex for the online interface of the calendar, default is google's "blue" default for new calendars
        @param timezone: string for the time zone of the calendar
        @param hidden: boolean to decide whether the calendar is to be hidden or visible in the online interface
        
        """
        calendar = gdata.calendar.CalendarListEntry()
        calendar.title = atom.Title(text=title)
        calendar.summary = atom.Summary(text=summary)
        calendar.where = gdata.calendar.Where(value_string=place)
        calendar.color = gdata.calendar.Color(value=color)
        calendar.timezone = gdata.calendar.Timezone(value=timezone)
        calendar.hidden = gdata.calendar.Hidden(value=hidden)
        
        new_calendar = self._client.InsertCalendar(new_calendar=calendar)
        
        title = cleanString(title)
        self.calendars._addCalendar(self, self._client, new_calendar)
        q.logger.log('Calendar %s added'%title, 2)
        
        return new_calendar

        
            
class Calendars(object):
    def __init__(self, connection, calClient):
        self._connection = connection
        self._calClient = calClient
        self._initialized = False
        self._cals = {}
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            self._retrieveCals()
            attrs.extend(self._cals.keys())
        return attrs
    
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_retrieveCals')()
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)
            
            
    @retry(10)
    def _retrieveCals(self):
        self._calFeed = self._calClient.GetOwnCalendarsFeed()
        q.logger.log('Calendars Added')
        map(lambda calObj: self._addCalendar(self._connection, self._calClient, calObj), self._calFeed.entry)
        self._initialized = True
    

    def _addCalendar(self, conn, client, calObject):
        title = cleanString(calObject.title.text)
        self._cals['%s'%title] = calObject
        setattr(self, title, Calendar(conn, client, calObject))
        
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_retrieveCals').__call__()
        key = cleanString(key)
        return self.__dict__[key]
    
    def __iter__(self):
        if not self._initialized:
            self._retrieveCals()
        return GoogleCalIterator(self.__dict__)

            
class Calendar(object):
    
    def __init__(self, calConnection, calClient, calendarObject):
        self._conn = calConnection
        self._client = calClient
        self._calObj = calendarObject
        self._initialized = False
        self.events = Events(self._conn, self._client, self._calObj)
    
    @retry(10)        
    def delete(self):
        """
        Deletes the selected calendar from the user's calendars.
        """
        path = self._calObj.GetAlternateLink().href
        path.replace('http:','https:')
        self._client.Delete(path)
        self._conn.calendars.__dict__.pop(self._calObj.title.text)
        self._conn.calendars._initialized = False
        
        
    def __getitem__(self, key):
        return self.events.__getitem__(key)
    
    def __iter__(self):
        return self.events.__iter__()
    
    def _createGuest(self, name, email=None):
        guest = gdata.calendar.Who()
        guest.valueString = name
        guest.email = email or name
        guest.name = name
        return guest
    
    @retry(10)
    def new(self, title='New Event', summary='New Event', place='A-Server', start_year=None, start_month=None, start_day=None,
            start_hour=None, start_min=0, end_year=None, end_month=None, end_day=None, end_hour=None, end_min=0, guests={}, 
            send_notifications=True, all_day=False):
        """
        Creates a new event in the selected calendar
        
        @param title: the string title of the new event, default is "New Event"
        @param summary: the string summary of the new event, default is "New Event"
        @param place: the string place of the new event
        @param start_year: the start year of the event, if not given the current year is used
        @param start_month: the start month of the event, if not given the current month is used
        @param start_day: the start day of the event, if not given the current day is used
        @param start_hour: the start hour of the event, if not given the current hour is used
        @param start_min: the start minute of the event, if hour not given the current minute is used, if hour is given resets to 0
        @param end_year: the end year of the event, if not given the start year is used
        @param end_month: the end month of the event, if not given the start month is used
        @param end_day: the end day of the event, if not given the start day is used
        @param end_hour: the end hour of the event, if not given default is one hour after the start hour
        @param end_min: the end minute of the event, if not given and end_hour not given the start minute is used, if hour given resets to 0
        @param guests: dictionary of guest names and emails
        @param send_notifications: boolean to determine whether to send notifications to guests, default is true
        @param all_day: boolean to determine if the event is an all-day event, default is false
        """
        
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text = summary)
        event.where.append(gdata.calendar.Where(value_string=place))

        event.who.extend(map(lambda (n, e): self._createGuest(n, e), guests.iteritems()))
        event.send_event_notifications = gdata.calendar.SendEventNotifications(value='true')
        
        
        time_now = time.localtime()
        
        start_year = start_year or time_now.tm_year
        start_month = start_month or time_now.tm_mon
        start_day = start_day or time_now.tm_mday

        if not all_day and start_hour is None:
            start_hour = time_now.tm_hour
            if start_min == 0:
                start_min = time_now.tm_min
        
        if all_day:
            start_date = datetime.date(start_year, start_month, start_day)
            start_time = start_date.strftime('%Y-%m-%d')
        else:
            start_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((start_year, start_month, start_day, start_hour, start_min, 0, 0, 0, 0)))
        
        end_year = end_year or start_year
        end_month = end_month or start_month
        end_day = end_day or start_day

        if not all_day and end_hour is None:
            end_hour = start_hour + 1
            if end_min == 0:
                end_min = start_min
                
        if all_day:
            end_date = datetime.date(end_year, end_month, end_day)
            end_time = end_date.strftime('%Y-%m-%d')
        else:
            end_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((end_year, end_month, end_day, end_hour, end_min, 0, 0, 0, 0)))
        
        
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
        
        path = self._calObj.GetAlternateLink().href
        path.replace('http:','https:')

        
        new_event = self._client.InsertEvent(event, path)
        self.events._addEvent(self._conn, self._client, self, new_event)
        q.logger.log('event "%s" created successfully'%title, 2)
        return new_event    
            
class Events(object):
    def __init__(self, calConnection, calClient, calObject):
        self._conn = calConnection
        self._client = calClient
        self._calObj = calObject
        self._initialized = False
        self._events = {}
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            self._initEvents()
            attrs.extend(self._events.keys())
        return attrs
    
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_initEvents')()
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)
    
    @retry(10)    
    def _getEventFeed(self):
        path = self._calObj.GetAlternateLink().href
        path.replace('http:','https:')
        
        self._eventFeed = self._client.GetCalendarEventFeed(path)
        q.logger.log('Event feed initialized')
        self._initialized = True
     
    def _initEvents(self):
        if not self._initialized:
            self._events = {}
            self._getEventFeed()
        map(lambda eventObj: self._addEvent(self._conn, self._client, self, eventObj), self._eventFeed.entry)

    
    def _addEvent(self, conn, client, calendar, event):
        title = cleanString(event.title.text)
        self._events['%s'%title] = event
        setattr(self, title, Event(conn, client, calendar, event))
    
    
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_initEvents')()
        key = cleanString(key)
        return self.__dict__[key]
    
    def __iter__(self):
        if not self._initialized:
            self._initEvents()
        return GoogleCalIterator(self.__dict__)



class Event(object):
    def __init__(self, calConnection, calClient, parentEvents, eventObject):
        self._client = calClient
        self._parentEvents = parentEvents
        self._conn = calConnection
        self._eventObj = eventObject
        self.title = self._eventObj.title.text
        self._guests = self._eventObj.who
        self.guestEmails = None
        self.guestNames = None
        self.guests = Guests(self._eventObj)
        
        self.attending = filter(lambda guest: self._checkAttendance(guest), self._guests)
        
        if not len(self._guests) == 1:
            self.guestEmails = map(lambda guest: guest.email, self._guests)
            self.guestNames = map(lambda guest: guest.name, self._guests)
            map(lambda guest: self.guests.addGuest(guest), self._guests)
        self.author = self._eventObj.author[0].name.text
        if not len(self._eventObj.when) == 0:
            self._start_time = self._eventObj.when[0].start_time
            self._end_time = self._eventObj.when[0].end_time
            
            self.starts = Date(self._start_time)
            
            self.ends = Date(self._end_time)
            
        if not len(self._eventObj.where) == 0:
            self.place = self._eventObj.where[0].value_string
        else:
            self.__dict__.pop('place')
            
    def _checkAttendance(self, guest):
        if guest.attendee_status and guest.attendee_status.value == 'ACCEPTED':
            return True
        else:
            return False
    
    @retry(10)
    def inviteGuest(self, name, email=None):
        """
        Invite a guest to the selected event. Requires at least one parameter, the email, if two
        parameters are given, one is considered the name and the other the email.
        
        @param name: the name of the guest
        @param email: the email of the guest, default is None
        
        """
        
        
        guest = gdata.calendar.Who()
        guest.valueString = name
        guest.email = email or name
        self._eventObj.who.append(guest)
        self._client.ssl = False
        path = self._eventObj.GetEditLink().href
        path.replace('http:','https:')
        self._client.UpdateEvent(path, self._eventObj)
        self.guests.addGuest(guest)
        if self.guestEmails:
            self.guestEmails.append(guest.email)
            self.guestNames.append(guest.valueString)
        else:
            self.guestEmails = [guest.email]
            self.guestNames = [guest.valueString]
        
    
    @retry(10)
    def delete(self):
        """
        Deletes the selected event from the user's calendar
        """
        path = self._eventObj.GetEditLink().href
        path.replace('http:','https:')
        self._eventObj.send_event_notifications = None #gdata.calendar.SendEventNotifications(value='true')
        self._client.DeleteEvent(path)
        q.logger.log('Event "%s" deleted successfully'%self.title, 2)
        self._parentEvents.__dict__.pop(cleanString(self.title))
    
    
    @retry(10)   
    def update(self, title=None, summary=None, place=None, start_year=None, start_month=None, start_day=None,
            start_hour=None, start_min=None, end_year=None, end_month=None, end_day=None, end_hour=None, end_min=None, all_day=False):
        """
        Updates the selected event with the given parameters. If start date and time change to after
        end date and time, the end date and time change accordingly.
        
        
        @param title: the new title to give the event, if any
        @param summary: the new summary to give the event, if any
        @param place: the new place to give the event, if any
        @param start_year: the new start year to give the event, if any
        @param start_month: the new start month to give the event, if any
        @param start_day: the new start day to give the event, if any
        @param start_hour: the new start hour to give the event, if any
        @param start_min: the new start minute to give the event, if any
        @param end_year: the new end year to give the event, if any
        @param end_month: the new end month to give the event, if any
        @param end_day: the new end day to give the event, if any
        @param end_hour: the new end hour to give the event, if any
        @param end_min: the new end minute to give the event, if any
        @param all_day: the new boolean determining if the event is an all-day event
        """
        if title:
            self._eventObj.title = atom.Title(text=title)
            self.title = title
        if summary:
            self._eventObj.content = atom.Content(text = summary)
        if place:
            self._eventObj.where.pop()
            self._eventObj.where.append(gdata.calendar.Where(value_string = place))
        
        if start_year or start_month or start_day or start_hour or start_min or end_year or end_month or end_day or end_hour or end_min:
            old_start = self.starts
            old_end = self.ends
            
            new_start_year = start_year or int(old_start.year)
            new_start_month = start_month or int(old_start.month)
            new_start_day = start_day or int(old_start.day)
            
            new_start_hour = start_hour or int(old_start.hour)
            new_start_min = start_min or int(old_start.minute)
            
            if all_day:
                start_date = datetime.date(new_start_year, new_start_month, new_start_day)
                start_time = start_date.strftime('%Y-%m-%d')
            else:
                start_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((new_start_year, new_start_month, new_start_day, new_start_hour, new_start_min, 0, 0, 0, 0)))
            
            
            
            new_end_year = end_year or int(old_end.year)
            new_end_month = end_month or int(old_end.month)
            new_end_day = end_day or int(old_end.day)
            
            new_end_hour = end_hour or int(old_end.hour)
            new_end_min = end_min or int(old_end.minute)
            
            if new_end_year < new_start_year:
                new_end_year = new_start_year
            if new_end_year == new_start_year and new_end_month < new_start_month:
                new_end_month = new_start_month
            if new_end_year == new_start_year and new_end_month == new_start_month and new_end_day < new_start_day:
                new_end_day = new_start_day
                
            if new_end_year == new_start_year and new_end_month == new_start_month and new_end_day == new_start_day and new_end_hour < new_start_hour:
                new_end_hour = new_start_hour
            if new_end_year == new_start_year and new_end_month == new_start_month and new_end_day == new_start_day and new_end_hour == new_start_hour and new_end_min > new_start_min:
                new_end_min = new_start_min
            
            
            if all_day:
                end_date = datetime.date(new_end_year, new_end_month, new_end_day)
                end_time = end_date.strftime('%Y-%m-%d')
            else:
                end_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((new_end_year, new_end_month, new_end_day, new_end_hour, new_end_min, 0, 0, 0, 0)))
                
            self._eventObj.when.pop()
            self._eventObj.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
        
        path = self._eventObj.GetEditLink().href
        path.replace('http:','https:')
        self._client.UpdateEvent(path, self._eventObj)
        self._parentEvents._initialized = False
        

class Guests(object):
    
    def __init__(self, event):
        self._eventObj = event
        
    def addGuest(self, guestObj):
        setattr(self, cleanString(guestObj.name), Guest(guestObj))


class Guest(object):
    def __init__(self, guestObj):
        self._guestObj = guestObj
        self.name = self._guestObj.name
        self.email = self._guestObj.email
        if self._guestObj.attendee_status:
            self.status = self._guestObj.attendee_status.value
        else:
            self.status = 'INVITED'
        
    def attending(self):
        """
        Returns the attending status of the selected guest, options are:
        @return: INVITED if the guest has not yet replied to the event
                 ACCEPTED if the guest is attending the event
                 DECLINED if the guest is not attending the event
        """
        return self.status


class Date(object):
    
    def __init__(self, year, month=None, day=None, hour=None, minute=None):
        try:
            int(year)
        except ValueError:
            self.year = year[0:4]
            self.month = year[5:7]
            self.day = year[8:10]
            
            self.hour = year[11:13]
            self.minute = year[14:16]
        else:
            self.year = year
            self.month = month
            self.day = day
            
            self.hour = hour
            self.minute = minute
        
    def __repr__(self):
        return 'Date: %s/%s/%s\nTime: %s:%s'%(self.day, self.month, self.year, self.hour, self.minute)



class GoogleCalIterator(object):
    def __init__(self, dict):
        self.inputDict = dict
        self.attributes = map(lambda attr: self.inputDict[attr], filter(lambda attr: attr not in ['new', 'calendars', 'events', 'delete', None], filter(lambda attr: not attr.startswith('_'), self.inputDict.keys())))
        self.index = 0

    
    def __iter__(self):
        return self
    
    
    def next(self):
        if self.index == len(self.attributes):
            raise StopIteration()
        attr = self.attributes[self.index]
        self.index += 1
        return attr   
        
        

def cleanString(s):
    s = re.sub('[^0-9a-zA-Z_]', '', s)
    s = re.sub('^[^a-zA-Z_]+', '', s)
    return s 


