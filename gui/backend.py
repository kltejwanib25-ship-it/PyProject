"""One integration boundary. Reference code is explicitly separate from team work."""
import importlib
import importlib.util
import os

mode = os.environ.get('COMMUNITYSCOPE_BACKEND', 'auto')
if mode not in {'auto', 'team', 'reference'}:
    raise ValueError('COMMUNITYSCOPE_BACKEND must be auto, team, or reference')
TEAM_MODE = mode == 'team' or (mode == 'auto' and importlib.util.find_spec('core') is not None)
PACKAGE = 'core' if TEAM_MODE else 'reference_backend'
MODE_LABEL = 'TEAM MODULES' if TEAM_MODE else 'REFERENCE DEMO'

def bind(module: str, name: str):
    """Fail clearly on incomplete team modules; never silently substitute results."""
    try:
        return getattr(importlib.import_module(f'{PACKAGE}.{module}'), name)
    except (ImportError, AttributeError) as exc:
        raise ImportError(f'Missing integration function: {PACKAGE}.{module}.{name}. See docs/FRIEND_HANDOFF.md. Original error: {exc}') from exc

load_csv = bind('data_loader','load_csv')
clean_data = bind('data_loader','clean_data')
sample_data = bind('data_loader','sample_data')
build_graph = bind('graph_builder','build_graph')
detect = bind('community_detection','detect')
ALGORITHMS = bind('community_detection','ALGORITHMS')
analyze = bind('network_analysis','analyze')
compare = bind('algorithm_comparison','compare')
export_reports = bind('report_generator','export_reports')
safe_csv = bind('report_generator','safe_csv')
