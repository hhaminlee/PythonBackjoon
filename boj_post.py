#!/usr/bin/env python3
import argparse, re, pathlib, sys, time, html, ast
from datetime import datetime
from collections import Counter

# --- 네트워킹 / 파싱 의존성 ---
try:
    import requests
    from bs4 import BeautifulSoup
except Exception:
    requests = None
    BeautifulSoup = None

META_KEYS = {
    "문제": r"^#\s*백준\s*(?P<num>\d+)\s+(?P<title>.+?)\s*$",
    "해결방법": r"^#\s*해결\s*방법\s*:\s*(?P<method>.+?)\s*$",
    "요약": r"^#\s*문제\s*요약\s*:\s*(?P<summary>.+?)\s*$",
    "처음접근": r"^#\s*처음\s*접근\s*:\s*(?P<first>.+?)\s*$",
    "시행착오": r"^#\s*시행착오\s*:\s*(?P<trouble>.+?)\s*$",
    "배운점": r"^#\s*(깨달음|배운점)\s*:\s*(?P<lesson>.+?)\s*$",
    # 최소 정보만 있는 경우(문제번호만)
    "문제번호만": r"^#\s*백준\s*(?P<num_only>\d+)\s*$",
}

UA = "Mozilla/5.0 (compatible; BOJ-Blog-Generator/1.0; +https://example.local)"
BASE = "https://www.acmicpc.net/problem/"

def parse_meta(lines):
    meta = {}
    for line in lines:
        s = line.strip()
        for _, pat in META_KEYS.items():
            m = re.match(pat, s)
            if m:
                meta.update({k: v for k, v in m.groupdict().items() if v})
    # 정규화
    if "num_only" in meta and "num" not in meta:
        meta["num"] = meta.pop("num_only")
    return meta

def extract_code(lines):
    idx = 0
    # 맨 위의 주석 블록까지는 메타로 보고 넘김
    while idx < len(lines) and lines[idx].lstrip().startswith("#"):
        idx += 1
    # 상단 공백 줄도 스킵
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return "".join(lines[idx:]).strip("\n")

def analyze_code(code):
    """코드를 분석해서 자동으로 풀이 아이디어를 생성"""
    insights = {
        "data_structures": [],
        "algorithms": [],
        "patterns": [],
        "complexity_hint": "",
        "approach": ""
    }
    
    try:
        tree = ast.parse(code)
        
        # 변수명과 함수명에서 패턴 추출
        var_names = []
        func_names = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                var_names.append(node.id)
            elif isinstance(node, ast.FunctionDef):
                func_names.append(node.id)
        
        # 자료구조 감지
        if any(name in code for name in ['deque', 'from collections import deque']):
            insights["data_structures"].append("덱(deque)")
        if any(name in code for name in ['heapq', 'import heapq']):
            insights["data_structures"].append("힙(heap)")
        if 'set(' in code or any('set' in name.lower() for name in var_names):
            insights["data_structures"].append("집합(set)")
        if any(name in code for name in ['dict(', 'defaultdict', 'Counter']):
            insights["data_structures"].append("해시맵/딕셔너리")
        if '[' in code and ']' in code:
            insights["data_structures"].append("배열/리스트")
            
        # 알고리즘 패턴 감지
        if 'sort' in code.lower():
            insights["algorithms"].append("정렬")
        if any(keyword in code for keyword in ['bfs', 'queue', 'popleft']):
            insights["algorithms"].append("BFS")
        if any(keyword in code for keyword in ['dfs', 'recursion']) or 'def ' in code and any('dfs' in name.lower() for name in func_names):
            insights["algorithms"].append("DFS")
        if 'dp' in code.lower() or any('dp' in name.lower() for name in var_names):
            insights["algorithms"].append("다이나믹 프로그래밍")
        if any(keyword in code for keyword in ['left', 'right', 'mid']) and 'while' in code:
            insights["algorithms"].append("이분탐색")
        if 'two' in code.lower() and 'pointer' in code.lower():
            insights["algorithms"].append("투 포인터")
        if any(keyword in code for keyword in ['union', 'find', 'parent']):
            insights["algorithms"].append("유니온 파인드")
            
    except:
        pass
        
    return insights

