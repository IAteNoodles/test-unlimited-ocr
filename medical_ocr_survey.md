# Medical Document OCR Research Survey (2025–2026)

## Scope
Comprehensive survey of medical document OCR research covering approaches, models, benchmarks, and datasets, organized by topic. Focus: single-page medical document OCR (reports + prescriptions).

---

## 1. Medical OCR Benchmarks

### MedRepBench (2025, arXiv)
- **Authors**: Not fully specified in search results
- **Year**: 2025
- **Venue**: arXiv preprint
- **Contribution**: First comprehensive VLM benchmark for medical reports — 1,900 de-identified Chinese medical reports across diverse hospital departments. Introduces dual evaluation: objective (field-level recall) + subjective (LLM-based scoring).
- **Method**: Evaluates both OCR+LLM pipelines and end-to-end VLMs. Includes GRPO (Group Relative Policy Optimization) fine-tuning of a mid-scale VLM.
- **Dataset**: 1,900 de-identified Chinese medical reports; field-level annotations for structured extraction.
- **Results**: GRPO fine-tuning yields ~6% recall improvement. OCR+LLM pipelines suffer from layout-blindness — they extract text but lose spatial/layout context critical for correct field assignment.
- **Capabilities**: Printed Chinese medical reports; structured field extraction; no handwriting or table-specific evaluation.
- **Code**: Not confirmed available.
- **Relevance**: **High** — only comprehensive medical report OCR benchmark found. Directly relevant to single-page medical report extraction. Demonstrates that end-to-end VLMs outperform OCR+LLM pipelines for structured field extraction due to layout awareness.

### GPT-4V OCR Evaluation (2023)
- **Authors**: Not specified
- **Year**: 2023
- **Venue**: Preprint
- **Contribution**: Quantitative evaluation of GPT-4V's OCR capabilities across document types.
- **Method**: Systematic OCR testing on printed text, handwriting, tables, and semantic entity recognition tasks.
- **Results**: GPT-4V struggles with non-Latin scripts, handwriting, table structure preservation, and end-to-end semantic entity recognition. Strong on clean printed Latin text.
- **Capabilities**: Printed (good), handwritten (poor), tables (poor), abbreviations (not tested).
- **Code**: N/A
- **Relevance**: **Medium** — establishes baseline limitations of general-purpose VLMs for OCR, motivating domain-specific fine-tuning.

---

## 2. Handwritten Prescription OCR

### RxVision (2026, ICCIDS)
- **Authors**: Not specified
- **Year**: 2026
- **Venue**: IEEE International Conference on Information and Data Science (ICCIDS)
- **Contribution**: End-to-end pipeline for handwritten prescription digitization into structured EHR records using YOLO detection + OCR recognition + spell correction.
- **Method**: Three-stage pipeline: (1) YOLO object detection to locate drug names, dosages, and patient info on prescription images; (2) OCR engine to recognize text in detected regions; (3) Spell correction / medical dictionary lookup to fix OCR errors and map to standard drug names.
- **Dataset**: Handwritten prescription images (dataset details not fully specified in search results).
- **Results**: mAP@0.5 = 0.93 (detection), Precision = 94.1%, Recall = 91.3%, F1 = 0.92.
- **Capabilities**: Handwritten prescriptions; drug name detection + recognition; dosage extraction; structured EHR output.
- **Code**: Not confirmed available.
- **Relevance**: **High** — directly addresses handwritten prescription OCR with a practical pipeline architecture. The YOLO+OCR+correction pattern is a strong baseline for production systems.

