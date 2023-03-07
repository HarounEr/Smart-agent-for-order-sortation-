import sqlite3

class agent():

    #construtor 
    def __init__(self):
        pass 

    #manufactures are the only ones that stays the same day to day 
    def readRequirments(self, day):
        with sqlite3.connect("SDGP.db") as conn:
            tempReq = conn.execute("select * from requirements where dayReq=(?)", (day,))
            tempReq = tempReq.fetchall()[0]
        req = Requirements(tempReq)
        return req

    def readCourierCap(self, day):
        courierList = []
        with sqlite3.connect("SDGP.db") as conn: 
            tempReq = conn.execute("select * from courier where dayReq = (?)", (day,))
            tempReq = tempReq.fetchall()[0]
        AB11 = Courier(tempReq[1], tempReq[2])
        DA27 = Courier(tempReq[3], tempReq[4])
        ABC22 = Courier(tempReq[5], tempReq[6])
        DFA19 = Courier(tempReq[7], tempReq[8])
        CFE34 = Courier(tempReq[9], tempReq[10])

        courierList= [AB11, DA27, ABC22, DFA19, CFE34]
        return courierList

    
    
    def readComponents(self):
        componentList = []
        with sqlite3.connect("SDGP.db") as conn: 
            tempReq = conn.execute("select * from components",)
            tempReq = tempReq.fetchall()
        for i in range(len(tempReq)):
            manu = {}
            total = 0
            name = tempReq[i][0]
            for j in range(1,len(tempReq),2):
                manu[tempReq[i][j]] = tempReq[i][j+1]
                total = total + tempReq[i][j+1]
            
            if i == 0: 
                XW123 = Components(name, total, manu)
                componentList.append(XW123)
            elif i == 1: 
                XW225 = Components(name, total, manu)
                componentList.append(XW225)
            elif i == 2: 
                XW331 = Components(name, total, manu)
                componentList.append(XW331)
            elif i == 3: 
                XW127 = Components(name, total, manu)
                componentList.append(XW127)
            elif i == 4: 
                XW321 = Components(name, total, manu)
                componentList.append(XW321)
            elif i == 5: 
                XDW24 = Components(name, total, manu)
                componentList.append(XDW24)
            elif i == 6: 
                XDW31 = Components(name, total, manu)
                componentList.append(XDW31)
            elif i == 7: 
                XDW39 = Components(name, total, manu)
                componentList.append(XDW39)
            elif i == 8: 
                XDW21 = Components(name, total, manu)
                componentList.append(XDW21)
        
        return componentList

    def addToHistory(self, cList, mList, day):
        mList_f = mList[0]
        mList_s = mList[1]

        man1 = ''
        man2 = ''
        
        for i in range(1, len(mList_f)):
            man1 += str(mList_f[i][0]) + ', '
        
        for i in range(1, len(mList_s)):
            man2 += str(mList_s[i][0]) + ', '

        man1 = man1[:-2]
        man2 = man2[:-2]

        cList_f = cList[0]
        cList_s = cList[1]

        cou1 = ''
        cou2 = ''

        for i in range(1, len(cList_f)):
            cou1 += str(cList_f[i][0]) + ', '
        
        for i in range(1, len(cList_s)):
            cou2 += str(cList_s[i][0]) + ', '

        cou1 = cou1[:-2]
        cou2 = cou2[:-2]

        print(mList_f[0][0],mList_f[0][1],day,man1,cou1)
        print(mList_s[0][0],mList_s[0][1],day,man2,cou2)

        with sqlite3.connect("SDGP.db") as conn:
            conn.execute("insert into history (component, dayReq, quantity, manufacturer, courier) values (?, ?, ?, ?, ?)",(mList_f[0][0], day, mList_f[0][1], man1, cou1))
            conn.execute("insert into history (component, dayReq, quantity, manufacturer, courier) values (?, ?, ?, ?, ?)",(mList_s[0][0], day, mList_s[0][1], man2, cou2))
            conn.commit()

    def sort(self, day):
        manufacturersUsed= [[],[]]
        couriersUsed = [[],[]]
        req = self.readRequirments(day)
        courierList = self.readCourierCap(day)
        componentList = self.readComponents()
        #read requirments
        #list of required components and their quantiy
        requirements = [req.getComp1(),req.getComp2()]

        #list of component objects 
        selComp = []

        #find the required components from the list and adds them to selComp
        for i in range(2):
            for comp in componentList:
                if comp.getName() == requirements[i][0]: #tested
                    selComp.append(comp)

        #take compnents and update list 
        for i in range(2):
            quantity, capacity = [requirements[i][1]]*2
            manufacturerDict = selComp[i].getManufacturer()
            manufacturersUsed[i].append([selComp[i].getName(), quantity])
            couriersUsed[i].append([selComp[i].getName(), capacity])
            #find manufacturer with high cap
            manufacturerKeys = [x for x in manufacturerDict]
            repeats = 0 
            highMan = [manufacturerKeys[0], manufacturerDict[manufacturerKeys[0]]]
            #print(highMan)
            while quantity != 0: # while we still need quantity
                visitiedMan = []
                for x in range(1,len(manufacturerKeys)):
                    if manufacturerDict[manufacturerKeys[x]] > highMan[1] and manufacturerKeys[x] not in visitiedMan: #search for the highest cap manufacturer
                        highMan = [manufacturerKeys[x], manufacturerDict[manufacturerKeys[x]]]
                visitiedMan.append(highMan[0])
                quanUsed, highMan[1], quantity = selComp[i].updateManQuantity(highMan[0], quantity)
                manufacturersUsed[i].append([highMan[0], quanUsed])
                repeats += 1
                if repeats == len(manufacturerKeys) and quantity != 0:
                    print("Insufficient manfucturer capacities to furfill order. {} items not found.".format(quantity))
                    break
            
            repeats = 0
            highCour = courierList[0]
            while capacity != 0:
                visitiedCour = []
                for x in range(1, len(courierList)):
                    if courierList[x].getCapacity() > highCour.getCapacity() and courierList[x].getName() not in visitiedCour:
                        highCour = courierList[x]
                visitiedCour.append(highCour.getName())
                capUsed, capacity = highCour.setCapacity(capacity)
                couriersUsed[i].append([highCour.getName(), capUsed])
                repeats += 1
                if repeats == len(courierList) and capacity != 0:
                    print("Insufficient courier capacities to furfill order. {} items not found.".format(quantity))
                    break
        self.addToHistory(couriersUsed, manufacturersUsed, day)
        #find courier and send items 
        return couriersUsed, manufacturersUsed



