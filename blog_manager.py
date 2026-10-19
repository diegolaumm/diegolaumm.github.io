import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime

# ==========================================
# 1. 基本設定區
# ==========================================
POSTS_DIR = 'posts'
TEMPLATE_FILE = 'template.html'
OUTPUT_FILE = 'index.html'

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

# ==========================================
# 2. 網頁生成邏輯 (Build Blog)
# ==========================================
def build_blog():
    post_it_html = ""
    # 取得所有 .txt 文章，按檔名排序（新到舊）
    if not os.path.exists(POSTS_DIR):
        return False
        
    files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.txt')], reverse=True)
    
    for filename in files:
        try:
            with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines()]
                if len(lines) < 6: continue
                
                # 從檔案標頭讀取設定
                font_class = lines[0].replace("Font: ", "") if lines[0].startswith("Font:") else "font-serif"
                color_class = lines[1].replace("Color: ", "") if lines[1].startswith("Color:") else "yellow"
                size_class = lines[2].replace("Size: ", "") if lines[2].startswith("Size:") else "normal"
                width_val = lines[3].replace("Width: ", "") if lines[3].startswith("Width:") else "240px"
                
                date = lines[4]
                title = lines[5]
                content = "\n".join(lines[6:])
                
                # 設定寬度樣式
                width_style = f' style="width: {width_val};"' if width_val else ""

                # 組裝 HTML
                post_it_html += f"""
        <div class="post-it {color_class} {font_class} {size_class}"{width_style}>
            <span class="date">{date}</span>
            <h2>{title}</h2>
            <p>{content.replace('\n', '<br>')}</p>
        </div>
    """
        except:
            continue

    # 讀取模板並替換
    if not os.path.exists(TEMPLATE_FILE):
        messagebox.showerror("錯誤", f"找不到模板檔案 {TEMPLATE_FILE}")
        return False

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    final_html = template.replace("[INSERT_POSTS_HERE]", post_it_html)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
    return True

# ==========================================
# 3. GUI 儲存與發佈邏輯
# ==========================================
def save_and_publish():
    title = entry_title.get().strip()
    date = entry_date.get().strip()
    content = text_content.get("1.0", "end-1c").strip()
    
    font_map = {
        "經典宋體 (預設)": "font-serif", 
        "現代黑體": "font-sans", 
        "草書": "font-poem", 
        "毛筆字": "font-brush",
        "芫荽 (手寫)": "font-iansui"
    }
    color_map = {"黃色": "yellow", "藍色": "blue", "粉色": "pink", "綠色": "green", "紫色": "purple"}
    
    font_style = font_map.get(combo_font.get(), "font-serif")
    color_style = color_map.get(combo_color.get(), "yellow")
    size_style = "normal" 

    sel_width = combo_width.get()
    if sel_width == "標準(240px)":
        final_width = "240px"
    elif sel_width == "七言(260px)":
        final_width = "260px"
    else:
        custom_val = entry_custom_width.get().strip()
        final_width = f"{custom_val}px" if custom_val else "240px"
        
    if not title or not content:
        messagebox.showwarning("警告", "標題和內容不能空白喔！")
        return

    safe_title = "".join(c for c in title if c.isalnum() or c in " 中文_-").strip()
    filename = os.path.join(POSTS_DIR, f"{date}_{safe_title}.txt")
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Font: {font_style}\n")
            f.write(f"Color: {color_style}\n")
            f.write(f"Size: {size_style}\n")
            f.write(f"Width: {final_width}\n")
            f.write(f"{date}\n")
            f.write(f"{title}\n")
            f.write(content)
        
        if build_blog():
            messagebox.showinfo("成功", f"文章【{title}】已發佈！")
            entry_title.delete(0, tk.END)
            text_content.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("錯誤", f"儲存失敗: {str(e)}")

# ==========================================
# 4. GUI 介面設計
# ==========================================
root = tk.Tk()
root.title("我的詩集後台管理")
root.geometry("600x700")

# 標題與日期
frame_top = tk.Frame(root)
# 修正處：px 改為 padx
frame_top.pack(pady=10, fill="x", padx=20)

tk.Label(frame_top, text="文章標題:").pack(side="left")
entry_title = tk.Entry(frame_top, width=30)
entry_title.pack(side="left", padx=5)

tk.Label(frame_top, text="日期:").pack(side="left", padx=(10, 0))
entry_date = tk.Entry(frame_top, width=12)
entry_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
entry_date.pack(side="left", padx=5)

# 樣式設定
frame_style = tk.LabelFrame(root, text="樣式設定", padx=10, pady=10)
frame_style.pack(pady=10, fill="x", padx=20)

tk.Label(frame_style, text="顏色:").pack(side="left")
combo_color = ttk.Combobox(frame_style, values=["黃色", "藍色", "粉色", "綠色", "紫色"], state="readonly", width=8)
combo_color.current(0)
combo_color.pack(side="left", padx=5)

tk.Label(frame_style, text="字體:").pack(side="left", padx=(10,0))
combo_font = ttk.Combobox(frame_style, values=["經典宋體 (預設)", "現代黑體", "草書", "毛筆字", "芫荽 (手寫)"], state="readonly", width=12)
combo_font.current(0)
combo_font.pack(side="left", padx=5)

tk.Label(frame_style, text="寬度:").pack(side="left", padx=(10, 0))
def on_width_select(event):
    if combo_width.get() == "其他(自訂)":
        frame_custom_width.pack(side="left", padx=5)
    else:
        frame_custom_width.pack_forget()

combo_width = ttk.Combobox(frame_style, values=["標準(240px)", "七言(260px)", "其他(自訂)"], state="readonly", width=12)
combo_width.current(0)
combo_width.pack(side="left", padx=5)
combo_width.bind("<<ComboboxSelected>>", on_width_select)

frame_custom_width = tk.Frame(frame_style)
entry_custom_width = tk.Entry(frame_custom_width, width=5)
entry_custom_width.pack(side="left")
tk.Label(frame_custom_width, text="px").pack(side="left")

# 內容
tk.Label(root, text="文章內容:").pack(anchor="w", padx=20)
text_content = tk.Text(root, height=20)
text_content.pack(pady=5, padx=20, fill="both", expand=True)

# 按鈕
btn_save = tk.Button(root, text="儲存並發佈到網頁", command=save_and_publish, bg="#4CAF50", fg="white", height=2, font=("Helvetica", 12, "bold"))
btn_save.pack(pady=20, fill="x", padx=20)

root.mainloop()
