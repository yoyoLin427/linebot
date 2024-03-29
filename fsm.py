from transitions.extensions import GraphMachine

from utils import send_text_message

import random

from string import Template

n_list=[0,1,2,3,4,5,6,7,8,9]
anslist=[1,2,7,4]

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        text = event.message.text
        return text.lower() == "start"

    def is_going_to_guess(self, event):
        text = event.message.text
        return text.lower() == "ok"

    def is_going_to_check(self, event):
        text = event.message.text
        print(len(text))
        if text.isdigit() and len(text) == 4:
            return True
        else:
            return False

    

    def on_enter_start(self, event):
        print("I'm entering start")
        global anslist

        anslist = random.sample(n_list,4)
        print("answer is")
        print(anslist)

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入 ok 開始玩遊戲!\n\n規則:\n謎底為一個四位數號碼(數字不重複)\n機器人會回復線索,以?A?B形式呈現，直到答對(4A0B)為止。\n(例如:當謎底為8123，而猜謎者猜1052時，出題者必須提示0A2B)")


    def on_enter_guess(self, event):
        print("I'm entering guess")
        print("answer is")
        print(anslist)

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入一個四位數號碼,數字不得重複")

    
    def on_enter_check(self, event):
        print("I'm entering check")
        print("answer is")
        print(anslist)

        
        A = 0
        B = 0
        Number = event.message.text
        print(Number)
        for i in range(4):        #算出相同位置數字相等的數字有幾個
            if (str(anslist[i]) == Number[i]):
                A = A+1
        for j in range(4): #算出數字相等的有幾個
            for k in range(4):
                if (str(anslist[j]) == Number[k]) and j!=k:
                    B = B+1 
        print("A is")
        print(A)
        print("B is")
        print(B)
        if A==4 and B ==0:
            msg=str(A)+"A"+str(B)+"B"+"\n恭喜你答對了!如果要繼續玩請輸入 start"
            reply_token = event.reply_token
            send_text_message(reply_token,msg)
            self.goto_user(event)
        else:
            msg=str(A)+"A"+str(B)+"B"+"\n請繼續輸入一個四位數號碼,數字不得重複"
            reply_token = event.reply_token
            send_text_message(reply_token,msg)
            self.goto_guess(event)