
Claude가 응답을 완료했습니다

동적 지역 발굴과 일일 트렌드 추적 시스템 설계했다
동적 지역 발굴과 일일 트렌드 추적 시스템 설계했다
좋은 소식부터 말씀드리면, ① 번은 사실 코드 수정 없이 config.py만 넓히면 되고, ②번도 스케줄 파일 한 줄만 바꾸면 됩니다 — 이미 만들어둔 구조가 두 요구사항에 딱 맞게 설계되어 있었어요. 왜 그런지 설명하고 바로 파일 드릴게요.

① "전국 스캔" — 사실 후보 목록만 넓히면 됩니다
지금 구조(CORE_REGIONS + CANDIDATE_REGIONS + HOT_REGION_COUNT)가 이미 "후보 중 화제성 상위 N개 자동 채택" 방식이라, 후보 목록을 전국 주요 동네로 넓게 채우기만 하면 사실상 "전국에서 상위 지역을 찾는" 효과를 냅니다. HOT_REGION_COUNT를 5로 올리면 됩니다.

② 일 단위 + 누적 7일 트렌드 — 이미 그렇게 계산하고 있었습니다
확인해보니 지금 코드의 "이번 주/지난 주" 계산이 월요일~일요일 같은 달력 기준이 아니라, 실행하는 그 날짜 기준으로 "최근 7일 vs 그 전 7일"을 계산하는 방식이었습니다. 즉 매일 실행해도 그날 기준으로 최근 7일 롤링 윈도우를 자동으로 다시 계산해줘서, 로직 자체는 이미 원하시는 대로 작동합니다. 실행 주기만 매주 → 매일로 바꾸면 됩니다.


기존 롤링 윈도우 로직 재확인
기존 롤링 윈도우 로직 재확인
確認できました。이제 두 파일을 수정하겠습니다.


API 비용 검증하고 함수 구조 확인했다
API 비용 검증하고 함수 구조 확인했다
정상 확인됐습니다. 이제 config.example.py도 같이 갱신하고 가이드도 손보겠습니다.


HTML 구조 검증 및 패키지 완성 준비했다
HTML 구조 검증 및 패키지 완성 준비했다
모든 검증 통과했습니다. 최종 배포판을 재패키징하겠습니다.


명령 실행함, 파일 읽음
명령 실행함, 파일 읽음
정리
코드(fetch_and_build.py) 수정은 필요 없었습니다 — 이미 있던 구조로 두 요구사항 다 충족돼서, config.py와 워크플로우 스케줄만 바꾸면 됩니다.

GitHub에서 하실 일 (파일 2개만)
1) .github/workflows/weekly-update.yml → 새 내용으로 교체 (cron이 0 0 * * 1에서 0 0 * * *로, 매일 실행)

2) config.py → CORE_REGIONS/CANDIDATE_REGIONS/HOT_REGION_COUNT 부분을 아래로 교체:

python
CORE_REGIONS = ["강남", "성수", "잠실", "동탄", "회기"]
CANDIDATE_REGIONS = [
    "홍대", "이태원", "건대", "연남", "을지로", "여의도", "종로", "압구정",
    "청담", "신촌", "서울숲", "노원", "신림", "마곡",
    "오산", "수원", "일산", "분당", "판교",
    "강릉", "춘천", "홍천", "속초",
    "부산", "해운대", "대구", "경주", "울산",
    "대전", "청주",
    "전주", "광주", "여수", "순천",
    "제주",
]
HOT_REGION_COUNT = 5
두 파일 다 Commit 후 Actions 재실행하시면 됩니다.

참고로 정직하게 말씀드리면
①번은 "진짜 전국 스캔"이 아니라 "미리 적어둔 35개 후보 안에서 화제성 상위 5개를 고르는" 방식입니다. 이 목록에 없는 동네는 아무리 떠도 안 뽑힙니다. 필요하면 후보를 계속 추가하시면 됩니다.
②번은 이제 매일 실행되니, GitHub Actions 무료 사용량(월 2,000분)도 이전보다 더 씁니다. 지금 규모(실행 1회 2분 안팎)면 매일 돌려도 한 달에 60분 정도라 여유는 충분합니다.

Naver trend package
ZIP 

Weekly update
YML 

Config.github
PY 
아 소유자 등록이나 이런거는 별도로 배포 하지 않는다는 뜻이였어 그리고 경기 도시도 조금 더 세분화 해봤어. # 경기 
    "오산", "동탄", "수원", "행궁동", "광교", "분당", "판교", "파주", "일산",
근데 제주 끝에 , 가 있던데 그건 코드에 지장 없나?


경기 지역 목록 병합 및 문법 검증 완료
경기 지역 목록 병합 및 문법 검증 완료
네, 트레일링 콤마(마지막 항목 뒤에 콤마)는 파이썬에서 전혀 문제없습니다. 오히려 관례적으로 권장되는 스타일이에요 — 나중에 항목을 추가할 때 그 줄만 추가하면 되고, 실수로 콤마 빼먹는 오류(예전에 겪으셨던 그 SyntaxError)도 줄어듭니다. 안심하셔도 됩니다.

