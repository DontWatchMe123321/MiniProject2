import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    import matplotlib.pyplot as plt
    plt.close('all') 

    input_path = os.path.join('input', 'parking.jpg') 
    output_dir = 'output'
    output_path = os.path.join(output_dir, 'result_atap_kepadatan.png') 

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Citra tidak ditemukan di jalur: {input_path}")
        return

    img_output = img.copy()
    img_plot = cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(blurred, 140, 255, cv2.THRESH_BINARY)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close)
    img_debug_bw = cv2.cvtColor(closed, cv2.COLOR_GRAY2RGB)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_mobil = 0
    total_bukan_mobil = 0

    batas_kepadatan = 0.50 

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        if w > 15 and h > 15:
            
            roi_atap = closed[y:y+h, x:x+w]
            
            jumlah_putih = cv2.countNonZero(roi_atap)
            luas_kotak = w * h
            persentase_kepadatan = float(jumlah_putih) / luas_kotak

            if persentase_kepadatan >= batas_kepadatan:
                total_mobil += 1
                
                cv2.rectangle(img_debug_bw, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img_debug_bw, f"{persentase_kepadatan:.2f}", (x, y - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                
                cv2.rectangle(img_plot, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img_plot, "Mobil", (x, y - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            else:
                total_bukan_mobil += 1
            
                cv2.rectangle(img_debug_bw, (x, y), (x + w, y + h), (255, 0, 0), 1)
                cv2.putText(img_debug_bw, f"{persentase_kepadatan:.2f}", (x, y - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                
                cv2.rectangle(img_plot, (x, y), (x + w, y + h), (255, 0, 0), 1)

    img_save = cv2.cvtColor(img_plot, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, img_save)

    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(thresh, cmap='gray')
    plt.title("1. Threshold Atap (Tanpa Canny)")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(img_debug_bw)
    plt.title("2. Cek Kepadatan (Angka = Rasio Putih)")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(img_plot)
    plt.title(f"3. Hasil (Mobil Padat: {total_mobil} | Bolong/Noise: {total_bukan_mobil})")
    plt.axis('off')

    plt.tight_layout()
    plt.show() 

if __name__ == "__main__":
    main()