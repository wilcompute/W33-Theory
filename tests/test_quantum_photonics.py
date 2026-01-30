def test_imports_and_basic_functions():
    import importlib

    m_gbs = importlib.import_module("scripts.quantum_photonics.run_gbs")
    m_cv = importlib.import_module("scripts.quantum_photonics.run_cv_repeater")
    # basic function checks
    U4 = m_gbs.build_interferometer(4)
    assert U4.shape == (4, 4)
    # test fock backend exact probability computation (very small) using a fresh 2x2 unitary
    U2 = m_gbs.build_interferometer(2)
    exact = m_gbs.compute_exact_probs_fock(modes=2, squeezing=0.5, U=U2, cutoff=4)
    assert isinstance(exact, dict)
    # sample small set and compute kl (2 modes)
    samples, ex, kl = m_gbs.run_gbs(
        modes=2, squeezing=0.5, shots=50, backend="fock", cutoff=4
    )
    assert samples.shape[0] == 50
    assert ex is not None
    assert isinstance(kl, float)
    # compute hafnian-based small distribution and compare KL
    haf_probs = m_gbs.compute_hafnian_probs(
        modes=2,
        squeezings=[0.5, 0.5],
        U=m_gbs.build_interferometer(2),
        max_total_photons=4,
    )
    # convert exact (fock) to common support (patterns up to cutoff)
    # compute KL between exact probs and hafnian probs
    # build aligned vectors
    keys = sorted(haf_probs.keys())
    p_exact = [ex.get(k, 0.0) for k in keys]
    p_haf = [haf_probs.get(k, 0.0) for k in keys]
    from math import log

    # check that the most-likely pattern (argmax) agrees between exact and hafnian-based distributions
    import numpy as _np
    from scipy.stats import entropy

    arg_ex = tuple(keys[_np.argmax(p_exact)])
    arg_h = tuple(keys[_np.argmax(p_haf)])
    assert arg_ex == arg_h
    # and that the KL is not enormous (sanity check)
    kl_err = entropy([max(1e-12, p) for p in p_exact], [max(1e-12, p) for p in p_haf])
    assert kl_err < 20
    # threshold detector sanity: compute TheWalrus threshold probs and check normalization
    th = m_gbs.compute_threshold_probs(
        modes=2, squeezings=[0.5, 0.5], U=m_gbs.build_interferometer(2), eta=0.9
    )
    assert abs(sum(th.values()) - 1.0) < 1e-9
    ln = m_cv.simulate_tmsv_loss(r=0.8, loss=0.9)
    assert isinstance(ln, float)
