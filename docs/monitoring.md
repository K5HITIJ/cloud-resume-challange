# Monitoring & Observability Enhancements

## 1. CloudWatch Dashboards
```yaml
# Add to template-simple.yaml
  ResumeMonitoringDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: CloudResumeChallenge
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "properties": {
                "metrics": [
                  ["AWS/Lambda", "Invocations", "FunctionName", "${VisitorCounterFunction}"],
                  ["AWS/Lambda", "Errors", "FunctionName", "${VisitorCounterFunction}"],
                  ["AWS/Lambda", "Duration", "FunctionName", "${VisitorCounterFunction}"]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "us-east-1",
                "title": "Lambda Metrics"
              }
            }
          ]
        }
```

## 2. Custom Metrics
- Track unique visitors per day
- Monitor API response times
- Track error rates
- Geographic visitor distribution

## 3. Alerting
- SNS notifications for errors
- CloudWatch alarms for high latency
- Email alerts for deployment failures
