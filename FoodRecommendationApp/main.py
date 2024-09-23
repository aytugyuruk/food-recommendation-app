import os
import tkinter as tk
import json
import sys

# JSON dosyasının bulunduğu dizini belirle
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
json_file_path = os.path.join(base_path, 'tarifler.json')

# JSON dosyasını oku ve tarifleri yükle
with open(json_file_path, 'r', encoding='utf-8') as f:
    tarifler = json.load(f)

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Yemek Öneri Uygulaması")

# Modern renk paleti
bg_color = "#F4F4F9"  # Arka plan rengi
primary_color = "#3A86FF"  # Birincil buton ve başlık rengi
secondary_color = "#FF006E"  # İkincil vurgu rengi
text_color = "#22223B"  # Metin rengi
entry_bg_color = "#FFFFFF"  # Giriş alanı arka plan rengi
entry_border_color = "#D1D1E9"  # Giriş alanı kenarlık rengi

# Pencere boyutunu ayarla ve arka plan rengini belirle
root.geometry("600x500")
root.configure(bg=bg_color)

# Başlık etiketi
title_label = tk.Label(root, text="Buzdolabındaki Malzemeler:", font=("Arial", 14), bg=bg_color, fg=text_color)
title_label.pack(pady=10)

# Kullanıcı girişi için giriş alanı
malzemeler_giris = tk.Entry(root, width=50, font=("Arial", 12), bg=entry_bg_color, fg=text_color, highlightbackground=entry_border_color, highlightthickness=2, bd=0)
malzemeler_giris.pack(pady=10)

# Yemek öner butonu
def yemek_oner():
    malzemeler = malzemeler_giris.get().lower().split(",")
    malzemeler = [malzeme.strip() for malzeme in malzemeler]
    uygun_tarifler = []

    for tarif in tarifler:
        tarif_malzeme_seti = set(tarif['malzemeler'])
        girilen_malzeme_seti = set(malzemeler)
        
        if girilen_malzeme_seti.issubset(tarif_malzeme_seti):
            eksik_malzemeler = tarif_malzeme_seti - girilen_malzeme_seti
            if eksik_malzemeler:
                uygun_tarifler.append(f"{tarif['isim']} (Eksik malzemeler: {', '.join(eksik_malzemeler)})")
            else:
                uygun_tarifler.append(tarif['isim'])

    # Sonuçları güncelle
    sonuc.delete(1.0, tk.END)
    if uygun_tarifler:
        sonuc.insert(tk.END, "Önerilen Yemekler:\n" + "\n".join(uygun_tarifler))
    else:
        sonuc.insert(tk.END, "Bu malzemelerle bir tarif bulunamadı.")

# Modern buton tasarımı
yemek_oner_btn = tk.Button(root, text="Yemek Öner", command=yemek_oner, font=("Arial", 12, "bold"), bg=primary_color, fg="white", activebackground=secondary_color, bd=0, padx=20, pady=10, cursor="hand2")
yemek_oner_btn.pack(pady=20)

# Sonuçları göstermek için bir text widget ve kaydırma çubuğu
sonuc_frame = tk.Frame(root, bg=bg_color)
sonuc_frame.pack(pady=20, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(sonuc_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

sonuc = tk.Text(sonuc_frame, font=("Arial", 12), wrap=tk.WORD, yscrollcommand=scrollbar.set, bg=entry_bg_color, fg=text_color, bd=0, padx=10, pady=10)
sonuc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=sonuc.yview)

# Ana döngüyü başlat
root.mainloop()