### Multimodal Handwritten Prescription Recognition (2026, QPAIN)
- **Authors**: Not specified
- **Year**: 2026
- **Venue**: QPAIN conference/workshop
- **Contribution**: Novel metadata-augmented CNN approach for handwritten drug name recognition — incorporates drug metadata (category, dosage form, OTC status) as embedding features to improve recognition accuracy.
- **Method**: Compares ResNet50, EfficientNet-B3, VGG16 backbones. Metadata embeddings (drug category, dosage form, OTC/Rx status) concatenated with image features. SHAP for explainability.
- **Dataset**: Doctors Handwritten Prescription BD dataset — 4,680 word images, 78 drug names.
- **Results**: 94.49% accuracy (best model). Metadata augmentation improves accuracy over image-only baselines. SHAP analysis confirms model attends to relevant character regions.
- **Capabilities**: Handwritten drug names (word-level); 78 drug classes; printed metadata not addressed.
- **Code**: Not confirmed available.
- **Relevance**: **High** — demonstrates that domain metadata (drug knowledge) significantly boosts handwritten recognition. The metadata-augmentation idea is transferable to VLM-based approaches via structured prompting.

### End-to-End Pipeline for Handwritten Prescription Understanding (2026)
- **Authors**: Sindhana Devi M, H. K.
- **Year**: 2026
- **Venue**: Shanlax International Journal of Arts, Science and Humanities
- **Contribution**: Complete OCR + clinical NLP pipeline for prescription understanding with explicit error propagation analysis — examines how OCR errors degrade downstream medication extraction.
- **Method**: OCR engine → clinical NLP pipeline for medication entity extraction. Tests on publicly available handwritten text + clinical NLP benchmarks. Analyzes error variability, entity-level extraction performance, and OCR-NLP interaction effects.
- **Dataset**: Publicly available handwritten text datasets + clinical NLP benchmarks (not prescription-specific for privacy reasons).
- **Results**: OCR and NLP perform reasonably independently, but their interaction is the bottleneck for overall system reliability. Joint evaluation is essential.
- **Capabilities**: Handwritten text; medication entity extraction; error propagation modeling.
- **Code**: Not confirmed available.
- **Relevance**: **Medium** — important methodological contribution: OCR error propagation analysis is critical for designing robust prescription OCR systems. Recommends joint OCR+NLP evaluation rather than separate component metrics.

### AI-Based OCR for Handwritten Prescriptions (various)
- **Year**: Various (2023–2025)
- **Contribution**: Multiple systems found using CNN+EMNIST character recognition and Tesseract-based pipelines for handwritten prescription digitization.
- **Method**: Character segmentation → CNN classification (EMNIST-trained) or Tesseract OCR with medical post-processing.
- **Results**: Varies widely; generally lower accuracy than deep learning approaches (60–80% character-level).
- **Relevance**: **Low** — older approaches superseded by YOLO+OCR and VLM methods.

---

## 3. Table Extraction from Medical Documents

### TRH2TQA: Table Recognition with Hierarchical Relationships (2025, WACV Workshop)
- **Authors**: Not specified
- **Year**: 2025
- **Venue**: WACV Workshop
- **Contribution**: Table recognition framework that captures hierarchical relationships between headers and cells, enabling table QA. Outputs HTML structure + header/hierarchy identification.
- **Method**: Two-stage: (1) table structure recognition → HTML representation; (2) header identification and hierarchy relationship extraction. Supports downstream table QA.
- **Dataset**: Table recognition benchmarks (not medical-specific).
- **Results**: SOTA on table structure recognition benchmarks; improved QA accuracy via hierarchy-aware representations.
- **Capabilities**: Printed tables; hierarchical header relationships; HTML output format.
- **Code**: Not confirmed available.
- **Relevance**: **Medium** — medical reports frequently contain lab result tables with hierarchical headers (e.g., "Hematology > WBC > Value/Range"). TRH2TQA's hierarchy-aware approach is directly applicable, though not medical-specific.

