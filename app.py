import RPi.GPIO as GPIO
import lcddriver
import urllib
from evdev import InputDevice, categorize, ecodes
from time import *

server = "http://127.0.0.1/api"






GPIO.setmode(GPIO.BCM)
lcd = lcddriver.lcd()

def my_callback(channel):
    	print "falling edge detected on 7"
	params = urllib.urlencode({'cmd':0})
        urllib.urlopen(server, params)





def lcdclear(arg):
	if arg ==1:
		lcd.lcd_display_string("                ",1)
	elif arg ==2:
		lcd.lcd_display_string("                ",2)
	else:
		lcd.lcd_display_string("                ",1)
		lcd.lcd_display_string("                ",2)


def main():

	GPIO.setup(7, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(9, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(10, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(11, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(7, GPIO.RISING, callback=my_callback, bouncetime=200)
	dev = InputDevice('/dev/input/event0')
	key = [55,69,71,72,73,74,75,76,77,78,79,80,81,82,83,96,98]
	keyval = ['*','Num','7','8','9','-','4','5','6','+','1','2','3','0','.','En','/']
	list_menu = [	" ",	
			"Chicken Noodle",
			"Pork Noodle",
			"Prawn Noodle",
			"Pork Congee",
			"Prawn Wonton Soup",
			"Braised Beef Clear Soup",
			"Pork Clear Soup",
			"Roast Chicken Wings",
			"Chicken in Brown Sauce with Rice",
			"Savoury Pork Burger with Rice",
			"Chicken & Basil with Rice",
			"Chicken Panang Curry with Rice",
			"Beef Panang Curry with Rice",
			"Chicken Green Curry with Rice",
			"Beef Green Curry with Rice",
			"Chicken Curry & Condiments with Rice",
			"Tom Kha Kai with rice",
			"Shrimp in Red curry with Rice",
			"Roast Chicken with Rice",
			"Tom-Yum-Goong",
			"Marinated London Broil",
			"Peppered New York Strip Steak",
			"Carne Asada",
			"Cowboy Steak",
			"Michael Jordan's 23 Delmonico Steak",
			"Herb-Crusted Fillet Mignon",
			"Oriental Tri-Tip Steak",
			"Basil-Oregano T-Bone Steaks",			
			"Cumin Marinated Skirt Steak",
			"Southwestern Tri-Tip Steak"
								] 
	cost_menu = [	0,
			30,
                        30,
                        35,
                        25,
                        35,
                        40,
                        35,
                        30,
                        35,
                        35,
                        35,
			35,
			40,
			40,
			40,
			35,
			40,
			79,
			69,
			79,
			79,
			89,
			79,
			79,
			89,
			79,
			79,
			89,
			79,
			99
			 	]
	orderid=1
	while True:
		lcd.lcd_display_string("SELECT MENU 1-30",1)
		text = ""
		#state 1
		print "State 1"
		next = False
		menu = ""
		queue = []
		while not next:    
			for event in dev.read_loop():
				if ( event.type == ecodes.EV_KEY )&( event.value ==1 ):
					if event.code in key:
						if event.code == 69:
							lcdclear(2)
							menu = ""
							lcd.lcd_display_string(menu,2)
						elif event.code == 96:
							try:
                                                                tmp = int(menu)
                                                        except:
                                                                tmp=0							
							if tmp in range(1,31):
								print menu								
								next = True
							else:
								lcdclear(2)
								menu = ""
						else:
							menu += keyval[key.index(event.code)]
							lcd.lcd_display_string(menu,2)
				if next:
					queue.append(menu)
					break

		print "amount"  
		#state 2
		print "State 2"
		next = False
		amountval = []
		amount = ""
		tmp = 0
		lcdclear(3)
		lcd.lcd_display_string("SELECT QUANTITY",1)
		while not next:
			for event in dev.read_loop():
				if ( event.type == ecodes.EV_KEY )&( event.value ==1 ):
					if event.code in key:
						if event.code == 69:
							lcdclear(2)
							amount = ""
							lcd.lcd_display_string(amount,2)
						elif event.code == 96 :
							try:
    								tmp = int(amount)
							except:
								tmp=0
							if tmp in range (1,6):
								next = True
							else:
								lcdclear(2)
								amount = ""
						else:
							amount += keyval[key.index(event.code)]
							lcd.lcd_display_string(amount,2)
				if next:
					amountval.append(amount)
					break


		#state 3
		print queue , amountval
		print "State 3"
		next = False
		lcdclear(3)
		cost = cost_menu[int(queue[0])]*int(amountval[0])
		print cost
		while not next:
			text = "INSERT COINS "+str(cost)
			lcd.lcd_display_string(text,1)
			if GPIO.input(10)==True:
				cost -= 1
				sleep(0.2)    
				lcd.lcd_display_string("INSERT COINS    ",1)
			if GPIO.input(11)==True:
				cost -= 5
				sleep(0.2)
				lcd.lcd_display_string("INSERT COINS    ",1)
			if GPIO.input(9)==True:
				cost -= 10
				sleep(0.2)
				lcd.lcd_display_string("INSERT COINS    ",1)
			if cost <= 0:
				print "next ",cost
				next = True

		#state 4
		print queue , amountval
		print "State 3"
		next = False
		lcdclear(3)
		if cost < 0:
			cost = abs(cost)
			text = "RETURN COINS "+str(cost)
			lcd.lcd_display_string(text,1)
			sleep(2)
		params = urllib.urlencode({'cmd':1,'orderid': orderid, 'menu':list_menu[int(queue[0])], 'quantity': amountval[0],'custom':"-"})
		urllib.urlopen(server, params)
		lcdclear(3)
		lcd.lcd_display_string("DONE",1)
		textid = "ORDER ID "+str(orderid)
		lcd.lcd_display_string(textid,2)
		sleep(5)
		lcdclear(2)
		orderid+=1




if __name__ == "__main__":
	 main()


