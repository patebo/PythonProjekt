from datetime import time, date, timedelta, datetime



def parse_time(txt):
    #parses the time in a string and give an output of the form datetime.time

    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    relative1 = ["last", "next"]
    relative2 = ["yesterday", "today", "tomorrow"]
    str_tokens = txt.split()
    ### Get information on the date of today
    tday = date.today()
    tday_wday = date(tday.year,tday.month,tday.day).weekday()
    d=False

    ### Insert "next" at the beginning of the token list if the given string is of the form: <day of the week> ...
    if str_tokens[0] in weekday:
        str_tokens.insert(0,"next")

    ### This part handles the string of the form: last(next) <day of the week>
    if str_tokens[0] in relative1:
        wday = weekday.index(str_tokens[1])
        if str_tokens[0] == "last":
            if tday_wday > wday:
                tdelta = timedelta(days=tday_wday-wday)
            elif tday_wday == wday:
                tdelta = timedelta(days=7)
            else:
                tdelta = timedelta(days=7-(wday-tday_wday))
            d = tday - tdelta
        else:
            if tday_wday > wday:
                tdelta = timedelta(days=7-(tday_wday-wday))
            elif tday_wday == wday:
                tdelta = timedelta(days=7)
            else:
                tdelta = timedelta(wday-tday_wday)
            d = tday + tdelta

    ### This part handles the string of the form: yesterday(today,tomorrow)
    if str_tokens[0] in relative2:
        if str_tokens[0] == "yesterday":
            d = tday -timedelta(days=1)
        elif str_tokens[0] == "today":
            d = tday
        else:
            d = tday + timedelta(days=1)
    result = d

    ### This part handles the time in the string & combine time with date
    if "at" in str_tokens:
        index_of_at = str_tokens.index("at")
        time_tokens = str_tokens[(index_of_at+1):]
        time1 = ""
        for token in time_tokens:
            time1 += token + " "
        #print (time1)
        t = parse_time(time1)
        result =datetime.combine(d,t)
    if result:
        return result

    ### This part processes the time (hour, minutes, second) and outputs a datime.time
    a= txt.split()
    if 'quarter' in a:
        a[a.index('quarter')]='fifteen'
    if 'half' in a:
        a[a.index('half')]='thirty'

    times= datetime.now()
    if ('hour' in a) or ('hours' in a):
        if 'ago' in a:
            hour= (times.hour)-(stringtonum(a[a.index('ago')-2]))
            ntime= time(hour, time.minute, time.second)
            return ntime
        elif 'in' in a:
            hour= (times.hour)+(stringtonum(a[a.index('in')+1]))
            ntime= time(hour, times.minute, times.second)
            return ntime
    elif ('minute' in a) or ('minutes' in a) or ('minutes\'' in a):
        if 'ago' in a:
            minute= (times.minute)-(stringtonum(a[a.index('ago')-2]))
            hour= (times.hour)
            if minute<0:
                hour= hour-1
                minute= 60+minute
            ntime= time( hour, minute, times.second)
            return ntime
        elif 'in' in a:
            minute= (times.minute)+(stringtonum(a[a.index('in')+1]))
            hour= times.hour
            if minute>59:
                hour= (times.hour)+1
                minute= minute-60
            ntime= time(hour, minute, times.second)
            return ntime
    elif ('second' in a) or ('seconds' in a):
        if 'ago' in a:
            second= (times.second)-(stringtonum(a[a.index('ago')-2]))
            minute= times.minute
            if second<0:
                minute= (times.minute)-1
                second= 60+second
            ntime= time(times.hour, minute, second)
            return ntime
        elif 'in' in a:
            second= (times.second)+(stringtonum(a[a.index('in')+1]))
            minute= times.minute
            if second>59:
                minute= (times.minute)+1
                second= second-60
            ntime= time( times.hour, minute, second)
            return ntime
    elif 'o\'clock' in a:
        hour= (stringtonum(a[a.index('o\'clock')-1]))
        ntime= time( hour, 0, 0)
        return ntime
    elif 'past' in a:
        hour=(stringtonum(a[a.index('past')+1]))
        minute=(stringtonum(a[a.index('past')-1]))
        ntime= time( hour, minute, 0)
        return ntime
    elif 'to' in a:
        hour=((stringtonum(a[a.index('to')+1]))-1)
        minute=60-(stringtonum(a[a.index('to')-1]))
        ntime= time(hour, minute, 0)
        return ntime
    else:
        #if the time is only given under the form "four twenty" or "two fifteen"
        hour=(stringtonum(a[0]))
        if len(a)>1:
            minute=(stringtonum(a[1]))
        else:
            minute=0
        ntime= time(hour, minute, 0)
        return ntime



def stringtonum(string):
    ###conversts a written number into an Integer
    s= string.lower()
    n= ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "twenty-one",
        "twenty-two", "twenty-three", "twenty-four", "twenty-five", "twenty-six",
        "twenty-seven", "twenty-eight", "twenty-nine", "thirty"]
    if s in n:
        return n.index(s)