### MinerU2.5 (2025)
- **Authors**: Not specified
- **Year**: 2025
- **Venue**: Preprint
- **Contribution**: 1.2B parameter document parsing VLM with two-stage coarse-to-fine architecture — handles layout analysis, text recognition, and table extraction in a single model.
- **Method**: Stage 1: layout analysis on downsampled image (identifies regions: text, table, figure, formula). Stage 2: content recognition on native-resolution crops of each region. This preserves fine-grained detail while maintaining layout understanding.
- **Dataset**: Multiple document parsing benchmarks (OmniDocBench, etc.).
- **Results**: SOTA on multiple document parsing benchmarks. Strong table structure recognition.
- **Capabilities**: Printed text, tables (HTML output), formulas, figures; multi-page; layout-aware.
- **Code**: Likely available (MinerU is an open-source project).
- **Relevance**: **High** — MinerU2.5's coarse-to-fine approach is directly applicable to medical reports with mixed content (text + tables + stamps). The 1.2B parameter size is practical for deployment.

---

## 4. Vision-Language Models for Medical Documents

### MeDocVL (2026, arXiv)
- **Authors**: Not specified
- **Year**: 2026
- **Venue**: arXiv preprint
- **Contribution**: Post-trained VLM specifically for medical document parsing. Introduces Training-driven Label Refinement and Noise-aware Hybrid Post-training (combining RL + SFT).
- **Method**: (1) Training-driven Label Refinement: iteratively improves training labels using model predictions. (2) Noise-aware Hybrid Post-training: alternates RL and SFT phases to handle label noise. Query-driven parsing — user specifies what fields to extract.
- **Dataset**: Medical invoice benchmarks (details not fully specified).
- **Results**: SOTA on medical invoice benchmarks. Outperforms general VLMs and OCR+LLM pipelines.
- **Capabilities**: Printed medical invoices; query-driven field extraction; structured output.
- **Code**: Not confirmed available.
- **Relevance**: **High** — most directly relevant VLM paper for medical document parsing. The query-driven approach and label refinement strategy are directly applicable to single-page medical report extraction.

### VLM Framework with Gemini 2.5 Flash (2025)
- **Authors**: Not specified
- **Year**: 2025
- **Venue**: Preprint
- **Contribution**: Automated medical image analysis + clinical report generation using Gemini 2.5 Flash in zero-shot mode.
- **Method**: Zero-shot prompting of Gemini 2.5 Flash for medical image analysis (CT, MRI, X-ray, Ultrasound) and structured report generation.
- **Dataset**: Medical imaging datasets across modalities.
- **Results**: Strong zero-shot performance on image analysis; report generation quality varies by modality.
- **Capabilities**: Medical images (not documents); report generation; zero-shot.
- **Code**: N/A (API-based).
- **Relevance**: **Low** — focuses on medical imaging (radiology), not document OCR. However, demonstrates VLM capability for structured medical output generation.

---

## 5. Fine-Tuning and RL for Medical OCR

### Efficient Medical VIE via RL (2025, arXiv)
- **Authors**: Not specified
- **Year**: 2025
- **Venue**: arXiv preprint
- **Contribution**: RLVR (Reinforcement Learning with Verifiable Rewards) framework for medical Visual Information Extraction. Fine-tunes Qwen2.5-VL-7B with only 100 annotated samples — extremely data-efficient.
- **Method**: RL fine-tuning with balanced precision-recall reward function. Verifiable rewards: extracted fields are checked against ground truth, reward = f(precision, recall). Only 100 annotated samples needed.
- **Dataset**: Medical VIE benchmark (details not fully specified).
- **Results**: SOTA on medical VIE with only 100 training samples. Performance drops on tasks dissimilar to training data — limited generalization.
- **Capabilities**: Printed medical documents; structured field extraction; query-driven.
- **Code**: Not confirmed available.
- **Relevance**: **Very High** — most practical method paper found. RLVR with 100 samples is feasible for rapid domain adaptation. Qwen2.5-VL-7B is the same base model used in multiple other works. The precision-recall reward design is directly applicable.

