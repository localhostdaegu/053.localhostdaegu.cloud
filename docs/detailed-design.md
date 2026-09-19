---
layout: document
title: 4. 상세 설계서
parent: 프로젝트 문서
nav_order: 6
permalink: /docs/detailed-design/
description: 서비스 저장소의 실제 코드와 실행 결과를 근거로 동작·인터페이스·예외 처리를 기록합니다.
status: 사전상담·후속 과제 구현 기록
updated: "2026-09-19"
owner: 담당 김충식 · 류준(기능별 구현)
---

<div class="notice"><strong>기록 기준</strong><br>9월 19일 밤 작업 로그까지 첫 배포·운영 페르소나 검증, 지도·사전상담 UI, 데이터 배선·11업종 지표를 반영했습니다. 최신 프론트 변경 재배포는 남아 있습니다.</div>

## 개발 개요·목적·기능

서비스명은 **localhostdaegu**, 주 동선은 계약 전 **창업자금 사전상담**입니다. 채팅 첫 화면(`/`) → 지도에서 자리 선택(`/map`) → 계산·최초안/현재안 비교와 선택(`/simulate`) → 상담자료(`/analysis`, `purpose=handoff`)로 이어집니다. 지역·업종·연도 등은 URL로 전달하고 상담 초안은 `sessionStorage`에 보관합니다. 지역 분석(`review`)은 보조 경로입니다.

| 구분 | 구현한 기능 | 이번 범위에서 제외 |
|---|---|---|
| REQ-002 | 자금 구성 분리, 계산안 비교·선택, 상담 후보 매칭, 세션·계획·노트·문서 기록, 최신 금리 기본값 | 매출 추정, 개인 신용 평가, 은행 API 전송 |
| REQ-003 | 한 문장 의도 해석, 행정동 지표·위험도, 목적별 리포트, 상담자료 Markdown·브라우저 인쇄/PDF 저장 | 카드 소비·생활인구 기반 진단, PDF 전용 생성 라이브러리, 블록체인 앵커링 |

## 실제 Data Flow

1. **의도 해석** — `POST /intent {text}` → `intent_type`, 구·동 코드와 이름, 업종 id, 예산(원), 빠진 항목. 사전은 8개 구·군, 144개 행정동, 랜드마크 15곳, 업종 동의어입니다. LLM을 쓰지 않는 규칙 기반입니다.
2. **지도·진단** — `GET /regions/geojson`(경계), `GET /metrics?industry&metric&year`(동별 지표), `GET /regions/{code}/summary`(요약 카드), `GET /metrics/risk`(위험도), `GET /stores`(점포 마커).
3. **자금 계산** — 프론트가 `GET /shocks/rates/latest?rate_type=loan_sme`로 대출금리 기본값을 채우고, `POST /finance/simulate`로 계산합니다.
4. **계산안·상담 후보** — 첫 성공 계산을 최초안으로 고정하고 재계산으로 현재안을 갱신합니다. 선택안의 자기자본 외 조달 필요액과 자격·지역 조건으로 `GET /matching/consultation`을 조회합니다. `include_unverified=true`이면 차선 후보도 받습니다.
5. **상담자료·지역 분석** — `POST /analysis {region, industry, year?, question?, finance?, purpose?, consultation?}` → `{analysis_id}` → `GET /analysis/{id}/events`(SSE, 한 번만 소비). handoff에는 `finance`·`consultation`이 필수입니다.
6. **서버 기록·내보내기** — 상담자료 생성 시 상담 세션·계획·노트를 기록하고 재생성 시 같은 세션을 갱신합니다. 완성된 자료를 내려받으면 선택안과 sha256 해시를 서버에 기록합니다. 공식 링크 이동은 은행으로 자료를 전송하지 않습니다.
7. **수집** — crontab이 `scripts/*.sh`를 실행: 뉴스 매시 10분, 인허가 04:20(수집 → 행정동 배정 → 지표 빌드), 공고 05:10, 검색 색인 05:30, 금리·임대료 월요일 05:20.

