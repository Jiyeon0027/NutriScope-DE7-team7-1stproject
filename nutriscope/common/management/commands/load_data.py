"""
JSON 데이터를 데이터베이스에 로드하는 Django 관리 명령어
"""

import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from common.models import NutriScopeData


class Command(BaseCommand):
    help = "JSON 파일에서 제품 데이터를 로드합니다"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="merged_products_top100_preprocessed_fin.json",
            help="로드할 JSON 파일명 (기본값: merged_products_top100_preprocessed_fin.json)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="기존 데이터를 모두 삭제한 후 새로 로드합니다",
        )

    def handle(self, *args, **options):
        file_name = options["file"]
        clear_existing = options["clear"]

        # 파일 경로 설정 (프로젝트 루트에서 data 폴더 찾기)
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
        )
        file_path = os.path.join(
            base_dir, "data", "preprocessed-data", file_name
        )

        # 파일 존재 확인
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f"파일을 찾을 수 없습니다: {file_path}")
            )
            return

        # 기존 데이터 삭제 (옵션)
        if clear_existing:
            deleted_count = NutriScopeData.objects.all().delete()[0]
            self.stdout.write(
                self.style.WARNING(
                    f"기존 데이터 {deleted_count}개를 삭제했습니다."
                )
            )

        # JSON 파일 읽기
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"JSON 파일을 읽는 중 오류가 발생했습니다: {e}"
                )
            )
            return

        # 데이터 검증 및 로드
        created_count = 0
        updated_count = 0
        error_count = 0

        for item in data:
            try:
                # 필수 필드 확인
                required_fields = [
                    "id",
                    "shop_name",
                    "display_name",
                    "product_name",
                    "quantity",
                    "brand_name",
                    "sale_price",
                    "image_url",
                    "rank",
                    "category",
                ]

                for field in required_fields:
                    if field not in item:
                        raise ValueError(f"필수 필드 누락: {field}")

                # 데이터 생성 또는 업데이트
                obj, created = NutriScopeData.objects.update_or_create(
                    id=item["id"],
                    defaults={
                        "shop_name": item["shop_name"],
                        "display_name": item["display_name"],
                        "product_name": item["product_name"],
                        "quantity": item["quantity"],
                        "brand_name": item["brand_name"],
                        "original_price": item.get("original_price"),
                        "sale_price": item["sale_price"],
                        "image_url": item["image_url"],
                        "rank": item["rank"],
                        "category": item["category"],
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'ID {item.get("id", "unknown")} 처리 중 오류: {e}'
                    )
                )

        # 결과 출력
        self.stdout.write(
            self.style.SUCCESS(
                f"\n데이터 로드 완료!\n"
                f"- 새로 생성: {created_count}개\n"
                f"- 업데이트: {updated_count}개\n"
                f"- 오류: {error_count}개\n"
                f"- 총 처리: {len(data)}개"
            )
        )

        # 최종 데이터베이스 상태 확인
        total_count = NutriScopeData.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"현재 데이터베이스에 총 {total_count}개의 제품이 저장되어 있습니다."
            )
        )
