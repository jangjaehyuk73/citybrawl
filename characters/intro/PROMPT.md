# 도시명물 대전 — 인트로 영상 프롬프트 (Gemini Veo)

약 8~10초 오프닝 시네마틱. 3캐릭터(춘천닭갈비·속초대게·대전소보로) 등장.

## 사용법
- 도구: **Google Veo** (Gemini 앱 또는 AI Studio의 Video Generation)
- **Aspect ratio 16:9**, 길이 최대(보통 8초). 10초 원하면 2컷 생성해 이어붙이기.
- **캐릭터 일관성(첨부 시드)**: image-to-video로 하면 우리 캐릭터 그대로 살아남.
  - `intro/intro_keyart_bg.png` — **배경(3개 도시) 포함** → 배경까지 애니메이션(추천)
  - `intro/intro_keyart.png` — 무지 배경(어두운 극적 + 이펙트 위주)
  - 첨부 없이 text-to-video 하면 Veo가 지도→도시 장면을 새로 생성(장면전환 풍부, 캐릭터는 근사치).
- 결과 mp4를 `characters/intro/intro.mp4` 로 저장 → 게임 시작 시 재생 연결(내가 붙여줌).

## 메인 프롬프트 (영어, text-to-video)

```
An explosive 8-second cinematic INTRO for a 2D fighting game titled "도시명물 대전" (City Specialty Brawl),
in vibrant anime / fighting-game key-art style (Street Fighter / King of Fighters opening vibe): bold clean
outlines, semi-realistic stylized 3D cartoon shading, dramatic rim lighting, motion blur, speed lines, lens
flares, high energy, 16:9.

Three larger-than-life Korean city mascot fighters:
1) ROOSTER WARRIOR (Chuncheon dakgalbi) — a muscular human bodybuilder body with a fierce rooster head (red
   comb, beak), a red feather skirt; throws a blazing straight PUNCH wreathed in fire.
2) GIANT ORANGE-RED CRAB WARRIOR (Sokcho snow crab) — spiky round shell, two huge symmetrical pincer claws,
   glaring eyestalks, roaring; snaps its claws unleashing a blast of water and bubbles.
3) HULKING FRIED-BREAD MUSCLE WARRIOR (Daejeon soboro) — head is a round golden fried streusel bun with two
   peanut eyes, an enormous crispy golden-crust bodybuilder body, bright yellow trunks; slams a giant fist
   sending a burst of hot bread crumbs and peanuts flying.

Shot sequence (fast, punchy cuts, dynamic sweeping camera):
- Open on a stylized glowing map of South Korea at night, three neon pins igniting on Chuncheon, Sokcho and
  Daejeon; camera swoops down toward the map.
- Cut to each fighter bursting into frame one by one with their signature action — flaming punch, water claw
  snap, crumb-and-peanut fist slam — each hit landing with a bright impact flash, shockwave and speed lines.
- Final hero shot: the three fighters land together in a dramatic line-up, glaring at camera, as a bold
  metallic-gold title "도시명물 대전" SMASHES onto the screen with a shockwave and sparks.

Mood: epic, exciting, fun. Rich warm color grade, deep contrast, glowing embers and particles in the air.
Only on-screen text is the final title "도시명물 대전". No watermark, no logo, no captions.
```

## 짧은 변형 (첨부 키아트로 image-to-video 할 때)
```
Animate this key-art into an epic 8-second fighting-game intro: the three mascot fighters lunge and throw
their signature attacks (rooster's fire punch, crab's water claw snap, bread-warrior's crumb fist slam) with
impact flashes, speed lines, motion blur, flying embers and particles; fast dynamic camera push-in; end on a
heroic three-fighter pose as a bold metallic-gold title "도시명물 대전" smashes in with a shockwave. Vibrant
anime fighting-game style, 16:9, high energy. No extra text besides the title.
```

## ★추천: 컬러풀 추상 에너지 배경 버전 (첨부: `intro/intro_keyart_energy.png`)
도시 배경 대신 **파이팅 에너지 추상 그래픽** 배경. 3캐릭터가 한 프레임에 담겨 있어 첨부 1장으로 OK.
```
Animate this fighting-game key-art into an explosive 8-second intro. Keep the THREE mascot fighters exactly
as shown. They lunge and unleash their signature attacks — the rooster warrior's flaming punch, the crab
warrior's water-blast claw snap, the golden fried-bread warrior's crumb-and-peanut fist slam — with big
impact flashes and shockwaves. BACKGROUND: a COLORFUL ABSTRACT ENERGY graphic, NO realistic scenery — a
vivid radial burst of gold→orange→magenta→purple, pulsing sunburst rays, expanding shockwave rings, bold
comic speed lines, glowing particles and embers all bursting outward with fighting energy. Fast dynamic
camera push-in with shake on each impact, motion blur, lens flares. End on a heroic three-fighter pose as a
bold metallic-gold title "도시명물 대전" smashes onto screen with a shockwave and sparks. Vibrant anime
fighting-game splash style, 16:9, extremely high energy. No extra text besides the title.
```

## ★★ 최종: 나노바나나 키아트 첨부 + 음악 포함 (Veo 3 권장)
나노바나나로 만든 3캐릭터 에너지 키아트를 첨부하고 아래로 요청. Veo 3면 음악+효과음까지 생성됨.
```
Animate this fighting-game key-art into an explosive 8-second intro. Keep the three characters EXACTLY as
shown (rooster warrior, crab warrior, golden fried-bread warrior). Bring it to life: their signature attacks
COLLIDE in the center — the rooster's flaming fist, the crab's water-blast claws, the bread warrior's
crumb-and-peanut fist — smashing together in a huge burst of fire, water and golden crumbs with bright
impact flashes and shockwaves. The colorful abstract energy background pulses and radiates: sunburst rays
spin, white shockwave rings expand outward, comic speed lines streak, embers and particles fly. Fast dynamic
camera: quick push-in toward the central clash with a screen shake on the big impact, subtle parallax. End on
a heroic freeze of the three fighters mid-clash as a bold metallic-gold title "도시명물 대전" smashes onto the
screen with a shockwave and sparks.
AUDIO: an intense, exciting, high-energy battle-intro MUSIC — driving electronic-rock / orchestral hybrid,
pounding drums, a heroic brass-and-synth hook building to a big hit on the final title; layered with punchy
impact SFX (whoosh, fire crackle, water splash, deep boom on the title reveal).
Style: vibrant anime fighting-game splash, bold outlines, dramatic lighting, motion blur, lens flares, 16:9,
extremely high energy. No extra text besides the title.
```
- **Veo 2**(오디오 없음)면 위에서 AUDIO 문단만 빼고 뽑은 뒤, 게임 BGM(우리 audio.js)이나 별도 음악을 입히면 됨.
- 10초 원하면 8초 2컷(예: ①맵/등장 ②클래시+타이틀) 이어붙이기.

## 게임 연결(나중에)
mp4가 준비되면 `game.html`에 인트로 씬을 추가:
- 페이지 로드 시 풀스크린 `<video>` 재생(약 10초) → 끝나면(또는 클릭 시 스킵) 지도 셀렉트로 전환
- 사운드는 영상 자체 오디오 사용(또는 우리 BGM으로 대체). "스킵" 버튼 제공.
