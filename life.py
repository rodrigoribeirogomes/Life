import sys
import god
from Env import Env;
import time
import os
from traceback import format_tb;

e = Env(10,10);
c = e.addCell();
c = e.addCell();
c = e.addCell();
c = e.addCell(name = 'Air');
c = e.addCell(name = 'Venen');




while True:
	lives  = e.getCells(live = True);
	
	
	print(  god.PrintEnv(e) );
	
	for c in lives:
		print(c, 'Life:', c.life, 'Actions:', c.actions);
	
	time.sleep(1);
	
	if not lives:
		break;
		
	#print(' --- ');
	os.system('cls');
	
lives  = e.getCells(live = False);

for x in lives:
	print('Cells died. Ex: ', x.ex, 'life: ', x.life);