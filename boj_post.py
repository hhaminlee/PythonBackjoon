#!/usr/bin/env python3
import argparse, re, pathlib, sys, time, os, json
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드 (스크립트와 같은 폴더의 .env)
load_dotenv(pathlib.Path(__file__).parent / ".env")

# --- 네트워킹 / 파싱 의존성 ---
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] 'requests'와 'beautifulsoup4' 라이브러리가 필요합니다. 'pip install requests beautifulsoup4'", file=sys.stderr)
    sys.exit(1)


# --- 기존 유틸리티 함수 ---

UA = "Mozilla/5.0 (compatible; BOJ-Blog-Generator/3.0; +https://example.local)"
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

# --- AI 백엔드 ---

def _call_ollama(prompt):
    """Ollama 로컬 모델로 프롬프트를 보내고 응답 텍스트를 반환한다."""
    import subprocess
    result = subprocess.run(
        ['ollama', 'run', 'qwen2.5:7b'],
        input=prompt,
        capture_output=True,
        timeout=300,
        encoding="utf-8",
        errors="ignore"
    )
    if result.returncode != 0:
        print(f"[ERROR] Ollama 실행 실패: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout.strip()

def _call_gemini(prompt):
    """Gemini API로 프롬프트를 보내고 응답 텍스트를 반환한다."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.", file=sys.stderr)
        print("  .env 파일에 GEMINI_API_KEY=your_key 를 추가하거나", file=sys.stderr)
        print("  https://aistudio.google.com/apikey 에서 발급받으세요.", file=sys.stderr)
        return None
    try:
        resp = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=60
        )
        if resp.status_code != 200:
            print(f"[ERROR] Gemini API 오류: {resp.status_code} {resp.text[:200]}", file=sys.stderr)
            return None
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"[ERROR] Gemini API 호출 실패: {e}", file=sys.stderr)
        return None

def _call_ai(prompt, backend="gemini"):
    """선택한 백엔드로 AI를 호출한다."""
    if backend == "gemini":
        return _call_gemini(prompt)
    else:
        return _call_ollama(prompt)

def _parse_json_response(response_text):
    """AI 응답에서 JSON을 추출한다."""
    if not response_text:
        return None
    try:
        json_text = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_text:
            json_str = json_text.group(1)
        else:
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text.strip()

        import unicodedata
        json_str = ''.join(char for char in json_str if unicodedata.category(char)[0] != 'C' or char in '\n\r\t')
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        json_str = re.sub(r'([^\\])\n', r'\1 ', json_str)

        return json.loads(json_str)
    except Exception as e:
        print(f"[ERROR] JSON 파싱 실패: {e}", file=sys.stderr)
        print(f"AI 응답 내용: {response_text[:500]}", file=sys.stderr)
        return None

# --- AI 분석 로직 ---

ANALYZE_PROMPT = """한국어로 답변하세요.

백준 문제와 파이썬 코드를 분석해서 JSON으로 답하세요.

### 문제
제목: {title}
{description}

### 코드
```python
{code}
```

다음 JSON 형식으로만 답하세요:

{{
  "tag": "알고리즘 분류 한 단어 (예: 그리디, DFS, DP, 구현, 정렬, 브루트포스, 문자열)",
  "idea": "이 문제를 풀기 위한 핵심 아이디어를 2-3문장으로 설명. 왜 이 방법을 쓰는지, 어떤 발상이 필요한지.",
  "steps": [
    "코드의 구현 흐름을 단계별로 설명. 한 단계당 1-2문장.",
    "각 단계에서 코드가 실제로 뭘 하는지 구체적으로.",
    "최대 4단계."
  ]
}}

규칙:
- "~했습니다", "~됩니다", "~것 같습니다" 같은 자연스러운 합니다체를 쓰세요.
- "~합니다만", "~였습니다만" 같은 딱딱한 표현은 쓰지 마세요.
- 독자가 처음 이 알고리즘을 접한다고 가정하고 쉽게 설명하세요.
- idea에는 "왜 이렇게 푸는지"를 꼭 포함하세요."""

POLISH_PROMPT = """아래 메모를 다듬어줘. 규칙:
- 원래 내용과 단어 선택을 최대한 그대로 유지
- 맞춤법, 띄어쓰기만 고치고 문장이 자연스럽게 읽히도록 약간만 손봐
- 내용을 추가하거나 늘리지 마
- 말투를 "~했습니다", "~됩니다", "~것 같습니다" 같은 자연스러운 합니다체로 통일
- "~합니다만", "~였습니다만" 같은 딱딱하고 어색한 표현은 절대 쓰지 마. 대신 "~했는데", "~지만" 등으로 자연스럽게 연결해
- 다듬은 문장만 출력하고 다른 말 붙이지 마

메모: {memo}"""

TRANSLATE_PROMPT = """아래 문제 설명이 영어라면 한국어로 자연스럽게 번역하세요.
이미 한국어라면 그대로 출력하세요.
번역문만 출력하고 다른 말 붙이지 마세요.

{text}"""

def translate_if_english(text, backend="gemini"):
    """텍스트가 영어면 한국어로 번역한다."""
    if re.search(r'[가-힣]', text):
        return text
    prompt = TRANSLATE_PROMPT.format(text=text)
    try:
        translated = _call_ai(prompt, backend)
        if not translated:
            return text
        return translated
    except Exception:
        return text

def analyze_with_ai(problem_info, code, backend="gemini"):
    """코드의 접근 방식과 알고리즘 분류를 생성한다."""
    prompt = ANALYZE_PROMPT.format(
        title=problem_info['title'],
        description=problem_info['description'],
        code=code
    )
    response_text = _call_ai(prompt, backend)
    return _parse_json_response(response_text)

def polish_memo(memo, backend="gemini"):
    """메모를 말투는 유지하면서 문장만 살짝 다듬는다."""
    prompt = POLISH_PROMPT.format(memo=memo)
    try:
        polished = _call_ai(prompt, backend)
        if not polished or len(polished) > len(memo) * 3:
            return memo
        return polished
    except Exception:
        return memo

# --- 마크다운 생성 ---

def build_markdown(meta, code, ai_analysis, memo=None, backend="gemini", description=""):
    """분석 결과를 바탕으로 마크다운 포스트를 생성합니다."""
    num = meta["num"]
    title = meta.get("title") or meta.get("fetched_title", "")

    style = """<style>
.boj-post {
    max-width: 800px;
    margin: 0 auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.8;
    color: #1a1a1a;
}
.problem-header {
    border-bottom: 2px solid #1a1a1a;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
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
.tag {
    display: inline-block;
    background: #f0f0f0;
    color: #333;
    padding: 0.2rem 0.6rem;
    border-radius: 3px;
    font-size: 0.85rem;
    font-weight: 500;
    margin-left: 0.5rem;
}
.toc {
    background: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 1rem 1.5rem;
    margin-bottom: 2.5rem;
}
.toc p {
    margin: 0 0 0.5rem 0;
    font-weight: 600;
    font-size: 0.95rem;
}
.toc ul {
    margin: 0;
    padding-left: 1.2rem;
    list-style: none;
}
.toc li {
    padding: 0.15rem 0;
    font-size: 0.9rem;
}
.toc a {
    color: #333;
    text-decoration: none;
    border-bottom: 1px dashed #999;
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
    padding-left: 0.5rem;
    color: #333;
}
.section-content p {
    margin: 0.5rem 0;
}
.step-item {
    padding: 0.4rem 0;
    color: #333;
}
.memo-box {
    background: #fafafa;
    border-left: 3px solid #999;
    padding: 1rem 1.25rem;
    color: #333;
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
    margin-top: 2rem;
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

    tag = ""
    idea = ""
    steps = []
    summary = description
    if ai_analysis:
        tag = ai_analysis.get("tag", "")
        idea = ai_analysis.get("idea", "")
        steps = ai_analysis.get("steps", [])

    # 헤더
    out.append('<div class="problem-header">\n')
    out.append(f"<h1>{title}</h1>\n")
    out.append(f'<div class="problem-meta">')
    out.append(f'<a href="{BASE}{num}" target="_blank">백준 {num}번</a>')
    if tag:
        out.append(f'<span class="tag">{tag}</span>')
    out.append('</div>\n')
    out.append("</div>\n\n")

    # 목차
    toc_items = ['<li><a href="#summary">문제 요약</a></li>']
    toc_items.append('<li><a href="#idea">아이디어</a></li>')
    if steps:
        toc_items.append('<li><a href="#impl">구현</a></li>')
    toc_items.append('<li><a href="#code">코드</a></li>')
    if memo:
        toc_items.append('<li><a href="#memo">메모</a></li>')

    out.append('<div class="toc">\n')
    out.append("<p>목차</p>\n")
    out.append("<ul>\n")
    for item in toc_items:
        out.append(f"  {item}\n")
    out.append("</ul>\n")
    out.append("</div>\n\n")

    # 문제 요약
    out.append('<div class="section" id="summary">\n')
    out.append("<h2>문제 요약</h2>\n")
    out.append(f'<div class="section-content">\n<p>{summary}</p>\n</div>\n')
    out.append("</div>\n\n")

    # 아이디어
    out.append('<div class="section" id="idea">\n')
    out.append("<h2>아이디어</h2>\n")
    out.append(f'<div class="section-content">\n<p>{idea}</p>\n</div>\n')
    out.append("</div>\n\n")

    # 구현
    if steps:
        out.append('<div class="section" id="impl">\n')
        out.append("<h2>구현</h2>\n")
        out.append('<div class="section-content">\n')
        for i, step in enumerate(steps, 1):
            out.append(f'<div class="step-item"><strong>{i}.</strong> {step}</div>\n')
        out.append("</div>\n")
        out.append("</div>\n\n")

    # 코드
    out.append('<div class="section" id="code">\n')
    out.append("<h2>코드</h2>\n")
    out.append('<pre><code class="language-python">')
    escaped_code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    out.append(escaped_code)
    out.append('</code></pre>\n')
    out.append("</div>\n\n")

    # 메모 (있을 때만)
    if memo:
        print("[INFO] 메모 다듬는 중...")
        memo = polish_memo(memo, backend)
        out.append('<div class="section" id="memo">\n')
        out.append("<h2>메모</h2>\n")
        out.append(f'<div class="memo-box">{memo}</div>\n')
        out.append("</div>\n\n")

    # 푸터
    out.append('<div class="footer-meta">\n')
    out.append(f'<a href="{BASE}{num}" target="_blank">백준 {num}번 문제 바로가기</a>\n')
    out.append("</div>\n\n")

    out.append("</div>\n")

    return "".join(out)

def main():
    ap = argparse.ArgumentParser(description="BOJ 풀이 → 블로그 포스트 생성")
    ap.add_argument("--src", required=True, help="파이썬 풀이 파일 경로")
    ap.add_argument("--memo", default=None, help="직접 쓰는 메모 (시행착오, 느낀 점 등)")
    ap.add_argument("--ai", default="gemini", choices=["gemini", "ollama"], help="AI 백엔드 선택 (기본: gemini)")
    ap.add_argument("--outdir", default="posts", help="출력 폴더 (기본: posts)")
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

    print(f"[INFO] 문제 번호 {meta['num']} 분석 시작... (AI: {args.ai})")
    problem_info = fetch_problem(meta["num"])
    if not problem_info:
        raise ConnectionError(f"백준에서 문제 정보를 가져오는 데 실패했습니다: {meta['num']}")

    meta["fetched_title"] = problem_info["title"]
    print(f"[INFO] 문제 제목: {problem_info['title']}")

    print("[INFO] AI 분석 중...")
    ai_analysis = analyze_with_ai(problem_info, code, backend=args.ai)
    if not ai_analysis:
        print("[WARN] AI 분석 실패, 분류/접근 없이 생성합니다.", file=sys.stderr)

    # 문제 설명이 영어면 번역
    description = translate_if_english(problem_info["description"], backend=args.ai)

    md_content = build_markdown(meta, code, ai_analysis, memo=args.memo, backend=args.ai, description=description)

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
        print(f"\n[FATAL] {e}", file=sys.stderr)
        sys.exit(1)
# 사용법:
#   python boj_post.py --src 6186.py --ai gemini
#   python boj_post.py --src 6186.py --ai ollama
#   python boj_post.py --src 6186.py --ai gemini --memo "dfs 배우고 처음 풀어본 문제"
