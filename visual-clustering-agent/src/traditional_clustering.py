"""
Traditional clustering methods for comparison with visual clustering agent.
"""
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, SpectralClustering
from sklearn.mixture import GaussianMixture
import hdbscan
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')


@dataclass
class ClusteringResult:
    """Result from a clustering algorithm."""
    method: str
    labels: np.ndarray
    n_clusters: int
    parameters: Dict


class TraditionalClusteringBaseline:
    """
    Collection of traditional clustering algorithms for baseline comparison.
    """

    def __init__(self):
        self.results = {}

    def kmeans(
        self,
        X: np.ndarray,
        n_clusters: int = 3,
        n_init: int = 10,
        random_state: int = 42
    ) -> ClusteringResult:
        """
        K-Means clustering.

        Args:
            X: Data matrix
            n_clusters: Number of clusters
            n_init: Number of initializations
            random_state: Random seed

        Returns:
            ClusteringResult
        """
        clusterer = KMeans(n_clusters=n_clusters, n_init=n_init, random_state=random_state)
        labels = clusterer.fit_predict(X)

        result = ClusteringResult(
            method='kmeans',
            labels=labels,
            n_clusters=n_clusters,
            parameters={'n_clusters': n_clusters, 'n_init': n_init}
        )
        self.results['kmeans'] = result
        return result

    def dbscan(
        self,
        X: np.ndarray,
        eps: Optional[float] = None,
        min_samples: int = 5
    ) -> ClusteringResult:
        """
        DBSCAN clustering.

        Args:
            X: Data matrix
            eps: Epsilon parameter (automatically estimated if None)
            min_samples: Minimum samples in neighborhood

        Returns:
            ClusteringResult
        """
        # Auto-estimate eps if not provided
        if eps is None:
            from sklearn.neighbors import NearestNeighbors
            neighbors = NearestNeighbors(n_neighbors=min_samples)
            neighbors_fit = neighbors.fit(X)
            distances, indices = neighbors_fit.kneighbors(X)
            distances = np.sort(distances[:, -1])
            # Use knee/elbow point heuristic
            eps = np.percentile(distances, 90)

        clusterer = DBSCAN(eps=eps, min_samples=min_samples)
        labels = clusterer.fit_predict(X)

        # Count clusters (excluding noise points labeled as -1)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        result = ClusteringResult(
            method='dbscan',
            labels=labels,
            n_clusters=n_clusters,
            parameters={'eps': eps, 'min_samples': min_samples}
        )
        self.results['dbscan'] = result
        return result

    def hdbscan_clustering(
        self,
        X: np.ndarray,
        min_cluster_size: int = 5,
        min_samples: Optional[int] = None
    ) -> ClusteringResult:
        """
        HDBSCAN clustering (hierarchical DBSCAN).

        Args:
            X: Data matrix
            min_cluster_size: Minimum cluster size
            min_samples: Minimum samples in neighborhood

        Returns:
            ClusteringResult
        """
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            gen_min_span_tree=True
        )
        labels = clusterer.fit_predict(X)

        # Count clusters (excluding noise points labeled as -1)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        result = ClusteringResult(
            method='hdbscan',
            labels=labels,
            n_clusters=n_clusters,
            parameters={'min_cluster_size': min_cluster_size, 'min_samples': min_samples}
        )
        self.results['hdbscan'] = result
        return result

    def gaussian_mixture(
        self,
        X: np.ndarray,
        n_components: int = 3,
        covariance_type: str = 'full',
        random_state: int = 42
    ) -> ClusteringResult:
        """
        Gaussian Mixture Model clustering.

        Args:
            X: Data matrix
            n_components: Number of mixture components
            covariance_type: Type of covariance matrix
            random_state: Random seed

        Returns:
            ClusteringResult
        """
        gmm = GaussianMixture(
            n_components=n_components,
            covariance_type=covariance_type,
            random_state=random_state
        )
        labels = gmm.fit_predict(X)

        result = ClusteringResult(
            method='gmm',
            labels=labels,
            n_clusters=n_components,
            parameters={'n_components': n_components, 'covariance_type': covariance_type}
        )
        self.results['gmm'] = result
        return result

    def agglomerative(
        self,
        X: np.ndarray,
        n_clusters: int = 3,
        linkage: str = 'ward'
    ) -> ClusteringResult:
        """
        Agglomerative (hierarchical) clustering.

        Args:
            X: Data matrix
            n_clusters: Number of clusters
            linkage: Linkage criterion

        Returns:
            ClusteringResult
        """
        clusterer = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        labels = clusterer.fit_predict(X)

        result = ClusteringResult(
            method='agglomerative',
            labels=labels,
            n_clusters=n_clusters,
            parameters={'n_clusters': n_clusters, 'linkage': linkage}
        )
        self.results['agglomerative'] = result
        return result

    def spectral(
        self,
        X: np.ndarray,
        n_clusters: int = 3,
        random_state: int = 42
    ) -> ClusteringResult:
        """
        Spectral clustering.

        Args:
            X: Data matrix
            n_clusters: Number of clusters
            random_state: Random seed

        Returns:
            ClusteringResult
        """
        clusterer = SpectralClustering(n_clusters=n_clusters, random_state=random_state, affinity='nearest_neighbors')
        labels = clusterer.fit_predict(X)

        result = ClusteringResult(
            method='spectral',
            labels=labels,
            n_clusters=n_clusters,
            parameters={'n_clusters': n_clusters}
        )
        self.results['spectral'] = result
        return result

    def run_all_methods(
        self,
        X: np.ndarray,
        true_n_clusters: Optional[int] = None,
        auto_detect: bool = True
    ) -> Dict[str, ClusteringResult]:
        """
        Run all clustering methods on the data.

        Args:
            X: Data matrix
            true_n_clusters: Known number of clusters (if available)
            auto_detect: Whether to use auto-detection for methods that support it

        Returns:
            Dictionary of method names to ClusteringResults
        """
        results = {}

        # Estimate number of clusters if not provided
        if true_n_clusters is None:
            # Use elbow method or silhouette for estimation
            from sklearn.metrics import silhouette_score
            max_k = min(10, X.shape[0] // 10)
            best_k = 2
            best_score = -1

            for k in range(2, max_k + 1):
                labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)
                score = silhouette_score(X, labels)
                if score > best_score:
                    best_score = score
                    best_k = k

            estimated_n_clusters = best_k
        else:
            estimated_n_clusters = true_n_clusters

        print(f"Using n_clusters={estimated_n_clusters} for parametric methods")

        # Methods that require specifying number of clusters
        print("Running K-Means...")
        results['kmeans'] = self.kmeans(X, n_clusters=estimated_n_clusters)

        print("Running Gaussian Mixture Model...")
        results['gmm'] = self.gaussian_mixture(X, n_components=estimated_n_clusters)

        print("Running Agglomerative Clustering...")
        results['agglomerative'] = self.agglomerative(X, n_clusters=estimated_n_clusters)

        print("Running Spectral Clustering...")
        results['spectral'] = self.spectral(X, n_clusters=estimated_n_clusters)

        # Methods that auto-detect number of clusters
        if auto_detect:
            print("Running DBSCAN...")
            results['dbscan'] = self.dbscan(X)

            print("Running HDBSCAN...")
            results['hdbscan'] = self.hdbscan_clustering(X)

        self.results = results
        return results


def main():
    """Test traditional clustering methods."""
    from data_generator import HighDimensionalDataGenerator

    print("Testing traditional clustering methods...")
    generator = HighDimensionalDataGenerator(seed=42)
    X, y_true = generator.generate_gaussian_clusters(n_samples=300, n_features=20, n_clusters=4)

    baseline = TraditionalClusteringBaseline()
    results = baseline.run_all_methods(X, true_n_clusters=4)

    print("\n" + "=" * 80)
    print("CLUSTERING RESULTS")
    print("=" * 80)
    print(f"True number of clusters: 4")
    print()

    for method, result in results.items():
        print(f"{method.upper()}:")
        print(f"  Predicted clusters: {result.n_clusters}")
        print(f"  Parameters: {result.parameters}")
        print()


if __name__ == '__main__':
    main()
