"""
Generate synthetic high-dimensional datasets with known cluster structure.
"""
import numpy as np
from sklearn.datasets import make_blobs, make_classification
from typing import Tuple, List, Dict


class HighDimensionalDataGenerator:
    """Generate high-dimensional data with known cluster structure."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        np.random.seed(seed)

    def generate_gaussian_clusters(
        self,
        n_samples: int = 500,
        n_features: int = 50,
        n_clusters: int = 5,
        cluster_std: float = 1.0,
        separation: float = 3.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate data with Gaussian clusters.

        Args:
            n_samples: Number of samples
            n_features: Number of dimensions
            n_clusters: Number of true clusters
            cluster_std: Standard deviation of clusters
            separation: How separated the clusters are

        Returns:
            X: Data matrix (n_samples, n_features)
            y: True cluster labels (n_samples,)
        """
        X, y = make_blobs(
            n_samples=n_samples,
            n_features=n_features,
            centers=n_clusters,
            cluster_std=cluster_std,
            center_box=(-separation * 5, separation * 5),
            random_state=self.seed
        )
        return X, y

    def generate_nested_clusters(
        self,
        n_samples: int = 500,
        n_features: int = 50,
        n_clusters: int = 3
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate nested spherical clusters (challenging case).

        Returns:
            X: Data matrix
            y: True cluster labels
        """
        samples_per_cluster = n_samples // n_clusters
        X_list = []
        y_list = []

        for i in range(n_clusters):
            # Generate points on hypersphere with different radii
            radius = (i + 1) * 3
            samples = samples_per_cluster

            # Random points on unit hypersphere
            points = np.random.randn(samples, n_features)
            points = points / np.linalg.norm(points, axis=1, keepdims=True)

            # Scale to desired radius and add noise
            points = points * radius + np.random.randn(samples, n_features) * 0.5

            X_list.append(points)
            y_list.append(np.full(samples, i))

        X = np.vstack(X_list)
        y = np.concatenate(y_list)

        # Shuffle
        perm = np.random.permutation(len(X))
        return X[perm], y[perm]

    def generate_manifold_clusters(
        self,
        n_samples: int = 500,
        n_features: int = 50,
        n_clusters: int = 4
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate clusters on low-dimensional manifolds embedded in high-dimensional space.

        Returns:
            X: Data matrix
            y: True cluster labels
        """
        samples_per_cluster = n_samples // n_clusters
        X_list = []
        y_list = []

        for i in range(n_clusters):
            # Create a 2D manifold (e.g., plane or curved surface)
            t = np.linspace(0, 2 * np.pi, samples_per_cluster)
            s = np.random.rand(samples_per_cluster) * 2 - 1

            # Parametric surface in 3D
            x = np.cos(t + i * np.pi / 2) * (2 + s)
            y_coord = np.sin(t + i * np.pi / 2) * (2 + s)
            z = s * 2

            # Embed in higher dimensions
            manifold_3d = np.column_stack([x, y_coord, z])

            # Random projection to high-dimensional space
            projection_matrix = np.random.randn(3, n_features)
            X_high = manifold_3d @ projection_matrix

            # Add small noise
            X_high += np.random.randn(*X_high.shape) * 0.3

            X_list.append(X_high)
            y_list.append(np.full(samples_per_cluster, i))

        X = np.vstack(X_list)
        y = np.concatenate(y_list)

        # Shuffle
        perm = np.random.permutation(len(X))
        return X[perm], y[perm]

    def generate_mixed_density_clusters(
        self,
        n_samples: int = 500,
        n_features: int = 50,
        n_clusters: int = 4
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate clusters with varying densities (challenging for density-based methods).

        Returns:
            X: Data matrix
            y: True cluster labels
        """
        X_list = []
        y_list = []

        samples_remaining = n_samples
        for i in range(n_clusters):
            # Vary cluster sizes and densities
            samples_this_cluster = samples_remaining // (n_clusters - i)
            samples_remaining -= samples_this_cluster

            # Exponentially varying density
            std = 0.5 * (2 ** i)

            # Random center
            center = np.random.randn(n_features) * 10

            # Generate cluster
            cluster_data = np.random.randn(samples_this_cluster, n_features) * std + center

            X_list.append(cluster_data)
            y_list.append(np.full(samples_this_cluster, i))

        X = np.vstack(X_list)
        y = np.concatenate(y_list)

        # Shuffle
        perm = np.random.permutation(len(X))
        return X[perm], y[perm]

    def get_dataset_info(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Get information about a dataset."""
        return {
            'n_samples': X.shape[0],
            'n_features': X.shape[1],
            'n_clusters': len(np.unique(y)),
            'cluster_sizes': [np.sum(y == label) for label in np.unique(y)],
            'feature_range': (X.min(), X.max()),
            'feature_mean_std': (X.mean(axis=0).mean(), X.std(axis=0).mean())
        }


def main():
    """Test data generation."""
    generator = HighDimensionalDataGenerator(seed=42)

    print("Generating test datasets...")

    # Test each type
    datasets = {
        'gaussian': generator.generate_gaussian_clusters(n_samples=300, n_features=20, n_clusters=4),
        'nested': generator.generate_nested_clusters(n_samples=300, n_features=20, n_clusters=3),
        'manifold': generator.generate_manifold_clusters(n_samples=300, n_features=20, n_clusters=4),
        'mixed_density': generator.generate_mixed_density_clusters(n_samples=300, n_features=20, n_clusters=4)
    }

    for name, (X, y) in datasets.items():
        info = generator.get_dataset_info(X, y)
        print(f"\n{name.upper()}:")
        print(f"  Shape: {X.shape}")
        print(f"  Clusters: {info['n_clusters']}")
        print(f"  Cluster sizes: {info['cluster_sizes']}")
        print(f"  Feature range: [{info['feature_range'][0]:.2f}, {info['feature_range'][1]:.2f}]")


if __name__ == '__main__':
    main()
