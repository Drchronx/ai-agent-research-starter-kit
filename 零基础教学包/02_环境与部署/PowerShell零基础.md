# PowerShell 零基础

## 1. PowerShell 是什么

PowerShell 是 Windows 自带的命令行工具。你可以把它理解为“用文字控制电脑”。

你需要掌握的命令不多：

| 命令 | 作用 |
|---|---|
| `cd 路径` | 进入文件夹 |
| `dir` | 查看当前文件夹内容 |
| `python --version` | 检查 Python 是否安装 |
| `powershell -File 脚本.ps1` | 运行脚本 |

## 2. 如何打开 PowerShell

方法一：

1. 按 Windows 键。
2. 输入 `PowerShell`。
3. 点击打开。

方法二：

1. 打开一个文件夹。
2. 在地址栏输入 `powershell`。
3. 按回车。

## 3. 进入本教学包

复制下面命令到 PowerShell：

```powershell
cd "<本项目路径>\零基础教学包"
```

如果成功，说明你已经进入教学包目录。

## 4. 查看当前目录

```powershell
dir
```

你应该能看到：

```text
00_先读我
01_认识AI_Agent
02_环境与部署
...
```

## 5. 运行环境检查

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_environment.ps1
```

如果看到 Python、Codex skills 目录等信息，说明检查正常。

## 6. 常见错误

### 错误 1：路径找不到

原因：路径打错，或者少了引号。

正确写法：

```powershell
cd "<本项目路径>\零基础教学包"
```

### 错误 2：禁止运行脚本

用这个写法：

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_environment.ps1
```

### 错误 3：python 不是内部或外部命令

说明 Python 没装好，或者没有加入 PATH。

先试：

```powershell
py --version
```

如果 `py` 能用，也可以用 `py -m pip install ...`。

