import os
import runpy

os.environ['TOMOTOPE_FOLLOWUP_SHOTS'] = os.environ.get('TOMOTOPE_FOLLOWUP_SHOTS','2000')
os.environ['TOMOTOPE_FOLLOWUP_BOOTSTRAP'] = os.environ.get('TOMOTOPE_FOLLOWUP_BOOTSTRAP','500')
os.environ['TOMOTOPE_FOLLOWUP_MODES'] = os.environ.get('TOMOTOPE_FOLLOWUP_MODES','8')
os.environ['TOMOTOPE_FOLLOWUP_KIND'] = os.environ.get('TOMOTOPE_FOLLOWUP_KIND','structured')

runpy.run_path(str(__file__).replace('_wrapper',''))