### MedRepBench GRPO Fine-Tuning (2025, arXiv)
- **Authors**: Not specified
- **Year**: 2025
- **Venue**: arXiv preprint (part of MedRepBench paper)
- **Contribution**: GRPO (Group Relative Policy Optimization) fine-tuning of mid-scale VLM for medical report extraction.
- **Method**: GRPO — group-relative advantage estimation for policy gradient. Applied to medical report field extraction.
- **Dataset**: MedRepBench (1,900 Chinese medical reports).
- **Results**: ~6% recall improvement over base VLM.
- **Capabilities**: Printed Chinese medical reports; field-level extraction.
- **Code**: Not confirmed available.
- **Relevance**: **High** — demonstrates GRPO effectiveness for medical OCR. Complements the RLVR approach (which uses a different RL formulation). Together, these show RL fine-tuning is a reliable method for boosting VLM performance on medical documents.

---

## 6. EHR OCR and Clinical Document Processing

### RPA for Cancer Registry Data Abstraction (2026, Journal of Clinical Medicine)
- **Authors**: S. Jung, J. Han, Kihyuk Lee, Ho-Young Lee
- **Year**: 2026
- **Venue**: Journal of Clinical Medicine
- **Contribution**: Robotic Process Automation (RPA) for clinical data abstraction from EHR in a production cancer registry. Not OCR per se, but addresses the same workflow: extracting structured data from clinical documents.
- **Method**: RPA bots navigate EHR interfaces to extract structured data for cancer registries (70 gastric cancer variables, 83 breast cancer variables).
- **Results**: 74% time reduction for gastric cancer (19.5→5.1 min/patient), 30% for breast cancer (25.4→17.8 min/patient). ~260 hours saved annually.
- **Relevance**: **Low** — RPA-based, not OCR. But highlights the clinical data abstraction problem and efficiency targets.

### Chinese EMR NER for Rehabilitation Robots (2024, Sensors)
- **Authors**: Jiawei Chu, Xiu Kan, Yan Che, Wanqing Song, A. Kudreyko, Zhengyuan Dong
- **Year**: 2024
- **Venue**: Italian National Conference on Sensors / Sensors journal
- **Contribution**: Medical entity recognition for Chinese electronic medical records using ALBERT + BiLSTM + MHA + CRF architecture.
- **Method**: ALBERT for semantic extraction, BiLSTM + Multi-Head Attention for dependency capture, CRF for entity boundary detection. Preprocessing with clinical knowledge (entity redefinition, outlier removal).
- **Results**: Significant accuracy improvement for Chinese EMR entity recognition.
- **Relevance**: **Low** — NER on text, not OCR. But relevant for the NLP post-processing stage after OCR.

---

## 7. Drug and Prescription Parsing

### MediCaption (2025)
- **Authors**: Not specified
- **Year**: 2025
- **Venue**: Not specified
- **Contribution**: YOLO + NLP pipeline for pharmaceutical package recognition and captioning.
- **Method**: YOLO detects pharmaceutical package elements (drug name, dosage, manufacturer, batch number). NLP pipeline extracts and structures medication information.
- **Results**: Not specified in search results.
- **Capabilities**: Printed pharmaceutical packages; drug name, dosage, manufacturer extraction.
- **Relevance**: **Medium** — addresses medication recognition from printed packaging, complementary to prescription OCR. The YOLO detection approach is similar to RxVision.

### Medication Dosage Extraction (various)
- **Year**: Various
- **Contribution**: Multiple works on medication dosage extraction from clinical text (post-OCR NLP stage).
- **Relevance**: **Medium** — relevant as downstream NLP component after prescription OCR.

---

## 8. Document Layout Analysis

### MinerU2.5 (2025) — see Section 3 for details
- Two-stage coarse-to-fine layout analysis is the most relevant layout analysis method found.
- Stage 1 operates on downsampled images for efficiency; Stage 2 processes native-resolution crops for accuracy.

### General Document Layout Analysis (2025)
- Multiple works on document layout analysis using DETR-based and YOLO-based detectors.
- Medical documents present specific challenges: stamps/seals overlapping text, pre-printed forms with handwritten entries, multi-column lab report layouts.
- **Relevance**: Layout analysis is a critical preprocessing step for OCR+LLM pipelines. VLM-based approaches (MeDocVL, MinerU2.5) integrate layout analysis end-to-end.

