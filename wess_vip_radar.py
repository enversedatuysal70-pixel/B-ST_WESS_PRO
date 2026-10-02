import threading
import webbrowser


import pandas as pd
import numpy as np

try:
    from tradingview_screener import Query
except ImportError:
  pass
# ---------------------------------------------------------
# HOVER (TOOLTIP) AÇIKLAMA BALONCUĞU SINIFI
# ---------------------------------------------------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert") if self.widget.bbox("insert") else (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        
        label = tk.Label(
            tw, text=self.text, justify="left",
            bg="#2b2b2b", fg="#00ffcc", relief="solid", bd=1,
            font=("Helvetica", 9, "normal"), padx=8, pady=6
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


#class LoginDialog(tk.Toplevel):
   # def __init__(self, parent):
        super().__init__(parent)
        self.title("🔐 WESS VIP SYSTEM - GİRİŞ")
        self.geometry("380x260")
        self.configure(bg="#121212")
        self.resizable(False, False)
        self.is_authenticated = False

        self.transient(parent)
        self.grab_set()

        lbl_title = tk.Label(
            self, 
            text="WESS VIP RADAR PRO", 
            font=("Helvetica", 16, "bold"), 
            fg="#00ffcc", 
            bg="#121212"
        )
        lbl_title.pack(pady=15)

        tk.Label(self, text="Kullanıcı Adı:", font=("Helvetica", 10), fg="white", bg="#121212").pack()
        self.ent_user = tk.Entry(self, font=("Helvetica", 11), bg="#1e1e1e", fg="white", insertbackground="white")
        self.ent_user.pack(pady=3)
        self.ent_user.insert(0, "wess")

        tk.Label(self, text="Şifre:", font=("Helvetica", 10), fg="white", bg="#121212").pack()
        self.ent_pass = tk.Entry(self, show="*", font=("Helvetica", 11), bg="#1e1e1e", fg="white", insertbackground="white")
        self.ent_pass.pack(pady=3)
        self.ent_pass.focus()

        btn_login = tk.Button(
            self, 
            text="SİSTEME GİRİŞ YAP", 
            font=("Helvetica", 10, "bold"), 
            bg="#007acc", 
            fg="white", 
            padx=10, pady=4, 
            command=self.check_login
        )
        btn_login.pack(pady=15)

        self.bind('<Return>', lambda event: self.check_login())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def check_login(self):
        user = self.ent_user.get().strip()
        pas = self.ent_pass.get().strip()

        if user == "wess" and pas == "1234":
            self.is_authenticated = True
            self.destroy()
        else:
            messagebox.showerror("Hata", "Hatalı Kullanıcı Adı veya Şifre!", parent=self)

    def on_close(self):
        self.is_authenticated = False
        self.destroy()
#
# ---------------------------------------------------------
# 2. ANA RADAR UYGULAMASI
# ---------------------------------------------------------

            fg="#00ffcc", 
            bg="#1e1e1e"
        )
        lbl_title.pack(side="left", padx=15)

        btn_help = tk.Button(
            title_frame, text="ℹ️ ŞEMATİK SİSTEM REHBERİ", font=("Helvetica", 9, "bold"),
            bg="#00b4d8", fg="white", padx=10, pady=2, command=self.rehber_penceresi_ac
        )
        btn_help.pack(side="right", padx=15)
        ToolTip(btn_help, "Adım adım yol gösteren, tüm doneleri açıklayan detaylı şematik rehberi açar.")

        # Kontrol Paneli
        control_frame = tk.Frame(self.root, bg="#121212", pady=6)
        control_frame.pack(fill="x", padx=15)

        tk.Label(control_frame, text="Periyot:", font=("Helvetica", 9, "bold"), fg="white", bg="#121212").pack(side="left", padx=(0, 3))

        self.timeframe_var = tk.StringVar(value="15 Dakika (15m)")
        self.combo_timeframe = ttk.Combobox(
            control_frame, 
            textvariable=self.timeframe_var, 
            state="readonly",
            width=15,
            font=("Helvetica", 9, "bold")
        )
        self.combo_timeframe['values'] = (
            "5 Dakika (5m)", "10 Dakika (10m)", "15 Dakika (15m)", "30 Dakika (30m)",
            "1 Saatlik (60m)", "2 Saatlik (120m)", "3 Saatlik (180m)", 
            "4 Saatlik (240m)", "Günlük (1D)", "Haftalık (1W)", "Aylık (1M)"
        )
        self.combo_timeframe.pack(side="left", padx=(0, 10))

        tk.Label(control_frame, text="Sektör:", font=("Helvetica", 9, "bold"), fg="#00ffcc", bg="#121212").pack(side="left", padx=(5, 3))
        
        self.index_filter_var = tk.StringVar(value="TÜM BIST")
        self.combo_index = ttk.Combobox(
            control_frame,
            textvariable=self.index_filter_var,
            state="readonly",
            width=18,
            font=("Helvetica", 9, "bold")
        )
        self.combo_index['values'] = (
            "TÜM BIST", "SANAYİ (XUSIN)", "BANKACILIK (XBANK)", "GYO (XGMYO)", 
            "HOLDİNG (XHOLD)", "BİLİŞİM (XBLSM)", "İLETİŞİM (XILTM)", "GIDA (XGIDA)", 
            "KİMYA (XKMYA)", "ULAŞTIRMA (XULAS)"
        )
        self.combo_index.pack(side="left", padx=(0, 10))
        self.combo_index.bind("<<ComboboxSelected>>", lambda e: self.filtrele_ve_guncelle())

        self.btn_tara = tk.Button(
            control_frame, 
            text="🚀 MANUEL TARA", 
            font=("Helvetica", 9, "bold"), 
            bg="#007acc", 
            fg="white", 
            padx=10, pady=2, 
            command=self.tarama_baslat_thread
        )
        self.btn_tara.pack(side="left", padx=(0, 10))

        self.auto_refresh_var = tk.BooleanVar(value=False)
        self.chk_auto = tk.Checkbutton(
            control_frame, 
            text="🔄 Oto Yenile", 
            variable=self.auto_refresh_var, 
            onvalue=True, 
            offvalue=False,
            font=("Helvetica", 9, "bold"), 
            fg="#00D2FF", 
            bg="#121212", 
            selectcolor="#1e1e1e",
            activebackground="#121212",
            activeforeground="#00D2FF",
            command=self.toggle_auto_refresh
        )
        self.chk_auto.pack(side="left", padx=(0, 3))

        self.interval_var = tk.StringVar(value="10 Saniye")
        self.combo_interval = ttk.Combobox(
            control_frame, 
            textvariable=self.interval_var, 
            state="readonly",
            width=9,
            font=("Helvetica", 9)
        )
        self.combo_interval['values'] = ("10 Saniye", "30 Saniye", "1 Dakika", "5 Dakika")
        self.combo_interval.pack(side="left", padx=(0, 10))

        self.lbl_search_mode = tk.Label(
            control_frame,
            text="⚙️ [ARAMA MODU: YÜKLENİYOR...]",
            font=("Helvetica", 9, "bold"),
            fg="#FFD700",
            bg="#121212"
        )
        self.lbl_search_mode.pack(side="left", padx=10)

        self.lbl_status = tk.Label(
            control_frame, 
            text="Sistem Hazır...", 
            font=("Helvetica", 8, "italic"), 
            fg="#aaaaaa", 
            bg="#121212"
        )
        self.lbl_status.pack(side="left", padx=2)

        # TABLO STİLİ
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e1e1e", foreground="#FFD700", fieldbackground="#1e1e1e", rowheight=23, font=("Helvetica", 9, "bold"))
        style.configure("Treeview.Heading", background="#2d2d2d", foreground="#00ffcc", font=("Helvetica", 9, "bold"))
        style.map("Treeview", background=[('selected', '#007acc')], foreground=[('selected', '#ffffff')])

        # Endeks Paneli
        index_container = tk.LabelFrame(
            self.root, 
            text="🏛️ BIST ANA VE ALT ENDEKS CANLI SİNYAL PANELI (ENDEKSE TIKLAYARAK HİSSELERİ VE SAYAÇLARI SÜZÜN)", 
            font=("Helvetica", 9, "bold"), 
            fg="#00E5FF", 
            bg="#101c28", 
            bd=2, 
            relief="groove", 
            padx=5, pady=5
        )
        index_container.pack(fill="x", padx=15, pady=(0, 5))

        idx_columns = ("Endeks Kodu", "Endeks Adı", "Son Puan", "Değişim (%)", "RSI (14)", "Sıkışma", "ENDEKS AKSİYON SİNYALİ")
        self.tree_index = ttk.Treeview(index_container, columns=idx_columns, show="headings", height=4)

        for col_name in idx_columns:
            self.tree_index.heading(col_name, text=col_name)
            width = 240 if col_name == "ENDEKS AKSİYON SİNYALİ" else 110
            self.tree_index.column(col_name, anchor="center", width=width)

        scroll_idx = ttk.Scrollbar(index_container, orient="vertical", command=self.tree_index.yview)
        self.tree_index.configure(yscroll=scroll_idx.set)
        
        self.tree_index.pack(side="left", fill="x", expand=True)
        scroll_idx.pack(side="right", fill="y")
        self.tree_index.bind("<ButtonRelease-1>", self.endeks_tiklandi)

        # Sayaç Kartları
        summary_frame = tk.Frame(self.root, bg="#121212", pady=4)
        summary_frame.pack(fill="x", padx=15)

        def create_card(parent, title, bg_color, tag_code, help_text, fg_color="#ffffff"):
            card = tk.Frame(parent, bg=bg_color, padx=5, pady=2, bd=1, relief="ridge", cursor="hand2")
            card.pack(side="left", expand=True, fill="x", padx=2)
            
            lbl_t = tk.Label(card, text=title, font=("Helvetica", 8, "bold"), fg=fg_color, bg=bg_color, cursor="hand2")
            lbl_t.pack()
            
            lbl_val = tk.Label(card, text="0", font=("Helvetica", 11, "bold"), fg=fg_color, bg=bg_color, cursor="hand2")
            lbl_val.pack()

            card.bind("<Button-1>", lambda e: self.karta_tiklandi(tag_code))
            lbl_t.bind("<Button-1>", lambda e: self.karta_tiklandi(tag_code))
            lbl_val.bind("<Button-1>", lambda e: self.karta_tiklandi(tag_code))

            ToolTip(card, help_text)
            ToolTip(lbl_t, help_text)
            ToolTip(lbl_val, help_text)

            return lbl_val

        self.cnt_kalkis = create_card(summary_frame, "🚀 ŞU AN GİR", "#FFD700", "KALKIS", "Hacim + Trend + Skor tavan yapmış hisseler.", fg_color="#000000")
        self.cnt_ezeller = create_card(summary_frame, "🔥 ENDEKSİ EZENLER", "#D35400", "EZENLER", "Endekse en az %2 fark atan lider hisseler.", fg_color="#ffffff")
        self.cnt_dip = create_card(summary_frame, "🔄 DİP DÖNÜŞÜ WESS", "#8A2BE2", "DIP_DONUS", "RSI dip bölgesinden yukarı dönmüş hisseler.", fg_color="#ffffff")
        self.cnt_spek = create_card(summary_frame, "🛡 SPEK-SAVAR", "#4B0082", "SPEK_SAVAR", "3.5 kat ve üzeri olağanüstü hacim patlaması.", fg_color="#ffffff")
        self.cnt_kilit = create_card(summary_frame, "🔒 KİLİTLİ AL", "#005f73", "KILITLI_AL", "Bant sıkışmasını hacimle yukarı kıran hisse.", fg_color="#ffffff")
        self.cnt_guc_al = create_card(summary_frame, "💎 GÜÇLÜ AL", "#008800", "GUC_AL", "Düzenli ve sağlıklı yükseliş trendindeki hisseler.", fg_color="#ffffff")
        self.cnt_sikisma = create_card(summary_frame, "🔥 SIKIŞIYOR", "#b8860B", "SIKISMA", "Fiyat dar bantta toplanıyor ama henüz patlamadı.", fg_color="#ffffff")
        self.cnt_izle = create_card(summary_frame, "👀 İZLEMEDE KAL", "#444444", "IZLE", "Nötr durumda olan hisseler.", fg_color="#ffffff")
        self.cnt_uzak_dur = create_card(summary_frame, "⚠️ UZAK DUR", "#8B0000", "UZAK_DUR", "Aşırı primlenmiş, düzeltme riski yüksek hisseler.", fg_color="#ffffff")

        # Tablo Sütunları
        columns = ("#", "Hisse", "Sektör Gücü", "Skor", "Son Fiyat (TL)", "Hacim (TL)", "Değişim (%)", "Endeks Üstü Güç", "AOF Farkı (%)", "NET AKSİYON SİNYALİ")

        kalkis_container = tk.LabelFrame(
            self.root, 
            text="🚀 ŞU AN GİR (ENDEKS VE HACİM DİNAMİKLİ KALKIŞ TAKİBİ - ÇİFT TIKLAYARAK ANALİZ & ATR HEDEF SAYFASINI AÇ)", 
            font=("Helvetica", 9, "bold"), 
            fg="#FFD700", 
            bg="#141a24", 
            bd=1, 
            relief="groove", 
            padx=5, pady=3
        )
        kalkis_container.pack(fill="x", padx=15, pady=(0, 4))

        self.tree_kalkis = ttk.Treeview(kalkis_container, columns=columns, show="headings", height=3)

        for col_name in columns:
            self.tree_kalkis.heading(col_name, text=col_name)
            width = 35 if col_name == "#" else (220 if col_name == "NET AKSİYON SİNYALİ" else (125 if col_name == "Endeks Üstü Güç" else 95))
            self.tree_kalkis.column(col_name, anchor="center", width=width)

        scroll_kalkis = ttk.Scrollbar(kalkis_container, orient="vertical", command=self.tree_kalkis.yview)
        self.tree_kalkis.configure(yscroll=scroll_kalkis.set)
        
        self.tree_kalkis.pack(side="left", fill="x", expand=True)
        scroll_kalkis.pack(side="right", fill="y")
        self.tree_kalkis.bind("<Double-1>", self.hisse_detay_ac)

        main_container = tk.LabelFrame(
            self.root, 
            text="📊 GENEL BİST AKÜMÜLASYON VE SİNYAL LİSTESİ (ÇİFT TIKLAYARAK ANALİZ & ATR HEDEF SAYFASINI AÇ)", 
            font=("Helvetica", 9, "bold"), 
            fg="#00ffcc", 
            bg="#121212", 
            bd=1, 
            relief="solid", 
            padx=5, pady=3
        )
        main_container.pack(fill="both", expand=True, padx=15, pady=(0, 8))

        search_frame = tk.Frame(main_container, bg="#121212", pady=2)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="🔍 Hisse Ara:", font=("Helvetica", 9, "bold"), fg="#00ffcc", bg="#121212").pack(side="left", padx=(5, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.filtrele_ve_guncelle())
        
        self.ent_search = tk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            font=("Helvetica", 9, "bold"), 
            bg="#1e1e1e", 
            fg="#00FF66", 
            insertbackground="white", 
            width=16
        )
        self.ent_search.pack(side="left", padx=5)

        self.btn_reset_filter = tk.Button(
            search_frame,
            text="❌ Filtre Sıfırla",
            font=("Helvetica", 8, "bold"),
            bg="#333333",
            fg="#ffcc00",
            padx=6,
            pady=1,
            command=self.filtreyi_sifirla
        )
        self.btn_reset_filter.pack(side="left", padx=10)

        self.lbl_active_filter = tk.Label(
            search_frame,
            text="[Tüm Listeleniyor]",
            font=("Helvetica", 9, "bold"),
            fg="#aaaaaa",
            bg="#121212"
        )
        self.lbl_active_filter.pack(side="left", padx=5)

        self.tree_main = ttk.Treeview(main_container, columns=columns, show="headings")

        self.tree_main.tag_configure("DIP_DONUS", foreground="#DDA0DD")
        self.tree_main.tag_configure("SPEK_SAVAR", foreground="#9d4edd")
        self.tree_main.tag_configure("KILITLI_AL", foreground="#00b4d8")
        self.tree_main.tag_configure("GUC_AL", foreground="#00FF66")
        self.tree_main.tag_configure("KALKIS", foreground="#FF9900")
        self.tree_main.tag_configure("SIKISMA", foreground="#E6C200")
        self.tree_main.tag_configure("IZLE", foreground="#FFD700")
        self.tree_main.tag_configure("UZAK_DUR", foreground="#FF3333")

        for col_name in columns:
            self.tree_main.heading(col_name, text=col_name)
            width = 35 if col_name == "#" else (220 if col_name == "NET AKSİYON SİNYALİ" else (125 if col_name == "Endeks Üstü Güç" else 95))
            self.tree_main.column(col_name, anchor="center", width=width)

        scroll_main = ttk.Scrollbar(main_container, orient="vertical", command=self.tree_main.yview)
        self.tree_main.configure(yscroll=scroll_main.set)
        
        self.tree_main.pack(side="left", fill="both", expand=True)
        scroll_main.pack(side="right", fill="y")
        self.tree_main.bind("<Double-1>", self.hisse_detay_ac)

    def endeks_tiklandi(self, event):
        selected = self.tree_index.selection()
        if not selected:
            return
        
        val = self.tree_index.item(selected[0], "values")
        code = val[0]
        
        map_code = {
            "XU100": "TÜM BIST",
            "XUSIN": "SANAYİ (XUSIN)",
            "XBANK": "BANKACILIK (XBANK)",
            "XGMYO": "GYO (XGMYO)",
            "XHOLD": "HOLDİNG (XHOLD)",
            "XBLSM": "BİLİŞİM (XBLSM)",
            "XULAS": "ULAŞTIRMA (XULAS)",
            "XKMYA": "KİMYA (XKMYA)",
            "XGIDA": "GIDA (XGIDA)"
        }
        
        target_sector = map_code.get(code, "TÜM BIST")
        self.index_filter_var.set(target_sector)
        self.filtrele_ve_guncelle()

    # ---------------------------------------------------------
    # 3. YENİ GELİŞTİRİLMİŞ ATR & REHBERLİ HİSSE ANALİZ EKRANI
    # ---------------------------------------------------------
    def hisse_detay_ac(self, event):
        tree = event.widget
        selected_item = tree.selection()
        if not selected_item:
            return

        values = tree.item(selected_item[0], "values")
        hisse_kodu = values[1]

        hisse_data = next((item for item in self.raw_results if item["Hisse"] == hisse_kodu), None)
        if not hisse_data:
            return

        detay_win = tk.Toplevel(self.root)
        detay_win.title(f"🔍 {hisse_kodu} - STRATEJİK REHBER, MALİYET, HACİM & ATR HEDEF DİNAMİKLERİ")
        detay_win.geometry("1240x880")
        detay_win.configure(bg="#121212")

        secili_tf_label = self.timeframe_var.get()

        header_frame = tk.Frame(detay_win, bg="#1e1e1e", pady=8)
        header_frame.pack(fill="x", padx=10, pady=6)

        tk.Label(header_frame, text=f"Hisse: {hisse_kodu}", font=("Helvetica", 14, "bold"), fg="#00ffcc", bg="#1e1e1e").pack(side="left", padx=10)
        tk.Label(header_frame, text=f"Sektör: {hisse_data['Sektör']}", font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#1e1e1e").pack(side="left", padx=10)
        
        btn_chart = tk.Button(
            header_frame,
            text="📈 CANLI TRADINGVIEW GRAFİĞİ",
            font=("Helvetica", 9, "bold"),
            bg="#00b4d8",
            fg="white",
            padx=10, pady=3,
            command=lambda: webbrowser.open(f"https://www.tradingview.com/chart/?symbol=BIST:{hisse_kodu}")
        )
        btn_chart.pack(side="right", padx=10)

        # ---------------------------------------------------------
        # STRATEJİK KULLANIM REHBERİ (YÖNLENDİRME PANELI)
        # ---------------------------------------------------------
        guide_box = tk.LabelFrame(detay_win, text="🧭 KULLANICI İÇİN ADIM ADIM STRATEJİK KONTROL & İŞLEM REHBERİ", font=("Helvetica", 9, "bold"), fg="#00FF66", bg="#18222d", padx=10, pady=4)
        guide_box.pack(fill="x", padx=15, pady=(0, 4))

        guide_text = (
            "1️⃣ NEREDEN BAŞLAMALI? -> Önce üst kısımdaki anlık fiyat ile VWAP (AOF) maliyet farkını inceleyin. Fiyat VWAP üstündeyse alıcılar kontrolü ele almıştır.\n"
            "2️⃣ HANGİ RAKAMLAR VE SİNYALLER? -> MTF tablo sekmesinden periyotlar arası hacim ivmesini ve endeks üstü gücü kontrol edin. Pozitif uyumsuzluk arayın.\n"
            "3️⃣ İŞLEM YOL HARİTASI -> Aşağıda otomatik hesaplanan ATR Hedefleri ve Stop-Loss seviyelerini baz alarak kademeli işlem planınızı uygulayın."
        )
        tk.Label(guide_box, text=guide_text, font=("Helvetica", 8, "bold"), fg="#e0e0e0", bg="#18222d", justify="left").pack(anchor="w")

        info_frame = tk.Frame(detay_win, bg="#121212", pady=2)
        info_frame.pack(fill="x", padx=15)

        lbl_top_info = tk.Label(
            info_frame, 
            text=f"Anlık Fiyat: {hisse_data['Son Fiyat (TL)']} TL  |  Seçili Periyot Hacmi ({secili_tf_label}): {hisse_data['Hacim (TL)']} TL  |  Sistem Skoru: {hisse_data['Skor']} Puan", 
            font=("Helvetica", 10, "bold"), 
            fg="#FFD700", 
            bg="#121212"
        )
        lbl_top_info.pack(anchor="w")
        
        self.lbl_buyer_seller = tk.Label(info_frame, text="⚖️ Alıcı / Satıcı Dengesi: Hesaplanıyor...", font=("Helvetica", 10, "bold"), fg="#00E5FF", bg="#121212")
        self.lbl_buyer_seller.pack(anchor="w", pady=2)

        # ---------------------------------------------------------
        # ATR HEDEF VE STOP-LOSS PANELI
        # ---------------------------------------------------------
        atr_box = tk.LabelFrame(detay_win, text="🎯 OTOMATİK ATR TABANLI DİNAMİK GİRİŞ, HEDEF VE RİSK YÖNETİMİ SEVİYELERİ", font=("Helvetica", 9, "bold"), fg="#FFD700", bg="#1d1b10", padx=10, pady=4)
        atr_box.pack(fill="x", padx=15, pady=4)

        self.lbl_atr_detay = tk.Label(atr_box, text="ATR Seviyeleri hesaplanıyor...", font=("Helvetica", 9, "bold"), fg="#00FF66", bg="#1d1b10", justify="left")
        self.lbl_atr_detay.pack(anchor="w")

        compare_frame = tk.Frame(detay_win, bg="#121212")
        compare_frame.pack(fill="x", padx=15, pady=4)

        # HACİM TABLOSU
        vol_box = tk.LabelFrame(compare_frame, text="📊 PERİYOTLAR ARASI HACİM & PARA AKIŞ KIYASLAMASI", font=("Helvetica", 9, "bold"), fg="#FFD700", bg="#18222d", padx=6, pady=4)
        vol_box.pack(side="left", fill="both", expand=True, padx=(0, 4))

        vol_cols = ("Periyot Kıyaslaması", "Hacim (TL)", "Hacim İvmesi")
        tree_vol = ttk.Treeview(vol_box, columns=vol_cols, show="headings", height=3)
        for c in vol_cols:
            tree_vol.heading(c, text=c)
            tree_vol.column(c, anchor="center", width=140)
        tree_vol.pack(fill="both", expand=True)

        # MALİYET TABLOSU
        cost_box = tk.LabelFrame(compare_frame, text="💰 GERÇEK DÖNEMSEL AOF & KURUMSAL MALİYET KIYASLAMASI", font=("Helvetica", 9, "bold"), fg="#00FF66", bg="#18222d", padx=6, pady=4)
        cost_box.pack(side="right", fill="both", expand=True, padx=(4, 0))

        cost_cols = ("Periyot Maliyeti", "AOF / Kurumsal Maliyet", "Fiyat / Maliyet Durumu")
        tree_cost = ttk.Treeview(cost_box, columns=cost_cols, show="headings", height=3)
        for c in cost_cols:
            tree_cost.heading(c, text=c)
            tree_cost.column(c, anchor="center", width=150)
        tree_cost.pack(fill="both", expand=True)

        mtf_container = tk.LabelFrame(
            detay_win, 
            text="⏳ ÇOKLU ZAMAN DİLİMİ (MTF) PERİYOTLARA GÖRE SİNYAL PANELI", 
            font=("Helvetica", 9, "bold"), 
            fg="#00E5FF", 
            bg="#18222d", 
            padx=8, pady=4
        )
        mtf_container.pack(fill="both", expand=True, padx=15, pady=(4, 8))

        cols = ("Zaman Periyodu", "TL Hacim", "Endeks Üstü Güç (%)", "AOF Farkı (%)", "RSI", "Skor", "PERİYOTA ÖZEL NET AKSİYON SİNYALİ")
        tree_mtf = ttk.Treeview(mtf_container, columns=cols, show="headings", height=4)

        for col in cols:
            tree_mtf.heading(col, text=col)
            w = 230 if col == "PERİYOTA ÖZEL NET AKSİYON SİNYALİ" else (115 if col in ["TL Hacim", "Endeks Üstü Güç (%)"] else 90)
            tree_mtf.column(col, anchor="center", width=w)

        tree_mtf.pack(fill="both", expand=True)

        def load_advanced_analysis():
            try:
                q_daily = Query().set_markets('turkey').select(
                    'name', 'close', 'volume', 'VWAP', 'change', 'high', 'low',
                    'average_volume_10d_calc', 'average_volume_30d_calc', 'SMA200', 'ATR'
                ).limit(650)
                _, df_d = q_daily.get_scanner_data()

                q_weekly = Query().set_markets('turkey').select(
                    'name', 'close|1W', 'volume|1W', 'VWAP|60', 'change|1W'
                ).limit(650)
                _, df_w = q_weekly.get_scanner_data()

                if df_d is not None and not df_d.empty:
                    h_d = df_d[df_d['name'] == hisse_kodu]
                    h_w = df_w[df_w['name'] == hisse_kodu] if df_w is not None and not df_w.empty else pd.DataFrame()

                    if not h_d.empty:
                        c_p = float(h_d['close'].values[0] or 0)
                        v_daily = float(h_d['volume'].values[0] or 0) * c_p
                        vwap_daily = float(h_d['VWAP'].values[0] or c_p)
                        high_p = float(h_d['high'].values[0] or c_p)
                        low_p = float(h_d['low'].values[0] or c_p)
                        sma200 = float(h_d['SMA200'].values[0] or (c_p * 0.88))
                        
                        atr_val = float(h_d['ATR'].values[0] if 'ATR' in h_d.columns and h_d['ATR'].values[0] is not None else (c_p * 0.03))
                        if atr_val <= 0:
                            atr_val = c_p * 0.03

                        giris_fiyati = c_p
                        aktif_sinyal = hisse_data["NET AKSİYON SİNYALİ"]

                        hedef_1 = giris_fiyati + (atr_val * 1.5)
                        hedef_2 = giris_fiyati + (atr_val * 3.0)
                        hedef_3 = giris_fiyati + (atr_val * 5.0)
                        stop_loss = giris_fiyati - (atr_val * 1.5)

                        atr_str = (
                            f"📌 Sinyal Segmenti: {aktif_sinyal}\n"
                            f"🚀 Referans Giriş Fiyatı: {giris_fiyati:.2f} TL  |  🛡️ Volatilite (ATR): {atr_val:.2f} TL\n"
                            f"🎯 Kar Al Hedef 1 (%{((hedef_1/giris_fiyati)-1)*100:+.1f}): {hedef_1:.2f} TL   |   "
                            f"🎯 Hedef 2 (%{((hedef_2/giris_fiyati)-1)*100:+.1f}): {hedef_2:.2f} TL   |   "
                            f"🎯 Hedef 3 (%{((hedef_3/giris_fiyati)-1)*100:+.1f}): {hedef_3:.2f} TL\n"
                            f"⛔ Risk Yönetimi Stop-Loss Sınırı (%{((stop_loss/giris_fiyati)-1)*100:.1f}): {stop_loss:.2f} TL"
                        )

                        if high_p > low_p:
                            buyer_ratio = ((c_p - low_p) / (high_p - low_p)) * 100
                            seller_ratio = 100 - buyer_ratio
                        else:
                            buyer_ratio = 50.0
                            seller_ratio = 50.0

                        if buyer_ratio >= 60.0:
                            bs_txt = f"⚖ Alıcı/Satıcı Denge: 🟢 %{buyer_ratio:.1f} ALICI AĞIRLIKLI (Güçlü Para Girişi Var)"
                            bs_color = "#00FF66"
                        elif seller_ratio >= 60.0:
                            bs_txt = f"⚖️️ Alıcı/Satıcı Denge: 🔴 %{seller_ratio:.1f} SATICI BASKILI (Para Çıkışı Var)"
                            bs_color = "#FF3333"
                        else:
                            bs_txt = f"⚖️ Alıcı/Satıcı Denge: ➡️ %{buyer_ratio:.1f} Alıcı / %{seller_ratio:.1f} Satıcı (Dengeli Piyasa)"
                            bs_color = "#FFD700"

                        v_weekly = v_daily * 5
                        vwap_weekly = vwap_daily
                        if not h_w.empty:
                            v_w_raw = float(h_w['volume|1W'].values[0] or 0)
                            if v_w_raw > 0: v_weekly = v_w_raw * c_p
                            vwap_w_raw = float(h_w['VWAP|60'].values[0] or 0)
                            if vwap_w_raw > 0: vwap_weekly = vwap_w_raw

                        v_monthly = v_weekly * 4
                        vwap_monthly = (vwap_daily * 0.4) + (vwap_weekly * 0.6)
                        vwap_12m = sma200

                        v_10d_avg = float(h_d['average_volume_10d_calc'].values[0] or 0) * c_p
                        w_vol_ratio = (v_daily / (v_10d_avg / 5)) if v_10d_avg > 0 else 1.0

                        vol_rows = [
                            ("Bu Günlük Canlı Hacim (1D)", f"{v_daily:,.0f}".replace(",", "."), "🟢 Aktif Seans"),
                            ("Bu Haftalık Toplam Hacim (1W)", f"{v_weekly:,.0f}".replace(",", "."), f"🔥 {w_vol_ratio:.1f}x Kat İvme" if w_vol_ratio > 1.2 else "➡️ Standart Akış"),
                            ("Aylık Tahmini Hacim Akışı", f"{v_monthly:,.0f}".replace(",", "."), "💎 Akümülasyon Var" if w_vol_ratio > 1.3 else "➡️ Normal"),
                            ("12 Aylık Hacim İvmesi", "Yıllık Kurumsal Hacim", "🚀 Yüksek Likidite")
                        ]

                        diff_d = ((c_p - vwap_daily) / vwap_daily * 100)
                        diff_w = ((c_p - vwap_weekly) / vwap_weekly * 100)
                        diff_m = ((c_p - vwap_monthly) / vwap_monthly * 100)
                        diff_12m = ((c_p - vwap_12m) / vwap_12m * 100)

                        cost_rows = [
                            ("Bu Günün AOF (VWAP) Maliyeti", f"{vwap_daily:.2f} TL", f"🟢 %{diff_d:+.2f} (Üstünde)" if diff_d >= 0 else f"🔴 %{diff_d:+.2f} (Altında)"),
                            ("Bu Haftanın Ort. AOF Maliyeti", f"{vwap_weekly:.2f} TL", f"🟢 %{diff_w:+.2f} (Üstünde)" if diff_w >= 0 else f"🔴 %{diff_w:+.2f} (Altında)"),
                            ("Bu Ayın Ort. AOF Maliyeti", f"{vwap_monthly:.2f} TL", f"🟢 %{diff_m:+.2f} (Üstünde)" if diff_m >= 0 else f"🔴 %{diff_m:+.2f} (Altında)"),
                            ("12 Aylık Genel Kurumsal Maliyet", f"{vwap_12m:.2f} TL", f"💎 %{diff_12m:+.2f} (Ana Destek)")
                        ]

                        def update_compare_ui():
                            self.lbl_buyer_seller.config(text=bs_txt, fg=bs_color)
                            self.lbl_atr_detay.config(text=atr_str)
                            for r in vol_rows:
                                tree_vol.insert("", "end", values=r)
                            for r in cost_rows:
                                tree_cost.insert("", "end", values=r)

                        detay_win.after(0, update_compare_ui)

                tf_map = {
                    "15 Dakika (15m)": "15",
                    "1 Saatlik (1h)": "60",
                    "4 Saatlik (4h)": "240",
                    "Günlük (1D)": "",
                    "Haftalık (1W)": "1W"
                }
                
                mtf_rows = []
                for label, suffix in tf_map.items():
                    c_col = f"close|{suffix}" if suffix else "close"
                    chg_col = f"change|{suffix}" if suffix else "change"
                    vol_col = f"volume|{suffix}" if suffix else "volume"
                    vol_avg_col = f"average_volume_10d_calc|{suffix}" if suffix else "average_volume_10d_calc"
                    vwap_col = f"VWAP|{suffix}" if suffix else "VWAP"
                    rsi_col = f"RSI|{suffix}" if suffix else "RSI"

                    q = Query().set_markets('turkey').select('name', c_col, chg_col, vol_col, vol_avg_col, vwap_col, rsi_col).limit(650)
                    _, df = q.get_scanner_data()

                    if df is not None and not df.empty:
                        bist_avg = df[chg_col].mean()
                        h_row = df[df['name'] == hisse_kodu]

                        if not h_row.empty:
                            c_val = float(h_row[c_col].values[0] or 0)
                            chg_val = float(h_row[chg_col].values[0] or 0)
                            vol_val = float(h_row[vol_col].values[0] or 0)
                            avg_vol_10d = float(h_row[vol_avg_col].values[0] or 0)
                            vwap_val = float(h_row[vwap_col].values[0] or 0)
                            rsi_val = float(h_row[rsi_col].values[0] or 50)

                            hacim_tl_per = vol_val * c_val
                            rvol = (vol_val / avg_vol_10d) if avg_vol_10d > 0 else 1.0

                            rel_p = chg_val - bist_avg
                            vwap_diff = ((c_val - vwap_val) / vwap_val * 100) if vwap_val > 0 else 0

                            if rel_p >= 2.0: guc_txt = f"🔥 +%{rel_p:.1f}"
                            elif rel_p >= 0.5: guc_txt = f"🟢 +%{rel_p:.1f}"
                            elif rel_p <= -1.5: guc_txt = f"🔻 %{rel_p:.1f}"
                            else: guc_txt = f"➡️ %{rel_p:.1f}"

                            p_skor = 30
                            if rvol >= 2.5: p_skor += 30
                            if rel_p >= 1.5: p_skor += 20
                            if 0.0 <= vwap_diff <= 2.0: p_skor += 20

                            if chg_val >= 7.5 or rsi_val > 80:
                                p_sinyal = "⚠️ UZAK DUR (Aşırı Primli)"
                            elif p_skor >= 70 and rvol >= 1.3:
                                p_sinyal = "🚀 ŞU AN GİR (Kalkış Var)"
                            elif rvol >= 3.0:
                                p_sinyal = "🛡️ SPEK-SAVAR (Hacim Patlaması)"
                            elif rsi_val <= 38:
                                p_sinyal = "🔄 DİP DÖNÜŞÜ WESS"
                            elif p_skor >= 60:
                                p_sinyal = "💎 GÜÇLÜ AL"
                            else:
                                p_sinyal = "👀 İZLEMEDE KAL"

                            mtf_rows.append((
                                label, 
                                f"{hacim_tl_per:,.0f}".replace(",", "."), 
                                guc_txt, 
                                f"%{vwap_diff:.2f}", 
                                f"{rsi_val:.1f}", 
                                p_skor, 
                                p_sinyal
                            ))

                def ui_update_mtf():
                    for r in mtf_rows:
                        tree_mtf.insert("", "end", values=r)

                detay_win.after(0, ui_update_mtf)

            except Exception:
                pass

        threading.Thread(target=load_advanced_analysis, daemon=True).start()

    def rehber_penceresi_ac(self):
        rehber = tk.Toplevel(self.root)
        rehber.title("ℹ WESS VIP RADAR PRO - DETAYLI ŞEMATİK SİSTEM REHBERİ")
        rehber.geometry("900x800")
        rehber.configure(bg="#121212")

        txt = tk.Text(rehber, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 10), padx=15, pady=15)
        txt.pack(fill="both", expand=True, padx=10, pady=10)

        txt.tag_config("title", foreground="#00ffcc", font=("Helvetica", 12, "bold"))
        txt.tag_config("schema", foreground="#00E5FF", font=("Consolas", 10, "bold"))
        txt.tag_config("yellow", foreground="#FFD700", font=("Helvetica", 10, "bold"))
        txt.tag_config("orange", foreground="#D35400", font=("Helvetica", 10, "bold"))
        txt.tag_config("purple", foreground="#DDA0DD", font=("Helvetica", 10, "bold"))
        txt.tag_config("dark_purple", foreground="#9d4edd", font=("Helvetica", 10, "bold"))
        txt.tag_config("blue", foreground="#00b4d8", font=("Helvetica", 10, "bold"))
        txt.tag_config("green", foreground="#00FF66", font=("Helvetica", 10, "bold"))
        txt.tag_config("brown", foreground="#E6C200", font=("Helvetica", 10, "bold"))
        txt.tag_config("gray", foreground="#aaaaaa", font=("Helvetica", 10, "bold"))
        txt.tag_config("red", foreground="#FF3333", font=("Helvetica", 10, "bold"))

        txt.insert("end", "📊 BORSADA ZARAR ETMEME, TAHTACIYI OKUMA & DİĞERLERİNDEN ÖNE GEÇME ŞEMASI\n\n", "title")

        schema_text = """
  +---------------------------------------------------------------------------------+
  |                        1. KURAL: RİSKİ YÖNET (UZAK DUR)                        |
  |  ⚠️️ Kırmızı [UZAK DUR]: Günlük %7.5+ primli veya RSI > 80. Asla atlama, düzeltir.|
  +---------------------------------------------------------------------------------+
                                         |
                                         v
  +---------------------------------------------------------------------------------+
  |                        2. KURAL: TRENDİ YAKALA (ŞU AN GİR & KİLİTLİ AL)        |
  |  🚀 Sarı [ŞU AN GİR]: Hacim patlaması + VWAP üstü + Yüksek Skor. En net kalkış.  |
  |  🔒 Mavi [KİLİTLİ AL]: Bollinger dar bantta sıkışmış, hacimle yukarı kırıyor.   |
  +---------------------------------------------------------------------------------+
                                         |
                                         v
  +---------------------------------------------------------------------------------+
  |                        3. KURAL: PİYASA ÇÖKERKEN LİDER KAL (ENDEKSİ EZENLER)     |
  |  🔥 Turuncu [ENDEKSİ EZENLER]: BIST eksi/yatayken bile endekse +%2 fark atanlar. |
  +---------------------------------------------------------------------------------+
                                         |
                                         v
  +---------------------------------------------------------------------------------+
  |                        4. KURAL: DİPTEN MAL TOPLAMA (DİP DÖNÜŞÜ & SPEK-SAVAR)    |
  |  🔄 Açık Mor [DİP DÖNÜŞÜ]: RSI 30-38 bandında dip dönüşü yapıyor (Ucuz maliyet).|
  |  🛡️️ Koyu Mor [SPEK-SAVAR]: Ortalamanın 3.5 katı hacimle tahtacı mal topluyor.   |
  +---------------------------------------------------------------------------------+
        \n"""
        txt.insert("end", schema_text, "schema")

        txt.insert("end", "TÜM DONELERİN VE GÖSTERGELERİN DETAYLI AÇIKLAMALARI:\n", "title")
        txt.insert("end", "---------------------------------------------------------------------------------\n")

        txt.insert("end", "1. SKOR SİSTEMİ (0 - 100 Puan): ", "yellow")
        txt.insert("end", "Hissenin hacim ivmesi, RVOL, endeks göreceli gücü, VWAP konumu ve RSI durumuna göre dinamik hesaplanır. 65 ve üzeri puanlar yüksek potansiyel barındırır.\n\n")

        txt.insert("end", "2. RVOL (Göreceli Hacim İvmesi): ", "blue")
        txt.insert("end", "Mevcut periyot hacminin 10 günlük ortalama hacme oranıdır. 1.5x ve üzeri değerler kurumsal para girişine işaret eder.\n\n")

        txt.insert("end", "3. AOF / VWAP MALİYETİ: ", "green")
        txt.insert("end", "Hacim ağırlıklı ortalama fiyattır. Fiyatın VWAP üzerinde olması alıcıların o seansta maliyet üstünlüğüne sahip olduğunu gösterir.\n\n")

        txt.insert("end", "4. ATR TABANLI HEDEFLER: ", "yellow")
        txt.insert("end", "Volatiliteye (Average True Range) göre otomatik hesaplanan Kar Al (Hedef 1, 2, 3) ve Stop-Loss seviyeleridir. Disiplinli kar almayı sağlar.\n\n")

        txt.insert("end", "5. ETİKETLERİN ANLAMLARI:\n", "title")
        txt.insert("end", "• 🚀 ŞU AN GİR [SARI]: ", "yellow")
        txt.insert("end", "Yüksek öncelikli hareketli kalkış bölgesi.\n")
        txt.insert("end", "• 🔥 ENDEKSİ EZENLER [TURUNCU]: ", "orange")
        txt.insert("end", "Piyasadan bağımsız pozitif ayrışan liderler.\n")
        txt.insert("end", "• 🔄 DİP DÖNÜŞÜ WESS [AÇIK MOR]: ", "purple")
        txt.insert("end", "RSI dip seviyelerden yukarı yönlü toparlanma bölgesi.\n")
        txt.insert("end", "• 🛡️ SPEK-SAVAR [KOYU MOR]: ", "dark_purple")
        txt.insert("end", "3.5 kat ve üzeri olağanüstü hacim yığma bölgesi.\n")
        txt.insert("end", "• 🔒 KİLİTLİ AL [AÇIK MAVİ]: ", "blue")
        txt.insert("end", "Sıkışma bandının yukarı kırılım anı.\n")
        txt.insert("end", "• 💎 GÜÇLÜ AL [YEŞİL]: ", "green")
        txt.insert("end", "Sağlıklı yükseliş trendindeki hisseler.\n")
        txt.insert("end", "• ⚠️️ UZAK DUR [KIRMIZI]: ", "red")
        txt.insert("end", "Aşırı primli, düzeltme riski taşıyan kağıtlar.\n\n")

        txt.config(state="disabled")

    def karta_tiklandi(self, tag_code):
        if self.selected_tag_filter == tag_code:
            self.selected_tag_filter = None
        else:
            self.selected_tag_filter = tag_code
        self.filtrele_ve_guncelle()

    def filtreyi_sifirla(self):
        self.selected_tag_filter = None
        self.search_var.set("")
        self.index_filter_var.set("TÜM BIST")
        self.filtrele_ve_guncelle()

    def toggle_auto_refresh(self):
        if self.auto_refresh_var.get():
            self.lbl_status.config(text="Otomatik yenileme aktif.", fg="#00D2FF")
            self.tarama_baslat_thread()
        else:
            if self.auto_refresh_job:
                self.root.after_cancel(self.auto_refresh_job)
                self.auto_refresh_job = None
            self.lbl_status.config(text="Otomatik yenileme durduruldu.", fg="#aaaaaa")

    def schedule_next_refresh(self):
        if not self.auto_refresh_var.get():
            return
            
        secenek = self.interval_var.get()
        ms = 10000
        if secenek == "30 Saniye": ms = 30000
        elif secenek == "1 Dakika": ms = 60000
        elif secenek == "5 Dakika": ms = 300000

        self.auto_refresh_job = self.root.after(ms, self.tarama_baslat_thread)

    def tarama_baslat_thread(self):
        if self.auto_refresh_job:
            self.root.after_cancel(self.auto_refresh_job)
            self.auto_refresh_job = None

        self.btn_tara.config(state="disabled")
        secili_periyot = self.timeframe_var.get()
        self.lbl_status.config(text=f"Endeksler ve Hisseler ({secili_periyot}) taranıyor...", fg="#ffcc00")
        threading.Thread(target=self.canli_bist_tara, daemon=True).start()

    def canli_bist_tara(self):
        results = []
        index_results = []
        
        real_bist_banks = ["AKBNK", "GARAN", "ISCTR", "YKBNK", "HALKB", "VAKBN", "TSKB", "ALBRK", "KLNMA", "QNBFB"]

        try:
            secili_periyot = self.timeframe_var.get()
            
            tf_map = {
                "5 Dakika (5m)": "5", 
                "10 Dakika (10m)": "10", 
                "15 Dakika (15m)": "15", 
                "30 Dakika (30m)": "30",
                "1 Saatlik (60m)": "60", 
                "2 Saatlik (120m)": "120", 
                "3 Saatlik (180m)": "180", 
                "4 Saatlik (240m)": "240", 
                "Günlük (1D)": "", 
                "Haftalık (1W)": "1W", 
                "Aylık (1M)": "1M"
            }
            
            suffix = tf_map.get(secili_periyot, "")
            
            close_col = f"close|{suffix}" if suffix else "close"
            change_col = f"change|{suffix}" if suffix else "change"
            volume_col = f"volume|{suffix}" if suffix else "volume"
            vol_avg_col = f"average_volume_10d_calc|{suffix}" if suffix else "average_volume_10d_calc"
            vwap_col = f"VWAP|{suffix}" if suffix else "VWAP"
            rsi_col = f"RSI|{suffix}" if suffix else "RSI"
            bb_upper_col = f"BB.upper|{suffix}" if suffix else "BB.upper"
            bb_lower_col = f"BB.lower|{suffix}" if suffix else "BB.lower"

            q = (
                Query()
                .set_markets('turkey')
                .select(
                    'name', 'sector', close_col, change_col, volume_col, vol_avg_col, 
                    vwap_col, rsi_col, bb_upper_col, bb_lower_col
                )
                .limit(650)
            )
            count, df_data = q.get_scanner_data()

            if df_data is not None and not df_data.empty:
                bist_genel_degisim = df_data[change_col].mean()

                if bist_genel_degisim >= 0.5:
                    mode_txt = "⚙️ [MOD: Endeks Pozitif - Fırsat Eşiği Düşük]"
                    mode_fg = "#00FF66"
                elif bist_genel_degisim <= -0.5:
                    mode_txt = "⚙️️ [MOD: Endeks Zayıf - Koruma Filtresi Aktif]"
                    mode_fg = "#FF3333"
                else:
                    mode_txt = "⚙️ [MOD: Endeks Yatay - Standart Filtre]"
                    mode_fg = "#FFD700"

                self.root.after(0, lambda: self.lbl_search_mode.config(text=mode_txt, fg=mode_fg))

                sector_performance = {}
                if 'sector' in df_data.columns:
                    sector_perf = df_data.groupby('sector')[change_col].mean().to_dict()
                    sector_performance = {k: round(v, 2) for k, v in sector_perf.items() if k}

                for _, row in df_data.iterrows():
                    try:
                        hisse = str(row.get('name', '')).strip()
                        sektor_adi = str(row.get('sector', 'Diğer')).strip()
                        fiyat = float(row.get(close_col, 0) or 0)
                        fark = float(row.get(change_col, 0) or 0)
                        lot_hacmi = float(row.get(volume_col, 0) or 0)
                        avg_lot_10d = float(row.get(vol_avg_col, 0) or 0)
                        
                        vwap_raw = row.get(vwap_col, None)
                        rsi_raw = row.get(rsi_col, None)
                        bb_up_raw = row.get(bb_upper_col, None)
                        bb_low_raw = row.get(bb_lower_col, None)

                        hacim_tl = lot_hacmi * fiyat

                        if fiyat <= 0 or not hisse:
                            continue

                        sektor_kat = "DİĞER"
                        sec_lower = sektor_adi.lower()
                        
                        if hisse in real_bist_banks:
                            sektor_kat = "BANKACILIK"
                        elif any(x in sec_lower for x in ["industrial", "producer", "process", "sanayi"]):
                            sektor_kat = "SANAYİ"
                        elif any(x in sec_lower for x in ["real estate", "gyo"]):
                            sektor_kat = "GYO"
                        elif any(x in sec_lower for x in ["holding"]):
                            sektor_kat = "HOLDİNG"
                        elif any(x in sec_lower for x in ["tech", "software", "bilişim"]):
                            sektor_kat = "BİLİŞİM"
                        elif any(x in sec_lower for x in ["transportation", "ulas"]):
                            sektor_kat = "ULAŞTIRMA"
                        elif any(x in sec_lower for x in ["food", "gıda"]):
                            sektor_kat = "GIDA"
                        elif any(x in sec_lower for x in ["chemical", "kimya"]):
                            sektor_kat = "KİMYA"
                        elif any(x in sec_lower for x in ["telecom", "iletişim"]):
                            sektor_kat = "İLETİŞİM"

                        rvol = (lot_hacmi / avg_lot_10d) if (avg_lot_10d > 0) else 1.0

                        vwap_fark = 0.0
                        has_vwap = False
                        if vwap_raw is not None and not np.isnan(vwap_raw) and float(vwap_raw) > 0:
                            vwap = float(vwap_raw)
                            vwap_fark = ((fiyat - vwap) / vwap) * 100
                            has_vwap = True

                        rsi = float(rsi_raw) if (rsi_raw is not None and not np.isnan(rsi_raw)) else 50.0

                        is_tight_band = False
                        if (bb_up_raw is not None and bb_low_raw is not None and 
                            not np.isnan(bb_up_raw) and not np.isnan(bb_low_raw)):
                            bb_up = float(bb_up_raw)
                            bb_low = float(bb_low_raw)
                            if bb_low > 0:
                                band_width = ((bb_up - bb_low) / fiyat) * 100
                                if band_width <= 6.0:
                                    is_tight_band = True

                        is_rsi_dip_reentry = (30.0 <= rsi <= 38.0) and (fark >= -0.2)

                        is_ezeller = False
                        endeks_fark = fark - bist_genel_degisim
                        if endeks_fark >= 2.0:
                            endeks_gucu_txt = f"🔥 +%{endeks_fark:.1f} (Eziyor)"
                            is_ezeller = True
                        elif endeks_fark >= 0.5:
                            endeks_gucu_txt = f"🟢 +%{endeks_fark:.1f} (Üstü)"
                        elif endeks_fark <= -1.5:
                            endeks_gucu_txt = f"🔻 %{endeks_fark:.1f} (Zayıf)"
                        else:
                            endeks_gucu_txt = f"➡️ %{endeks_fark:.1f} (Paralel)"

                        skor = 20
                        sektor_ort_degisim = sector_performance.get(sektor_adi, 0.0)
                        sektor_etiket = "🔥 POZİTİF" if sektor_ort_degisim >= 0.8 else ("⚠️ ZAYIF" if sektor_ort_degisim < -0.5 else "➡️ NÖTR")

                        if sektor_ort_degisim >= 1.0: skor += 15
                        elif sektor_ort_degisim < -0.8: skor -= 10

                        if rvol >= 3.0: skor += 40
                        elif rvol >= 2.0: skor += 30
                        elif rvol >= 1.2: skor += 15

                        if endeks_fark >= 2.0: skor += 20

                        if is_tight_band: skor += 20
                        if is_rsi_dip_reentry: skor += 30

                        if has_vwap and 0.0 <= vwap_fark <= 2.0: skor += 15
                        elif has_vwap and -0.5 <= vwap_fark < 0.0: skor += 10

                        if 0.5 <= fark <= 4.0: skor += 15
                        elif 4.0 < fark <= 6.0: skor += 10

                        if hacim_tl >= 15_000_000: skor += 10

                        min_skor_kalkis = 75
                        min_rvol_kalkis = 1.5
                        if bist_genel_degisim >= 0.5:
                            min_skor_kalkis = 65
                            min_rvol_kalkis = 1.2

                        tag = "IZLE"

                        if fark >= 7.5 or rsi > 80.0:
                            sinyal = "⚠ UZAK DUR (PRİMLENDİ)"
                            tag = "UZAK_DUR"
                        elif (skor >= min_skor_kalkis and rvol >= min_rvol_kalkis and 0.5 <= fark <= 5.5):
                            sinyal = "🚀 ŞU AN GİR (WESS DİNAMİK KALKIŞ)"
                            tag = "KALKIS"
                        elif (rvol >= 3.5 and 1.0 <= fark <= 6.0):
                            sinyal = "🛡️ WESS SPEK-SAVAR (HACİM PATLAMASI)"
                            tag = "SPEK_SAVAR"
                        elif (is_tight_band and rvol >= 2.0 and 0.0 <= vwap_fark <= 1.5):
                            sinyal = "🔒 KİLİTLİ AL (SIKIŞMA BREAKOUT)"
                            tag = "KILITLI_AL"
                        elif is_rsi_dip_reentry:
                            sinyal = "🔄 DİP DÖNÜŞÜ WESS"
                            tag = "DIP_DONUS"
                        elif skor >= 65 and 0.0 <= vwap_fark <= 2.5:
                            sinyal = "💎 TAM ZAMANI (GÜÇLÜ AL)"
                            tag = "GUC_AL"
                        elif (is_tight_band or (abs(vwap_fark) <= 0.8 and rvol >= 1.1)) and -1.0 <= fark <= 2.5:
                            sinyal = "🔥 SIKIŞIYOR (TOPLANIYOR)"
                            tag = "SIKISMA"
                        else:
                            sinyal = "👀 İZLEMEDE KAL"
                            tag = "IZLE"

                        results.append({
                            "Hisse": hisse,
                            "Sektör": sektor_adi,
                            "Sektör_Kategori": sektor_kat,
                            "Sektör Gücü": sektor_etiket,
                            "Skor": skor,
                            "Son Fiyat (TL)": round(fiyat, 2),
                            "Hacim (TL)": f"{hacim_tl:,.0f}".replace(",", "."),
                            "Değişim (%)": round(fark, 2),
                            "Endeks Üstü Güç": endeks_gucu_txt,
                            "AOF Farkı (%)": round(vwap_fark, 2),
                            "NET AKSİYON SİNYALİ": sinyal,
                            "Tag": tag,
                            "Is_Ezeller": is_ezeller,
                            "RSI": rsi,
                            "Band_Tight": is_tight_band
                        })
                    except Exception:
                        continue

            if results:
                df_res = pd.DataFrame(results)
                
                target_indices = [
                    ("XU100", "BIST 100", "TÜM BIST"),
                    ("XUSIN", "SANAYİ ENDEKSİ", "SANAYİ"),
                    ("XBANK", "BANKACILIK ENDEKSİ", "BANKACILIK"),
                    ("XGMYO", "GYO ENDEKSİ", "GYO"),
                    ("XHOLD", "HOLDİNG ENDEKSİ", "HOLDİNG"),
                    ("XBLSM", "BİLİŞİM ENDEKSİ", "BİLİŞİM"),
                    ("XULAS", "ULAŞTIRMA ENDEKSİ", "ULAŞTIRMA"),
                    ("XKMYA", "KİMYA ENDEKSİ", "KİMYA"),
                    ("XGIDA", "GIDA ENDEKSİ", "GIDA")
                ]

                for code, name, kat in target_indices:
                    if kat == "TÜM BIST":
                        sub_df = df_res
                    else:
                        sub_df = df_res[df_res["Sektör_Kategori"] == kat]

                    if not sub_df.empty:
                        avg_change = sub_df["Değişim (%)"].mean()
                        avg_rsi = sub_df["RSI"].mean()
                        tight_ratio = sub_df["Band_Tight"].mean()

                        sikisma_txt = "🔥 VAR" if tight_ratio >= 0.25 else "HAYIR"

                        if avg_rsi <= 38.0 and avg_change >= -0.2:
                            idx_sinyal = "🔄 DİP DÖNÜŞÜ WESS (DİPTE)"
                            idx_tag = "DIP_DONUS"
                        elif avg_change >= 0.8 and avg_rsi >= 52.0:
                            idx_sinyal = "🚀 ŞU AN GİR (KALKIŞ VAR)"
                            idx_tag = "KALKIS"
                        elif sikisma_txt == "🔥 VAR":
                            idx_sinyal = "🔥 SIKIŞIYOR (Sıkışma Yüksek)"
                            idx_tag = "SIKISMA"
                        elif avg_change > 0:
                            idx_sinyal = "💎 GÜÇLÜ (Pozitif Trend)"
                            idx_tag = "GUC_AL"
                        else:
                            idx_sinyal = "👀 İZLEMEDE KAL (Nötr)"
                            idx_tag = "IZLE"

                        index_results.append({
                            "Endeks Kodu": code,
                            "Endeks Adı": name,
                            "Son Puan": f"Ort %{avg_change:+.2f}",
                            "Değişim (%)": round(avg_change, 2),
                            "RSI (14)": round(avg_rsi, 1),
                            "Sıkışma": sikisma_txt,
                            "ENDEKS AKSİYON SİNYALİ": idx_sinyal,
                            "Tag": idx_tag
                        })

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Veri Çekme Hatası: {str(e)}", parent=self.root))

        self.root.after(0, self.ekrani_guncelle, results, index_results)

    def ekrani_guncelle(self, results, index_results):
        self.raw_results = results
        self.raw_index_results = index_results

        for item in self.tree_index.get_children():
            self.tree_index.delete(item)

        for row in index_results:
            self.tree_index.insert("", "end", values=(
                row["Endeks Kodu"], row["Endeks Adı"], row["Son Puan"], 
                row["Değişim (%)"], row["RSI (14)"], row["Sıkışma"], 
                row["ENDEKS AKSİYON SİNYALİ"]
            ))

        self.filtrele_ve_guncelle()

        periyot = self.timeframe_var.get()
        self.lbl_status.config(text=f"✅ [{periyot}] Güncellendi!", fg="#00ffcc")
        self.btn_tara.config(state="normal")

        self.schedule_next_refresh()

    def filtrele_ve_guncelle(self, *args):
        for item in self.tree_kalkis.get_children():
            self.tree_kalkis.delete(item)
        for item in self.tree_main.get_children():
            self.tree_main.delete(item)

        if not self.raw_results:
            return

        arama = str(self.search_var.get()).strip().upper()
        secili_endeks_filtre = self.index_filter_var.get()
        
        rapor_df = pd.DataFrame(self.raw_results).sort_values(by="Skor", ascending=False)

        if secili_endeks_filtre != "TÜM BIST":
            if "SANAYİ" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "SANAYİ"]
            elif "BANKA" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "BANKACILIK"]
            elif "GYO" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "GYO"]
            elif "HOLDİNG" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "HOLDİNG"]
            elif "BİLİŞİM" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "BİLİŞİM"]
            elif "ULAŞTIRMA" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "ULAŞTIRMA"]
            elif "GIDA" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "GIDA"]
            elif "KİMYA" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "KİMYA"]
            elif "İLETİŞİM" in secili_endeks_filtre:
                rapor_df = rapor_df[rapor_df["Sektör_Kategori"] == "İLETİŞİM"]

        self.cnt_kalkis.config(text=str(len(rapor_df[rapor_df["Tag"] == "KALKIS"])))
        self.cnt_ezeller.config(text=str(len(rapor_df[rapor_df["Is_Ezeller"] == True])))
        self.cnt_dip.config(text=str(len(rapor_df[rapor_df["Tag"] == "DIP_DONUS"])))
        self.cnt_spek.config(text=str(len(rapor_df[rapor_df["Tag"] == "SPEK_SAVAR"])))
        self.cnt_kilit.config(text=str(len(rapor_df[rapor_df["Tag"] == "KILITLI_AL"])))
        self.cnt_guc_al.config(text=str(len(rapor_df[rapor_df["Tag"] == "GUC_AL"])))
        self.cnt_sikisma.config(text=str(len(rapor_df[rapor_df["Tag"] == "SIKISMA"])))
        self.cnt_izle.config(text=str(len(rapor_df[rapor_df["Tag"] == "IZLE"])))
        self.cnt_uzak_dur.config(text=str(len(rapor_df[rapor_df["Tag"] == "UZAK_DUR"])))

        tag_labels = {
            "KALKIS": "🚀 ŞU AN GİR",
            "EZENLER": "🔥 ENDEKSİ EZENLER",
            "DIP_DONUS": "🔄 DİP DÖNÜŞÜ WESS",
            "SPEK_SAVAR": "🛡 SPEK-SAVAR",
            "KILITLI_AL": "🔒 KİLİTLİ AL",
            "GUC_AL": "💎 GÜÇLÜ AL",
            "SIKISMA": "🔥 SIKIŞIYOR",
            "IZLE": "👀 İZLEMEDE KAL",
            "UZAK_DUR": "⚠ UZAK DUR"
        }
        
        if self.selected_tag_filter:
            lbl_txt = f"[{tag_labels.get(self.selected_tag_filter, '')} Filtrelendi - {secili_endeks_filtre}]"
            self.lbl_active_filter.config(text=lbl_txt, fg="#00ffcc")
        else:
            self.lbl_active_filter.config(text=f"[{secili_endeks_filtre} Listeleniyor]", fg="#aaaaaa")

        sadece_kalkis = rapor_df[rapor_df["Tag"] == "KALKIS"].reset_index(drop=True)
        if arama:
            sadece_kalkis = sadece_kalkis[sadece_kalkis["Hisse"].astype(str).str.upper().str.contains(arama, na=False)].reset_index(drop=True)

        for idx, row in sadece_kalkis.iterrows():
            self.tree_kalkis.insert("", "end", values=(
                idx + 1, row["Hisse"], row["Sektör Gücü"], row["Skor"], row["Son Fiyat (TL)"], 
                row["Hacim (TL)"], row["Değişim (%)"], row["Endeks Üstü Güç"],
                row["AOF Farkı (%)"], row["NET AKSİYON SİNYALİ"]
            ))

        genel_liste = rapor_df.reset_index(drop=True)
        
        if self.selected_tag_filter:
            if self.selected_tag_filter == "EZENLER":
                genel_liste = genel_liste[genel_liste["Is_Ezeller"] == True].reset_index(drop=True)
            else:
                genel_liste = genel_liste[genel_liste["Tag"] == self.selected_tag_filter].reset_index(drop=True)

        if arama:
            genel_liste = genel_liste[genel_liste["Hisse"].astype(str).str.upper().str.contains(arama, na=False)].reset_index(drop=True)

        for idx, row in genel_liste.iterrows():
            self.tree_main.insert("", "end", values=(
                idx + 1, row["Hisse"], row["Sektör Gücü"], row["Skor"], row["Son Fiyat (TL)"], 
                row["Hacim (TL)"], row["Değişim (%)"], row["Endeks Üstü Güç"],
                row["AOF Farkı (%)"], row["NET AKSİYON SİNYALİ"]
            ), tags=(row["Tag"],))

# ---------------------------------------------------------
# 5. UYGULAMA BAŞLATICI
# ---------------------------------------------------------
def main():
    import streamlit as st
    st.title("WESS VIP RADAR")

    app = WessVIPRadarApp(None)
    
    if st.button("Taramayı Başlat"):
        st.info("Veriler güncelleniyor ve analiz ediliyor...")
        app.filtrele_ve_guncelle()
        
        if hasattr(app, 'genel_liste') and not app.genel_liste.empty:
            st.success("Tarama başarıyla tamamlandı!")
            st.dataframe(app.genel_liste, use_container_width=True)
        else:
            st.warning("Gösterilecek veri bulunamadı.")
   # login_dialog = LoginDialog(root)
 #   root.wait_window(login_dialog)
#
  #  if login_dialog.is_authenticated:
#        app = WessVIPRadarApp(root)
 #       root.mainloop()
 #   else:
 #       root.destroy()

if __name__ == "__main__":
    main()