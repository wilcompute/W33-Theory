import importlib.util
import os

print('spec pillars =', importlib.util.find_spec('pillars'))
print('spec underlying =', importlib.util.find_spec('pillars.THEORY_PART_CCLXXIX_AMPLITUHEDRON_POSITIVE_GEOMETRY'))
print('pillars files count =', len([f for f in os.listdir('pillars') if f.endswith('.py')]))
print('sample exists =', os.path.exists('pillars/THEORY_PART_CCLXXIX_AMPLITUHEDRON_POSITIVE_GEOMETRY.py'))