---

## 9. Chinese Medical OCR

### MedRepBench (2025) — see Section 1 for details
- Only comprehensive Chinese medical document OCR benchmark found.
- 1,900 de-identified Chinese medical reports.
- Demonstrates VLM superiority over OCR+LLM for Chinese medical reports.

### Multi-Scheme Chinese Medical NER (2024, CCL)
- **Authors**: Wang Shanshan, Zhang Kunyuan, Yan Rong
- **Year**: 2024
- **Venue**: China National Conference on Chinese Computational Linguistics (CCL)
- **Contribution**: Multi-scheme integration for Chinese medical named entity recognition.
- **Relevance**: **Low** — NER on text, not OCR. Relevant for post-OCR processing of Chinese medical documents.

### GPT-4V on Chinese (2023)
- GPT-4V struggles significantly with Chinese OCR, especially handwriting and complex layouts.
- **Relevance**: Motivates domain-specific Chinese medical OCR models.

**Gap**: No dedicated Chinese medical OCR model found. MedRepBench is the primary resource. Chinese handwritten medical document OCR remains largely unaddressed in published research.

---

## 10. Production Medical OCR Systems

### Fullerton Health Claims Document Understanding (2026, arXiv)
- **Authors**: Lilu Cheng, Jing Lu, Yi Chan, Quoc Khai Nguyen, John Bi, Sean Ho
- **Year**: 2026
- **Venue**: arXiv preprint
- **Contribution**: **Production-deployed** multi-stage pipeline for medical claims document processing at Fullerton Health. Handles tens of millions of claims annually across 9 Asian markets (Singapore, Philippines, Indonesia, Malaysia, China, Hong Kong, Vietnam, Papua New Guinea, Cambodia).
- **Method**: Three-stage pipeline: (1) PaddleOCR for multilingual OCR; (2) Logistic Regression classifier for document-type classification; (3) Qwen2.5-VL-7B VLM for field-level extraction. Deployed in mobile application.
- **Dataset**: Production claims data — typed invoices, handwritten medical reports, diverse layouts, 9 languages.
- **Results**: Document-type classification accuracy >95%. Field-level extraction accuracy ~87%. Average processing latency <2 seconds/document. 300x improvement over manual processing (~10 min → ~2 sec). Processing tens of thousands of claims weekly.
- **Capabilities**: Printed + handwritten; multilingual (9 Asian languages); typed invoices + handwritten medical reports; diverse layouts; mobile deployment.
- **Code**: Not open-source (production system).
- **Relevance**: **Very High** — most relevant production system found. Uses the same base VLM (Qwen2.5-VL-7B) as the RLVR and MeDocVL papers. Demonstrates that PaddleOCR + VLM hybrid is the production-ready architecture. The 87% field accuracy and <2s latency are realistic production benchmarks. The hybrid approach (traditional OCR + ML classifier + VLM) balances accuracy, speed, and cost.

---

## Landscape Summary

### Dominant Approaches (2025–2026)

| Approach | Examples | Strengths | Weaknesses |
|---|---|---|---|
| **VLM fine-tuning (RLVR/GRPO)** | Efficient Medical VIE, MedRepBench GRPO, MeDocVL | Best accuracy; layout-aware; query-driven; data-efficient (100 samples) | Requires GPU for inference; limited generalization across task types |
| **YOLO + OCR + post-processing** | RxVision, MediCaption | Fast; modular; good for detection-heavy tasks | Loses layout context; error propagation OCR→NLP |
| **End-to-end VLM document parsing** | MinerU2.5 | Unified; handles mixed content; layout-aware | Larger model; may need fine-tuning for medical domain |
| **Hybrid (OCR + ML + VLM)** | Fullerton Health | Production-proven; balances speed/accuracy; multilingual | Complex pipeline; more components to maintain |
| **Metadata-augmented CNN** | Multimodal Prescription Recognition | Domain knowledge boosts accuracy | Limited to word-level; requires metadata availability |

