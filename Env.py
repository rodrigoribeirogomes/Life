# This is env!
import random
import cell
from operator import xor
import traceback
import threading;

def expandList(l, newSize, default = None):
	current = len(l);
	AmountNew = newSize - current  + 1;
	if AmountNew > 0:
		News = [default] * AmountNew;
		l.extend(News);
		
def getListPos(l, pos):
	if l is None or pos is None:
		return None;

	if len(l) <= pos:
		return None;
		
	return l[pos];
	
	

class Matrix:

	def __init__(self):
		self.__matrix = [] * 0;
		self.__size = {'x':0, 'y':0};
		self.TransformLock = threading.Lock();
		
	#Get a random position on env...
	def randomPos(self, x = None, y = None):
	
		if x is None:
			x = random.randint(0,  self.__size['x'] )
			
		if y is None:
			y = random.randint(0,  self.__size['y'] )
			
		if x > self.__size['x']:
			self.__size['x'] = x;
			
		if y > self.__size['y']:
			self.__size['y'] = y;
		
		return {
			'x':x ,'y':y
		}
		
	#Nothing creates, nothing destroyes, all transforms!
	def  transform(self, x = None, y = None, e = None, **options):
		randomPos = self.randomPos(x, y);
		x = randomPos['x']
		y = randomPos['y']
	
		if y < 0 or x < 0:
			return;

		#Expands if need..
		expandList(self.__matrix, self.__size['y']);
		
		#Expands all slots!
		for i in range(len(self.__matrix)):
			YSlot = self.__matrix[i];
			
			if YSlot is None:
				YSlot = [];
				self.__matrix[i] = YSlot;
			
			expandList(YSlot, self.__size['x'], default = options.get('default'));
			
		#Get the specified slot!
		YSlot = self.__matrix[y];
		YSlot[x] = e;
	
		
		return {'x':x,'y':y,'e':e};

			
		
	def get(self, x,y):
		YSlot = getListPos(self.__matrix, y);
		return getListPos(YSlot, x);
		
	def getSource(self):
		return self.__matrix;
		
	def getSize(self):
		return self.__size;
			

class Env:

	def __init__(self, x = 0, y = 0, e = None):
		self.__env = Matrix();
		self.__env.transform(x, y, e,default = e);
		self.cells = [];
		self.GetLock = threading.Lock();
		self.TransformLock = threading.Lock();
		
	def exclude(self, x, y):
		x = self.__env.transform(x,y, None);

		
	def randomPos(self, x, y):
		return self.__env.randomPos(x,y);
		
	def transform(self, x = None, y = None, e = None, force = False):
		with self.TransformLock:
			pos = self.__env.randomPos(x,y);
			c = self.__env.get(pos['x'],pos['y']);
			
			if isinstance(c, cell.Cell) and not force:
				return None;
			
			return self.__env.transform(pos['x'],pos['y'],e);

		
	def GetMatrix(self):
		return self.__env;
		
	def GetEnvSize(self):
		return self.__env.getSize();
		
		
	#Get some particle from env!
	#Env will empty the place
	def get(self, x, y):
		with self.GetLock:
			p = self.__env.get(x, y);
			self.transform(x, y, None);
			
		return p;
		
	#Insert some particle in env!
	def put(self,p, **options):
	
		if options.get('x'):
			x = options.get('x')
			
		if options.get('y'):
			y = options.get('y');
			
		size = self.GetEnvSize();
		
		if x is None:
			x = random.choice()
	
		return self.transform(x, y, p);
	
	
	def addCell(self,x = None, y = None, name = 'Cell'):
		bornPos = self.transform( e = None, x = x, y  = y );
		
		if not bornPos:
			return None;
		
		CellClass = getattr(cell, name, None);
		
		if not CellClass:
			raise ValueError('INVALID_CELL: ', name);
			
		if not issubclass(CellClass, cell.Cell):
			raise ValueError('ISNOT_A_CELL: ', name);
			

		NewCell = CellClass(self, bornPos);
		NewPos = self.transform(  bornPos['x'], bornPos['y'], NewCell  );
		
		if NewPos:
			NewCell.pos = NewPos;
			self.cells += [NewCell];
			NewCell.soul.start();
			return NewCell;
		else:
			return None;
		
		

		
	def getCells(self, **options):
		live = options.get('live');
	
		cells = [];
		for c in self.cells:
			if live is None or c.soul.is_alive() == live:
				cells += [c];
				
		return cells;
		
	
		
	#Get in some direction!
	def getNext(self, x, y, count = 1, maxTries = -1):
		got = [];
		tryCount 	= 0;
		directions	= [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
		round		= 0;
		
		CurrentDirections = [];
		
		while True:
		
			Size = self.GetEnvSize();
			Total = Size['x'] * Size['y'];
			
			if maxTries == -1:
				maxTries = Total;
			
			#Have directions in current round?
			if not CurrentDirections:
				round += 1;
				CurrentDirections = directions.copy();
				
			#Choose next direction!
			NextDirection = random.choice(CurrentDirections);
			#Removes!
			CurrentDirections.remove(NextDirection);
						
			xNext = NextDirection[0] * round;
			yNext = NextDirection[1] * round;
			
			CurrentX = x + xNext;
			CurrentY = y + yNext;
			
			if tryCount > Total or tryCount >= maxTries:
				break;
			
			if CurrentX < 0:
				CurrentX = 0;
				
			if CurrentX > Size['x']:
				CurrentX = Size['x'];
			
			if CurrentY < 0:
				CurrentY = 0;
				
			if CurrentY > Size['y']:
				CurrentY = Size['y'];
				
			
			if CurrentX != x or CurrentY != y:	
				#print('Try get from x:%s y:%s count:%s try:%s count:%s' %(CurrentX,CurrentY,count, tryCount, Total))
				p = self.get(CurrentX,CurrentY);
			else:
				p = None;
				
			tryCount += 1;
			
			
			if not p is None:
				count -= 1;
				got += [p];
				
			if count == 0:
				break;
				
			
			
		return got;

		


		
	