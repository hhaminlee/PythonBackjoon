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
        print(f"[DEBUG] 캐시에서 로딩: {cache_file}")
        html_text = cache_file.read_text(encoding="utf-8")
    else:
        url = f"{BASE}{num}"
        print(f"[DEBUG] URL 요청: {url}")
        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
            print(f"[DEBUG] 응답 코드: {resp.status_code}")
            if resp.status_code == 200:
                html_text = resp.text
                cache_file.write_text(html_text, encoding="utf-8")
                time.sleep(0.5)
            else:
                print(f"[ERROR] HTTP 오류: {resp.status_code}")
                return None
        except requests.RequestException as e:
            print(f"[ERROR] 네트워크 요청 실패: {e}")
            return None

    try:
        soup = BeautifulSoup(html_text, "html.parser")
        
        title_elem = soup.select_one("#problem_title")
        desc_elem = soup.select_one("#problem_description")
        
        print(f"[DEBUG] title 요소 발견: {title_elem is not None}")
        print(f"[DEBUG] description 요소 발견: {desc_elem is not None}")
        
        if not title_elem:
            print("[ERROR] #problem_title 요소를 찾을 수 없습니다")
            return None
        if not desc_elem:
            print("[ERROR] #problem_description 요소를 찾을 수 없습니다")
            return None
            
        title = title_elem.get_text(strip=True)
        description = desc_elem.get_text("\n", strip=True)
        
        print(f"[DEBUG] 제목: {title}")
        return {"title": title, "description": description}
        
    except Exception as e:
        print(f"[ERROR] HTML 파싱 중 오류: {e}")
        import traceback
        traceback.print_exc()
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
    다음 백준 문제와 실제 작성한 파이썬 코드를 분석해서 **코드에 실제로 구현된 내용만** 기반으로 JSON을 생성하세요.
    코드에 없는 내용은 절대 추측하지 마세요. 주석이 있다면 주석 분석을 최우선으로 하세요.

    ### 문제
    제목: {problem_info['title']}
    {problem_info['description']}

    ### 제 코드
    ```python
    {code}
    ```

    ### JSON 출력 형식 (반드시 이 형식으로만 답변)
    {{
      "problem_core": "문제의 핵심을 한 문장으로 설명",

      "code_flow": {{
        "step1": "코드의 첫 번째 주요 로직 (주석이나 실제 코드 기준)",
        "step2": "코드의 두 번째 주요 로직",
        "step3": "코드의 세 번째 주요 로직 (없으면 생략)"
      }},

      "trial_and_error": [
        {{
          "issue": "시행착오 상황 (주석에 '틀림', '오류', '수정' 등이 있을 경우만)",
          "solution": "해결 방법"
        }}
      ],

      "code_points": [
        "코드에서 눈여겨볼 특징 1 (실제 코드 기준)",
        "코드에서 눈여겨볼 특징 2"
      ],

      "key_lesson": "이 코드를 통해 배운 핵심 한 가지 (1문장)"
    }}

    **중요 지침**:
    1. 주석에 있는 내용을 최우선으로 분석하세요
    2. 코드에 없는 내용은 절대 지어내지 마세요
    3. trial_and_error는 주석에 명시적으로 언급된 경우만 포함하고, 없으면 빈 배열 []로 반환하세요
    4. code_flow의 step3는 정말 중요한 로직이 3개 이상일 때만 포함하세요
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
    today = datetime.now().strftime("%Y-%m-%d")

    # HTML 스타일 정의
    style = """<style>
.boj-post {
    max-width: 800px;
    margin: 0 auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #1a1a1a;
}
.problem-header {
    border-bottom: 2px solid #1a1a1a;
    padding-bottom: 1.5rem;
    margin-bottom: 3rem;
}
.problem-header h1 {
    margin: 0 0 0.5rem 0;
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
}
.problem-meta {
    color: #666;
    font-size: 0.9rem;
}
.problem-meta a {
    color: #1a1a1a;
    text-decoration: none;
    border-bottom: 1px solid #1a1a1a;
}
.section {
    margin-bottom: 2.5rem;
}
.section h2 {
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: #1a1a1a;
    border-left: 3px solid #1a1a1a;
    padding-left: 0.75rem;
}
.section-content {
    padding-left: 1rem;
}
.step-item {
    padding: 0.5rem 0;
    color: #333;
}
.error-box {
    background: #f5f5f5;
    border-left: 3px solid #666;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
}
.error-box h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #1a1a1a;
}
.error-box p {
    margin: 0.5rem 0;
    color: #333;
}
.point-item {
    padding: 0.4rem 0;
    color: #333;
    line-height: 1.8;
}
.lesson-box {
    background: #f5f5f5;
    padding: 1.5rem;
    border-left: 3px solid #1a1a1a;
    font-size: 1rem;
    color: #1a1a1a;
    line-height: 1.8;
}
pre {
    background: #f5f5f5;
    padding: 1.5rem;
    border-radius: 4px;
    overflow-x: auto;
    margin: 1rem 0;
}
code {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #1a1a1a;
}
.footer-meta {
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
    border-top: 1px solid #e0e0e0;
    color: #666;
    font-size: 0.9rem;
}
.footer-meta a {
    color: #1a1a1a;
    text-decoration: none;
    border-bottom: 1px solid #1a1a1a;
}
</style>

<div class="boj-post">

"""

    out = [style]

    # AI 분석 결과가 있을 경우
    if ai_analysis:
        problem_core = ai_analysis.get("problem_core", "")
        code_flow = ai_analysis.get("code_flow", {})
        trial_and_error = ai_analysis.get("trial_and_error", [])
        code_points = ai_analysis.get("code_points", [])
        key_lesson = ai_analysis.get("key_lesson", "")

        # 문제
        out.append('<div class="section">\n')
        out.append("<h2>문제</h2>\n")
        out.append(f'<div class="section-content">\n<p>{problem_core}</p>\n</div>\n')
        out.append("</div>\n\n")

        # 풀이 과정
        out.append('<div class="section">\n')
        out.append("<h2>풀이 과정</h2>\n")
        out.append('<div class="section-content">\n')
        if code_flow.get("step1"):
            out.append(f'<div class="step-item"><strong>1.</strong> {code_flow["step1"]}</div>\n')
        if code_flow.get("step2"):
            out.append(f'<div class="step-item"><strong>2.</strong> {code_flow["step2"]}</div>\n')
        if code_flow.get("step3"):
            out.append(f'<div class="step-item"><strong>3.</strong> {code_flow["step3"]}</div>\n')
        out.append("</div>\n")
        out.append("</div>\n\n")

        # 시행착오 (있을 경우에만)
        if trial_and_error:
            out.append('<div class="section">\n')
            out.append("<h2>시행착오</h2>\n")
            out.append('<div class="section-content">\n')
            for i, item in enumerate(trial_and_error, 1):
                issue = item.get("issue", "")
                solution = item.get("solution", "")
                out.append('<div class="error-box">\n')
                out.append(f"<h3>문제상황 {i}</h3>\n")
                out.append(f"<p>{issue}</p>\n")
                out.append(f"<p><strong>→ 해결:</strong> {solution}</p>\n")
                out.append("</div>\n")
            out.append("</div>\n")
            out.append("</div>\n\n")

        # 핵심 포인트
        if code_points:
            out.append('<div class="section">\n')
            out.append("<h2>핵심 포인트</h2>\n")
            out.append('<div class="section-content">\n')
            for point in code_points:
                out.append(f'<div class="point-item">• {point}</div>\n')
            out.append("</div>\n")
            out.append("</div>\n\n")

        # 배운 점
        if key_lesson:
            out.append('<div class="section">\n')
            out.append("<h2>배운 점</h2>\n")
            out.append(f'<div class="lesson-box">{key_lesson}</div>\n')
            out.append("</div>\n\n")

    else:  # AI 분석 실패 시 기본 템플릿
        out.append('<div class="section">\n<h2>문제</h2>\n<div class="section-content"></div>\n</div>\n\n')
        out.append('<div class="section">\n<h2>풀이 과정</h2>\n<div class="section-content"></div>\n</div>\n\n')
        out.append('<div class="section">\n<h2>핵심 포인트</h2>\n<div class="section-content"></div>\n</div>\n\n')
        out.append('<div class="section">\n<h2>배운 점</h2>\n<div class="lesson-box"></div>\n</div>\n\n')

    # 코드
    out.append('<div class="section">\n')
    out.append("<h2>코드</h2>\n")
    out.append('<pre><code class="language-python">')
    # HTML 특수문자 이스케이프
    escaped_code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    out.append(escaped_code)
    out.append('</code></pre>\n')
    out.append("</div>\n\n")

    # 문제 링크 (맨 마지막, 임베딩 가능)
    out.append('<div class="footer-meta">\n')
    out.append(f'<a href="{BASE}{num}" target="_blank">백준 {num}번 문제 바로가기 →</a>\n')
    out.append("</div>\n\n")

    out.append("</div>\n")

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
# 맥
#   .venv/bin/python boj_post.py --src 4458.py

  # 윈도우
#   .venv\Scripts\python boj_post.py --src 4458.py