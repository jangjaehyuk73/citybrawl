# 속초 대게 — 포즈 생성 프롬프트 (AI Studio, Nano Banana 2 `gemini-3.1-flash-image`)

## 방법 (검증됨)
- 모델: **Nano Banana 2** (`aistudio.google.com/prompts/new_chat?model=gemini-3.1-flash-image`)
- 우측 **Aspect ratio = 3:4**
- **포즈마다 "새 채팅"으로 fresh 생성** (이전 이미지 참조하는 편집은 서버 오류가 잦음 → 매번 새로 시작)
- 에러("An internal error"/"permission denied") 나면 **재시도**(재생성 ✦) — 대략 절반 성공
- 성공 이미지 → 다운로드(⬇) → `~/Downloads/daege_<pose>.png` 로 저장 (예: `daege_punch.png`)
- 다 되면 프로젝트에서: `cd characters/daege && python3 ingest.py`

## 공통 접두 (매 프롬프트 앞에 그대로)
> A STYLIZED 3D CARTOON fighting-game character, front view, full body head-to-toe, centered on a plain flat LIGHT-GRAY studio background. The character is a fierce ORANGE-RED SNOW CRAB warrior: a round spiny orange-red carapace body covered in bumpy spikes, a wide fanged cartoon mouth, two big orange eyes on short eye-stalks, TWO EQUALLY-LARGE symmetrical oversized orange-red pincer claws, and several pointed jointed crab legs. Clean cartoon illustration style with bold dark outlines, smooth cel shading, vibrant saturated colors, NOT photorealistic. CRITICAL FRAMING: ZOOM OUT so the ENTIRE crab — including both fully-extended pincers and every leg — is completely visible with generous empty margin/padding on ALL FOUR sides; nothing is cropped or touching the image edges; the character sits small and fully contained inside the frame. Plain flat light-gray background, soft ground shadow, no text, no watermark.

**비율 팁**: 옆으로 뻗는 **punch·kick·special** 은 우측 Aspect ratio 를 **1:1** 로 (가로 여유↑). 나머지는 3:4 유지. (게임이 크기 자동 정규화하므로 비율 달라도 OK)

## 포즈별 (공통 접두 + 아래 "POSE:" 문장)

**punch** (`daege_punch.png`)  ※옆으로 뻗기
> POSE: throwing a powerful straight PUNCH TO THE SIDE — the body faces the viewer but it thrusts ONE giant pincer claw straight out HORIZONTALLY to its RIGHT (screen-right), arm fully extended sideways as if striking an enemy standing beside it; the other pincer pulled back. Roaring, eyes glaring wide. The punching claw reaches out to the SIDE, NOT toward the viewer.

**kick** (`daege_kick.png`)  ※둘째 다리로 옆차기, 몸통 비스듬히 듦
> POSE: a strong KICK TO THE RIGHT — the crab TILTS its whole body diagonally, lifting and leaning to one side for leverage, and swings its SECOND leg (the second leg from the front) out, extended straight HORIZONTALLY to its RIGHT (screen-right) to kick an enemy standing beside it. The other legs plant and brace, both big pincers raised for balance, roaring with mouth open, eyes wide. The kicking leg reaches to the SIDE, body clearly tilted at an angle.

**jump** (`daege_jump.png`)
> POSE: springing JUMP in mid-air — legs tucked and compact under the body, both pincers raised, whole body coiled and airborne, eyes wide.

**special** (`daege_special.png`)  ※옆으로 발사
> POSE: launching its SIGNATURE ATTACK TO THE SIDE — the body faces the viewer but both giant pincers thrust out HORIZONTALLY to its RIGHT (screen-right) as if firing them at an enemy standing beside it, body braced and leaning right, roaring fiercely. (keep both claws attached in this image)

**guard** (`daege_guard.png`)
> POSE: DEFENSIVE GUARD — both big pincers crossed in front of the face and chest like a shield, shoulders hunched, body compact, eyes narrowed.

**crouch** (`daege_crouch.png`)
> POSE: CROUCHING low to the ground — legs deeply bent, body pulled close to the floor, both pincers tucked in front, eyes narrowed. (keep the whole body inside the frame)

**hit** (`daege_hit.png`)
> POSE: taking a HIT — recoiling backward, body off-balance, one pincer flung out to the side, mouth open in pain, eyes bulging.

**ko** (`daege_ko.png`)
> POSE: KNOCKED OUT lying flat on its back, HORIZONTAL on the ground, belly up, legs and pincers sprawled limp, eyes replaced with dizzy spirals. (the crab is lying down horizontal, NOT standing)

## 필살기 투사체 — 분리된 집게 (`daege_claw.png`)
> A single detached ORANGE-RED crab PINCER CLAW, side profile, isolated and centered on a plain flat LIGHT-GRAY studio background. Clean cartoon illustration style with bold dark outlines, smooth cel shading, vibrant colors, NOT photorealistic, spiky and menacing, the open claw pointing to the right as if hurtling through the air. No text, no watermark, no arm, just the claw.

---
※ idle 은 `ref/base_new.jpg`(승인본)로 이미 게임 반영됨. walk 도 확보됨. 남은 8포즈 + claw 를 위 방식으로.
