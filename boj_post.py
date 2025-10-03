#!/usr/bin/env python3
import argparse, re, pathlib, sys, time, os, json
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# --- 네트워킹 / 파싱 의존성 ---
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] 'requests'와 'beautifulsoup4' 라이브러리가 필요합니다. 'pip install requests beautifulsoup4'", file=sys.stderr)
    sys.exit(1)

# --- AI 분석 의존성 ---
try:
    import google.generativeai as genai
except ImportError:
    print("[ERROR] 'google-generativeai' 라이브러리가 필요합니다. 'pip install google-generativeai'", file=sys.stderr)
    sys.exit(1)


# --- 기존 유틸리티 함수 (일부 유지) ---

UA = "Mozilla/5.0 (compatible; BOJ-Blog-Generator/2.0; +https://example.local)"
BASE = "https://www.acmicpc.net/problem/"

def parse_meta(lines):
    """소스코드 상단의 메타 주석을 파싱합니다."""
    meta = {}
    meta_keys = {"문제": r"^#\s*백준\s*(?P<num>\d+)\s+(?P<title>.+?)\s*$", "문제번호만": r"^#\s*백준\s*(?P<num_only>\d+)\s*$",}
    for line in lines:
        s = line.strip()
        for _, pat in meta_keys.items():
            m = re.match(pat, s)
            if m:
                meta.update({k: v for k, v in m.groupdict().items() if v})
    if "num_only" in meta and "num" not in meta:
        meta["num"] = meta.pop("num_only")
    return meta

def extract_code(lines):
    """주석과 공백을 제외한 순수 코드를 추출합니다."""
    idx = 0
    while idx < len(lines) and lines[idx].lstrip().startswith("#"):
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return "".join(lines[idx:]).strip()

def fetch_problem(num, cache_dir=".boj_cache", timeout=10):
    """백준 문제 페이지를 크롤링하여 정보를 가져옵니다."""
    cache = pathlib.Path(cache_dir)
    cache.mkdir(exist_ok=True)
    cache_file = cache / f"{num}.html"
    html_text = None
    if cache_file.exists():
        html_text = cache_file.read_text(encoding="utf-8")
    else:
        url = f"{BASE}{num}"
        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
            if resp.status_code == 200:
                html_text = resp.text
                cache_file.write_text(html_text, encoding="utf-8")
                time.sleep(0.5)
            else: return None
        except requests.RequestException: return None

    try:
        soup = BeautifulSoup(html_text, "html.parser")
        title = soup.select_one("#problem_title").get_text(strip=True)
        description = soup.select_one("#problem_description").get_text("\n", strip=True)
        return {"title": title, "description": description}
    except Exception:
        return None

# --- AI 분석 로직 (핵심) ---

def analyze_with_ai(problem_info, code):
    """Gemini API를 사용하여 문제와 코드를 분석하고 해설을 생성합니다."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    아래 백준 문제와 제 파이썬 풀이 코드를 분석해서 간결한 블로그 포스트를 작성해주세요.
    제 코드에 실제로 구현된 내용만 기반으로 작성하고, 일반적인 이론 설명은 최소화하세요.

    ### 문제
    제목: {problem_info['title']}
    {problem_info['description']}

    ### 제 코드
    ```python
    {code}
    ```

    ### JSON 출력 형식 (이 형식으로만 답변)
    {{
      "problem_summary": "문제 핵심을 1문장으로",
      "solution_idea": {{
        "core_method": "코드에서 사용한 알고리즘/자료구조만 간단히 (예: 그리디, 정렬)",
        "approach": "제 코드가 어떻게 동작하는지 핵심 로직만 2-3문장으로",
        "lesson": "이 코드의 핵심 포인트 1문장"
      }},
      "complexity_analysis": {{
        "time_complexity": "O() 표기",
        "time_explanation": "제 코드 기준으로 1문장",
        "space_complexity": "O() 표기",
        "space_explanation": "제 코드 기준으로 1문장"
      }}
    }}
    """

    try:
        response = model.generate_content(prompt)
        # AI 응답에서 JSON 부분만 추출
        json_text = re.search(r'```json\n({.*?})\n```', response.text, re.DOTALL)
        if json_text:
            return json.loads(json_text.group(1))
        else:
            return json.loads(response.text)
    except Exception as e:
        print(f"[ERROR] AI 분석 중 오류 발생: {e}", file=sys.stderr)
        print(f"AI 응답 내용: {response.text if 'response' in locals() else 'N/A'}", file=sys.stderr)
        return None

