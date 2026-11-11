import importlib.util,json,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('builder',Path(__file__).resolve().parents[1]/'scripts/build_catalog.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class CatalogTests(unittest.TestCase):
    def sample(self):
        dev={'manufacturer':'Sony','commercial_model':'KD-55XE9005','product':'BRAVIA_ATV2_EU','android_sdk':'28','firmware_revision':'672201'}
        return {'schema':3,'app':'TV Clean Manager','device':dev,'experiences':[{'id':'11111111-2222-3333-4444-555555555555','nickname':'aleraco','provenance':'manual_declared','device':dev,'verification':{'reboot':'user_attested','restore_on_hardware':'not_recorded'},'actions':[{'type':'disable_package','package':'com.sony.dtv.promos'}]}]}
    def parse(self,r):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'report.json';p.write_text(json.dumps(r),encoding='utf-8');return module.parse_report(p)
    def test_named_adb(self):
        e=self.parse(self.sample())[0]
        self.assertEqual(e['method'],'adb_manual')
        self.assertTrue(e['reboot_attested'])
        self.assertFalse(e['restore_attested'])
    def test_bad_model(self):
        r=self.sample();r['experiences'][0]['device']=dict(r['device'],commercial_model='KD-55XE9500')
        with self.assertRaises(ValueError):self.parse(r)
    def test_invalid_action(self):
        r=self.sample();r['experiences'][0]['actions'][0]['type']='arbitrary_command'
        with self.assertRaises(ValueError):self.parse(r)
    def test_no_auto_app_upgrade(self):
        r=self.sample();r['experiences'][0]['provenance']='external_tool_declared'
        self.assertEqual(self.parse(r)[0]['method'],'external_tool')
if __name__=='__main__':unittest.main()
