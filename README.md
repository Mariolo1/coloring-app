# Coloring App — Flutter + FastAPI + Stable Diffusion

Aplikacja mobilna do tworzenia kolorowanek z twarzą osoby w formie krasnoludka.

## Co zawiera
- Flutter mobile app
- FastAPI backend
- detekcja twarzy MediaPipe
- generacja obrazu `img2img` przez Diffusers
- fallback bez AI, jeśli model nie jest dostępny
- line-art do kolorowanki
- eksport PDF A4
- gotowe pliki Docker + README

## Ważna uwaga
Ten projekt jest gotowy do uruchomienia, ale jakość efektu końcowego zależy od:
- dostępności GPU,
- pobrania modelu z Hugging Face,
- doboru promptów,
- ewentualnego dalszego dopracowania pipeline'u SDXL + ControlNet.

Domyślnie backend ma dwa tryby:
1. **AI mode** — używa Diffusers i modelu img2img.
2. **Fallback mode** — gdy model nie wczyta się poprawnie, generuje prostszą wersję kolorowanki bez Stable Diffusion.

Dzięki temu projekt można uruchomić od razu, nawet bez GPU.

---

## Struktura

```text
coloring_app/
├── README.md
├── .gitignore
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── start.sh
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── schemas.py
│       ├── storage/
│       │   ├── __init__.py
│       │   └── file_store.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── image_utils.py
│       └── services/
│           ├── __init__.py
│           ├── face_service.py
│           ├── generation_service.py
│           ├── lineart_service.py
│           └── pdf_service.py
└── mobile_app/
    ├── pubspec.yaml
    ├── analysis_options.yaml
    ├── README.md
    └── lib/
        ├── main.dart
        ├── models/
        │   └── generation_result.dart
        ├── services/
        │   ├── api_service.dart
        │   └── image_picker_service.dart
        └── screens/
            ├── home_screen.dart
            ├── preview_screen.dart
            └── result_screen.dart
```

---

## Backend — szybki start

### 1. Python
Polecany Python: **3.10 lub 3.11**

### 2. Instalacja
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Uruchomienie
```bash
./start.sh
```

Backend wystartuje na:
```text
http://0.0.0.0:8000
```

Healthcheck:
```text
GET /health
```

Swagger:
```text
GET /docs
```

### 4. Ustawienia `.env`
Najważniejsze pola:
- `BASE_URL`
- `DEVICE` (`cpu` albo `cuda`)
- `HF_MODEL_ID`
- `ENABLE_AI=true`

Przykład CPU:
```env
DEVICE=cpu
ENABLE_AI=true
```

Przykład GPU:
```env
DEVICE=cuda
ENABLE_AI=true
```

### 5. Modele
Domyślny model w `.env.example` to lekki model img2img, łatwiejszy do uruchomienia niż SDXL.
Jeśli chcesz mocniejszą jakość, podmień `HF_MODEL_ID` na model zgodny z Twoim pipeline'em.

---

## Flutter — szybki start

### 1. Instalacja zależności
```bash
cd mobile_app
flutter pub get
```

### 2. Android emulator
Domyślnie aplikacja używa:
```dart
http://10.0.2.2:8000
```
To jest poprawny adres dla emulatora Androida.

### 3. iPhone / iOS simulator
Dla iPhone'a i iOS simulatora uruchamiaj aplikację z adresem backendu przez `--dart-define`, np.:
```bash
flutter run --dart-define=API_BASE_URL=http://192.168.1.50:8000
```

Dla iOS simulatora możesz też użyć:
```bash
flutter run --dart-define=API_BASE_URL=http://127.0.0.1:8000
```
jeśli backend działa lokalnie na tym samym Macu.

### 4. Uprawnienia iOS
Do projektu dodałem gotowy szablon:
```text
mobile_app/ios_templates/Runner/Info.plist.template
```
Wstaw jego klucze do docelowego `ios/Runner/Info.plist` po wykonaniu `flutter create .` lub po otwarciu projektu w Xcode.

Najważniejsze wpisy:
- `NSCameraUsageDescription`
- `NSPhotoLibraryUsageDescription`
- `NSPhotoLibraryAddUsageDescription`
- `NSAppTransportSecurity` dla lokalnego HTTP w trakcie developmentu

### 5. Uruchomienie
```bash
flutter pub get
flutter run --dart-define=API_BASE_URL=http://192.168.1.50:8000
```

### 6. Budowanie pod iOS
Na Macu wykonaj w katalogu `mobile_app`:
```bash
flutter create .
open ios/Runner.xcworkspace
```
Następnie w Xcode ustaw:
- Team / Signing
- Bundle Identifier
- uprawnienia z `ios_templates/Runner/Info.plist.template`


---

## Docker backend

```bash
cd backend
docker build -t coloring-backend .
docker run --rm -p 8000:8000 --env-file .env coloring-backend
```

---

## Co warto zrobić jako następny krok
- dodać ControlNet,
- dodać kolejkę zadań,
- zapisać historię generacji,
- dodać autoryzację,
- dodać S3/MinIO,
- dopracować prompt engineering i podobieństwo twarzy.


---

## Wersja App Store ready

W katalogu `ios_release/` znajdziesz dodatkowe materiały do publikacji:
- `APP_STORE_CHECKLIST.md`
- `APP_STORE_METADATA_TEMPLATE.md`
- `PRIVACY_POLICY_TEMPLATE.md`
- `EXPORT_COMPLIANCE.md`
- `app_store_assets/README.md`

Dodatkowo w `mobile_app/ios_templates/Runner/` dodałem:
- `Info.plist.release.template`
- `Release.xcconfig.template`

Dla builda App Store pamiętaj, aby używać **HTTPS** i produkcyjnego backendu.
