# App Store ready — checklista publikacyjna

## Krytyczne przed wysłaniem
- Ustaw docelowy `PRODUCT_BUNDLE_IDENTIFIER`.
- Skonfiguruj `Team` i Signing w Xcode.
- Ustaw wersję `1.0.0` i build number.
- Upewnij się, że build release używa **HTTPS**, nie lokalnego HTTP.
- Usuń wszelkie testowe adresy IP z `--dart-define` i konfiguracji release.
- Dodaj działający adres `Privacy Policy URL` i `Support URL` w App Store Connect.
- Sprawdź, że opisy uprawnień w `Info.plist` dokładnie odpowiadają funkcjom aplikacji.
- Zweryfikuj, że backend usuwa zdjęcia i PDF-y zgodnie z polityką prywatności.
- Zweryfikuj, czy nie zapisujesz zdjęć dłużej niż to konieczne.
- Przygotuj konto testowe tylko jeśli aplikacja będzie wymagała logowania. Ten projekt nie wymaga logowania.

## iOS / Xcode
- Otwórz `ios/Runner.xcworkspace`.
- Włącz automatyczne signing albo ustaw profile ręcznie.
- Ustaw minimalną wersję iOS zgodną z używanymi bibliotekami Flutter.
- Upewnij się, że `Release` wskazuje na produkcyjny backend.
- Wygeneruj archiwum w Xcode i przejdź walidację przed uploadem.

## App Store Connect
- Nazwa aplikacji.
- Subtitle.
- Description.
- Keywords.
- Support URL.
- Privacy Policy URL.
- Kategoria.
- Odpowiedzi App Privacy.
- Zrzuty ekranów iPhone.
- Ikona aplikacji.
- Informacja o wykorzystaniu AI w Review Notes, jeśli chcesz zminimalizować pytania recenzenta.

## Review Notes — sugerowany tekst
This app lets a user take or select a photo and send it to our backend to generate a printable black-and-white coloring page in a fantasy dwarf style. No account is required. Photos are processed only after the user taps the generate button.
