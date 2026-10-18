"""Run with: python -m unittest discover -s tests -v"""
import json, tempfile, unittest
from pathlib import Path
import numpy as np
from src.recognition.preprocessing import npz_features
from src.recognition.top_k import candidates

class TestFeatures(unittest.TestCase):
    def test_npz_shape_missing_and_location(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.npz'
            c=np.full((5,2,21,3),np.nan,dtype='float32')
            c[2:4,0,:,:]=0.0
            c[2:4,0,:,0]=0.8
            mask=np.zeros((5,2),bool);mask[2:4,0]=True
            np.savez_compressed(p,coordinates=c,detected=mask,slot_order=np.array(['Left','Right']))
            out=npz_features(p,48)
            self.assertEqual(out.shape,(48,134))
            self.assertTrue(np.isfinite(out).all())
            self.assertEqual(out[0,-2],0.0)
            self.assertTrue((out[:,-2] > 0).any())
            # Left-hand x wrist coordinate preserved, important for sign location.
            self.assertTrue(np.max(out[:,126]) >= 0.8-1e-6)
    def test_top3_ranking(self):
        labels=[{'sign_id':'S01','gloss':'amma'},{'sign_id':'S02','gloss':'father'},{'sign_id':'S03','gloss':'go'}]
        out=candidates([0.2,0.7,0.1],labels)
        self.assertEqual(out[0]['sign_id'],'S02')
        self.assertEqual(out[0]['rank'],1)
        self.assertAlmostEqual(out[0]['score'],0.7)

if __name__=='__main__':unittest.main()
