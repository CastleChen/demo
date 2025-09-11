import cv2
import numpy as np
import pyautogui
import time
import ctypes

#基于模板匹配识别图标位置的方法：
def findTar(img, template):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    h, w = template.shape[:2]
    
    # 通常TM_CCOEFF_NORMED效果较好
    method = cv2.TM_CCOEFF_NORMED
    
    # 执行模板匹配
    result = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = (top_left[0] + w//2, top_left[1] + h//2)
        
    return center[0], center[1], max_val

def get_screen_scaling_factor():
    """获取系统显示缩放比例"""
    try:
        # Windows系统
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        hdc = ctypes.windll.user32.GetDC(0)
        scale = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88) / 96.0
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return scale
    except:
        # macOS/Linux系统或Windows获取失败
        return 1.0  # 默认无缩放

def move_mouse_to_target(target_position, duration = 0.01):
    """
    将鼠标移动至目标位置
    参数:
        target_position: 目标坐标(x, y)
        duration: 移动动画持续时间 (秒)
    """
    
    try:
        scaling_factor = get_screen_scaling_factor()
        print(f"检测到屏幕缩放比例: {scaling_factor}")
        
        # 应用缩放比例
        scaled_x = int(target_position[0] * scaling_factor)
        scaled_y = int(target_position[1] * scaling_factor)
        
        # 获取当前鼠标位置
        current_x, current_y = pyautogui.position()

        # 计算移动距离
        distance = ((scaled_x - current_x)**2 + (scaled_y - current_y)**2)**0.5

        # 如果距离太近则不移动
        if distance < 5 :
            print("目标位置与当前距离小于5像素, 不移动鼠标")
            return
        # 移动鼠标至目标位置
        pyautogui.moveTo(scaled_x, scaled_y, duration=duration)
        print("已将鼠标移动至目标位置:({scaled_x, scaled_y})")

        # 添加短暂延迟, 确保移动完成
        # time.sleep(1)
    except Exception as e:
        print(f"移动鼠标出错: {str(e)}")
        
def capture_screen():
    """捕获整个屏幕并返回OpenCV图像"""
    # 使用pyautogui获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    
    # 截取屏幕
    screenshot = pyautogui.screenshot()
    
    # 转换为OpenCV格式
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    return img

def show_image_fullscreen(img):
    """以无边框全屏模式显示图像"""
    cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def perform_single_click():
    """执行双击操作"""
    try:
        # 第一次点击
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        print("已执行单击操作")
    except Exception as e:
        print(f"执行单击操作时出错: {str(e)}")

def perform_double_click(interval=0.1):
    """执行双击操作"""
    try:
        # 第一次点击
        perform_single_click()
        
        # 短暂延迟
        time.sleep(interval)
        
        # 第二次点击
        perform_single_click()
        
        print("已执行双击操作")
        
    except Exception as e:
        print(f"执行双击操作时出错: {str(e)}")


# 使用示例
if __name__ == "__main__":
    vx_img = cv2.imread('ZY-win\src\demo\WeChatClick\wechat_icon.png')
    enter_img = cv2.imread('ZY-win\src\demo\WeChatClick\enter_vx.png')

    # double click WeChat
    detect_img = capture_screen()

    find_vx = findTar(detect_img, vx_img)
    if find_vx[2] > 0.8:
         move_mouse_to_target([find_vx[0], find_vx[1]])
         perform_single_click()
    while True:
        # enter WeChat
        detect_img = capture_screen()
        time.sleep(0.5)
        find_enter = findTar(detect_img, enter_img)
        if find_enter[2] > 0.8:
            move_mouse_to_target([find_enter[0], find_enter[1]])
            perform_single_click()
            break
