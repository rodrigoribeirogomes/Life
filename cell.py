# This is cell
import threading;
import time
import random
import traceback;
import re
import multiprocessing;

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

NODIGITS_REGEX = re.compile('[^0-9]');
LIFE_SEMAPHORE = threading.Semaphore( multiprocessing.cpu_count() );

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
						,'benefit'	: 1.0
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
		
		return self.life * self.getSeed();
		
	def emotion_predator( self, partner):
		AmountFood = partner.getSeed();
		partner.life -= AmountFood;
		
		AmountFood = self.life + AmountFood - partner.life;
		
		return AmountFood;
		
		
	def emotion_judge(self, partner):
		partnerContribution = partner.getSeed();
		meContribution = self.getSeed();
		
		newPartnerLife = partner.life - partnerContribution + meContribution;
		newMeLife = self.life - meContribution + partnerContribution;
		
		self.life = newMeLife;
		AmountFood = - meContribution + partnerContribution;
		
		return AmountFood;
		
	def emotion_love(self, partner):
		amountLife = self.getSeed();
		FoodAmount = -amountLife;
		
		if str(self) == str(partner):
			setStats('sex');
			setStats('LastSex', type(self).__name__);
			
			if int(self.life) * self.getSeed() == partner.life * partner.getSeed():
				b = self.env.addCell( name = type(self).__name__ );
				FoodAmount = self.getSeed();

				if b:
					FoodAmount += self.getSeed();
					setStats('borns');
				
		self.life -= amountLife;
		partner.life += amountLife;
		
		return FoodAmount;
		
	def getDigits(self, count = 1):
		t = [];
		
		rawDigitsLife =  NODIGITS_REGEX.sub(  str(self.life), '' );
		
		if not rawDigitsLife:
			rawDigitsLife = ['0'];
		
		if count == 0:
			count = len(rawDigitsLife);
		
		for i in range(count):				
			r = random.choice(rawDigitsLife);
			
			t += [int(r)]
			
		return t;
		
	def getSeed(self):
		allDigits 	= self.getDigits(0);
		digitCount	= len(allDigits);
		firstDigit	= allDigits[0];
		return min(firstDigit,digitCount)/digitCount;
		
		
	def move(self, x = None, y = None):
		with MOVE_LOCK:
			rd = self.getDigits(0);
			
			expand = True;
			for i in rd:
				if i != rd[0]:
					expand = False;
					break;
			
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
				with LIFE_SEMAPHORE:
					if self.life <= 0:
						raise ValueError('DIED');
						
					TheInput = self.input();
					self.act('Inputing', TheInput);
					food = 0;
					seed = self.getSeed();
					
					if not TheInput:
						food = -1;
					else:
						for i in TheInput:
							if issubclass(type(i), Cell):
								if i == self:
									self.act('SelfInput', True);
									food -= int(self.life * seed);
								else:
									setStats('relationships');
									
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

					
					foodSeed 	= self.getSeed();
					food = food * foodSeed;
					self.act('Food', food);
					self.life += food;
					
					if food > 0:
						faeces = max(1,int(food *  (1 - foodSeed) ));
					else:
						faeces = None;
					
					self.act('Feaces', faeces);		

					#Try output up die...
					while True and not faeces is None and self.life:
						r = self.output(faeces);
						if r:
							break;
						self.life -= 1;
					
					
					self.respiration += int(self.getSeed() * 10);
					self.act('R', self.respiration);
					
					if food <= 0:
						self.move();
				
				time.sleep(0);
				
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


