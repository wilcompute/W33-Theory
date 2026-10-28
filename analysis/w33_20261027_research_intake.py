"""Stream archival of the frozen481-commit intake and all210 PDF pages.

Archival/extraction is deliberately distinguished from model reading. GitKraken
is unavailable (transport closed); subprocess Git is the recorded fallback.
Archives are scratch duplicates of Git objects and are not publication artifacts.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
SCRATCH=ROOT/'.research_20261027_intake'
READ_PAGES=set(range(72,135))|{204}
READ_COMMIT_PREFIXES={'ccee9e84e','5bb5acd74','909913f17','a23c01282','47e5d1365','a15185e5c',
                      'c63b9ade1','887c9718e','6a26f6bed','d579880fe','752562e19',
                      'be700f9c7','da24b4f20','7acd13de0','7fb937f8a','31c150bc8',
                      '52515ea07','00cf043ac','78ae741e3'}
EXPECTED_PDF_SHA256='c5b44ee9e447561e4fbb892bb870d2506187e37e35c613a39eaf85af6cf6e19c'
FROZEN_PDF_GIT_REF='a03ff9dc04d4b43c684e83dab22121b46ff5b624:papers/forty_points/main.pdf'
LIVE_REVIEW_SHA256='c813e604f3cb2c8fc6f6417f85e7ed96a2eeb8faa191d7ccbc6b869d21e3f9a5'


def command(*args):
    return subprocess.check_output(args,cwd=ROOT)


def frozen_pdf():
    live=ROOT/'papers/forty_points/main.pdf'
    if hashlib.sha256(live.read_bytes()).hexdigest()==EXPECTED_PDF_SHA256:return live
    target=SCRATCH/'frozen_forty_points_main_a03ff9dc0.pdf'
    if not target.exists():
        raw=command('git','show',FROZEN_PDF_GIT_REF)
        assert hashlib.sha256(raw).hexdigest()==EXPECTED_PDF_SHA256
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==EXPECTED_PDF_SHA256
    return target


def archive_commit(sha):
    target=SCRATCH/'commits'/f'{sha}.patch.gz'
    target.parent.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256();size=0
    proc=subprocess.Popen(['git','show','--format=fuller','--diff-merges=separate','--no-ext-diff','--binary',sha],
                          cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    with gzip.open(target,'wb',compresslevel=5) as out:
        while block:=proc.stdout.read(1024*1024):
            digest.update(block);size+=len(block);out.write(block)
    error=proc.stderr.read().decode('utf-8',errors='replace')
    assert proc.wait()==0,error
    return {'sha':sha,'patch_sha256':digest.hexdigest(),'patch_bytes':size,
            'gzip_bytes':target.stat().st_size,'archive':str(target.relative_to(ROOT)),
            'full_patch_model_read':any(sha.startswith(p) for p in READ_COMMIT_PREFIXES)}


def certificate_references():
    files=command('rg','--files').decode('utf-8').splitlines()
    names={Path(x).name for x in files}
    references=[]
    for path in (ROOT/'papers/forty_points').glob('*.tex'):
        source=path.read_text(encoding='utf-8')
        for value in re.findall(r'\\cert\{([^}]*)\}',source,re.S):
            name=re.sub(r'\s+','',value.replace(r'\_','_'))
            candidates=[ROOT/folder/name for folder in ('','analysis','data','artifacts','scripts')]
            external=Path('C:/Repos/Holotrade/analysis')/name
            exists=Path(name).name in names or any(p.is_file() for p in candidates)
            record={'tex':str(path.relative_to(ROOT)),'reference':name,
                    'basename_exists':exists,'resolution':'local_file' if exists else 'unresolved'}
            if not exists and external.is_file():
                record.update(resolution='external_Holotrade_file',external_path=str(external))
            digest=name.removeprefix('Holotrade')
            if not exists and re.fullmatch('[a-f0-9]{7,40}',digest):
                for repository in (ROOT,Path('C:/Repos/Holotrade')):
                    probe=subprocess.run(['git','cat-file','-e',digest+'^{commit}'],cwd=repository,
                                         stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    if probe.returncode==0:
                        record.update(resolution='commit_object',commit_repository=str(repository));break
            references.append(record)
    return {'total':len(references),'unresolved':[r for r in references if r['resolution']=='unresolved'],
            'references':references,
            'scope':'Literal cert-macro basename existence only. This neither executes the witnesses nor validates their mathematics or correspondence to individual claims.'}


def run():
    subjects=(ROOT/'analysis/2026-10-27_week_commit_subjects.txt').read_text(encoding='utf-8').splitlines()
    all_sha=command('git','rev-list','origin/master').decode().splitlines()
    chosen=[]
    for subject in subjects:
        prefix=subject.split()[0]
        matches=[h for h in all_sha if h.startswith(prefix)]
        assert len(matches)==1,(prefix,matches)
        chosen.append(matches[0])
    assert len(set(chosen))==481
    with ThreadPoolExecutor(max_workers=2) as pool:
        commits=list(pool.map(archive_commit,chosen))
    pdf=frozen_pdf()
    pages=[]
    for number in range(1,211):
        raw=command('pdftotext','-f',str(number),'-l',str(number),'-layout',str(pdf),'-')
        target=SCRATCH/'pdf'/f'page{number:03}.txt'
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        pages.append({'page':number,'text_bytes':len(raw),'text_sha256':hashlib.sha256(raw).hexdigest(),
                      'archive':str(target.relative_to(ROOT)),
                      'full_text_model_read_this_continuation':number in READ_PAGES})
    return {'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
            'historical_week_commits':commits,
            'historical_week_fullpatch_bytes':sum(c['patch_bytes'] for c in commits),
            'pdf_pages':pages,
            'certificate_references':certificate_references(),
            'explicitly_model_read_additional_commits':[
                {'sha':'a0db8f2a2c279d48d198a8b5b13af6b79ed4cb27','scope':'entire patch and metadata; formula-index refresh only'}],
            'paper_read_findings':[
                'Pages72-76 distinguish a clock-selected Lorentzian Albert real form from a spacetime propagation law; neither chooses the loop kinetic normalization.',
                'Pages77-79 retract the proposed equivariant tick-to-clock bijection; use actual named maps rather than count matches.',
                'Pages80-85 distinguish untwisted family counts, full orbifold spectra, hypercharge normalization and conditional non-SUSY candidates; finite Qpsi-compatible hopping is not a validated heterotic vacuum.',
                'Pages86-90 give Albert/Peirce and spinor/parity structure; the charge dictionary used here is an already-owned result, not a new matter spectrum.'
            ],
            'completion':'All frozen patches and PDF pages archived with hashes. Full481-commit/210-page model reading remains incomplete. A read flag is not inferred from successful extraction.'}


if __name__=='__main__':
    out=ROOT/'analysis/2026-10-27_research_intake_coverage.json'
    if '--references-only' in sys.argv:
        d=json.loads(out.read_text());d['certificate_references']=certificate_references()
        assert d['pdf_sha256']==EXPECTED_PDF_SHA256
        for page in d['pdf_pages']:
            page['full_text_model_read_this_continuation']=page['page'] in READ_PAGES
        for commit in d['historical_week_commits']:
            commit['full_patch_model_read']=any(commit['sha'].startswith(p)for p in READ_COMMIT_PREFIXES)
        d['reading_increment_20261027_microscopic']={
            'pages_added':list(range(95,111)),
            'full_patches_added':['ccee9e84e','5bb5acd74','909913f17','a23c01282','47e5d1365','a15185e5c'],
            'patch_scope':'Five empty reservation commits plus the entire substantive a15185e5c patch, including code, JSON, TeX and PDF text conversion. This does not validate every inherited string claim.',
            'findings':'Pages95-110 document FI/parity, fractional-charge, Yukawa-degeneracy and vacuum-instability constraints. The native spatial reflection is distinct from the Delta54 family reflection. Full patch a15185e5c exposes the Pass12330 common-threshold scan; the new packet proves a continuous bound under exactly that running model.'}
        finding='Pages91-94 explicitly distinguish finite1+3+8 modules from gauge Lie algebras and prove a Pauli-stable E6 obstruction. Our U1/internal-index construction does not claim a nonabelian Pauli E6 action.'
        if finding not in d['paper_read_findings']:d['paper_read_findings'].append(finding)
    elif '--refresh-merges' in sys.argv:
        d=json.loads(out.read_text())
        merges={r.split()[0] for r in command('git','rev-list','--parents','origin/master').decode().splitlines() if len(r.split())>2}
        d['historical_week_commits']=[archive_commit(c['sha']) if c['sha'] in merges else c for c in d['historical_week_commits']]
        d['historical_week_fullpatch_bytes']=sum(c['patch_bytes']for c in d['historical_week_commits'])
        d['archive_diff_mode']='Separate full binary diff against every parent for merge commits; ordinary full diff for single-parent commits.'
    else:
        d=run()
    d.setdefault('reading_increment_20261027_microscopic',{
        'pages_added':list(range(95,111)),
        'full_patches_added':['ccee9e84e','5bb5acd74','909913f17','a23c01282','47e5d1365','a15185e5c'],
        'patch_scope':'Five empty reservation commits plus the entire substantive a15185e5c patch, including code, JSON, TeX and PDF text conversion. This does not validate every inherited string claim.',
        'findings':'The full a15185e5c patch led to the continuous Pass12330 bound in the microscopic-response packet.'})
    # Preserve content-specific review provenance on every generation path.
    d['reading_increment_20261027_operator']={
        'pages_added':list(range(111,119)),
        'full_patches_added':['c63b9ade1','887c9718e','6a26f6bed'],
        'findings':'Pages111-118 separate hosting chirality from selecting it, finite orientation/antiunitary character from a field-theory measure, and modulus-dependent vacuum/matter choices. This packet supplies Euclidean Weyl projectors but no dynamical handedness selection. Three full patches cover an honest earlier391-commit audit, a hosted12194-12198 receipt, and the faithful20-dimensional CSS action; none proves a TOE.'}
    d['reading_increment_20261027_gap']={
        'pages_added':list(range(119,127)),
        'full_patches_added':['d579880fe','752562e19','be700f9c7','da24b4f20','7acd13de0'],
        'findings':'Pages119-126 constrain flavour: local-SU5 up degeneracy, shared flux/Higgs CKM failures, stabilizer/Hesse locks, and supplied soft-supertrace escape parameters. Do not interpret the SU5 cubic intertwiner as a realistic flavour vacuum. Five full test-only patches distinguish exact finite Levi/Frobenius certificates, numerical Weil checks and failed Xi-identification; imported producers have not thereby been fully read.'}
    d['reading_increment_20261027_acoustic']={
        'pages_added':list(range(127,135))+[204],
        'full_patches_added':['7fb937f8a','31c150bc8','52515ea07','00cf043ac','78ae741e3'],
        'visual_pages_checked':[132],
        'findings':'Pages127-130 distinguish fitted flavour/Nelson-Barr existence from scalar-vacuum stability and retract the axiflavon interpretation. Page131 excludes numerical coincidences as evidence. Pages132-134 describe engineering/compiler/code results, not a derived field-theory vacuum; page132 figures were rendered and visually read. Five full patches cover a finite modular Jordan test, completed-Xi spectral falsifiers, analytic prime-tail bounds with uncertified quadrature, and finite signing samples. Imported complete producers were not thereby read. The finite-density tensor identity is scoped to the named27-site operator.'}
    live_hash=hashlib.sha256((ROOT/'papers/forty_points/main.pdf').read_bytes()).hexdigest()
    d['live_pdf_edition']={
        'current_sha256':live_hash,'matches_frozen_review':live_hash==EXPECTED_PDF_SHA256,
        'frozen_git_ref':FROZEN_PDF_GIT_REF,
        'live_full_text_pages_read':[86,204]if live_hash==LIVE_REVIEW_SHA256 else[],
        'scope':'Historical210-page flags refer only to the frozen c5b44ee9 edition. The70278ece1 live edition changed during this continuation; only its pages86 and204 and source diffs were read. No flags transfer to another edition by extraction alone.'}
    out.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'commits':len(d['historical_week_commits']),
                      'patch_bytes':d['historical_week_fullpatch_bytes'],
                      'pdf_pages':len(d['pdf_pages']),
                      'newly_read_pages':sum(p['full_text_model_read_this_continuation'] for p in d['pdf_pages'])}))
