# This is cell
import threading;
import time

class Cell:

	def __init__(self, env):
		self.env 	= env;
		self.pos	= self.env.transform( e = self );
		self.life 	= 1; 
		
		worker 		= threading.Thread(target = self.born);
		worker.setDaemon(True);
		worker.start();
	
	def born(self):
		self.LifeCycle();
		
	def input(self):
		return self.env.getNext( self.pos['x'], self.pos['y'], 1 );
		
	def output(self):
		return self.env.transform( e = random.randint() );
		
	def __int__(self):
		return self.life;
		
	def __str__(self):
		return 'C';
		
	def LifeCycle(self):
	
		while True:
		
			if not self.Life:
				print('Died...');
				return;
		
			self.life = int(self.input())/self.life;
			self.output();
			time.sleep(1);
			
			
			

