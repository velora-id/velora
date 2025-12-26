#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Your Google Cloud Project ID.
PROJECT_ID="your-gcp-project-id"

# The GCS bucket where your backups are stored.
BUCKET_NAME="your-firestore-backup-bucket"

# The base directory within the bucket where backups are stored.
BACKUP_DIR="firestore-backups"

# --- Main Script ---

# Check for the backup date argument.
if [ -z "$1" ]; then
  echo "Error: No backup date provided."
  echo "Usage: ./restore.sh YYYY-MM-DD" >&2
  exit 1
fi

BACKUP_DATE=$1

# The full path for the backup to restore.
BACKUP_PATH="gs://${BUCKET_NAME}/${BACKUP_DIR}/${BACKUP_DATE}"


echo "Starting Firestore restore for project ${PROJECT_ID} from ${BACKUP_PATH}..."

# Check if gcloud is installed.
if ! [ -x "$(command -v gcloud)" ]; then
  echo 'Error: gcloud is not installed. Please install and configure the Google Cloud SDK.' >&2
  exit 1
fi

# Set the project.
gcloud config set project ${PROJECT_ID}

# IMPORTANT: Importing data will overwrite ALL existing data in your Firestore database.
# This is a destructive action. You should only run this on a clean database or
# if you are certain you want to roll back to a previous state.

read -p "ARE YOU SURE you want to overwrite all data in the Firestore database for project ${PROJECT_ID}? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# Run the import command.
echo "Importing data from ${BACKUP_PATH}"
gcloud firestore import "${BACKUP_PATH}" \
    --async


echo ""
echo "Restore process initiated. To monitor progress, run:"
echo "gcloud firestore operations list --project=${PROJECT_ID}"
echo ""
echo "Restore successfully started for project ${PROJECT_ID}."
