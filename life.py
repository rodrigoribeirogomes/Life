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
#c = e.addCell(name = 'Venen');


def PrintCell(c):
	pass;
	#print( c, 'Life:',  c.life, 'Actions:', c.actions, 'p:', c.pos['x'],c.pos['y'] );



while True:
	lives  = e.getCells(live = True);
	dieds  = e.getCells(live = False);
	
	print(  god.PrintEnv(e) );
	
	print('lives:', len(lives))
	for c in lives:
		PrintCell(c);
	
	print('dieds:', len(dieds));
	for d in dieds:
		PrintCell(d);
	
	
	time.sleep(1);
	
	if not lives:
		break;
		
	#print(' --- ');
	os.system('cls');
	
lives  = e.getCells(live = False);

for x in lives:
	print('Cells died. Ex: ', x.ex, 'life: ', x.life);