def generate_algorithm_explanation(insights, code):
    """알고리즘별 상세한 설명 생성"""
    explanations = {}
    
    # 투 포인터 설명
    if any('pointer' in algo.lower() for algo in insights["algorithms"]) or \
       (any(keyword in code for keyword in ['left', 'right']) and 'while' in code):
        explanations["two_pointer"] = {
            "name": "투 포인터(Two Pointers)",
            "description": "두 수의 합 문제를 효율적으로 해결하는 전형적인 방법",
            "steps": [
                "재료 리스트를 오름차순 정렬합니다.",
                "가장 작은 값(left)과 가장 큰 값(right)에서 시작합니다.",
                "두 수의 합(s)을 계산하여 목표값과 비교합니다.",
                "s == 목표값 → 쌍을 찾았으므로 카운트 증가, 포인터 둘 다 이동",
                "s < 목표값 → 합을 키워야 하므로 left 증가", 
                "s > 목표값 → 합을 줄여야 하므로 right 감소"
            ],
            "why": "이 과정을 반복하면 모든 가능한 쌍을 빠짐없이 확인할 수 있습니다."
        }
    
    # 힙 설명
    if "힙(heap)" in insights["data_structures"]:
        explanations["heap"] = {
            "name": "힙(Heap)",
            "description": "우선순위가 높은 요소에 빠르게 접근할 수 있는 자료구조",
            "steps": [
                "최댓값을 빠르게 찾기 위해 최대 힙을 사용합니다.",
                "Python heapq는 최소힙이므로 음수로 변환하여 최대힙 구현",
                "매번 최댓값을 꺼내고 조작 후 다시 삽입",
                "힙의 루트에서 항상 최댓값을 O(log n)에 접근"
            ],
            "why": "매번 최댓값을 찾는 작업을 효율적으로 처리할 수 있습니다."
        }
    
    # BFS 설명
    if "BFS" in insights["algorithms"]:
        explanations["bfs"] = {
            "name": "너비우선탐색(BFS)",
            "description": "그래프나 트리에서 레벨 순으로 탐색하는 알고리즘",
            "steps": [
                "시작 노드를 큐에 삽입하고 방문 처리",
                "큐에서 노드를 꺼내 인접한 노드들을 확인",
                "방문하지 않은 인접 노드를 큐에 삽입하고 방문 처리",
                "큐가 빌 때까지 반복"
            ],
            "why": "최단 거리 문제나 레벨별 탐색에 적합합니다."
        }
    
    return explanations

def generate_auto_content(meta, code, problem_info=None):
    """메타 정보가 부족해도 코드 분석으로 자동 콘텐츠 생성"""
    insights = analyze_code(code)
    auto_content = {}
    
    # 상세한 알고리즘 설명 생성
    algo_explanations = generate_algorithm_explanation(insights, code)
    auto_content["algorithm_explanations"] = algo_explanations
    
    # 자동 해결방법 생성
    if not meta.get("method"):
        methods = []
        if insights["algorithms"]:
            methods.extend(insights["algorithms"])
        if insights["data_structures"]:
            methods.extend(insights["data_structures"])
        if methods:
            auto_content["method"] = " + ".join(methods[:2])  # 최대 2개만
    
    # 자동 접근방법 생성  
    if not meta.get("first"):
        if insights["data_structures"]:
            ds = insights["data_structures"][0]
            auto_content["first"] = f"{ds}를 활용한 구현 접근"
        elif insights["algorithms"]:
            algo = insights["algorithms"][0]
            auto_content["first"] = f"{algo} 알고리즘으로 해결"
    
    # 자동 배운점 생성
    if not meta.get("lesson"):
        lessons = []
        if len(insights["data_structures"]) > 1:
            lessons.append("여러 자료구조의 조합 활용")
        if "이분탐색" in insights["algorithms"]:
            lessons.append("이분탐색의 조건 설정")
        if "다이나믹 프로그래밍" in insights["algorithms"]:
            lessons.append("DP 상태 정의와 점화식")
        if lessons:
            auto_content["lesson"] = lessons[0]
    
    # 복잡도 자동 분석 (더 정밀하게)
    time_complexity = "O(n)"  # 기본값
    space_complexity = "O(1)"  # 기본값
    complexity_details = []
    
    if "정렬" in insights["algorithms"]:
        time_complexity = "O(n log n)"
        complexity_details.append("정렬: O(n log n)")
        if any('pointer' in algo.lower() for algo in insights["algorithms"]):
            complexity_details.append("투 포인터 탐색: O(n)")
            complexity_details.append("총 시간 복잡도: O(n log n)")
    elif code.count('for') >= 2 or (code.count('for') >= 1 and code.count('while') >= 1):
        time_complexity = "O(n²)" 
    elif "이분탐색" in insights["algorithms"]:
        time_complexity = "O(log n)"
        
    if any(ds in insights["data_structures"] for ds in ["덱(deque)", "힙(heap)", "해시맵/딕셔너리"]):
        space_complexity = "O(n)"
        if "힙(heap)" in insights["data_structures"]:
            complexity_details.append("힙 저장 공간: O(n)")
    
    if complexity_details:
        auto_content["complexity"] = "\n".join([
            f"시간복잡도: {time_complexity}",
            f"공간복잡도: {space_complexity} (정렬 인플레이스 기준)"
        ] + [f"- {detail}" for detail in complexity_details[:3]])
    else:
        auto_content["complexity"] = f"시간복잡도: {time_complexity}\n공간복잡도: {space_complexity}"
    
    return auto_content

