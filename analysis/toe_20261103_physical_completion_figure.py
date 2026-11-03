"""Export the declared-model constraints as a standalone scientific figure."""
import json,pathlib,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    radio=json.loads((ROOT/'data/toe_20261103_dark_radiative_stability.json').read_text())
    p=next(r for r in radio['rows']if r['dataset']=='dovekie'and r['branch']=='free_c_neg')
    cap=p['MS_no_curvature_cancellation_DM_mass_cap_eV'];mass=np.geomspace(1e-4,1e10,400)
    fig,axes=plt.subplots(1,3,figsize=(15,4.6),layout='constrained')
    ax=axes[0];ax.loglog(mass,(mass/cap)**4,label='Unprotected Dirac mass',color='#b14c32')
    delta=1e-13;ax.loglog(mass,mass**2*delta**2/cap**4,label='Paired spectrum; soft parameter $10^{-13}$ eV',color='#2b6f9c')
    ax.axhline(1,color='black',lw=1,ls=':');ax.axvline(cap,color='#b14c32',lw=1,ls='--')
    ax.set(xlabel='Dark-particle mass (eV)',ylabel=r'$|\Delta m_\phi^2|/H_0^2$',title='Radiative benchmark; counterterms matter')
    ax.set_ylim(1e-28,1e49);ax.legend(fontsize=8,loc='upper left');ax.grid(alpha=.15,which='major')
    ax.text(.02,.03,'Naturalness prescription; not an observational exclusion',transform=ax.transAxes,fontsize=8)
    ax=axes[1];t=np.linspace(0,np.pi/2,400)
    for ratio,color in [(0,'#2b6f9c'),(.5,'#b14c32'),(1,'#555555')]:
        n=np.maximum(0,np.exp(-2*ratio*t)/2*(abs(np.sin(2*t))-np.sinh(2*ratio*t)))
        ax.plot(t,n,label=rf'$\Gamma/|J|={ratio:g}$',color=color)
    ax.set(xlabel=r'$|J|t$',ylabel='Two-qubit negativity',title='A specified gravity-channel test',ylim=(-.015,.52));ax.legend(fontsize=9);ax.grid(alpha=.15)
    ax.text(.02,.03,'Static phase alone does not identify mediator spin',transform=ax.transAxes,fontsize=8)
    ax=axes[2];a=np.linspace(1,4,300);ax.plot(a*a,5/a,color='#2b6f9c')
    ax.axhline(2,color='black',ls=':');ax.axvline(25/4,color='#555555',ls='--');ax.scatter([9],[5/3],color='#b14c32',zorder=5)
    ax.annotate(r'$\Delta=5/3$',xy=(9,5/3),xytext=(10.2,2.4),arrowprops={'arrowstyle':'->'},fontsize=10)
    ax.set(xlabel='Generalized velocity condition number',ylabel='Mirror interaction scaling dimension',title='Local chiral benchmark in 1+1D',ylim=(1,5.3));ax.grid(alpha=.15)
    ax.text(.02,.03,'Both interactions relevant below dimension 2',transform=ax.transAxes,fontsize=8)
    target=ROOT/'artifacts';target.mkdir(exist_ok=True)
    for suffix in ['png','svg']:fig.savefig(target/f'toe_20261103_physical_completion.{suffix}',dpi=180)
    svg=target/'toe_20261103_physical_completion.svg'
    svg.write_text('\n'.join(line.rstrip()for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig);print('EXPORTED_PHYSICAL_COMPLETION_PNG_SVG',flush=True)

if __name__=='__main__':main()
