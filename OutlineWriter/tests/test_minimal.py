import unittest
from content_generator import ContentGenerator

class TestMinimalContent(unittest.TestCase):
    def test_minimal_input(self):
        generator = ContentGenerator()
        result = generator.generate_minimal_content(
            problem="Bankers forgetting key skills",
            goal="Create structured training program"
        )
        self.assertIn("title", result)
        self.assertIn("main_point", result)
        self.assertGreaterEqual(len(result["supporting_points"]), 1) 