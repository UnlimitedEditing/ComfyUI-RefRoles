from nodes import build_prompt, parse_roles


def test_letters_words_and_separators():
    assert parse_roles("cso") == ["c", "s", "o"]
    assert parse_roles("c, s ,o") == ["c", "s", "o"]
    assert parse_roles("character scene outfit") == ["c", "s", "o"]
    assert parse_roles("c-s") == ["c", "x", "s"]
    assert parse_roles("") == []


def test_empty_roles_leave_prompt_untouched():
    assert build_prompt("make it night", "", 3) == "make it night"
    assert build_prompt("make it night", "xx", 2) == "make it night"


def test_labels_follow_image_order_and_respect_count():
    out = build_prompt("put her in the park", "cso", 2)
    assert out.startswith("Reference roles: Image 1 is the character")
    assert "Image 2 is the scene" in out
    assert "Image 3" not in out
    assert out.endswith("put her in the park")


def test_scene_plus_subject_adds_relight_instruction():
    out = build_prompt("go", "cs", 2)
    assert "relight the subject" in out and "the scene's lighting" in out
    assert "relight" in build_prompt("go", "so", 2)
    # a lighting image replaces the scene's lighting as the target
    assert "image 3's lighting" in build_prompt("go", "csl", 3)


def test_no_relight_without_scene_and_subject():
    assert "relight" not in build_prompt("go", "cy", 2)
    assert "relight" not in build_prompt("go", "s", 1)
    assert "relight" not in build_prompt("go", "sy", 2)


def test_skipped_image_keeps_numbering():
    out = build_prompt("go", "xs", 2)
    assert "Image 1" not in out and "Image 2 is the scene" in out
