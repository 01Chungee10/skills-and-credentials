# 숙련은 어떻게 자격이 되는가

독일·호주·미국 직업교육훈련사를 읽는 한국어 웹 전시. r004 장표를 따라 작업대, 세 나라의 제도, 국가 비교, 자동화 설비에서의 판단으로 이어진다.

## 실행과 편집

정적 서버로 저장소 루트를 열면 된다. 배포물은 `index.html`, `style.css`, `assets/`, `reading/`이다. 자바스크립트를 수정한 뒤 `npm ci`와 `npm run build`로 배포 번들을 다시 만들 수 있다. 3D 모듈과 모델은 관객이 3D 보기를 선택할 때 불러온다. 정지 이미지는 동일한 Blender 장면을 렌더링했다. `studio/workshop.blend`에는 작업대, 두 초안, 호주 등록 기록, 미국 대응 재원, 조명·카메라 컬렉션이 들어 있다. Blender에서 컬렉션 가시성을 바꾸면 각 장면을 편집할 수 있다. 저장소 루트에서 `blender -b -P studio/build.py`를 실행하면 절차적으로 작성된 기본 모형을 재생성한다.

## 장면을 추가할 때

| 장면 | 장표 | 읽을 근거 | 화면에서 보여줄 관계 |
|---|---:|---|---|
| 독일 | 6–7 | 서독 연방의회 VI/778 및 Ulmer 외, PDF 19–21쪽 | 법 시행과 후대의 기준 개정 절차를 구분. 두 문서의 관할과 공동 조율 |
| 호주 | 12–13 | Goozee, PDF 25–27쪽 및 Bowman & McKenna, PDF 22쪽 | 학습자의 성취 기록과 기관 등록 지위의 상호인정 |
| 미국 | 18 | Hayward & Benson, PDF 13–14, 17쪽 | 대응 부담, 주 계획, 교사 급여의 용도 |
| 한국 | 27, 32–33 | r004 자동화·숙련 및 결론 | 관측된 결과와 교육 설계 예시의 구별 |

새 장면마다 장표 번호, 핵심 질문, 근거 쪽, 스크롤 전후 화면, 모바일 정지 화면, 확인할 관계를 먼저 정한다. 웹 원문은 발행처에 연결하고 보유 원문 폴더는 독자의 브라우저에서만 연결한다. 표지·문서·교실의 3D 장면은 직접 제작한 설명용 모형이다.

## 참조한 공개 제작 지침

- [스크롤 전시의 장면 설계](https://github.com/openai/plugins/tree/981b02c0c44058b595f3b4180002c3ae3c806d40/plugins/build-web-data-visualization/skills/scrollytelling-and-parallax-data-visualization) — 장면별 정지 상태와 역스크롤 점검.
- [GreenSock 공식 제작 지침](https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760) — 스크롤 위치에 연동하고 동작 줄이기를 존중한다.
- [Three.js 장면 구성](https://github.com/CloudAI-X/threejs-skills/tree/0e181866f095b5f06d005133876e926515390d95) — 카메라·조명·객체 관리.
- [프런트엔드 디자인](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/frontend-design) — 발표의 실제 사물을 시각 언어로 삼는다.
