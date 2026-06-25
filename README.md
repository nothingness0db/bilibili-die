# BiliBlock

我真的很讨厌一些傻逼视频博主。刷到就恶心，拉黑了一个又来一个，B站推荐跟喂屎一样。我觉得不止有我一个人吃屎。

这个东西就是用来干这个的：我把我的黑名单导出来，一键拉黑，后面还会加人，黑名单会一直更新。你们也可以开你们的黑名单，毕竟我的黑名单非常的主观。

## 你要怎么用

```bash
git clone https://github.com/<用户名>/bilblock.git
cd bilblock
pip install -r requirements.txt
```

然后去B站拿你的 Cookie：

1. 浏览器登录 bilibili.com
2. F12 → Application → Cookies → `https://www.bilibili.com`
3. 复制 `SESSDATA` 和 `bili_jct` 的值

```bash
cp config.example.json config.json
```

编辑 `config.json`，把那两个值粘进去。

然后：

```bash
python block.py
```

它会先查一遍所有人的粉丝数，超过1万的列到 `review.md` 给你看一眼，确认了再拉黑。

## 我也想分享我的黑名单

```bash
python export.py
```

跑一次，你的黑名单就导出成 `blacklist.json` 了，推到 GitHub 就行。

## 其他

```bash
python block.py --dry-run        # 只看不拉
python block.py --skip-review    # 跳过确认直接全拉
python block.py --delay 2        # 每次间隔2秒，防限流
```
