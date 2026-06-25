# 用法

## 快速开始

```
git clone https://github.com/nothingness0db/bilibili-die.git
cd bilibili-die
pip install -r requirements.txt
```

然后去B站拿你的 Cookie：

1. 浏览器登录 bilibili.com
2. F12 → Application → Cookies → `https://www.bilibili.com`
3. 复制 `SESSDATA` 和 `bili_jct` 的值

```
cp config.example.json config.json
```

编辑 `config.json`，把那两个值粘进去。

然后：

```
python block.py
```

它会先查一遍所有人的粉丝数，超过1万的列到 `review.md` 给你看一眼，确认了再拉黑。

## 导出你自己的黑名单

```
python export.py
```

跑一次，你的黑名单就导出成 `blacklist.json` 了，推到 GitHub 就行。

## 其他参数

```
python block.py --dry-run        # 只看不拉
python block.py --skip-review    # 跳过确认直接全拉
python block.py --delay 2        # 每次间隔2秒，防限流
```

## Claude Code 用法

克隆仓库后直接开 Claude Code，它会自动读 AGENTS.md，告诉它"拉黑"就行。
