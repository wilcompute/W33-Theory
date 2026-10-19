exec(open('cpphase.py').read().split('# control')[0])
rng = np.random.default_rng(99)
rand = []
for t in range(36):
    a, b2 = rng.uniform(0, 2 * np.pi, 2)
    f = fit(lambda p, a=a, b2=b2: p[3] * np.array([1, np.exp(1j * a), np.exp(1j * b2)]), 4, starts=12, seed=500 + t)
    rand.append(np.linalg.norm(f.fun))
rand = np.sort(rand)
print('random fixed phases: best', rand[:5].round(4), ' median', np.median(rand).round(4))
f = fit(lambda p: p[3] * np.array([1, 1, np.exp(5j * np.pi / 3)]), 4, starts=40, seed=7)
print('quantised (0,5) refit 40 starts:', np.linalg.norm(f.fun).round(4), ' residual vector', np.round(f.fun, 4))
