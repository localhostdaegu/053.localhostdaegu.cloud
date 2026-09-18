# beyondbob Jekyll Draft Implementation Plan

> **For agentic workers:** Execute the approved draft in this workspace. Use executing-plans inline; use requesting-code-review for the final read-only review. User authorization to create the draft is already recorded in the conversation.

**Goal:** 세 후보 기능과 사진의 산출물 체계를 담은 실행 가능한 beyondbob Jekyll 초안을 만든다.

**Architecture:** Just the Docs의 탐색·검색을 사용한다. 문서는 Markdown, 공통 현황은 YAML, 화면은 Liquid와 CSS로 나눈다.

**Tech Stack:** Jekyll 4.4.1, Just the Docs 0.12.0, Liquid, Markdown, CSS.

**Spec:** `docs/superpowers/specs/2026-09-15-beyondbob-design.md`

## Global Constraints

- 팀: beyondbob. 장민석, 김충식, 류준. 역할·프로필은 미정.
- 확정 트랙: 소상공인·골목상권 디지털 금융.
- 구현되지 않은 기능·측정되지 않은 지표를 실적으로 표시하지 않는다.
- 원본 자료와 내부 설계 문서는 공개 빌드에서 제외한다.

## Task 1: 실행 기반과 공통 데이터

- [x] `Gemfile`, `_config.yml`, `.gitignore`, `_data/{project,team,tasks,deliverables}.yml` 작성.
- [x] 공통 레이아웃·브랜드·문서 메타데이터·푸터 작성.
- [x] `bundle lock --local`로 설치된 의존성을 잠그고 `bundle check`로 확인.

## Task 2: 문서와 허브 콘텐츠

- [x] `index.html`과 `docs/index.md`에서 일관된 목차를 제공.
- [x] 개요·해커톤·WBS·요구사항·상위 설계·상세 설계·테스트·검수 문서를 작성.
- [x] 진행 현황·미결 사항·개발 기록·출품 시나리오·팀 페이지 작성.
- [x] 각 문서에 제안·미정·미측정 상태와 관련 요구사항 링크를 표시.

## Task 3: 화면과 작성 안내

- [x] `assets/css/beyondbob.css`에 반응형 홈·카드·일정·문서·칸반 스타일 작성.
- [x] 색상과 라벨이 있는 모듈 흐름도 SVG 작성.
- [x] `README.md`에 로컬 실행·파일 구성·문서와 팀 정보 수정법 작성.

## Task 4: 검증과 검토

- [x] `bundle exec jekyll build --trace`로 전체 빌드 확인.
- [x] 생성 HTML의 로컬 경로·앵커 및 원본 제외 여부 검사.
- [x] 1440px 데스크톱과 390px 모바일에서 화면·검색·메뉴 확인.
- [x] 읽기 전용 코드 리뷰 후 문제 수정, 필요한 검증 재실행.
- [x] 결과와 실행 명령을 사용자에게 전달.

## 검증 결과 — 2026-09-15

Jekyll 빌드 성공. HTML 18개, 로컬 참조 627개, 검색 색인 121개를 확인했으며 누락 경로·앵커·원본 유출은 없었다. 브라우저에서 한국어 검색 8개 결과, 모바일 메뉴 이동, 1440/1024/768/390px 주요 페이지의 가로 넘침과 JavaScript 오류가 없음을 확인했다. 읽기 전용 리뷰에서 지적된 단위·통합 시나리오 누락은 UT 4개·IT 3개를 추가해 해소했다. 상위 테마의 Sass 사용 중단 예정 경고는 README에 기록했다. 공개 배포와 Git 커밋은 수행하지 않았다.
