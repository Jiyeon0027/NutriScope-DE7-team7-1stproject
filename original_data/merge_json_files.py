import json
import pandas as pd
import os


def merge_json_files_with_dataframe():
    """
    4개의 JSON 파일을 데이터프레임으로 읽어서 합치고 각 데이터에 고유 ID를 추가합니다.
    각 파일에서 상위 100개씩만 선택합니다.
    """
    # 원하는 열 이름들 (순서대로)
    target_columns = [
        "id",
        "shop_name",
        "display_name",
        "brand_name",
        "original_price",
        "sale_price",
        "image_url",
        "rank",
    ]

    # JSON 파일 경로들과 해당 쇼핑몰 정보
    json_files = [
        ("kurly_products_int.json", "kurly"),
        ("gmarket_product_list_20250929_1.json", "gmarket"),
        ("data.json", "iHerb"),
        ("kakao_gift_products.json", "Kakao Gift"),
    ]

    dataframes = []

    for file_path, shop_name in json_files:
        print(f"처리 중: {file_path}")

        try:
            # JSON 파일을 데이터프레임으로 읽기
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            df = pd.DataFrame(data)

            # shop_name이 없는 경우 추가
            if "shop_name" not in df.columns:
                df["shop_name"] = shop_name

            # 상위 100개 선택
            if "rank" in df.columns:
                # rank 컬럼이 있으면 rank 기준으로 정렬하여 상위 100개 선택
                df_top100 = df.sort_values("rank").head(100)
                print(f"  - rank 기준으로 상위 100개 선택")
            else:
                # rank 컬럼이 없으면 처음 100개 선택
                df_top100 = df.head(100)
                print(f"  - 처음 100개 선택")

            # 필요한 열들만 선택 (id 제외)
            available_columns = [
                col for col in target_columns[1:] if col in df_top100.columns
            ]
            df_selected = df_top100[available_columns].copy()

            # 없는 열들은 None으로 채우기
            for col in target_columns[1:]:
                if col not in df_selected.columns:
                    df_selected[col] = None

            # 열 순서 맞추기 (id 제외)
            df_selected = df_selected[target_columns[1:]]

            dataframes.append(df_selected)
            print(f"  - {len(df_selected)}개 항목 추가됨")
            print(f"  - 사용된 열: {list(df_selected.columns)}")

        except Exception as e:
            print(f"  - 오류 발생: {e}")

    # 모든 데이터프레임 합치기
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)

        # ID 추가 (1부터 시작) - 첫 번째 위치에
        merged_df.insert(0, "id", range(1, len(merged_df) + 1))

        # 최종 열 순서 맞추기
        merged_df = merged_df[target_columns]

        print(f"\n총 {len(merged_df)}개 항목이 합쳐졌습니다.")

        # 데이터프레임 정보 출력
        print(f"\n데이터프레임 정보:")
        print(f"  - 행 수: {len(merged_df)}")
        print(f"  - 열 수: {len(merged_df.columns)}")
        print(f"  - 열 이름: {list(merged_df.columns)}")

        # 쇼핑몰별 통계
        print(f"\n쇼핑몰별 통계:")
        shop_counts = merged_df["shop_name"].value_counts()
        for shop, count in shop_counts.items():
            print(f"  - {shop}: {count}개")

        # 결측값 확인
        print(f"\n결측값 확인:")
        missing_data = merged_df.isnull().sum()
        for col, missing_count in missing_data.items():
            if missing_count > 0:
                print(f"  - {col}: {missing_count}개")

        # 데이터프레임을 JSON으로 저장
        output_file = "merged_products_top100.json"
        merged_df.to_json(
            output_file, orient="records", force_ascii=False, indent=2
        )
        print(f"\n{output_file}에 저장되었습니다.")

        # CSV로도 저장 (선택사항)
        csv_file = "merged_products_top100.csv"
        merged_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
        print(f"{csv_file}에도 저장되었습니다.")

        # 샘플 데이터 출력
        print(f"\n샘플 데이터 (처음 3개):")
        print(merged_df.head(3).to_string())

        return merged_df
    else:
        print("처리할 데이터가 없습니다.")
        return None


if __name__ == "__main__":
    # 데이터 합치기
    merged_df = merge_json_files_with_dataframe()
