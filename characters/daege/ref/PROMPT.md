# 속초 대게 — Gemini 생성 프롬프트 (집게 파이터)

## 컨셉
- 도시: 속초 (명물: 대게 snow crab)
- 아키타입: 집게 그래플러 / 리치형
- 스타일: 춘천닭갈비와 동일한 semi-realistic 3D 격투게임 아트 (일관성)

## 메인 프롬프트 (Gemini, 새 채팅)
```
A full-body semi-realistic stylized 3D fighting-game character, front view, standing on a plain flat LIGHT-GRAY studio background. The character is a muscular humanoid CRAB WARRIOR — the mascot fighter of Sokcho, Korea (famous for snow crab).

Body: athletic muscular human-like torso and legs, with a hard vivid ORANGE-RED CRAB SHELL armoring the chest, shoulders and back (spiny snow-crab carapace), and a cream-white armored belly.

Head: a fierce crab-warrior head — an orange-red crab carapace helmet with two short eye-stalks and glaring dark eyes, small mandibles, an aggressive fighting expression.

Arms: the RIGHT arm ends in a GIANT oversized orange-red crab PINCER/claw (his signature weapon), the LEFT arm ends in a smaller crab pincer; thick spiny crab-leg accents on the shoulders.

Legs: powerful muscular legs ending in pointed crab-clawed feet.

Theme: Sokcho snow crab — vivid orange-red carapace, cream underside, a coastal sea warrior, a grappler with long reach.

Style: semi-realistic stylized 3D like a modern fighting game (Street Fighter 6 / Overwatch), strong volumetric shading, dramatic rim lighting, dimensional and NOT flat, bold clean silhouette, high face/claw detail. Full body head-to-toe, centered, plain flat light-gray studio background, soft ground shadow. High resolution, no text.
```

## 이후
- 배경제거: `process_all.py` 방식 재사용
- 동작 세트(idle,walk,punch,kick,jump,special,guard,crouch,hit,ko) → 원본 대화 이어서 "same character, change only pose"
- 필살기: 대게라 물/거품 or 집게 강타 이펙트
