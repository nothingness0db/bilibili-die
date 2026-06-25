# Agents

本项目提供两个 B站黑名单自动化脚本，可配合 AI Agent 使用。

## 工具

### export.py — 导出黑名单

从当前登录账号导出所有已拉黑用户，生成 `blacklist.json`。

```
python export.py
```

输入：`config.json`（B站 Cookie）
输出：`blacklist.json`

### block.py — 批量拉黑

读取黑名单文件，批量拉黑所有用户。

```
python block.py [--file <路径>] [--dry-run] [--delay <秒>]
```

参数：
- `--file` — 黑名单文件路径，默认 `blacklist.json`
- `--dry-run` — 只预览不执行
- `--delay` — 每次请求间隔，默认 1 秒

## API 参考

| 接口 | 方法 | 说明 |
|------|------|------|
| `/x/relation/blacks` | GET | 获取黑名单列表（分页） |
| `/x/relation/modify` | POST | 拉黑（act=5）/ 取消拉黑（act=6） |

认证：Cookie 中的 `SESSDATA` + `bili_jct`

## Agent 调用示例

Agent 可以直接调用这些脚本完成任务：

```
# 导出我的黑名单
python export.py

# 预览将要拉黑的用户
python block.py --dry-run

# 执行批量拉黑
python block.py

# 拉黑指定文件中的用户
python block.py --file other_blacklist.json
```
