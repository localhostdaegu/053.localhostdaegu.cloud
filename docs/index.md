---
layout: document
title: 프로젝트 문서
permalink: /docs/
nav_order: 2
has_children: true
description: 기획에서 출품까지. 요구사항과 설계, 검증 결과를 하나의 흐름으로 연결합니다.
status: 9/20 배포 갱신·접수 완료 반영
updated: "2026-09-20"
owner: 담당 장민석 · PM/아키텍트
---

<div class="notice"><strong>문서 읽는 순서</strong><br>프로젝트 개요로 방향을 확인한 뒤, 요구사항 → 상위 설계 → 상세 설계 → 테스트 → 검수 → 출품 순서로 읽어 주세요. 9월 19일 밤 작업 로그와 9월 20일 팀의 완료 확인을 반영했습니다. 첫 배포와 운영 페르소나 검증, 데이터 신뢰·AI 진행 안내, 11개 업종 지표 연결을 완료했습니다. 최신 변경 배포 갱신·제안요약서 작성·접수까지 완료했으며, 시연 영상은 구현 화면으로 대체했습니다. 날짜별 변화는 <a href="{{ '/journal/' | relative_url }}">개발 기록</a>과 <a href="{{ '/progress/' | relative_url }}">진행 현황</a>에서 확인할 수 있습니다.</div>

<div class="doc-links"><a class="doc-link" href="{{ '/docs/overview/' | relative_url }}">프로젝트 개요 <span>확정한 방향, 처음 검토한 세 주제, 범위 기준</span></a><a class="doc-link" href="{{ '/docs/hackathon/' | relative_url }}">해커톤 안내 <span>참가 트랙, 공식 일정, 접수 현황, 활용 데이터</span></a><a class="doc-link" href="{{ '/docs/target-industries/' | relative_url }}">타깃 업종 <span>수요 동인 4유형으로 고른 10종과 대구 지표 현황</span></a></div>

## 산출물 목차

{% for item in site.data.deliverables %}
<a class="deliverable-row" href="{{ item.url | relative_url }}"><span class="row-number">{{ item.number }}</span><span class="row-title">{{ item.title }}<small>{{ item.description }}</small></span><span class="status-pill">{{ item.status }}</span><span class="row-arrow" aria-hidden="true">↗</span></a>
{% endfor %}

## 문서 사이의 연결

**요구사항 번호 → WBS 작업 → 설계 모듈 → 테스트 번호 → 데모 장면**을 연결합니다. 같은 내용은 원본 문서 한 곳에서 관리하고, 다른 페이지에서는 그 문서로 연결합니다.

| 문서 | 답해야 하는 질문 |
|---|---|
| 요구사항 | 누구의 어떤 문제를 해결해야 하는가? |
| 상위 설계 | 어떤 모듈과 데이터 흐름이 필요한가? |
| 상세 설계 | 실제 코드에서는 어떻게 동작하는가? |
| 테스트 | 어떤 입력에서 어떤 결과가 나와야 하는가? |
| 최종 검수 | 다른 환경에서도 설치하고 재현할 수 있는가? |
| 출품 시나리오 | 발표에서 무엇을 어떤 근거와 함께 보여줄 것인가? |

## 문서 상태를 읽는 방법

- **구현 / 로컬 실행 결과:** 서비스 개발 작업 로그에 구현과 로컬 검증이 기록된 내용입니다. 작업별 검증 시점과 배포 환경 확인은 따로 표시합니다.
- **초안 / 검토안 / 계획안:** 팀 논의와 검증을 거쳐 바뀔 수 있는 제안입니다.
- **작성 틀:** 구현·실측 이후 채울 항목을 정리한 상태입니다.
- **미정:** 아직 결정하지 않은 항목입니다.
- **미측정 / 미실행:** 실제 성능 측정이나 테스트를 수행하지 않은 상태입니다.

[진행 현황]({{ '/progress/' | relative_url }}) · [논의와 결정]({{ '/decisions/' | relative_url }}) · [프로젝트 안내]({{ '/about/' | relative_url }})
