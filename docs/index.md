---
layout: document
title: 프로젝트 문서
permalink: /docs/
nav_order: 2
has_children: true
description: 기획에서 출품까지. 요구사항과 설계, 검증 결과를 하나의 흐름으로 연결합니다.
status: 초안 v0.1
---

<div class="notice"><strong>문서 읽는 순서</strong><br>프로젝트 개요로 방향을 확인한 뒤, 요구사항 → 상위 설계 → 상세 설계 → 테스트 → 검수 → 출품 순서로 읽어 주세요. 현재는 기획 초안이며 실제 서비스 구현과 성능 검증은 진행 전입니다.</div>

<div class="doc-links"><a class="doc-link" href="{{ '/docs/overview/' | relative_url }}">프로젝트 개요 <span>대상 사용자, 세 후보 기능, 결정할 범위</span></a><a class="doc-link" href="{{ '/docs/hackathon/' | relative_url }}">해커톤 안내 <span>참가 트랙, 공식 일정, 제출 자료</span></a></div>

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

- **초안 / 검토안 / 계획안:** 팀 논의와 검증을 거쳐 바뀔 수 있는 제안입니다.
- **작성 틀:** 구현·실측 이후 채울 항목을 정리한 상태입니다.
- **미정:** 아직 결정하지 않은 항목입니다.
- **미측정 / 미실행:** 실제 성능 측정이나 테스트를 수행하지 않은 상태입니다.

[진행 현황]({{ '/progress/' | relative_url }}) · [미결·결정 기록]({{ '/decisions/' | relative_url }}) · [참고 사이트와 구성 원칙]({{ '/about/' | relative_url }})
