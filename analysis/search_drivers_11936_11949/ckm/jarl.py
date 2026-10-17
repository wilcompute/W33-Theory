import sys,re,ast; sys.path.insert(0,'.'); from th24 import *
import numpy as np, mpmath as mp
eta=lambda t: complex(mp.exp(2j*mp.pi*t/24)*mp.qp(mp.exp(2j*mp.pi*t)))
weber=lambda t: np.exp(-1j*np.pi/24)*eta((t+1)/2)/eta(t)
for f in sorted(__import__('glob').glob('fite_*.txt')):
    s=open(f).read(); x=np.array(ast.literal_eval(s[s.index(' x ')+3:].strip()))
    c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,w,z1,z2=c
    Yu=theta(np.array([[tau,eu],[eu,tau]]),(w,w)); Yd=theta(np.array([[tau,ed],[ed,td]]),(z1,z2))
    Uu,su,_=np.linalg.svd(Yu); Ud,sd,_=np.linalg.svd(Yd); V=Uu.conj().T@Ud
    # rows (t,c,u), cols (b,s,d) -> standard order (u,c,t)x(d,s,b)
    V=V[::-1,::-1]
    J=np.imag(V[0,0]*V[1,1]*np.conj(V[0,1])*np.conj(V[1,0]))
    cost=float(re.search(r'cost (\S+)',s).group(1))
    print(f, 'cost %.1e' % cost, 'J %.3e' % J, '|f(tau)|^8 %.3f' % abs(weber(tau))**8, 'tau', np.round(tau,3), 'td', np.round(td,3), '-1/td', np.round(-1/td,2), '|eu| %.4f |ed| %.4f |w| %.3f |z1| %.3f |z2| %.3f' % (abs(eu),abs(ed),abs(w),abs(z1),abs(z2)))
