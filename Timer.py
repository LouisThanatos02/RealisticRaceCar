import datetime

class Timer:
    def __init__(self): 
        self.timer_range = 7
        self.insert = 0
    #def start(self):
        #self.times.append(datetime.datetime.now())

    def getTime(self):
        self.times[self.insert] = datetime.datetime.now()
        #print(self.times[-1] - self.times[0])

    def getAll(self):
        #self.times_ch = [0,0,0,0,0,0,0]
        math = self.times[self.insert] - self.times[0]
        min = int(math.seconds/60)
        if(min < 10):
            min_str = '0'+str(min)
        else:
            min_str = str(min)

        sec = math.seconds%60
        if(sec < 10):
            sec_str = '0'+str(sec)
        else:
            sec_str = str(sec)

        milli = int(math.microseconds/10000)
        if(milli < 10):
            milli_str = '0'+str(milli)
        else:
            milli_str = str(milli)

        self.times_ch[self.insert] = min_str +':'+ sec_str +'.'+ milli_str
        #print(self.times_ch)
        return self.times_ch

    def reset(self):
        self.set()

    def set(self):
        self.times = []
        self.times_ch = []
        for i in range(self.timer_range):
            self.times.append(datetime.datetime.now())
            self.times_ch.append('')
        self.insert = 0
        

if __name__ == "__main__":
    timer = Timer()
    timer.set()
    ch = ''
    while(ch != '5'):
        ch = input('(1)開始+單圈 (2)重新計時 (4)離開 : ')
        try:
            if(ch == '1'):
                timer.getTime()
                print(timer.getAll())
                timer.insert += 1
            if(ch == '2'):
                timer.reset()
            if(ch == '3'):
                timer.reset()
            if(ch == '4'):
                break
        except:
            print('The End')
            break
            