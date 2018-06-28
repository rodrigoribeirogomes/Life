# This is cell
import threading;
import time
import random
import traceback;

STATS = {
	 'Food'		: 0
	,'predator'	: 0
	,'relationships': 0
	,'judge': 0
	,'love': 0
	,'borns': 0
	,'sex': 0
	,'LastSex': ""
}

MOVE_LOCK 	= threading.Lock();
STATS_LOCK	= threading.Lock();

def getStats():
	return STATS;
	
def setStats(name, value = None):
	with STATS_LOCK:
		if name not in STATS:
			STATS[name] = 0;
			
		if value is None:
			value = STATS[name] + 1;
			
		STATS[name] = value;

class Cell:

	def __init__(self, env, pos):
		self.env 	= env;
		self.pos	= pos;
		self.life 	= 10;
		self.actions = {};
		self.died	 = False;
		self.respiration = 0;
		self.logentries	 = []
		
		self.emotions = [];
		self.loadEmotions();
		
		self.ex = None;
		self.soul = threading.Thread(target = self.born);
		self.soul.setDaemon(True);
		
	
	def loadEmotions(self):
		for m in dir(self):
			if m.startswith('emotion_'):
				self.emotions += [{
						'dna'		: getattr(self, m)
						,'benefit'	: 1
						,'UseCount'	: 0
					}]
			
	def log(self, d):
		self.logentries += [d];
			
	def born(self):
		self.LifeCycle();
		
	def input(self):
		if self.respiration == 0:
			maxTries = self.life;
			
		else:
			maxTries = self.life % self.respiration + 1
	
		self.act('LastTries', maxTries);
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
		
		return self.life * 0.2;
		
	def emotion_predator( self, partner, factor = 1.1 ):
		AmountFood = int(self.produce(partner) * factor);
		partner.life -= AmountFood;
		
		AmountFood -= self.life;
		
		return AmountFood;
		
		
	def emotion_judge(self, partner, factor = 2):
		partnerContribution = partner.life/factor;
		meContribution = self.life/factor;
		
		newPartnerLife = partner.life - partnerContribution + meContribution;
		newMeLife = self.life - meContribution + partnerContribution;
		
		self.life = newMeLife;
		AmountFood = - meContribution + partnerContribution;
		
		return AmountFood;
		
	def emotion_love(self, partner, factor = 0.2):
		amountLife = int(self.life * factor);
		FoodAmount = -amountLife;
		
		if str(self) == str(partner):
			setStats('sex');
			setStats('LastSex', type(self).__name__);
			
			if int(self.life + partner.life) % 2  == 0:
				b = self.env.addCell( name = type(self).__name__ );
				FoodAmount = 1;

				if b:
					FoodAmount *= 2;
					setStats('borns');
				
		self.life -= amountLife;
		partner.life += amountLife;
		
		return FoodAmount;
		
	def getDigits(self, count = 1):
		t = [];
		
		rawDigitsLife =  str(self.life).replace('.','').replace('-','')
		
		for i in range(count):
			if not rawDigitsLife:
			r = random.choice(rawDigitsLife);
				= rawDigitsLife.replace(r, '');
			
			if not r:
				r = '0';
			
			t += [int(r)]
			
		return t;
		
		
		
	def move(self, x = None, y = None):
		with MOVE_LOCK:
			rd = self.getDigits(2);
			
			if rd[0] == rd[1]*2:
				self.log('can expand: '+str(rd));
				expand = True
			else:	
				expand = False;
			
			
			randomPos = self.env.randomPos(x,y, expand = expand);
			x = randomPos['x'];
			y = randomPos['y'];
			
			dest = self.env.get(x,y);
			
			if not dest is None:
				return;
				
			CurrentPos = self.pos;
			currx = self.pos['x'];
			curry = self.pos['y'];
			
			self.env.exclude( currx, curry);
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
						if issubclass(type(i), Cell):
							if i == self:
								self.act('SelfInput', True);
								food -= int(self.life * 0.1);
							else:
								STATS['relationships'] += 1;
								
								self.act('SelfInput', False);
								
								#Access emotion in benefit order...
								RankedEmotions = sorted(  self.emotions, key = lambda k: k['benefit'], reverse = True  );
								
								
								for e in RankedEmotions:
									if e['benefit'] <= 0:
										continue;
										
									emotionDNA	= e['dna'];	
									emotionName  = emotionDNA.__name__.replace('emotion_', '');
									
									produced 	= emotionDNA( i );
									
									if not produced is None:
										food += produced;
										
									if produced is None:
										benefit = 0;
									else:
										benefit = produced;
										
									e['benefit'] += benefit;
									e['UseCount'] += 1;
									self.act('LastEmotion',  '%s:%s' %( emotionDNA.__name__, e['benefit'] ) );
									setStats(emotionName);
										
						else:
							try:
								food += int(i);
							except:
								food += 0;

				
				food = food * 0.4;
				self.act('Food', food);
				self.life += food;
				
				if food > 0:
					faeces = max(1,int(food * 0.6));
				else:
					faeces = None;
				
				self.act('Feaces', faeces);		

				
				#Try output up die...
				while True and not faeces is None and self.life:
				
					r = self.output(faeces);
					
					if r:
						break;
						
					self.life -= faeces;
					
				
				
				
				self.respiration += 1;
				self.act('R', self.respiration);
				
				if food <= 0:
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


