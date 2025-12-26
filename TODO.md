Velora AI Automation Agent — Development Checklist
Platform AI agent & workflow automation berbasis Python + FastAPI + Firebase.
📌 Status Legenda
⬜ Not started
🟨 In progress
✅ Done
🏗️ 1. Project Setup & Bootstrap
⬜ Init GitHub repo
✅ Setup FastAPI project structure
✅ Add Dockerfile & docker-compose
✅ Add .env.example
✅ Health check endpoint /health
⬜ Basic logging & error handler
🔥 2. Firebase Integration
✅ Add Firebase Admin SDK
✅ Init Firebase on startup
✅ Create core/firebase.py
✅ JWT verify dependency
✅ Test Firebase connection
🔐 3. Auth & Security
✅ /auth/register endpoint
✅ /auth/me endpoint
✅ Store user profile in Firestore users/{uid}
✅ RBAC middleware
✅ API key support
✅ Rate limiting
✅ Request logging
🏢 4. Organization & Collaboration
✅ Create organization/workspace
✅ List user organizations
✅ Invite/add members
✅ Roles: owner, admin, editor, viewer
✅ Org access dependency
✅ Firestore schema:
organizations/{orgId}
organizations/{orgId}/members/{uid}
🤖 5. AI Agent Management
✅ CRUD AI agents
✅ Fields: name, type, system_prompt, model, config, status
✅ Assign agent to organization
✅ Prompt & config versioning
✅ Firestore:
organizations/{orgId}/agents/{agentId}
🔄 6. Workflow Automation Engine
✅ CRUD workflows
✅ JSON steps schema
✅ Step types: LLM, API, condition, delay
✅ Triggers: manual, webhook
✅ Run endpoint /workflows/{id}/run
✅ Firestore:
organizations/{orgId}/workflows/{id}
⚙️ 7. Task & Execution Management
✅ Create task on workflow run
🟨 Status: queued, running, success, failed
✅ Step-by-step logs
⬜ Re-run failed tasks
🟨 Async/background runner
✅ Firestore:
organizations/{orgId}/tasks/{taskId}
organizations/{orgId}/tasks/{taskId}/logs/{logId}
🧠 8. LLM Orchestration
✅ Unified LLM client interface
✅ OpenAI provider
✅ Prompt templating
✅ Token & cost tracking
✅ Fallback model support
✅ Firestore:
organizations/{orgId}/llm_usages/{id}
🔌 9. Integrations Hub
✅ CRUD integrations config
✅ SMTP email sender
✅ Webhook sender/receiver
✅ REST API connector
✅ Firestore:
organizations/{orgId}/integrations/{id}
🌍 10. Webhooks & Public API
✅ Incoming webhook triggers
✅ Outgoing webhook actions
✅ API key auth for public endpoints
✅ Signature verification
✅ Public API docs
✅ Firestore:
webhook_triggers/{triggerId}
📊 11. Analytics
✅ Total workflow runs
✅ Success vs failure rate
✅ Token usage per agent/workflow
✅ Time saved estimate
✅ /analytics endpoints
🪵 12. Logs & Audit Trail
✅ User activity logs
✅ Agent execution logs
✅ Store audit logs:
organizations/{orgId}/audit_logs/{id}
✅ Filter & search APIs
✅ Export CSV/JSON
💳 13. Billing & Subscription
✅ Plan management
✅ Subscribe/cancel APIs
✅ Stripe/Midtrans webhook
✅ Quota enforcement middleware
✅ Firestore:
organizations/{orgId}/subscriptions/{id}
🎟️ 14. Credits & Wallet
✅ Credit balance per org
✅ Deduct on LLM usage
✅ Top-up records
✅ Low balance alert
✅ Firestore:
organizations/{orgId}/credits/{id}
🧩 15. Developer Tools
✅ Prompt playground
✅ Agent simulator (dry-run)
✅ Workflow tester
✅ API explorer helpers
✅ /devtools endpoints
🐳 16. DevOps & Environment
✅ Final Dockerfile
✅ docker-compose (api, worker)
✅ Env separation (dev/staging/prod)
✅ Health & readiness probes
⬜ Backup & restore scripts
🧪 17. Testing & Versioning
✅ pytest setup
🟨 API tests for core modules
⬜ Agent versioning
⬜ Workflow versioning
⬜ Rollback feature
⬜ Seed demo data
📄 18. Documentation
⬜ README setup guide
⬜ API usage examples
⬜ Architecture diagram
⬜ Contribution guide
⬜ Changelog
🚀 19. Production Readiness
⬜ Security review
⬜ Performance tuning
⬜ Cost optimization
⬜ Monitoring & alerting
⬜ Deployment to cloud
🗺️ Suggested Milestones
MVP: Sections 1–8
Beta: Sections 9–14
v1.0: Sections 15–19