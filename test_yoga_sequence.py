import io
import subprocess
import sys
import types
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from yoga_sequence import build_sequence, main, parse_focus


class ParseFocusTests(unittest.TestCase):
    def test_splits_on_commas(self):
        self.assertEqual(parse_focus("hips,core"), ["hips", "core"])

    def test_ignores_spaces_case_and_empty_pieces(self):
        self.assertEqual(parse_focus(" Hips , ,CORE,"), ["hips", "core"])

    def test_empty_text_gives_empty_list(self):
        self.assertEqual(parse_focus(""), [])


class BuildSequenceTests(unittest.TestCase):
    def test_is_a_generator(self):
        self.assertIsInstance(build_sequence("hips"), types.GeneratorType)

    def test_yields_lazily_one_pose_at_a_time(self):
        poses = build_sequence("core")
        self.assertEqual(next(poses), "Cat-Cow")
        self.assertEqual(next(poses), "Boat Pose")
        self.assertEqual(next(poses), "Child's Pose")
        with self.assertRaises(StopIteration):
            next(poses)

    def test_example_from_the_task(self):
        self.assertEqual(
            list(build_sequence("hips,core")),
            ["Cat-Cow", "Downward Dog", "Warrior II", "Boat Pose", "Child's Pose"],
        )

    def test_only_matching_poses_in_the_middle(self):
        middle = list(build_sequence("shoulders"))[1:-1]
        self.assertEqual(middle, ["Downward Dog", "Eagle Arms"])

    def test_pose_matching_two_focus_areas_appears_once(self):
        poses = list(build_sequence("hips,shoulders"))
        self.assertEqual(poses.count("Downward Dog"), 1)

    def test_no_focus_gives_gentle_full_body_sequence(self):
        self.assertEqual(
            list(build_sequence("")),
            ["Cat-Cow", "Downward Dog", "Cobra", "Seated Forward Fold", "Child's Pose"],
        )

    def test_blank_focus_counts_as_no_focus(self):
        self.assertEqual(list(build_sequence(" , ")), list(build_sequence("")))

    def test_always_starts_with_warm_up_and_ends_with_cool_down(self):
        for text in ["", "hips", "core,back", "toes"]:
            poses = list(build_sequence(text))
            self.assertEqual(poses[0], "Cat-Cow")
            self.assertEqual(poses[-1], "Child's Pose")

    def test_unknown_focus_gives_only_warm_up_and_cool_down(self):
        self.assertEqual(list(build_sequence("toes")), ["Cat-Cow", "Child's Pose"])


class MainTests(unittest.TestCase):
    def run_main(self, args):
        out = io.StringIO()
        with redirect_stdout(out):
            main(args)
        return out.getvalue()

    def test_prints_one_pose_per_line(self):
        self.assertEqual(
            self.run_main(["hips,core"]),
            "Cat-Cow\nDownward Dog\nWarrior II\nBoat Pose\nChild's Pose\n",
        )

    def test_separate_words_are_joined_as_focus_areas(self):
        self.assertEqual(self.run_main(["hips", "core"]), self.run_main(["hips,core"]))

    def test_no_arguments_prints_default_sequence(self):
        self.assertEqual(
            self.run_main([]),
            "Cat-Cow\nDownward Dog\nCobra\nSeated Forward Fold\nChild's Pose\n",
        )

    def test_command_line_entry_point(self):
        script = Path(__file__).with_name("yoga_sequence.py")
        result = subprocess.run(
            [sys.executable, str(script), "hips", "core"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            result.stdout,
            "Cat-Cow\nDownward Dog\nWarrior II\nBoat Pose\nChild's Pose\n",
        )


if __name__ == "__main__":
    unittest.main()