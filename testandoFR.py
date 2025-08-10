import cv2
import face_recognition as fr

def load_rgb(path, use_cv2=False):
    if use_cv2:
        bgr = cv2.imread(path)
        if bgr is None:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    else:
        # face_recognition.load_image_file já entrega RGB
        img = fr.load_image_file(path)
        if img is None:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        return img

p1 = r"C:\Users\lucas\Downloads\WhatsApp Unknown 2025-08-07 at 11.04.37\facialRecognition\gil1.jpeg"
p2 = r"C:\Users\lucas\Downloads\WhatsApp Unknown 2025-08-07 at 11.04.37\facialRecognition\gil2.jpeg"

img1 = load_rgb(p1, use_cv2=False)
img2 = load_rgb(p2, use_cv2=False)

# detectar faces (tente model='cnn' se hog falhar e você tiver dlib com suporte)
locs1 = fr.face_locations(img1,model='cnn')  
locs2 = fr.face_locations(img2,model='cnn')

if not locs1:
    print("Nenhuma face detectada em img1 — verifique rotação/recorte/qualidade.")
if not locs2:
    print("Nenhuma face detectada em img2 — verifique rotação/recorte/qualidade.")

# Extrair encodings com segurança
enc1 = fr.face_encodings(img1, known_face_locations=locs1) if locs1 else []
enc2 = fr.face_encodings(img2, known_face_locations=locs2) if locs2 else []

if not enc1 or not enc2:
    print("Não foi possível extrair encoding de uma das imagens. Abortando comparação.")
else:
    e1 = enc1[0]
    e2 = enc2[0]
    matches = fr.compare_faces([e1], e2)
    dist = fr.face_distance([e1], e2)
    print("Matches:", matches, "Distância:", dist)

# desenhar retângulos e exibir (converter para BGR pro cv2.imshow)
def draw_and_show(img, locs, window_name="Image"):
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    for (top,right,bottom,left) in locs:
        cv2.rectangle(img_bgr, (left, top), (right, bottom), (0,255,0), 2)
    cv2.imshow(window_name, img_bgr)

if locs1:
    draw_and_show(img1, locs1, "Img1")
if locs2:
    draw_and_show(img2, locs2, "Img2")

cv2.waitKey(0)
cv2.destroyAllWindows()
