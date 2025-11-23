"""
Visual Clustering Agent - Using vision models for clustering analysis.
"""
__version__ = '0.1.0'

from .data_generator import HighDimensionalDataGenerator
from .visualizer import MultiViewVisualizer
from .visual_clustering_agent import VisualClusteringAgent
from .traditional_clustering import TraditionalClusteringBaseline
from .evaluation import ClusteringEvaluator

__all__ = [
    'HighDimensionalDataGenerator',
    'MultiViewVisualizer',
    'VisualClusteringAgent',
    'TraditionalClusteringBaseline',
    'ClusteringEvaluator',
]
