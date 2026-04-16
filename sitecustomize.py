import sys
import importlib
import importlib.util
import importlib.abc


class PillarsAliasLoader(importlib.abc.Loader):
    def __init__(self, fullname, underlying_name):
        self.fullname = fullname
        self.underlying = underlying_name

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        m = importlib.import_module(self.underlying)
        for k, v in m.__dict__.items():
            if k.startswith('__'):
                # keep some dunder metadata
                if k in ('__doc__', '__file__', '__package__', '__name__'):
                    module.__dict__[k] = v
                continue
            module.__dict__[k] = v


class PillarsAliasFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if not fullname.startswith('THEORY_PART_'):
            return None
        underlying = 'pillars.' + fullname
        try:
            spec = importlib.util.find_spec(underlying)
        except Exception:
            spec = None
        if spec is None:
            return None
        loader = PillarsAliasLoader(fullname, underlying)
        return importlib.util.spec_from_loader(fullname, loader, origin=spec.origin)


try:
    # Insert at front so this mapping wins before other finders
    sys.meta_path.insert(0, PillarsAliasFinder())
except Exception:
    pass
