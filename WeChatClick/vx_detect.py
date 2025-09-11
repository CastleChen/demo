import cv2
import numpy as np
import pyautogui

def locate_and_draw_wechat_icon(template_path, threshold=0.5):
    """
    在桌面屏幕上查找微信图标的位置，并在屏幕上绘制矩形框
    
    参数:
    template_path (str): 微信图标模板图像的路径
    threshold (float): 匹配相似度阈值，默认0.8
    
    返回:
    image_with_box: 绘制了矩形框的图像（numpy数组格式）
    icon_center: 图标中心坐标 (x, y)，如未找到返回 None
    """
    # 1. 读取模板图像并转换为灰度图[2,4](@ref)
    template = cv2.imread(template_path, 0)  # 以灰度模式读取
    if template is None:
        print("错误：无法加载模板图像，请检查路径")
        return None, None
    w, h = template.shape[::-1]  # 获取模板宽度和高度[1](@ref)

    # 2. 截取屏幕并转换为灰度图
    screenshot = pyautogui.screenshot()  # 获取屏幕截图
    screenshot = np.array(screenshot)  # 转换为 numpy 数组
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # 转换为灰度图[4](@ref)

    # 3. 执行模板匹配[1,2](@ref)
    # 使用归一化相关系数匹配方法（TM_CCOEFF_NORMED）[2](@ref)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    
    # 4. 定位匹配区域[1](@ref)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)  # 获取最佳匹配值和位置
    if max_val >= threshold:
        top_left = max_loc  # 最佳匹配区域的左上角坐标
        bottom_right = (top_left[0] + w, top_left[1] + h)  # 计算右下角坐标[1](@ref)

        # 5. 在屏幕截图上绘制矩形框[6,7](@ref)
        # 为了绘制矩形框，我们需要将灰度截图转换回BGR格式（因为矩形框需要颜色）
        screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        cv2.rectangle(screenshot_bgr, top_left, bottom_right, (0, 255, 0), 2)  # 绿色矩形框，线宽2像素[6](@ref)

        # 计算图标中心坐标（可选）
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        print(f"找到微信图标，相似度: {max_val:.2f}, 中心位置: ({center_x}, {center_y})")
        
        return screenshot_bgr, (center_x, center_y)
    else:
        print(f"未找到微信图标，最高相似度仅 {max_val:.2f}，低于阈值 {threshold}")
        return None, None

# 使用示例
if __name__ == "__main__":
    template_path = "ZY-win\src\demo\WeChatClick\wechat_icon.png"  # 替换为你的微信图标模板图像路径
    result_image, icon_center = locate_and_draw_wechat_icon(template_path)
    
    if result_image is not None:
        # 显示带有矩形框的结果图像[1](@ref)
        cv2.imshow('WeChat Icon Located', result_image)
        cv2.waitKey(0)  # 等待按键关闭窗口
        cv2.destroyAllWindows()
        print(f"图标已框选，中心坐标: {icon_center}")
    else:
        print("未能识别微信图标")