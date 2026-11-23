"""Minimal reverse-mode autodiff on numpy arrays (Claude track, Pass 12718): enough for small transformers.
Ops: matmul (batched), add/sub/mul (broadcast), relu, softmax (last axis), layernorm (last axis), transpose of the last two axes,
take the last position, cross-entropy with integer labels, straight-through quantised views."""
import numpy as np


def unbroadcast(g, shape):
    while g.ndim > len(shape): g = g.sum(0)
    for i, s in enumerate(shape):
        if s == 1 and g.shape[i] != 1: g = g.sum(i, keepdims=True)
    return g


class T:
    def __init__(s, val, parents=(), back=None):
        s.val = np.asarray(val, float); s.grad = np.zeros_like(s.val); s.parents = parents; s.back = back

    def __add__(s, o):
        o = o if isinstance(o, T) else T(o)
        r = T(s.val + o.val, (s, o))
        def b(): s.grad += unbroadcast(r.grad, s.val.shape); o.grad += unbroadcast(r.grad, o.val.shape)
        r.back = b; return r

    def __mul__(s, c):
        if isinstance(c, T):
            r = T(s.val * c.val, (s, c))
            def b(): s.grad += unbroadcast(r.grad * c.val, s.val.shape); c.grad += unbroadcast(r.grad * s.val, c.val.shape)
        else:
            r = T(s.val * c, (s,))
            def b(): s.grad += r.grad * c
        r.back = b; return r

    def __matmul__(s, o):
        r = T(s.val @ o.val, (s, o))
        def b():
            s.grad += unbroadcast(r.grad @ np.swapaxes(o.val, -1, -2), s.val.shape)
            o.grad += unbroadcast(np.swapaxes(s.val, -1, -2) @ r.grad, o.val.shape)
        r.back = b; return r

    def tr(s):
        r = T(np.swapaxes(s.val, -1, -2), (s,))
        def b(): s.grad += np.swapaxes(r.grad, -1, -2)
        r.back = b; return r

    def relu(s):
        r = T(np.maximum(s.val, 0), (s,))
        def b(): s.grad += r.grad * (s.val > 0)
        r.back = b; return r

    def softmax(s):
        z = s.val - s.val.max(-1, keepdims=True); e = np.exp(z); p = e / e.sum(-1, keepdims=True)
        r = T(p, (s,))
        def b(): s.grad += p * (r.grad - (r.grad * p).sum(-1, keepdims=True))
        r.back = b; return r

    def layernorm(s, eps=1e-5):
        mu = s.val.mean(-1, keepdims=True); xc = s.val - mu; var = (xc ** 2).mean(-1, keepdims=True); inv = 1 / np.sqrt(var + eps)
        y = xc * inv; r = T(y, (s,))
        def b():
            g = r.grad; n = s.val.shape[-1]
            s.grad += inv * (g - g.mean(-1, keepdims=True) - y * (g * y).mean(-1, keepdims=True))
        r.back = b; return r

    def last(s):
        r = T(s.val[:, -1, :], (s,))
        def b(): s.grad[:, -1, :] += r.grad
        r.back = b; return r

    def backward(s):
        order, seen = [], set()
        def visit(v):
            if id(v) in seen: return
            seen.add(id(v))
            for p in v.parents: visit(p)
            order.append(v)
        visit(s); s.grad = np.ones_like(s.val)
        for v in reversed(order):
            if v.back: v.back()


def cross_entropy(logits, y):
    z = logits.val - logits.val.max(-1, keepdims=True); p = np.exp(z); p /= p.sum(-1, keepdims=True)
    n = len(y); loss = -np.mean(np.log(p[np.arange(n), y] + 1e-12))
    r = T(loss, (logits,))
    def b():
        g = p.copy(); g[np.arange(n), y] -= 1; logits.grad += g / n * r.grad
    r.back = b; return r


def ste(W, qfun):
    """straight-through quantised view of parameter W."""
    r = T(qfun(W.val), (W,))
    def b(): W.grad += r.grad
    r.back = b; return r