# --- 마크다운 생성 로직 (수정) ---

def build_markdown(meta, code, ai_analysis):
    """AI 분석 결과를 바탕으로 마크다운 포스트를 생성합니다."""
    num = meta["num"]
    title = meta.get("title") or meta.get("fetched_title", "")
    head = f"# [백준] {num} {title}".rstrip()

    out = [head + "\n\n"]
    
    # AI 분석 결과가 있을 경우 우선 사용
    if ai_analysis:
        summary = ai_analysis.get("problem_summary", "AI 요약 생성에 실패했습니다.")
        idea = ai_analysis.get("solution_idea", {})
        complexity = ai_analysis.get("complexity_analysis", {})

        out.append("## 문제 요약\n")
        out.append(f"{summary}\n\n***\n\n")

        out.append("## 풀이 아이디어\n")
        out.append(f"- **핵심 방법**: {idea.get('core_method', 'N/A')}\n")
        out.append(f"- **접근 방식**: {idea.get('approach', 'N/A')}\n")
        out.append(f"- **배운 점**: {idea.get('lesson', 'N/A')}\n\n")

        out.append("## 복잡도 분석\n")
        out.append(f"**시간 복잡도**: {complexity.get('time_complexity', 'N/A')}\n")
        out.append(f"_{complexity.get('time_explanation', '')}_\n\n")
        out.append(f"**공간 복잡도**: {complexity.get('space_complexity', 'N/A')}\n")
        out.append(f"_{complexity.get('space_explanation', '')}_\n\n")

    else: # AI 분석 실패 시 기본 템플릿
        out.append("## 문제 요약\n\n***\n\n## 풀이 아이디어\n\n## 복잡도 분석\n\n")

    out.append("## 파이썬 코드\n")
    out.append(f"```python\n{code}\n```\n\n")

    out.append("## 문제 링크\n")
    out.append(f"{BASE}{num}\n")
    
    return "".join(out)

def main():
    ap = argparse.ArgumentParser(description="BOJ 풀이 → AI 기반 블로그 Markdown 자동 생성")
    ap.add_argument("--src", required=True, help="파이썬 풀이 파일 경로")
    ap.add_argument("--outdir", default="posts", help="Markdown 출력 폴더 (기본: posts)")
    args = ap.parse_args()

    src = pathlib.Path(args.src)
    if not src.exists():
        raise FileNotFoundError(f"소스 파일을 찾을 수 없습니다: {src}")

    lines = src.read_text(encoding="utf-8").splitlines(True)
    meta = parse_meta(lines)

    if "num" not in meta:
        raise ValueError("메타 주석에 '백준 문제번호'가 필요합니다. (예: '# 백준 1940')")

    code = extract_code(lines)
    if not code:
        raise ValueError("코드 내용이 비어 있습니다.")

    print(f"[INFO] 문제 번호 {meta['num']} 분석 시작...")
    problem_info = fetch_problem(meta["num"])
    if not problem_info:
        raise ConnectionError(f"백준에서 문제 정보를 가져오는 데 실패했습니다: {meta['num']}")
    
    meta["fetched_title"] = problem_info["title"]
    print(f"[INFO] 문제 제목: {problem_info['title']}")

    print("[INFO] AI를 통해 코드 분석 및 해설 생성 중...")
    ai_analysis = analyze_with_ai(problem_info, code)
    if not ai_analysis:
        print("[WARN] AI 분석에 실패하여 기본 템플릿으로 생성합니다.", file=sys.stderr)

    md_content = build_markdown(meta, code, ai_analysis)

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[\s/\\?%*:|"<>]', '-', problem_info["title"])
    fname = f"{today}-boj-{meta['num']}-{safe_title}.md"
    outpath = outdir / fname

    outpath.write_text(md_content, encoding="utf-8")
    print(f"\n[SUCCESS] 생성 완료! → {outpath}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[FATAL] 스크립트 실행 중 오류가 발생했습니다: {e}", file=sys.stderr)
        sys.exit(1)
# python boj_post.py --src 1940.py