---
layout: document
title: 1. Milestone & WBS
parent: 프로젝트 문서
nav_order: 3
permalink: /docs/milestones/
description: 작업을 산출물과 완료 조건으로 나누고 공식 대회 일정에 맞춰 연결합니다.
status: 팀 계획 초안
owner: 담당 장민석 · PM
---

## 9월 — 10월 마일스톤

{% for item in site.data.project.milestones %}
<div class="timeline-item"><div class="timeline-date">{{ item.date }}</div><div class="timeline-body"><h3>{{ item.title }}</h3><span class="status-pill">{{ item.kind }}</span><p>{{ item.description }}</p></div></div>
{% endfor %}

## WBS — 작업 분해 구조

9월 18일 기능 단위로 담당을 정했습니다. 아래 표는 처음 세운 작업 분해 구조이고, 실제 담당과 상태는 작업 현황에 기록합니다.

| 단계 | 작업 | 산출물 / 완료 조건 | 선행 조건 |
|---|---|---|---|
| 환경 구성 | 저장소·개발 환경·실행 방법 정리 | 팀원이 같은 안내로 실행 | 사용 스택 결정 |
| 타당성 검토 | 대상 사용자·데이터·실행 가능성 확인 | 대표 시나리오와 데이터 샘플 확보 | 사용자 문제 선정 |
| 개발 착수 | MVP와 우선순위 확정 | 필수·확장·제외 범위 합의 | 타당성 검토 |
| 요구사항 | 기능·품질 요구사항과 판정 조건 작성 | 요구사항 번호와 테스트 연결 | MVP 결정 |
| 상위 설계 | 모듈·AI·외부 API·인프라 흐름 작성 | 모듈별 입력·출력 설명 | 요구사항 정리 |
| 구현·상세 설계 | 핵심 시나리오 구현과 실제 구조 기록 | 코드와 문서의 동작 일치 | 상위 설계 |
| 테스트 | 단위·통합·성능·예외 검증 | 재현 가능한 결과와 결함 기록 | 실행 가능한 기능 |
| 추가 요구 | 피드백 반영 여부와 범위 변경 기록 | 영향·일정·재검증 범위 합의 | 변경 요청 |
| 검수·출품 | 설치·이전·데모·자료 확인 | 검수 기록과 제출본 정리 | 테스트 결과 |

## 작업 현황

{% for task in site.data.tasks %}
- **{{ task.id }} · [{{ task.title }}]({{ task.url | relative_url }})** — {{ task.status }} / {{ task.assignee }}. 완료 조건: {{ task.output }}.
{% endfor %}

## 추가 요구사항 처리

변경 이유 → 영향받는 요구사항·모듈 → 일정 영향 → 채택 여부 → 재검증 시나리오를 기록합니다. 기존 요구사항을 수정한 경우 변경 이유를 [미결·결정 기록]({{ '/decisions/' | relative_url }})에 연결합니다.

## 일정 관리 원칙

- 공식 일정과 팀 내부 계획을 구분합니다.
- 본선 이후 작업은 진출을 조건으로 계획합니다.
- 작업 완료는 파일 존재뿐 아니라 각 작업의 완료 조건을 기준으로 판단합니다.
- [진행 현황]({{ '/progress/' | relative_url }})은 이 문서와 같은 작업 데이터를 표시합니다.
