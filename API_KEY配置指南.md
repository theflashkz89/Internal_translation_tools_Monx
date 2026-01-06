# DeepSeek API Key 配置指南

## 📋 配置步骤

### 方法 1：使用 Streamlit Secrets（推荐）

1. 打开项目根目录下的 `.streamlit/secrets.toml` 文件
2. 将 `your-api-key-here` 替换为你的实际 DeepSeek API Key
3. 保存文件

示例：
```toml
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 方法 2：使用环境变量

#### Windows PowerShell:
```powershell
$env:DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

#### Windows CMD:
```cmd
set DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 永久设置（Windows）:
1. 右键"此电脑" -> 属性
2. 高级系统设置 -> 环境变量
3. 在"用户变量"中添加新变量：
   - 变量名：`DEEPSEEK_API_KEY`
   - 变量值：你的 API Key

## ✅ 测试配置

运行测试脚本验证配置：

```bash
python test_api.py
```

如果配置正确，你会看到：
- ✓ 找到 API Key
- ✓ API 调用成功
- ✅ 所有测试通过！

## 🔑 获取 DeepSeek API Key

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册/登录账号
3. 进入 API 管理页面
4. 创建新的 API Key
5. 复制 API Key 并按照上述方法配置

## ⚠️ 注意事项

- **不要**将包含真实 API Key 的 `secrets.toml` 文件提交到 Git
- `.gitignore` 已配置，会自动忽略 `secrets.toml` 文件
- API Key 泄露可能导致费用损失，请妥善保管






