"""Render the certified two model responses; no physical unit calibration."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'w33_genus_six_execution.json').read_text())
    t,m,q=np.array(data['oscillator']['rows']).T
    fig,ax=plt.subplots(figsize=(9,4))
    ax.plot(t,m,label='Mechanical: x double-dot = -(3I-A)x')
    ax.plot(t,q,label='First order: i psi-dot = A psi',linestyle='--')
    ax.set(xlabel='Dimensionless time',ylabel='Return amplitude (real part)',title='Heawood middle-sector responses from the same initial vector')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout()
    fig.savefig(ROOT/'W33_GENUS_SIX_RESPONSE.svg',metadata={'Date':None})
    plt.close(fig)
if __name__=='__main__':main()
