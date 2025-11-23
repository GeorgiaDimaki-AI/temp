"""
Visual Clustering Agent - Uses vision models to analyze cluster structure
from multiple visual projections of high-dimensional data.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
import base64
import io
from PIL import Image
import json
from dataclasses import dataclass, asdict
from collections import Counter


@dataclass
class ClusterObservation:
    """Represents what the vision model observed in a single view."""
    view_type: str  # e.g., 'pca_2d', 'tsne_2d', 'pca_3d_azim_45'
    n_clusters_observed: int
    cluster_descriptions: List[str]
    confidence: str  # 'high', 'medium', 'low'
    observations: str  # Detailed description


class VisualClusteringAgent:
    """
    Agent that uses vision models to identify clusters from multiple visual projections.
    """

    def __init__(self, use_api: bool = False, api_key: Optional[str] = None):
        """
        Initialize the visual clustering agent.

        Args:
            use_api: Whether to use the Anthropic API (requires API key)
            api_key: Anthropic API key (if use_api=True)
        """
        self.use_api = use_api
        self.observations: List[ClusterObservation] = []

        if use_api:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError("anthropic package required for API mode. Install with: pip install anthropic")
        else:
            self.client = None

    def _encode_image(self, image: Image.Image) -> str:
        """Encode PIL Image to base64."""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def _analyze_image_mock(self, image: Image.Image, view_type: str) -> ClusterObservation:
        """
        Mock analysis for testing without API calls.
        Returns a simulated observation.
        """
        # Simulate different observations based on view type
        mock_responses = {
            'pca': {
                'n_clusters': 4,
                'descriptions': ['Dense cluster in upper-left', 'Scattered cluster center-right',
                               'Tight cluster lower-left', 'Elongated cluster right side'],
                'confidence': 'high',
                'observations': 'Clear separation between 4 distinct groups. Well-separated with minimal overlap.'
            },
            'tsne': {
                'n_clusters': 4,
                'descriptions': ['Compact cluster top', 'Medium density cluster left',
                               'Dense cluster bottom-right', 'Loose cluster center'],
                'confidence': 'medium',
                'observations': 'Four clusters visible but some boundary ambiguity between center groups.'
            },
            'umap': {
                'n_clusters': 4,
                'descriptions': ['Well-defined cluster upper region', 'Distinct cluster left',
                               'Clear cluster lower-right', 'Separated cluster center-right'],
                'confidence': 'high',
                'observations': 'Strong cluster structure with 4 well-separated groups.'
            }
        }

        # Choose mock response based on view type
        for key in mock_responses:
            if key in view_type.lower():
                resp = mock_responses[key]
                return ClusterObservation(
                    view_type=view_type,
                    n_clusters_observed=resp['n_clusters'],
                    cluster_descriptions=resp['descriptions'],
                    confidence=resp['confidence'],
                    observations=resp['observations']
                )

        # Default mock response
        return ClusterObservation(
            view_type=view_type,
            n_clusters_observed=3,
            cluster_descriptions=['Cluster A', 'Cluster B', 'Cluster C'],
            confidence='medium',
            observations='Multiple clusters visible with moderate separation.'
        )

    def _analyze_image_api(self, image: Image.Image, view_type: str) -> ClusterObservation:
        """
        Analyze image using Claude's vision API.

        Args:
            image: PIL Image to analyze
            view_type: Description of the view type

        Returns:
            ClusterObservation
        """
        if not self.client:
            raise ValueError("API client not initialized. Set use_api=True and provide api_key.")

        # Encode image
        image_data = self._encode_image(image)

        # Prepare prompt
        prompt = """Analyze this scatter plot visualization of high-dimensional data.

Your task is to identify distinct clusters in the data. A cluster is a group of points that are:
1. Closer to each other than to points in other groups
2. Visually separable (you can draw a boundary around them)
3. Have consistent density within the group

Please provide:
1. The number of distinct clusters you observe (be conservative - only count clear clusters)
2. Brief description of each cluster's location and characteristics
3. Your confidence level (high/medium/low) in this assessment
4. Any additional observations about cluster structure, overlap, or ambiguity

