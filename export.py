"""导出你的B站黑名单到 blacklist.json"""

import json
import time
import requests


def load_config():
    with open("config.json", encoding="utf-8") as f:
        return json.load(f)


def get_blacklist(sessdata, bili_jct):
    cookies = {"SESSDATA": sessdata, "bili_jct": bili_jct}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }
    users = []
    page = 1
    while True:
        resp = requests.get(
            "https://api.bilibili.com/x/relation/blacks",
            params={"pn": page, "ps": 50, "relation": 0},
            cookies=cookies,
            headers=headers,
        ).json()
        if resp["code"] != 0:
            print(f"API 错误: {resp}")
            break
        data = resp["data"]
        for u in data["list"]:
            users.append({
                "uid": u["mid"],
                "name": u["uname"],
                "sign": u.get("sign", ""),
                "blocked_at": time.strftime("%Y-%m-%d", time.localtime(u["mtime"])),
            })
        print(f"第 {page} 页，已获取 {len(users)}/{data['total']} 个用户")
        if len(users) >= data["total"]:
            break
        page += 1
        time.sleep(0.5)
    return users


def get_follower_count(uid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }
    resp = requests.get(
        "https://api.bilibili.com/x/relation/stat",
        params={"vmid": uid},
        headers=headers,
    ).json()
    if resp["code"] == 0:
        return resp["data"]["follower"]
    return 0


def enrich_followers(users):
    print("正在查询粉丝数...")
    for i, u in enumerate(users):
        u["follower"] = get_follower_count(u["uid"])
        if (i + 1) % 20 == 0:
            print(f"  已查询 {i + 1}/{len(users)}")
        time.sleep(0.3)
    return users


def main():
    config = load_config()
    print("正在获取黑名单...")
    users = get_blacklist(config["sessdata"], config["bili_jct"])
    result = {
        "version": 1,
        "updated": time.strftime("%Y-%m-%d"),
        "count": len(users),
        "users": users,
    }
    with open("blacklist.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"已导出 {len(users)} 个用户到 blacklist.json")


if __name__ == "__main__":
    main()
