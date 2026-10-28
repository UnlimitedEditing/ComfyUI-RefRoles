# ComfyUI-RefRoles

One node, **Reference Role Prompt** (`RefRolePromptBuilder`). It turns a one-letter-per-image role code into a plain-English
preamble ahead of an edit prompt, for multi-reference image editors (FLUX 3 Image Klein, Qwen Image Edit, ...).

| Letter | Role | Word aliases |
|---|---|---|
| c | character (identity, face, hair, body) | character, person, face, identity |
| s | scene (setting, location) | scene, background, setting, location |
| o | outfit (clothing) | outfit, clothes, clothing, garment |
| y | style (palette, rendering, texture only) | style, look |
| p | pose | pose |
| i | object | object, item, prop |
| l | lighting | lighting, light |
| e | image to edit | edit, base, source |
| x - _ . | no role for this image | none, skip |

`roles = "cso"` (or `"c,s,o"`, or `"character scene outfit"`) with the prompt `put her in the park` gives:

```
Reference roles: Image 1 is the character (keep this person's identity, face, hair and body). Image 2 is the scene (use this setting, location and environment). Image 3 is the outfit (dress the subject in exactly this clothing).

put her in the park
```

`image_count` drops roles beyond the images actually present (0 = label every role given). Images are numbered in the order
given. Unknown letters count as "no role". There are no dependencies.

There is no official role syntax in FLUX 3 Image Klein; the prompt upsampler simply sees the images in order. This node
only makes the intent explicit.