Format your response as JSON:
{
    "n_clusters": <number>,
    "cluster_descriptions": [<list of brief descriptions>],
    "confidence": "<high/medium/low>",
    "observations": "<detailed observations>"
}"""

        # Call Claude API
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        # Parse response
        response_text = message.content[0].text

        # Extract JSON from response (might be wrapped in markdown code blocks)
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()

        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback parsing
            result = {
                'n_clusters': 3,
                'cluster_descriptions': ['Unable to parse detailed response'],
                'confidence': 'low',
                'observations': response_text
            }

        return ClusterObservation(
            view_type=view_type,
            n_clusters_observed=result.get('n_clusters', 0),
            cluster_descriptions=result.get('cluster_descriptions', []),
            confidence=result.get('confidence', 'low'),
            observations=result.get('observations', '')
        )

    def analyze_view(self, image: Image.Image, view_type: str) -> ClusterObservation:
        """
        Analyze a single view of the data.

        Args:
            image: PIL Image of the visualization
            view_type: Description of the view (e.g., 'pca_2d', 'tsne_3d_azim_90')

        Returns:
            ClusterObservation
        """
        if self.use_api:
            observation = self._analyze_image_api(image, view_type)
        else:
            observation = self._analyze_image_mock(image, view_type)

        self.observations.append(observation)
        return observation

    def analyze_multiple_views(
        self,
        images: List[Tuple[Image.Image, str]]
    ) -> List[ClusterObservation]:
        """
        Analyze multiple views of the data.

        Args:
            images: List of (image, view_type) tuples

        Returns:
            List of ClusterObservations
        """
        observations = []
        for image, view_type in images:
            obs = self.analyze_view(image, view_type)
            observations.append(obs)
        return observations

    def synthesize_observations(self) -> Dict:
        """
        Synthesize all observations to reach a conclusion about cluster structure.

        Returns:
            Dictionary with synthesis results
        """
        if not self.observations:
            return {
                'conclusion': 'No observations to synthesize',
                'confidence': 'none',
                'n_clusters_predicted': 0
            }

        # Count cluster predictions
        cluster_counts = [obs.n_clusters_observed for obs in self.observations]
        count_frequency = Counter(cluster_counts)

        # Most common prediction
        most_common_n_clusters = count_frequency.most_common(1)[0][0]
        agreement_rate = count_frequency[most_common_n_clusters] / len(cluster_counts)

        # Aggregate confidence
        confidence_scores = {'high': 3, 'medium': 2, 'low': 1}
        avg_confidence_score = np.mean([confidence_scores.get(obs.confidence, 1) for obs in self.observations])

        if avg_confidence_score >= 2.5:
            overall_confidence = 'high'
        elif avg_confidence_score >= 1.5:
            overall_confidence = 'medium'
        else:
            overall_confidence = 'low'

        # Adjust confidence based on agreement
        if agreement_rate < 0.5:
            overall_confidence = 'low'

        # Build synthesis
        synthesis = {
            'n_clusters_predicted': most_common_n_clusters,
            'confidence': overall_confidence,
            'agreement_rate': agreement_rate,
            'cluster_count_distribution': dict(count_frequency),
            'n_views_analyzed': len(self.observations),
            'view_types': [obs.view_type for obs in self.observations],
            'summary': self._generate_summary(most_common_n_clusters, agreement_rate, overall_confidence)
        }

        return synthesis

    def _generate_summary(self, n_clusters: int, agreement: float, confidence: str) -> str:
        """Generate human-readable summary."""
        summary = f"Based on {len(self.observations)} visual projections, "
        summary += f"the agent predicts {n_clusters} clusters "
        summary += f"with {confidence} confidence.\n"
        summary += f"Agreement across views: {agreement*100:.1f}%\n"

        if agreement >= 0.8:
            summary += "Strong consensus across different projections."
        elif agreement >= 0.6:
            summary += "Moderate consensus, some variation in cluster perception across views."
        else:
            summary += "Low consensus - cluster structure varies significantly across projections."

        return summary

    def get_detailed_report(self) -> str:
        """Generate a detailed report of all observations."""
        report = "=" * 80 + "\n"
        report += "VISUAL CLUSTERING AGENT - DETAILED REPORT\n"
        report += "=" * 80 + "\n\n"

        for i, obs in enumerate(self.observations, 1):
            report += f"Observation {i}: {obs.view_type}\n"
            report += f"  Clusters observed: {obs.n_clusters_observed}\n"
            report += f"  Confidence: {obs.confidence}\n"
            report += f"  Descriptions:\n"
            for j, desc in enumerate(obs.cluster_descriptions, 1):
                report += f"    {j}. {desc}\n"
            report += f"  Notes: {obs.observations}\n"
            report += "-" * 80 + "\n"

        synthesis = self.synthesize_observations()
        report += "\nSYNTHESIS:\n"
        report += synthesis['summary']
        report += f"\n\nDistribution of cluster predictions: {synthesis['cluster_count_distribution']}\n"

        return report

    def save_observations(self, filepath: str):
        """Save observations to JSON file."""
        data = {
            'observations': [asdict(obs) for obs in self.observations],
            'synthesis': self.synthesize_observations()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Test the visual clustering agent."""
    print("Testing Visual Clustering Agent (Mock Mode)...")

    # Create mock agent (no API calls)
    agent = VisualClusteringAgent(use_api=False)

    # Simulate analyzing multiple views
    # In real use, these would be actual images
    mock_image = Image.new('RGB', (800, 600), color='white')

    views = [
        (mock_image, 'pca_2d'),
        (mock_image, 'tsne_2d'),
        (mock_image, 'umap_2d'),
        (mock_image, 'pca_3d_azim_0'),
        (mock_image, 'pca_3d_azim_90'),
    ]

    print(f"\nAnalyzing {len(views)} different views...")
    observations = agent.analyze_multiple_views(views)

    print("\nGenerating synthesis...")
    synthesis = agent.synthesize_observations()

    print("\n" + agent.get_detailed_report())

    print("\nTest complete!")


if __name__ == '__main__':
    main()
