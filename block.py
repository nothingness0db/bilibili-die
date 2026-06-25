"""读取 blacklist.json，批量拉黑用户"""

import argparse
import json
import time
import requests


REVIEW_FILE = "review.md"


def load_config():
    with open("config.json", encoding="utf-8") as f:
        return json.load(f)


def get_follower_count(uid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }
    try:
        resp = requests.get(
            "https://api.bilibili.com/x/relation/stat",
            params={"vmid": uid},
            headers=headers,
        ).json()
        if resp["code"] == 0:
            return resp["data"]["follower"]
    except Exception:
        pass
    return 0


def fetch_followers(users):
    print(f"正在查询 {len(users)} 个用户的粉丝数...")
    for i, u in enumerate(users):
        u["follower"] = get_follower_count(u["uid"])
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(users)}")
        time.sleep(0.2)
    print("  查询完成")
    return users


def write_review(users):
    big = [u for u in users if u.get("follower", 0) >= 10000]
    big.sort(key=lambda x: x.get("follower", 0), reverse=True)
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("# 拉黑确认 - 大V列表（粉丝 ≥ 1万）\n\n")
        f.write(f"共 {len(big)} 人，请检查。不想拉黑的删掉对应行。\n\n")
        f.write("| UID | 用户名 | 粉丝数 | 简介 |\n")
        f.write("|-----|--------|--------|------|\n")
        for u in big:
            sign = u.get("sign", "").replace("|", "\\|").replace("\n", " ")
            if len(sign) > 30:
                sign = sign[:30] + "..."
            follower = f"{u['follower']:,}"
            f.write(f"| {u['uid']} | {u['name']} | {follower} | {sign} |\n")
    return big


def read_review():
    """读取 review.md，解析出保留的 UID"""
    uids = []
    with open(REVIEW_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|") or line.startswith("| UID") or line.startswith("|---"):
                continue
            parts = [p.strip() for p in line.split("|")]
            # parts[0] is empty, parts[1] is UID
            try:
                uids.append(int(parts[1]))
            except (ValueError, IndexError):
                pass
    return uids


def block_user(sessdata, bili_jct, uid):
    cookies = {"SESSDATA": sessdata, "bili_jct": bili_jct}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
        "Origin": "https://www.bilibili.com",
    }
    data = {"fid": uid, "act": 5, "re_src": 11, "csrf": bili_jct}
    resp = requests.post(
        "https://api.bilibili.com/x/relation/modify",
        data=data,
        cookies=cookies,
        headers=headers,
    ).json()
    return resp["code"] == 0


def main():
    parser = argparse.ArgumentParser(description="批量拉黑B站用户")
    parser.add_argument("--file", default="blacklist.json", help="黑名单文件路径")
    parser.add_argument("--dry-run", action="store_true", help="只预览不执行拉黑")
    parser.add_argument("--delay", type=float, default=1.0, help="每次请求间隔(秒)")
    parser.add_argument("--skip-review", action="store_true", help="跳过确认，直接拉黑全部")
    args = parser.parse_args()

    with open(args.file, encoding="utf-8") as f:
        bl = json.load(f)

    users = bl["users"]
    print(f"黑名单共 {len(users)} 个用户")

    # 查询粉丝数
    users = fetch_followers(users)

    # 生成 review.md
    big = write_review(users)
    print(f"\n粉丝 ≥ 1万的用户: {len(big)} 人")
    print(f"已生成 {REVIEW_FILE}，请检查后确认。")

    if args.dry_run:
        print("\n--dry-run 模式，未执行拉黑。")
        return

    if not args.skip_review:
        input(f"\n检查完 {REVIEW_FILE} 后，按回车开始拉黑（Ctrl+C 取消）...")

    # 读取 review.md 中保留的 UID
    review_uids = read_review()
    review_set = set(review_uids)

    # 拉黑：大V只拉黑 review.md 中保留的，小号全部拉黑
    config = load_config()
    ok, fail, skip = 0, 0, 0
    for i, u in enumerate(users, 1):
        uid = u["uid"]
        is_big = u.get("follower", 0) >= 10000
        if is_big and uid not in review_set:
            skip += 1
            continue
        try:
            if block_user(config["sessdata"], config["bili_jct"], uid):
                ok += 1
                print(f"[{i}/{len(users)}] ✓ {uid} {u['name']}")
            else:
                fail += 1
                print(f"[{i}/{len(users)}] ✗ {uid} {u['name']} (API 返回失败)")
        except Exception as e:
            fail += 1
            print(f"[{i}/{len(users)}] ✗ {uid} {u['name']} ({e})")
        time.sleep(args.delay)

    print(f"\n完成: 成功 {ok}, 失败 {fail}, 跳过 {skip}")


if __name__ == "__main__":
    main()
