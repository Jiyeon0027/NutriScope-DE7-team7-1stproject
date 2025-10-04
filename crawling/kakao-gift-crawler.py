import json
import time
import re

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class KakaoGiftCrawler:
    def __init__(self):
        self.base_url = (
            "https://gift.kakao.com/ranking/best/delivery/8?priceRange=ALL"
        )
        self.base_url_detail = "https://gift.kakao.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) "
            + "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
            + "image/webp,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def setup_selenium_driver(self, headless=True):
        """Selenium 드라이버 설정"""
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            f'--user-agent={self.headers["User-Agent"]}'
        )

        # 추가 안정성 옵션
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        chrome_options.add_experimental_option("useAutomationExtension", False)

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            return driver
        except Exception as e:
            print(f"Chrome 드라이버 설정 실패: {e}")
            return None

    def is_jpg_image(self, image_url):
        """이미지 URL이 JPG인지 확인"""
        if not image_url or image_url == "이미지 없음":
            return False

        # URL에서 확장자 확인
        if ".jpg" in image_url.lower() or ".jpeg" in image_url.lower():
            return True

        # 카카오 이미지 URL 패턴 확인
        if "kakaocdn.net" in image_url and "fwebp" in image_url:
            # fname 파라미터에서 실제 확장자 확인
            if "fname=" in image_url:
                fname_part = image_url.split("fname=")[1]
                if (
                    ".jpg" in fname_part.lower()
                    or ".jpeg" in fname_part.lower()
                ):
                    return True

        return False

    def extract_product_data(self, element):
        """상품 요소에서 데이터 추출"""
        try:
            # 순위 추출
            rank_element = element.find_element(By.CSS_SELECTOR, ".num_rank")
            rank = int(rank_element.text.strip()) if rank_element else -1

            # 브랜드명 추출
            brand_element = element.find_element(By.CSS_SELECTOR, ".txt_brand")
            brand_name = (
                brand_element.text.strip() if brand_element else "브랜드 없음"
            )

            # 상품명 추출
            product_name_element = element.find_element(
                By.CSS_SELECTOR, ".txt_prdname"
            )
            display_name = (
                product_name_element.text.strip()
                if product_name_element
                else "상품명 없음"
            )

            # 상품 링크 추출 (shop_name을 위해)
            link_element = element.find_element(By.CSS_SELECTOR, ".link_thumb")
            product_link = (
                link_element.get_attribute("href") if link_element else ""
            )

            product_data = {
                "shop_name": "Kakao Gift",  # 기본값
                "display_name": display_name,
                "brand_name": brand_name,
                "rank": rank,
                "product_link": product_link,
            }

            return product_data

        except Exception as e:
            print(f"상품 데이터 추출 중 오류: {e}")
            return None

    def crawl_product_detail(self, product):
        """상품 상세 크롤링"""
        try:
            # Selenium 드라이버 설정
            driver = self.setup_selenium_driver(headless=True)
            if not driver:
                print(f"드라이버 설정 실패: {product['product_link']}")
                return None

            # 상품 상세 페이지로 이동
            detail_url = product["product_link"]
            print(f"상세 페이지 크롤링: {detail_url}")

            driver.get(detail_url)
            time.sleep(3)

            detail_data = {}

            # 1. 썸네일 이미지 (class='thumb_product' 내의 첫 번째 이미지)
            try:
                thumb_container = driver.find_element(
                    By.CSS_SELECTOR, ".thumb_product"
                )
                thumb_img = thumb_container.find_element(By.TAG_NAME, "img")
                thumbnail_url = thumb_img.get_attribute("src")
                detail_data["image_url"] = thumbnail_url
                print(f"  - 썸네일: {thumbnail_url}")
            except Exception as e:
                print(f"  - 썸네일 추출 실패: {e}")
                detail_data["image_url"] = None

            # 2. txt_total 판매가
            try:
                total_element = driver.find_element(
                    By.CSS_SELECTOR, ".txt_total"
                )
                total_text = total_element.text.strip()
                total_number = re.sub(r"[^\d]", "", total_text)
                detail_data["sale_price"] = int(
                    total_number if total_number else "0"
                )
                print(f"  - 판매가: {total_text} -> {total_number}")
            except Exception as e:
                print(f"  - txt_total 판매가 추출 실패: {e}")
                detail_data["sale_price"] = 0

            # 3. txt_price 정상가
            try:
                price_element = driver.find_element(
                    By.CSS_SELECTOR, ".txt_price"
                )
                price_text = price_element.text.strip()
                price_number = re.sub(r"[^\d]", "", price_text)
                detail_data["original_price"] = int(
                    price_number if price_number else "0"
                )
                print(f"  - 정상가: {price_text} -> {price_number}")
            except Exception as e:
                print(f"  - txt_price 정상가 추출 실패: {e}")
                detail_data["original_price"] = 0

            driver.quit()
            return detail_data

        except Exception as e:
            print(f"상품 상세 크롤링 중 오류: {e}")
            if "driver" in locals():
                driver.quit()
            return None

    def crawl_with_selenium(self):
        """Selenium을 사용한 크롤링"""
        driver = self.setup_selenium_driver(headless=False)

        if not driver:
            print("Selenium 드라이버 설정 실패")
            return None

        try:
            print("페이지 로딩 중...")
            driver.get(self.base_url)
            time.sleep(5)

            products = []
            seen_products = set()  # 중복 제거
            scroll_count = 0
            max_scrolls = 30
            scroll_distance = 800  # 한 번에 스크롤할 픽셀 수

            while scroll_count < max_scrolls:
                print(f"\n=== 스크롤 {scroll_count + 1}회차 ===")

                # 상품 요소들 찾기
                elements = driver.find_elements(By.CSS_SELECTOR, "app-product")
                print(f"발견된 상품 수: {len(elements)}")

                if not elements:
                    print("상품을 찾을 수 없습니다.")
                    break

                # 각 상품에서 데이터 추출
                for i, element in enumerate(elements):
                    product_data = self.extract_product_data(element)

                    if product_data:
                        # 중복 제거
                        product_key = product_data["product_link"]
                        if product_key not in seen_products:
                            seen_products.add(product_key)
                            products.append(product_data)
                            print(f"  - 순위: {product_data['rank']}")
                            print(f"  - 브랜드: {product_data['brand_name']}")

                print(f"스크롤 다운 중... ({scroll_distance}px)")
                driver.execute_script(
                    f"window.scrollBy(0, {scroll_distance});"
                )

                if len(products) == 100:
                    break

                time.sleep(3)
                scroll_count += 1

            print(f"\n총 {len(products)}개의 상품 데이터를 수집했습니다.")
            return products

        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")
            return None
        finally:
            driver.quit()
            print("브라우저가 종료되었습니다.")

    def save_to_json(self, products, filename="kakao_gift_products.json"):
        """결과를 JSON 파일로 저장"""
        if not products:
            print("저장할 데이터가 없습니다.")
            return

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"결과가 {filename}에 저장되었습니다.")

    def save_to_csv(self, products, filename="kakao_gift_products.csv"):
        """결과를 CSV 파일로 저장"""
        if not products:
            print("저장할 데이터가 없습니다.")
            return

        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"결과가 {filename}에 저장되었습니다.")

    def run(self):
        """크롤링 실행"""
        print("카카오 기프트 배송 랭킹 크롤링 시작...")
        print(f"대상 URL: {self.base_url}")

        products = self.crawl_with_selenium()

        if products is None:
            print("크롤링된 데이터가 없습니다.")
            return

        print(f"크롤링된 데이터: {len(products)}개")

        # 상품 상세 크롤링
        for i, product in enumerate(products):
            print(f"\n상세 크롤링 진행: {i+1}/{len(products)}")
            product_detail = self.crawl_product_detail(product)
            if product_detail:
                product.update(product_detail)

        # JSON과 CSV로 저장
        self.save_to_json(products)
        self.save_to_csv(products)


if __name__ == "__main__":
    crawler = KakaoGiftCrawler()
    crawler.run()
