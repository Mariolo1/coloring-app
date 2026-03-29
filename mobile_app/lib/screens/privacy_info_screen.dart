import 'package:flutter/material.dart';

class PrivacyInfoScreen extends StatelessWidget {
  const PrivacyInfoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Prywatność i bezpieczeństwo')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Text(
            'Ta aplikacja używa zdjęcia wyłącznie do wygenerowania kolorowanki i pliku PDF.',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
          SizedBox(height: 12),
          Text(
            'Zakładany model publikacyjny App Store dla tego projektu:'
            '\n\n• zdjęcie jest wysyłane na Twój backend tylko po kliknięciu przycisku generowania'
            '\n• aplikacja nie wymaga logowania'
            '\n• aplikacja nie sprzedaje danych osobowych'
            '\n• zdjęcia i wygenerowane pliki powinny być automatycznie usuwane po określonym czasie po stronie serwera'
            '\n• polityka prywatności powinna być opublikowana publicznie przed wysłaniem aplikacji do App Store',
          ),
          SizedBox(height: 16),
          Text(
            'Przed publikacją sprawdź także:'
            '\n\n• zgodność opisów uprawnień iOS z rzeczywistym działaniem aplikacji'
            '\n• brak testowych adresów URL w buildzie produkcyjnym'
            '\n• działającą stronę wsparcia i polityki prywatności',
          ),
        ],
      ),
    );
  }
}
