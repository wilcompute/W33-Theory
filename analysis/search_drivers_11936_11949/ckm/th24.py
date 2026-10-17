import numpy as np
N=24
n=np.arange(-N,N+1); n1,n2=np.meshgrid(n,n,indexing='ij')
def theta(Om, z=(0,0)):
    Y=np.zeros((3,3),complex)
    for a in range(3):
        for b in range(3):
            v1,v2=n1+a/3,n2+b/3
            Q=Om[0,0]*v1*v1+2*Om[0,1]*v1*v2+Om[1,1]*v2*v2
            Y[a,b]=np.exp(3j*np.pi*Q+6j*np.pi*(v1*z[0]+v2*z[1])).sum()
    return Y
def left(Y):
    U,s,Vh=np.linalg.svd(Y); return U, s/s[0]
def ckm(Yu,Yd):
    Uu,su=left(Yu); Ud,sd=left(Yd); return np.abs(Uu.conj().T@Ud), su, sd
