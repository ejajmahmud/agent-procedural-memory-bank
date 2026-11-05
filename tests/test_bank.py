"""Tests for agent-procedural-memory-bank."""
import unittest
from agent_procedural_memory_bank.bank import ProceduralBank


class TestProceduralBank(unittest.TestCase):
    def setUp(self):
        self.bank = ProceduralBank()

    def test_recipe_instantiation(self):
        self.bank.register_recipe(
            "docker_build",
            [{"tool": "docker", "args": {"tag": "$tag", "dockerfile": "Dockerfile"}}],
            ["tag"]
        )
        recipe = self.bank.get_recipe("docker_build")
        self.assertIsNotNone(recipe)
        plan = recipe.instantiate({"tag": "v1.2.0"})
        self.assertEqual(plan[0]["args"]["tag"], "v1.2.0")

    def test_success_tracking(self):
        self.bank.register_recipe("backup", [{"tool": "rsync", "args": {}}], [])
        r = self.bank.get_recipe("backup")
        r.record_result(True)
        r.record_result(True)
        r.record_result(False)
        self.assertAlmostEqual(r.success_rate(), 2/3)


if __name__ == "__main__":
    unittest.main()
