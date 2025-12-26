# Flask API Service Starter

This is a minimal Flask API service starter based on [Google Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service).

## Getting Started

Server should run automatically when starting a workspace. To run manually, run:
```sh
./devserver.sh
```

## Backup and Restore

This project includes scripts to backup and restore your Firestore database. These scripts use the `gcloud` command-line tool.

### Prerequisites

1.  **Install `gcloud`:** Follow the official instructions to [install the Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
2.  **Authenticate:** Log in to your Google Cloud account:
    ```sh
    gcloud auth login
    ```
3.  **Configure Project:** Set your Google Cloud project ID in both `backup.sh` and `restore.sh`:
    ```sh
    PROJECT_ID="your-gcp-project-id"
    ```
4.  **Create a GCS Bucket:** Create a Google Cloud Storage bucket to store your backups. Update the `BUCKET_NAME` in both scripts:
    ```sh
    BUCKET_NAME="your-firestore-backup-bucket"
    ```

### Backing Up Data

To back up your Firestore data, run the following command:

```sh
chmod +x backup.sh
./backup.sh
```

This will start an asynchronous export of your Firestore data to the specified GCS bucket. The backups will be organized by date.

### Restoring Data

To restore your Firestore data from a backup, you need to provide the date of the backup you want to restore. For example, to restore the backup from October 27, 2023, you would run:

```sh
chmod +x restore.sh
./restore.sh 2023-10-27
```

**WARNING:** Restoring from a backup will overwrite all existing data in your Firestore database. This is a destructive action.
