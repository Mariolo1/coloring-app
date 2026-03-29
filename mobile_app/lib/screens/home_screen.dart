import 'dart:io';

import 'package:flutter/material.dart';

import '../services/image_picker_service.dart';
import 'preview_screen.dart';
import 'privacy_info_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ImagePickerService _pickerService = ImagePickerService();
  bool _loading = false;

  Future<void> _pickCamera() async {
    setState(() => _loading = true);
    final File? file = await _pickerService.pickFromCamera();
    if (!mounted) return;
    setState(() => _loading = false);
    if (file == null) return;

    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => PreviewScreen(imageFile: file)),
    );
  }

  Future<void> _pickGallery() async {
    setState(() => _loading = true);
    final File? file = await _pickerService.pickFromGallery();
    if (!mounted) return;
    setState(() => _loading = false);
    if (file == null) return;

    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => PreviewScreen(imageFile: file)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Kolorowanka krasnoludek')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.auto_awesome,
                size: 72,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 24),
              const Text(
                'Zrób zdjęcie osoby albo wybierz je z galerii. Aplikacja przygotuje kolorowankę krasnoludka do wydruku.',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: _loading ? null : _pickCamera,
                  icon: const Icon(Icons.camera_alt),
                  label: const Text('Zrób zdjęcie'),
                ),
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: _loading ? null : _pickGallery,
                  icon: const Icon(Icons.photo_library),
                  label: const Text('Wybierz z galerii'),
                ),
              ),
              const SizedBox(height: 24),
              TextButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const PrivacyInfoScreen()),
                  );
                },
                child: const Text('Prywatność i bezpieczeństwo'),
              ),
              if (_loading) ...[
                const SizedBox(height: 24),
                const CircularProgressIndicator(),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