def generate_detailed_io_summary(input_format, output_format):
    """입력/출력 형식을 상세하게 분석하여 구조화된 요약 생성"""
    if not input_format or not output_format:
        return None
    
    # 입력 분석
    input_lines = []
    if "첫째 줄" in input_format or "첫 번째 줄" in input_format:
        # 첫 줄 정보 추출
        if "정수 N" in input_format or "정수 n" in input_format:
            if "M" in input_format or "m" in input_format:
                input_lines.append("재료의 개수 n과 목표값 m")
            else:
                input_lines.append("재료의 개수 n")
        elif "정수" in input_format:
            input_lines.append("정수 입력")
    
    if "둘째 줄" in input_format or "두 번째 줄" in input_format:
        if "N개" in input_format or "n개" in input_format:
            if "정수" in input_format:
                input_lines.append("n개의 정수 (재료 번호 또는 값)")
        elif "배열" in input_format or "수열" in input_format:
            input_lines.append("정수 배열")
    
    # 출력 분석
    output_desc = ""
    if "개수" in output_format:
        if "쌍" in output_format or "조합" in output_format:
            output_desc = "조건을 만족하는 쌍의 개수"
        else:
            output_desc = "조건을 만족하는 경우의 개수"
    elif "최대" in output_format:
        output_desc = "최댓값"
    elif "최소" in output_format:
        output_desc = "최솟값"
    elif "가능" in output_format or "YES" in output_format or "NO" in output_format:
        output_desc = "가능 여부 (YES/NO)"
    else:
        output_desc = "결과값"
    
    return {
        "input_lines": input_lines,
        "output_desc": output_desc
    }

def generate_io_summary(input_format, output_format):
    """기본 요약 (하위 호환)"""
    detailed = generate_detailed_io_summary(input_format, output_format)
    if not detailed:
        return None
    
    if detailed["input_lines"]:
        return f"주어진 {', '.join(detailed['input_lines'][:2])}에서 {detailed['output_desc']}를 구하는 문제"
    else:
        return f"{detailed['output_desc']}를 구하는 문제"

def fetch_problem(num, cache_dir=".boj_cache", timeout=10):
    """백준 문제 페이지를 가져와 제목/요약/입출력 형식을 추출. 캐시 사용."""
    if requests is None or BeautifulSoup is None:
        return None

    cache = pathlib.Path(cache_dir)
    cache.mkdir(exist_ok=True, parents=True)
    cache_file = cache / f"{num}.html"

    html_text = None
    if cache_file.exists():
        html_text = cache_file.read_text(encoding="utf-8", errors="ignore")
    else:
        url = f"{BASE}{num}"
        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
            if resp.status_code == 200:
                html_text = resp.text
                cache_file.write_text(html_text, encoding="utf-8")
                # 매너 대기
                time.sleep(0.8)
            else:
                return None
        except Exception:
            return None

    try:
        soup = BeautifulSoup(html_text, "html.parser")
        
        # 제목
        title_el = soup.select_one("#problem_title")
        title = title_el.get_text(strip=True) if title_el else None

        # 설명(첫 문단)
        desc_el = soup.select_one("#problem_description")
        summary = None
        if desc_el:
            # 첫 번째 <p> 텍스트만 간단 추출
            p = desc_el.find("p")
            raw = p.get_text(" ", strip=True) if p else desc_el.get_text(" ", strip=True)
            # 너무 길면 자르기
            summary = raw.strip()
            if len(summary) > 180:
                summary = summary[:177].rstrip() + "…"

        # 입력 형식 추출
        input_el = soup.select_one("#problem_input")
        input_format = None
        if input_el:
            input_format = input_el.get_text(" ", strip=True)
            if len(input_format) > 200:
                input_format = input_format[:197].rstrip() + "…"

        # 출력 형식 추출
        output_el = soup.select_one("#problem_output")
        output_format = None
        if output_el:
            output_format = output_el.get_text(" ", strip=True)
            if len(output_format) > 200:
                output_format = output_format[:197].rstrip() + "…"

        return {
            "title": title, 
            "summary": summary,
            "input_format": input_format,
            "output_format": output_format
        }
    except Exception:
        return None

