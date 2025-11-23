#!/usr/bin/env python3
"""
Quick demo of the Visual Clustering Agent.
Runs a simple experiment without API calls (uses mock mode).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import HighDimensionalDataGenerator
from visualizer import MultiViewVisualizer
from visual_clustering_agent import VisualClusteringAgent
from traditional_clustering import TraditionalClusteringBaseline
from evaluation import ClusteringEvaluator
from sklearn.cluster import KMeans


def main():
    print("=" * 80)
    print("VISUAL CLUSTERING AGENT - QUICK DEMO")
    print("=" * 80)
    print("\nThis demo runs in MOCK mode (no API calls)")
    print("For real vision analysis, use: python experiments/run_experiment.py --use-api --api-key YOUR_KEY")
    print()

    # Create output directory
    os.makedirs('results', exist_ok=True)

    # Step 1: Generate synthetic data
    print("Step 1: Generating synthetic high-dimensional data...")
    generator = HighDimensionalDataGenerator(seed=42)
    X, y_true = generator.generate_gaussian_clusters(
        n_samples=300,
        n_features=25,
        n_clusters=4,
        separation=3.0
    )
    info = generator.get_dataset_info(X, y_true)
    print(f"  ✓ Generated {info['n_samples']} samples")
    print(f"  ✓ Dimensions: {info['n_features']}")
    print(f"  ✓ True clusters: {info['n_clusters']}")
    print(f"  ✓ Cluster sizes: {info['cluster_sizes']}")

    # Step 2: Generate visualizations
    print("\nStep 2: Generating multi-view visualizations...")
    visualizer = MultiViewVisualizer()

    views = []

    print("  ✓ PCA 2D projection")
    img = visualizer.generate_2d_plot(X, y_true, method='pca', title='PCA Projection')
    img.save('results/demo_pca.png')
    views.append((img, 'pca_2d'))

    print("  ✓ t-SNE 2D projection")
    img = visualizer.generate_2d_plot(X, y_true, method='tsne', title='t-SNE Projection')
    img.save('results/demo_tsne.png')
    views.append((img, 'tsne_2d'))

    print("  ✓ UMAP 2D projection")
    img = visualizer.generate_2d_plot(X, y_true, method='umap', title='UMAP Projection')
    img.save('results/demo_umap.png')
    views.append((img, 'umap_2d'))

    print("  ✓ PCA 3D projections (multiple angles)")
    for azim in [0, 90, 180]:
        img = visualizer.generate_3d_plot(X, y_true, method='pca', azimuth=azim)
        views.append((img, f'pca_3d_azim_{azim}'))

    print("  ✓ Multi-view grid")
    grid = visualizer.generate_multi_view_grid(X, y_true)
    grid.save('results/demo_multiview.png')

    # Step 3: Visual clustering agent
    print("\nStep 3: Running Visual Clustering Agent (mock mode)...")
    agent = VisualClusteringAgent(use_api=False)

    print(f"  Analyzing {len(views)} different visual projections...")
    observations = agent.analyze_multiple_views(views)

    synthesis = agent.synthesize_observations()
    print(f"\n  VISUAL AGENT RESULTS:")
    print(f"    Predicted clusters: {synthesis['n_clusters_predicted']}")
    print(f"    Confidence: {synthesis['confidence']}")
    print(f"    Agreement rate: {synthesis['agreement_rate']*100:.1f}%")

    # Save detailed report
    report = agent.get_detailed_report()
    with open('results/demo_visual_report.txt', 'w') as f:
        f.write(report)
    print(f"    ✓ Detailed report saved to results/demo_visual_report.txt")

    # Step 4: Traditional clustering methods
    print("\nStep 4: Running traditional clustering methods for comparison...")
    baseline = TraditionalClusteringBaseline()
    traditional_results = baseline.run_all_methods(X, true_n_clusters=4)

    print("  Traditional methods:")
    for method, result in traditional_results.items():
        print(f"    {method}: {result.n_clusters} clusters")

    # Step 5: Evaluation
    print("\nStep 5: Evaluating all methods...")
    evaluator = ClusteringEvaluator()

    # Prepare predictions
    predictions = {name: result.labels for name, result in traditional_results.items()}

    # Add visual agent prediction (using k-means with predicted k)
    visual_k = synthesis['n_clusters_predicted']
    if visual_k > 0:
        visual_labels = KMeans(n_clusters=visual_k, random_state=42).fit_predict(X)
        predictions['visual_agent'] = visual_labels

    # Run evaluation
    evaluation_results = evaluator.compare_methods(X, predictions, y_true)

    # Generate report
    eval_report = evaluator.generate_comparison_report()
    print("\n" + eval_report)

    # Save report
    with open('results/demo_evaluation.txt', 'w') as f:
        f.write(eval_report)

    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nGenerated files in results/:")
    print("  - demo_pca.png, demo_tsne.png, demo_umap.png (visualizations)")
    print("  - demo_multiview.png (grid of all views)")
    print("  - demo_visual_report.txt (visual agent analysis)")
    print("  - demo_evaluation.txt (comparative evaluation)")
    print("\nTo run with actual Claude Vision API:")
    print("  python experiments/run_experiment.py --use-api --api-key YOUR_API_KEY")
    print()


if __name__ == '__main__':
    main()
