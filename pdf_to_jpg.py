import os
import pymupdf
from PIL import Image

# Klasör yolları
source_dir = r'c:\Users\Victus\Desktop\2026 Veritas Guncel Duzenlenmıs Katalog PDF'
jpg_dir = os.path.join(source_dir, 'jpg')

# jpg klasörü oluştur
os.makedirs(jpg_dir, exist_ok=True)

# PDF dosyalarını bul
pdf_files = sorted([f for f in os.listdir(source_dir) if f.lower().endswith('.pdf')])

print(f"Toplam {len(pdf_files)} PDF dosyasi bulundu.\n")

for i, pdf_file in enumerate(pdf_files, 1):
    pdf_path = os.path.join(source_dir, pdf_file)
    file_name_without_ext = os.path.splitext(pdf_file)[0]
    
    try:
        # PDF'i aç
        pdf_document = pymupdf.open(pdf_path)
        
        # Her sayfa için JPG oluştur
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Yüksek kalitede render et (300 DPI)
            mat = pymupdf.Matrix(2, 2)  # 2x zoom = ~300 DPI
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # JPG dosya adını oluştur
            if len(pdf_document) == 1:
                # Tek sayfalı PDF: orijinal adı kullan
                jpg_file = f"{file_name_without_ext}.jpg"
            else:
                # Çok sayfalı PDF: sayfa numarasıyla adlandır
                jpg_file = f"{file_name_without_ext}_sayfa_{page_num + 1}.jpg"
            
            jpg_path = os.path.join(jpg_dir, jpg_file)
            
            # JPG olarak kaydet
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(jpg_path, "JPEG", quality=95)
        
        pdf_document.close()
        print(f"[{i}/{len(pdf_files)}] OK {pdf_file}")
        
    except Exception as e:
        print(f"[{i}/{len(pdf_files)}] ERROR {pdf_file} - {str(e)}")

print(f"\nDonusturme tamamlandi! Dosyalar '{jpg_dir}' klasorune kaydedildi.")