def build_markdown(meta, code, auto_content=None):
    num = meta["num"].strip()
    title = meta.get("title", "") or meta.get("fetched_title", "") or ""
    
    # 자동 생성 내용과 메타 정보 합치기
    if auto_content:
        method = (meta.get("method") or auto_content.get("method") or "").strip()
        first = (meta.get("first") or auto_content.get("first") or "").strip()
        trouble = (meta.get("trouble") or "").strip()
        lesson = (meta.get("lesson") or auto_content.get("lesson") or "").strip()
        complexity = meta.get("complexity") or auto_content.get("complexity") or ""
        algo_explanations = auto_content.get("algorithm_explanations", {})
        detailed_io = auto_content.get("detailed_io", {})
    else:
        method = (meta.get("method") or "").strip()
        first = (meta.get("first") or "").strip()
        trouble = (meta.get("trouble") or "").strip()
        lesson = (meta.get("lesson") or "").strip()
        complexity = meta.get("complexity") or ""
        algo_explanations = {}
        detailed_io = {}
    
    summary = (meta.get("summary") or "").strip() or (meta.get("fetched_summary") or "").strip()

    # 제목은 항상 [백준] 문제번호 문제 이름
    head = f"# [백준] {num} {title}".rstrip()

    out = []
    out.append(head + "\n\n")

    # 문제 요약 - 상세한 입출력 정보 포함
    if detailed_io and detailed_io.get("input_lines"):
        out.append("## 문제 요약\n")
        out.append("### 입력\n")
        for i, input_line in enumerate(detailed_io["input_lines"], 1):
            out.append(f"- {input_line}\n")
        out.append("\n### 출력\n")
        out.append(f"- {detailed_io.get('output_desc', '결과값')}\n\n")
    elif summary:
        out.append("## 문제 요약\n")
        out.append(f"{summary}\n\n")

    # 풀이 아이디어
    out.append("## 풀이 아이디어\n")
    
    # 상세한 알고리즘 설명이 있으면 사용
    if algo_explanations:
        for algo_key, algo_info in algo_explanations.items():
            out.append(f"이 문제는 **{algo_info['name']}**을(를) 사용합니다.\n\n")
            out.append(f"{algo_info['description']}\n\n")
            
            for i, step in enumerate(algo_info['steps'], 1):
                out.append(f"{i}. {step}\n")
            out.append(f"\n{algo_info['why']}\n\n")
            break  # 주요 알고리즘 하나만 상세 설명
    else:
        # 기본 풀이 아이디어
        if method:
            out.append(f"- **핵심 방법**: {method}\n")
        if first:
            out.append(f"- **접근 방식**: {first}\n")
        if trouble:
            out.append(f"- **시행착오**: {trouble}\n")
        if lesson:
            out.append(f"- **배운 점**: {lesson}\n")
        
        # 아무것도 없으면 기본 메시지
        if not any([method, first, trouble, lesson]):
            out.append("- 코드 분석을 통한 자동 생성 내용이 없습니다. 메타 주석을 추가해보세요.\n")
        out.append("\n")

    # 복잡도 분석
    out.append("## 복잡도 분석\n")
    if complexity:
        # 복잡도가 여러 줄이면 적절히 포맷팅
        for line in complexity.split('\n'):
            if line.strip():
                if not line.strip().startswith('-'):
                    out.append(f"**{line.strip()}**\n")
                else:
                    out.append(f"{line.strip()}\n")
        out.append("\n")
    else:
        out.append("**시간복잡도: O(n)**\n**공간복잡도: O(1)**\n\n")

    # 파이썬 코드
    out.append("## 파이썬 코드\n")
    out.append("```python\n")
    out.append(code.rstrip() + "\n")
    out.append("```\n\n")

    # 문제 링크는 항상 맨 마지막
    out.append("## 문제 링크\n")
    out.append(f"{BASE}{num}\n")
    return "".join(out)

