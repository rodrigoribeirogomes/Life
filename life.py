import sys
import god
from Env import Env;
import time
import os
from traceback import format_tb;
import cell

print('Creating env...');
e = Env(5,5);

print('Creating first cells...');
c = e.addCell(0,0);
c = e.addCell(0,1);


#c = e.addCell(name = 'Venen');


def PrintCell(c):
	return;
	print( c, 'Life:',  c.life, 'Actions:', c.actions, 'p:', c.pos['x'],c.pos['y']);
	
	ems = []
	for e in c.emotions:
		n = e['dna'].__name__;
		ems += [  '%s = b:%s c:%s' % (n, e['benefit'], e['UseCount'])  ];
		
	print( '	Emotions:', ' '.join(ems) );
	pass
	
def PrintStats():
	s  = cell.getStats();
	print( 'Stats:',s );

print('Starting loop');
while True:
	lives  = e.getCells(live = True);
	dieds  = e.getCells(live = False);
	
	print(  god.PrintEnv(e) );
	
	PrintStats();
	
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