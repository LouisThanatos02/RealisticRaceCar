import datetime

class Timer:
    def __init__(self):
        self.reset()   

    #def start(self):
        #self.times.append(datetime.datetime.now())

    def getTime(self):
        self.times.append(datetime.datetime.now())
        #print(self.times[-1] - self.times[0])

    def getAll(self):
        self.times_ch = []
        for i in range(len(self.times)) :
            math = self.times[i] - self.times[0]
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

            self.times_ch.append(min_str +':'+ sec_str +'.'+ milli_str)
        print(self.times_ch)
        return self.times_ch
         
    def reset(self):
        self.times = []
        self.times_ch = [] 
        

if __name__ == "__main__":
    timer = Timer()
    ch = ''
    while(ch != '5'):
        ch = input('(1)開始 (2)單圈 (3)重新計時 (4)停止 (5)離開 : ')
        if(ch == '1'):
            timer.getTime()
        if(ch == '2'):
            timer.getTime()
        if(ch == '3'):
            timer.reset()
        if(ch == '4'):
            timer.getAll()
        if(ch == '5'):
            break
            