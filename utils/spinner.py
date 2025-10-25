"""
命令行加载动画工具
提供旋转和跳动的加载提示，防止用户以为程序卡死
"""

import sys
import time
import threading


class Spinner:
    """命令行加载动画"""
    
    # 旋转符号动画
    SPINNER_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    # 跳动点动画
    DOTS_FRAMES = ['.  ', '.. ', '...', '.. ', '.  ', '   ']
    
    # 进度条动画
    BAR_FRAMES = ['[=    ]', '[==   ]', '[===  ]', '[ === ]', '[  ===]', '[   ==]', '[    =]', '[   ==]', '[  ===]', '[ === ]']
    
    def __init__(self, message: str = "处理中", style: str = "spinner"):
        """
        初始化加载动画
        
        Args:
            message: 显示的提示信息
            style: 动画风格 (spinner/dots/bar)
        """
        self.message = message
        self.style = style
        self.running = False
        self.thread = None
        
        # 根据风格选择帧
        if style == "spinner":
            self.frames = self.SPINNER_FRAMES
        elif style == "dots":
            self.frames = self.DOTS_FRAMES
        elif style == "bar":
            self.frames = self.BAR_FRAMES
        else:
            self.frames = self.SPINNER_FRAMES
    
    def _animate(self):
        """动画循环"""
        i = 0
        while self.running:
            frame = self.frames[i % len(self.frames)]
            # 使用 \r 回到行首，覆盖之前的内容
            sys.stdout.write(f'\r{frame} {self.message}')
            sys.stdout.flush()
            time.sleep(0.1)  # 100ms 刷新一次
            i += 1
        
        # 清空动画行
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def start(self):
        """启动动画"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate, daemon=True)
            self.thread.start()
    
    def stop(self):
        """停止动画"""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=0.5)
    
    def __enter__(self):
        """支持 with 语句"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持 with 语句"""
        self.stop()


def spinner(message: str = "处理中", style: str = "spinner"):
    """
    创建一个加载动画上下文管理器
    
    使用示例:
        with spinner("正在生成内容", style="spinner"):
            # 执行耗时操作
            time.sleep(5)
    
    Args:
        message: 显示的提示信息
        style: 动画风格 (spinner/dots/bar)
    
    Returns:
        Spinner对象
    """
    return Spinner(message, style)


# 便捷函数
def show_thinking(message: str = "AI思考中"):
    """显示AI思考提示"""
    return Spinner(message, style="spinner")


def show_generating(message: str = "内容生成中"):
    """显示内容生成提示"""
    return Spinner(message, style="dots")


def show_processing(message: str = "处理中"):
    """显示处理提示"""
    return Spinner(message, style="bar")


if __name__ == "__main__":
    # 测试代码
    print("测试旋转符号动画:")
    with spinner("AI思考中", style="spinner"):
        time.sleep(3)
    print("✅ 完成\n")
    
    print("测试跳动点动画:")
    with spinner("内容生成中", style="dots"):
        time.sleep(3)
    print("✅ 完成\n")
    
    print("测试进度条动画:")
    with spinner("处理中", style="bar"):
        time.sleep(3)
    print("✅ 完成")
