"""
测试 DeepSeek 和 DeepL API 配置和连接
运行此脚本以验证 API Key 是否正确配置
"""
import os
import sys

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def test_api_key_config(api_name="DEEPSEEK"):
    """测试 API Key 配置"""
    print("=" * 50)
    print(f"{api_name} API 配置测试")
    print("=" * 50)
    
    env_var_name = f"{api_name}_API_KEY"
    
    # 检查环境变量
    env_key = os.getenv(env_var_name)
    if env_key:
        print(f"✓ 从环境变量找到 {api_name} API Key")
        print(f"  Key 前缀: {env_key[:10]}...")
        return env_key
    else:
        print(f"✗ 未在环境变量中找到 {env_var_name}")
    
    # 检查 Streamlit secrets
    try:
        from pathlib import Path
        import re
        
        secrets_path = Path(".streamlit/secrets.toml")
        if secrets_path.exists():
            print("✓ 找到 .streamlit/secrets.toml 文件")
            # 简单读取 TOML 文件（不使用外部库）
            with open(secrets_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 使用正则表达式提取 API Key
                match = re.search(rf'{env_var_name}\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    secrets_key = match.group(1)
                    if secrets_key and secrets_key not in ["your-api-key-here", "your-deepl-api-key-here"]:
                        print(f"✓ 从 secrets.toml 找到 {api_name} API Key")
                        print(f"  Key 前缀: {secrets_key[:10]}...")
                        return secrets_key
                    else:
                        print(f"✗ secrets.toml 中的 {api_name} API Key 未配置或仍为默认值")
                else:
                    print(f"✗ 无法从 secrets.toml 中解析 {env_var_name}")
        else:
            print("✗ 未找到 .streamlit/secrets.toml 文件")
    except Exception as e:
        print(f"⚠ 检查 secrets 时出错: {e}")
    
    return None


def test_api_call(api_key):
    """测试 API 调用"""
    print("\n" + "=" * 50)
    print("测试 API 调用")
    print("=" * 50)
    
    try:
        from utils import call_deepseek_api
        
        # 如果从环境变量获取的 key，需要设置环境变量
        if api_key and not os.getenv("DEEPSEEK_API_KEY"):
            os.environ["DEEPSEEK_API_KEY"] = api_key
        
        print("正在调用 DeepSeek API...")
        print("测试文本: '你好'")
        print("测试 Prompt: '你是一个友好的助手，请用中文回复。'")
        print("-" * 50)
        
        result = call_deepseek_api(
            text="你好",
            prompt="你是一个友好的助手，请用中文回复。"
        )
        
        print("✓ API 调用成功！")
        print(f"\nAI 回复:\n{result}\n")
        return True
        
    except ValueError as e:
        print(f"✗ 配置错误: {e}")
        print("\n请检查:")
        print("1. 是否在 .streamlit/secrets.toml 中配置了 DEEPSEEK_API_KEY")
        print("2. 或是否设置了环境变量 DEEPSEEK_API_KEY")
        return False
    except Exception as e:
        print(f"✗ API 调用失败: {e}")
        print("\n可能的原因:")
        print("1. API Key 无效或已过期")
        print("2. 网络连接问题")
        print("3. DeepSeek API 服务暂时不可用")
        return False


def test_deepl_api_call(api_key):
    """测试 DeepL API 调用"""
    print("\n" + "=" * 50)
    print("测试 DeepL API 调用")
    print("=" * 50)
    
    try:
        from utils import call_deepl_api
        
        # 如果从环境变量获取的 key，需要设置环境变量
        if api_key and not os.getenv("DEEPL_API_KEY"):
            os.environ["DEEPL_API_KEY"] = api_key
        
        print("正在调用 DeepL API...")
        print("测试文本: '你好，世界'")
        print("目标语言: 英语 (EN-US)")
        print("-" * 50)
        
        result = call_deepl_api(
            text="你好，世界",
            target_lang="EN-US"
        )
        
        print("✓ API 调用成功！")
        print(f"\n翻译结果: {result}\n")
        return True
        
    except ValueError as e:
        print(f"✗ 配置错误: {e}")
        print("\n请检查:")
        print("1. 是否在 .streamlit/secrets.toml 中配置了 DEEPL_API_KEY")
        print("2. 或是否设置了环境变量 DEEPL_API_KEY")
        return False
    except Exception as e:
        print(f"✗ API 调用失败: {e}")
        print("\n可能的原因:")
        print("1. API Key 无效或已过期")
        print("2. 网络连接问题")
        print("3. DeepL API 服务暂时不可用")
        print("4. API 额度已用完")
        return False


def test_deepl_api_batch():
    """测试 DeepL 批量翻译 API"""
    print("\n" + "=" * 50)
    print("测试 DeepL 批量翻译 API")
    print("=" * 50)
    
    try:
        from utils import call_deepl_api_batch
        
        test_texts = [
            "你好",
            "世界",
            "测试批量翻译"
        ]
        
        print("正在调用 DeepL 批量翻译 API...")
        print(f"测试文本列表: {test_texts}")
        print("目标语言: 英语 (EN-US)")
        print("-" * 50)
        
        results = call_deepl_api_batch(
            texts=test_texts,
            target_lang="EN-US"
        )
        
        print("✓ 批量翻译成功！")
        print("\n翻译结果:")
        for i, (original, translated) in enumerate(zip(test_texts, results), 1):
            print(f"  {i}. '{original}' -> '{translated}'")
        print()
        return True
        
    except Exception as e:
        print(f"✗ 批量翻译失败: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        # 让用户选择测试哪个 API
        print("=" * 50)
        print("API 测试工具")
        print("=" * 50)
        print("\n请选择要测试的 API:")
        print("1. DeepSeek API")
        print("2. DeepL API")
        print("3. 测试所有 API")
        print()
        
        try:
            choice = input("请输入选项 (1/2/3，默认为 2): ").strip() or "2"
        except EOFError:
            # 非交互式环境，默认测试 DeepL
            choice = "2"
            print("非交互式环境，默认测试 DeepL API")
    
    all_success = True
    
    # 测试 DeepSeek API
    if choice in ["1", "3"]:
        api_key = test_api_key_config("DEEPSEEK")
        
        if not api_key:
            print("\n" + "=" * 50)
            print("❌ 未找到有效的 DeepSeek API Key")
            print("=" * 50)
            print("\n配置方法:")
            print("方法 1: 设置环境变量")
            print("  PowerShell: $env:DEEPSEEK_API_KEY='your-api-key'")
            print("  CMD: set DEEPSEEK_API_KEY=your-api-key")
            print("\n方法 2: 编辑 .streamlit/secrets.toml")
            print("  将 DEEPSEEK_API_KEY 的值改为你的实际 API Key")
            if choice == "1":
                sys.exit(1)
            all_success = False
        else:
            success = test_api_call(api_key)
            if not success:
                all_success = False
    
    # 测试 DeepL API
    if choice in ["2", "3"]:
        deepl_key = test_api_key_config("DEEPL")
        
        if not deepl_key:
            print("\n" + "=" * 50)
            print("❌ 未找到有效的 DeepL API Key")
            print("=" * 50)
            print("\n配置方法:")
            print("方法 1: 设置环境变量")
            print("  PowerShell: $env:DEEPL_API_KEY='your-api-key'")
            print("  CMD: set DEEPL_API_KEY=your-api-key")
            print("\n方法 2: 编辑 .streamlit/secrets.toml")
            print("  将 DEEPL_API_KEY 的值改为你的实际 API Key")
            print("  注意: 免费版 API Key 通常以 :fx 结尾")
            if choice == "2":
                sys.exit(1)
            all_success = False
        else:
            # 测试单条翻译
            success = test_deepl_api_call(deepl_key)
            if not success:
                all_success = False
            
            # 测试批量翻译
            if success:
                batch_success = test_deepl_api_batch()
                if not batch_success:
                    all_success = False
    
    # 总结
    print("\n" + "=" * 50)
    if all_success:
        print("✅ 所有测试通过！API 配置正常。")
    else:
        print("❌ 部分测试失败，请检查配置。")
    print("=" * 50)
    
    if not all_success:
        sys.exit(1)