class Requirements():

    def __init__(self, list):
        self.day = list[0]
        self.comp1 = list[1] 
        self.quant1 = list[2]
        self.comp2 = list[3]
        self.quant2 = list[4] 

    def getDay(self):
        return self.day 

    def getComp1(self):
        return self.comp1, self.quant1

    def getComp2(self):
        return self.comp2, self.quant2

    def __str__(self):
        return "day: "+str(self.day)+" comp1: "+str(self.comp1)+" quant1: "+str(self.quant1)+" comp2: "+str(self.comp2)+" quant2: "+str(self.quant2) 

class Courier(): 

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def getDay(self):
        return self.day 

    def getName(self):
        return self.name

    def getCapacity(self):
        return self.capacity

    def setCapacity(self, numUsed):
        capUsed = 0
        if self.capacity == 0:
            return capUsed, numUsed
        elif self.capacity - numUsed < 0:
            capUsed = self.capacity
            quantityLeft = numUsed - self.capacity 
            self.capacity = 0
            return capUsed, quantityLeft
        else: 
            capUsed = numUsed
            self.capacity = self.capacity - numUsed
            return capUsed, 0

    #read database for capitcity of each courier add to constructor 

    #update capiticity for each after order completion 

class Components():
    
    def __init__(self, name, quantity, manufacturer):
        self.name = name
        self.totalQuantity = quantity
        self.manufacturer = manufacturer
    
    def getName(self):
        return self.name

    def getTotalQuantity(self):
        return self.totalQuantity

    def getManufacturer(self):
        return self.manufacturer

    def findManufacturer(self, man):
        return self.manufacturer[man]

    def updateManQuantity(self, man, numUsed):
        quanUsed = 0
        if self.manufacturer[man] == 0:
            return quanUsed, self.manufacturer[man], numUsed
        elif self.manufacturer[man] - numUsed < 0:
            quanUsed = self.manufacturer[man]
            quantityLeft = numUsed - self.manufacturer[man] 
            self.manufacturer[man] = 0
            return quanUsed, self.manufacturer[man], quantityLeft
        else: 
            quanUsed = numUsed
            self.manufacturer[man] = self.manufacturer[man] - numUsed
            return quanUsed, self.manufacturer[man], 0
            
                
    def __str__(self):
        return "Name :"+self.name+" Quantity :"+str(self.totalQuantity)+" Manufacturer :"+self.manufacturer



def select_courier():
    with sqlite3.connect("SDGP.db") as conn: 
        temp_courier = conn.execute("select * from courier",)
        temp_courier = temp_courier.fetchall()
    
    return temp_courier

def select_manufacturers():
    with sqlite3.connect("SDGP.db") as conn: 
        temp_man = conn.execute("select * from components",)
        temp_man = temp_man.fetchall()

    return temp_man

def select_order_history():
    with sqlite3.connect("SDGP.db") as conn: 
        temp_history = conn.execute("select * from history",)
        temp_history = temp_history.fetchall()

    return temp_history

def delete_order_history():
    with sqlite3.connect("SDGP.db") as conn: 
        temp_history = conn.execute("delete from history",)
        temp_history = temp_history.fetchall()

def select_requirements():
    with sqlite3.connect("SDGP.db") as conn: 
        temp_req = conn.execute("select * from requirements",)
        temp_req = temp_req.fetchall()

    return temp_req

# not working properly
def update_requirements(day,quantity,new_quantity):
    with sqlite3.connect("SDGP.db") as conn: 
        temp_req = conn.execute("update requirements set",)
        temp_req = temp_req.fetchall()

    return temp_req

ai = agent()


#print(select_courier()[0])
#print(select_manufacturers())
#delete_order_history()
#print(select_order_history())
#print(select_requirements())

#ai.sort(1)

#print(ai.readRequirments(1))
#comp = ai.readComponents()
#print(comp[0].getManufacturer())
#lists = ai.sort(1)

#print(ai.readComponents())

#print(lists)