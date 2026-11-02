# Exact integration contract
All three friends implement modules inside `core/`, with an empty `core/__init__.py`. Node IDs must be strings. Do not import GUI modules from core. Functions run in a worker and must not manipulate widgets.

## Friend 1 — data and graph
`core/data_loader.py`:
- load_csv(path, directed=False, weighted=True) -> (DataFrame, note_string)
- clean_data(frame, directed=False, weighted=True) -> (DataFrame, note_string)
- sample_data(seed=42, size=120) -> raw DataFrame
Clean DataFrame columns, in order: source, target, weight. Names nonempty strings; finite positive float weights. Invalid input raises ValueError. Duplicate/reversed undirected weights sum; unweighted links become 1. Self-rows declare users but do not create self-loops. Impose documented size limits.

`core/graph_builder.py`:
- build_graph(frame, directed=False) -> nx.Graph or nx.DiGraph
- community_graph(graph) -> undirected graph (used by other friends)
Edge attributes: weight=strength, distance=1/strength. Preserve isolates. Reciprocal directed strengths sum in the community projection.

## Friend 2 — detection
`core/community_detection.py`:
- ALGORITHMS: list of algorithm display strings.
- detect(graph, algorithm='Louvain') -> dict
Required keys: algorithm (str), communities (list of lists of string IDs), mapping (dict user -> integer community ID starting at 1), modularity (float), seconds (float).
Every node must appear exactly once. Empty graph: empty communities/mapping, zero modularity. Use deterministic seeds where possible. Girvan–Newman size limit failures raise ValueError and comparison should record them as skipped. If limits change, tell Karan to update the help text.

## Friend 3 — analytics and reporting
`core/network_analysis.py`:
- analyze(graph, result) -> (stats_dict, metrics_dataframe)
Stats keys exactly: Users, Connections, Communities, Density, Average clustering, Modularity, Connected components. Optional report keys: Directed, Betweenness sampled. Counts are integers, ratios are numeric.
Metrics columns exactly: user, community, degree, betweenness, closeness, pagerank, clustering. Numeric metric values, one row per user. Empty graphs must still return all column headers.

`core/algorithm_comparison.py`:
- compare(graph) -> (comparison_dataframe, results_dict)
Comparison columns: algorithm, communities, modularity, seconds, sizes, status. Successful status exactly 'OK'; skipped rows contain a readable reason. results_dict maps successful algorithm names to detection results. Calls Friend 2's detect, does not duplicate it.

`core/report_generator.py`:
- safe_csv(frame, path) -> None. Escape formula prefixes in text for spreadsheet safety.
- export_reports(folder, graph, result, stats, centrality, comparison) -> output Path
Filenames: community_membership.csv, user_centrality.csv, network_statistics.csv, algorithm_comparison.csv, summary.pdf. The UI owns the overwrite-confirmation dialog. Backend owns file writing and charts. Support empty data and an unrun comparison with headers only. Raise errors instead of hiding them.

## Handoff acceptance
Each friend supplies working functions, tests and documented semantics. Karan runs main.py --team, confirms TEAM MODULES in the sidebar, and exercises all screens. reference_backend/ contains one compatible example implementation; it is not part of the individual UI contribution.