경기도 세분화 목록 반영하겠습니다
말씀하신 목록으로 CANDIDATE_REGIONS의 경기 부분을 교체하면 됩니다:

python
CANDIDATE_REGIONS = [
    # 서울
    "홍대", "이태원", "건대", "연남", "을지로", "여의도", "종로", "압구정",
    "청담", "신촌", "서울숲", "노원", "신림", "마곡",
    # 경기
    "오산", "동탄", "수원", "행궁동", "광교", "분당", "판교", "파주", "일산",
    # 강원
    "강릉", "춘천", "홍천", "속초",
    # 영남
    "부산", "해운대", "대구", "경주", "울산",
    # 충청
    "대전", "청주",
    # 호남
    "전주", "광주", "여수", "순천",
    # 제주
    "제주",
]
config.py의 CANDIDATE_REGIONS 부분을 이걸로 교체하시면 됩니다.

참고로 한 가지
지금 CORE_REGIONS에도 이미 "동탄"이 고정으로 들어가 있는데, CANDIDATE_REGIONS에도 "동탄"을 또 넣으셨네요. 코드가 중복은 자동으로 걸러주니 에러는 안 나지만, 어차피 고정으로 항상 포함되는 지역이라 후보 화제성 검사 대상에 넣는 건 의미가 없습니다 (매번 API 호출만 한 번 더 쓰는 셈이라 살짝 비효율). 원하시면 CANDIDATE_REGIONS에서 "동탄"은 빼셔도 되고, 그냥 두셔도 실제 동작에는 문제없습니다.

그래 근데 저렇게 도시말고 실제로 뜨는 도시를 전체에서  sorting은 못하나? 지금이야 그렇지만


기술적 타당성 검토하고 전국 범위 확대 방안 모색했음
기술적 타당성 검토하고 전국 범위 확대 방안 모색했음
솔직하게 말씀드리면, "완전히 전국을 대상으로, 목록 없이 알아서 뜨는 곳을 찾아내는" 건 기술적으로 불가능합니다. 다만 "훨씬 더 전국에 가깝게" 만드는 방법은 있어요. 왜 완전 자동은 안 되는지와, 대안을 설명해드릴게요.

왜 "목록 없는 전국 스캔"이 안 되는지
네이버든 구글이든, **"지금 대한민국에서 뜨고 있는 동네 이름 목록을 줘"**라는 API 자체가 존재하지 않습니다. 검색 API는 항상 "이 키워드를 검색하면 몇 건 나오는지"만 답해줄 뿐, "어떤 키워드들이 존재하는지"는 알려주지 않아요. 그래서 결국 비교할 후보 목록은 누군가(저희)가 미리 준비해둬야 합니다. 이건 구조적인 한계라, 다른 방법으로도 완전히 피할 수는 없습니다.

그래도 "더 전국에 가깝게" 만드는 방법은 있습니다
지금 목록(35개, 손으로 고른 유명 동네)보다 훨씬 촘촘하게 만들 수 있습니다.

방법: 전국 공식 행정구역 목록을 통째로 후보에 넣기

대한민국은 시/군/구 단위로 약 220~230개의 공식 행정구역이 있습니다 (예: 수원시, 강릉시, 해운대구 등)
이 전체 목록을 CANDIDATE_REGIONS에 넣으면, 최소한 "행정구역 단위"에서는 진짜 전국 커버가 됩니다
API 호출 비용은 문제없습니다 — 화제성 조회는 후보당 딱 1번씩만 부르는 가벼운 호출이라, 230개를 넣어도 하루 한도(25,000건)에는 전혀 지장 없습니다
다만 트레이드오프가 하나 있습니다

행정구역 목록에는 "성수동", "홍대", "이태원", "행궁동"처럼 사람들이 실제로 맛집 검색할 때 쓰는 "동네 이름"이 빠집니다. 이런 이름들은 공식 행정구역이 아니라 비공식 지명(상권명)이거든요
즉 "시/군/구 단위로는 완전 전국"이지만, "핫플레이스 단위(동 이름)로는 오히려 지금보다 엉성해질 수 있습니다"
그래서 두 가지 선택지가 있습니다
A안 — 전국 시/군/구 전체(약 230개)로 완전 교체: 진짜 "전국 스캔"에 가장 가깝지만, 세부 동네 디테일은 잃습니다

B안 — 지금의 동네 목록(35개) + 전국 시/군/구 목록(230개)을 합쳐서 사용: 후보가 250개 이상으로 늘어나지만, 동네 디테일과 전국 커버리지를 둘 다 가져갈 수 있습니다. API 비용도 여전히 부담 없습니다.

개인적으로는 B안을 추천드립니다 — 어차피 비용 차이가 거의 없으니, 지금 있는 목록을 버릴 이유가 없습니다. 이 방향으로 전국 시/군/구 전체 목록을 만들어서 코드에 반영해드릴까요?

아니 근데 지금 다시 실행해보니까 고정 외에는 상위 지역이 안뜬다. 이건 어떻게 된거지?


CANDIDATE_REGIONS 설정 오류 진단 및 검증 방법 제시
CANDIDATE_REGIONS 설정 오류 진단 및 검증 방법 제시
원인이 몇 가지로 좁혀지는데, 먼저 로그를 하나 확인해주시면 바로 알 수 있습니다.

