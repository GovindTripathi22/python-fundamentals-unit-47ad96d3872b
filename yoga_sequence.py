import sys

# Every class starts and ends with these two poses.
WARM_UP = "Cat-Cow"
COOL_DOWN = "Child's Pose"

# The middle of the class, already in a logical order:
# standing poses first, then floor poses.
POSES = [
    {"name": "Downward Dog", "areas": ["hips", "shoulders", "hamstrings", "gentle"]},
    {"name": "Warrior II", "areas": ["hips", "legs"]},
    {"name": "Tree Pose", "areas": ["legs", "balance"]},
    {"name": "Eagle Arms", "areas": ["shoulders"]},
    {"name": "Boat Pose", "areas": ["core"]},
    {"name": "Cobra", "areas": ["back", "gentle"]},
    {"name": "Seated Forward Fold", "areas": ["hamstrings", "back", "gentle"]},
]

# Used when the instructor gives no focus areas at all.
DEFAULT_FOCUS = ["gentle"]


def parse_focus(text):
    """Turn 'Hips, core' into ['hips', 'core'], dropping empty pieces."""
    focus = []
    for piece in text.split(","):
        piece = piece.strip().lower()
        if piece:
            focus.append(piece)
    return focus


def build_sequence(text):
    """Yield pose names one by one: warm-up, matching poses, cool-down."""
    focus = parse_focus(text)
    if not focus:
        focus = DEFAULT_FOCUS

    matches = lambda pose: any(area in pose["areas"] for area in focus)

    yield WARM_UP
    for pose in POSES:
        if matches(pose):
            yield pose["name"]
    yield COOL_DOWN


def main(args):
    text = ",".join(args)
    for name in build_sequence(text):
        print(name)


if __name__ == "__main__":
    main(sys.argv[1:])