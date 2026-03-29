class GenerationResult {
  final String jobId;
  final String previewUrl;
  final String pdfUrl;
  final bool usedAi;

  GenerationResult({
    required this.jobId,
    required this.previewUrl,
    required this.pdfUrl,
    required this.usedAi,
  });

  factory GenerationResult.fromJson(Map<String, dynamic> json) {
    return GenerationResult(
      jobId: json['job_id'] as String,
      previewUrl: json['preview_url'] as String,
      pdfUrl: json['pdf_url'] as String,
      usedAi: json['used_ai'] as bool? ?? false,
    );
  }
}
