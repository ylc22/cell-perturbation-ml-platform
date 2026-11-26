# Production Reference Architecture

```mermaid
flowchart LR
    RAW[Public / internal assay data] --> S3[S3 raw zone]
    S3 --> ETL[Glue / ECS validation]
    ETL --> CURATED[S3 curated + catalog]
    CURATED --> TRAIN[SageMaker training]
    TRAIN --> REG[Model Registry]
    REG --> SERVE[ECS / SageMaker endpoint]
    SERVE --> API[API Gateway]
    API --> CLIENT[Scientist / application]
    SERVE --> OBS[CloudWatch + OpenTelemetry]
    CURATED --> ATHENA[Athena / warehouse analytics]
```

## Design principles

- immutable raw data and versioned curated datasets
- explicit data, feature, and model versions
- promotion gates based on evaluation, not training success
- perturbation, batch, and cell-type holdouts
- async batch inference for high-throughput workloads
- least-privilege IAM, KMS encryption, private networking
- no raw biological data in application logs
- latency, error, drift, and model-version observability
