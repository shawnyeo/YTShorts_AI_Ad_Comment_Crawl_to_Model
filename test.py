# %%
#✅ ✅ ① setup_driver()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    # 옵션 원하는 대로 추가
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    return driver


# %%
#✅ ✅ ② open_shorts_page()
def open_shorts_page(driver, url):
    driver.get(url)
    print(f"✅ 페이지 열림: {url}")
    time.sleep(5)


# %%
#✅ ✅ ③ click_comment_button()
def click_comment_button(driver):
    try:
        comment_button = driver.find_element(By.CSS_SELECTOR, "#comments-button")
        comment_button.click()
        print("✅ 댓글 버튼 클릭 완료")
        time.sleep(3)
    except Exception as e:
        print("❌ 댓글 버튼 클릭 실패:", e)
        raise


# %%
# ✅ ✅ ④ find_scroll_container()
def find_scroll_container(driver):
    try:
        container = driver.find_element(By.CSS_SELECTOR, "ytd-item-section-renderer #contents")
        print("✅ 댓글창 스크롤 컨테이너 찾음")
        return container
    except Exception as e:
        print("❌ 스크롤 컨테이너 못 찾음:", e)
        raise


# %%
def human_like_scroll(driver, container, wait_time=3, max_rounds=50):
    print("\n✅ 사람스러운 무한스크롤 시작")
    prev_height = driver.execute_script("return arguments[0].scrollHeight;", container)

    for i in range(max_rounds):
        print(f"👉 스크롤 {i+1}회")

        # 1. 바닥까지
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", container)
        print("✅ 바닥까지 스크롤")

        # 2. 기다림
        print(f"⏱️ wait {wait_time}s")
        time.sleep(wait_time)

        # 3. 높이 변화 체크
        new_height = driver.execute_script("return arguments[0].scrollHeight;", container)
        print(f"📏 scrollHeight 변화: {prev_height} -> {new_height}")

        if new_height == prev_height:
            print("✅ 더 이상 continuation 없음. 스크롤 종료.")
            break

        prev_height = new_height

    print("✅ 스크롤 루프 완료\n")


# %%
#✅ ✅ ⑥ parse_comments()
from bs4 import BeautifulSoup

def parse_comments_soup(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    all_threads = soup.select('ytd-comment-thread-renderer')
    print(f"✅ 찾은 댓글 블록 수: {len(all_threads)}")

    for thread in all_threads:
        # AUTHOR
        author_tag = thread.select_one('a#author-text')
        if not author_tag:
            author_tag = thread.select_one('span.style-scope.ytd-comment-view-model')
        author_text = author_tag.get_text(strip=True) if author_tag else "N/A"

        # CONTENT
        content_tag = thread.select_one('yt-attributed-string#content-text')
        if not content_tag:
            content_tag = thread.select_one('span.yt-core-attributed-string')
        content_text = content_tag.get_text(strip=True) if content_tag else "N/A"

        results.append((author_text, content_text))

    print(f"✅ 파싱 완료. 총 댓글 수: {len(results)}")
    return results



# %%
#✅ ✅ ⑦ 전체 메인 플로우
if __name__ == "__main__":
    driver = setup_driver()

    # 🎯 1. 페이지 열기
    url = "https://www.youtube.com/shorts/JssAW9IruVo"
    open_shorts_page(driver, url)

    # 🎯 2. 댓글 버튼 열기
    click_comment_button(driver)

    # 🎯 3. 댓글창 스크롤 컨테이너 찾기
    container = find_scroll_container(driver)

    # 🎯 4. 스크롤 → continuation 모두 불러오기
    human_like_scroll(driver, container)

    # 🎯 5. 파싱
    comment_data = parse_comments_soup(driver)

    # 🎯 6. 출력
    for idx, (author, text) in enumerate(comment_data, start=1):
        print(f"{idx}. {author}: {text}")

    # # 🎯 7. 종료
    # driver.quit()


# %%



