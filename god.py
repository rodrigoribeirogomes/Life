import os
import sys
import BigBang
import Env


def PrintEnv(env):
	EnvMatrix = env.GetMatrix();
	Matrix = EnvMatrix.getSource();
	MatrixSize = env.GetEnvSize();
	FullMatrix = [];

	CurrentY = 0;
	for y in Matrix:
		FullMatrix += [''];
		for x in Matrix[CurrentY]:
			c = '';
			

			if x is None:
				c = '--- '
			elif hasattr(x, 'iscell'):
				if x.died:
					c = ' :X '
				else:
					c = str(x)[:3]+' '
			else:
				c = ('---' + str(x))[-3:] + ' '
				#c = '.   '
			
			FullMatrix[CurrentY] += c;
		
		CurrentY += 1;
			
	return '\n'.join(FullMatrix);
			
			

























		