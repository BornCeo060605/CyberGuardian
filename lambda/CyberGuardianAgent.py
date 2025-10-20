import json
import uuid
import boto3
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CyberGuardianLogs')
runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')

# Save item to DynamoDB
def save_to_dynamo(item):
    try:
        table.put_item(Item=item)
        logger.info("✅ Item saved to DynamoDB.")
    except Exception as e:
        logger.error(f"❌ Failed to save to DynamoDB: {str(e)}", exc_info=True)

# Generate metadata and override logic
def generate_metadata(message, label, score):
    message_lower = message.lower()

    # Keyword-based risk detection
    risky_keywords = ["bank account", "update now", "verify", "click here", "urgent", "suspend", "claim prize"]
    keyword_hits = [kw for kw in risky_keywords if kw in message_lower]

    # Severity logic
    severity = "high" if any(kw in message_lower for kw in ["bank account", "update now", "urgent"]) else \
               "medium" if any(kw in message_lower for kw in ["click here", "verify"]) else "low"

    # Source logic
    source = "email" if "verify" in message_lower or "account" in message_lower else "SMS"

    # Recommendation logic
    recommendation = "Report to authorities" if severity == "high" else "Ignore or delete"

    # Override logic
    override = label == "LABEL_1" or len(keyword_hits) >= 2
    final_label = "LABEL_1" if override else label
    final_score = max(score, 0.95) if override else score

    # Verdict formatting
    if override:
        verdict = (
            f"⚠️ Warning: This message is likely a phishing attempt. "
            f"Classified as '{final_label}' with {final_score:.2f} confidence based on risky keywords. "
            f"Please do not click any links and report this message to the appropriate authority."
        )
    else:
        verdict = "✅ This message appears safe."

    # Agent decision explanation
    if keyword_hits:
        agent_decision = (
            f"The message contains keywords like {', '.join(keyword_hits)}, which are commonly used in phishing attempts. "
            f"Based on this, the agent classified it as '{verdict}'."
        )
    else:
        agent_decision = f"The message did not contain known phishing patterns. The agent classified it as '{verdict}'."

    return severity, source, recommendation, verdict, agent_decision

# Main Lambda handler
def lambda_handler(event, context):
    try:
        logger.info(f"📥 Received event: {json.dumps(event)}")

        # Parse input
        if "body" in event and isinstance(event["body"], str):
            body = json.loads(event["body"])
        else:
            body = event

        user_input = body.get("message", "").strip()
        if not user_input:
            raise ValueError("Missing or empty 'message' in request")

        logger.info("📡 Calling SageMaker endpoint...")
        response = runtime.invoke_endpoint(
            EndpointName='CyberGuardianEndpoint',
            ContentType='application/json',
            Body=json.dumps({"inputs": user_input})
        )
        logger.info("✅ SageMaker response received.")

        result = json.loads(response['Body'].read().decode())
        label = result[0].get('label', 'LABEL_0')
        score = float(result[0].get('score', 0.0))

        # Generate metadata and verdict
        severity, source, recommendation, verdict, agent_decision = generate_metadata(user_input, label, score)

        # Create log item
        item = {
            'id': str(uuid.uuid4()),
            'message': user_input,
            'analysis': verdict,
            'severity': severity,
            'source': source,
            'recommendation': recommendation,
            'agent_decision': agent_decision,
            'timestamp': datetime.utcnow().isoformat()
        }

        save_to_dynamo(item)

        return {
            "statusCode": 200,
            "body": json.dumps(item, ensure_ascii=False)
        }

    except Exception as e:
        logger.error(f"❌ Error occurred: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal Server Error",
                "details": str(e)
            }, ensure_ascii=False)
        }