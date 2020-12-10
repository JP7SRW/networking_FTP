import tkinter
from tkinter import ttk

# メインウィンドウ
main_win = tkinter.Tk()
main_win.title("FTPサーバを立ち上げる")
main_win.geometry("500x120")

# メインフレーム
main_frm = ttk.Frame(main_win)
main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

# ウィジェット作成（フォルダパス）
folder_label = ttk.Label(main_frm, text="フォルダ指定")
folder_box = ttk.Entry(main_frm)
folder_btn = ttk.Button(main_frm, text="参照")

# ウィジェット作成（並び順）
order_label = ttk.Label(main_frm, text="並び順")
order_comb = ttk.Combobox(main_frm, values=["昇順", "降順"], width=10)
order_comb.current(0)

# ウィジェット作成（実行ボタン）
app_btn = ttk.Button(main_frm, text="実行")

# ウィジェットの配置
folder_label.grid(column=0, row=0, pady=10)
folder_box.grid(column=1, row=0, sticky=tkinter.EW, padx=5)
folder_btn.grid(column=2, row=0)
order_label.grid(column=0, row=1)
order_comb.grid(column=1, row=1, sticky=tkinter.W, padx=5)
app_btn.grid(column=1, row=2)

# 配置設定
main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
main_frm.columnconfigure(1, weight=1)

main_win.mainloop()
