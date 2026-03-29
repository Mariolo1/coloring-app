# Mobile App

## Uruchomienie
```bash
flutter pub get
flutter run
```

## Ważne
Backend URL jest ustawiony dla emulatora Androida:
```dart
http://10.0.2.2:8000
```

Dla fizycznego telefonu zmień adres w `lib/services/api_service.dart` na IP Twojego komputera w tej samej sieci.

## Android permissions
Dodaj do `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
```
