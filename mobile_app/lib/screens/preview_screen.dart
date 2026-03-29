import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

import '../models/generation_result.dart';
import '../services/api_service.dart';
import 'result_screen.dart';

class PreviewScreen extends StatefulWidget {
  final File imageFile;

  const PreviewScreen({super.key, required this.imageFile});

  @override
  State<PreviewScreen> createState() => _PreviewScreenState();
}

class _PreviewScreenState extends State<PreviewScreen> {
  final ApiService _apiService = ApiService();
  bool _submitting = false;
  String? _error;

  Future<void> _generate() async {
    setState(() {
      _submitting = true;
      _error = null;
    });

    try {
      final GenerationResult result = await _apiService.generateColoringPage(widget.imageFile);
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => ResultScreen(result: result)),
      );
    } on DioException catch (e) {
      final dynamic detail = e.response?.data;
      final message = detail is Map<String, dynamic>
          ? (detail['detail']?.toString() ?? 'Błąd generowania')
          : 'Błąd generowania';
      setState(() => _error = message);
    } catch (_) {
      setState(() => _error = 'Nie udało się wygenerować kolorowanki.');
    } finally {
      if (mounted) {
        setState(() => _submitting = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Podgląd zdjęcia')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.file(widget.imageFile, fit: BoxFit.contain),
              ),
            ),
            const SizedBox(height: 16),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Text(
                  _error!,
                  style: const TextStyle(color: Colors.red),
                  textAlign: TextAlign.center,
                ),
              ),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _submitting ? null : _generate,
                child: _submitting
                    ? const Padding(
                        padding: EdgeInsets.all(8),
                        child: SizedBox(
                          width: 24,
                          height: 24,
                          child: CircularProgressIndicator(strokeWidth: 2.5),
                        ),
                      )
                    : const Text('Generuj kolorowankę'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
