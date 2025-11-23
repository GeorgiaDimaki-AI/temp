"""
Multi-view visualization engine for high-dimensional data.
Generates various 2D/3D projections for visual inspection.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
from typing import List, Tuple, Optional
import io
from PIL import Image


class MultiViewVisualizer:
    """Generate multiple views of high-dimensional data."""

    def __init__(self, figsize: Tuple[int, int] = (10, 8), dpi: int = 100):
        self.figsize = figsize
        self.dpi = dpi

    def _apply_projection(self, X: np.ndarray, method: str, n_components: int = 2, **kwargs) -> np.ndarray:
        """
        Apply dimensionality reduction.

        Args:
            X: Data matrix
            method: 'pca', 'tsne', 'umap', or 'random'
            n_components: Number of components (2 or 3)
            **kwargs: Additional parameters for the method

        Returns:
            Projected data
        """
        if method == 'pca':
            reducer = PCA(n_components=n_components, **kwargs)
            return reducer.fit_transform(X)

        elif method == 'tsne':
            # t-SNE parameters
            perplexity = kwargs.get('perplexity', 30)
            reducer = TSNE(n_components=n_components, perplexity=perplexity, random_state=kwargs.get('random_state', 42))
            return reducer.fit_transform(X)

        elif method == 'umap':
            # UMAP parameters
            n_neighbors = kwargs.get('n_neighbors', 15)
            min_dist = kwargs.get('min_dist', 0.1)
            reducer = umap.UMAP(n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, random_state=kwargs.get('random_state', 42))
            return reducer.fit_transform(X)

        elif method == 'random':
            # Random projection (fast, preserves some structure)
            projection_matrix = np.random.randn(X.shape[1], n_components)
            projection_matrix /= np.linalg.norm(projection_matrix, axis=0)
            return X @ projection_matrix

        elif method == 'feature_pairs':
            # Just select specific feature pairs
            feature_idx = kwargs.get('feature_idx', [0, 1])
            return X[:, feature_idx]

        else:
            raise ValueError(f"Unknown method: {method}")

    def generate_2d_plot(
        self,
        X: np.ndarray,
        true_labels: Optional[np.ndarray] = None,
        method: str = 'pca',
        title: str = '',
        **kwargs
    ) -> Image.Image:
        """
        Generate a 2D scatter plot.

        Args:
            X: Data matrix
            true_labels: Ground truth labels (optional, for coloring)
            method: Projection method
            title: Plot title
            **kwargs: Additional parameters for projection method

        Returns:
            PIL Image of the plot
        """
        # Project to 2D
        X_2d = self._apply_projection(X, method, n_components=2, **kwargs)

        # Create plot
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        if true_labels is not None:
            # Color by true labels
            scatter = ax.scatter(X_2d[:, 0], X_2d[:, 1], c=true_labels, cmap='tab10', alpha=0.6, s=20)
            plt.colorbar(scatter, ax=ax, label='True Cluster')
        else:
            ax.scatter(X_2d[:, 0], X_2d[:, 1], alpha=0.6, s=20, c='blue')

        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_title(title or f'{method.upper()} Projection')
        ax.grid(True, alpha=0.3)

        # Convert to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)

    def generate_3d_plot(
        self,
        X: np.ndarray,
        true_labels: Optional[np.ndarray] = None,
        method: str = 'pca',
        title: str = '',
        elevation: float = 30,
        azimuth: float = 45,
        **kwargs
    ) -> Image.Image:
        """
        Generate a 3D scatter plot from a specific viewing angle.

        Args:
            X: Data matrix
            true_labels: Ground truth labels (optional)
            method: Projection method
            title: Plot title
            elevation: Viewing elevation angle
            azimuth: Viewing azimuth angle
            **kwargs: Additional parameters

        Returns:
            PIL Image of the plot
        """
        # Project to 3D
        X_3d = self._apply_projection(X, method, n_components=3, **kwargs)

        # Create 3D plot
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')

        if true_labels is not None:
            scatter = ax.scatter(X_3d[:, 0], X_3d[:, 1], X_3d[:, 2],
                                c=true_labels, cmap='tab10', alpha=0.6, s=20)
            plt.colorbar(scatter, ax=ax, label='True Cluster', pad=0.1)
        else:
            ax.scatter(X_3d[:, 0], X_3d[:, 1], X_3d[:, 2], alpha=0.6, s=20, c='blue')

        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_zlabel('Component 3')
        ax.set_title(title or f'{method.upper()} 3D Projection (elev={elevation}, azim={azimuth})')

        # Set viewing angle
        ax.view_init(elev=elevation, azim=azimuth)

        # Convert to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)

    def generate_multi_view_grid(
        self,
        X: np.ndarray,
        true_labels: Optional[np.ndarray] = None,
        methods: List[str] = ['pca', 'tsne', 'umap'],
        n_random_projections: int = 3
    ) -> Image.Image:
        """
        Generate a grid of multiple views using different projection methods.

        Args:
            X: Data matrix
            true_labels: Ground truth labels
            methods: List of projection methods to use
            n_random_projections: Number of random projections to include

        Returns:
            PIL Image containing grid of plots
        """
        n_plots = len(methods) + n_random_projections
        n_cols = 3
        n_rows = (n_plots + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows), dpi=self.dpi)
        axes = axes.flatten() if n_plots > 1 else [axes]

        plot_idx = 0

        # Standard methods
        for method in methods:
            ax = axes[plot_idx]
            try:
                X_2d = self._apply_projection(X, method, n_components=2)

                if true_labels is not None:
                    ax.scatter(X_2d[:, 0], X_2d[:, 1], c=true_labels, cmap='tab10', alpha=0.6, s=20)
                else:
                    ax.scatter(X_2d[:, 0], X_2d[:, 1], alpha=0.6, s=20, c='blue')

                ax.set_title(f'{method.upper()} Projection')
                ax.grid(True, alpha=0.3)
                plot_idx += 1
            except Exception as e:
                ax.text(0.5, 0.5, f'Error: {str(e)}', ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f'{method.upper()} (failed)')
                plot_idx += 1

        # Random projections
        for i in range(n_random_projections):
            ax = axes[plot_idx]
            X_2d = self._apply_projection(X, 'random', n_components=2, random_state=i)

            if true_labels is not None:
                ax.scatter(X_2d[:, 0], X_2d[:, 1], c=true_labels, cmap='tab10', alpha=0.6, s=20)
            else:
                ax.scatter(X_2d[:, 0], X_2d[:, 1], alpha=0.6, s=20, c='blue')

            ax.set_title(f'Random Projection {i+1}')
            ax.grid(True, alpha=0.3)
            plot_idx += 1

        # Hide unused subplots
        for idx in range(plot_idx, len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()

        # Convert to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)

    def generate_3d_rotation_sequence(
        self,
        X: np.ndarray,
        true_labels: Optional[np.ndarray] = None,
        method: str = 'pca',
        n_angles: int = 8
    ) -> List[Image.Image]:
        """
        Generate a sequence of 3D plots from different viewing angles.

        Args:
            X: Data matrix
            true_labels: Ground truth labels
            method: Projection method
            n_angles: Number of different viewing angles

        Returns:
            List of PIL Images showing different angles
        """
        images = []
        azimuths = np.linspace(0, 360, n_angles, endpoint=False)

        for azimuth in azimuths:
            img = self.generate_3d_plot(
                X, true_labels, method,
                title=f'{method.upper()} 3D (azimuth={azimuth:.0f}°)',
                elevation=30,
                azimuth=azimuth
            )
            images.append(img)

        return images


def main():
    """Test visualization."""
    from data_generator import HighDimensionalDataGenerator

    print("Testing visualizer...")
    generator = HighDimensionalDataGenerator(seed=42)
    X, y = generator.generate_gaussian_clusters(n_samples=300, n_features=20, n_clusters=4)

    visualizer = MultiViewVisualizer()

    # Test 2D plot
    print("Generating 2D PCA plot...")
    img = visualizer.generate_2d_plot(X, y, method='pca', title='Test PCA')
    img.save('/home/user/temp/visual-clustering-agent/test_2d.png')
    print("Saved to test_2d.png")

    # Test multi-view grid
    print("Generating multi-view grid...")
    img = visualizer.generate_multi_view_grid(X, y)
    img.save('/home/user/temp/visual-clustering-agent/test_grid.png')
    print("Saved to test_grid.png")


if __name__ == '__main__':
    main()
