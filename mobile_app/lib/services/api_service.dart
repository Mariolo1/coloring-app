import 'dart:io';

import 'package:dio/dio.dart';

import '../config/app_config.dart';
import '../models/generation_result.dart';

class ApiService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: AppConfig.resolveBaseUrl(),
      connectTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(minutes: 2),
      receiveTimeout: const Duration(minutes: 5),
    ),
  );

  Future<GenerationResult> generateColoringPage(File imageFile) async {
    final fileName = imageFile.path.split('/').last;

    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(imageFile.path, filename: fileName),
    });

    final response = await _dio.post('/generate', data: formData);
    return GenerationResult.fromJson(response.data as Map<String, dynamic>);
  }

  Future<String> downloadPdf(String url, String savePath) async {
    await _dio.download(url, savePath);
    return savePath;
  }
}
