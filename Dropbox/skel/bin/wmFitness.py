#!/usr/bin/env python


#todo
# reset input boxes after add data
# delete data
# modify data

import pygtk
pygtk.require('2.0')
import gtk
import sqlite3
import datetime
import string
import time

version = 'v.02'
debug = 0

def addtext(TV,text):
    buffer = TV.get_buffer()
    iter = buffer.get_iter_at_mark(buffer.get_insert())
    mark = buffer.create_mark("end", buffer.get_end_iter(), False)
    buffer.insert(iter,text)   # use "\n" for newlines
    TV.scroll_to_mark(mark, 0.05, True, 0.0, 1.0)
    
class wjmFitness:
    now = datetime.datetime.now()
    def __init__(self,x,y):
        
        self.marked_date = 31*[0]
        
        self.textview = gtk.TextView()
        # create windwow
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(400,550)
        self.window.set_title('wjmFitness')
        
        self.mainbox = gtk.VBox(False,0)
        self.window.add(self.mainbox)
        
        # gui elements
        self.combobox = gtk.combo_box_new_text()

        self.bbutton0 = gtk.Button('Monthly  ')
        self.bbutton1 = gtk.Button('Weekly   ')
        self.bbutton2 = gtk.Button('Reports   ')
        self.bbutton3 = gtk.Button('  ')
        
        self.mbutton0 = gtk.Button('M1 ')
        self.mbutton0.set_border_width(15)
        self.mbutton1 = gtk.Button('M2 ')
        self.mbutton1.set_border_width(15)
        self.mbutton2 = gtk.Button('M3 ')
        self.mbutton2.set_border_width(15)
        self.mbutton3 = gtk.Button('M4 ')
        self.mbutton3.set_border_width(15)
        
        self.button1 = gtk.Button(stock=gtk.STOCK_ADD)
        self.button2 = gtk.Button(stock=gtk.STOCK_CLOSE)
        
        self.entry1 = gtk.Entry()
        self.entry1.set_editable(False)
        self.entry2 = gtk.Entry()
        self.entry3 = gtk.Entry()
        
        self.label0 = gtk.Label('Type:')
        self.label1 = gtk.Label('       Date:           ')
        self.label2 = gtk.Label('   Workout Time:')
        self.label3 = gtk.Label('   Workout Distance:')
        
        self.calendar = gtk.Calendar()

        frame1 = gtk.Frame('Fitness Calendar')
        frame2 = gtk.Frame('Workouts')
        
        # multi line text area
        frame2 = gtk.Frame('Fitness Data')
        sw = gtk.ScrolledWindow(hadjustment=None)
        sw.add(self.textview)
        sw.set_size_request(200,150)
        self.textview.set_editable(False)
        self.textview.get_buffer().set_text('        ------------[ wjmFitness %s ]------------             \n        by William J. MacLeod                  \n'% version)
        frame2.add(sw)
        
        #box to hold button bar
        box0 = gtk.HBox(False,0)
        
        # box to hold entry boxes
        box1 = gtk.HBox(False,5)

        # box to hold buttons side by side
        box2 = gtk.HBox(False,5)
        box3 = gtk.HBox(False,5)
        #box for labels
        box5 = gtk.HBox(False,5)

        frame1.add(self.calendar)
        box4 = gtk.VBox(False,5)
        
        # pack boxes now
        box0.pack_start(self.bbutton0,True,True,1)
        box0.pack_start(self.bbutton1,True,True,1)
        box0.pack_start(self.bbutton2,True,True,1)
        box0.pack_start(self.bbutton3,True,True,1)
        
        box1.pack_start(self.combobox,True,True,1)
        box1.pack_start(self.entry1,True,True,1)
        box1.pack_start(self.entry2,True,True,1)
        box1.pack_start(self.entry3,True,True,1)

        box2.pack_start(self.button1,True,True,5) # Add Button
        box2.pack_start(self.button2,True,True,5) # Close button
        
        box3.pack_start(frame1,True,True,1)
        box3.pack_start(box4,True,True,1)
        
        box4.pack_start(self.mbutton0,True,True,5)
        box4.pack_start(self.mbutton1,True,True,5)
        box4.pack_start(self.mbutton2,True,True,5)
        box4.pack_start(self.mbutton3,True,True,5)

        box5.pack_start(self.label0,True,True,1)
        box5.pack_start(self.label1,True,True,1)
        box5.pack_start(self.label2,True,True,1)
        box5.pack_start(self.label3,True,True,1)

        
        # Pack gui elements into the main window
        self.mainbox.pack_start(box0,True,True,0)
        self.mainbox.pack_start(box3,True,True,0)
        self.mainbox.pack_start(frame2,True,True,0)
        self.mainbox.pack_start(box5,True,True,0)
        self.mainbox.pack_start(box1,True,True,5)
        self.mainbox.pack_start(box2,True,True,5)

        # combo box elements
        self.combobox.append_text('Workout Type:')
        self.combobox.append_text('Run')
        self.combobox.append_text('Bike')
        self.combobox.set_active(1)
        
        # entry box elements
        self.entry1.set_max_length(10)
        self.entry1.set_text(self.now.strftime('%m/%d/%Y'))
        self.entry2.set_max_length(10)
        self.entry2.set_text('00:00:00')
        self.entry3.set_max_length(10)
        self.entry3.set_text('0.0')

        # macro button connect events
        self.mbutton0.connect("clicked",self.macrohandler,'3.4')
        self.mbutton1.connect("clicked",self.macrohandler,'5.7')
        self.mbutton2.connect("clicked",self.macrohandler,'15.9')
        self.mbutton3.connect("clicked",self.macrohandler,'3.4')

        #button bar connect events
        self.bbutton0.connect("clicked",self.bbarhandler,"monthlydist")
        self.bbutton1.connect("clicked",self.bbarhandler,"weeklydist")
        self.bbutton2.connect("clicked",self.bbarhandler,"reports")
        self.bbutton3.connect("clicked",self.current,"now")

        # connect events with callbacks
        self.button1.connect("clicked", self.add_data, self.entry1, self.entry2, self.entry3 )
        self.button2.connect("clicked", lambda w: gtk.main_quit())

        #calendar connect items
        self.calendar.connect("day_selected_double_click",self.calendar_day_selected_double_click)
        self.calendar.connect("day_selected",self.calendar_day_selected,)
        self.calendar.connect("month_changed", self.calendar_month_changed)
        self.calendar.connect("prev_year", self.calendar_year_changed)
        self.calendar.connect("next_year", self.calendar_year_changed)

        self.window.connect("delete_event", lambda w,e: gtk.main_quit())

        self.window.show_all()  # displays window and all components
        self.window.move(x,y)
        self.update_calendar()
   
    def macrohandler(self,widget,source):
        self.entry3.set_text(source)
    
    def bbarhandler(self,widget,source):
        if source == 'monthlydist':
            self.monthly_dist()
        if source == 'weeklydist':
            self.weekly_dist() 
        if source == 'reports':
            self.reports()
    
    def add_data(self,widget,eDate,eTime,eDist):
        
        # get workout type from combobox
        model = self.combobox.get_model()
        index = self.combobox.get_active()
        self.woType = model[index][0]
        
        # get date from calendar entry box
        year, month, day = self.calendar.get_date()
        month = month+1
        self.woDate = datetime.date(year,month,day)
        
        # get workout time from entrybox
        self.woTime = eTime.get_text()
        
        # get workout distance from entybox
        self.woDist = float(eDist.get_text())
        #clear textview 
        self.clearbuffer = self.textview.get_buffer().set_text('')
        
        # start database communication
        connection = sqlite3.connect('wmFitness.db')
        cur = connection.cursor()
        cur.execute('INSERT INTO workout VALUES (null, ?, ?, ?, ?)', (self.woType, self.woDate, self.woTime, self.woDist))
        # display workout 
        cur.execute ('SELECT * FROM workout')
        for row in cur:
            self.textview.get_buffer().set_text('        ------------[ wjmFitness %s ]------------             \n' %version)
            addtext(self.textview,'-'*20 +'\n')
            addtext(self.textview,'Workout Type: '+str(row[1])+'\n')
            addtext(self.textview,'Date: '+ datetime.datetime.strptime(row[2],'%Y-%m-%d').strftime('%m/%d/%Y')+'\n')
            addtext(self.textview,'Time: '+ str(row[3])+'\n')
            addtext(self.textview,'Distance: '+ str(row[4])+'mi\n')
            addtext(self.textview,'-'*20 )
        cur.close()
        connection.commit()
        connection.close()
        
        #update calendar marks
        self.update_calendar()

    def calendar_date_to_string(self):
        year, month, day = self.calendar.get_date()
        mytime = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        return time.strftime("%x", time.localtime(mytime))
    
    def calendar_day_selected(self, widget):
        buffer = self.calendar_date_to_string()
        self.entry1.set_text(buffer)
    
    def calendar_day_selected_double_click(self, widget):
        #buffer = self.calendar_date_to_string() +'\n'
        buffer = self.calendar_date_to_string()
        #addtext(self.textview,buffer) 
        self.year, self.month, self.day = self.calendar.get_date()
        self.month = self.month+1
        self.date_lookup() 
       
    def date_lookup(self):
        connection = sqlite3.connect('wmFitness.db')
        year, month, day = self.calendar.get_date()
        date = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        date = time.strftime("%x", time.localtime(date))
        date = datetime.datetime.strptime(date,'%m/%d/%Y').strftime('%Y-%m-%d')
        date = (date,)
        cur = connection.cursor() 
        self.textview.get_buffer().set_text('        ------------[ wjmFitness %s ]------------             \n' %version)
        cur.execute('SELECT * FROM workout WHERE woDate = ?',date)  
        for row in cur:
            self.textview.get_buffer().set_text('        ------------[ wjmFitness %s ]------------             \n' %version)
            addtext(self.textview,'-'*20 +'\n')
            addtext(self.textview,'Workout Type: '+str(row[1])+'\n')
            addtext(self.textview,'Date: '+ datetime.datetime.strptime(row[2],'%Y-%m-%d').strftime('%m/%d/%Y')+'\n')
            addtext(self.textview,'Time: '+ str(row[3])+'\n')
            addtext(self.textview,'Distance: '+ str(row[4])+'mi\n')
            addtext(self.textview,'-'*20 )
        cur.close()
        connection.close() 
        
    def update_calendar(self):
        year, month, day = self.calendar.get_date()
        month = month+1 
        month = datetime.datetime.strptime(str(month),'%m').strftime('%m') 
        connection = sqlite3.connect('wmFitness.db')
        cur = connection.cursor()
        try:
            cur.execute('SELECT woDate FROM workout')
            for row in cur:
                woDay = datetime.datetime.strptime(row[0],'%Y-%m-%d').strftime('%d')
                woMonth = datetime.datetime.strptime(row[0],'%Y-%m-%d').strftime('%m')
                woYear = datetime.datetime.strptime(row[0],'%Y-%m-%d').strftime('%Y')
                if woMonth == month and woYear == str(year):
                    self.mark_calendar(woDay)
        except sqlite3.OperationalError:
            cur.execute('CREATE TABLE workout ( id INTEGER PRIMARY KEY, type VARCHAR(10), woDate DATE, time BLOB, distance FLOAT)')
        cur.close()
        connection.close()
    
    def mark_calendar(self,day):
         day = int(day)
         if self.marked_date[day-1] == 0:
            self.calendar.mark_day(day)

    def calendar_month_changed(self, widget):
        self.calendar.clear_marks()
        self.update_calendar() 
    
    def calendar_year_changed(self, widget):
        self.calendar.clear_marks()
        self.update_calendar()
    
    def monthly_dist(self):
        connection = sqlite3.connect('wmFitness.db')
        cur = connection.cursor()
        year,month,day = self.calendar.get_date()
        month = month+1
        month = datetime.datetime.strptime(str(month),'%m').strftime('%m')
        year = datetime.datetime.strptime(str(year),'%Y').strftime('%Y')
        cur.execute("SELECT time,distance FROM workout WHERE strftime('%m', woDate)=? AND strftime('%Y',woDate)=?", (month,year))
        mi=float() 
        fin = datetime.timedelta() 
        for row in cur:
            mi = mi + row[1]       
            d1 =  datetime.datetime.strptime(row[0],"%H:%M:%S")
            dt1 = datetime.timedelta(minutes=d1.minute, seconds=d1.second)
            fin = fin + dt1    
        self.textview.get_buffer().set_text('        ------------[ wjmFitness %s Reports]------------             \n' %version) 
        self.output('\n Monthly Distance: '+ str(mi)+' mi')
        self.output('\n Monthly Time Total: '+ str(fin)+' \n')
        cur.close()
        connection.close()
    
    def weekly_dist(self):
        connection = sqlite3.connect('wmFitness.db')
        cur = connection.cursor()
        year,month,day = self.calendar.get_date()
        month = month+1
        date = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        date = time.strftime("%x", time.localtime(date))
        week = datetime.datetime.strptime(date,'%m/%d/%Y').strftime('%W')
        year = datetime.datetime.strptime(date,'%m/%d/%Y').strftime('%Y')
        week = int(week)-4
        week = str(week)
        cur.execute("SELECT time,distance FROM workout WHERE strftime('%W', woDate)=? AND strftime('%Y',woDate)=?",(week,year))
        mi=float() 
        fin = datetime.timedelta() 
        for row in cur:
            mi = mi + row[1]       
            d1 =  datetime.datetime.strptime(row[0],"%H:%M:%S")
            dt1 = datetime.timedelta(minutes=d1.minute, seconds=d1.second)
            fin = fin + dt1
        self.textview.get_buffer().set_text('        ------------[ wjmFitness %s Reports]------------             \n' %version)
        self.output('\n Weekly Distance: '+ str(mi)+' mi')
        self.output('\n Weekly Time Total: '+ str(fin)+' \n') 
        cur.close()
        connection.close()
    
    def current(self,widget,type):
        connection = sqlite3.connect('wmFitness.db')
        cur = connection.cursor()
        year,month,day = self.calendar.get_date()
        month = month+1
        month = datetime.datetime.strptime(str(month),'%m').strftime('%m')
        year = datetime.datetime.strptime(str(year),'%Y').strftime('%Y')
        cur.execute("SELECT time, distance FROM workout WHERE strftime('%m', woDate)=? AND strftime('%Y',woDate)=?", (month,year)) 
        mi=float() 
        fin = datetime.timedelta() 
        for row in cur:
            mi = mi + row[1]       
            d1 =  datetime.datetime.strptime(row[0],"%H:%M:%S")
            dt1 = datetime.timedelta(minutes=d1.minute, seconds=d1.second)
            fin = fin + dt1
        
        self.output('Total Time: '+ str(fin)+ '\n')
        self.output('Total Mileage: '+str(mi)+ ' mi \n') 
        cur.close()
        connection.close()
    
    def output(self,message):
        addtext(self.textview,' '+ message)

    def reports(self):
        self.textview.get_buffer().set_text('        ------------[ wjmFitness %s Reports]------------             \n' %version)
        self.weekly_dist()
        self.monthly_dist()


wjmFitness(200,20)
gtk.main()
