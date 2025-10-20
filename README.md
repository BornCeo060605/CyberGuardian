# 🛡️ CyberGuardian

**CyberGuardian** is a serverless safety agent that classifies incoming messages for phishing threats using AWS Lambda and SageMaker, stores results in DynamoDB, and displays them via a real-time dashboard hosted on S3 or Amplify. It is designed for proactive detection, explainable verdicts, and scalable deployment.

---

## 📐 Architecture Overview

![CyberGuardian Architecture](https://github.com/BornCeo060605/CyberGuardian/blob/main/Architecture%20Diagram.png?raw=true)

CyberGuardian integrates multiple AWS services in a modular, event-driven architecture:

- **CyberGuardian Dashboard**  
  Static frontend (`cyberguardian.html`) built with HTML, CSS, and JavaScript. Hosted on Amazon S3 or Amplify. Displays real-time classification logs with verdicts, severity, source, and recommendations.

- **API Gateway**  
  Two documented endpoints:  
  - `POST /analyze` — Accepts message content for classification  
  - `GET /logs` — Returns recent classification results from DynamoDB  
  Defined using OpenAPI specs for reproducibility.

- **Lambda Functions**  
  - `CyberGuardianAgent.py` — Applies phishing detection rules, invokes SageMaker, logs to DynamoDB  
  - `DashboardReader.py` — Reads recent logs for dashboard display

- **AWS SageMaker Endpoint**  
  Analyzes message content and returns severity scores and classification metadata.

- **DynamoDB Logs Table**  
  Stores structured logs including message, verdict, severity, source, recommendation, and timestamp.

---

## 🖥️ Dashboard Functionality

The dashboard provides a clean, tabular view of classified messages:

| Message | Verdict | Severity | Source | Recommendation | Timestamp |
|--------|---------|----------|--------|----------------|-----------|
| Verify your email to continue using the service. | Safe | Medium | Email | Ignore or delete | 2025-10-04T13:48:18 |
| Your bank account is suspended. Click here to unlock. | Likely phishing | High | SMS | Report to authorities | 2025-10-04T13:48:15 |

- ✅ Verdicts are rule-based and ML-enhanced  
- ⚠️ Severity is scored by SageMaker  
- 📤 Source detection helps contextualize threats  
- 🧠 Recommendations guide user action  
- 🕒 Timestamps ensure traceability

---

## 📁 Folder Structure

CyberGuardian/ ├── api-Gateway/ │   ├── CyberGuardianAPI.yaml │   └── CyberGuardianDashboardAPI.yaml ├── dashboard/ │   └── cyberguardian.html ├── dynamodb/ │   └── schema.json ├── lambda/ │   ├── CyberGuardianAgent.py │   └── DashboardReader.py ├── architecture-diagram.png ├── .gitattributes ├── .gitignore ├── README.md └── LICENSE

---

---

## 🚀 Features

- Real-time classification via `POST /analyze`  
- Severity scoring using AWS SageMaker  
- Structured log storage in DynamoDB  
- Dashboard interface for viewing results via `GET /logs`  
- OpenAPI specs for reproducible API setup  
- Modular Lambda functions for classification and log retrieval

---

## 🧪 Setup Instructions

### 1. Deploy Backend

- Upload `CyberGuardianAgent.py` and `DashboardReader.py` as Lambda functions  
- Configure API Gateway using the provided YAML specs  
- Set up DynamoDB table using `schema.json`  
- Deploy SageMaker model and expose it as an endpoint

### 2. Host Frontend

- Upload `cyberguardian.html` to an S3 bucket or Amplify app  
- Ensure CORS settings allow API Gateway access

### 3. Connect Components

- Link API Gateway to Lambda functions  
- Ensure Lambda has permissions to invoke SageMaker and write to DynamoDB  
- Test end-to-end flow using sample messages

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

