"""Run on Windows. Team builds require all teammates' modules."""
import argparse
import importlib
import subprocess
import sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--team',action='store_true');args=parser.parse_args()
    if sys.platform!='win32':raise SystemExit('Build Windows executables on Windows.')
    package='core' if args.team else 'reference_backend'
    modules=['data_loader','graph_builder','community_detection','network_analysis','algorithm_comparison','report_generator']
    for module in modules:importlib.import_module(f'{package}.{module}')
    name='CommunityScope' if args.team else 'CommunityScope_ReferenceDemo'
    command=[sys.executable,'-m','PyInstaller','--noconfirm','--clean','--windowed','--name',name,
             '--add-data','assets;assets','--add-data','data;data','--collect-all','scipy']
    for module in modules:command+=['--hidden-import',f'{package}.{module}']
    command+=['main.py']
    subprocess.run(command,cwd=Path(__file__).resolve().parent,check=True)
    print(f'Distribute the entire dist/{name} folder.')
if __name__=='__main__':main()
