# bilibili-die

B站黑名单共享工具。用户把自己的黑名单导出成 JSON，分享到 GitHub，别人一键拉黑。

## 项目结构

```
├── blacklist.json      # 黑名单数据（UID、用户名、简介、拉黑时间）
├── export.py           # 导出脚本：从当前账号导出已拉黑用户 → blacklist.json
├── block.py            # 拉黑脚本：读取 blacklist.json → 批量拉黑
├── config.example.json # Cookie 配置模板
├── config.json         # 实际配置（不提交，包含 SESSDATA 和 bili_jct）
├── review.md           # 拉黑前生成的确认文件（粉丝≥1万的用户列表）
├── requirements.txt    # Python 依赖：requests
└── LICENSE             # MIT
```

## B站 API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/x/relation/blacks` | GET | 获取自己的黑名单（需登录） |
| `/x/relation/modify` | POST | 拉黑（act=5）/ 取消拉黑（act=6） |
| `/x/relation/stat` | GET | 查粉丝数（无需登录） |

认证：Cookie 中的 `SESSDATA` + `bili_jct`，从浏览器 F12 → Application → Cookies 获取。

## 用法

### 拉黑（使用者）

```bash
pip install -r requirements.txt
cp config.example.json config.json
# 编辑 config.json 填入 Cookie
python block.py
```

流程：查粉丝数 → 粉丝≥1万的输出到 review.md → 用户确认 → 执行拉黑。

参数：
- `--dry-run` — 只预览不拉黑
- `--skip-review` — 跳过确认直接全拉
- `--delay 2` — 每次请求间隔秒数

### 导出（分享者）

```bash
python export.py
```

生成 `blacklist.json`，推到 GitHub 即可。

## Claude Code 操作流程

1. 读取用户浏览器 Cookie（Firefox: `%APPDATA%\Mozilla\Firefox\Profiles\*\cookies.sqlite`，查 `bilibili.com` 的 `SESSDATA` 和 `bili_jct`）
2. 写入 `config.json`
3. 运行 `python block.py`
4. 等待用户确认 `review.md` 后继续
