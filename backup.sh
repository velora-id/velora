#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Your Google Cloud Project ID.
PROJECT_ID="your-gcp-project-id"

# The GCS bucket where you want to store your backups.
# IMPORTANT: You must create this bucket first.
BUCKET_NAME="your-firestore-backup-bucket"

# The directory within the bucket to store the backups.
BACKUP_DIR="firestore-backups"

# The current date in YYYY-MM-DD format.
TIMESTAMP=$(date +%F)

# The full path for the backup.
BACKUP_PATH="gs://${BUCKET_NAME}/${BACKUP_DIR}/${TIMESTAMP}"

# --- Main Script ---

echo "Starting Firestore backup for project ${PROJECT_ID}..."

# Check if gcloud is installed.
if ! [ -x "$(command -v gcloud)" ]; then
  echo 'Error: gcloud is not installed. Please install and configure the Google Cloud SDK.' >&2
  exit 1
fi

# Authenticate if needed (uncomment the following line or log in manually).
# gcloud auth login

# Set the project.
gcloud config set project ${PROJECT_ID}

# Run the export command.
echo "Exporting data to ${BACKUP_PATH}"
gcloud firestore export "${BACKUP_PATH}" \
    --async

# The --async flag makes the command return immediately.
# You can monitor the progress in the Google Cloud Console.
echo ""
echo "Backup process initiated. To monitor progress, run:"
echo "gcloud firestore operations list --project=${PROJECT_ID}"
echo ""
echo "Backup successfully started for project ${PROJECT_ID}."
