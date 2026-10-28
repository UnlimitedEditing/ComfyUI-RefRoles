import re

# One letter per reference image, in the order the images are given (image 1 = the source/first image).
ROLES = {
    "c": ("the character", "keep this person's identity, face, hair and body"),
    "s": ("the scene", "use this setting, location and environment"),
    "o": ("the outfit", "dress the subject in exactly this clothing"),
    "y": ("the style", "match its colour palette, rendering, medium and texture, but not its subject matter"),
    "p": ("the pose", "copy this body pose and camera angle, not the person or the clothing"),
    "i": ("an object", "include this item"),
    "l": ("the lighting", "match its light direction, colour and mood"),
    "e": ("the image to edit", "keep its composition and change only what is asked"),
}
SKIP = set("x-_.")

WORDS = {
    "character": "c", "person": "c", "face": "c", "identity": "c",
    "scene": "s", "background": "s", "setting": "s", "location": "s",
    "outfit": "o", "clothes": "o", "clothing": "o", "garment": "o",
    "style": "y", "look": "y",
    "pose": "p",
    "object": "i", "item": "i", "prop": "i",
    "lighting": "l", "light": "l",
    "edit": "e", "base": "e", "source": "e",
    "none": "x", "skip": "x",
}


def parse_roles(roles):
    """'cso' / 'c,s,o' / 'character scene outfit' -> ['c', 's', 'o']. Unknown letters count as no role."""
    out = []
    for tok in re.split(r"[\s,;|+]+", (roles or "").strip().lower()):
        if not tok:
            continue
        if tok in WORDS:
            out.append(WORDS[tok])
        else:
            out.extend(ch if ch in ROLES else "x" for ch in tok)
    return out


def build_prompt(prompt, roles, image_count=0):
    letters = parse_roles(roles)
    if image_count > 0:
        letters = letters[:image_count]
    parts = []
    for n, ch in enumerate(letters, 1):
        if ch in ROLES:
            label, rule = ROLES[ch]
            parts.append(f"Image {n} is {label} ({rule}).")
    if not parts:
        return prompt
    return "Reference roles: " + " ".join(parts) + integration(letters) + "\n\n" + prompt


SUBJECT_ROLES = set("coip")


def integration(letters):
    """A scene combined with a subject must be relit, not pasted in: the subject keeps its identity but not its light."""
    if "s" not in letters or not SUBJECT_ROLES & set(letters):
        return ""
    src = f"image {letters.index('l') + 1}'s lighting" if "l" in letters else "the scene's lighting"
    return (
        " Integrate the subject into the scene as if photographed there: relight the subject and everything they"
        f" wear or hold to match {src}, with its ambient and diffused light, key direction, colour temperature and"
        " hue, the same shadows, rim light, reflections and atmosphere (rain, haze, glow from practical lights)."
        " The subject keeps their identity but not their original lighting or background colour cast; grade skin,"
        " fabric and highlights to the scene's tones."
    )


class RefRolePromptBuilder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "roles": ("STRING", {"default": "", "tooltip": "One letter per image in order: c character, s scene, o outfit, y style, p pose, i object, l lighting, e image to edit, x none. Words also work: 'character scene outfit'."}),
                "image_count": ("INT", {"default": 0, "min": 0, "max": 10, "tooltip": "Images actually present; roles beyond this are dropped. 0 labels every role given."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build"
    CATEGORY = "text"

    def build(self, prompt, roles, image_count):
        return (build_prompt(prompt, roles, image_count),)


NODE_CLASS_MAPPINGS = {"RefRolePromptBuilder": RefRolePromptBuilder}
NODE_DISPLAY_NAME_MAPPINGS = {"RefRolePromptBuilder": "Reference Role Prompt"}