## 요구사항별 상세 설계 기록

### REQ-001 · 세무·매출 AI 도우미

이번 범위에서 제외했습니다. 관련 코드·API·테스트가 없습니다([요구사항]({{ '/docs/requirements/' | relative_url }}#req-001)).

### REQ-002 · 자금 계산과 금융상품 매칭
{: #design-req-002 }

| 기록 항목 | 내용 |
|---|---|
| 구현 범위 | 재무 엔진(결정론), 계산안 보관·비교·선택, 상담 후보, 최신 금리 조회. 결과 주 지표는 손익분기 매출·총 준비자금·조달 필요액입니다. |
| 근거 | 백엔드 `apps/finance`, `apps/matching`, `apps/product`, `apps/consultation`, 프론트 `features/simulator` |
| 입력 | 금액 10개(원, 0 이상), 원가율·수수료율·대출금리(0 이상 1 미만), 원가율 + 수수료율 < 1 |
| 처리 | 초기 투자비 = 보증금 + 권리금 + 인테리어 + 설비 / 월 고정비 = 월세 + 대출이자(희망 대출 × 금리 ÷ 12) + 보험 + 인건비 / 손익분기 매출 = 월 고정비 ÷ (1 − 원가율 − 수수료율). 자금 구성은 아래 표처럼 분리하며 기존 산식을 노출한 작업입니다. |
| 시나리오 | 예상 월매출 × 0.6(비관)·1.0(기준)·1.6(낙관)마다 영업이익, 영업이익이 양수면 투자 회수 개월, 음수면 버틸 수 있는 개월. 금리 +1%p·+2%p일 때 고정비와 기준 영업이익 |
| 출력 | `capex`, `monthly_fixed`, `bep_revenue`, `operating_reserve`, `total_required_funds`, `external_funding_need`, `funding_gap`, `scenarios[]`, `stress[]` |
| 상담 매칭 규칙 | 조달 필요액(`external_funding_need`) 기준. 한도가 작아도 후보를 유지하고 부족분을 설명합니다. 은행 연결 등급 direct → linked → unverified를 우선하고 같은 등급 안에서 보증 → 은행 → 정책자금 순입니다. `none`은 차선 후보에도 넣지 않습니다. 자격 조건은 양쪽 그룹에 동일 적용하며 모르는 나이·자치구는 확인 사항으로 남깁니다. |
| 지역 매칭 | `finance_product.district_code`는 자치구 5자리 nullable FK. 행정동 코드 앞 5자리로 비교합니다. 달성군 dgsinbo-5·북구 youth-1은 해당 지역의 linked 후보입니다. 구·군 한정 상품은 기존 `GET /matching`에서는 계속 제외합니다. |
| 저장 구조 | 조사 JSON 12건을 product BC의 DB 테이블로 시드합니다. 레거시 `GET /matching`의 15필드 계약과 JSON 폴백을 유지하고, 상담 경로는 별도 로더로 메타데이터·절차를 읽습니다. 업종 `null`(무관)·`[]`(해당 업종 없음)·목록(제한)은 DB 왕복에서도 구분합니다. |
| 실패 처리 | 스키마 위반·원가율 + 수수료율 ≥ 1 → 422. 금리 조회 중이거나 실패하면 4.5% 사용, 사용자가 입력한 금리는 덮어쓰지 않음 |
| 알려진 제한 | 예상 매출·시나리오 배수·6개월 운영준비금은 가정입니다. 금리 미공개는 "은행별 상이", 한도 미공개는 "한도 미정"으로 표시합니다. 재무 입력이 없으면 계산과 상품 매칭을 건너뜁니다. 미확인 금액은 빈 칸으로 보이고 `PlanSnapshot.unconfirmed`에 기록합니다. 비율은 업종 벤치마크·ECOS 출처가 있어 미입력 판정에서 제외합니다. |
| 검증 연결 | [TC-002]({{ '/docs/testing/' | relative_url }}#tc-002), [TC-005]({{ '/docs/testing/' | relative_url }}#tc-005) |

| 자금 항목 | 필드 | 산식·의미 |
|---|---|---|
| 운영준비금 | `operating_reserve` | 월 고정비 × 6 |
| 총 준비자금 | `total_required_funds` | 초기 투자비 + 운영준비금 |
| 자기자본 외 조달 필요액 | `external_funding_need` | max(0, 총 준비자금 − 자기자본) |
| 희망대출 반영 후 남는 부족액 | `funding_gap` | max(0, 총 준비자금 − 자기자본 − 희망대출) |

자기자본 4,000만 원·희망대출 2,500만 원인 검산 사례에서는 조달 필요액 2,260만 원, 남는 부족액 0원입니다. 부족액이 0원이어도 자기자본만으로 충분하다는 뜻은 아닙니다.

**계산안과 서버 기록.** 화면 초안의 정본은 `sessionStorage`의 `localhostdaegu.consultation.v1`입니다. 첫 성공 계산을 최초안으로 고정하고 이후 현재안을 갱신합니다. 지역·업종 변경 시 이전 결과와 선택을 무효화하고, 미제출 수정 중에는 이전 결과임을 알리며 선택을 잠급니다. 비교표에는 바뀐 입력만 표시합니다.

상담자료 생성 시 서버에 감사·재현용 스냅샷을 기록하지만 리포트는 그 저장값을 읽지 않고 입력 13필드로 다시 계산합니다. 초안의 `session_id`로 세션을 재사용하며 `PUT /consultation/{id}`는 전체 초안 교체입니다. `assumptions`·`open_questions`는 `toConsultationContext`와 같은 규칙으로 만들고, `replace_notes`로 노트를 교체해 재전송에도 쌓이지 않게 합니다. 계획안은 같은 `plan_kind`로 재전송해도 행이 늘지 않습니다.

완성된 handoff 자료만 Markdown으로 내려받거나 브라우저 인쇄로 PDF 저장합니다. 문서 기록에서는 서버가 `(session_id, plan_kind)`로 계획안을 찾아 sha256 해시를 남깁니다. 세션 저장 실패는 상담자료 생성을 막지 않고, 문서 기록 실패도 이미 끝난 다운로드를 되돌리지 않습니다. sha256은 변경 확인용이며 블록체인 앵커링이 아닙니다.

### REQ-003 · 상권 진단과 AI 리포트
{: #design-req-003 }

| 기록 항목 | 내용 |
|---|---|
| 구현 범위 | 의도 해석, 행정동 × 업종 × 연도 지표, 위험도(단건·업종별 순위·지역별 순위), 섹션별 AI 리포트 |
| 근거 | 백엔드 `apps/intent`, `apps/metric`, `apps/master`, `apps/analysis`, `apps/rag` / 프론트 `features/intent-gate`, `features/map-explorer`, `features/agent-report` |
| 의도 해석 | 긴 지명을 먼저 비교하고, 금액은 단위가 붙은 첫 표현을 찾아 "1억 5천만원"처럼 이어진 단위를 합산합니다. 랜드마크는 실제 행정동에 연결합니다(동대구역은 좌표·지번 기준 신암4동). |
| 지표 | 인허가의 개업·폐업 일자로 연도별 점포 수를 재구성합니다. 폐업률 = 해당 연도 폐업 수 ÷ 전년 말 점포 수, 점포 증감률 = (개업 수 − 폐업 수) ÷ 전년 말 점포 수. 행정동은 좌표 공간조인으로 배정합니다. |
| 기준 연도 | 선택 연도를 `AnalysisRequest.year` → `MarketDataPort.fetch` → 요약·지표·위험도까지 전달합니다. 기본값 `None`은 마지막 완결 연도(현재 2025)이며 2026은 "(집계 중)" 표시입니다. 캐시 프록시의 `year` 누락도 모델 평가 중 발견해 수정했습니다. |
| 위험도 | 폐업률·점포 수·성장률 각각의 지역 간 백분위를 0.4 · 0.4 · 0.2로 섞은 0~100점. 70점 이상 red, 40점 이상 yellow, 나머지 green. 점포가 순증해도 점수가 오르며, 창업 실패 확률이 아닙니다. |
| 리포트 섹션 | `review`: 종합 진단·상권·충격·정책자금, 재무 입력 시 계산표. `handoff`: plan·comparison·calculator·funding·questions·market이며 verdict·shock은 없습니다. `_SECTION_PLANS` 팩토리가 목적에 맞는 구성을 주입합니다. 비교표는 서버 엔진으로 다시 계산하고 LLM을 쓰지 않으며, 확인 질문은 코드가 미확인 항목을 정한 뒤 LLM이 문장만 씁니다. |
| 이벤트 계약 | `agent_status`(orchestrator·market·shock·funding × running/done/error), `tool_call`, `report_delta`(section, markdown), `report_done`(report_id, citations) |
| 검색 | 뉴스·공고를 pgvector에서 검색합니다. 색인과 같은 임베더(`gemini-embedding-001`)로 만든 벡터만 조회합니다. 인용은 번호 대신 문서 제목을 「」로 붙이고, 매칭 상품 목록에는 붙이지 않습니다. |
| 저장 구조 | 분석 요청은 메모리 저장소(워커 1개 전제). 이벤트를 소비하면 요청이 사라집니다. |
| 실패 처리 | 에이전트 실패 시 `error` 상태를 알리고 계속, 섹션 생성 실패 시 대체 문구. 없거나 이미 소비한 ID → 404 `ANALYSIS_NOT_FOUND`. `region`·`industry` 32자, `question` 500자 초과 → 422. handoff에 재무·상담 입력이 빠져도 422 |
| 알려진 제한 | "충격 분석"은 관련 뉴스 검색이며 금리·매출 영향 계산이 아닙니다. 9/19 다른 구·군 전용 문서 제외, 개업 30일 이내 종료 제외, 지표 분모 설명·상대 순위·AI 진행 문구를 반영했습니다. 기간 필터는 없으며 학원·부동산·어린이집은 폐업률(추정), 편의점은 담배소매인 기준임을 표시합니다. |
| 검증 연결 | [TC-001]({{ '/docs/testing/' | relative_url }}#tc-001), [TC-003]({{ '/docs/testing/' | relative_url }}#tc-003) |

## API와 데이터 모델

### 구현된 API

| 경로 | 용도 |
|---|---|
| `POST /intent` | 한 문장 → 지역·업종·예산 |
| `GET /regions/geojson` · `GET /regions/{code}/summary` | 행정동 경계 · 요약 카드 |
| `GET /metrics` · `GET /metrics/risk` | 동별 지표(`closure_rate`·`growth_rate`·`store_count`) · 위험도 |
| `GET /stores` | 영업 중 점포 마커 |
| `POST /finance/simulate` | 재무 시뮬레이션 |
| `GET /matching` | 금융상품 매칭 |
| `GET /matching/consultation` | iM뱅크 상담 후보·선택적 차선 후보, 자치구 조건 적용 |
| `POST /consultation` · `GET /consultation/{id}` | 상담 세션 생성·조회 |
| `PUT /consultation/{id}` | 선택안·변경 이유 등 전체 초안 교체 |
| `PUT /consultation/{id}/plans/{kind}` | 최초안·현재안 기록, 같은 종류 재전송 시 갱신 |
| `POST /consultation/{id}/documents` | 선택 계획안과 상담자료 해시 기록 |
| `GET /shocks` · `GET /shocks/rates/latest` | 충격 이벤트 · 최신 금리 |
| `GET /funding` | 접수 중 지원사업 |
| `POST /analysis` · `GET /analysis/{id}/events` | AI 리포트 시작 · SSE 스트림 |
| `GET /health` | 서버 상태 |

지표·위험도·AI 리포트의 404·400 오류는 `{error: {code, message}}` 형식을 씁니다. 입력 검증 실패(422)는 FastAPI 기본 형식입니다. `/metrics/risk`는 응답 형태가 세 가지라 OpenAPI 스키마가 없습니다.

### 주요 테이블

| 테이블 | 내용 | 9/19 밤 작업 로그 기준(행별 시점 구분) |
|---|---|---|
| `district` · `region` · `industry` | 구·군 8, 행정동 144(경계 142), 업종 11 | 마스터 시드 |
| `store` | 인허가 이력(과거 폐업 포함) | 173,816건(인허가 161,185건 포함). 인허가 좌표 158,870건·행정동 158,859건 |
| `region_industry_metric` | 행정동 × 업종 × 연도 지표 | 12,360건·등록 11업종(2019~2026) |
| `population_stat` | 주민등록 인구 8개 시점 | 48,174건. 지도에 주민등록 인구·연령대 변화 연결 |
| `rent_price` · `interest_rate` | 임대료·공실률 · 금리 | 786건 · 365건 |
| `funding_program` · `news_article` · `rag_chunk` | 지원사업 · 뉴스 · 검색 색인 | 1,735 · 1,926 · 3,643건(9/19 22:30 스냅샷, 정기 수집으로 변동) |
| `shock_event` | 대구 코로나 타임라인·거리두기 구간 | 29건(9/18) |
| `finance_product` · `finance_product_category` · `product_consultation_metadata` · `product_procedure_step` | 상품·업종 조건·상담 메타데이터·절차 | 상품 12건, 9/18 원문 대조 12/12. 은행 연결 등급 9/18 direct 2·linked 3·unverified 7 → 9/19 direct 2·linked 7·unverified 3(재단 보증 4건 승격, 제도 구조에 대한 팀 확인 근거) |
| `external_dataset` · `regional_indicator` | 외부 데이터셋·지역 지표 | 공공데이터 5종 적재·지도 연결. 센터 민간 데이터는 미확보 |
| `consultation_*` 4테이블 | 세션·계획·가정/확인 질문·문서 해시 | 서버 쓰기 경로 연결. 화면 초안은 sessionStorage가 정본 |

9/19 ERD에서 비어 있는 근거를 정리한 테이블은 `shock_event_region`·`finance_product_category`·`consultation_document`입니다. 담배소매업 33,804건·학원 수강료 21,646건·편의점 2,019건은 적재됐고, 학원 수강료의 화면 활용은 남아 있습니다. 스키마 변경은 Alembic 마이그레이션으로 관리합니다.

**스키마·경계 후속 작업.** 19 → 29테이블 확장 마이그레이션(`b93358fab70e`)은 기존 컬럼 변경 없이 테이블 10개·인덱스 8개를 추가했고 테스트 DB 왕복·`alembic check`를 통과했습니다. 이후 지역 한정 상품용 `district_code`를 별도 마이그레이션(`079cb96619ca`)으로 추가했습니다. 개발 DB 상품 재시드와 상담 세션·계획 생성도 후속 로그에서 확인했습니다. 이후 어린이집 등을 포함한 현재 31테이블 ERD 원문은 서비스 저장소 `docs/erd.md`에 있습니다.

`regional_indicator`는 업종·슬라이스가 NULL인 행도 중복 적재되지 않도록 `NULLS NOT DISTINCT` 고유 인덱스를 사용합니다. 고립 테이블 `interest_rate`는 전국 시계열, `funding_program`은 안전한 지역 관계를 만들 근거가 부족해 예외로 유지하며 `test_schema_isolation.py`로 감시합니다. matching은 product의 어댑터를 직접 불러오던 경로를 `FinanceProductUseCase` 입력 포트 주입으로 바꿨고 `test_matching_bc_boundary.py`가 다른 BC 어댑터 import를 금지합니다.

## 애플리케이션 설정과 예외 처리
{: #configuration }

| 구분 | 현재 설정 | 확인 근거 |
|---|---|---|
| 모델 설정 | 기본 리포트 `gemini-3.8-flash`, 임베딩 `gemini-embedding-001`. 리포트는 `REPORT_WRITER_PROVIDER=ollama`·`OLLAMA_REPORT_MODEL=gemma4:12b`로 로컬 선택 가능. 9/19 halfvec(2560) 변경·provider 설정화 완료. qwen 전환은 해당 임베더 재색인·환경변수 변경·백엔드 재시작 | 9/19 [모델 평가]({{ '/docs/model-evaluation/' | relative_url }}) |
| 연결 설정 | 루트 `.env` → `backend/.env` 순으로 읽고 빈 값은 무시. DB·Redis·Neo4j 주소와 외부 API 키 이름은 서비스 저장소의 API 목록 문서에 정리(값은 커밋하지 않음) | 설정 테스트 |
| CORS·mock | `CORS_ALLOW_ORIGINS`로 운영 출처를 추가하고 로컬 출처는 유지. `NEXT_PUBLIC_API_BASE` 미설정 시 mock 사용. mock도 handoff 목적과 대구 기준 검산값을 반영 | 9/18 preflight·mock 후속 수정 |
| 재시도 | 온통청년 4xx 포함 지수 백오프 4회, Gemini 임베딩 429·5xx 재시도. 리포트 생성은 재시도 없이 섹션 대체 문구 | 게이트웨이 테스트 |
| 데이터 부족 | 위험도 데이터가 없으면 단건 404, 순위는 빈 배열. 리포트 상권 섹션은 "데이터가 없습니다" 표기 | 코드 확인 |
| 사용자 설정 | 지도 연도(기본 2025), 지표·업종 선택, 재무 입력 13항목, 추가 질문 | 프론트 테스트·E2E |
| 관측 | 수집 스크립트별 로그 파일, 가장 나쁜 종료 코드 기록, 중복 실행 방지. 외부 API 오류 메시지에서 키를 제거 | 가짜 키 오류 테스트 |

## 상위 설계와 달라진 점

9월 15일 기획서와 실제 구현의 차이입니다.

| 기획 | 구현 | 이유·영향 |
|---|---|---|
| 위험도 = 경쟁밀도 0.3 + 폐업률 0.3 + 매출감소 0.2 + 프랜차이즈 포화 0.2 | 폐업률 0.4 + 점포 수 0.4 + 성장률 0.2의 상대 순위 | 매출·프랜차이즈 데이터를 쓰지 않고, 점포 수는 면적·인구·반경으로 나눈 밀도가 아님. 점수 해석 수위는 OPEN-009에서 결정 |
| 상가정보·실거래가·먹거리골목·대규모점포·전통시장 반경 등 대구 특화 변수 | 일부 반영 | 편의점 상가정보 적재, 공공데이터 5종 적재·지도 배선 완료(9/19). 실거래가·골목·대규모점포 및 반경 분석은 미구현 |
| 네이버 뉴스 API | 구글 뉴스 RSS | 네이버 키 문제(DEC-008) |
| 9/28 멘토링 때 센터 집계 반출 | 미확보·일정 미확인 | 확인된 정책·예약이 아니었음(OPEN-004) |
| Redis·Neo4j 활용 | 컨테이너만 구성 | 분석 요청 저장소는 메모리로 구현(워커 1개 전제) |
| 서울 거리두기 충격 데이터 | 대구 코로나 타임라인 + 공공데이터 구간 | 리뷰에서 서울 원본 잔재 발견(DEC-012) |
| (선택) 리포트 해시 블록체인 기록 | 범위 제외. 상담자료 sha256 해시만 서버 기록 | 9/18 결정(DEC-018) |
