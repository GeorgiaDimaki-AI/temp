"""
Evaluation framework for comparing visual clustering with traditional methods.
"""
import numpy as np
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    fowlkes_mallows_score,
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class EvaluationMetrics:
    """Container for evaluation metrics."""
    method: str

    # External validation (requires ground truth)
    adjusted_rand_index: Optional[float] = None
    normalized_mutual_info: Optional[float] = None
    fowlkes_mallows_index: Optional[float] = None

    # Internal validation (no ground truth needed)
    silhouette_score: Optional[float] = None
    calinski_harabasz_score: Optional[float] = None
    davies_bouldin_score: Optional[float] = None

    # Cluster count accuracy
    n_clusters_predicted: int = 0
    n_clusters_true: Optional[int] = None
    cluster_count_error: Optional[int] = None

    # Additional info
    noise_points: int = 0
    noise_percentage: float = 0.0


class ClusteringEvaluator:
    """
    Evaluate and compare clustering results.
    """

    def __init__(self):
        self.results: Dict[str, EvaluationMetrics] = {}

    def evaluate(
        self,
        X: np.ndarray,
        labels_pred: np.ndarray,
        labels_true: Optional[np.ndarray] = None,
        method_name: str = "unknown"
    ) -> EvaluationMetrics:
        """
        Evaluate clustering result.

        Args:
            X: Data matrix
            labels_pred: Predicted cluster labels
            labels_true: Ground truth labels (if available)
            method_name: Name of the method

        Returns:
            EvaluationMetrics
        """
        metrics = EvaluationMetrics(method=method_name)

        # Handle noise points (labeled as -1 in DBSCAN/HDBSCAN)
        noise_mask = labels_pred == -1
        metrics.noise_points = np.sum(noise_mask)
        metrics.noise_percentage = 100 * metrics.noise_points / len(labels_pred)

        # Get non-noise labels for internal metrics
        if np.any(noise_mask):
            X_clean = X[~noise_mask]
            labels_clean = labels_pred[~noise_mask]
        else:
            X_clean = X
            labels_clean = labels_pred

        # Number of clusters
        metrics.n_clusters_predicted = len(np.unique(labels_clean))

        # External validation metrics (require ground truth)
        if labels_true is not None:
            metrics.n_clusters_true = len(np.unique(labels_true))
            metrics.cluster_count_error = abs(metrics.n_clusters_predicted - metrics.n_clusters_true)

            try:
                metrics.adjusted_rand_index = adjusted_rand_score(labels_true, labels_pred)
            except Exception:
                metrics.adjusted_rand_index = None

            try:
                metrics.normalized_mutual_info = normalized_mutual_info_score(labels_true, labels_pred)
            except Exception:
                metrics.normalized_mutual_info = None

            try:
                metrics.fowlkes_mallows_index = fowlkes_mallows_score(labels_true, labels_pred)
            except Exception:
                metrics.fowlkes_mallows_index = None

        # Internal validation metrics (no ground truth needed)
        if len(X_clean) > 0 and metrics.n_clusters_predicted > 1:
            try:
                metrics.silhouette_score = silhouette_score(X_clean, labels_clean)
            except Exception:
                metrics.silhouette_score = None

            try:
                metrics.calinski_harabasz_score = calinski_harabasz_score(X_clean, labels_clean)
            except Exception:
                metrics.calinski_harabasz_score = None

            try:
                metrics.davies_bouldin_score = davies_bouldin_score(X_clean, labels_clean)
            except Exception:
                metrics.davies_bouldin_score = None

        self.results[method_name] = metrics
        return metrics

    def compare_methods(
        self,
        X: np.ndarray,
        predictions: Dict[str, np.ndarray],
        labels_true: Optional[np.ndarray] = None
    ) -> Dict[str, EvaluationMetrics]:
        """
        Compare multiple clustering methods.

        Args:
            X: Data matrix
            predictions: Dictionary of method_name -> predicted_labels
            labels_true: Ground truth labels (if available)

        Returns:
            Dictionary of method_name -> EvaluationMetrics
        """
        results = {}
        for method_name, labels_pred in predictions.items():
            metrics = self.evaluate(X, labels_pred, labels_true, method_name)
            results[method_name] = metrics

        self.results = results
        return results

    def get_ranking(self, metric_name: str, higher_is_better: bool = True) -> List[tuple]:
        """
        Rank methods by a specific metric.

        Args:
            metric_name: Name of the metric to rank by
            higher_is_better: Whether higher values are better

        Returns:
            List of (method_name, metric_value) tuples, sorted
        """
        rankings = []
        for method, metrics in self.results.items():
            value = getattr(metrics, metric_name, None)
            if value is not None:
                rankings.append((method, value))

        rankings.sort(key=lambda x: x[1], reverse=higher_is_better)
        return rankings

    def generate_comparison_report(self) -> str:
        """Generate a detailed comparison report."""
        report = "=" * 100 + "\n"
        report += "CLUSTERING EVALUATION REPORT\n"
        report += "=" * 100 + "\n\n"

        if not self.results:
            return report + "No results to report.\n"

        # Summary table
        report += "CLUSTER COUNT SUMMARY\n"
        report += "-" * 100 + "\n"
        report += f"{'Method':<20} {'Predicted':<12} {'True':<12} {'Error':<12} {'Noise %':<12}\n"
        report += "-" * 100 + "\n"

        for method, metrics in self.results.items():
            true_str = str(metrics.n_clusters_true) if metrics.n_clusters_true is not None else "N/A"
            error_str = str(metrics.cluster_count_error) if metrics.cluster_count_error is not None else "N/A"
            report += f"{method:<20} {metrics.n_clusters_predicted:<12} {true_str:<12} {error_str:<12} {metrics.noise_percentage:<12.2f}\n"

        # External metrics (if ground truth available)
        if any(m.adjusted_rand_index is not None for m in self.results.values()):
            report += "\n\nEXTERNAL VALIDATION METRICS (with ground truth)\n"
            report += "-" * 100 + "\n"
            report += f"{'Method':<20} {'ARI':<15} {'NMI':<15} {'FMI':<15}\n"
            report += "-" * 100 + "\n"

            for method, metrics in self.results.items():
                ari = f"{metrics.adjusted_rand_index:.4f}" if metrics.adjusted_rand_index is not None else "N/A"
                nmi = f"{metrics.normalized_mutual_info:.4f}" if metrics.normalized_mutual_info is not None else "N/A"
                fmi = f"{metrics.fowlkes_mallows_index:.4f}" if metrics.fowlkes_mallows_index is not None else "N/A"
                report += f"{method:<20} {ari:<15} {nmi:<15} {fmi:<15}\n"

        # Internal metrics
        report += "\n\nINTERNAL VALIDATION METRICS (no ground truth needed)\n"
        report += "-" * 100 + "\n"
        report += f"{'Method':<20} {'Silhouette':<15} {'Calinski-H':<15} {'Davies-B':<15}\n"
        report += "-" * 100 + "\n"

        for method, metrics in self.results.items():
            sil = f"{metrics.silhouette_score:.4f}" if metrics.silhouette_score is not None else "N/A"
            ch = f"{metrics.calinski_harabasz_score:.2f}" if metrics.calinski_harabasz_score is not None else "N/A"
            db = f"{metrics.davies_bouldin_score:.4f}" if metrics.davies_bouldin_score is not None else "N/A"
            report += f"{method:<20} {sil:<15} {ch:<15} {db:<15}\n"

        # Rankings
        report += "\n\nRANKINGS\n"
        report += "-" * 100 + "\n"

        if any(m.adjusted_rand_index is not None for m in self.results.values()):
            report += "\nBy Adjusted Rand Index (higher is better):\n"
            for i, (method, score) in enumerate(self.get_ranking('adjusted_rand_index', higher_is_better=True), 1):
                report += f"  {i}. {method}: {score:.4f}\n"

        if any(m.silhouette_score is not None for m in self.results.values()):
            report += "\nBy Silhouette Score (higher is better):\n"
            for i, (method, score) in enumerate(self.get_ranking('silhouette_score', higher_is_better=True), 1):
                report += f"  {i}. {method}: {score:.4f}\n"

        if any(m.cluster_count_error is not None for m in self.results.values()):
            report += "\nBy Cluster Count Error (lower is better):\n"
            for i, (method, score) in enumerate(self.get_ranking('cluster_count_error', higher_is_better=False), 1):
                report += f"  {i}. {method}: {score}\n"

        report += "\n" + "=" * 100 + "\n"
        report += "METRIC INTERPRETATION:\n"
        report += "- ARI (Adjusted Rand Index): Similarity to ground truth, 1.0 = perfect, 0.0 = random\n"
        report += "- NMI (Normalized Mutual Info): Information shared with ground truth, 1.0 = perfect\n"
        report += "- FMI (Fowlkes-Mallows Index): Geometric mean of precision and recall, 1.0 = perfect\n"
        report += "- Silhouette Score: Cluster separation quality, range [-1, 1], higher is better\n"
        report += "- Calinski-Harabasz: Ratio of between-cluster to within-cluster variance, higher is better\n"
        report += "- Davies-Bouldin: Average similarity between clusters, lower is better\n"
        report += "=" * 100 + "\n"

        return report

    def save_results(self, filepath: str):
        """Save evaluation results to JSON."""
        data = {
            method: asdict(metrics)
            for method, metrics in self.results.items()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Test evaluation framework."""
    from data_generator import HighDimensionalDataGenerator
    from traditional_clustering import TraditionalClusteringBaseline

    print("Testing evaluation framework...")

    # Generate test data
    generator = HighDimensionalDataGenerator(seed=42)
    X, y_true = generator.generate_gaussian_clusters(n_samples=300, n_features=20, n_clusters=4)

    # Run clustering methods
    baseline = TraditionalClusteringBaseline()
    clustering_results = baseline.run_all_methods(X, true_n_clusters=4)

    # Prepare predictions dictionary
    predictions = {
        name: result.labels
        for name, result in clustering_results.items()
    }

    # Evaluate
    evaluator = ClusteringEvaluator()
    evaluator.compare_methods(X, predictions, y_true)

    # Generate report
    print("\n" + evaluator.generate_comparison_report())


if __name__ == '__main__':
    main()
