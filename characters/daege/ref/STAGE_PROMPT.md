# 속초 대게 스테이지 — 영덕항(강구항) 배경 생성 프롬프트

춘천닭갈비 골목 배경(`characters/dakgalbi/stage/chuncheon.png`)과 **같은 톤**:
황혼 노을 + 따뜻한 네온/등불 글로우 + 반실사 게임 시네마틱 + 중앙 소실점 대칭 구도 + 하단 바닥 밴드.
무대는 춘천 골목 → **영덕 강구항 대게거리(항구)** 로 교체. 캐릭터는 넣지 않음(순수 배경).

## 사용법 (AI Studio)
- 모델: **Nano Banana / Imagen 4** (텍스트 생성이면 Imagen 4 권장)
- **Aspect ratio = 16:9**
- 결과물 → `characters/daege/stage/yeongdeok.png` 로 저장 (필요시 `yeongdeok_muted.png` 로 채도 낮춘 버전도)

## 메인 프롬프트 (영어)

```
A 2D fighting-game STAGE BACKGROUND, 16:9, cinematic wide shot, NO characters, NO UI, NO text overlay.

Scene: a cozy Korean harbor seafood alley at dusk — "Yeongdeok Ganggu Port snow-crab street".
Rows of two- and three-story wooden seafood restaurants line both sides of a harbor quay, receding
toward a central vanishing point where a calm reflective SEA opens up under a dramatic sunset.

Mood & tone (match reference): warm nostalgic dusk. Deep CRIMSON-to-ORANGE sunset sky fading to indigo
with soft clouds and the first faint stars; distant low coastal hills silhouetted on the horizon.
Everything lit by that warm glow plus the shops' own lights.

Signage & lights: glowing warm NEON signs and backlit boards on the storefronts advertising crab and
seafood ("영덕대게", "대게", "회", "물회") with little CRAB pictograms; red paper LANTERNS hung along the
eaves; strings of small warm bulb lights criss-crossing overhead across the alley; light spilling warm
and golden from restaurant windows with the silhouettes of diners inside.

Harbor details: small fishing boats and trawlers moored along the quay with stacked CRAB TRAPS/POTS,
buoys, and coiled ropes; a red-and-white LIGHTHOUSE at the tip of a stone breakwater off to one side in
the mid-distance; a big friendly stylized CRAB statue/landmark glowing near the waterfront; neon and
sunset colors REFLECTING on the wet harbor water. Gentle STEAM rising from boiling crab pots at the
storefronts; soft warm haze and glowing bokeh embers in the air.

Foreground (fighter floor): a flat, wide, empty STONE/CONCRETE HARBOR QUAY pavement running straight
across the bottom of the frame — slightly wet with faint puddle reflections, a bollard and coiled rope
at each lower corner as framing props. The CENTER of the stage is kept OPEN and unobstructed so two
fighters can stand and move there.

Composition: symmetrical, shops on both left and right converging to the central sea/lighthouse vanishing
point (like a stage backdrop); clear horizontal ground band across the lower ~25% of the image; balanced
depth, strong atmospheric perspective.

Style: semi-realistic stylized ILLUSTRATION, modern fighting-game / anime cinematic stage art
(Street Fighter 6 / KOF stage vibe, Ghibli-warm color grade), rich volumetric lighting, warm
red-orange + neon palette, high detail, painterly but clean. No characters, no watermark, no logo, no border.
```

## 한국어 요약
> 캐릭터 없는 **16:9 격투 스테이지 배경**. 황혼의 **영덕 강구항 대게거리** — 양옆으로 목조 해산물 가게가
> 늘어서 중앙 바다(멀리 등대·소실점)로 모이는 대칭 구도. 붉은-주황 노을 하늘, 따뜻한 네온 대게 간판·붉은
> 종이등·꼬마전구 줄, 창밖으로 새는 손님 실루엣. 항구엔 정박한 어선·대게통발·부표·밧줄, 방파제 끝 홍백 등대,
> 물가의 큰 대게 조형물, 수면에 반사되는 네온·노을, 냄비에서 오르는 김과 은은한 안개·보케. 하단엔 넓고 평평한
> **젖은 돌 부두 바닥**(양쪽 하단 코너에 볼라드+밧줄), 가운데는 캐릭터가 서도록 비움. 반실사 게임 시네마틱 스타일.

## 게임 적용 필수 조건
- **16:9**, 캐릭터·텍스트 UI 없음(순수 배경)
- **중앙은 비우고**, 하단 ~25% 는 평평한 바닥 밴드(발 딛는 곳)
- 좌우 대칭 + 중앙 소실점(바다/등대)으로 깊이감
- 춘천 배경과 **동일 톤**: 황혼 노을 + 따뜻한 네온/등불 글로우 + 반실사 일러스트
- 고해상도. 원하면 채도 낮춘 `_muted` 버전도 뽑아 캐릭터가 튀게.
