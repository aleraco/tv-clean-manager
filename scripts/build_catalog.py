#!/usr/bin/env python3
"""Build a privacy-constrained public index from human-reviewed schema-3 reports.

Review is necessary: this tool rejects malformed input but does not prove identity,
independence or device safety. Publisher must review uploaded package inventories.
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,150}$")
ACTIONS = {'disable_package','enable_package','install_app','install_launcher','set_home_launcher','disable_stock_launcher','restore_stock_launcher','other'}
METHODS = {'manual_declared':'adb_manual', 'external_tool_declared':'external_tool'}

def clean(s,limit=150):
    if not isinstance(s,str) or not s or len(s)>limit or not PATTERN.fullmatch(s):
        raise ValueError(f'invalid field: {str(s)[:60]}')
    return s

def parse_report(path):
    if path.stat().st_size > 2_097_152: raise ValueError('report too large')
    data=json.loads(path.read_text(encoding='utf-8-sig'))
    if data.get('schema') != 3 or data.get('app') not in ('TV Clean Manager','BRAVIA Clean Installer'):
        raise ValueError('expected schema 3 report')
    dev=data['device']
    base={field:clean(str(dev[field]).lower() if field=='commercial_model' else str(dev[field])) for field in ('manufacturer','commercial_model','product','android_sdk','firmware_revision')}
    out=[]
    for exp in data.get('experiences',[]):
        ident=clean(exp['id'])
        author=clean(exp['nickname'])
        method=METHODS.get(exp['provenance'])
        if not method: raise ValueError('invalid provenance')
        edev=exp['device']
        if str(edev['product']) != base['product'] or str(edev['firmware_revision']) != base['firmware_revision'] or str(edev['android_sdk']) != base['android_sdk'] or str(edev['commercial_model']).lower() != base['commercial_model']:
            raise ValueError('experience device mismatch; correct model before submitting')
        ver=exp.get('verification',{})
        reboot=ver.get('reboot')=='user_attested'
        restore=ver.get('restore_on_hardware')=='user_attested'
        for action in exp['actions']:
            typ=action['type'];pkg=clean(action['package'])
            if typ not in ACTIONS: raise ValueError('invalid action')
            out.append(dict(**base,package=pkg,action=typ,author=author,method=method,experience_id=ident,reboot_attested=reboot,restore_attested=restore,evidence='self_reported'))
    # Automatic app operations are linked to a self-declared publisher. They never
    # contribute to the two independent ADB-person confirmation threshold.
    author=data.get('publisher')
    if author:
        author=clean(author,40)
        for op in data.get('operations',[]):
            if op.get('method') != 'app_executed': continue
            state=op.get('state')
            typ={'disabled':'disable_package','restored':'enable_package'}.get(state)
            if not typ: continue  # Do not publish pending/planned operations as successes.
            op_id=clean(op.get('operation_id',''))
            out.append(dict(**base,package=clean(op['package']),action=typ,author=author,method='app_executed',experience_id=op_id,reboot_attested=False,restore_attested=False,evidence='app_journal_reported_not_independently_verified'))
    return out

def build():
    entries=[];seen=set()
    for path in sorted((ROOT/'reports').glob('*.json')):
        for item in parse_report(path):
            key=(item['experience_id'],item['package'],item['action'])
            if key in seen: continue
            seen.add(key); entries.append(item)
    entries.sort(key=lambda e:(e['manufacturer'],e['product'],e['commercial_model'],e['firmware_revision'],e['package'],e['action'],e['author']))
    # Count unique claimed identities, not independent people. Source GitHub PR author
    # must be reviewed before considering any report a distinct independent contributor.
    groups=defaultdict(list)
    for e in entries:
        key=(e['product'],e['android_sdk'],e['commercial_model'],e['firmware_revision'],e['package'],e['action'])
        groups[key].append(e)
    summaries=[]
    for key,vals in sorted(groups.items()):
        adb_authors={e['author'].lower() for e in vals if e['method']=='adb_manual'}
        app_runs=sum(e['method']=='app_executed' for e in vals)
        summaries.append(dict(product=key[0],android_sdk=key[1],commercial_model=key[2],firmware_revision=key[3],package=key[4],action=key[5],adb_named_contributors=len(adb_authors),app_execution_reports=app_runs,community_candidate=(len(adb_authors)>=2),identity_and_independence_verified=False,warning='Claims only. No automatic unlock or safety guarantee.'))
    payload={'schema':1,'source':'curated community reports','entries':entries,'summaries':summaries,'warning':'Self-reports, not independent technical verification. Never use as a package allowlist.'}
    dest=ROOT/'site/catalog/index.json';dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Validated {len(entries)} actions, {len(summaries)} combinations')

if __name__=='__main__':
    try: build()
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print('INVALID REPORT:',exc,file=sys.stderr);sys.exit(1)
