# This is cell
import threading;
import time
import random
import traceback;


class Cell:

	def __init__(self, env, pos):
		self.env 	= env;
		self.pos	= pos;
		self.life 	= 10;
		self.actions = {};
		self.died	 = False;
		self.respiration = 0;
		
		self.ex = None;
		self.soul = threading.Thread(target = self.born);
		self.soul.setDaemon(True);
		self.soul.start();
		
	
	def born(self):
		self.LifeCycle();
		
	def input(self):
		if self.respiration == 0:
			maxTries = self.life;
			
		else:
			maxTries = self.life % self.respiration + 1
	
		i = self.env.getNext( self.pos['x'], self.pos['y'], 1, maxTries = maxTries );
		return i;
		
	def output(self, s):
		return self.env.transform( e = s );
		
	def __int__(self):
		return self.life;
		
		
	def __str__(self):
		return 'CELL';
		
	def __repr__(self):
		return str(self);
		
	def iscell(self):
		return True;
		
	def act(self, a, v):
		self.actions[a] = v
		
		
	def produce(self, predator):
		
		if type(predator) == Cell:
			self.env.addCell(name = 'Air');
	
		return self.life * 0.2;
		
	def move(self, x = None, y = None):
	
		randomPos = self.env.randomPos(x,y);
		x = randomPos['x'];
		y = randomPos['y'];
		
		dest = self.env.get(x,y);
		
		if not dest is None:
			return;
			
		CurrentPos = self.pos;
		currx = self.pos['x'];
		curry = self.pos['y'];
		
		self.env.transform( currx, curry, None,  force = True  );
		NewPos = self.env.transform( x, y, self  );
		
		if NewPos:
			self.pos = NewPos;
	
	
	def __die(self):
		CurrentPos = self.pos;
		currx = self.pos['x'];
		curry = self.pos['y'];
		self.env.transform( currx, curry, None, force = True );
		self.died = True;
		
		
	def LifeCycle(self):
		try: 
			while True:
			
				if self.life <= 0:
					raise ValueError('DIED');
					
				TheInput = self.input();
				self.act('Inputing', TheInput);
				food = 0;
				
				if not TheInput:
					food = -1 * max(1, int(self.life * 0.1 ));
				else:
					for i in TheInput:
						try:
							if issubclass(type(i), Cell):
								if i == self:
									self.act('SelfInput', True);
									food -= int(self.life * 0.1);
								else:
									self.act('SelfInput', False);
									total = int(i.produce(self));
									
									food += int(total * 1.1);
									i.life -= total;
							else:
								food += int(i);
						except:
							food += 0;
				
				food = int(food);
				self.act('Food', food);
				self.life += food;
				
				if food > 0:
					faeces = max(1,int(food * 0.4));
				else:
					faeces = None;
				
				self.act('Feaces', faeces);					
				self.output( faeces  );
				
				self.respiration += 1;
				self.act('R', self.respiration);
				
				if self.respiration % 10 == 0 and food <= 0:
					self.move();
				
				time.sleep(0.1);
				
		except BaseException as e:
			self.ex = traceback.format_exc();
			self.__die();
			return;
			
			

class Air(Cell):
	
	def __str__(self):
		return 'AIR';
		
	def produce(self, predator):
		return self.life * 2;
		
		
class Venen(Cell):

	def __str__(self):
		return 'VEN';
		
	def produce(self, predator):
		self.life  -= int(self.life/2);
		
		if  type(predator) == Air:
			self.env.addCell( name = type(self).__name__ );
			self.life = 1;
			
		if type(predator) == type(self):
			self.env.addCell( name = type(self).__name__ );
			self.env.addCell( name = type(self).__name__ );
			self.life = 100;
		
		return -1 * predator.life/2;


