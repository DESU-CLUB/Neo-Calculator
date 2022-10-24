import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
import math
#Today's task -> Comeup with basic display
#Tmr task -> Understand RPN (Shunting Yard Algo)
#PHASE 1: BASIC CALCULATOR -> COMPLETE
#PHASE 2: CALCULATOR WITH EXTRA FRAME AND EXTRA FUNCTIONS (RIGHT ASSOCIATIVE)
#PHASE 3: Break each frame into separate class

class Stack():
    def __init__(self):
        self.stack = []
        
    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()
        else:
            return None
    
    def push(self,item):
        self.stack.append(item)

    def length(self):
        return len(self.stack)

    def peek(self):
        if len(self.stack) > 0:
            return self.stack[-1] 

    def isEmpty(self):
        if self.length() == 0:
            return True

class App(tk.Frame, object):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.pack() #Class way of creating root window

        #This will be the calculator display
        self.displayFrame = tk.Frame(relief = 'sunken',highlightbackground = 'black',highlightthickness = 1)
        self.display = tk.Label(master=self.displayFrame)
        self.displayFrame.pack(fill = 'x')
        self.display.pack()
        self.error = False
        

        #This will be the keypads
        self.btnlist = {}
        self.keyFrame = tk.Frame(master = master)
        self.keyFrame.grid()
        self.keyFrame.pack(expand = True,fill="both")
        
        
    
        
        self.buttons = [

                    ['C','%','Del','/'],
                    ['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],                                
                    ['(','0',')','='] 
        ]           
                                        
        self.bindings = {}        
        for charlist in self.buttons:
            for char in charlist:
               self.bindings[char] = char
        self.bindings['C'] = 'Tab'
        self.bindings['Del'] = 'BackSpace'
        self.bindings['-'] = 'minus'
        self.bindings['+'] = 'plus'
        self.bindings['%'] = 'percent'
        self.bindings['/'] = 'slash'
        self.bindings['*'] = 'asterisk'
        self.bindings['('] = 'parenleft'
        self.bindings[')'] = 'parenright'
        for i in range(len(self.buttons)):
            self.keyFrame.columnconfigure(i,weight = 1, minsize = 30)
            self.keyFrame.rowconfigure(i, weight = 1,minsize = 30)
            for j in range(len(self.buttons[i])):
                val = self.buttons[i][j]
                btn = tk.Button(self.keyFrame,text = val,pady = 5,padx = 5, relief = tk.RAISED, command = lambda x = val: self.updateLabel(x))
                self.btnlist[val] = btn
                self.btnlist[val].grid(row = i, column = j,padx = 5,pady = 5,sticky = 'NSEW')

    def updateLabel(self,prompt):
        nowtext = self.display.cget("text")
        if "Syntax Error" in nowtext:
            print("WHY NOT WORKING")
            self.display.configure(text = '')
            nowtext = ''
             

        if prompt == '=':
             out = self.calculate(nowtext)
             self.display.configure(text = out)
        elif prompt == 'C':
            self.display.configure(text = '')
        elif prompt == 'Del':
            self.display.configure(text = nowtext[:-1])
        elif prompt in self.bindings:
            self.display.configure(text = nowtext+prompt)
        else:
            self.display.configure(text = "Syntax Error")

    def new_method(self):
        pass

    def calculate(self,text):
        print("Syntax Error" in text)
        if "Syntax Error" in text:
            print('hi')
            self.display.configure(text = ' ')
            return ''

        inp = self.to_rpn(text)
        print(inp)

        if inp == None:
             return 'Syntax Error'

        numstack = Stack()
        tokens = inp.stack
        while not inp.isEmpty():
            val = tokens.pop(0)
            if val not in '-/+*%':
                numstack.push(val)
            else:
                right = numstack.pop()
                left = numstack.pop()
                if left ==None or right == None:
                    self.display.configure(text = 'Syntax Error')
                    print('hi')
                else:
                    right,left = float(right),float(left)
                    pass
                if val == '-':
                    result = left - right
                elif val == '+':
                    result = left+right
                elif val == '/':
                    result = left/right
                elif val == '%':
                    result = left%right
                else:
                    result = left*right
                   
                numstack.push(result)
        
        if numstack.length()!= 1:
            print('hello! wrong already!')
            self.display.configure(text = 'Syntax Error')
            pass
        else:
            return str(numstack.pop())

                   




        

    def to_rpn(self,text):
        #First, need to format the thing properly
        charlist = list(text)
        newcharlist = []
        ops = {'+':1,'-':1,'*':2,'/':2,'%':2,'(':0,')':0}
        currnum = ''
        if charlist[0] == '-' and charlist[1] not in ops:
            charlist.pop(0)
            charlist[0]  = '-'+charlist[0]

        for i in charlist:
            if i not in ops:
                currnum+=i
            else:
                if currnum !='':
                    newcharlist.append(currnum)
                    currnum = ''
                newcharlist.append(i)
        if currnum != '':
            newcharlist.append(currnum)
        print(newcharlist,'hi')
        #Next, need to do RPN conversion
        opstack = Stack()
        out = Stack()
        for i in newcharlist:
            if i not in ops:
                out.push(i)
            else:
                curop = i
                print(opstack.stack,i)
                if curop in '-+/*%':
                    while not opstack.isEmpty() and ops[curop] <= ops[opstack.peek()]:
                        out.push(opstack.pop())
                    opstack.push(curop)
                    

                elif curop == ')':
                    while not opstack.isEmpty() and opstack.peek() !='(':
                        out.push(opstack.pop())
                    if opstack.isEmpty():
                        return None
                    opstack.pop()

                elif curop == '(':
                    opstack.push(curop)

                else:
                    out.push(curop)
        print(out.stack)
        while not opstack.isEmpty():
            val = opstack.pop()
            if val == '(':
                return None
            else:
                out.push(val)
        print(out.stack)

        return out

                

                
                

           
           
               






    
        

root = tk.Tk()
myApp = App(root) #Creates instance of App,using window created
myApp.mainloop() #Runs program