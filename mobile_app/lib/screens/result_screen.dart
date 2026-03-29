import 'package:flutter/material.dart';
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';

import '../models/generation_result.dart';
import '../services/api_service.dart';

class ResultScreen extends StatefulWidget {
  final GenerationResult result;

  const ResultScreen({super.key, required this.result});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  final ApiService _apiService = ApiService();
  bool _downloading = false;
  String? _message;

  Future<void> _downloadPdf() async {
    setState(() {
      _downloading = true;
      _message = null;
    });

    try {
      final dir = await getApplicationDocumentsDirectory();
      final filePath = '${dir.path}/${widget.result.jobId}.pdf';
      await _apiService.downloadPdf(widget.result.pdfUrl, filePath);
      await OpenFilex.open(filePath);
      setState(() => _message = 'PDF zapisany i otwarty.');
    } catch (_) {
      setState(() => _message = 'Nie udało się pobrać PDF.');
    } finally {
      if (mounted) {
        setState(() => _downloading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gotowa kolorowanka')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.network(widget.result.previewUrl, fit: BoxFit.contain),
              ),
            ),
            const SizedBox(height: 12),
            Text(
              widget.result.usedAi
                  ? 'Wynik wygenerowany z użyciem modelu AI.'
                  : 'Wynik wygenerowany w trybie uproszczonym fallback.',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            if (_message != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Text(_message!, textAlign: TextAlign.center),
              ),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _downloading ? null : _downloadPdf,
                icon: const Icon(Icons.picture_as_pdf),
                label: Text(_downloading ? 'Pobieranie...' : 'Pobierz PDF'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