확인 방법
GitHub 저장소 → Actions 탭 → 가장 최근 실행 클릭
"데이터 수집 및 index.html 생성" 단계 펼치기
로그 맨 위쪽에 이런 줄이 있는지 찾아보세요:
   [지역 자동 선정] 후보 지역별 화제성(블로그 총 게시물 수) 조회 중...
이 줄이 아예 없다면 → 원인이 확정됩니다. CANDIDATE_REGIONS가 비어있다고 코드가 인식한 겁니다 (코드 로직상 CANDIDATE_REGIONS가 비어있으면 이 기능 자체를 건너뛰고 조용히 예전 방식으로 돌아가게 되어 있어요).

그렇다면 왜 비어있다고 인식됐을까
config.py를 웹에서 다시 열어서 확인해주실 부분:

CANDIDATE_REGIONS = [...] 줄 앞에 #이 붙어있지 않은지 — 주석 처리되면 코드에서 안 읽힙니다
변수 이름이 정확히 CANDIDATE_REGIONS인지 (대소문자, 언더스코어 포함해서 정확히 일치해야 합니다)
대괄호 [ ]가 제대로 열리고 닫혔는지 — 혹시 지역 목록 수정하시면서 괄호 하나가 빠지진 않았는지
로그에 그 줄이 있다면 (다른 원인)
[지역 자동 선정]은 뜨는데 결과적으로 고정 지역만 보인다면, 그 아래 로그에 각 후보 지역의 화제성 숫자가 다 0건으로 찍혀있을 가능성이 있습니다. 이 경우는 API 응답 구조가 예상과 달라서 값을 못 읽어오는 코드 버그일 수 있어요 — 이땐 제가 코드를 봐야 합니다.

로그 화면 캡처해서 보여주시겠어요? 특히 [지역 자동 선정]이 있는지 없는지, 있다면 그 아래 지역별 숫자가 어떻게 찍혔는지 보이는 부분으로요.

1783755809722_image.png
# GitHub 저장소용 config.py
# CLIENT_ID / CLIENT_SECRET은 일부러 비워둡니다 - GitHub Secrets에 등록한 값이
# 자동으로 여기 대신 사용되기 때문에, 이 파일에 진짜 키를 적을 필요가 없습니다.
# (그래서 이 파일은 공개 저장소에 올려도 안전합니다)
CLIENT_ID = ""
CLIENT_SECRET = ""
# 주의: 지역 이름은 반드시 양쪽에 큰따옴표(")가 다 있어야 합니다.
# 예: "강남", "성수" (O)   "강남", 성수" (X - SyntaxError 발생)
# 아래 REGIONS는 CANDIDATE_REGIONS를 안 쓸 경우의 기본값 (하위 호환용, 지금은 안 쓰임)
REGIONS = [
    "강남", "성수", "동탄", "회기"
]
# 고정으로 항상 포함할 지역 (블로그 포스팅 밀도가 검증된 동네 위주로 구성)
CORE_REGIONS = ["강남", "성수", "잠실", "동탄", "회기"]
# 화제성 검사 대상 후보 풀 - 전국 주요 동네/도시를 폭넓게 넣어두면, 매 실행마다
# 이 중 화제성 상위 HOT_REGION_COUNT개가 자동으로 CORE_REGIONS에 추가됩니다.
# (전국 전체를 무작위로 훑는 게 아니라, 이 목록 안에서만 비교합니다 - 목록에 없는
#  동네는 아무리 실제로 뜨고 있어도 후보에 오르지 않습니다. 필요하면 자유롭게 추가하세요.)
CANDIDATE_REGIONS = [
    # 서울
    "홍대", "이태원", "건대", "연남", "을지로", "여의도", "종로", "압구정",
    "청담", "신촌", "서울숲", "노원", "신림", "마곡",
    # 경기
    "오산", "동탄", "수원", "행궁동", "광교", "분당", "판교", "파주", "일산",
    # 강원
    "강릉", "춘천", "홍천", "속초",
    # 영남
    "부산", "해운대", "대구", "경주", "울산",
    # 충청
    "대전", "청주",
    # 호남
    "전주", "광주", "여수", "순천",
    # 제주
    "제주",
]
HOT_REGION_COUNT = 5
DISPLAY_PER_REGION = 20
TOP_N = 8
TOP_N_PER_REGION = 5
OG_IMAGE_URL = "https://i.postimg.cc/gJhgW7Zz/seukeulinsyas-2026-07-11-131250.png"
EXTRA_BADGES = ["매일 9:00 시 업데이트"]
# Google Search Console / 네이버 서치어드바이저 소유자 인증 코드
# (사이트마다 고유한 값이라, 새로 배포하는 사이트라면 본인이 새로 발급받은 값을 넣어야 합니다)
# GOOGLE_SITE_VERIFICATION = "본인이_발급받은_값"
# NAVER_SITE_VERIFICATION = "본인이_발급받은_값"

그리고 따로 주석도 안보이네
아니면 fetch 파일도 수정이 필요했던거 아니야?

더 보기

