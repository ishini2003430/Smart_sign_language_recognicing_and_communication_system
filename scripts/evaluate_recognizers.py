"""Read previously saved evaluation without reusing test set for tuning.

Models are evaluated at training time; this script reports the stored values.
"""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',choices=['pilot','three_signer'],default='pilot')
    opts=p.parse_args()
    root=ROOT/'outputs'/'recognition'/opts.mode
    file=root/'comparison.json'
    if not file.exists():raise FileNotFoundError(f'{file}; train models first')
    print('MODEL             ACC       MACRO-F1    TOP-K      N_TEST')
    for report in json.loads(file.read_text(encoding='utf-8')):
        print(f"{report['model']:<17} {report['accuracy']:<9.3f} {report['macro_f1']:<11.3f} {report['top_k_recall']:<10.3f} {report['n_test']}")
    if opts.mode=='pilot':
        print('\nDo NOT choose the final best model from this pilot: only two signers and one training example/class.')
    else:
        print('\nPreliminary performance only. Full post-context accuracy requires separate expert-verified sequences.')

if __name__=='__main__':main()
