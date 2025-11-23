# Quick Usage Guide

## Installation

```bash
pip install -r requirements.txt
```

## Running the Demo (No API Required)

The fastest way to see the system in action:

```bash
python demo.py
```

This will:
1. Generate synthetic 25D data with 4 clusters
2. Create PCA, t-SNE, and UMAP visualizations
3. Run the visual clustering agent in mock mode
4. Compare with 6 traditional clustering methods
5. Generate evaluation reports

**Output files** (in `results/`):
- `demo_pca.png`, `demo_tsne.png`, `demo_umap.png` - Individual projections
- `demo_multiview.png` - Grid of all projections
- `demo_visual_report.txt` - Visual agent's analysis
- `demo_evaluation.txt` - Comparative metrics

## Running with Claude Vision API

For actual vision-based analysis:

```bash
# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run on a single dataset
python experiments/run_experiment.py --use-api --dataset gaussian_easy

# Run all experiments
python experiments/run_experiment.py --use-api
```

## Command Line Options

```bash
python experiments/run_experiment.py [OPTIONS]

Options:
  --use-api          Use Claude Vision API (requires --api-key)
  --api-key KEY      Anthropic API key
  --dataset NAME     Run single dataset: gaussian_easy, gaussian_hard,
                     nested, manifold, mixed_density
  --n-views N        Number of visual projections (default: 6)
  --output-dir DIR   Output directory (default: ../results)
```

## Understanding the Output

### Visual Agent Report

Example from `demo_visual_report.txt`:

```
Observation 1: pca_2d
  Clusters observed: 4
  Confidence: high
  Descriptions:
    1. Dense cluster in upper-left
    2. Scattered cluster center-right
    ...

SYNTHESIS:
  Predicted clusters: 4
  Confidence: high
  Agreement across views: 100.0%
```

### Evaluation Metrics

The evaluation report shows:

1. **Cluster Count Summary**: How many clusters each method found
2. **External Metrics** (if ground truth available):
   - ARI (Adjusted Rand Index): 1.0 = perfect match
   - NMI (Normalized Mutual Info): How much information is shared
   - FMI (Fowlkes-Mallows): Precision/recall balance

3. **Internal Metrics** (no ground truth needed):
   - Silhouette: How well-separated clusters are (-1 to 1, higher better)
   - Calinski-Harabasz: Variance ratio (higher better)
   - Davies-Bouldin: Cluster similarity (lower better)

## Python API Usage

### Generate Custom Data

```python
from src.data_generator import HighDimensionalDataGenerator

generator = HighDimensionalDataGenerator(seed=42)

# Easy case: well-separated clusters
X, y = generator.generate_gaussian_clusters(
    n_samples=500,
    n_features=50,
    n_clusters=5,
    separation=4.0  # larger = more separated
)

# Hard case: nested spheres
X, y = generator.generate_nested_clusters(
    n_samples=400,
    n_features=30,
    n_clusters=3
)
```

### Create Visualizations

```python
from src.visualizer import MultiViewVisualizer

viz = MultiViewVisualizer(figsize=(10, 8), dpi=100)

# Single 2D plot
img = viz.generate_2d_plot(X, y, method='tsne', title='My Data')
img.save('my_plot.png')

# 3D plot from specific angle
img = viz.generate_3d_plot(X, y, method='pca', azimuth=45, elevation=30)

# Multi-view grid
grid = viz.generate_multi_view_grid(X, y, methods=['pca', 'tsne', 'umap'])
grid.save('multiview.png')
```

### Run Visual Clustering Agent

```python
from src.visual_clustering_agent import VisualClusteringAgent

# Mock mode (no API)
agent = VisualClusteringAgent(use_api=False)

# Real mode (requires API key)
agent = VisualClusteringAgent(use_api=True, api_key="sk-ant-...")

# Analyze views
views = [(img1, 'pca_2d'), (img2, 'tsne_2d'), ...]
observations = agent.analyze_multiple_views(views)

# Get synthesis
synthesis = agent.synthesize_observations()
print(f"Predicted clusters: {synthesis['n_clusters_predicted']}")
print(f"Confidence: {synthesis['confidence']}")

# Detailed report
print(agent.get_detailed_report())
```

### Run Traditional Clustering

