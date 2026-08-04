# 춘천닭갈비 — Google AI Studio 이미지 생성 프롬프트

## 사용법 (AI Studio)
1. **aistudio.google.com** 접속 → 좌측에서 이미지 생성 가능한 모델 선택
   - **Gemini 2.5 Flash Image ("Nano Banana")** — 내 손그림을 첨부해 img2img (자세·디자인 유지에 최고, 캐릭터 일관성 좋음). **← 추천**
   - 또는 **Imagen 4** — 텍스트만으로 고퀄 생성
2. **내 손그림 파일을 첨부**하고 아래 프롬프트를 입력
3. 배경은 **단색(밝은 회색)** 으로 뽑기 → 배경 제거가 깔끔함
4. 마음에 드는 컷이 나오면 `characters/dakgalbi/ref/` 폴더에 저장

---

## 메인 프롬프트 (영어 — 이미지 생성은 영어가 결과 더 좋음)

```
Use the attached sketch as the exact pose and design reference. Keep the same
pose, proportions, and all features — but render it as a dimensional, fully
3D-shaded stylized fighting-game character (NOT flat, NOT a line drawing).

Subject: a muscular humanoid ROOSTER WARRIOR — a buff human bodybuilder's body
with an angry rooster's head. Theme: "Chuncheon Dakgalbi" (Korean spicy grilled
chicken) — a hot-blooded fiery brawler.

Head: fierce rooster head, large floppy RED COMB on top, sharp yellow beak
slightly open in a battle snarl, red wattle under the chin, furious eyes with
sharp V-shaped angry brows, cream-white feathered face, a ruff of jagged golden
neck feathers (hackle) around the collar.

Body: broad muscular chest, defined pecs and six-pack abs, thick powerful arms
and legs, warm reddish-tan muscular skin. Both arms raised in an aggressive
fighting pose — RIGHT hand a clenched fist, LEFT hand an open clawed talon-hand
(as in the sketch). A jagged RED FEATHER KILT/BELT around the waist. Legs end in
YELLOW three-toed CHICKEN TALON feet.

Style: semi-realistic stylized 3D like a modern fighting game (Street Fighter 6 /
Overwatch cinematic), strong volumetric shading, dramatic rim lighting, clear
depth and form, bold clean silhouette, high face detail, fiery red-orange palette.

Framing for game use: FULL BODY head-to-toe, character centered and vertical,
plain flat LIGHT-GRAY studio background, soft ground shadow, even key light.
No text, no logo, no border. High resolution.
```

## 한국어 요약 (참고용)
> 첨부한 손그림을 자세·비율·특징 그대로 유지하되, **평면 선화가 아니라 입체적으로 3D 셰이딩된
> 격투게임 캐릭터**로 렌더. 근육질 인간 몸 + 성난 수탉 머리(큰 붉은 볏·부리·와틀·V자 눈썹),
> 한 손 주먹·한 손 갈퀴발톱, 붉은 깃털 치마, 노란 닭발톱 발. 춘천닭갈비=매운 불의 파이터
> 컨셉(붉은/주황). 스파6·오버워치급 입체 셰이딩+림라이트. **전신·중앙정렬·단색 밝은회색 배경**.

---

## 게임 적용을 위한 필수 조건 (꼭 지킬 것)
- **전신**이 다 나오게 (머리 끝~발끝, 잘리지 않게)
- **정면·수직·중앙 정렬**
- **단색 배경**(밝은 회색 권장) → 배경 제거 쉬움
- **고해상도** (1024px 이상)

## 다음 단계 (동작용)
기본 이미지가 확정되면, **같은 캐릭터·같은 스타일**로 자세만 바꿔 추가 생성:
- `same character, same style, now in a neutral idle fighting stance`
- `...throwing a straight punch`, `...doing a flying kick`, `...breathing fire`
→ 이렇게 뽑은 컷들을 스프라이트로 묶어 애니메이션.
