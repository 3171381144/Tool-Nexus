import argparse

from app.app import create_app
from app.seed import bootstrap_database


app = create_app()


def main() -> None:
    parser = argparse.ArgumentParser(description="Portal Auth Service utility")
    parser.add_argument("--init-db", action="store_true", help="初始化数据库并写入测试数据")
    args = parser.parse_args()

    if args.init_db:
        bootstrap_database()
        print("数据库初始化完成。")
    else:
        print("请使用: python -m uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
