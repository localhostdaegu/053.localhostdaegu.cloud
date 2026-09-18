# beyondbob — 대구 소상공인·골목상권 AI 프로젝트

2026 AI Blockchain Challenge in Daegu 참가 준비를 위한 Jekyll 프로젝트 허브입니다.

- **팀:** beyondbob / 장민석 · 김충식 · 류준
- **트랙:** 소상공인·골목상권 디지털 금융
- **서비스:** localhostdaegu — 창업 금융 네비게이터(청년창업 매칭 + 골목상권 AI 컨설팅, 세무·매출은 제외)
- **역할:** 장민석 팀장·PM/아키텍트 · 김충식·류준 기능 단위 풀스택
- **상태:** 2026-09-18 기준 프로토타입 로컬 완주, 창업자금 사전상담 전환·제출 문서·오프라인 대응 모델 평가 완료, 배포·접수 준비 중. 사이트는 서비스 저장소 개발 기록을 수동으로 반영합니다.
- **사이트 주소:** `https://053.localhostdaegu.cloud`

## 로컬 실행

Ruby와 Bundler가 필요합니다. Jekyll 4.4 계열을 사용하며 현재 검증 환경은 Ruby 3.4입니다.

```bash
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4300
```

브라우저에서 `http://127.0.0.1:4300`을 엽니다. 다른 Jekyll 서버가 해당 포트를 사용하면 `--port` 값을 바꿉니다. 설정 파일을 수정한 경우 서버를 재시작합니다.

```bash
bundle exec jekyll build --trace
```

정적 결과는 `_site/`에 생성됩니다. 게시 전 도메인·호스팅 환경·공식 제출 정보를 확인합니다.

## GitHub Pages 배포

`.github/workflows/pages.yml`이 `main` 푸시 또는 수동 실행 시 사이트를 배포합니다.

1. Ruby 3.4를 준비하고 Gemfile 의존성을 설치합니다.
2. 저장소에 설정된 Pages 도메인과 경로를 읽습니다.
3. production 모드로 Jekyll을 빌드하고 주요 결과 파일을 확인합니다.
4. `_site/`를 업로드한 뒤 기존 `github-pages` 환경으로 배포합니다.

저장소의 Pages 소스는 **GitHub Actions**, 사용자 지정 도메인은 **053.localhostdaegu.cloud**로 설정되어 있습니다. `_config.yml`의 `url`만 지정하는 것으로는 배포되지 않으며, 이 워크플로의 성공 여부를 확인해야 합니다.

수동 재배포는 저장소 **Actions → Deploy Jekyll to GitHub Pages → Run workflow**에서 실행합니다. 의존성 락 파일은 현재 저장소의 `.gitignore` 규칙에 따라 추적하지 않습니다.

## 파일 구성

| 경로 | 역할 |
|---|---|
| `index.html` | 프로젝트 홈 |
| `docs/` | 개요·해커톤·WBS·요구사항·설계·테스트·검수 |
| `docs/model-evaluation.md` | 독립 최상위 메뉴인 모델 평가(진행 현황과 개발 기록 사이). 기존 `/docs/model-evaluation/` 주소 유지 |
| `progress.html` | 공통 일정과 작업 데이터를 표시하는 현황 |
| `decisions.md` | 논의와 결정(팀 소개와 프로젝트 안내 사이). 미결 항목과 결정 이유 |
| `journal.html`, `_posts/` | 최신순 개발 기록 |
| `showcase.md` | 출품 시나리오·자료 준비 상태 |
| `team.html`, `_data/team.yml` | 팀 소개와 프로필 데이터 |
| `_data/project.yml` | 처음 검토한 세 주제·일정·사이트 기준일 |
| `_data/tasks.yml` | WBS 작업·상태·담당·완료 조건 |
| `_data/deliverables.yml` | 홈과 문서 목차가 공유하는 산출물 목록 |
| `_layouts/`, `_includes/` | 공통 문서·기록 레이아웃과 브랜드 |
| `assets/css/beyondbob.css` | 사이트 반응형 스타일 |
| `assets/css/home.css` | 홈 전용 쇼케이스 스타일 |
| `assets/images/neighborhood*.webp` | Blender로 제작한 골목 모형, 데스크톱·모바일용 |
| `scripts/render-neighborhood.py` | 골목 모형 생성·렌더링 원본(Blender 5, 외부 에셋 없음). 공개 빌드 제외 |
| `assets/js/search-language.js` | 검색 색인에서 한글을 보존하는 Lunr 확장 |
| `assets/images/` | 원본 SVG 아이콘과 흐름도 |

