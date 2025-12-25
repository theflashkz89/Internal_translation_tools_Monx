import streamlit.web.cli as stcli
import os
import sys
import traceback


def resolve_path(path):
    if getattr(sys, "frozen", False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)


if __name__ == "__main__":
    try:
        # 设置环境变量
        os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"  # 不显示服务器启动信息

        # 获取 app.py 的绝对路径
        app_path = resolve_path("app.py")
        
        # 模拟命令行启动
        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--global.developmentMode=false",
        ]
        stcli.main()
    except Exception as e:
        # 打印详细错误堆栈
        traceback.print_exc()
    finally:
        # 无论正常结束还是报错结束，都暂停等待用户按键
        input("程序已结束或出错，按回车键退出...")