### Key Base Models
- **Qwen2.5-VL-7B**: Most popular base VLM for medical document OCR (used in Efficient Medical VIE, MeDocVL, Fullerton Health). Good balance of capability and deployability.
- **PaddleOCR**: Production-proven multilingual OCR engine (Fullerton Health).
- **YOLO**: Standard for region detection in prescription OCR (RxVision, MediCaption).
- **MinerU2.5 (1.2B)**: Purpose-built document parsing VLM.

### Key Datasets
| Dataset | Size | Type | Language | Availability |
|---|---|---|---|---|
| MedRepBench | 1,900 reports | Medical reports (printed) | Chinese | Research |
| Doctors Handwritten Prescription BD | 4,680 word images | Handwritten prescriptions | English | Public |
| Fullerton Health production data | Tens of millions | Claims (printed + handwritten) | 9 languages | Private |

### Gaps Identified
1. **No comprehensive English medical report OCR benchmark** — MedRepBench is Chinese-only.
2. **IHU-EPN dataset**: Not found in any academic database. May be private or non-academic.
3. **CNHREC**: Not found. May not exist under this name in published literature.
4. **Chinese handwritten medical OCR**: Largely unaddressed. MedRepBench covers printed reports only.
5. **Prescription OCR standardization**: No standard benchmark; datasets are small (4,680 images) and non-standardized.
6. **Drug abbreviation expansion**: Not directly addressed in any found paper. Would require medical knowledge base integration.

---

## Recommendation for Single-Page Medical Document OCR (Reports + Prescriptions)

### Recommended Architecture: Hybrid VLM Pipeline

Based on the survey, the most practical approach for single-page medical document OCR (reports + prescriptions) is a **hybrid pipeline** combining:

1. **Document type classification** (Logistic Regression or lightweight classifier) → route to report vs. prescription processing
2. **Qwen2.5-VL-7B fine-tuned with RLVR** (100–500 annotated samples) for:
   - Printed medical reports: structured field extraction with layout awareness
   - Handwritten prescriptions: drug name + dosage + frequency extraction
3. **PaddleOCR** as fallback / supplementary OCR for regions where VLM confidence is low
4. **Medical knowledge post-processing**: drug dictionary lookup, abbreviation expansion, dosage validation

### Why This Approach
- **Production-proven**: Fullerton Health deploys this exact architecture (PaddleOCR + Qwen2.5-VL-7B) processing tens of thousands of documents weekly at 87% field accuracy, <2s latency.
- **Data-efficient**: RLVR fine-tuning requires only 100 annotated samples (Efficient Medical VIE).
- **Layout-aware**: VLM handles layout natively, avoiding the layout-blindness problem of OCR+LLM pipelines (MedRepBench finding).
- **Handles both reports and prescriptions**: VLM can be prompted differently for each document type; YOLO detection (RxVision-style) can be added for prescription-specific region detection if needed.
- **Deployable**: Qwen2.5-VL-7B runs on a single GPU; PaddleOCR is lightweight.

### Alternative: MinerU2.5 + Medical Fine-Tuning
If a unified single-model approach is preferred, MinerU2.5 (1.2B parameters) with medical domain fine-tuning is the strongest candidate. Its coarse-to-fine architecture naturally handles mixed-content medical reports (text + tables + stamps). However, it would require more training data than the RLVR approach and hasn't been specifically validated on medical documents.

### Not Recommended
- **OCR + LLM pipeline** (Tesseract/PaddleOCR → GPT/Claude): Suffers from layout-blindness (MedRepBench), error propagation (End-to-End Pipeline paper), and higher latency.
- **Zero-shot VLM** (GPT-4V, Gemini): Struggles with handwriting, tables, and medical abbreviations (GPT-4V eval). Domain fine-tuning is essential.
- **Character-level CNN** (EMNIST-based): Superseded by VLM and YOLO+OCR approaches.