## 팀 프로필 수정

`_data/team.yml`에서 각 팀원의 `role`, `description`, `profile_status`를 수정합니다. 선택 항목 `bio`, `github`를 추가하면 팀 페이지에 표시됩니다. 사진 기능은 프로필을 받은 뒤 추가할 수 있습니다. 근거 없는 역할이나 경력을 채우지 않습니다.

## 문서 수정

Markdown 상단 메타데이터의 `title`, `parent`, `nav_order`, `permalink`, `status`, `updated`, `owner`를 사용합니다. `owner`는 문서 머리의 담당 표시(예: `담당 장민석 · PM/아키텍트`)이며, 생략하면 "담당 미배정"으로 표시됩니다. 개별 문서를 바꾼 날은 `updated: "YYYY-MM-DD"`로 기록합니다. 날짜를 생략하면 `_data/project.yml`의 공통 기준일을 표시합니다.

요구사항 번호(REQ), 작업 번호(WBS), 테스트 번호(TC)를 유지해 관련 문서를 연결합니다. 기능의 실제 구현 범위가 정해지면 홈의 후보 상태와 요구사항·설계·출품 자료를 함께 갱신합니다.

작업 상태는 현재 `논의 중`, `예정`, `완료`입니다. `_data/tasks.yml`의 항목을 수정하면 WBS와 보드가 같은 내용을 표시합니다. 현황은 **파일 편집 후 다시 빌드**하면 반영됩니다. 웹에서 상태를 저장하거나 드래그하는 기능은 없습니다.

## 개발 기록 추가

`_posts/YYYY-MM-DD-short-title.md`를 만듭니다.

```yaml
---
title: 기록 제목
date: 2026-09-15 09:00:00 +0900
category: 개발 기록
author: beyondbob
description: 무엇을 바꾸고 확인했는지 한 문장으로 요약
---
```

본문은 무엇을 했는지 → 이유 → 검증한 결과 → 남은 문제 순서로 작성합니다. 미래 날짜의 기록은 기본적으로 게시되지 않습니다.

## 원본 자료와 참고

사용자가 제공한 루트 Markdown 2개와 스크린샷은 원본으로 보존합니다. `_config.yml`에서 이 원본과 `docs/superpowers` 내부 설계 자료를 공개 결과에서 제외합니다. 새 공개 이미지는 `assets/images/`에 두고 필요할 경우 PNG 제외 패턴을 조정합니다.

- [redoceanmap](https://blog.redoceanmap.com/posts/): 개발 기록
- [solidbob](https://docs.solidbob.cloud/): 진행 관리와 산출물
- [Life Tutorial](https://lifetutorial.beyondfacade.cloud/): 문서 탐색과 출품 자료
- [Just the Docs](https://just-the-docs.com/): Jekyll 테마

구현·측정하지 않은 항목은 `예정`, `미정`, `미측정`, `미실행`으로 표시하고, 구현한 항목에는 실행일과 환경(로컬·배포)을 함께 적습니다.

## 초안 검증

- Jekyll 전체 빌드 성공
- 18개 HTML 페이지의 내부 링크·앵커 및 검색 색인 연결 확인
- 한국어 검색과 모바일 메뉴 이동 확인
- 1440 / 1024 / 768 / 390px에서 주요 페이지의 가로 넘침 없음 확인
- 원본 자료·내부 설계 문서의 공개 빌드 제외 확인

현재 Just the Docs 0.12.0의 Sass 코드에서 사용 중단 예정 경고가 출력됩니다. 빌드는 통과하며, 테마를 업데이트할 때 경고 해소 여부를 확인합니다.
