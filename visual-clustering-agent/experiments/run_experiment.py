"""
Main experiment runner comparing visual clustering agent with traditional methods.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from data_generator import HighDimensionalDataGenerator
from visualizer import MultiViewVisualizer
from visual_clustering_agent import VisualClusteringAgent
from traditional_clustering import TraditionalClusteringBaseline
from evaluation import ClusteringEvaluator
from typing import Dict, List
import argparse
from datetime import datetime
import json


class ExperimentRunner:
    """Run comprehensive clustering experiments."""

    def __init__(
        self,
        use_vision_api: bool = False,
        api_key: str = None,
        output_dir: str = '../results'
    ):
        """
        Initialize experiment runner.

        Args:
            use_vision_api: Whether to use actual vision API (requires API key)
            api_key: Anthropic API key
            output_dir: Directory to save results
        """
        self.use_vision_api = use_vision_api
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.data_generator = HighDimensionalDataGenerator(seed=42)
        self.visualizer = MultiViewVisualizer(figsize=(10, 8), dpi=100)
        self.visual_agent = VisualClusteringAgent(use_api=use_vision_api, api_key=api_key)
        self.traditional_baseline = TraditionalClusteringBaseline()
        self.evaluator = ClusteringEvaluator()

    def run_single_experiment(
        self,
        dataset_name: str,
        X: np.ndarray,
        y_true: np.ndarray,
        n_views: int = 6
    ) -> Dict:
        """
        Run experiment on a single dataset.

        Args:
            dataset_name: Name of the dataset
            X: Data matrix
            y_true: Ground truth labels
            n_views: Number of visual projections to generate

        Returns:
            Dictionary with experiment results
        """
        print(f"\n{'='*80}")
        print(f"EXPERIMENT: {dataset_name}")
        print(f"{'='*80}")
        print(f"Dataset shape: {X.shape}")
        print(f"True clusters: {len(np.unique(y_true))}")

        results = {
            'dataset_name': dataset_name,
            'dataset_shape': X.shape,
            'true_n_clusters': len(np.unique(y_true)),
            'timestamp': datetime.now().isoformat()
        }

        # Step 1: Generate visualizations
        print(f"\nGenerating {n_views} visual projections...")
        view_images = []

        # PCA views
        print("  - PCA 2D")
        img = self.visualizer.generate_2d_plot(X, y_true, method='pca', title=f'{dataset_name} - PCA')
        img.save(f'{self.output_dir}/{dataset_name}_pca_2d.png')
        view_images.append((img, 'pca_2d'))

        print("  - PCA 3D (multiple angles)")
        for azim in [0, 90, 180]:
            img = self.visualizer.generate_3d_plot(X, y_true, method='pca', azimuth=azim)
            view_images.append((img, f'pca_3d_azim_{azim}'))

        # t-SNE view
        print("  - t-SNE 2D")
        img = self.visualizer.generate_2d_plot(X, y_true, method='tsne', title=f'{dataset_name} - t-SNE')
        img.save(f'{self.output_dir}/{dataset_name}_tsne_2d.png')
        view_images.append((img, 'tsne_2d'))

        # UMAP view
        print("  - UMAP 2D")
        img = self.visualizer.generate_2d_plot(X, y_true, method='umap', title=f'{dataset_name} - UMAP')
        img.save(f'{self.output_dir}/{dataset_name}_umap_2d.png')
        view_images.append((img, 'umap_2d'))

        # Multi-view grid
        print("  - Multi-view grid")
        grid_img = self.visualizer.generate_multi_view_grid(X, y_true)
        grid_img.save(f'{self.output_dir}/{dataset_name}_multiview.png')

        # Step 2: Visual clustering agent analysis
        print(f"\nRunning Visual Clustering Agent...")
        print(f"  Mode: {'API (Claude Vision)' if self.use_vision_api else 'Mock (simulated)'}")

        visual_observations = self.visual_agent.analyze_multiple_views(view_images[:n_views])
        visual_synthesis = self.visual_agent.synthesize_observations()

        print(f"  Visual Agent Prediction: {visual_synthesis['n_clusters_predicted']} clusters")
        print(f"  Confidence: {visual_synthesis['confidence']}")
        print(f"  Agreement: {visual_synthesis['agreement_rate']*100:.1f}%")

        # Save visual agent report
        report = self.visual_agent.get_detailed_report()
        with open(f'{self.output_dir}/{dataset_name}_visual_agent_report.txt', 'w') as f:
            f.write(report)

        results['visual_agent'] = visual_synthesis

        # Step 3: Traditional clustering methods
        print(f"\nRunning Traditional Clustering Methods...")
        traditional_results = self.traditional_baseline.run_all_methods(
            X,
            true_n_clusters=len(np.unique(y_true))
        )

        # Step 4: Evaluation
        print(f"\nEvaluating Methods...")

        # Prepare predictions for evaluation
        predictions = {
            name: result.labels
            for name, result in traditional_results.items()
        }

        # Add visual agent "pseudo-labels" for comparison
        # Since visual agent only predicts number of clusters, we use k-means with that k
        from sklearn.cluster import KMeans
        visual_k = visual_synthesis['n_clusters_predicted']
        if visual_k > 0:
            visual_labels = KMeans(n_clusters=visual_k, random_state=42).fit_predict(X)
            predictions['visual_agent'] = visual_labels

        # Run evaluation
        evaluation_results = self.evaluator.compare_methods(X, predictions, y_true)

        # Generate and save evaluation report
        eval_report = self.evaluator.generate_comparison_report()
        print(f"\n{eval_report}")

        with open(f'{self.output_dir}/{dataset_name}_evaluation_report.txt', 'w') as f:
            f.write(eval_report)

        # Save evaluation metrics as JSON
        self.evaluator.save_results(f'{self.output_dir}/{dataset_name}_metrics.json')

        results['evaluation'] = {
            method: {
                'n_clusters': metrics.n_clusters_predicted,
                'ari': metrics.adjusted_rand_index,
                'nmi': metrics.normalized_mutual_info,
                'silhouette': metrics.silhouette_score,
                'cluster_count_error': metrics.cluster_count_error
            }
            for method, metrics in evaluation_results.items()
        }

        return results

    def run_all_experiments(self, n_views: int = 6) -> List[Dict]:
        """
        Run experiments on all dataset types.

        Args:
            n_views: Number of visual projections per dataset

        Returns:
            List of experiment result dictionaries
        """
        all_results = []

        # Dataset configurations
        datasets = {
            'gaussian_easy': {
                'generator': lambda: self.data_generator.generate_gaussian_clusters(
                    n_samples=400, n_features=30, n_clusters=4, separation=4.0
                ),
                'description': 'Well-separated Gaussian clusters (easy case)'
            },
            'gaussian_hard': {
                'generator': lambda: self.data_generator.generate_gaussian_clusters(
                    n_samples=400, n_features=30, n_clusters=5, separation=2.0
                ),
                'description': 'Overlapping Gaussian clusters (hard case)'
            },
            'nested': {
                'generator': lambda: self.data_generator.generate_nested_clusters(
                    n_samples=400, n_features=30, n_clusters=3
                ),
                'description': 'Nested spherical clusters'
            },
            'manifold': {
                'generator': lambda: self.data_generator.generate_manifold_clusters(
                    n_samples=400, n_features=30, n_clusters=4
                ),
                'description': 'Clusters on low-dimensional manifolds'
            },
            'mixed_density': {
                'generator': lambda: self.data_generator.generate_mixed_density_clusters(
                    n_samples=400, n_features=30, n_clusters=4
                ),
                'description': 'Clusters with varying densities'
            }
        }

        for dataset_name, config in datasets.items():
            print(f"\n\n{'#'*80}")
            print(f"# DATASET: {dataset_name}")
            print(f"# {config['description']}")
            print(f"{'#'*80}")

            # Generate dataset
            X, y_true = config['generator']()

            # Run experiment
            try:
                result = self.run_single_experiment(dataset_name, X, y_true, n_views)
                all_results.append(result)
            except Exception as e:
                print(f"ERROR in {dataset_name}: {str(e)}")
                import traceback
                traceback.print_exc()

        # Save summary
        summary_path = f'{self.output_dir}/experiment_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)

        print(f"\n\n{'='*80}")
        print(f"ALL EXPERIMENTS COMPLETE")
        print(f"Results saved to: {self.output_dir}")
        print(f"Summary: {summary_path}")
        print(f"{'='*80}")

        return all_results


def main():
    parser = argparse.ArgumentParser(description='Run visual clustering experiments')
    parser.add_argument('--use-api', action='store_true',
                       help='Use actual Claude Vision API (requires --api-key)')
    parser.add_argument('--api-key', type=str,
                       help='Anthropic API key for vision analysis')
    parser.add_argument('--output-dir', type=str,
                       default='../results',
                       help='Output directory for results')
    parser.add_argument('--n-views', type=int, default=6,
                       help='Number of visual projections to analyze')
    parser.add_argument('--dataset', type=str,
                       help='Run single dataset only (gaussian_easy, gaussian_hard, nested, manifold, mixed_density)')

    args = parser.parse_args()

    # Validate API key if using API
    if args.use_api and not args.api_key:
        # Try environment variable
        import os
        args.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not args.api_key:
            print("ERROR: --api-key required when using --use-api")
            print("Or set ANTHROPIC_API_KEY environment variable")
            return

    # Create experiment runner
    runner = ExperimentRunner(
        use_vision_api=args.use_api,
        api_key=args.api_key,
        output_dir=args.output_dir
    )

    # Run experiments
    if args.dataset:
        # Run single dataset
        generator = HighDimensionalDataGenerator(seed=42)
        if args.dataset == 'gaussian_easy':
            X, y = generator.generate_gaussian_clusters(n_samples=400, n_features=30, n_clusters=4, separation=4.0)
        elif args.dataset == 'gaussian_hard':
            X, y = generator.generate_gaussian_clusters(n_samples=400, n_features=30, n_clusters=5, separation=2.0)
        elif args.dataset == 'nested':
            X, y = generator.generate_nested_clusters(n_samples=400, n_features=30, n_clusters=3)
        elif args.dataset == 'manifold':
            X, y = generator.generate_manifold_clusters(n_samples=400, n_features=30, n_clusters=4)
        elif args.dataset == 'mixed_density':
            X, y = generator.generate_mixed_density_clusters(n_samples=400, n_features=30, n_clusters=4)
        else:
            print(f"Unknown dataset: {args.dataset}")
            return

        runner.run_single_experiment(args.dataset, X, y, args.n_views)
    else:
        # Run all datasets
        runner.run_all_experiments(args.n_views)


if __name__ == '__main__':
    main()