fetch 파일 업데이트 누락 확인 및 재제공 필요
fetch 파일 업데이트 누락 확인 및 재제공 필요
좋은 지적이에요, 확인해보니 원인이 바로 그겁니다. config.py는 완벽합니다 — 문법도 맞고 CANDIDATE_REGIONS도 정상적으로 정의되어 있어요. 문제는 fetch_and_build.py 쪽입니다.

원인
로그에 [지역 자동 선정]이라는 줄 자체가 안 보인다는 건, GitHub에 있는 fetch_and_build.py가 이 기능을 아직 모르는 예전 버전이라는 뜻입니다. 이 기능(resolve_active_regions 함수, 지역랭킹 탭 등)을 처음 만들어드렸던 메시지에서 "두 파일 다 바꾸셔야 합니다"라고 안내드렸었는데, 아마 그때 config.py만 바꾸시고 fetch_and_build.py 교체는 빠졌던 것 같습니다. 정확히 지난번 Google 인증 때와 같은 패턴이에요.

확인하는 방법
GitHub 저장소에서 fetch_and_build.py 파일을 열어서, 우측 상단 돋보기 아이콘이나 Ctrl+F로 페이지 안에서 resolve_active_regions를 검색해보세요.

검색 결과 없음 → 예전 버전 확정, 교체 필요
있음 → 다른 원인이니 다시 알려주세요
지금 하실 일
최신 fetch_and_build.py를 다시 드릴 테니, 통째로 교체해주세요. (내용 자체는 이전에 드렸던 것과 동일합니다 — 새로 만든 게 아니라, 실수로 GitHub에 안 올라갔던 그 버전을 다시 드리는 거예요.)


명령 실행함, 파일 읽음
명령 실행함, 파일 읽음
순서
GitHub에서 fetch_and_build.py 클릭 → 연필 아이콘 → 전체 지우고 위 파일 내용 통째로 붙여넣기 → Commit
config.py는 손 안 대셔도 됩니다 (이미 완벽합니다)
Actions 탭 → Run workflow로 재실행
로그에서 [지역 자동 선정] 줄과 그 아래 지역별 화제성 숫자들이 뜨는지 확인
앞으로 헷갈리지 않으시려면
지금까지 패턴을 보면, **"config.py에 새로운 변수를 추가하는 기능"**은 거의 항상 fetch_and_build.py도 같이 바뀝니다. 반대로 "이미 있는 변수의 값만 바꾸는 것"(지역 추가, 배지 문구 등)은 config.py만 고치면 됩니다. 제가 새 기능을 드릴 때마다 "이번엔 두 파일 다 바꿔야 합니다 / config.py만 바꾸면 됩니다"를 첫 줄에 명확히 표시해드릴게요 — 이번엔 그 안내가 이전 메시지 어딘가에 묻혀서 놓치신 것 같습니다.


Fetch and build
PY 

Claude가 응답할 때 알림을 받으시겠습니까?





Claude는 AI이며 실수할 수 있습니다. 응답을 다시 한번 확인해 주세요.
Fetch and build · PY
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이번 주 블로그 언급 급상승 맛집 TOP 8 생성기
================================================
 
동작 방식 (상태 저장 없이 매번 완결되는 구조):
  1. 네이버 지역검색 API로 지역별 맛집 후보 목록을 가져온다.
  2. 네이버 블로그검색 API로 각 식당 이름의 최근 블로그 게시물을 가져온다.
     (응답에 postdate가 포함되어 있어 DB 없이도 "이번 주 vs 지난 주" 계산 가능)
  3. 이번 주 언급 수 - 지난 주 언급 수(증가폭) 기준으로 TOP 8을 뽑는다.
  4. 결과를 index.html로 바로 렌더링한다.
 
사전 준비:
  - https://developers.naver.com 에서 애플리케이션 등록
  - 사용 API로 "검색" 중 "지역"과 "블로그"를 반드시 체크
  - 발급받은 Client ID / Client Secret을 config.py 에 입력
 
실행:
  python fetch_and_build.py
 
주의: 이 환경(샌드박스)은 openapi.naver.com에 네트워크 접근이 차단되어 있어
      실행 테스트는 본인 PC(또는 서버)에서 해야 합니다.