def main():
    ap = argparse.ArgumentParser(description="BOJ 풀이 → 블로그 Markdown 자동 생성 (코드 분석 + 크롤링 지원)")
    ap.add_argument("--src", required=True, help="파이썬 풀이 파일 경로 (상단 메타 주석 포함 권장)")
    ap.add_argument("--outdir", default="posts", help="Markdown 출력 폴더 (기본: posts)")
    ap.add_argument("--slug", help="파일명 슬러그(미지정 시 자동)")
    ap.add_argument("--crawl", action="store_true", help="제목/요약이 비었으면 백준 페이지에서 보충")
    ap.add_argument("--auto", action="store_true", default=True, help="코드 자동 분석으로 내용 생성 (기본: 활성화)")
    ap.add_argument("--no-auto", action="store_true", help="자동 분석 비활성화")
    args = ap.parse_args()

    src = pathlib.Path(args.src)
    lines = src.read_text(encoding="utf-8").splitlines(True)
    meta = parse_meta(lines)

    # 문제번호는 필수 (제목/요약은 크롤링으로 보완 가능)
    if "num" not in meta:
        raise SystemExit("메타 주석에 '백준 문제번호'가 필요합니다. (예: '# 백준 1940 주몽' 또는 '# 백준 1940')")

    # 코드 추출
    code = extract_code(lines)
    if not code.strip():
        raise SystemExit("코드가 비어 있습니다. 소스에 실제 풀이 코드를 포함하세요.")

    # 크롤링 보완
    problem_info = None
    if args.crawl and (not meta.get("title") or not meta.get("summary")):
        problem_info = fetch_problem(meta["num"])
        if problem_info:
            if not meta.get("title") and problem_info.get("title"):
                meta["fetched_title"] = problem_info["title"]
            
            # 기존 요약이 없으면 입출력 기반으로 생성
            if not meta.get("summary"):
                if problem_info.get("input_format") and problem_info.get("output_format"):
                    io_summary = generate_io_summary(problem_info["input_format"], problem_info["output_format"])
                    if io_summary:
                        meta["fetched_summary"] = io_summary
                        print(f"[IO] 입출력 형식 기반 요약 생성: {io_summary[:50]}...")
                elif problem_info.get("summary"):
                    meta["fetched_summary"] = problem_info["summary"]

    # 자동 콘텐츠 생성
    auto_content = None
    if args.auto and not args.no_auto:
        auto_content = generate_auto_content(meta, code, problem_info)
        
        # 상세한 입출력 정보 추가
        if problem_info and problem_info.get("input_format") and problem_info.get("output_format"):
            detailed_io = generate_detailed_io_summary(problem_info["input_format"], problem_info["output_format"])
            if detailed_io:
                auto_content["detailed_io"] = detailed_io
        
        insights = analyze_code(code)
        detected = ', '.join(insights['algorithms'] + insights['data_structures']) or '기본 구현'
        print(f"[AUTO] 자동 분석 완료 - 감지된 알고리즘/자료구조: {detected}")

    # 파일명 생성
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    # 제목이 없을 수도 있으므로 슬러그 안전 처리
    safe_title = (meta.get("title") or meta.get("fetched_title") or "").replace(" ", "-")
    base_slug = args.slug or f"boj-{meta['num']}-{safe_title}".strip("-")
    fname = f"{today}-{base_slug or f'boj-{meta['num']}'}.md"
    # 공백 제거
    fname = re.sub(r"\s+", "-", fname).replace("--", "-")
    outpath = outdir / fname

    # 마크다운 생성
    md = build_markdown(meta, code, auto_content)
    outpath.write_text(md, encoding="utf-8")
    print(f"[OK] 생성됨 → {outpath}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

# 자동 분석 + 크롤링
#   python boj_post.py --src 1940.py --crawl

# 자동 분석만
#   python boj_post.py --src 1940.py

# 자동 분석 끄기
#   python boj_post.py --src 1940.py --no-auto