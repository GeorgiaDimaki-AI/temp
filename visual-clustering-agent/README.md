# Visual Clustering Agent

An experimental approach to clustering high-dimensional data using vision models to analyze multiple 2D/3D projections.

## 🔬 Research Question

**Can vision models identify cluster structure from visual projections as effectively as traditional computational clustering algorithms?**

This project explores whether the pattern recognition capabilities of modern vision models (like Claude) can be leveraged for clustering by analyzing multiple visual projections of high-dimensional data, potentially offering:
- Complementary insights to traditional methods
- Better handling of visually-apparent but mathematically complex cluster structures
- Interpretable clustering decisions through visual analysis

## 🎯 Approach

### The Visual Clustering Agent Pipeline

1. **Multi-View Generation**: Generate diverse 2D/3D projections of high-dimensional data
   - PCA, t-SNE, UMAP projections
   - Multiple 3D viewing angles
   - Random projections for additional perspectives

2. **Visual Analysis**: Vision model analyzes each projection
   - Identifies distinct clusters
   - Describes cluster characteristics
   - Provides confidence assessments

3. **Synthesis**: Aggregate observations across views
   - Consensus voting on cluster count
   - Confidence weighting
   - Agreement rate analysis

4. **Comparison**: Benchmark against traditional methods
   - K-Means, DBSCAN, HDBSCAN
   - Gaussian Mixture Models
   - Agglomerative & Spectral Clustering

## 📁 Project Structure

```
visual-clustering-agent/
├── src/
│   ├── data_generator.py          # Synthetic dataset generation
│   ├── visualizer.py               # Multi-view visualization engine
│   ├── visual_clustering_agent.py # Vision-based clustering agent
│   ├── traditional_clustering.py  # Baseline clustering methods
│   └── evaluation.py               # Evaluation metrics & comparison
├── experiments/
│   └── run_experiment.py           # Main experiment runner
├── results/                        # Generated results (created on run)
├── demo.py                         # Quick demo script
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to the directory
cd visual-clustering-agent

# Install dependencies
pip install -r requirements.txt
```

### Quick Demo (No API Required)

```bash
python demo.py
```

This runs a complete experiment in mock mode (simulated vision analysis), generating:
- Multiple visualization projections
- Visual agent analysis report
- Comparative evaluation with traditional methods

### Full Experiments with Claude Vision API

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run all experiments
python experiments/run_experiment.py --use-api

# Or run a single dataset
python experiments/run_experiment.py --use-api --dataset gaussian_easy
```

**Available datasets:**
- `gaussian_easy`: Well-separated Gaussian clusters
- `gaussian_hard`: Overlapping Gaussian clusters
- `nested`: Nested spherical clusters
- `manifold`: Clusters on low-dimensional manifolds
- `mixed_density`: Clusters with varying densities

## 📊 Evaluation Metrics

### External Validation (requires ground truth)
- **Adjusted Rand Index (ARI)**: Similarity to ground truth (1.0 = perfect)
- **Normalized Mutual Information (NMI)**: Information overlap with ground truth
- **Fowlkes-Mallows Index (FMI)**: Geometric mean of precision/recall

### Internal Validation (no ground truth needed)
- **Silhouette Score**: Cluster separation quality [-1, 1]
- **Calinski-Harabasz Index**: Between/within cluster variance ratio
- **Davies-Bouldin Index**: Average cluster similarity (lower is better)

## 🧪 Experimental Design

### Synthetic Datasets

The project generates several types of challenging high-dimensional datasets:

1. **Gaussian Clusters**: Classic blob-like clusters with varying separation
2. **Nested Clusters**: Concentric spherical clusters (challenging for density-based methods)
3. **Manifold Clusters**: Clusters on curved low-dimensional manifolds
4. **Mixed Density**: Clusters with exponentially varying densities

### Dimensionality Reduction Methods

Multiple projection methods capture different aspects of data structure:
- **PCA**: Linear, preserves global variance
- **t-SNE**: Non-linear, preserves local structure
- **UMAP**: Non-linear, balances local and global structure
- **Random Projections**: Fast, preserves some distance properties

## 📈 Expected Findings

### When Visual Clustering May Excel
- Clusters with clear visual separation in projections
- Cases where mathematical density definitions are ambiguous
- Scenarios requiring human-interpretable cluster identification

### When Traditional Methods Should Win
- Very high dimensions where projections lose critical information
- Mathematically well-defined cluster structures
- Large-scale datasets (computational efficiency)

### Interesting Failure Modes
- **Projection artifacts**: Clusters appear/disappear in different views
- **Low agreement**: Different projections suggest different cluster counts
- **Dimensionality curse**: True high-dimensional structure not visible in 2D/3D

## 🔧 Customization

### Create Custom Datasets

```python
from src.data_generator import HighDimensionalDataGenerator