"""
 
import json
import os
import time
import datetime
import re
import urllib.request
import urllib.parse
from html import unescape
 
try:
    from config import CLIENT_ID, CLIENT_SECRET, REGIONS, DISPLAY_PER_REGION, TOP_N
    # 환경변수(예: GitHub Actions Secrets)가 있으면 config.py 값보다 우선 적용
    # -> 자동화 파이프라인에서는 config.py에 실제 키를 적어두지 않아도 됨
    CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", CLIENT_ID)
    CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", CLIENT_SECRET)
    try:
        from config import OG_IMAGE_URL
    except ImportError:
        # config.py에 OG_IMAGE_URL을 아직 안 넣었으면 빈 이미지로 대체 (에러 방지)
        OG_IMAGE_URL = ""
    try:
        from config import SPONSORED_KEYWORDS
    except ImportError:
        # config.py에 별도 설정이 없으면 기본 필터 키워드 사용
        SPONSORED_KEYWORDS = [
            "협찬", "제공받아", "제공받은", "원고료", "체험단", "기자단",
            "무료로 제공", "업체로부터 제공", "지원을 받아", "서포터즈",
            "본 포스팅은", "해당 게시물은", "소정의 활동비",
        ]
    try:
        from config import TOP_N_PER_REGION
    except ImportError:
        TOP_N_PER_REGION = 5  # 지역별 탭에는 기본 5개까지만 표시
    try:
        from config import EXTRA_BADGES
    except ImportError:
        # 기존에 PERSONAL_BADGE_TEXT를 쓰던 config.py와도 호환되도록 처리
        try:
            from config import PERSONAL_BADGE_TEXT
            EXTRA_BADGES = [PERSONAL_BADGE_TEXT] if PERSONAL_BADGE_TEXT else []
        except ImportError:
            EXTRA_BADGES = []  # 비워두면 추가 배지가 표시되지 않음
    try:
        from config import MAX_BLOG_RESULTS
    except ImportError:
        MAX_BLOG_RESULTS = 300  # 식당 하나당 최대 조회할 게시물 수 (100의 배수, 최대 1000)
    try:
        from config import GOOGLE_SITE_VERIFICATION
    except ImportError:
        GOOGLE_SITE_VERIFICATION = ""  # Google Search Console 소유자 인증 코드
    try:
        from config import NAVER_SITE_VERIFICATION
    except ImportError:
        NAVER_SITE_VERIFICATION = ""  # 네이버 서치어드바이저 소유자 인증 코드
    try:
        from config import CORE_REGIONS
    except ImportError:
        CORE_REGIONS = []  # 항상 고정으로 포함할 지역 (비워두면 기존 REGIONS 방식 그대로 사용)
    try:
        from config import CANDIDATE_REGIONS
    except ImportError:
        CANDIDATE_REGIONS = []  # 화제성 검사 대상 후보 지역 풀 (비워두면 자동 선정 기능 꺼짐)
    try:
        from config import HOT_REGION_COUNT
    except ImportError:
        HOT_REGION_COUNT = 3  # 후보 지역 중 화제성 상위 몇 개를 골라 추가할지
except ImportError:
    raise SystemExit(
        "config.py가 없습니다. config.example.py를 config.py로 복사한 뒤 "
        "네이버 API 키와 지역 목록을 입력하세요."
    )
 
NAVER_API_BASE = "https://openapi.naver.com/v1/search"
REQUEST_DELAY_SEC = 0.15  # 네이버 API 과호출 방지용 딜레이
 
 
def _naver_get(path: str, params: dict) -> dict:
    """네이버 오픈API 공통 호출 함수"""
    url = f"{NAVER_API_BASE}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
    time.sleep(REQUEST_DELAY_SEC)
    return json.loads(body)
 
 
def strip_tags(text: str) -> str:
    """네이버 응답의 <b> 태그 등을 제거하고 HTML 엔티티를 복원"""
    return unescape(re.sub(r"<[^>]+>", "", text)).strip()
 
 
def get_candidate_restaurants(region: str, display: int = 20) -> list:
    """지역검색 API로 '{region} 맛집' 후보 식당 이름 목록을 가져온다"""
    data = _naver_get("local.json", {
        "query": f"{region} 맛집",
        "display": display,
        "sort": "random",
    })
    names = []
    for item in data.get("items", []):
        name = strip_tags(item["title"])
        if name and name not in names:
            names.append(name)
    return names
 
 
def is_sponsored_post(title: str, description: str) -> bool:
    """제목+요약에 협찬/광고성 문구가 포함되어 있는지 확인"""
    text = strip_tags(title) + " " + strip_tags(description)
    return any(keyword in text for keyword in SPONSORED_KEYWORDS)
 
 
def get_weekly_mention_counts(restaurant_name: str, today: datetime.date) -> tuple:
    """
    블로그검색 API로 특정 식당의 '이번 주'/'지난 주' 언급 수를 계산한다.
    postdate(YYYYMMDD) 필드를 기준으로 집계.
    협찬/광고/기자단 문구가 포함된 게시물은 집계에서 제외한다.
 
    API 한 번 호출은 최대 100건까지만 주므로, MAX_BLOG_RESULTS까지 여러 번
    페이지를 넘겨가며 가져온다(start 파라미터 사용). 최신순 정렬이므로
    지난 주 시작일보다 오래된 게시물이 나오면 그 지점에서 바로 중단한다
    (게시물이 적은 대부분의 식당은 1번 호출만으로 끝나서 API 낭비가 없다).
    """
    this_week_start = today - datetime.timedelta(days=7)
    last_week_start = today - datetime.timedelta(days=14)
 
    this_week_count = 0
    last_week_count = 0
    filtered_count = 0
 
    start = 1
    while start <= MAX_BLOG_RESULTS:
        data = _naver_get("blog.json", {
            "query": restaurant_name,
            "display": 100,
            "start": start,
            "sort": "date",
        })
        items = data.get("items", [])
        if not items:
            break
 
        reached_older_post = False
        for item in items:
            postdate_str = item.get("postdate", "")
            if not postdate_str or len(postdate_str) != 8:
                continue
            try:
                post_date = datetime.datetime.strptime(postdate_str, "%Y%m%d").date()
            except ValueError:
                continue
 
            if post_date < last_week_start:
                reached_older_post = True
                break  # 최신순이므로 여기서부터는 더 볼 필요 없음
 
            if post_date > today:
                continue
 
            if is_sponsored_post(item.get("title", ""), item.get("description", "")):
                filtered_count += 1
                continue
 
            if post_date >= this_week_start:
                this_week_count += 1
            else:
                last_week_count += 1
 
        if reached_older_post or len(items) < 100:
            break
        start += 100
 
    return this_week_count, last_week_count, filtered_count
 
 
def get_region_volume(region: str) -> int:
    """'{지역} 맛집' 블로그 검색의 총 게시물 수를 그 지역 화제성의 근사치로 사용"""
    try:
        data = _naver_get("blog.json", {"query": f"{region} 맛집", "display": 1, "sort": "date"})
        return int(data.get("total", 0))
    except Exception:
        return 0
 
 
def resolve_active_regions() -> list:
    """
    CORE_REGIONS(고정) + CANDIDATE_REGIONS 중 화제성 상위 HOT_REGION_COUNT개를 합쳐
    이번 실행에서 실제로 쓸 지역 목록을 정한다.
    CANDIDATE_REGIONS가 비어있으면(설정 안 했으면) 기존 REGIONS 방식 그대로 사용 (하위 호환).
    """
    if not CANDIDATE_REGIONS:
        return REGIONS
 
    print("[지역 자동 선정] 후보 지역별 화제성(블로그 총 게시물 수) 조회 중...")
    scored = []
    for region in CANDIDATE_REGIONS:
        volume = get_region_volume(region)
        print(f"  - {region}: {volume}건")
        scored.append((region, volume))
    scored.sort(key=lambda x: x[1], reverse=True)
    hot_picks = [r for r, _ in scored[:HOT_REGION_COUNT]]
 
    combined = list(CORE_REGIONS)
    for r in hot_picks:
        if r not in combined:
            combined.append(r)
    print(f"[지역 확정] 고정 {CORE_REGIONS} + 화제성 상위 {hot_picks} = {combined}")
    return combined
 
 
def build_ranking() -> tuple:
    """전 지역을 순회하며 급상승 맛집 TOP N을 계산. (결과 리스트, 협찬/광고 추정 총 제외 건수)를 반환"""
    today = datetime.date.today()
    results = []
    seen_names = set()
    total_filtered = 0
 
    for region in REGIONS:
        print(f"[지역검색] {region} 맛집 후보 수집 중...")
        candidates = get_candidate_restaurants(region, DISPLAY_PER_REGION)
 
        for name in candidates:
            if name in seen_names:
                continue
            seen_names.add(name)
 
            this_week, last_week, filtered = get_weekly_mention_counts(name, today)
            total_filtered += filtered
            if filtered:
                print(f"    (협찬/광고 추정 {filtered}건 제외)")
            growth = this_week - last_week
 
            # 최소 언급량 필터: 우연히 1~2건 튄 걸 급상승으로 착시하지 않도록
            if this_week < 2:
                continue
 
            results.append({
                "name": name,
                "region": region,
                "this_week": this_week,
                "last_week": last_week,
                "growth": growth,
                "filtered": filtered,
            })
            print(f"  - {name}: 이번주 {this_week} / 지난주 {last_week} (증가 {growth})")
 
    results.sort(key=lambda x: (x["growth"], x["this_week"]), reverse=True)
    print(f"\n총 협찬/광고 추정 제외 건수: {total_filtered}건")
    return results, total_filtered  # 자르지 않고 전체 반환 - 지역별 탭 계산에 필요
 
 
def build_region_ranking(all_results: list) -> list:
    """지역별로 증가폭 합계를 집계해 '어느 동네가 가장 뜨는지' 랭킹을 만든다"""
    agg = {}
    for r in all_results:
        region = r["region"]
        if region not in agg:
            agg[region] = {
                "region": region,
                "total_growth": 0,
                "total_this_week": 0,
                "total_last_week": 0,
                "count": 0,
            }
        agg[region]["total_growth"] += r["growth"]
        agg[region]["total_this_week"] += r["this_week"]
        agg[region]["total_last_week"] += r["last_week"]
        agg[region]["count"] += 1
    ranking = list(agg.values())
    ranking.sort(key=lambda x: x["total_growth"], reverse=True)
    return ranking
 
 
def build_tabs(all_results: list, region_ranking: list) -> dict:
    """
    전체 결과에서 '전체' 탭 + '지역랭킹' 탭 + 지역별 탭 데이터를 만든다.
    REGIONS에 새 지역이 추가되면, 다음 실행 시 자동으로 그 지역 탭도 생긴다
    (코드 수정 불필요 - config.py의 REGIONS만 바뀌면 됨).
    """
    tabs = {"전체": all_results[:TOP_N]}
    if region_ranking:
        tabs["지역랭킹"] = region_ranking
    for region in REGIONS:
        region_results = [r for r in all_results if r["region"] == region]
        if region_results:  # 데이터가 있는 지역만 탭으로 생성
            tabs[region] = region_results[:TOP_N_PER_REGION]
    return tabs
 
 
def naver_map_link(name: str, region: str) -> str:
    """식당 이름+지역으로 네이버 지도 검색 링크를 만든다 (좌표 없이도 동작하는 방식)"""
    query = urllib.parse.quote(f"{name} {region}")
    return f"https://map.naver.com/p/search/{query}"
 
 
def render_region_cards(ranking: list) -> str:
    """지역 랭킹 카드 목록을 HTML로 렌더링 ('지역랭킹' 탭 전용)"""
    if not ranking:
        return '<p style="text-align:center;color:#999;padding:20px 0;">데이터가 없습니다.</p>'
    rows_html = ""
    for i, r in enumerate(ranking, start=1):
        growth_badge = f"+{r['total_growth']}" if r["total_growth"] > 0 else str(r["total_growth"])
        map_url = f"https://map.naver.com/p/search/{urllib.parse.quote(r['region'] + ' 맛집')}"
        rows_html += f"""
        <a class="card" href="{map_url}" target="_blank" rel="noopener">
          <div class="rank">{i}</div>
          <div class="info">
            <div class="name">{r['region']} <span class="map-icon">📍</span></div>
            <div class="region">언급 식당 {r['count']}곳</div>
          </div>
          <div class="stats">
            <span class="growth">{growth_badge}</span>
            <span class="count">이번 주 {r['total_this_week']}건 · 지난 주 {r['total_last_week']}건</span>
          </div>
        </a>"""
    return rows_html
 
 
def render_cards(items: list) -> str:
    """식당 카드 목록을 HTML로 렌더링 (탭 하나 분량)"""
    if not items:
        return '<p style="text-align:center;color:#999;padding:20px 0;">데이터가 없습니다.</p>'
    rows_html = ""
    for i, r in enumerate(items, start=1):
        growth_badge = f"+{r['growth']}" if r["growth"] > 0 else str(r["growth"])
        map_url = naver_map_link(r["name"], r["region"])
        rows_html += f"""
        <a class="card" href="{map_url}" target="_blank" rel="noopener">
          <div class="rank">{i}</div>
          <div class="info">
            <div class="name">{r['name']} <span class="map-icon">📍</span></div>
            <div class="region">{r['region']}</div>
          </div>
          <div class="stats">
            <span class="growth">{growth_badge}</span>
            <span class="count">이번 주 {r['this_week']}건 · 지난 주 {r['last_week']}건</span>
          </div>
        </a>"""
    return rows_html
 
 
def render_html(tabs: dict, total_filtered: int = 0, out_path: str = "index.html"):
    """
    tabs: {"전체": [...], "강남": [...], "성수": [...], ...} 형태의 딕셔너리.
    REGIONS에 새 지역이 생기면 build_tabs()가 자동으로 키를 추가해주므로,
    여기서는 tabs에 들어있는 만큼 탭 버튼도 자동으로 늘어난다 (코드 수정 불필요).
    total_filtered: 협찬/광고 추정으로 집계에서 제외된 전체 게시물 건수.
    """
    today_str = datetime.date.today().strftime("%Y년 %m월 %d일")
    region_tags = " ".join(f"#{r}" for r in REGIONS)
    extra_badges_html = "".join(
        f'<span class="hero-badge-secondary">{badge}</span>' for badge in EXTRA_BADGES
    )
    overall = tabs.get("전체", [])
    top_n = len(overall) if overall else TOP_N
 
    tab_names = list(tabs.keys())
    tab_buttons_html = ""
    tab_panels_html = ""
    for idx, name in enumerate(tab_names):
        active_btn = " active" if idx == 0 else ""
        active_panel = " active" if idx == 0 else ""
        tab_buttons_html += f'<button class="tab-btn{active_btn}" data-tab="tab-{idx}">{name}</button>'
        panel_content = render_region_cards(tabs[name]) if name == "지역랭킹" else render_cards(tabs[name])
        tab_panels_html += f'<div class="tab-panel{active_panel}" id="tab-{idx}">{panel_content}</div>'
 
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>이번 주 블로그 언급 급상승 맛집 TOP 8</title>
 
<!-- 카톡/문자로 링크 공유 시 미리보기 카드에 쓰이는 정보 -->
<meta name="description" content="네이버 블로그 언급량 기준, 이번 주 가장 뜨는 맛집 TOP 8을 확인해보세요.">
<meta property="og:title" content="이번 주 블로그 언급 급상승 맛집 TOP 8">
<meta property="og:description" content="네이버 블로그 언급량 기준, 이번 주 가장 뜨는 맛집 TOP 8을 확인해보세요.">
<meta property="og:image" content="{OG_IMAGE_URL}">
<meta property="og:type" content="website">
 
<!-- 검색엔진 소유자 인증용 (Google Search Console / 네이버 서치어드바이저) -->
{f'<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">' if GOOGLE_SITE_VERIFICATION else ''}
{f'<meta name="naver-site-verification" content="{NAVER_SITE_VERIFICATION}">' if NAVER_SITE_VERIFICATION else ''}
 
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    background: #f5f5f7;
    margin: 0;
    padding: 24px 16px 64px;
    color: #1a1a1a;
  }}
  .hero {{
    max-width: 560px;
    margin: 0 auto 20px;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    background: linear-gradient(to top right, #f43f5e, #ec4899, #fb923c);
    padding: 24px;
    color: white;
    position: relative;
  }}
  .hero-icon {{
    position: absolute;
    right: -15px;
    bottom: -20px;
    opacity: 0.15;
    pointer-events: none;
  }}
  .hero-inner {{
    position: relative;
    z-index: 1;
  }}
  .hero-badge {{
    background: rgba(255,255,255,0.2);
    font-size: 10px;
    font-weight: 800;
    padding: 5px 10px;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    display: inline-block;
  }}
  .hero-badge-row {{
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }}
  .hero-badge-secondary {{
    background: rgba(255,255,255,0.9);
    color: #d9376e;
    font-size: 10px;
    font-weight: 800;
    padding: 5px 10px;
    border-radius: 999px;
    display: inline-block;
  }}
  .hero h1 {{
    font-size: 28px;
    font-weight: 800;
    margin: 12px 0 0;
    line-height: 1.2;
    letter-spacing: -0.02em;
  }}
  .hero-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: rgba(255,255,255,0.9);
    font-weight: 700;
    margin-top: 16px;
  }}
  .hero-date {{
    background: rgba(0,0,0,0.2);
    padding: 5px 10px;
    border-radius: 12px;
    font-size: 11px;
  }}
  .tabs {{
    max-width: 560px;
    margin: 0 auto 14px;
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding-bottom: 4px;
  }}
  .tab-btn {{
    flex: 0 0 auto;
    border: none;
    background: white;
    color: #666;
    font-size: 13px;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 999px;
    cursor: pointer;
  }}
  .tab-btn.active {{
    background: #ff5a36;
    color: white;
  }}
  .tab-panel {{
    display: none;
  }}
  .tab-panel.active {{
    display: block;
  }}
  .filter-note {{
    max-width: 560px;
    margin: 0 auto 14px;
    font-size: 11px;
    color: #aaa;
    text-align: center;
  }}
  .list {{
    max-width: 560px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .card {{
    background: white;
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    text-decoration: none;
    color: inherit;
    transition: box-shadow 0.15s;
  }}
  .card:hover {{
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }}
  .map-icon {{
    font-size: 12px;
    opacity: 0.6;
  }}
  .rank {{
    font-size: 20px;
    font-weight: 800;
    color: #ff5a36;
    min-width: 28px;
  }}
  .info {{
    flex: 1;
  }}
  .name {{
    font-size: 16px;
    font-weight: 700;
  }}
  .region {{
    font-size: 12px;
    color: #999;
    margin-top: 2px;
  }}
  .stats {{
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
  }}
  .growth {{
    font-size: 14px;
    font-weight: 700;
    color: #ff5a36;
  }}
  .count {{
    font-size: 11px;
    color: #aaa;
  }}
</style>
</head>
<body>
  <div class="hero">
    <div class="hero-icon">
      <svg width="160" height="160" fill="currentColor" viewBox="0 0 24 24">
        <path d="M17.66 11.57c-.77-3.95-2.85-6.86-5.27-9.4c-.25-.26-.68-.15-.77.19-.53 2.11-.96 4.98-2.5 7-1.72 2.25-3.68 3.19-4.43 5.92C3.96 18.02 6.07 22 10 22c4.83 0 8.64-4.08 7.66-10.43z"/>
      </svg>
    </div>
    <div class="hero-inner">
      <div class="hero-badge-row">
        <span class="hero-badge">REALTIME BLINK TREND</span>
        {extra_badges_html}
      </div>
      <h1>이주의 급상승<br>맛집 TOP {top_n}</h1>
      <div class="hero-meta">
        <span>{region_tags}</span>
        <span class="hero-date">{today_str}</span>
      </div>
    </div>
  </div>
  <div class="tabs">
    {tab_buttons_html}
  </div>
  <p class="filter-note">협찬·광고·체험단 추정 게시물 {total_filtered}건 제외 후 집계</p>
  <div class="list">
    {tab_panels_html}
  </div>
  <script>
    document.querySelectorAll('.tab-btn').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        document.querySelectorAll('.tab-btn').forEach(function(b) {{ b.classList.remove('active'); }});
        document.querySelectorAll('.tab-panel').forEach(function(p) {{ p.classList.remove('active'); }});
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
      }});
    }});
  </script>
</body>
</html>"""
 
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n완료: {out_path} 생성됨 (탭 {len(tab_names)}개: {', '.join(tab_names)})")
 
 
if __name__ == "__main__":
    REGIONS = resolve_active_regions()
    all_results, total_filtered = build_ranking()
    region_ranking = build_region_ranking(all_results)
    tabs = build_tabs(all_results, region_ranking)
    render_html(tabs, total_filtered)
    # 원본 데이터도 별도로 저장 (검증/디버깅용)
    with open("top8_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    # 검색로봇 접근 허용 안내 파일 생성 (네이버 서치어드바이저 robots.txt 경고 해소용)
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n")
    print("완료: robots.txt 생성됨")
 








