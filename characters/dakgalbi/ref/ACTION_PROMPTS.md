# 춘천닭갈비 — 동작별 생성 프롬프트 세트

## 공통 규칙 (일관성 유지 — 매 컷 앞에 붙일 것)
> **첫 생성 이미지(기본 정면)를 참조로 첨부**하고 아래 문장을 머리말로 사용:

```
Keep the EXACT same character, same art style, same colors, same 3D shading and
rim lighting as the reference image (muscular humanoid rooster fighter, red comb,
cream face, wooden belt, red feather kilt, yellow talon feet). Only change the
POSE and camera as described. Full body head-to-toe, centered, plain flat
light-gray studio background, soft ground shadow, high resolution, no text.
```

**중요 — 대전용 시점:** 게임에서 서로 마주 보므로 **¾ 측면(3/4 side view), 오른쪽을 향하도록**. 모든 컷을 같은 방향(오른쪽 바라봄)으로 통일.
> 문장: `Camera: 3/4 side view, the character facing to the RIGHT.`

---

## 1. idle (기본 대기)
```
Pose: relaxed but ready fighting stance, both fists up near chest in a boxer's
guard, weight balanced, slight lean forward, alert glare. Feet shoulder-width.
Camera: 3/4 side view, facing RIGHT.
```

## 2. walk (전진)
```
Pose: mid-stride walking forward, one leg lifted forward, arms in a low guard,
leaning into the step, aggressive forward momentum.
Camera: 3/4 side view, facing RIGHT.
```

## 3. punch (주먹치기)
```
Pose: explosive straight punch — right fist thrust fully forward toward the right,
body rotated into the punch, other fist pulled back to the chin, back leg braced.
Dynamic, powerful.
Camera: 3/4 side view, facing RIGHT.
```

## 4. kick (발차기)
```
Pose: high roundhouse kick to the right, one leg extended horizontally with the
yellow talon foot leading, arms out for balance, supporting leg bent. Explosive.
Camera: 3/4 side view, facing RIGHT.
```

## 5. special — 불 필살기 (불판 화염)
```
Pose: both hands thrust forward unleashing a blast of FIRE to the right, mouth
open in a battle cry, glowing fiery energy and flames around the fists, body
braced and leaning into the blast. Epic finishing-move energy.
Camera: 3/4 side view, facing RIGHT.
```

## 6. hit (피격)
```
Pose: recoiling backward from a hit, head snapped back, one arm flailing up,
staggering off balance, pained expression.
Camera: 3/4 side view, facing RIGHT.
```

## 7. ko (넉다운)
```
Pose: knocked out, fallen flat on his back on the ground, limbs sprawled, dizzy
X-eyes, comb drooping. Lying down, seen from a slightly high angle.
Camera: side view.
```

---

## 팁
- 한 번에 한 자세씩, **기본 이미지를 매번 첨부**해 캐릭터를 고정.
- 색·근육·볏이 달라지면 "match the reference exactly, same character" 를 강조해 재생성.
- 잘 나온 컷을 `characters/dakgalbi/ref/` 에 `idle.png`, `punch.png` … 이름으로 저장 → 내가 배경 제거·정렬·스프라이트 조립.