```python
from src.traditional_clustering import TraditionalClusteringBaseline

baseline = TraditionalClusteringBaseline()

# Run all methods
results = baseline.run_all_methods(X, true_n_clusters=5)

# Or run individual methods
kmeans_result = baseline.kmeans(X, n_clusters=5)
dbscan_result = baseline.dbscan(X, eps=0.5, min_samples=5)
hdbscan_result = baseline.hdbscan_clustering(X, min_cluster_size=10)
```

### Evaluate and Compare

```python
from src.evaluation import ClusteringEvaluator

evaluator = ClusteringEvaluator()

# Prepare predictions
predictions = {
    'kmeans': kmeans_labels,
    'dbscan': dbscan_labels,
    'visual_agent': visual_labels,
}

# Evaluate
results = evaluator.compare_methods(X, predictions, y_true)

# Print report
print(evaluator.generate_comparison_report())

# Get rankings
top_methods = evaluator.get_ranking('adjusted_rand_index', higher_is_better=True)
```

## Dataset Types

### Gaussian (Easy)
- Well-separated spherical clusters
- `separation=4.0` creates clear gaps
- Best case for most algorithms

### Gaussian (Hard)
- Overlapping clusters
- `separation=2.0` creates ambiguity
- Tests robustness to noise

### Nested
- Concentric spherical shells
- Challenges density-based methods
- Tests non-convex cluster detection

### Manifold
- Clusters on curved surfaces
- Tests preservation of intrinsic structure
- Requires good dimensionality reduction

### Mixed Density
- Exponentially varying cluster densities
- Challenges DBSCAN (single epsilon)
- Tests adaptivity

## Tips for Best Results

### For Visual Clustering Agent

1. **Use diverse projections**: PCA (global), t-SNE (local), UMAP (balanced)
2. **Multiple angles**: 3D plots from different viewpoints catch different structures
3. **Mock mode for testing**: Fast iteration without API costs
4. **Real API for production**: More nuanced cluster identification

### For Traditional Methods

1. **K-Means**: Fast, works well for spherical clusters with known k
2. **DBSCAN**: Good for arbitrary shapes, but sensitive to epsilon
3. **HDBSCAN**: Handles varying densities better than DBSCAN
4. **GMM**: Better than K-Means for elliptical clusters
5. **Spectral**: Excellent for manifold/graph-structured data

### For Evaluation

1. **Use external metrics** when ground truth available (ARI, NMI)
2. **Use internal metrics** for real-world data (Silhouette, CH)
3. **Visual inspection** is crucial - metrics don't tell the whole story
4. **Consider domain**: Different applications value different cluster properties

## Common Patterns

### Pattern 1: Visual agent has low agreement

```
Agreement rate: 45%
Cluster predictions: {3: 3, 4: 2, 5: 2}
```

**Interpretation**: Cluster structure varies across projections. Either:
- High-dimensional structure is genuinely ambiguous
- Different projections reveal different aspects
- Suggests using ensemble methods

### Pattern 2: Visual agent differs from all traditional methods

```
Visual agent: 5 clusters (high confidence)
All traditional: 3 clusters
```

**Interpretation**: Visual patterns not captured by mathematical definitions. Worth investigating:
- Check visualizations manually
- May indicate substructure within clusters
- Consider hierarchical clustering

### Pattern 3: Perfect agreement everywhere

```
All methods predict 4 clusters
All have ARI > 0.95
```

**Interpretation**: Very clean dataset. In real-world:
- Rare but good!
- Suggests robust cluster structure
- Any method will work well

## Troubleshooting

**Q: Visual agent always predicts wrong number**
A: In mock mode, it returns simulated results. Use `--use-api` for real analysis.

**Q: DBSCAN finds 0 or 1 clusters**
A: Epsilon too large/small. Let auto-detection handle it, or tune manually.

**Q: Out of memory errors**
A: Reduce `n_samples` or `n_features` in data generation.

**Q: t-SNE/UMAP very slow**
A: Expected for large datasets. Consider PCA first, or reduce samples.

**Q: All metrics are perfect (1.0)**
A: Your dataset is too easy! Try `gaussian_hard` or `nested`.

## Next Steps

1. **Try different datasets**: Experiment with the 5 built-in types
2. **Add custom data**: Bring your own high-dimensional data
3. **Tune parameters**: Adjust separation, density, manifold curvature
4. **Compare projections**: Which reduction method reveals structure best?
5. **Extend methods**: Add new clustering algorithms or projection techniques

## Need Help?

- Check the main [README.md](README.md) for conceptual overview
- Review code in `src/` for implementation details
- Run `python demo.py` to verify installation
- Examine `results/` output files for examples
