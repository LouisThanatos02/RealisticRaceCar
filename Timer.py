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
        for i in self.times :
            if(i != 0):
                self.times_ch.append(i - self.times[0])
        #print(self.times_ch)
        
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
            