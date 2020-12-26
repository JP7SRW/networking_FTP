# -*- coding: utf-8 -*-
import tkinter
from tkinter import ttk
import tkinter.font as tkfont

def main(ip, port, user, password):
    # メインウィンドウ
    main_win = tkinter.Tk()
    main_win.title("FTPサーバの接続情報")
    main_win.geometry("500x200")

    # メインフレーム
    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

    # フォントスタイル定義
    fontstyle = tkfont.Font(family="Meiryo", size=60)

    # ウィジェット作成
    ip_label = ttk.Label(main_frm, text="IPアドレス", font=fontstyle)
    ip_info = ttk.Label(main_frm, text=ip, font=fontstyle)

    port_label = ttk.Label(main_frm, text="ポート:", font=fontstyle)
    port_info = ttk.Label(main_frm, text=port, font=fontstyle)

    user_label = ttk.Label(main_frm, text="ユーザ名:", font=fontstyle)
    user_info = ttk.Label(main_frm, text=user, font=fontstyle)

    password_label = ttk.Label(main_frm, text="パスワード:", font=fontstyle)
    password_info = ttk.Label(main_frm, text=password, font=fontstyle)

    # ウィジェットの配置
    ip_label.grid(column=0, row=0, pady=10)
    ip_info.grid(column=1, row=0, pady=10)

    port_label.grid(column=0, row=1, pady=10)
    port_info.grid(column=1, row=1, pady=10)

    user_label.grid(column=0, row=2, pady=10)
    user_info.grid(column=1, row=2, pady=10)

    password_label.grid(column=0, row=3, pady=10)
    password_info.grid(column=1, row=3, pady=10)

    # 配置設定
    main_win.columnconfigure(0, weight=1)
    main_win.rowconfigure(0, weight=1)
    main_frm.columnconfigure(1, weight=1)

    main_win.mainloop()
if __name__ == '__main__':
    main()