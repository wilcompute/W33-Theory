import sys,ast,json,glob,numpy as np
sys.path.insert(0,'.'); from th40 import theta
def normsv(Om,z):
    Y=theta(Om,z); z=np.asarray(z); f=np.exp(-3*np.pi*z.imag@np.linalg.inv(Om.imag)@z.imag)
    return np.linalg.svd(Y,compute_uv=False)*f
rows=[]
pol=json.load(open('hy2_polished.json'))
for lab,x in [('relaxed-'+str(s),np.array(v)) for s,v in zip((41,43,45,46),pol)]+[('pinned-'+f[3:5],np.array(ast.literal_eval(open(f).read().split(' x ')[1].strip()))) for f in sorted(glob.glob('hy_*.txt'))]:
    c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,z2=c; Om=np.array([[tau,ed],[ed,td]])
    sd=normsv(Om,(0,z2)); se=normsv(Om,(0,6*z2))
    print('%-11s td %s z_d %s : m_s/m_b %.4f m_d/m_s %.4f | m_mu/m_tau %.4f m_e/m_mu %.5f | y_b/y_tau %.3f' % (lab,np.round(td,4),np.round(z2,4),sd[1]/sd[0],sd[2]/sd[1],se[1]/se[0],se[2]/se[1],sd[0]/se[0]))