generator = HighDimensionalDataGenerator(seed=42)
X, y = generator.generate_gaussian_clusters(
    n_samples=500,
    n_features=50,
    n_clusters=5,
    separation=3.0
)
```

### Add Custom Clustering Methods

```python
from src.traditional_clustering import TraditionalClusteringBaseline

baseline = TraditionalClusteringBaseline()
# Add your method...
```

### Modify Visualization Strategy

```python
from src.visualizer import MultiViewVisualizer

visualizer = MultiViewVisualizer(figsize=(12, 10), dpi=150)
# Generate custom projections...
```

## 🤔 Research Implications

### Why This Matters

1. **Multi-view learning**: Demonstrates value of ensemble perspectives
2. **Vision-language models**: Novel application domain for vision models
3. **Interpretability**: Visual clustering provides human-understandable rationale
4. **Hybrid systems**: Could guide parameter selection for traditional methods

### Limitations to Consider

1. **Computational cost**: Vision model inference vs. direct clustering computation
2. **Information loss**: 2D/3D projections necessarily lose high-dimensional information
3. **Projection bias**: Results depend heavily on chosen projection methods
4. **Lack of guarantees**: No mathematical convergence or optimality guarantees

### Future Research Directions

- **Adaptive projection selection**: Learn which projections are most informative
- **Active learning**: Iteratively request specific views to resolve ambiguity
- **Hybrid approaches**: Use visual analysis to guide traditional clustering
- **Real-world data**: Test on actual high-dimensional datasets (genomics, images, etc.)
- **Multi-modal fusion**: Combine visual analysis with computational metrics

## 📚 Technical Details

### Vision Model Prompting

The agent asks vision models to:
1. Count distinct, separable clusters
2. Describe each cluster's visual characteristics
3. Assess confidence in the analysis
4. Note any ambiguities or overlaps

### Consensus Mechanism

- **Voting**: Most common cluster count across views
- **Confidence weighting**: High-confidence observations weighted more
- **Agreement threshold**: Low agreement triggers "uncertain" verdict

### Comparison Fairness

Since the visual agent only predicts cluster count (not labels), we use K-means with the predicted K for fair metric comparison.

## 🙏 Acknowledgments

This project is an experimental exploration inspired by:
- The success of vision-language models in diverse pattern recognition tasks
- Multi-view clustering literature
- The observation that humans can identify clusters visually more easily than we can define them mathematically

## 📄 License

This is an experimental research project. Use and modify as needed for your research.

## 🐛 Troubleshooting

### Common Issues

**Import errors**: Make sure you're running from the project root and dependencies are installed

```bash
pip install -r requirements.txt
```

**API errors**: Verify your API key is set correctly

```bash
echo $ANTHROPIC_API_KEY
```

**Memory issues**: Reduce dataset size or number of samples

```python
X, y = generator.generate_gaussian_clusters(n_samples=200, n_features=20)
```

## 📬 Contact & Contribution

This is an experimental project. Feel free to:
- Extend the evaluation metrics
- Add new dataset types
- Implement different projection methods
- Test on real-world data
- Compare with other vision models

---

**Note**: This is a research experiment, not a production clustering library. For production use cases, stick with established methods (scikit-learn, HDBSCAN, etc.) unless you have specific needs that visual clustering addresses.
