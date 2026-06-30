"""
tools_cloud_devops.py
NPM Agent — AI OS by Sonu Kumar (NPMAI ECOSYSTEM)
Cloud & DevOps Tools Vertical
"""

import os
import sys
import json
import re
import subprocess
import tempfile
import time
import threading
import hashlib
import base64
import shutil
import glob
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Any

# ── Auto-installer ────────────────────────────────────────────────────────────
def _ensure(pkg: str, import_name: str = None):
    name = import_name or pkg
    try:
        __import__(name)
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "-q"],
            check=False
        )

_ensure("boto3",       "boto3")
_ensure("requests",    "requests")
_ensure("psutil",      "psutil")
_ensure("gputil",      "GPUtil")
_ensure("watchdog",    "watchdog")
_ensure("kubernetes",  "kubernetes")

# ── Imports from agent_core ───────────────────────────────────────────────────
from core import ToolResult, CredStore


# ══════════════════════════════════════════════════════════════════════════════
# 1. AWSS3Tool
# ══════════════════════════════════════════════════════════════════════════════
class AWSS3Tool:
    name = "aws_s3"
    description = "Complete AWS S3 operations: buckets, objects, presigned URLs, static sites, sync"
    use = (
        """
Name of Tool:- AWSS3Tool,

Purpose of Tool:- 
The AWSS3Tool provides a complete, production-ready interface to Amazon Web Services (AWS) S3 for bucket and object management. 
It supports creating and deleting buckets (with versioning and ACL options), uploading and downloading individual files or entire folders, listing objects, copying objects, generating presigned URLs for secure sharing, setting bucket policies, enabling static website hosting, advanced folder synchronization (with change detection via MD5), retrieving object metadata, listing buckets, and calculating bucket size. 
All operations are performed using the boto3 library with credentials loaded from CredStore. 
This tool is ideal for cloud storage automation, static asset deployment, backups, data pipelines, static website hosting, and agentic cloud infrastructure management.

Methods:-
- _client: Internal helper to initialize authenticated S3 boto3 client.
- create_bucket: Creates a new S3 bucket with optional versioning and ACL.
- delete_bucket: Deletes a bucket (optionally with force to empty it first).
- upload_file: Uploads a single local file to S3.
- upload_folder: Recursively uploads an entire local folder to S3.
- download_file: Downloads a single file from S3 to local path.
- download_folder: Recursively downloads all objects under a prefix to local folder.
- list_objects: Lists objects in a bucket with optional prefix and delimiter.
- delete_object: Deletes a single object from a bucket.
- copy_object: Copies an object between buckets or within the same bucket.
- get_presigned_url: Generates a time-limited presigned URL for downloading an object.
- set_bucket_policy: Applies a JSON bucket policy for access control.
- enable_static_website: Enables static website hosting on a bucket.
- sync_folder: Bidirectional-aware sync from local folder to S3 (with change detection and optional delete).
- get_object_metadata: Retrieves detailed metadata for a specific object.
- list_buckets: Lists all buckets owned by the authenticated user.
- get_bucket_size: Calculates total size and object count of a bucket.

How to use Tool Methods:-

1. _client (Internal Authentication Helper):
   - Purpose: Creates and returns a boto3 S3 client using credentials from CredStore.
   - Arguments:
     a) cred_key: str (default: "aws") - Key to load AWS credentials from CredStore.
   - Credential format expected: {'access_key_id': '...', 'secret_access_key': '...', 'region': 'us-east-1'}.
   - Note: Internal method. Do not call directly.

2. create_bucket:
   - Purpose: Creates a new S3 bucket with optional configuration.
   - Arguments:
     a) name: str - Bucket name (globally unique).
     b) region: str (default: "us-east-1") - AWS region.
     c) versioning: bool (default: False) - Enable object versioning.
     d) acl: str (default: "private") - Bucket ACL ("private", "public-read", etc.).
     e) cred_key: str (default: "aws").
   - How to call: AWSS3Tool.create_bucket(name="my-unique-bucket", region="ap-south-1", versioning=True)

3. delete_bucket:
   - Purpose: Deletes an S3 bucket. Use force=True to empty it first (handles versions and delete markers).
   - Arguments:
     a) name: str - Bucket name.
     b) force: bool (default: False) - Empty bucket before deletion.
     c) cred_key: str (default: "aws").
   - How to call: AWSS3Tool.delete_bucket(name="my-bucket", force=True)

4. upload_file:
   - Purpose: Uploads a single file with optional ACL and metadata.
   - Arguments:
     a) bucket: str - Target bucket name.
     b) local_path: str - Path to local file.
     c) s3_key: str (default: "") - Target key in S3 (defaults to filename).
     d) acl: str (default: "private").
     e) metadata: dict (default: None) - Custom metadata key-value pairs.
     f) cred_key: str (default: "aws").
   - How to call: AWSS3Tool.upload_file(bucket="my-bucket", local_path="report.pdf", s3_key="reports/report.pdf", metadata={"category": "finance"})

5. upload_folder:
   - Purpose: Recursively uploads all files from a local folder, preserving structure.
   - Arguments:
     a) bucket: str
     b) local_folder: str - Local directory path.
     c) prefix: str (default: "") - S3 prefix/folder path.
     d) cred_key: str (default: "aws").
   - How to call: AWSS3Tool.upload_folder(bucket="my-bucket", local_folder="./static", prefix="assets")

6. download_file:
   - Purpose: Downloads a single object from S3.
   - Arguments:
     a) bucket: str
     b) s3_key: str - Object key in S3.
     c) local_path: str - Destination path (creates directories if needed).
     d) cred_key: str (default: "aws").
   - How to call: AWSS3Tool.download_file(bucket="my-bucket", s3_key="data/file.zip", local_path="./downloads/file.zip")

7. download_folder:
   - Purpose: Recursively downloads all objects under a prefix.
   - Arguments:
     a) bucket: str
     b) prefix: str - S3 prefix to download.
     c) local_path: str - Local destination folder.
     d) cred_key: str (default: "aws").
   - How to call: AWSS3Tool.download_folder(bucket="my-bucket", prefix="backups/", local_path="./restored")

8. list_objects:
   - Purpose: Lists objects in a bucket with pagination support.
   - Arguments:
     a) bucket: str
     b) prefix: str (default: "") - Filter by prefix.
     c) delimiter: str (default: "") - For folder-like grouping.
     d) max_keys: int (default: 1000).
     e) cred_key: str (default: "aws").
   - Returns: List of objects with key, size, and last_modified.
   - How to call: AWSS3Tool.list_objects(bucket="my-bucket", prefix="images/", max_keys=500)

9. delete_object:
   - Purpose: Deletes a single object.
   - Arguments: bucket, key, cred_key.
   - How to call: AWSS3Tool.delete_object(bucket="my-bucket", key="oldfile.txt")

10. copy_object:
    - Purpose: Copies an object between buckets or renames within the same bucket.
    - Arguments:
      a) source_bucket: str
      b) source_key: str
      c) dest_bucket: str
      d) dest_key: str
      e) cred_key: str (default: "aws").
    - How to call: AWSS3Tool.copy_object(source_bucket="old-bucket", source_key="file.jpg", dest_bucket="new-bucket", dest_key="images/file.jpg")

11. get_presigned_url:
    - Purpose: Generates a temporary public URL for downloading a private object.
    - Arguments:
      a) bucket: str
      b) key: str
      c) expiry_seconds: int (default: 3600) - URL validity in seconds.
      d) cred_key: str (default: "aws").
    - How to call: AWSS3Tool.get_presigned_url(bucket="my-bucket", key="report.pdf", expiry_seconds=86400)

12. set_bucket_policy:
    - Purpose: Applies a custom JSON bucket policy for fine-grained access control.
    - Arguments:
      a) bucket: str
      b) policy_json: str or dict - Bucket policy JSON.
      c) cred_key: str (default: "aws").
    - How to call: AWSS3Tool.set_bucket_policy(bucket="my-bucket", policy_json=policy_dict)

13. enable_static_website:
    - Purpose: Configures a bucket for static website hosting.
    - Arguments:
      a) bucket: str
      b) index: str (default: "index.html") - Index document.
      c) error: str (default: "error.html") - Error document.
      d) cred_key: str (default: "aws").
    - Returns: Website URL.
    - How to call: AWSS3Tool.enable_static_website(bucket="my-static-site", index="index.html")

14. sync_folder:
    - Purpose: Intelligent synchronization of local folder to S3. Skips unchanged files using MD5 comparison and optionally deletes remote files not present locally.
    - Arguments:
      a) local: str - Local folder path.
      b) bucket: str
      c) prefix: str (default: "") - Target S3 prefix.
      d) delete: bool (default: False) - Delete remote files not in local.
      e) cred_key: str (default: "aws").
    - Returns: Summary of uploaded, skipped, and deleted counts.
    - How to call: AWSS3Tool.sync_folder(local="./website", bucket="my-static-site", prefix="", delete=True)

15. get_object_metadata:
    - Purpose: Gets detailed metadata (size, content type, ETag, last modified, custom metadata) for an object.
    - Arguments: bucket, key, cred_key.
    - How to call: AWSS3Tool.get_object_metadata(bucket="my-bucket", key="file.pdf")

16. list_buckets:
    - Purpose: Lists all S3 buckets owned by the account.
    - Arguments: cred_key.
    - How to call: AWSS3Tool.list_buckets()

17. get_bucket_size:
    - Purpose: Computes total storage size and object count for a bucket.
    - Arguments: bucket, cred_key.
    - Returns: Object count and size in bytes/MB.
    - How to call: AWSS3Tool.get_bucket_size(bucket="my-bucket")
""")
    
    @staticmethod
    def _client(cred_key: str = "aws"):
        import boto3
        c = CredStore.load(cred_key)
        return boto3.client(
            "s3",
            aws_access_key_id=c.get("access_key_id", ""),
            aws_secret_access_key=c.get("secret_access_key", ""),
            region_name=c.get("region", "us-east-1"),
        )

    @staticmethod
    def create_bucket(name: str, region: str = "us-east-1",
                      versioning: bool = False, acl: str = "private",
                      cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            kwargs: dict = {"Bucket": name}
            if region != "us-east-1":
                kwargs["CreateBucketConfiguration"] = {"LocationConstraint": region}
            s3.create_bucket(**kwargs)
            if acl != "private":
                s3.put_bucket_acl(Bucket=name, ACL=acl)
            if versioning:
                s3.put_bucket_versioning(
                    Bucket=name,
                    VersioningConfiguration={"Status": "Enabled"}
                )
            return ToolResult(True, f"✓ Bucket '{name}' created in {region}")
        except Exception as e:
            return ToolResult(False, f"✗ create_bucket failed: {e}")

    @staticmethod
    def delete_bucket(name: str, force: bool = False,
                      cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            if force:
                paginator = s3.get_paginator("list_object_versions")
                for page in paginator.paginate(Bucket=name):
                    versions = page.get("Versions", []) + page.get("DeleteMarkers", [])
                    for v in versions:
                        s3.delete_object(Bucket=name, Key=v["Key"],
                                         VersionId=v["VersionId"])
                paginator2 = s3.get_paginator("list_objects_v2")
                for page in paginator2.paginate(Bucket=name):
                    for obj in page.get("Contents", []):
                        s3.delete_object(Bucket=name, Key=obj["Key"])
            s3.delete_bucket(Bucket=name)
            return ToolResult(True, f"✓ Bucket '{name}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_bucket failed: {e}")

    @staticmethod
    def upload_file(bucket: str, local_path: str, s3_key: str = "",
                    acl: str = "private", metadata: dict = None,
                    cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            key = s3_key or Path(local_path).name
            extra: dict = {"ACL": acl}
            if metadata:
                extra["Metadata"] = {str(k): str(v) for k, v in metadata.items()}
            s3.upload_file(local_path, bucket, key, ExtraArgs=extra)
            return ToolResult(True, f"✓ Uploaded '{local_path}' → s3://{bucket}/{key}")
        except Exception as e:
            return ToolResult(False, f"✗ upload_file failed: {e}")

    @staticmethod
    def upload_folder(bucket: str, local_folder: str, prefix: str = "",
                      cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            base = Path(local_folder)
            count = 0
            for fp in base.rglob("*"):
                if fp.is_file():
                    rel = fp.relative_to(base)
                    key = f"{prefix}/{rel}".lstrip("/") if prefix else str(rel)
                    s3.upload_file(str(fp), bucket, key)
                    count += 1
            return ToolResult(True, f"✓ Uploaded {count} files to s3://{bucket}/{prefix}")
        except Exception as e:
            return ToolResult(False, f"✗ upload_folder failed: {e}")

    @staticmethod
    def download_file(bucket: str, s3_key: str, local_path: str,
                      cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(bucket, s3_key, local_path)
            return ToolResult(True, f"✓ Downloaded s3://{bucket}/{s3_key} → {local_path}")
        except Exception as e:
            return ToolResult(False, f"✗ download_file failed: {e}")

    @staticmethod
    def download_folder(bucket: str, prefix: str, local_path: str,
                        cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            paginator = s3.get_paginator("list_objects_v2")
            count = 0
            for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
                for obj in page.get("Contents", []):
                    key = obj["Key"]
                    rel = key[len(prefix):].lstrip("/")
                    dest = Path(local_path) / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    s3.download_file(bucket, key, str(dest))
                    count += 1
            return ToolResult(True, f"✓ Downloaded {count} files to {local_path}")
        except Exception as e:
            return ToolResult(False, f"✗ download_folder failed: {e}")

    @staticmethod
    def list_objects(bucket: str, prefix: str = "", delimiter: str = "",
                     max_keys: int = 1000, cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            kwargs: dict = {"Bucket": bucket, "MaxKeys": max_keys}
            if prefix:
                kwargs["Prefix"] = prefix
            if delimiter:
                kwargs["Delimiter"] = delimiter
            resp = s3.list_objects_v2(**kwargs)
            objects = [
                {"key": o["Key"], "size": o["Size"],
                 "last_modified": o["LastModified"].isoformat()}
                for o in resp.get("Contents", [])
            ]
            return ToolResult(True, f"✓ {len(objects)} objects in s3://{bucket}", objects)
        except Exception as e:
            return ToolResult(False, f"✗ list_objects failed: {e}")

    @staticmethod
    def delete_object(bucket: str, key: str,
                      cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            s3.delete_object(Bucket=bucket, Key=key)
            return ToolResult(True, f"✓ Deleted s3://{bucket}/{key}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_object failed: {e}")

    @staticmethod
    def copy_object(source_bucket: str, source_key: str,
                    dest_bucket: str, dest_key: str,
                    cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            copy_source = {"Bucket": source_bucket, "Key": source_key}
            s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_key)
            return ToolResult(True, f"✓ Copied s3://{source_bucket}/{source_key} → s3://{dest_bucket}/{dest_key}")
        except Exception as e:
            return ToolResult(False, f"✗ copy_object failed: {e}")

    @staticmethod
    def get_presigned_url(bucket: str, key: str, expiry_seconds: int = 3600,
                          cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expiry_seconds
            )
            return ToolResult(True, f"✓ Presigned URL generated (expires in {expiry_seconds}s)", url)
        except Exception as e:
            return ToolResult(False, f"✗ get_presigned_url failed: {e}")

    @staticmethod
    def set_bucket_policy(bucket: str, policy_json: str,
                          cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            policy = policy_json if isinstance(policy_json, str) else json.dumps(policy_json)
            s3.put_bucket_policy(Bucket=bucket, Policy=policy)
            return ToolResult(True, f"✓ Bucket policy applied to '{bucket}'")
        except Exception as e:
            return ToolResult(False, f"✗ set_bucket_policy failed: {e}")

    @staticmethod
    def enable_static_website(bucket: str, index: str = "index.html",
                               error: str = "error.html",
                               cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            s3.put_bucket_website(
                Bucket=bucket,
                WebsiteConfiguration={
                    "IndexDocument": {"Suffix": index},
                    "ErrorDocument": {"Key": error}
                }
            )
            url = f"http://{bucket}.s3-website.amazonaws.com"
            return ToolResult(True, f"✓ Static website enabled: {url}", {"url": url})
        except Exception as e:
            return ToolResult(False, f"✗ enable_static_website failed: {e}")

    @staticmethod
    def sync_folder(local: str, bucket: str, prefix: str = "",
                    delete: bool = False, cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            base = Path(local)
            uploaded, skipped = 0, 0

            # Build remote index for comparison
            remote_keys: set = set()
            paginator = s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
                for obj in page.get("Contents", []):
                    remote_keys.add(obj["Key"])

            local_keys: set = set()
            for fp in base.rglob("*"):
                if not fp.is_file():
                    continue
                rel = fp.relative_to(base)
                key = f"{prefix}/{rel}".lstrip("/") if prefix else str(rel)
                local_keys.add(key)
                # Check etag vs md5 to skip unchanged files
                md5 = hashlib.md5(fp.read_bytes()).hexdigest()
                try:
                    head = s3.head_object(Bucket=bucket, Key=key)
                    remote_etag = head.get("ETag", "").strip('"')
                    if remote_etag == md5:
                        skipped += 1
                        continue
                except Exception:
                    pass
                s3.upload_file(str(fp), bucket, key)
                uploaded += 1

            deleted = 0
            if delete:
                for key in remote_keys - local_keys:
                    s3.delete_object(Bucket=bucket, Key=key)
                    deleted += 1

            return ToolResult(
                True,
                f"✓ Sync done: {uploaded} uploaded, {skipped} skipped, {deleted} deleted",
                {"uploaded": uploaded, "skipped": skipped, "deleted": deleted}
            )
        except Exception as e:
            return ToolResult(False, f"✗ sync_folder failed: {e}")

    @staticmethod
    def get_object_metadata(bucket: str, key: str,
                             cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            resp = s3.head_object(Bucket=bucket, Key=key)
            meta = {
                "content_type": resp.get("ContentType"),
                "content_length": resp.get("ContentLength"),
                "last_modified": resp.get("LastModified", "").isoformat()
                    if resp.get("LastModified") else None,
                "etag": resp.get("ETag", "").strip('"'),
                "metadata": resp.get("Metadata", {}),
            }
            return ToolResult(True, f"✓ Metadata for s3://{bucket}/{key}", meta)
        except Exception as e:
            return ToolResult(False, f"✗ get_object_metadata failed: {e}")

    @staticmethod
    def list_buckets(cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            resp = s3.list_buckets()
            buckets = [
                {"name": b["Name"],
                 "created": b["CreationDate"].isoformat()}
                for b in resp.get("Buckets", [])
            ]
            return ToolResult(True, f"✓ {len(buckets)} buckets", buckets)
        except Exception as e:
            return ToolResult(False, f"✗ list_buckets failed: {e}")

    @staticmethod
    def get_bucket_size(bucket: str, cred_key: str = "aws") -> ToolResult:
        try:
            s3 = AWSS3Tool._client(cred_key)
            paginator = s3.get_paginator("list_objects_v2")
            total_size = 0
            total_objects = 0
            for page in paginator.paginate(Bucket=bucket):
                for obj in page.get("Contents", []):
                    total_size += obj["Size"]
                    total_objects += 1
            size_mb = round(total_size / (1024 * 1024), 2)
            return ToolResult(
                True,
                f"✓ Bucket '{bucket}': {total_objects} objects, {size_mb} MB",
                {"objects": total_objects, "size_bytes": total_size, "size_mb": size_mb}
            )
        except Exception as e:
            return ToolResult(False, f"✗ get_bucket_size failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 2. AWSLambdaTool
# ══════════════════════════════════════════════════════════════════════════════
class AWSLambdaTool:
    name = "aws_lambda"
    description = "AWS Lambda function management: create, deploy, invoke, logs, triggers"
    use = (
        """
Name of Tool:- AWSLambdaTool,

Purpose of Tool:- 
The AWSLambdaTool provides a complete interface for managing AWS Lambda functions. 
It supports the full lifecycle of serverless functions: creation with code deployment, code and configuration updates, invocation (synchronous and asynchronous), deletion, listing, detailed inspection, layer management, event source triggers (S3 and API Gateway), log retrieval, and version listing. 
All operations use the boto3 Lambda client with AWS credentials loaded from CredStore. 
This tool is designed for serverless application deployment, automation, CI/CD integration, event-driven architectures, and agentic cloud function management on AWS.

Methods:-
- _client: Internal helper to initialize authenticated Lambda boto3 client.
- create_function: Creates a new Lambda function from a deployment package.
- update_function_code: Updates the code of an existing Lambda function.
- update_function_config: Updates configuration settings like environment variables, timeout, and memory.
- invoke_function: Invokes a Lambda function (sync or async) with optional payload.
- delete_function: Deletes a Lambda function.
- list_functions: Lists all Lambda functions with optional name prefix filtering.
- get_function: Retrieves detailed configuration and status of a specific function.
- add_layer: Attaches a Lambda layer to a function.
- create_trigger_s3: Sets up an S3 event trigger for a Lambda function.
- create_trigger_api_gateway: Creates an HTTP API Gateway endpoint that triggers the Lambda.
- get_logs: Retrieves recent CloudWatch logs for a Lambda function.
- list_versions: Lists published versions of a Lambda function.

How to use Tool Methods:-

1. _client (Internal Authentication Helper):
   - Purpose: Creates and returns a boto3 Lambda client using credentials from CredStore.
   - Arguments:
     a) cred_key: str (default: "aws") - Key to load AWS credentials from CredStore.
   - Credential format expected: {'access_key_id': '...', 'secret_access_key': '...', 'region': 'us-east-1'}.
   - Note: This is an internal method used by all other methods. You generally do not call it directly.

2. create_function:
   - Purpose: Creates a new Lambda function by uploading a deployment ZIP package and configuring runtime settings.
   - Arguments:
     a) name: str - Name of the Lambda function (required).
     b) runtime: str - Runtime environment (e.g., "python3.12", "nodejs20.x").
     c) handler: str - Handler identifier (e.g., "lambda_function.lambda_handler").
     d) zip_path: str - Local path to the deployment ZIP file containing code.
     e) role_arn: str - IAM Role ARN with necessary permissions for the Lambda.
     f) env: dict (default: None) - Environment variables for the function.
     g) timeout: int (default: 30) - Maximum execution time in seconds.
     h) memory: int (default: 128) - Memory allocation in MB.
     i) cred_key: str (default: "aws").
   - Returns: Function ARN and initial state.
   - How to call: 
     AWSLambdaTool.create_function(
         name="my-function",
         runtime="python3.12",
         handler="app.lambda_handler",
         zip_path="deployment.zip",
         role_arn="arn:aws:iam::123456789012:role/lambda-role",
         env={"ENV": "production"},
         timeout=60,
         memory=512
     )

3. update_function_code:
   - Purpose: Deploys new code to an existing Lambda function by uploading a fresh ZIP package.
   - Arguments:
     a) name: str - Function name.
     b) zip_path: str - Path to the new deployment ZIP.
     c) cred_key: str (default: "aws").
   - Returns: New version ID.
   - How to call: AWSLambdaTool.update_function_code(name="my-function", zip_path="new_code.zip")

4. update_function_config:
   - Purpose: Modifies runtime configuration without changing the code.
   - Arguments:
     a) name: str
     b) env: dict (default: None) - New environment variables.
     c) timeout: int (default: None)
     d) memory: int (default: None)
     e) cred_key: str (default: "aws").
   - How to call: AWSLambdaTool.update_function_config(name="my-function", env={"DEBUG": "true"}, timeout=120)

5. invoke_function:
   - Purpose: Executes a Lambda function and optionally waits for the response.
   - Arguments:
     a) name: str - Function name.
     b) payload: dict (default: None) - JSON-serializable input data.
     c) async_invoke: bool (default: False) - If True, fires and forgets (Event invocation).
     d) cred_key: str (default: "aws").
   - Returns: Execution result (for sync) or status (for async).
   - How to call: AWSLambdaTool.invoke_function(name="my-function", payload={"key": "value"})

6. delete_function:
   - Purpose: Permanently deletes a Lambda function and all its versions.
   - Arguments: name, cred_key.
   - How to call: AWSLambdaTool.delete_function(name="my-function")

7. list_functions:
   - Purpose: Lists all Lambda functions in the account with basic configuration info.
   - Arguments:
     a) prefix: str (default: "") - Filter functions by name prefix.
     b) cred_key: str (default: "aws").
   - Returns: List of functions with name, runtime, memory, timeout, etc.
   - How to call: AWSLambdaTool.list_functions(prefix="prod-")

8. get_function:
   - Purpose: Retrieves comprehensive information about a specific Lambda function.
   - Arguments: name, cred_key.
   - Returns: ARN, runtime, handler, memory, timeout, state, environment variables, etc.
   - How to call: AWSLambdaTool.get_function(name="my-function")

9. add_layer:
   - Purpose: Attaches an existing Lambda layer (for shared libraries, dependencies, etc.) to a function.
   - Arguments:
     a) name: str - Function name.
     b) layer_arn: str - Full ARN of the layer to attach.
     c) cred_key: str (default: "aws").
   - How to call: AWSLambdaTool.add_layer(name="my-function", layer_arn="arn:aws:lambda:us-east-1:123456789012:layer:my-layer:1")

10. create_trigger_s3:
    - Purpose: Configures an S3 bucket event notification to automatically invoke the Lambda on specified events (e.g., object upload).
    - Arguments:
      a) function: str - Lambda function name.
      b) bucket: str - S3 bucket name.
      c) events: list (default: None) - List of S3 events (e.g., ["s3:ObjectCreated:*"]).
      d) cred_key: str (default: "aws").
    - How to call: AWSLambdaTool.create_trigger_s3(function="my-function", bucket="my-data-bucket", events=["s3:ObjectCreated:Put"])

11. create_trigger_api_gateway:
    - Purpose: Creates a simple HTTP API Gateway that exposes the Lambda function as a public (or protected) REST endpoint.
    - Arguments:
      a) function: str - Lambda function name.
      b) cred_key: str (default: "aws").
    - Returns: API ID and endpoint URL.
    - How to call: AWSLambdaTool.create_trigger_api_gateway(function="my-function")

12. get_logs:
    - Purpose: Fetches the most recent CloudWatch log events for a Lambda function.
    - Arguments:
      a) function: str
      b) start_time: int (default: None) - Unix timestamp in milliseconds.
      c) end_time: int (default: None)
      d) cred_key: str (default: "aws").
    - Returns: List of log events with timestamp and message.
    - How to call: AWSLambdaTool.get_logs(function="my-function")

13. list_versions:
    - Purpose: Lists all published versions of a Lambda function.
    - Arguments: name, cred_key.
    - Returns: List of versions with version number, description, and modification time.
    - How to call: AWSLambdaTool.list_versions(name="my-function")
""")
    
    @staticmethod
    def _client(cred_key: str = "aws"):
        import boto3
        c = CredStore.load(cred_key)
        return boto3.client(
            "lambda",
            aws_access_key_id=c.get("access_key_id", ""),
            aws_secret_access_key=c.get("secret_access_key", ""),
            region_name=c.get("region", "us-east-1"),
        )

    @staticmethod
    def create_function(name: str, runtime: str, handler: str,
                        zip_path: str, role_arn: str,
                        env: dict = None, timeout: int = 30,
                        memory: int = 128,
                        cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            with open(zip_path, "rb") as fh:
                code = fh.read()
            kwargs: dict = {
                "FunctionName": name,
                "Runtime": runtime,
                "Role": role_arn,
                "Handler": handler,
                "Code": {"ZipFile": code},
                "Timeout": timeout,
                "MemorySize": memory,
            }
            if env:
                kwargs["Environment"] = {"Variables": {str(k): str(v) for k, v in env.items()}}
            resp = lm.create_function(**kwargs)
            return ToolResult(True, f"✓ Lambda '{name}' created", {
                "arn": resp.get("FunctionArn"),
                "state": resp.get("State"),
            })
        except Exception as e:
            return ToolResult(False, f"✗ create_function failed: {e}")

    @staticmethod
    def update_function_code(name: str, zip_path: str,
                              cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            with open(zip_path, "rb") as fh:
                code = fh.read()
            resp = lm.update_function_code(FunctionName=name, ZipFile=code)
            return ToolResult(True, f"✓ Lambda '{name}' code updated",
                              {"version": resp.get("Version")})
        except Exception as e:
            return ToolResult(False, f"✗ update_function_code failed: {e}")

    @staticmethod
    def update_function_config(name: str, env: dict = None,
                                timeout: int = None, memory: int = None,
                                cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            kwargs: dict = {"FunctionName": name}
            if env is not None:
                kwargs["Environment"] = {"Variables": {str(k): str(v) for k, v in env.items()}}
            if timeout is not None:
                kwargs["Timeout"] = timeout
            if memory is not None:
                kwargs["MemorySize"] = memory
            lm.update_function_configuration(**kwargs)
            return ToolResult(True, f"✓ Lambda '{name}' config updated")
        except Exception as e:
            return ToolResult(False, f"✗ update_function_config failed: {e}")

    @staticmethod
    def invoke_function(name: str, payload: dict = None,
                        async_invoke: bool = False,
                        cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            invocation_type = "Event" if async_invoke else "RequestResponse"
            resp = lm.invoke(
                FunctionName=name,
                InvocationType=invocation_type,
                Payload=json.dumps(payload or {}).encode()
            )
            if async_invoke:
                return ToolResult(True, f"✓ Lambda '{name}' invoked async",
                                  {"status_code": resp.get("StatusCode")})
            result_payload = resp["Payload"].read().decode()
            try:
                result_data = json.loads(result_payload)
            except Exception:
                result_data = result_payload
            return ToolResult(True, f"✓ Lambda '{name}' invoked", result_data)
        except Exception as e:
            return ToolResult(False, f"✗ invoke_function failed: {e}")

    @staticmethod
    def delete_function(name: str, cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            lm.delete_function(FunctionName=name)
            return ToolResult(True, f"✓ Lambda '{name}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_function failed: {e}")

    @staticmethod
    def list_functions(prefix: str = "", cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            paginator = lm.get_paginator("list_functions")
            funcs = []
            for page in paginator.paginate():
                for fn in page.get("Functions", []):
                    if not prefix or fn["FunctionName"].startswith(prefix):
                        funcs.append({
                            "name": fn["FunctionName"],
                            "runtime": fn.get("Runtime"),
                            "memory": fn.get("MemorySize"),
                            "timeout": fn.get("Timeout"),
                            "last_modified": fn.get("LastModified"),
                        })
            return ToolResult(True, f"✓ {len(funcs)} Lambda functions", funcs)
        except Exception as e:
            return ToolResult(False, f"✗ list_functions failed: {e}")

    @staticmethod
    def get_function(name: str, cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            resp = lm.get_function(FunctionName=name)
            cfg = resp.get("Configuration", {})
            return ToolResult(True, f"✓ Lambda '{name}' info", {
                "arn": cfg.get("FunctionArn"),
                "runtime": cfg.get("Runtime"),
                "handler": cfg.get("Handler"),
                "memory": cfg.get("MemorySize"),
                "timeout": cfg.get("Timeout"),
                "state": cfg.get("State"),
                "last_modified": cfg.get("LastModified"),
                "env": cfg.get("Environment", {}).get("Variables", {}),
            })
        except Exception as e:
            return ToolResult(False, f"✗ get_function failed: {e}")

    @staticmethod
    def add_layer(name: str, layer_arn: str,
                  cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            resp = lm.get_function_configuration(FunctionName=name)
            existing = [l["Arn"] for l in resp.get("Layers", [])]
            if layer_arn not in existing:
                existing.append(layer_arn)
            lm.update_function_configuration(FunctionName=name, Layers=existing)
            return ToolResult(True, f"✓ Layer added to Lambda '{name}'")
        except Exception as e:
            return ToolResult(False, f"✗ add_layer failed: {e}")

    @staticmethod
    def create_trigger_s3(function: str, bucket: str,
                          events: list = None,
                          cred_key: str = "aws") -> ToolResult:
        try:
            import boto3
            c = CredStore.load(cred_key)
            lm = AWSLambdaTool._client(cred_key)
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=c.get("access_key_id", ""),
                aws_secret_access_key=c.get("secret_access_key", ""),
                region_name=c.get("region", "us-east-1"),
            )
            fn_resp = lm.get_function(FunctionName=function)
            fn_arn = fn_resp["Configuration"]["FunctionArn"]
            # Add permission for S3 to invoke Lambda
            try:
                lm.add_permission(
                    FunctionName=function,
                    StatementId=f"s3-trigger-{bucket}-{int(time.time())}",
                    Action="lambda:InvokeFunction",
                    Principal="s3.amazonaws.com",
                    SourceArn=f"arn:aws:s3:::{bucket}",
                )
            except Exception:
                pass  # Permission may already exist
            event_list = events or ["s3:ObjectCreated:*"]
            notification_config = {
                "LambdaFunctionConfigurations": [
                    {"LambdaFunctionArn": fn_arn, "Events": event_list}
                ]
            }
            s3_client.put_bucket_notification_configuration(
                Bucket=bucket,
                NotificationConfiguration=notification_config
            )
            return ToolResult(True, f"✓ S3 trigger created: bucket='{bucket}' → Lambda='{function}'")
        except Exception as e:
            return ToolResult(False, f"✗ create_trigger_s3 failed: {e}")

    @staticmethod
    def create_trigger_api_gateway(function: str,
                                    cred_key: str = "aws") -> ToolResult:
        try:
            import boto3
            c = CredStore.load(cred_key)
            lm = AWSLambdaTool._client(cred_key)
            apigw = boto3.client(
                "apigatewayv2",
                aws_access_key_id=c.get("access_key_id", ""),
                aws_secret_access_key=c.get("secret_access_key", ""),
                region_name=c.get("region", "us-east-1"),
            )
            fn_resp = lm.get_function(FunctionName=function)
            fn_arn = fn_resp["Configuration"]["FunctionArn"]
            region = c.get("region", "us-east-1")
            # Create HTTP API
            api_resp = apigw.create_api(
                Name=f"{function}-api",
                ProtocolType="HTTP",
                Target=fn_arn,
            )
            api_id = api_resp["ApiId"]
            endpoint = api_resp.get("ApiEndpoint", "")
            # Grant API Gateway permission to invoke Lambda
            account_id = boto3.client(
                "sts",
                aws_access_key_id=c.get("access_key_id", ""),
                aws_secret_access_key=c.get("secret_access_key", ""),
                region_name=region,
            ).get_caller_identity().get("Account")
            try:
                lm.add_permission(
                    FunctionName=function,
                    StatementId=f"apigw-{api_id}",
                    Action="lambda:InvokeFunction",
                    Principal="apigateway.amazonaws.com",
                    SourceArn=f"arn:aws:execute-api:{region}:{account_id}:{api_id}/*",
                )
            except Exception:
                pass
            return ToolResult(True, f"✓ API Gateway trigger created for '{function}'",
                              {"api_id": api_id, "endpoint": endpoint})
        except Exception as e:
            return ToolResult(False, f"✗ create_trigger_api_gateway failed: {e}")

    @staticmethod
    def get_logs(function: str, start_time: int = None, end_time: int = None,
                 cred_key: str = "aws") -> ToolResult:
        try:
            import boto3
            c = CredStore.load(cred_key)
            logs = boto3.client(
                "logs",
                aws_access_key_id=c.get("access_key_id", ""),
                aws_secret_access_key=c.get("secret_access_key", ""),
                region_name=c.get("region", "us-east-1"),
            )
            log_group = f"/aws/lambda/{function}"
            # Get latest log stream
            streams_resp = logs.describe_log_streams(
                logGroupName=log_group,
                orderBy="LastEventTime",
                descending=True,
                limit=1
            )
            if not streams_resp.get("logStreams"):
                return ToolResult(True, f"✓ No log streams found for '{function}'", [])
            stream_name = streams_resp["logStreams"][0]["logStreamName"]
            kwargs: dict = {"logGroupName": log_group, "logStreamName": stream_name}
            if start_time:
                kwargs["startTime"] = start_time
            if end_time:
                kwargs["endTime"] = end_time
            events_resp = logs.get_log_events(**kwargs)
            events = [
                {"timestamp": e["timestamp"],
                 "message": e["message"].strip()}
                for e in events_resp.get("events", [])
            ]
            return ToolResult(True, f"✓ {len(events)} log events from '{function}'", events)
        except Exception as e:
            return ToolResult(False, f"✗ get_logs failed: {e}")

    @staticmethod
    def list_versions(name: str, cred_key: str = "aws") -> ToolResult:
        try:
            lm = AWSLambdaTool._client(cred_key)
            paginator = lm.get_paginator("list_versions_by_function")
            versions = []
            for page in paginator.paginate(FunctionName=name):
                for v in page.get("Versions", []):
                    versions.append({
                        "version": v.get("Version"),
                        "description": v.get("Description"),
                        "last_modified": v.get("LastModified"),
                    })
            return ToolResult(True, f"✓ {len(versions)} versions of '{name}'", versions)
        except Exception as e:
            return ToolResult(False, f"✗ list_versions failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 3. AWSECSTool
# ══════════════════════════════════════════════════════════════════════════════
class AWSECSTool:
    name = "aws_ecs"
    description = "ECS/Fargate container orchestration: clusters, tasks, services, logs"
    use = (
        """
Name of Tool:- AWSECSTool,

Purpose of Tool:- 
The AWSECSTool provides a comprehensive interface to Amazon Elastic Container Service (ECS) with Fargate support for container orchestration on AWS. 
It enables full management of ECS clusters, task definitions, individual tasks, long-running services, service updates, task lifecycle control (run/stop/describe), and retrieval of container logs from CloudWatch. 
All operations use the boto3 ECS client (and CloudWatch Logs client where needed) with AWS credentials loaded from CredStore. 
This tool is designed for deploying, scaling, and managing containerized applications, microservices, batch jobs, and serverless container workloads in production environments.

Methods:-
- _client: Internal helper to initialize authenticated ECS boto3 client.
- create_cluster: Creates a new ECS cluster.
- delete_cluster: Deletes an existing ECS cluster.
- register_task_definition: Registers a new task definition for Fargate.
- run_task: Runs one or more standalone tasks on Fargate.
- stop_task: Stops a running task.
- list_tasks: Lists tasks in a cluster, optionally filtered by service and status.
- create_service: Creates a long-running ECS service.
- update_service: Updates an existing service (task definition or desired count).
- delete_service: Deletes an ECS service.
- describe_tasks: Retrieves detailed information about specific tasks.
- get_task_logs: Fetches CloudWatch logs for a specific task and container.

How to use Tool Methods:-

1. _client (Internal Authentication Helper):
   - Purpose: Creates and returns a boto3 ECS client using credentials from CredStore.
   - Arguments:
     a) cred_key: str (default: "aws") - Key to load AWS credentials from CredStore.
   - Credential format expected: {'access_key_id': '...', 'secret_access_key': '...', 'region': 'us-east-1'}.
   - Note: Internal method used by all other methods. You generally do not call it directly.

2. create_cluster:
   - Purpose: Creates a new ECS cluster, optionally with specific capacity providers.
   - Arguments:
     a) name: str - Name of the cluster (required).
     b) capacity_providers: list (default: None) - List of capacity providers (e.g., ["FARGATE", "FARGATE_SPOT"]).
     c) cred_key: str (default: "aws").
   - Returns: Cluster ARN and status.
   - How to call: AWSECSTool.create_cluster(name="production-cluster", capacity_providers=["FARGATE"])

3. delete_cluster:
   - Purpose: Deletes an ECS cluster (cluster must be empty of services and tasks).
   - Arguments:
     a) name: str - Cluster name.
     b) cred_key: str (default: "aws").
   - How to call: AWSECSTool.delete_cluster(name="production-cluster")

4. register_task_definition:
   - Purpose: Registers a new task definition compatible with Fargate, defining container configurations.
   - Arguments:
     a) family: str - Task definition family name.
     b) containers: list - List of container definitions (each containing image, name, portMappings, environment, etc.).
     c) cpu: str (default: "256") - CPU units (e.g., "256", "512", "1024").
     d) memory: str (default: "512") - Memory in MB (e.g., "512", "1024", "2048").
     e) network_mode: str (default: "awsvpc").
     f) cred_key: str (default: "aws").
   - Returns: Task definition ARN and revision number.
   - How to call: AWSECSTool.register_task_definition(family="my-app", containers=[{"name": "web", "image": "nginx:latest", ...}], cpu="512", memory="1024")

5. run_task:
   - Purpose: Launches one or more standalone tasks (suitable for batch jobs or one-off executions) on Fargate.
   - Arguments:
     a) cluster: str - Target ECS cluster name.
     b) task_def: str - Task definition ARN or family:revision.
     c) subnets: list (default: None) - List of VPC subnet IDs.
     d) security_groups: list (default: None) - List of security group IDs.
     e) overrides: dict (default: None) - Task overrides (environment variables, command, etc.).
     f) count: int (default: 1) - Number of tasks to run.
     g) cred_key: str (default: "aws").
   - Returns: Started tasks and any failures.
   - How to call: AWSECSTool.run_task(cluster="production-cluster", task_def="my-app:1", subnets=["subnet-123"], count=2)

6. stop_task:
   - Purpose: Stops a running task with an optional reason.
   - Arguments:
     a) cluster: str
     b) task_id: str - Task ARN or short ID.
     c) reason: str (default: "Stopped by NPM Agent").
     d) cred_key: str (default: "aws").
   - How to call: AWSECSTool.stop_task(cluster="production-cluster", task_id="task-arn", reason="Maintenance")

7. list_tasks:
   - Purpose: Lists tasks in a cluster, optionally filtered by service and desired status.
   - Arguments:
     a) cluster: str
     b) service: str (default: "") - Filter by service name.
     c) status: str (default: "RUNNING") - "RUNNING", "PENDING", "STOPPED", etc.
     d) cred_key: str (default: "aws").
   - Returns: List of task ARNs.
   - How to call: AWSECSTool.list_tasks(cluster="production-cluster", service="web-service", status="RUNNING")

8. create_service:
   - Purpose: Creates a managed, long-running ECS service that maintains the desired number of tasks.
   - Arguments:
     a) cluster: str
     b) name: str - Service name.
     c) task_def: str - Task definition to use.
     d) desired_count: int (default: 1) - Number of tasks to maintain.
     e) lb_config: dict (default: None) - Load balancer configuration for target group registration.
     f) cred_key: str (default: "aws").
   - Returns: Service ARN and status.
   - How to call: AWSECSTool.create_service(cluster="production-cluster", name="web-service", task_def="my-app:1", desired_count=3)

9. update_service:
   - Purpose: Updates an existing service's task definition or desired task count.
   - Arguments:
     a) cluster: str
     b) name: str - Service name.
     c) task_def: str (default: None) - New task definition.
     d) desired_count: int (default: None) - New desired count.
     e) cred_key: str (default: "aws").
   - How to call: AWSECSTool.update_service(cluster="production-cluster", name="web-service", desired_count=5)

10. delete_service:
    - Purpose: Deletes an ECS service (optionally scales it down to zero first).
    - Arguments:
      a) cluster: str
      b) name: str
      c) force: bool (default: False) - Scale to zero before deletion.
      d) cred_key: str (default: "aws").
    - How to call: AWSECSTool.delete_service(cluster="production-cluster", name="web-service", force=True)

11. describe_tasks:
    - Purpose: Gets detailed status and container information for one or more tasks.
    - Arguments:
      a) cluster: str
      b) tasks: list - List of task ARNs or IDs.
      c) cred_key: str (default: "aws").
    - Returns: Rich task details including container statuses and exit codes.
    - How to call: AWSECSTool.describe_tasks(cluster="production-cluster", tasks=["task-arn-1", "task-arn-2"])

12. get_task_logs:
    - Purpose: Retrieves recent CloudWatch Logs for a specific task and container using standard ECS log stream naming.
    - Arguments:
      a) cluster: str
      b) task_id: str - Full task ARN or short ID.
      c) container: str - Container name as defined in task definition.
      d) cred_key: str (default: "aws").
    - Returns: List of log events with timestamp and message.
    - How to call: AWSECSTool.get_task_logs(cluster="production-cluster", task_id="task-arn", container="web")
""")
    
    @staticmethod
    def _client(cred_key: str = "aws"):
        import boto3
        c = CredStore.load(cred_key)
        return boto3.client(
            "ecs",
            aws_access_key_id=c.get("access_key_id", ""),
            aws_secret_access_key=c.get("secret_access_key", ""),
            region_name=c.get("region", "us-east-1"),
        )

    @staticmethod
    def create_cluster(name: str,
                       capacity_providers: list = None,
                       cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            kwargs: dict = {"clusterName": name}
            if capacity_providers:
                kwargs["capacityProviders"] = capacity_providers
            resp = ecs.create_cluster(**kwargs)
            cluster = resp.get("cluster", {})
            return ToolResult(True, f"✓ ECS cluster '{name}' created",
                              {"arn": cluster.get("clusterArn"),
                               "status": cluster.get("status")})
        except Exception as e:
            return ToolResult(False, f"✗ create_cluster failed: {e}")

    @staticmethod
    def delete_cluster(name: str, cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            ecs.delete_cluster(cluster=name)
            return ToolResult(True, f"✓ ECS cluster '{name}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_cluster failed: {e}")

    @staticmethod
    def register_task_definition(family: str, containers: list,
                                  cpu: str = "256", memory: str = "512",
                                  network_mode: str = "awsvpc",
                                  cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            resp = ecs.register_task_definition(
                family=family,
                containerDefinitions=containers,
                cpu=cpu,
                memory=memory,
                networkMode=network_mode,
                requiresCompatibilities=["FARGATE"],
            )
            td = resp.get("taskDefinition", {})
            return ToolResult(True, f"✓ Task definition '{family}' registered",
                              {"arn": td.get("taskDefinitionArn"),
                               "revision": td.get("revision")})
        except Exception as e:
            return ToolResult(False, f"✗ register_task_definition failed: {e}")

    @staticmethod
    def run_task(cluster: str, task_def: str,
                 subnets: list = None, security_groups: list = None,
                 overrides: dict = None, count: int = 1,
                 cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            kwargs: dict = {
                "cluster": cluster,
                "taskDefinition": task_def,
                "count": count,
                "launchType": "FARGATE",
            }
            if subnets or security_groups:
                network_cfg: dict = {"awsvpcConfiguration": {
                    "subnets": subnets or [],
                    "securityGroups": security_groups or [],
                    "assignPublicIp": "ENABLED",
                }}
                kwargs["networkConfiguration"] = network_cfg
            if overrides:
                kwargs["overrides"] = overrides
            resp = ecs.run_task(**kwargs)
            tasks = [{"arn": t.get("taskArn"), "status": t.get("lastStatus")}
                     for t in resp.get("tasks", [])]
            failures = resp.get("failures", [])
            return ToolResult(True, f"✓ {len(tasks)} task(s) started on cluster '{cluster}'",
                              {"tasks": tasks, "failures": failures})
        except Exception as e:
            return ToolResult(False, f"✗ run_task failed: {e}")

    @staticmethod
    def stop_task(cluster: str, task_id: str,
                  reason: str = "Stopped by NPM Agent",
                  cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            ecs.stop_task(cluster=cluster, task=task_id, reason=reason)
            return ToolResult(True, f"✓ Task '{task_id}' stopped on cluster '{cluster}'")
        except Exception as e:
            return ToolResult(False, f"✗ stop_task failed: {e}")

    @staticmethod
    def list_tasks(cluster: str, service: str = "",
                   status: str = "RUNNING",
                   cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            kwargs: dict = {"cluster": cluster, "desiredStatus": status}
            if service:
                kwargs["serviceName"] = service
            resp = ecs.list_tasks(**kwargs)
            task_arns = resp.get("taskArns", [])
            return ToolResult(True, f"✓ {len(task_arns)} tasks in cluster '{cluster}'", task_arns)
        except Exception as e:
            return ToolResult(False, f"✗ list_tasks failed: {e}")

    @staticmethod
    def create_service(cluster: str, name: str, task_def: str,
                       desired_count: int = 1, lb_config: dict = None,
                       cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            kwargs: dict = {
                "cluster": cluster,
                "serviceName": name,
                "taskDefinition": task_def,
                "desiredCount": desired_count,
                "launchType": "FARGATE",
            }
            if lb_config:
                kwargs["loadBalancers"] = [lb_config]
            resp = ecs.create_service(**kwargs)
            svc = resp.get("service", {})
            return ToolResult(True, f"✓ ECS service '{name}' created",
                              {"arn": svc.get("serviceArn"),
                               "status": svc.get("status")})
        except Exception as e:
            return ToolResult(False, f"✗ create_service failed: {e}")

    @staticmethod
    def update_service(cluster: str, name: str,
                       task_def: str = None, desired_count: int = None,
                       cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            kwargs: dict = {"cluster": cluster, "service": name}
            if task_def:
                kwargs["taskDefinition"] = task_def
            if desired_count is not None:
                kwargs["desiredCount"] = desired_count
            ecs.update_service(**kwargs)
            return ToolResult(True, f"✓ ECS service '{name}' updated")
        except Exception as e:
            return ToolResult(False, f"✗ update_service failed: {e}")

    @staticmethod
    def delete_service(cluster: str, name: str, force: bool = False,
                       cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            if force:
                ecs.update_service(cluster=cluster, service=name, desiredCount=0)
            ecs.delete_service(cluster=cluster, service=name, force=force)
            return ToolResult(True, f"✓ ECS service '{name}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_service failed: {e}")

    @staticmethod
    def describe_tasks(cluster: str, tasks: list,
                       cred_key: str = "aws") -> ToolResult:
        try:
            ecs = AWSECSTool._client(cred_key)
            resp = ecs.describe_tasks(cluster=cluster, tasks=tasks)
            result = []
            for t in resp.get("tasks", []):
                result.append({
                    "arn": t.get("taskArn"),
                    "status": t.get("lastStatus"),
                    "desired_status": t.get("desiredStatus"),
                    "started_at": str(t.get("startedAt", "")),
                    "containers": [
                        {"name": c.get("name"), "status": c.get("lastStatus"),
                         "exit_code": c.get("exitCode")}
                        for c in t.get("containers", [])
                    ],
                })
            return ToolResult(True, f"✓ Described {len(result)} tasks", result)
        except Exception as e:
            return ToolResult(False, f"✗ describe_tasks failed: {e}")

    @staticmethod
    def get_task_logs(cluster: str, task_id: str, container: str,
                      cred_key: str = "aws") -> ToolResult:
        try:
            import boto3
            c = CredStore.load(cred_key)
            logs = boto3.client(
                "logs",
                aws_access_key_id=c.get("access_key_id", ""),
                aws_secret_access_key=c.get("secret_access_key", ""),
                region_name=c.get("region", "us-east-1"),
            )
            # Standard ECS log group pattern
            task_short = task_id.split("/")[-1]
            log_group = f"/ecs/{cluster}"
            log_stream = f"ecs/{container}/{task_short}"
            resp = logs.get_log_events(
                logGroupName=log_group,
                logStreamName=log_stream,
            )
            events = [{"timestamp": e["timestamp"], "message": e["message"].strip()}
                      for e in resp.get("events", [])]
            return ToolResult(True, f"✓ {len(events)} log events for task '{task_short}'", events)
        except Exception as e:
            return ToolResult(False, f"✗ get_task_logs failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 4. CloudflareTool
# ══════════════════════════════════════════════════════════════════════════════
class CloudflareTool:
    name = "cloudflare"
    description = "Full Cloudflare management: DNS, cache, Workers, KV, firewall, analytics"
    use = (
        """
Name of Tool:- CloudflareTool,

Purpose of Tool:- 
The CloudflareTool provides a comprehensive interface to the Cloudflare API (v4) for managing DNS records, zones, cache purging, Cloudflare Workers, KV storage, firewall rules, and analytics. 
It supports both API Token and API Key + Email authentication methods via CredStore. 
This tool enables full automation of DNS management, edge caching control, serverless Workers deployment and routing, key-value storage, security rules, and performance analytics. 
It is ideal for domain management, CDN optimization, serverless application deployment, security hardening, and agentic cloud operations on the Cloudflare platform.

Methods:-
- _headers: Internal helper to generate authentication headers.
- _get: Internal helper for GET requests to Cloudflare API.
- _post: Internal helper for POST requests.
- _put: Internal helper for PUT requests.
- _delete: Internal helper for DELETE requests.
- list_zones: Lists all zones (domains) in the account.
- get_zone: Retrieves details for a specific zone by name.
- create_dns_record: Creates a new DNS record (A, CNAME, TXT, etc.).
- update_dns_record: Updates an existing DNS record.
- delete_dns_record: Deletes a DNS record.
- list_dns_records: Lists DNS records with optional filtering.
- purge_cache: Purges CDN cache for specific files or entire zone.
- get_analytics: Retrieves zone analytics and traffic statistics.
- create_worker: Creates or updates a Cloudflare Worker script.
- update_worker: Alias for create_worker (updates existing worker).
- delete_worker: Deletes a Cloudflare Worker.
- list_workers: Lists all Workers in the account.
- set_worker_route: Maps a URL pattern/route to a Worker.
- create_kv_namespace: Creates a new KV (Key-Value) namespace.
- write_kv: Writes or updates a key-value pair in a KV namespace.
- read_kv: Reads the value for a specific key.
- delete_kv: Deletes a key from a KV namespace.
- list_kv: Lists all keys in a KV namespace.
- get_firewall_rules: Retrieves existing firewall rules for a zone.
- create_firewall_rule: Creates a new firewall rule using filter expressions.

How to use Tool Methods:-

1. _headers (Internal Authentication Helper):
   - Purpose: Constructs the correct authentication headers based on credentials stored in CredStore (supports both API Token and legacy API Key + Email).
   - Arguments: cred_key: str (default: "cloudflare")
   - Credential options in CredStore: 
     - Preferred: {"api_token": "your-global-api-token"}
     - Alternative: {"email": "user@example.com", "api_key": "your-api-key", "account_id": "..."}

2. _get / _post / _put / _delete (Internal HTTP Helpers):
   - Purpose: Perform authenticated HTTP requests to Cloudflare API endpoints.
   - These are internal methods used by all public methods. You generally do not call them directly.

3. list_zones:
   - Purpose: Lists all domains/zones associated with the authenticated account.
   - Arguments: cred_key: str (default: "cloudflare")
   - Returns: List of zones with id, name, and status.
   - How to call: CloudflareTool.list_zones()

4. get_zone:
   - Purpose: Retrieves detailed information about a specific zone by domain name.
   - Arguments:
     a) zone_name: str - Domain name (e.g., "example.com")
     b) cred_key: str (default: "cloudflare")
   - Returns: Zone ID, name, status, and name servers.
   - How to call: CloudflareTool.get_zone(zone_name="example.com")

5. create_dns_record:
   - Purpose: Creates a new DNS record in a zone (A, AAAA, CNAME, TXT, MX, etc.).
   - Arguments:
     a) zone: str - Domain name.
     b) type: str - Record type (A, CNAME, TXT, etc.).
     c) name: str - Record name (e.g., "@", "www", "sub").
     d) content: str - Record value (IP, target, text, etc.).
     e) ttl: int (default: 1) - Time to live (1 = automatic).
     f) proxied: bool (default: True) - Enable Cloudflare proxy (orange cloud).
     g) cred_key.
   - How to call: CloudflareTool.create_dns_record(zone="example.com", type="A", name="www", content="192.0.2.1", proxied=True)

6. update_dns_record:
   - Purpose: Updates an existing DNS record.
   - Arguments: zone, record_id, type, name, content, proxied, cred_key.
   - How to call: CloudflareTool.update_dns_record(zone="example.com", record_id="record-id", type="CNAME", name="www", content="target.example.com")

7. delete_dns_record:
   - Purpose: Deletes a specific DNS record.
   - Arguments: zone, record_id, cred_key.
   - How to call: CloudflareTool.delete_dns_record(zone="example.com", record_id="record-id")

8. list_dns_records:
   - Purpose: Lists all DNS records for a zone with optional type and name filters.
   - Arguments:
     a) zone: str
     b) type: str (default: "") - Filter by record type.
     c) name: str (default: "") - Filter by record name.
     d) cred_key.
   - Returns: List of records with id, type, name, content, proxied status.
   - How to call: CloudflareTool.list_dns_records(zone="example.com", type="A")

9. purge_cache:
   - Purpose: Purges Cloudflare CDN cache for specific files or the entire zone.
   - Arguments:
     a) zone: str
     b) files: list (default: None) - List of URLs to purge.
     c) everything: bool (default: False) - Purge entire cache.
     d) cred_key.
   - How to call: CloudflareTool.purge_cache(zone="example.com", everything=True) or with specific files.

10. get_analytics:
    - Purpose: Retrieves traffic analytics and statistics for a zone.
    - Arguments:
      a) zone: str
      b) since: str (default: "-10080") - Minutes ago or timestamp.
      c) until: str (default: "0")
      d) cred_key.
    - How to call: CloudflareTool.get_analytics(zone="example.com")

11. create_worker:
    - Purpose: Creates or updates a Cloudflare Worker script (JavaScript).
    - Arguments:
      a) name: str - Worker name.
      b) script: str - Full JavaScript source code.
      c) cred_key (must contain account_id).
    - How to call: CloudflareTool.create_worker(name="my-worker", script="addEventListener('fetch', ...);")

12. update_worker:
    - Purpose: Updates an existing Worker (alias for create_worker).
    - Same arguments as create_worker.

13. delete_worker:
    - Purpose: Deletes a Cloudflare Worker.
    - Arguments: name, cred_key (requires account_id).
    - How to call: CloudflareTool.delete_worker(name="my-worker")

14. list_workers:
    - Purpose: Lists all Workers in the account.
    - Arguments: cred_key (requires account_id).
    - How to call: CloudflareTool.list_workers()

15. set_worker_route:
    - Purpose: Routes traffic matching a URL pattern to a specific Worker.
    - Arguments:
      a) zone: str
      b) pattern: str - URL pattern (e.g., "example.com/*").
      c) worker: str - Worker name.
      d) cred_key.
    - How to call: CloudflareTool.set_worker_route(zone="example.com", pattern="api.example.com/*", worker="my-api-worker")

16. create_kv_namespace:
    - Purpose: Creates a new Key-Value (KV) storage namespace.
    - Arguments: title: str, cred_key (requires account_id).
    - Returns: Namespace ID.
    - How to call: CloudflareTool.create_kv_namespace(title="my-config-store")

17. write_kv:
    - Purpose: Writes or overwrites a value for a key in a KV namespace.
    - Arguments: namespace_id, key, value (string), cred_key.
    - How to call: CloudflareTool.write_kv(namespace_id="ns-id", key="config", value='{"key": "value"}')

18. read_kv:
    - Purpose: Retrieves the value for a specific key.
    - Arguments: namespace_id, key, cred_key.
    - Returns: The stored value as string.
    - How to call: CloudflareTool.read_kv(namespace_id="ns-id", key="config")

19. delete_kv:
    - Purpose: Deletes a key from a KV namespace.
    - Arguments: namespace_id, key, cred_key.
    - How to call: CloudflareTool.delete_kv(namespace_id="ns-id", key="old-key")

20. list_kv:
    - Purpose: Lists all keys in a KV namespace (up to 100).
    - Arguments: namespace_id, cred_key.
    - How to call: CloudflareTool.list_kv(namespace_id="ns-id")

21. get_firewall_rules:
    - Purpose: Lists existing firewall rules for a zone.
    - Arguments: zone, cred_key.
    - How to call: CloudflareTool.get_firewall_rules(zone="example.com")

22. create_firewall_rule:
    - Purpose: Creates a new firewall rule using WAF filter expressions.
    - Arguments:
      a) zone: str
      b) expression: str - Filter expression (e.g., "(http.request.uri.path eq \"/admin\")").
      c) action: str (default: "block") - block, challenge, allow, etc.
      d) cred_key.
    - How to call: CloudflareTool.create_firewall_rule(zone="example.com", expression="(ip.src eq 1.2.3.4)", action="block")
""")
    
    CF_BASE = "https://api.cloudflare.com/client/v4"

    @staticmethod
    def _headers(cred_key: str = "cloudflare") -> dict:
        import requests  # noqa
        c = CredStore.load(cred_key)
        token = c.get("api_token", "")
        email = c.get("email", "")
        api_key = c.get("api_key", "")
        if token:
            return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        return {"X-Auth-Email": email, "X-Auth-Key": api_key, "Content-Type": "application/json"}

    @staticmethod
    def _get(path: str, cred_key: str = "cloudflare") -> dict:
        import requests
        r = requests.get(f"{CloudflareTool.CF_BASE}{path}",
                         headers=CloudflareTool._headers(cred_key), timeout=15)
        return r.json()

    @staticmethod
    def _post(path: str, data: dict, cred_key: str = "cloudflare") -> dict:
        import requests
        r = requests.post(f"{CloudflareTool.CF_BASE}{path}",
                          headers=CloudflareTool._headers(cred_key),
                          json=data, timeout=15)
        return r.json()

    @staticmethod
    def _put(path: str, data: dict, cred_key: str = "cloudflare") -> dict:
        import requests
        r = requests.put(f"{CloudflareTool.CF_BASE}{path}",
                         headers=CloudflareTool._headers(cred_key),
                         json=data, timeout=15)
        return r.json()

    @staticmethod
    def _delete(path: str, cred_key: str = "cloudflare") -> dict:
        import requests
        r = requests.delete(f"{CloudflareTool.CF_BASE}{path}",
                            headers=CloudflareTool._headers(cred_key), timeout=15)
        return r.json()

    @staticmethod
    def list_zones(cred_key: str = "cloudflare") -> ToolResult:
        try:
            resp = CloudflareTool._get("/zones", cred_key)
            if not resp.get("success"):
                return ToolResult(False, f"✗ Cloudflare error: {resp.get('errors')}")
            zones = [{"id": z["id"], "name": z["name"], "status": z["status"]}
                     for z in resp.get("result", [])]
            return ToolResult(True, f"✓ {len(zones)} zones", zones)
        except Exception as e:
            return ToolResult(False, f"✗ list_zones failed: {e}")

    @staticmethod
    def get_zone(zone_name: str, cred_key: str = "cloudflare") -> ToolResult:
        try:
            resp = CloudflareTool._get(f"/zones?name={zone_name}", cred_key)
            if not resp.get("success") or not resp.get("result"):
                return ToolResult(False, f"✗ Zone '{zone_name}' not found")
            z = resp["result"][0]
            return ToolResult(True, f"✓ Zone '{zone_name}' found",
                              {"id": z["id"], "name": z["name"], "status": z["status"],
                               "name_servers": z.get("name_servers", [])})
        except Exception as e:
            return ToolResult(False, f"✗ get_zone failed: {e}")

    @staticmethod
    def create_dns_record(zone: str, type: str, name: str, content: str,
                          ttl: int = 1, proxied: bool = True,
                          cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            resp = CloudflareTool._post(f"/zones/{zone_id}/dns_records", {
                "type": type, "name": name, "content": content,
                "ttl": ttl, "proxied": proxied,
            }, cred_key)
            if not resp.get("success"):
                return ToolResult(False, f"✗ DNS create failed: {resp.get('errors')}")
            r = resp["result"]
            return ToolResult(True, f"✓ DNS record created: {type} {name} → {content}",
                              {"id": r["id"]})
        except Exception as e:
            return ToolResult(False, f"✗ create_dns_record failed: {e}")

    @staticmethod
    def update_dns_record(zone: str, record_id: str, type: str,
                          name: str, content: str, proxied: bool = True,
                          cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            resp = CloudflareTool._put(
                f"/zones/{zone_id}/dns_records/{record_id}",
                {"type": type, "name": name, "content": content, "proxied": proxied},
                cred_key
            )
            if not resp.get("success"):
                return ToolResult(False, f"✗ DNS update failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ DNS record '{record_id}' updated")
        except Exception as e:
            return ToolResult(False, f"✗ update_dns_record failed: {e}")

    @staticmethod
    def delete_dns_record(zone: str, record_id: str,
                          cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            resp = CloudflareTool._delete(f"/zones/{zone_id}/dns_records/{record_id}", cred_key)
            if not resp.get("success"):
                return ToolResult(False, f"✗ DNS delete failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ DNS record '{record_id}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_dns_record failed: {e}")

    @staticmethod
    def list_dns_records(zone: str, type: str = "",
                         name: str = "",
                         cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            params = ""
            if type:
                params += f"&type={type}"
            if name:
                params += f"&name={name}"
            resp = CloudflareTool._get(f"/zones/{zone_id}/dns_records?per_page=100{params}", cred_key)
            records = [
                {"id": r["id"], "type": r["type"], "name": r["name"],
                 "content": r["content"], "proxied": r.get("proxied", False)}
                for r in resp.get("result", [])
            ]
            return ToolResult(True, f"✓ {len(records)} DNS records", records)
        except Exception as e:
            return ToolResult(False, f"✗ list_dns_records failed: {e}")

    @staticmethod
    def purge_cache(zone: str, files: list = None,
                    everything: bool = False,
                    cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            if everything:
                data: dict = {"purge_everything": True}
            else:
                data = {"files": files or []}
            resp = CloudflareTool._post(f"/zones/{zone_id}/purge_cache", data, cred_key)
            if not resp.get("success"):
                return ToolResult(False, f"✗ Cache purge failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ Cache purged for zone '{zone}'")
        except Exception as e:
            return ToolResult(False, f"✗ purge_cache failed: {e}")

    @staticmethod
    def get_analytics(zone: str, since: str = "-10080",
                      until: str = "0",
                      cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            resp = CloudflareTool._get(
                f"/zones/{zone_id}/analytics/dashboard?since={since}&until={until}&continuous=false",
                cred_key
            )
            if not resp.get("success"):
                return ToolResult(False, f"✗ Analytics failed: {resp.get('errors')}")
            totals = resp.get("result", {}).get("totals", {})
            return ToolResult(True, f"✓ Analytics for zone '{zone}'", totals)
        except Exception as e:
            return ToolResult(False, f"✗ get_analytics failed: {e}")

    @staticmethod
    def create_worker(name: str, script: str,
                      cred_key: str = "cloudflare") -> ToolResult:
        try:
            import requests
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            if not account_id:
                return ToolResult(False, "✗ account_id required in cloudflare credentials")
            headers = CloudflareTool._headers(cred_key)
            headers.pop("Content-Type", None)
            r = requests.put(
                f"{CloudflareTool.CF_BASE}/accounts/{account_id}/workers/scripts/{name}",
                headers=headers,
                data=script.encode(),
                timeout=30,
            )
            resp = r.json()
            if not resp.get("success"):
                return ToolResult(False, f"✗ Worker create failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ Worker '{name}' created/updated")
        except Exception as e:
            return ToolResult(False, f"✗ create_worker failed: {e}")

    @staticmethod
    def update_worker(name: str, script: str,
                      cred_key: str = "cloudflare") -> ToolResult:
        return CloudflareTool.create_worker(name, script, cred_key)

    @staticmethod
    def delete_worker(name: str, cred_key: str = "cloudflare") -> ToolResult:
        try:
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            if not account_id:
                return ToolResult(False, "✗ account_id required")
            resp = CloudflareTool._delete(
                f"/accounts/{account_id}/workers/scripts/{name}", cred_key
            )
            if not resp.get("success"):
                return ToolResult(False, f"✗ Worker delete failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ Worker '{name}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_worker failed: {e}")

    @staticmethod
    def list_workers(cred_key: str = "cloudflare") -> ToolResult:
        try:
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            if not account_id:
                return ToolResult(False, "✗ account_id required")
            resp = CloudflareTool._get(f"/accounts/{account_id}/workers/scripts", cred_key)
            workers = [{"id": w.get("id"), "modified_on": w.get("modified_on")}
                       for w in resp.get("result", [])]
            return ToolResult(True, f"✓ {len(workers)} workers", workers)
        except Exception as e:
            return ToolResult(False, f"✗ list_workers failed: {e}")

    @staticmethod
    def set_worker_route(zone: str, pattern: str, worker: str,
                         cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            resp = CloudflareTool._post(f"/zones/{zone_id}/workers/routes",
                                        {"pattern": pattern, "script": worker}, cred_key)
            if not resp.get("success"):
                return ToolResult(False, f"✗ Route set failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ Worker route '{pattern}' → '{worker}' set")
        except Exception as e:
            return ToolResult(False, f"✗ set_worker_route failed: {e}")

    @staticmethod
    def create_kv_namespace(title: str, cred_key: str = "cloudflare") -> ToolResult:
        try:
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            if not account_id:
                return ToolResult(False, "✗ account_id required")
            resp = CloudflareTool._post(
                f"/accounts/{account_id}/storage/kv/namespaces",
                {"title": title}, cred_key
            )
            if not resp.get("success"):
                return ToolResult(False, f"✗ KV namespace create failed: {resp.get('errors')}")
            r = resp["result"]
            return ToolResult(True, f"✓ KV namespace '{title}' created",
                              {"id": r.get("id")})
        except Exception as e:
            return ToolResult(False, f"✗ create_kv_namespace failed: {e}")

    @staticmethod
    def write_kv(namespace_id: str, key: str, value: str,
                 cred_key: str = "cloudflare") -> ToolResult:
        try:
            import requests
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            headers = CloudflareTool._headers(cred_key)
            r = requests.put(
                f"{CloudflareTool.CF_BASE}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key}",
                headers={k: v for k, v in headers.items() if k != "Content-Type"},
                data=value.encode(), timeout=15,
            )
            resp = r.json()
            if not resp.get("success"):
                return ToolResult(False, f"✗ KV write failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ KV key '{key}' written")
        except Exception as e:
            return ToolResult(False, f"✗ write_kv failed: {e}")

    @staticmethod
    def read_kv(namespace_id: str, key: str,
                cred_key: str = "cloudflare") -> ToolResult:
        try:
            import requests
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            headers = CloudflareTool._headers(cred_key)
            r = requests.get(
                f"{CloudflareTool.CF_BASE}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key}",
                headers=headers, timeout=15,
            )
            if r.status_code == 404:
                return ToolResult(False, f"✗ KV key '{key}' not found")
            return ToolResult(True, f"✓ KV key '{key}' read", r.text)
        except Exception as e:
            return ToolResult(False, f"✗ read_kv failed: {e}")

    @staticmethod
    def delete_kv(namespace_id: str, key: str,
                  cred_key: str = "cloudflare") -> ToolResult:
        try:
            import requests
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            headers = CloudflareTool._headers(cred_key)
            r = requests.delete(
                f"{CloudflareTool.CF_BASE}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key}",
                headers=headers, timeout=15,
            )
            resp = r.json()
            if not resp.get("success"):
                return ToolResult(False, f"✗ KV delete failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ KV key '{key}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_kv failed: {e}")

    @staticmethod
    def list_kv(namespace_id: str, cred_key: str = "cloudflare") -> ToolResult:
        try:
            c = CredStore.load(cred_key)
            account_id = c.get("account_id", "")
            resp = CloudflareTool._get(
                f"/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/keys?limit=100",
                cred_key
            )
            keys = [k.get("name") for k in resp.get("result", [])]
            return ToolResult(True, f"✓ {len(keys)} KV keys", keys)
        except Exception as e:
            return ToolResult(False, f"✗ list_kv failed: {e}")

    @staticmethod
    def get_firewall_rules(zone: str, cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            resp = CloudflareTool._get(f"/zones/{zone_id}/firewall/rules", cred_key)
            rules = [
                {"id": r["id"], "action": r.get("action"),
                 "description": r.get("description"),
                 "expression": r.get("filter", {}).get("expression")}
                for r in resp.get("result", [])
            ]
            return ToolResult(True, f"✓ {len(rules)} firewall rules", rules)
        except Exception as e:
            return ToolResult(False, f"✗ get_firewall_rules failed: {e}")

    @staticmethod
    def create_firewall_rule(zone: str, expression: str,
                             action: str = "block",
                             cred_key: str = "cloudflare") -> ToolResult:
        try:
            zone_resp = CloudflareTool.get_zone(zone, cred_key)
            if not zone_resp.success:
                return zone_resp
            zone_id = zone_resp.data["id"]
            # First create a filter
            filter_resp = CloudflareTool._post(
                f"/zones/{zone_id}/filters",
                [{"expression": expression}], cred_key
            )
            if not filter_resp.get("success"):
                return ToolResult(False, f"✗ Filter create failed: {filter_resp.get('errors')}")
            filter_id = filter_resp["result"][0]["id"]
            # Then create the rule
            rule_resp = CloudflareTool._post(
                f"/zones/{zone_id}/firewall/rules",
                [{"filter": {"id": filter_id}, "action": action}], cred_key
            )
            if not rule_resp.get("success"):
                return ToolResult(False, f"✗ Firewall rule create failed: {rule_resp.get('errors')}")
            r = rule_resp["result"][0]
            return ToolResult(True, f"✓ Firewall rule created: {action} where {expression}",
                              {"id": r.get("id")})
        except Exception as e:
            return ToolResult(False, f"✗ create_firewall_rule failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 5. VercelTool
# ══════════════════════════════════════════════════════════════════════════════
class VercelTool:
    name = "vercel"
    description = "Vercel deployment: deploy projects, manage domains, env vars, rollback"
    use = (
        """
Name of Tool:- VercelTool,

Purpose of Tool:- 
The VercelTool provides a full-featured interface to the Vercel platform for deploying frontend and serverless applications, managing projects, deployments, domains, environment variables, and rollbacks. 
It supports both CLI-based deployment (for local project directories with full build context) and direct REST API calls for project management, listing deployments, logs, domain configuration, and environment variables. 
Authentication is done via a Vercel API token stored in CredStore. 
This tool is ideal for automated CI/CD pipelines, preview deployments, production releases, domain management, and agentic frontend/serverless deployment workflows.

Methods:-
- _headers: Internal helper to generate authentication headers.
- _get: Internal helper for GET requests to Vercel API.
- _post: Internal helper for POST requests.
- _delete: Internal helper for DELETE requests.
- deploy: Deploys a local project using the Vercel CLI.
- list_deployments: Lists recent deployments.
- get_deployment: Retrieves details of a specific deployment.
- delete_deployment: Deletes a specific deployment.
- list_projects: Lists all projects in the account.
- create_project: Creates a new project.
- delete_project: Deletes a project.
- set_env_var: Sets or updates an environment variable.
- list_env_vars: Lists environment variables for a project.
- get_deployment_logs: Retrieves build and runtime logs for a deployment.
- rollback: Rolls back a project to a previous deployment.
- add_domain: Adds a custom domain to a project.
- list_domains: Lists domains associated with a project.

How to use Tool Methods:-

1. _headers (Internal Authentication Helper):
   - Purpose: Constructs the Bearer token authorization header required by Vercel API.
   - Arguments: cred_key: str (default: "vercel")
   - Credential requirement: CredStore must contain {'token': 'your-vercel-api-token'}.
   - Note: Internal method. Do not call directly.

2. _get / _post / _delete (Internal HTTP Helpers):
   - Purpose: Perform authenticated HTTP requests to the Vercel REST API.
   - These are internal methods used by most API-based operations. You generally do not call them directly.

3. deploy:
   - Purpose: Deploys a local project directory using the official Vercel CLI. This is the most complete method as it handles build, environment, and full Vercel features.
   - Arguments:
     a) project_path: str - Local directory path containing the project (must have vercel.json or supported framework files).
     b) project_name: str (default: "") - Custom project name.
     c) env: dict (default: None) - Environment variables to inject during deployment.
     d) prod: bool (default: False) - Deploy directly to production (instead of preview).
     e) cred_key: str (default: "vercel").
   - Returns: Deployment URL and full CLI output.
   - How to call: 
     VercelTool.deploy(
         project_path="./my-nextjs-app",
         project_name="my-awesome-site",
         env={"API_KEY": "secret123", "NODE_ENV": "production"},
         prod=True
     )

4. list_deployments:
   - Purpose: Lists recent deployments (up to 20) for the account or a specific project.
   - Arguments:
     a) project: str (default: "") - Project ID to filter by.
     b) cred_key: str (default: "vercel").
   - Returns: List of deployments with uid, url, state, created time, etc.
   - How to call: VercelTool.list_deployments(project="prj_abc123")

5. get_deployment:
   - Purpose: Gets detailed information about a specific deployment.
   - Arguments:
     a) deployment_id: str - Deployment UID.
     b) cred_key: str (default: "vercel").
   - Returns: Deployment metadata including URL, state, timestamps.
   - How to call: VercelTool.get_deployment(deployment_id="dpl_abc123")

6. delete_deployment:
   - Purpose: Permanently deletes a deployment.
   - Arguments: deployment_id, cred_key.
   - How to call: VercelTool.delete_deployment(deployment_id="dpl_abc123")

7. list_projects:
   - Purpose: Lists all projects in the Vercel account.
   - Arguments: cred_key.
   - Returns: List of projects with id, name, framework, updated time.
   - How to call: VercelTool.list_projects()

8. create_project:
   - Purpose: Creates a new Vercel project (optionally linked to a Git repository).
   - Arguments:
     a) name: str - Project name.
     b) git_repo: str (default: "") - GitHub repository in "owner/repo" format.
     c) framework: str (default: "") - Framework preset (e.g., "nextjs", "vite").
     d) cred_key.
   - Returns: Project ID and name.
   - How to call: VercelTool.create_project(name="my-new-app", git_repo="username/my-repo", framework="nextjs")

9. delete_project:
   - Purpose: Deletes a project and all its deployments.
   - Arguments: project_id, cred_key.
   - How to call: VercelTool.delete_project(project_id="prj_abc123")

10. set_env_var:
    - Purpose: Creates or updates an environment variable for a project across specified environments.
    - Arguments:
      a) project_id: str
      b) key: str - Variable name.
      c) value: str - Variable value.
      d) targets: list (default: ["production", "preview", "development"]).
      e) cred_key.
    - How to call: VercelTool.set_env_var(project_id="prj_abc123", key="API_URL", value="https://api.example.com", targets=["production"])

11. list_env_vars:
    - Purpose: Lists all environment variables configured for a project.
    - Arguments: project_id, cred_key.
    - Returns: List of env vars with id, key, and target environments.
    - How to call: VercelTool.list_env_vars(project_id="prj_abc123")

12. get_deployment_logs:
    - Purpose: Retrieves build and runtime logs for a specific deployment.
    - Arguments: deployment_id, cred_key.
    - Returns: List of log events.
    - How to call: VercelTool.get_deployment_logs(deployment_id="dpl_abc123")

13. rollback:
    - Purpose: Rolls back a project to a previous successful deployment.
    - Arguments:
      a) project_id: str
      b) deployment_id: str - Target deployment to roll back to.
      c) cred_key.
    - How to call: VercelTool.rollback(project_id="prj_abc123", deployment_id="dpl_old123")

14. add_domain:
    - Purpose: Adds a custom domain to a Vercel project.
    - Arguments:
      a) project_id: str
      b) domain: str - Full domain name (e.g., "app.example.com").
      c) cred_key.
    - How to call: VercelTool.add_domain(project_id="prj_abc123", domain="app.example.com")

15. list_domains:
    - Purpose: Lists all custom domains associated with a project.
    - Arguments: project_id, cred_key.
    - Returns: List of domains with verification status.
    - How to call: VercelTool.list_domains(project_id="prj_abc123")
""")
    
    VERCEL_API = "https://api.vercel.com"

    @staticmethod
    def _headers(cred_key: str = "vercel") -> dict:
        token = CredStore.load(cred_key).get("token", "")
        if not token:
            raise ValueError("No Vercel token in credentials")
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    @staticmethod
    def _get(path: str, cred_key: str = "vercel") -> dict:
        import requests
        r = requests.get(f"{VercelTool.VERCEL_API}{path}",
                         headers=VercelTool._headers(cred_key), timeout=30)
        return r.json()

    @staticmethod
    def _post(path: str, data: dict, cred_key: str = "vercel") -> dict:
        import requests
        r = requests.post(f"{VercelTool.VERCEL_API}{path}",
                          headers=VercelTool._headers(cred_key),
                          json=data, timeout=30)
        return r.json()

    @staticmethod
    def _delete(path: str, cred_key: str = "vercel") -> dict:
        import requests
        r = requests.delete(f"{VercelTool.VERCEL_API}{path}",
                            headers=VercelTool._headers(cred_key), timeout=30)
        if r.status_code == 204:
            return {"success": True}
        return r.json()

    @staticmethod
    def deploy(project_path: str, project_name: str = "",
               env: dict = None, prod: bool = False,
               cred_key: str = "vercel") -> ToolResult:
        try:
            cmd = ["vercel", "--yes", "--no-clipboard"]
            if project_name:
                cmd += ["--name", project_name]
            if prod:
                cmd.append("--prod")
            if env:
                for k, v in env.items():
                    cmd += ["--env", f"{k}={v}"]
            token = CredStore.load(cred_key).get("token", "")
            if token:
                cmd += ["--token", token]
            result = subprocess.run(
                cmd, cwd=project_path,
                capture_output=True, text=True, timeout=300
            )
            output = result.stdout + result.stderr
            success = result.returncode == 0
            # Extract deployment URL from output
            url_match = re.search(r"https://[^\s]+\.vercel\.app", output)
            url = url_match.group(0) if url_match else ""
            return ToolResult(success,
                              f"✓ Deployed to {url}" if success else f"✗ Deploy failed: {output}",
                              {"url": url, "output": output})
        except Exception as e:
            return ToolResult(False, f"✗ deploy failed: {e}")

    @staticmethod
    def list_deployments(project: str = "",
                         cred_key: str = "vercel") -> ToolResult:
        try:
            path = f"/v6/deployments"
            if project:
                path += f"?projectId={project}&limit=20"
            resp = VercelTool._get(path, cred_key)
            deployments = [
                {"uid": d.get("uid"), "url": d.get("url"),
                 "state": d.get("state"), "created": d.get("created"),
                 "name": d.get("name")}
                for d in resp.get("deployments", [])
            ]
            return ToolResult(True, f"✓ {len(deployments)} deployments", deployments)
        except Exception as e:
            return ToolResult(False, f"✗ list_deployments failed: {e}")

    @staticmethod
    def get_deployment(deployment_id: str,
                       cred_key: str = "vercel") -> ToolResult:
        try:
            resp = VercelTool._get(f"/v13/deployments/{deployment_id}", cred_key)
            return ToolResult(True, f"✓ Deployment '{deployment_id}'", {
                "uid": resp.get("uid"),
                "url": resp.get("url"),
                "state": resp.get("state"),
                "created": resp.get("createdAt"),
                "ready": resp.get("readyAt"),
            })
        except Exception as e:
            return ToolResult(False, f"✗ get_deployment failed: {e}")

    @staticmethod
    def delete_deployment(deployment_id: str,
                          cred_key: str = "vercel") -> ToolResult:
        try:
            VercelTool._delete(f"/v13/deployments/{deployment_id}", cred_key)
            return ToolResult(True, f"✓ Deployment '{deployment_id}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_deployment failed: {e}")

    @staticmethod
    def list_projects(cred_key: str = "vercel") -> ToolResult:
        try:
            resp = VercelTool._get("/v9/projects?limit=50", cred_key)
            projects = [
                {"id": p.get("id"), "name": p.get("name"),
                 "framework": p.get("framework"),
                 "updated": p.get("updatedAt")}
                for p in resp.get("projects", [])
            ]
            return ToolResult(True, f"✓ {len(projects)} projects", projects)
        except Exception as e:
            return ToolResult(False, f"✗ list_projects failed: {e}")

    @staticmethod
    def create_project(name: str, git_repo: str = "",
                       framework: str = "",
                       cred_key: str = "vercel") -> ToolResult:
        try:
            data: dict = {"name": name}
            if framework:
                data["framework"] = framework
            if git_repo:
                data["gitRepository"] = {"repo": git_repo, "type": "github"}
            resp = VercelTool._post("/v10/projects", data, cred_key)
            if "error" in resp:
                return ToolResult(False, f"✗ Project create failed: {resp['error']}")
            return ToolResult(True, f"✓ Vercel project '{name}' created",
                              {"id": resp.get("id"), "name": resp.get("name")})
        except Exception as e:
            return ToolResult(False, f"✗ create_project failed: {e}")

    @staticmethod
    def delete_project(project_id: str, cred_key: str = "vercel") -> ToolResult:
        try:
            VercelTool._delete(f"/v9/projects/{project_id}", cred_key)
            return ToolResult(True, f"✓ Project '{project_id}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_project failed: {e}")

    @staticmethod
    def set_env_var(project_id: str, key: str, value: str,
                    targets: list = None,
                    cred_key: str = "vercel") -> ToolResult:
        try:
            data = {
                "key": key,
                "value": value,
                "type": "plain",
                "target": targets or ["production", "preview", "development"],
            }
            resp = VercelTool._post(f"/v10/projects/{project_id}/env", data, cred_key)
            if "error" in resp:
                return ToolResult(False, f"✗ Env var set failed: {resp['error']}")
            return ToolResult(True, f"✓ Env var '{key}' set on project '{project_id}'")
        except Exception as e:
            return ToolResult(False, f"✗ set_env_var failed: {e}")

    @staticmethod
    def list_env_vars(project_id: str, cred_key: str = "vercel") -> ToolResult:
        try:
            resp = VercelTool._get(f"/v9/projects/{project_id}/env", cred_key)
            envs = [{"id": e.get("id"), "key": e.get("key"),
                     "target": e.get("target")}
                    for e in resp.get("envs", [])]
            return ToolResult(True, f"✓ {len(envs)} env vars", envs)
        except Exception as e:
            return ToolResult(False, f"✗ list_env_vars failed: {e}")

    @staticmethod
    def get_deployment_logs(deployment_id: str,
                             cred_key: str = "vercel") -> ToolResult:
        try:
            resp = VercelTool._get(f"/v2/deployments/{deployment_id}/events", cred_key)
            logs = [{"type": e.get("type"), "text": e.get("payload", {}).get("text", ""),
                     "date": e.get("date")}
                    for e in (resp if isinstance(resp, list) else [])]
            return ToolResult(True, f"✓ {len(logs)} log events", logs)
        except Exception as e:
            return ToolResult(False, f"✗ get_deployment_logs failed: {e}")

    @staticmethod
    def rollback(project_id: str, deployment_id: str,
                 cred_key: str = "vercel") -> ToolResult:
        try:
            import requests
            headers = VercelTool._headers(cred_key)
            r = requests.post(
                f"{VercelTool.VERCEL_API}/v9/projects/{project_id}/rollback/{deployment_id}",
                headers=headers, timeout=30
            )
            if r.status_code in (200, 201, 204):
                return ToolResult(True, f"✓ Rolled back project '{project_id}' to '{deployment_id}'")
            return ToolResult(False, f"✗ Rollback failed: {r.text}")
        except Exception as e:
            return ToolResult(False, f"✗ rollback failed: {e}")

    @staticmethod
    def add_domain(project_id: str, domain: str,
                   cred_key: str = "vercel") -> ToolResult:
        try:
            resp = VercelTool._post(f"/v10/projects/{project_id}/domains",
                                    {"name": domain}, cred_key)
            if "error" in resp:
                return ToolResult(False, f"✗ Domain add failed: {resp['error']}")
            return ToolResult(True, f"✓ Domain '{domain}' added to project '{project_id}'")
        except Exception as e:
            return ToolResult(False, f"✗ add_domain failed: {e}")

    @staticmethod
    def list_domains(project_id: str, cred_key: str = "vercel") -> ToolResult:
        try:
            resp = VercelTool._get(f"/v9/projects/{project_id}/domains", cred_key)
            domains = [{"name": d.get("name"), "verified": d.get("verified"),
                        "apex": d.get("apexName")}
                       for d in resp.get("domains", [])]
            return ToolResult(True, f"✓ {len(domains)} domains", domains)
        except Exception as e:
            return ToolResult(False, f"✗ list_domains failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 6. NetlifyTool
# ══════════════════════════════════════════════════════════════════════════════
class NetlifyTool:
    name = "netlify"
    description = "Netlify deployment: sites, deploys, env vars, domains, forms"
    use = (
        """Name of Tool:- NetlifyTool

Purpose of Tool:- 
The NetlifyTool is a deployment and cloud hosting administration utility that enables programmatic control over web applications hosted on Netlify. It provides direct automation wrappers around the official Netlify REST API to manage static web assets, handle CI/CD delivery pipelines, orchestrate atomic rolling updates, and manipulate runtime parameters. The tool supports deploying local code folders directly by calculating file hash maps and syncing dynamic file payloads via octet-stream buffers. Additionally, it streamlines site configurations by letting users modify environment variables, provision custom domain names, manage rollback versions, and download user submission records captured from native Netlify HTML form parsing layers.

Methods:-
- list_sites: Retrieves a summary list of all web application projects tied to the active account profile.
- create_site: Instantiates a new workspace slot on Netlify, optionally configuring continuous integration bindings to a remote GitHub branch.
- delete_site: Permanently destroys a targeted hosting project slot and cleans up its remote web presence.
- deploy_folder: Scans local sub-directories to map unique file digests, initializing atomic state uploads to release project content updates.
- list_deploys: Compiles chronological historical data logs tracking site release states, time marks, and explicit entry paths.
- rollback_deploy: Switches the active production pointer of a web application to point back to a previous build artifact version.
- lock_deploy: Freezes a specific production state, ensuring subsequent continuous integration code pushes do not overwrite active live environments.
- set_env_var: Patches runtime application configurations by writing key-value parameter sets directly to site container blocks.
- list_env_vars: Returns a structured map containing all environmental configuration fields linked to a targeted site.
- delete_env_var: Removes targeted key-value pairs from site container runtime blocks.
- add_domain: Provisions custom domain aliases, binding public web address configurations directly onto target hosting structures.
- list_forms: Tracks parsed native HTML form layers detected inside site pages and reports active response tallies.
- get_form_submissions: Extracts tabular contact records, timelines, and payloads collected from active contact forms.

How to use Tool Methods:-

1. list_sites:
   - Purpose: Lists accessible web projects, pulling structural operational data like IDs, current states, and default system URLs.
   - Arguments:
     a) cred_key: str (default: "netlify") - Reference index used to select specific token blocks out of credential stores.
   - Returns: ToolResult packaging arrays of dictionary records mapped from active projects.
   - How to call: NetlifyTool.list_sites(cred_key="production_token")

2. create_site:
   - Purpose: provisions a clean staging area or links a new instance block to an automated main GitHub code branch tracking system.
   - Arguments:
     a) name: str - Target site descriptor tag defining the alphanumeric root domain name.
     b) repo_url: str (default: "") - Destination web link pointing to target GitHub source projects.
     c) cred_key: str (default: "netlify") - Vault lookup pointer for loading operational token keys.
   - Returns: ToolResult passing the unique project ID string alongside target staging URLs.
   - How to call: NetlifyTool.create_site(name="portfolio-v4-2026", repo_url="https://github.com/user/portfolio-v4", cred_key="netlify")

3. delete_site:
   - Purpose: Erases active web instances to prevent unnecessary cloud footprint consumption.
   - Arguments:
     a) site_id: str - Unique target alphanumeric hash code mapped to a project.
     b) cred_key: str (default: "netlify") - Vault lookup key string for verification tokens.
   - Returns: ToolResult validating deletion completion states.
   - How to call: NetlifyTool.delete_site(site_id="661ba2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c")

4. deploy_folder:
   - Purpose: Deploys local folder assets manually by building a digest map of file signatures and shipping missing files to Netlify's content network.
   - Arguments:
     a) site_id: str - Target identification code string pointing to a site.
     b) folder_path: str - Local directory file path tracking static project code structures.
     c) message: str (default: "Deploy via NPM Agent") - Build title note explaining the source of the release update.
     d) cred_key: str (default: "netlify") - Reference token label key.
   - Returns: ToolResult containing deployment index numbers and distinct preview path URLs.
   - How to call: NetlifyTool.deploy_folder(site_id="portfolio-v4-2026", folder_path="./dist", message="Production hotfix build")

5. list_deploys:
   - Purpose: Compiles a history of recent build iterations to track operational stability metrics.
   - Arguments:
     a) site_id: str - Project tracking hash value.
     b) cred_key: str (default: "netlify") - Security authentication key selector.
   - Returns: ToolResult outputting arrays that detail past deployment identifiers, creation dates, and status codes.
   - How to call: NetlifyTool.list_deploys(site_id="661ba2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c")

6. rollback_deploy:
   - Purpose: Instantly restores web pages to a known safe historical build version during runtime emergencies.
   - Arguments:
     a) site_id: str - Target project lookup reference code.
     b) deploy_id: str - target historical build signature map pointing to preferred states.
     c) cred_key: str (default: "netlify") - Security verification key text.
   - Returns: ToolResult confirming operational pointer updates.
   - How to call: NetlifyTool.rollback_deploy(site_id="portfolio-v4-2026", deploy_id="661c98e7a1b2c3d4e5f6a7b8")

7. lock_deploy:
   - Purpose: Implements strict continuous delivery version freezes to conduct production maintenance or prevent automated pipeline updates.
   - Arguments:
     a) site_id: str - Project identification hash string.
     b) deploy_id: str - Build reference marker to freeze in place.
     c) cred_key: str (default: "netlify") - Vault validation pointer.
   - Returns: ToolResult recording frozen state flags.
   - How to call: NetlifyTool.lock_deploy(site_id="portfolio-v4-2026", deploy_id="661c98e7a1b2c3d4e5f6a7b8")

8. set_env_var:
   - Purpose: injects crucial runtime configuration properties like API keys or backend endpoint strings into site containers.
   - Arguments:
     a) site_id: str - target reference code string identifying the site.
     b) key: str - Uppercase string labeling the target environment parameter.
     c) value: str - Configuration string stored alongside target keys.
     d) cred_key: str (default: "netlify") - Access token index label.
   - Returns: ToolResult ensuring safe parameter inclusion.
   - How to call: NetlifyTool.set_env_var(site_id="661ba2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c", key="DATABASE_URL", value="mongodb+srv://admin:pass@cluster.io")

9. list_env_vars:
   - Purpose: Inspects site container environments to verify active runtime values and identify structural discrepancies.
   - Arguments:
     a) site_id: str - System identifier tracking the target site.
     b) cred_key: str (default: "netlify") - Internal security credential map key.
   - Returns: ToolResult packaging complete dictionaries of runtime parameters.
   - How to call: NetlifyTool.list_env_vars(site_id="661ba2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c")

10. delete_env_var:
    - Purpose: Removes stale configuration elements or resets runtime variables back to global project defaults.
    - Arguments:
      a) site_id: str - Target site index token.
      b) key: str - Configuration descriptor name to remove.
      c) cred_key: str (default: "netlify") - Access validation key string.
    - Returns: ToolResult verifying removal from site settings.
    - How to call: NetlifyTool.delete_env_var(site_id="portfolio-v4-2026", key="STAGING_API_KEY")

11. add_domain:
    - Purpose: Binds external custom domains onto Netlify routing matrices to set up polished, branded production entryways.
    - Arguments:
      a) site_id: str - target workspace index value mapping projects.
      b) domain: str - Fully qualified web address name string.
      c) cred_key: str (default: "netlify") - Internal system token reference.
    - Returns: ToolResult confirming custom domain mapping.
    - How to call: NetlifyTool.add_domain(site_id="661ba2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c", domain="www.mycustomportfolio.com")

12. list_forms:
    - Purpose: Enumerates forms found during page parsing routines, providing immediate visibility into interaction counts.
    - Arguments:
      a) site_id: str - Project lookup identification string.
      b) cred_key: str (default: "netlify") - Encryption key locator tracking credentials.
    - Returns: ToolResult summarizing form structures, system tags, and submission metrics.
    - How to call: NetlifyTool.list_forms(site_id="portfolio-v4-2026")

13. get_form_submissions:
    - Purpose: Pulls form data records submitted by users directly into clean, actionable dataset arrays.
    - Arguments:
      a) form_id: str - Unique form identifier hash token generated by Netlify.
      b) cred_key: str (default: "netlify") - Vault validation credential pointer.
    - Returns: ToolResult matching data entries with explicit transaction timestamps.
    - How to call: NetlifyTool.get_form_submissions(form_id="661da5e4b3c2a1f0e9d8c7b6")
    """)
    
    NETLIFY_API = "https://api.netlify.com/api/v1"

    @staticmethod
    def _headers(cred_key: str = "netlify") -> dict:
        token = CredStore.load(cred_key).get("token", "")
        if not token:
            raise ValueError("No Netlify token in credentials")
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    @staticmethod
    def _get(path: str, cred_key: str = "netlify") -> Any:
        import requests
        r = requests.get(f"{NetlifyTool.NETLIFY_API}{path}",
                         headers=NetlifyTool._headers(cred_key), timeout=30)
        return r.json()

    @staticmethod
    def _post(path: str, data: Any, cred_key: str = "netlify") -> Any:
        import requests
        r = requests.post(f"{NetlifyTool.NETLIFY_API}{path}",
                          headers=NetlifyTool._headers(cred_key),
                          json=data, timeout=30)
        return r.json()

    @staticmethod
    def _delete(path: str, cred_key: str = "netlify") -> bool:
        import requests
        r = requests.delete(f"{NetlifyTool.NETLIFY_API}{path}",
                            headers=NetlifyTool._headers(cred_key), timeout=30)
        return r.status_code in (200, 204)

    @staticmethod
    def list_sites(cred_key: str = "netlify") -> ToolResult:
        try:
            resp = NetlifyTool._get("/sites?per_page=100", cred_key)
            sites = [{"id": s.get("id"), "name": s.get("name"),
                      "url": s.get("url"), "state": s.get("state")}
                     for s in (resp if isinstance(resp, list) else [])]
            return ToolResult(True, f"✓ {len(sites)} Netlify sites", sites)
        except Exception as e:
            return ToolResult(False, f"✗ list_sites failed: {e}")

    @staticmethod
    def create_site(name: str, repo_url: str = "",
                    cred_key: str = "netlify") -> ToolResult:
        try:
            data: dict = {"name": name}
            if repo_url:
                data["repo"] = {"url": repo_url, "provider": "github",
                                 "branch": "main", "cmd": "", "dir": ""}
            resp = NetlifyTool._post("/sites", data, cred_key)
            if "id" not in resp:
                return ToolResult(False, f"✗ Site create failed: {resp}")
            return ToolResult(True, f"✓ Netlify site '{name}' created",
                              {"id": resp.get("id"), "url": resp.get("url")})
        except Exception as e:
            return ToolResult(False, f"✗ create_site failed: {e}")

    @staticmethod
    def delete_site(site_id: str, cred_key: str = "netlify") -> ToolResult:
        try:
            NetlifyTool._delete(f"/sites/{site_id}", cred_key)
            return ToolResult(True, f"✓ Netlify site '{site_id}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_site failed: {e}")

    @staticmethod
    def deploy_folder(site_id: str, folder_path: str,
                      message: str = "Deploy via NPM Agent",
                      cred_key: str = "netlify") -> ToolResult:
        try:
            import requests
            import hashlib as hl
            # Build file digest map
            base = Path(folder_path)
            files_map: dict = {}
            for fp in base.rglob("*"):
                if fp.is_file():
                    rel = str(fp.relative_to(base))
                    files_map[f"/{rel}"] = hl.sha1(fp.read_bytes()).hexdigest()
            # Start deployment
            headers = NetlifyTool._headers(cred_key)
            r1 = requests.post(
                f"{NetlifyTool.NETLIFY_API}/sites/{site_id}/deploys",
                headers=headers,
                json={"files": files_map, "title": message},
                timeout=30,
            )
            deploy = r1.json()
            deploy_id = deploy.get("id")
            required = deploy.get("required", [])
            # Upload required files
            for sha in required:
                for path_key, file_sha in files_map.items():
                    if file_sha == sha:
                        fp = base / path_key.lstrip("/")
                        if fp.exists():
                            upload_headers = {
                                "Authorization": headers["Authorization"],
                                "Content-Type": "application/octet-stream",
                            }
                            requests.put(
                                f"{NetlifyTool.NETLIFY_API}/deploys/{deploy_id}/files{path_key}",
                                headers=upload_headers,
                                data=fp.read_bytes(),
                                timeout=60,
                            )
            return ToolResult(True, f"✓ Deployed folder to Netlify site '{site_id}'",
                              {"deploy_id": deploy_id, "url": deploy.get("deploy_ssl_url")})
        except Exception as e:
            return ToolResult(False, f"✗ deploy_folder failed: {e}")

    @staticmethod
    def list_deploys(site_id: str, cred_key: str = "netlify") -> ToolResult:
        try:
            resp = NetlifyTool._get(f"/sites/{site_id}/deploys?per_page=20", cred_key)
            deploys = [{"id": d.get("id"), "state": d.get("state"),
                        "created_at": d.get("created_at"),
                        "url": d.get("deploy_ssl_url")}
                       for d in (resp if isinstance(resp, list) else [])]
            return ToolResult(True, f"✓ {len(deploys)} deploys", deploys)
        except Exception as e:
            return ToolResult(False, f"✗ list_deploys failed: {e}")

    @staticmethod
    def rollback_deploy(site_id: str, deploy_id: str,
                        cred_key: str = "netlify") -> ToolResult:
        try:
            import requests
            r = requests.post(
                f"{NetlifyTool.NETLIFY_API}/sites/{site_id}/deploys/{deploy_id}/restore",
                headers=NetlifyTool._headers(cred_key), timeout=30
            )
            if r.status_code in (200, 201):
                return ToolResult(True, f"✓ Rolled back to deploy '{deploy_id}'")
            return ToolResult(False, f"✗ Rollback failed: {r.text}")
        except Exception as e:
            return ToolResult(False, f"✗ rollback_deploy failed: {e}")

    @staticmethod
    def lock_deploy(site_id: str, deploy_id: str,
                    cred_key: str = "netlify") -> ToolResult:
        try:
            import requests
            r = requests.post(
                f"{NetlifyTool.NETLIFY_API}/deploys/{deploy_id}/lock",
                headers=NetlifyTool._headers(cred_key), timeout=30
            )
            if r.status_code in (200, 201):
                return ToolResult(True, f"✓ Deploy '{deploy_id}' locked")
            return ToolResult(False, f"✗ Lock failed: {r.text}")
        except Exception as e:
            return ToolResult(False, f"✗ lock_deploy failed: {e}")

    @staticmethod
    def set_env_var(site_id: str, key: str, value: str,
                    cred_key: str = "netlify") -> ToolResult:
        try:
            import requests
            # Get existing env vars first
            r = requests.get(
                f"{NetlifyTool.NETLIFY_API}/accounts",
                headers=NetlifyTool._headers(cred_key), timeout=15
            )
            # Use site-level env vars endpoint
            r2 = requests.post(
                f"{NetlifyTool.NETLIFY_API}/sites/{site_id}/env",
                headers=NetlifyTool._headers(cred_key),
                json={key: value}, timeout=15
            )
            if r2.status_code in (200, 201):
                return ToolResult(True, f"✓ Env var '{key}' set")
            return ToolResult(False, f"✗ Env var set failed: {r2.text}")
        except Exception as e:
            return ToolResult(False, f"✗ set_env_var failed: {e}")

    @staticmethod
    def list_env_vars(site_id: str, cred_key: str = "netlify") -> ToolResult:
        try:
            resp = NetlifyTool._get(f"/sites/{site_id}/env", cred_key)
            return ToolResult(True, f"✓ Env vars for site '{site_id}'", resp)
        except Exception as e:
            return ToolResult(False, f"✗ list_env_vars failed: {e}")

    @staticmethod
    def delete_env_var(site_id: str, key: str,
                       cred_key: str = "netlify") -> ToolResult:
        try:
            import requests
            r = requests.delete(
                f"{NetlifyTool.NETLIFY_API}/sites/{site_id}/env/{key}",
                headers=NetlifyTool._headers(cred_key), timeout=15
            )
            if r.status_code in (200, 204):
                return ToolResult(True, f"✓ Env var '{key}' deleted")
            return ToolResult(False, f"✗ Delete env var failed: {r.text}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_env_var failed: {e}")

    @staticmethod
    def add_domain(site_id: str, domain: str,
                   cred_key: str = "netlify") -> ToolResult:
        try:
            resp = NetlifyTool._post(f"/sites/{site_id}/domain_aliases",
                                     {"domain": domain}, cred_key)
            if "id" in resp or "name" in resp:
                return ToolResult(True, f"✓ Domain '{domain}' added to site '{site_id}'")
            return ToolResult(False, f"✗ Domain add failed: {resp}")
        except Exception as e:
            return ToolResult(False, f"✗ add_domain failed: {e}")

    @staticmethod
    def list_forms(site_id: str, cred_key: str = "netlify") -> ToolResult:
        try:
            resp = NetlifyTool._get(f"/sites/{site_id}/forms", cred_key)
            forms = [{"id": f.get("id"), "name": f.get("name"),
                      "submission_count": f.get("submission_count")}
                     for f in (resp if isinstance(resp, list) else [])]
            return ToolResult(True, f"✓ {len(forms)} forms", forms)
        except Exception as e:
            return ToolResult(False, f"✗ list_forms failed: {e}")

    @staticmethod
    def get_form_submissions(form_id: str,
                              cred_key: str = "netlify") -> ToolResult:
        try:
            resp = NetlifyTool._get(f"/forms/{form_id}/submissions?per_page=50", cred_key)
            submissions = [{"id": s.get("id"), "created_at": s.get("created_at"),
                            "data": s.get("data")}
                           for s in (resp if isinstance(resp, list) else [])]
            return ToolResult(True, f"✓ {len(submissions)} form submissions", submissions)
        except Exception as e:
            return ToolResult(False, f"✗ get_form_submissions failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 7. RailwayTool
# ══════════════════════════════════════════════════════════════════════════════
class RailwayTool:
    name = "railway"
    description = "Railway.app deployment: projects, services, env vars, logs"
    use = (
        """
Name of Tool:- RailwayTool,

Purpose of Tool:- 
The RailwayTool provides a comprehensive interface to Railway.app for deploying and managing applications on their platform. 
It supports project and service management, deployments (via CLI and GraphQL), environment variables, logs, and deployment history. 
The tool combines direct GraphQL API calls for most management operations with the official Railway CLI for deployment and log streaming. 
All operations require a Railway API token stored in CredStore. 
This tool is ideal for automated deployments, DevOps workflows, environment management, and agentic full-stack application hosting on Railway.

Methods:-
- _headers: Internal helper to generate authentication headers.
- _gql: Internal helper to execute GraphQL queries and mutations.
- deploy: Deploys a local project using the Railway CLI.
- list_projects: Lists all projects in the account.
- create_project: Creates a new project.
- list_services: Lists services within a project.
- deploy_service: Triggers a new deployment for a service.
- restart_service: Redeploys/restarts a service.
- set_env_var: Sets or updates an environment variable.
- list_env_vars: Lists environment variables for a service.
- get_logs: Retrieves recent logs for a service using the Railway CLI.
- get_deployments: Lists deployment history for a service.

How to use Tool Methods:-

1. _headers (Internal Authentication Helper):
   - Purpose: Constructs the Bearer token authorization header required by Railway API.
   - Arguments: cred_key: str (default: "railway")
   - Credential requirement: CredStore must contain {'token': 'your-railway-api-token'}.
   - Note: Internal method. Do not call directly.

2. _gql (Internal GraphQL Helper):
   - Purpose: Executes GraphQL queries and mutations against Railway's GraphQL API.
   - Arguments:
     a) query: str - GraphQL query or mutation string.
     b) variables: dict (default: None) - Variables for the query.
     c) cred_key: str (default: "railway").
   - Note: Internal method used by most API operations.

3. deploy:
   - Purpose: Deploys (or updates) a local project directory to Railway using the official CLI. This handles build, environment detection, and full deployment lifecycle.
   - Arguments:
     a) project_path: str - Local directory path containing the project (with railway.json or auto-detectable framework).
     b) environment: str (default: "production") - Target environment name.
     c) cred_key: str (default: "railway").
   - Returns: Success status and full CLI output.
   - How to call: 
     RailwayTool.deploy(
         project_path="./my-app",
         environment="production"
     )

4. list_projects:
   - Purpose: Lists all projects accessible to the authenticated user.
   - Arguments: cred_key: str (default: "railway").
   - Returns: List of projects with id, name, and creation time.
   - How to call: RailwayTool.list_projects()

5. create_project:
   - Purpose: Creates a new project on Railway.
   - Arguments:
     a) name: str - Name of the new project.
     b) cred_key: str (default: "railway").
   - Returns: Project ID and name.
   - How to call: RailwayTool.create_project(name="my-new-project")

6. list_services:
   - Purpose: Lists all services inside a specific project.
   - Arguments:
     a) project_id: str - Railway project ID.
     b) cred_key: str (default: "railway").
   - Returns: List of services with id and name.
   - How to call: RailwayTool.list_services(project_id="prj_abc123")

7. deploy_service:
   - Purpose: Triggers a new deployment for an existing service.
   - Arguments:
     a) service_id: str - Service ID.
     b) cred_key: str (default: "railway").
   - How to call: RailwayTool.deploy_service(service_id="svc_xyz789")

8. restart_service:
   - Purpose: Redeploys/restarts a running service.
   - Arguments: service_id, cred_key.
   - How to call: RailwayTool.restart_service(service_id="svc_xyz789")

9. set_env_var:
   - Purpose: Creates or updates an environment variable for a service.
   - Arguments:
     a) project_id: str
     b) service_id: str
     c) key: str - Variable name.
     d) value: str - Variable value.
     e) cred_key: str (default: "railway").
   - How to call: RailwayTool.set_env_var(project_id="prj_abc123", service_id="svc_xyz789", key="DATABASE_URL", value="...")

10. list_env_vars:
    - Purpose: Retrieves all environment variables for a service.
    - Arguments:
      a) project_id: str
      b) service_id: str
      c) cred_key: str (default: "railway").
    - Returns: Dictionary of environment variables.
    - How to call: RailwayTool.list_env_vars(project_id="prj_abc123", service_id="svc_xyz789")

11. get_logs:
    - Purpose: Fetches recent logs for a service using the Railway CLI (supports tailing).
    - Arguments:
      a) service_id: str
      b) lines: int (default: 100) - Number of log lines to retrieve.
      c) cred_key: str (default: "railway").
    - Returns: Raw log output.
    - How to call: RailwayTool.get_logs(service_id="svc_xyz789", lines=200)

12. get_deployments:
    - Purpose: Retrieves deployment history for a service.
    - Arguments:
      a) service_id: str
      b) cred_key: str (default: "railway").
    - Returns: List of deployments with id, status, creation time, and URL.
    - How to call: RailwayTool.get_deployments(service_id="svc_xyz789")
""")
    
    RAILWAY_API = "https://backboard.railway.app/graphql/v2"

    @staticmethod
    def _headers(cred_key: str = "railway") -> dict:
        token = CredStore.load(cred_key).get("token", "")
        if not token:
            raise ValueError("No Railway token in credentials")
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    @staticmethod
    def _gql(query: str, variables: dict = None,
             cred_key: str = "railway") -> dict:
        import requests
        r = requests.post(
            RailwayTool.RAILWAY_API,
            headers=RailwayTool._headers(cred_key),
            json={"query": query, "variables": variables or {}},
            timeout=30,
        )
        return r.json()

    @staticmethod
    def deploy(project_path: str, environment: str = "production",
               cred_key: str = "railway") -> ToolResult:
        try:
            token = CredStore.load(cred_key).get("token", "")
            env = os.environ.copy()
            if token:
                env["RAILWAY_TOKEN"] = token
            result = subprocess.run(
                ["railway", "up", "--environment", environment],
                cwd=project_path,
                capture_output=True, text=True, timeout=300, env=env
            )
            output = result.stdout + result.stderr
            success = result.returncode == 0
            return ToolResult(success,
                              f"✓ Deployed to Railway ({environment})" if success
                              else f"✗ Deploy failed: {output}",
                              {"output": output})
        except Exception as e:
            return ToolResult(False, f"✗ deploy failed: {e}")

    @staticmethod
    def list_projects(cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            query { me { projects { edges { node { id name createdAt } } } } }
            """
            resp = RailwayTool._gql(query, cred_key=cred_key)
            edges = resp.get("data", {}).get("me", {}).get("projects", {}).get("edges", [])
            projects = [{"id": e["node"]["id"], "name": e["node"]["name"],
                         "created_at": e["node"]["createdAt"]}
                        for e in edges]
            return ToolResult(True, f"✓ {len(projects)} Railway projects", projects)
        except Exception as e:
            return ToolResult(False, f"✗ list_projects failed: {e}")

    @staticmethod
    def create_project(name: str, cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            mutation($name: String!) {
              projectCreate(input: { name: $name }) { id name }
            }
            """
            resp = RailwayTool._gql(query, {"name": name}, cred_key)
            project = resp.get("data", {}).get("projectCreate", {})
            if not project.get("id"):
                return ToolResult(False, f"✗ Project create failed: {resp.get('errors')}")
            return ToolResult(True, f"✓ Railway project '{name}' created",
                              {"id": project.get("id")})
        except Exception as e:
            return ToolResult(False, f"✗ create_project failed: {e}")

    @staticmethod
    def list_services(project_id: str, cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            query($id: String!) {
              project(id: $id) {
                services { edges { node { id name createdAt } } }
              }
            }
            """
            resp = RailwayTool._gql(query, {"id": project_id}, cred_key)
            edges = resp.get("data", {}).get("project", {}).get("services", {}).get("edges", [])
            services = [{"id": e["node"]["id"], "name": e["node"]["name"]}
                        for e in edges]
            return ToolResult(True, f"✓ {len(services)} services in project", services)
        except Exception as e:
            return ToolResult(False, f"✗ list_services failed: {e}")

    @staticmethod
    def deploy_service(service_id: str, cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            mutation($id: String!) {
              serviceInstanceDeploy(serviceId: $id)
            }
            """
            resp = RailwayTool._gql(query, {"id": service_id}, cred_key)
            if resp.get("errors"):
                return ToolResult(False, f"✗ Service deploy failed: {resp['errors']}")
            return ToolResult(True, f"✓ Service '{service_id}' deploy triggered")
        except Exception as e:
            return ToolResult(False, f"✗ deploy_service failed: {e}")

    @staticmethod
    def restart_service(service_id: str, cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            mutation($id: String!) {
              serviceInstanceRedeploy(serviceId: $id)
            }
            """
            resp = RailwayTool._gql(query, {"id": service_id}, cred_key)
            if resp.get("errors"):
                return ToolResult(False, f"✗ Restart failed: {resp['errors']}")
            return ToolResult(True, f"✓ Service '{service_id}' restarted")
        except Exception as e:
            return ToolResult(False, f"✗ restart_service failed: {e}")

    @staticmethod
    def set_env_var(project_id: str, service_id: str,
                    key: str, value: str,
                    cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            mutation($input: VariableUpsertInput!) {
              variableUpsert(input: $input)
            }
            """
            variables = {"input": {
                "projectId": project_id,
                "serviceId": service_id,
                "environmentId": "",
                "name": key,
                "value": value,
            }}
            resp = RailwayTool._gql(query, variables, cred_key)
            if resp.get("errors"):
                return ToolResult(False, f"✗ Env var set failed: {resp['errors']}")
            return ToolResult(True, f"✓ Env var '{key}' set on service '{service_id}'")
        except Exception as e:
            return ToolResult(False, f"✗ set_env_var failed: {e}")

    @staticmethod
    def list_env_vars(project_id: str, service_id: str,
                      cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            query($projectId: String!, $serviceId: String!, $environmentId: String!) {
              variables(projectId: $projectId, serviceId: $serviceId, environmentId: $environmentId)
            }
            """
            resp = RailwayTool._gql(
                query,
                {"projectId": project_id, "serviceId": service_id, "environmentId": ""},
                cred_key
            )
            variables = resp.get("data", {}).get("variables", {})
            return ToolResult(True, f"✓ Env vars for service '{service_id}'", variables)
        except Exception as e:
            return ToolResult(False, f"✗ list_env_vars failed: {e}")

    @staticmethod
    def get_logs(service_id: str, lines: int = 100,
                 cred_key: str = "railway") -> ToolResult:
        try:
            token = CredStore.load(cred_key).get("token", "")
            env = os.environ.copy()
            if token:
                env["RAILWAY_TOKEN"] = token
            result = subprocess.run(
                ["railway", "logs", "--service", service_id, "--tail", str(lines)],
                capture_output=True, text=True, timeout=30, env=env
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0,
                              f"✓ Logs for service '{service_id}'" if result.returncode == 0
                              else f"✗ Logs failed: {output}",
                              output)
        except Exception as e:
            return ToolResult(False, f"✗ get_logs failed: {e}")

    @staticmethod
    def get_deployments(service_id: str, cred_key: str = "railway") -> ToolResult:
        try:
            query = """
            query($serviceId: String!) {
              deployments(input: { serviceId: $serviceId }) {
                edges { node { id status createdAt url } }
              }
            }
            """
            resp = RailwayTool._gql(query, {"serviceId": service_id}, cred_key)
            edges = resp.get("data", {}).get("deployments", {}).get("edges", [])
            deployments = [{"id": e["node"]["id"], "status": e["node"]["status"],
                            "created_at": e["node"]["createdAt"],
                            "url": e["node"].get("url")}
                           for e in edges]
            return ToolResult(True, f"✓ {len(deployments)} deployments", deployments)
        except Exception as e:
            return ToolResult(False, f"✗ get_deployments failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 8. KubernetesTool
# ══════════════════════════════════════════════════════════════════════════════
class KubernetesTool:
    name = "kubernetes"
    description = "Full kubectl/Kubernetes operations: pods, deployments, services, nodes, helm"
    use = (
        """
Name of Tool:- KubernetesTool,

Purpose of Tool:- 
The KubernetesTool provides a comprehensive, production-ready interface for interacting with Kubernetes clusters using the kubectl CLI and Helm. 
It supports applying manifests, managing pods, deployments, services, nodes, namespaces, secrets, ConfigMaps, resource usage monitoring, pod execution, port forwarding, scaling, rollouts, and full Helm chart lifecycle management (install, upgrade, uninstall, list). 
This tool is designed for cluster administration, application deployment, troubleshooting, scaling, and agentic Kubernetes operations across any cluster where kubectl is configured and accessible.

Methods:-
- _kubectl: Internal helper to execute kubectl commands.
- apply: Applies Kubernetes manifests (file or inline YAML).
- delete_resource: Deletes a Kubernetes resource.
- get_pods: Lists pods with status and readiness information.
- describe_pod: Describes a pod in detail.
- get_pod_logs: Retrieves logs from a pod or specific container.
- exec_in_pod: Executes a command inside a running pod.
- get_deployments: Lists deployments with replica status.
- scale_deployment: Scales a deployment to a desired number of replicas.
- rollout_restart: Restarts a deployment (triggers rolling update).
- rollout_status: Checks the rollout status of a deployment.
- get_services: Lists services with type, ClusterIP, and ports.
- port_forward: Sets up local port forwarding to a Kubernetes resource.
- get_nodes: Lists cluster nodes with capacity and readiness.
- cordon_node: Marks a node as unschedulable.
- drain_node: Drains a node (evicts pods) for maintenance.
- apply_secret: Creates or updates a Secret from a dictionary.
- get_configmap: Retrieves a ConfigMap's data.
- create_namespace: Creates a new namespace.
- list_namespaces: Lists all namespaces.
- get_resource_usage: Shows CPU and memory usage of pods (kubectl top).
- helm_install: Installs a Helm chart.
- helm_upgrade: Upgrades or installs a Helm chart.
- helm_uninstall: Uninstalls a Helm release.
- helm_list: Lists deployed Helm releases.

How to use Tool Methods:-

1. _kubectl (Internal Helper):
   - Purpose: Executes kubectl commands with optional namespace and stdin support.
   - Arguments:
     a) args: list - List of kubectl command arguments.
     b) namespace: str (default: None) - Target namespace.
     c) stdin_data: str (default: None) - Data to pipe to stdin (for apply -f -).
     d) timeout: int (default: 60) - Command timeout in seconds.
   - Note: Internal method. You generally do not call it directly.

2. apply:
   - Purpose: Applies Kubernetes resources from a file or inline YAML string. Supports both file paths and direct manifest content.
   - Arguments:
     a) manifest_path_or_yaml: str - Either path to a YAML file or the full YAML content as string.
     b) namespace: str (default: "default").
   - How to call: 
     KubernetesTool.apply(manifest_path_or_yaml="deployment.yaml", namespace="production")
     or
     KubernetesTool.apply(manifest_path_or_yaml='''apiVersion: v1\nkind: Pod\n...''')

3. delete_resource:
   - Purpose: Deletes a specific Kubernetes resource (pod, deployment, service, etc.).
   - Arguments:
     a) kind: str - Resource kind (pod, deployment, service, configmap, secret, etc.).
     b) name: str - Name of the resource.
     c) namespace: str (default: "default").
   - How to call: KubernetesTool.delete_resource(kind="deployment", name="my-app", namespace="production")

4. get_pods:
   - Purpose: Lists pods in a namespace with phase, readiness, and node information.
   - Arguments:
     a) namespace: str (default: "default")
     b) label_selector: str (default: "") - e.g., "app=my-app"
   - Returns: List of pods with name, status, ready containers count, and node.
   - How to call: KubernetesTool.get_pods(namespace="default", label_selector="app=nginx")

5. describe_pod:
   - Purpose: Returns detailed information about a pod (events, conditions, spec, status).
   - Arguments: name, namespace (default: "default")
   - How to call: KubernetesTool.describe_pod(name="my-pod-xyz", namespace="default")

6. get_pod_logs:
   - Purpose: Retrieves container logs from a pod.
   - Arguments:
     a) name: str - Pod name
     b) namespace: str (default: "default")
     c) container: str (default: "") - Specific container name
     d) tail: int (default: 100) - Number of recent lines
     e) follow: bool (default: False) - Follow logs (limited timeout)
   - How to call: KubernetesTool.get_pod_logs(name="my-pod", tail=200)

7. exec_in_pod:
   - Purpose: Executes a shell command inside a running pod.
   - Arguments:
     a) name: str - Pod name
     b) namespace: str (default: "default")
     c) command: list (default: ["sh", "-c", "echo hello"])
     d) container: str (default: "")
   - How to call: KubernetesTool.exec_in_pod(name="my-pod", command=["ls", "-la"])

8. get_deployments:
   - Purpose: Lists deployments with replica counts and availability.
   - Arguments: namespace (default: "default")
   - How to call: KubernetesTool.get_deployments(namespace="production")

9. scale_deployment:
   - Purpose: Scales a deployment to the specified number of replicas.
   - Arguments:
     a) name: str - Deployment name
     b) replicas: int - Desired replica count
     c) namespace: str (default: "default")
   - How to call: KubernetesTool.scale_deployment(name="my-app", replicas=5)

10. rollout_restart:
    - Purpose: Triggers a rolling restart of a deployment.
    - Arguments: deployment, namespace
    - How to call: KubernetesTool.rollout_restart(deployment="my-app")

11. rollout_status:
    - Purpose: Checks the rollout status of a deployment with timeout.
    - Arguments: deployment, namespace
    - How to call: KubernetesTool.rollout_status(deployment="my-app")

12. get_services:
    - Purpose: Lists services with type, ClusterIP, and exposed ports.
    - Arguments: namespace
    - How to call: KubernetesTool.get_services(namespace="default")

13. port_forward:
    - Purpose: Starts a local port-forward to a Kubernetes resource (pod, service, etc.).
    - Arguments:
      a) resource: str - e.g., "pod/my-pod" or "service/my-svc"
      b) local_port: int
      c) remote_port: int
      d) namespace: str (default: "default")
    - Returns: Process PID (background process)
    - How to call: KubernetesTool.port_forward(resource="service/my-api", local_port=8080, remote_port=3000)

14. get_nodes:
    - Purpose: Lists cluster nodes with readiness, capacity, and roles.
    - How to call: KubernetesTool.get_nodes()

15. cordon_node / drain_node:
    - Purpose: Cordon marks a node unschedulable. Drain evicts pods for maintenance.
    - How to call: KubernetesTool.drain_node(name="node-1", force=True)

16. apply_secret:
    - Purpose: Creates or updates a Kubernetes Secret from a Python dictionary.
    - Arguments:
      a) name: str
      b) namespace: str
      c) data: dict - Key-value pairs (automatically base64 encoded)
    - How to call: KubernetesTool.apply_secret(name="db-credentials", namespace="default", data={"username": "admin", "password": "secret"})

17. get_configmap:
    - Purpose: Retrieves data from a ConfigMap.
    - Arguments: name, namespace
    - How to call: KubernetesTool.get_configmap(name="my-config", namespace="default")

18. create_namespace / list_namespaces:
    - Standard namespace management.

19. get_resource_usage:
    - Purpose: Shows real-time CPU and memory usage of pods (requires metrics-server).
    - Arguments: namespace
    - How to call: KubernetesTool.get_resource_usage(namespace="default")

20. helm_install / helm_upgrade / helm_uninstall / helm_list:
    - Full Helm chart management.
    - Arguments include release name, chart name/reference, values dict, and namespace.
    - How to call: KubernetesTool.helm_install(release="my-app", chart="nginx", values={"replicaCount": 3})
""")
    
    @staticmethod
    def _kubectl(args: list, namespace: str = None,
                 stdin_data: str = None, timeout: int = 60) -> subprocess.CompletedProcess:
        cmd = ["kubectl"] + args
        if namespace:
            cmd += ["-n", namespace]
        return subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True, text=True, timeout=timeout
        )

    @staticmethod
    def apply(manifest_path_or_yaml: str, namespace: str = "default") -> ToolResult:
        try:
            # Detect if it's YAML content or a file path
            if manifest_path_or_yaml.strip().startswith(("apiVersion:", "kind:", "---")):
                result = KubernetesTool._kubectl(
                    ["apply", "-f", "-"],
                    namespace=namespace,
                    stdin_data=manifest_path_or_yaml,
                )
            else:
                result = KubernetesTool._kubectl(
                    ["apply", "-f", manifest_path_or_yaml],
                    namespace=namespace,
                )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0,
                              output.strip() or "✓ Applied",
                              {"output": output})
        except Exception as e:
            return ToolResult(False, f"✗ apply failed: {e}")

    @staticmethod
    def delete_resource(kind: str, name: str,
                        namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["delete", kind, name], namespace=namespace
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ delete_resource failed: {e}")

    @staticmethod
    def get_pods(namespace: str = "default",
                 label_selector: str = "") -> ToolResult:
        try:
            args = ["get", "pods", "-o", "json"]
            if label_selector:
                args += ["-l", label_selector]
            result = KubernetesTool._kubectl(args, namespace=namespace)
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            data = json.loads(result.stdout)
            pods = [{"name": p["metadata"]["name"],
                     "status": p["status"].get("phase"),
                     "ready": sum(1 for c in p["status"].get("containerStatuses", []) if c.get("ready")),
                     "node": p["spec"].get("nodeName")}
                    for p in data.get("items", [])]
            return ToolResult(True, f"✓ {len(pods)} pods in '{namespace}'", pods)
        except Exception as e:
            return ToolResult(False, f"✗ get_pods failed: {e}")

    @staticmethod
    def describe_pod(name: str, namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["describe", "pod", name], namespace=namespace
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip(), output)
        except Exception as e:
            return ToolResult(False, f"✗ describe_pod failed: {e}")

    @staticmethod
    def get_pod_logs(name: str, namespace: str = "default",
                     container: str = "", tail: int = 100,
                     follow: bool = False) -> ToolResult:
        try:
            args = ["logs", name, f"--tail={tail}"]
            if container:
                args += ["-c", container]
            if follow:
                args.append("-f")
            result = KubernetesTool._kubectl(args, namespace=namespace, timeout=30)
            return ToolResult(result.returncode == 0,
                              result.stdout + result.stderr, result.stdout)
        except Exception as e:
            return ToolResult(False, f"✗ get_pod_logs failed: {e}")

    @staticmethod
    def exec_in_pod(name: str, namespace: str = "default",
                    command: list = None,
                    container: str = "") -> ToolResult:
        try:
            cmd = command or ["sh", "-c", "echo hello"]
            args = ["exec", name, "--"]
            if container:
                args = ["exec", name, "-c", container, "--"]
            args += cmd
            result = KubernetesTool._kubectl(args, namespace=namespace, timeout=60)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip(), output)
        except Exception as e:
            return ToolResult(False, f"✗ exec_in_pod failed: {e}")

    @staticmethod
    def get_deployments(namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["get", "deployments", "-o", "json"], namespace=namespace
            )
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            data = json.loads(result.stdout)
            deploys = [
                {"name": d["metadata"]["name"],
                 "replicas": d["spec"].get("replicas"),
                 "ready": d["status"].get("readyReplicas", 0),
                 "available": d["status"].get("availableReplicas", 0)}
                for d in data.get("items", [])
            ]
            return ToolResult(True, f"✓ {len(deploys)} deployments in '{namespace}'", deploys)
        except Exception as e:
            return ToolResult(False, f"✗ get_deployments failed: {e}")

    @staticmethod
    def scale_deployment(name: str, replicas: int,
                         namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["scale", "deployment", name, f"--replicas={replicas}"],
                namespace=namespace
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ scale_deployment failed: {e}")

    @staticmethod
    def rollout_restart(deployment: str,
                        namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["rollout", "restart", "deployment", deployment],
                namespace=namespace
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ rollout_restart failed: {e}")

    @staticmethod
    def rollout_status(deployment: str,
                       namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["rollout", "status", "deployment", deployment, "--timeout=120s"],
                namespace=namespace, timeout=130
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ rollout_status failed: {e}")

    @staticmethod
    def get_services(namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["get", "services", "-o", "json"], namespace=namespace
            )
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            data = json.loads(result.stdout)
            services = [
                {"name": s["metadata"]["name"],
                 "type": s["spec"].get("type"),
                 "cluster_ip": s["spec"].get("clusterIP"),
                 "ports": [f"{p.get('port')}/{p.get('protocol','TCP')}"
                           for p in s["spec"].get("ports", [])]}
                for s in data.get("items", [])
            ]
            return ToolResult(True, f"✓ {len(services)} services", services)
        except Exception as e:
            return ToolResult(False, f"✗ get_services failed: {e}")

    @staticmethod
    def port_forward(resource: str, local_port: int, remote_port: int,
                     namespace: str = "default") -> ToolResult:
        try:
            proc = subprocess.Popen(
                ["kubectl", "port-forward", resource,
                 f"{local_port}:{remote_port}", "-n", namespace],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            time.sleep(1.5)
            if proc.poll() is not None:
                err = proc.stderr.read().decode()
                return ToolResult(False, f"✗ Port-forward failed: {err}")
            return ToolResult(True,
                              f"✓ Port-forward {resource} {local_port}→{remote_port} (PID {proc.pid})",
                              {"pid": proc.pid})
        except Exception as e:
            return ToolResult(False, f"✗ port_forward failed: {e}")

    @staticmethod
    def get_nodes() -> ToolResult:
        try:
            result = KubernetesTool._kubectl(["get", "nodes", "-o", "json"])
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            data = json.loads(result.stdout)
            nodes = []
            for n in data.get("items", []):
                conditions = {c["type"]: c["status"]
                              for c in n["status"].get("conditions", [])}
                nodes.append({
                    "name": n["metadata"]["name"],
                    "ready": conditions.get("Ready") == "True",
                    "cpu": n["status"].get("capacity", {}).get("cpu"),
                    "memory": n["status"].get("capacity", {}).get("memory"),
                    "roles": [k.replace("node-role.kubernetes.io/", "")
                               for k in n["metadata"].get("labels", {})
                               if k.startswith("node-role.kubernetes.io/")],
                })
            return ToolResult(True, f"✓ {len(nodes)} nodes", nodes)
        except Exception as e:
            return ToolResult(False, f"✗ get_nodes failed: {e}")

    @staticmethod
    def cordon_node(name: str) -> ToolResult:
        try:
            result = KubernetesTool._kubectl(["cordon", name])
            return ToolResult(result.returncode == 0,
                              result.stdout.strip() or f"✓ Node '{name}' cordoned")
        except Exception as e:
            return ToolResult(False, f"✗ cordon_node failed: {e}")

    @staticmethod
    def drain_node(name: str, force: bool = False,
                   ignore_daemonsets: bool = True) -> ToolResult:
        try:
            args = ["drain", name]
            if force:
                args.append("--force")
            if ignore_daemonsets:
                args.append("--ignore-daemonsets")
            result = KubernetesTool._kubectl(args, timeout=120)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ drain_node failed: {e}")

    @staticmethod
    def apply_secret(name: str, namespace: str,
                     data: dict) -> ToolResult:
        try:
            encoded = {k: base64.b64encode(str(v).encode()).decode()
                       for k, v in data.items()}
            manifest = json.dumps({
                "apiVersion": "v1",
                "kind": "Secret",
                "metadata": {"name": name, "namespace": namespace},
                "data": encoded,
            })
            result = KubernetesTool._kubectl(
                ["apply", "-f", "-"],
                stdin_data=manifest
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ apply_secret failed: {e}")

    @staticmethod
    def get_configmap(name: str, namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["get", "configmap", name, "-o", "json"], namespace=namespace
            )
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            data = json.loads(result.stdout)
            return ToolResult(True, f"✓ ConfigMap '{name}'",
                              data.get("data", {}))
        except Exception as e:
            return ToolResult(False, f"✗ get_configmap failed: {e}")

    @staticmethod
    def create_namespace(name: str) -> ToolResult:
        try:
            result = KubernetesTool._kubectl(["create", "namespace", name])
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ create_namespace failed: {e}")

    @staticmethod
    def list_namespaces() -> ToolResult:
        try:
            result = KubernetesTool._kubectl(["get", "namespaces", "-o", "json"])
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            data = json.loads(result.stdout)
            namespaces = [{"name": n["metadata"]["name"],
                           "status": n["status"].get("phase")}
                          for n in data.get("items", [])]
            return ToolResult(True, f"✓ {len(namespaces)} namespaces", namespaces)
        except Exception as e:
            return ToolResult(False, f"✗ list_namespaces failed: {e}")

    @staticmethod
    def get_resource_usage(namespace: str = "default") -> ToolResult:
        try:
            result = KubernetesTool._kubectl(
                ["top", "pods", "--no-headers"], namespace=namespace
            )
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            usage = []
            for line in result.stdout.strip().splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    usage.append({"pod": parts[0], "cpu": parts[1], "memory": parts[2]})
            return ToolResult(True, f"✓ Resource usage for {len(usage)} pods", usage)
        except Exception as e:
            return ToolResult(False, f"✗ get_resource_usage failed: {e}")

    @staticmethod
    def helm_install(release: str, chart: str,
                     values: dict = None, namespace: str = "default") -> ToolResult:
        try:
            cmd = ["helm", "install", release, chart, "-n", namespace, "--create-namespace"]
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml",
                                             delete=False) as f:
                if values:
                    import yaml
                    yaml.dump(values, f)
                    cmd += ["-f", f.name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ helm_install failed: {e}")

    @staticmethod
    def helm_upgrade(release: str, chart: str,
                     values: dict = None, namespace: str = "default") -> ToolResult:
        try:
            cmd = ["helm", "upgrade", "--install", release, chart, "-n", namespace]
            if values:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                    import yaml
                    yaml.dump(values, f)
                    cmd += ["-f", f.name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ helm_upgrade failed: {e}")

    @staticmethod
    def helm_uninstall(release: str, namespace: str = "default") -> ToolResult:
        try:
            result = subprocess.run(
                ["helm", "uninstall", release, "-n", namespace],
                capture_output=True, text=True, timeout=60
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ helm_uninstall failed: {e}")

    @staticmethod
    def helm_list(namespace: str = "default") -> ToolResult:
        try:
            result = subprocess.run(
                ["helm", "list", "-n", namespace, "-o", "json"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            releases = json.loads(result.stdout or "[]")
            return ToolResult(True, f"✓ {len(releases)} Helm releases in '{namespace}'", releases)
        except Exception as e:
            return ToolResult(False, f"✗ helm_list failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 9. TerraformTool
# ══════════════════════════════════════════════════════════════════════════════
class TerraformTool:
    name = "terraform"
    description = "Infrastructure as Code: init, plan, apply, destroy, state management, workspaces"
    use = (
        """Name of Tool:- TerraformTool

Purpose of Tool:- 
The TerraformTool is an Infrastructure as Code (IaC) automation utility that allows for programmatic management of cloud and on-premise infrastructure. Acting as a Python wrapper around the Terraform CLI, this tool facilitates the complete lifecycle of infrastructure deployment. It handles initialization, execution plans, real-time resource provisioning, destruction routines, state file manipulations, and multi-tenant workspace management. It processes outputs directly into JSON, automatically formats and validates declarative HashiCorp Configuration Language (HCL) scripts, resolves resource dependency mappings into graphable layouts, and imports existing manual infrastructure configurations under formal lifecycle control.

Methods:-
- init: Sets up the local working environment, downloads required resource providers, and connects state backends.
- plan: Generates predictive structural execution delta logs mapping out pending state modifications.
- apply: Provisions and updates active network components to lock down target environment schemas.
- destroy: Tensors clean teardowns across cloud assets linked to monitored script frameworks.
- validate: Runs localized structural parsing loops to sweep for broken syntax arrays or illegal property associations.
- fmt: Rewrites layout alignments to conform with official standardized spacing rules.
- show: Deconstructs explicit binary execution files or target state tracking payloads into readable structural data.
- output: Grabs active deployment state parameters for programmatic handoffs to external tools.
- state_list: Queries managed tracking databases to list all managed structural resource blocks.
- state_show: Displays operational configuration parameters currently stored for a distinct provisioned item.
- state_rm: Forces tracking items out of local state systems without destroying the physical components.
- import_resource: Binds pre-existing untracked external components directly onto active internal script targets.
- graph: Compiles structural dependency links between modules into a DOT notation visual mapping script.
- workspace_list: Catalogs isolated storage namespaces available for running concurrent variable setups.
- workspace_new: Spins up a new virtual state segment block to segregate environment scopes.
- workspace_select: Toggles the active context pointer over to an alternate infrastructure namespace pipeline.

How to use Tool Methods:-

1. init:
   - Purpose: Prepares an infrastructure directory by configuring remote storage nodes and pulling structural provider runtimes.
   - Arguments:
     a) path: str - Target filesystem location containing standard infrastructure code scripts.
     b) backend_config: dict (default: None) - Context key-value blocks used to customize state backends during setup.
   - Returns: ToolResult storing complete raw log captures indicating operational initialization states.
   - How to call: TerraformTool.init(path="./infra/prod", backend_config={"bucket": "tf-state-prod", "key": "network/terraform.tfstate"})

2. plan:
   - Purpose: Examines target code updates against current reality to map out additions, adjustments, and destructive alterations.
   - Arguments:
     a) path: str - System root directory mapping the active target deployment scripts.
     b) var_file: str (default: "") - Target location pointer resolving a specific `.tfvars` properties path.
     c) vars: dict (default: None) - Direct dynamic variable dictionaries passed to overwrite script configurations.
     d) out: str (default: "tfplan") - Local name string assigned to export the compiled execution binary plan file.
   - Returns: ToolResult passing plan check assertions alongside explicit binary destination tags.
   - How to call: TerraformTool.plan(path="./infra/prod", vars={"instance_count": 3, "env": "production"}, out="outputs/june_deploy.tfplan")

3. apply:
   - Purpose: Runs targeted changes against cloud providers to build out infrastructure, using optional binary plans to guarantee consistency.
   - Arguments:
     a) path: str - Directory system pointer enclosing target resource blueprints.
     b) plan_file: str (default: "") - Reference path string targeting pre-compiled plan files.
     c) var_file: str (default: "") - Property settings path matching targeted infrastructure files.
     d) vars: dict (default: None) - Supplemental variable definitions dictionary.
     b) auto_approve: bool (default: False) - Flag that bypasses interactive prompt checks when toggled true.
   - Returns: ToolResult confirming whether runtime provider provisioning completed cleanly.
   - How to call: TerraformTool.apply(path="./infra/prod", plan_file="outputs/june_deploy.tfplan", auto_approve=True)

4. destroy:
   - Purpose: Runs systematic teardown loops that remove active live cloud infrastructure components safely.
   - Arguments:
     a) path: str - Targeted project folder path string containing tracking parameters.
     b) var_file: str (default: "") - Auxiliary property file configuration path.
     c) vars: dict (default: None) - Key-value parameter arguments dictionary.
     d) auto_approve: bool (default: False) - Bypasses execution prompts to run unprompted server drops.
   - Returns: ToolResult validating resource removal operations.
   - How to call: TerraformTool.destroy(path="./infra/staging", auto_approve=True)

5. validate:
   - Purpose: Checks infrastructure code structure locally to catch typing errors, invalid configurations, or missing fields before execution.
   - Arguments:
     a) path: str - System file directory location housing target configuration parameters.
   - Returns: ToolResult outlining global schema consistency checks alongside explicit error indices.
   - How to call: TerraformTool.validate(path="./infra/dev")

6. fmt:
   - Purpose: Standardizes code structure across all project modules to match proper canonical indentation rules.
   - Arguments:
     a) path: str - Local file mapping folder path to clean.
     b) recursive: bool (default: True) - Traverses nested folder locations when set to true.
   - Returns: ToolResult listing changed file pathways.
   - How to call: TerraformTool.fmt(path="./infra", recursive=True)

7. show:
   - Purpose: Converts binary plan details or live operational tracking components into clean JSON data structures.
   - Arguments:
     a) path: str - Workspace directory string.
     b) plan_file: str (default: "") - Specific execution tracker plan file name string.
   - Returns: ToolResult packaging nested metadata records explaining configuration profiles.
   - How to call: TerraformTool.show(path="./infra/prod", plan_file="outputs/june_deploy.tfplan")

8. output:
   - Purpose: Queries completed state registers to pull active endpoints, keys, or server IP addresses.
   - Arguments:
     a) path: str - Active resource directory tracking location.
     b) name: str (default: "") - Filters the lookup to return a single parameter string when configured.
   - Returns: ToolResult returning single data strings or complete output field map records.
   - How to call: TerraformTool.output(path="./infra/prod", name="load_balancer_dns")

9. state_list:
   - Purpose: Shows all active hardware blocks currently managed by the active project configuration.
   - Arguments:
     a) path: str - System reference directory targeting the infrastructure module.
   - Returns: ToolResult sorting active tracked address labels into linear string lists.
   - How to call: TerraformTool.state_list(path="./infra/prod")

10. state_show:
    - Purpose: Inspects state cache entries to return a detailed property snapshot for a specific managed item.
    - Arguments:
      a) path: str - Workspace location string tracking projects.
      b) resource: str - Fully qualified path identifier pointing to the target infrastructure block.
    - Returns: ToolResult outlining provider status values and cloud resource IDs.
    - How to call: TerraformTool.state_show(path="./infra/prod", resource="aws_instance.web_server[0]")

11. state_rm:
    - Purpose: Removes an infrastructure item from tracking without physically deleting the resource from the cloud provider.
    - Arguments:
      a) path: str - Target configuration repository folder map.
      b) resource: str - Reference address tag pointing to the specific component to stop tracking.
    - Returns: ToolResult reflecting state modifications.
    - How to call: TerraformTool.state_rm(path="./infra/prod", resource="aws_security_group.legacy_firewall")

12. import_resource:
    - Purpose: Connects a manually provisioned cloud resource to a matching configuration block in your codebase.
    - Arguments:
      a) path: str - Directory system pointer holding configuration scripts.
      b) address: str - Target resource address mapping string inside active modules.
      c) id: str - Official identification code provided by the external cloud service host.
    - Returns: ToolResult charting standard state inclusion actions.
    - How to call: TerraformTool.import_resource(path="./infra/prod", address="aws_s3_bucket.assets", id="my-legacy-global-assets-bucket")

13. graph:
    - Purpose: Generates structural code dependency diagrams to analyze orchestration paths and resolve sequencing blocks.
    - Arguments:
      a) path: str - Baseline repository map tracking target modules.
      b) output_file: str (default: "graph.dot") - Local destination path where visual relationship files are written.
    - Returns: ToolResult passing successful generation verification strings.
    - How to call: TerraformTool.graph(path="./infra/prod", output_file="visuals/infra_tree.dot")

14. workspace_list:
    - Purpose: Enumerates separate deployment branches running inside the same baseline code block directory.
    - Arguments:
      a) path: str - Target tracking workspace root directory.
    - Returns: ToolResult revealing all valid tracking labels alongside active focus flags.
    - How to call: TerraformTool.workspace_list(path="./infra/apps")

15. workspace_new:
    - Purpose: Builds isolated tracking states within a single project directory to help segregate environments like staging and production.
    - Arguments:
      a) path: str - System operational baseline code track directory.
      b) name: str - Target workspace alphanumeric identification string.
    - Returns: ToolResult documenting setup status indicators.
    - How to call: TerraformTool.workspace_new(path="./infra/apps", name="staging-environment")

16. workspace_select:
    - Purpose: Switches the active tracking context pointer over to an alternate workspace segment.
    - Arguments:
      a) path: str - Module baseline folder tracking structure locations.
      b) name: str - Target environment segment tag string to swap in.
    - Returns: ToolResult logging workspace activation adjustments.
    - How to call: TerraformTool.workspace_select(path="./infra/apps", name="staging-environment")
    """)
    
    @staticmethod
    def _tf(args: list, cwd: str, timeout: int = 600,
            env_extra: dict = None) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["TF_IN_AUTOMATION"] = "true"
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            ["terraform"] + args,
            cwd=cwd, capture_output=True, text=True,
            timeout=timeout, env=env
        )

    @staticmethod
    def init(path: str, backend_config: dict = None) -> ToolResult:
        try:
            args = ["init", "-no-color"]
            if backend_config:
                for k, v in backend_config.items():
                    args += [f"-backend-config={k}={v}"]
            result = TerraformTool._tf(args, path)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf init failed: {e}")

    @staticmethod
    def plan(path: str, var_file: str = "", vars: dict = None,
             out: str = "tfplan") -> ToolResult:
        try:
            args = ["plan", "-no-color", f"-out={out}"]
            if var_file:
                args += [f"-var-file={var_file}"]
            if vars:
                for k, v in vars.items():
                    args += [f"-var={k}={v}"]
            result = TerraformTool._tf(args, path)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip(), {"plan_file": out})
        except Exception as e:
            return ToolResult(False, f"✗ tf plan failed: {e}")

    @staticmethod
    def apply(path: str, plan_file: str = "",
              var_file: str = "", vars: dict = None,
              auto_approve: bool = False) -> ToolResult:
        try:
            args = ["apply", "-no-color"]
            if auto_approve:
                args.append("-auto-approve")
            if plan_file:
                args.append(plan_file)
            else:
                if var_file:
                    args += [f"-var-file={var_file}"]
                if vars:
                    for k, v in vars.items():
                        args += [f"-var={k}={v}"]
            result = TerraformTool._tf(args, path, timeout=900)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf apply failed: {e}")

    @staticmethod
    def destroy(path: str, var_file: str = "", vars: dict = None,
                auto_approve: bool = False) -> ToolResult:
        try:
            args = ["destroy", "-no-color"]
            if auto_approve:
                args.append("-auto-approve")
            if var_file:
                args += [f"-var-file={var_file}"]
            if vars:
                for k, v in vars.items():
                    args += [f"-var={k}={v}"]
            result = TerraformTool._tf(args, path, timeout=900)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf destroy failed: {e}")

    @staticmethod
    def validate(path: str) -> ToolResult:
        try:
            result = TerraformTool._tf(["validate", "-no-color", "-json"], path)
            output = result.stdout + result.stderr
            try:
                data = json.loads(result.stdout)
                valid = data.get("valid", False)
                return ToolResult(valid,
                                  "✓ Configuration is valid" if valid
                                  else f"✗ Validation failed: {data.get('error_count', 0)} error(s)",
                                  data)
            except Exception:
                return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf validate failed: {e}")

    @staticmethod
    def fmt(path: str, recursive: bool = True) -> ToolResult:
        try:
            args = ["fmt", "-no-color"]
            if recursive:
                args.append("-recursive")
            result = TerraformTool._tf(args, path)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0,
                              output.strip() or "✓ Files formatted")
        except Exception as e:
            return ToolResult(False, f"✗ tf fmt failed: {e}")

    @staticmethod
    def show(path: str, plan_file: str = "") -> ToolResult:
        try:
            args = ["show", "-no-color", "-json"]
            if plan_file:
                args.append(plan_file)
            result = TerraformTool._tf(args, path)
            try:
                data = json.loads(result.stdout)
                return ToolResult(result.returncode == 0,
                                  "✓ Plan/state shown", data)
            except Exception:
                return ToolResult(result.returncode == 0,
                                  result.stdout + result.stderr)
        except Exception as e:
            return ToolResult(False, f"✗ tf show failed: {e}")

    @staticmethod
    def output(path: str, name: str = "") -> ToolResult:
        try:
            args = ["output", "-no-color", "-json"]
            if name:
                args.append(name)
            result = TerraformTool._tf(args, path)
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            try:
                data = json.loads(result.stdout)
                return ToolResult(True, "✓ Outputs retrieved", data)
            except Exception:
                return ToolResult(True, result.stdout.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf output failed: {e}")

    @staticmethod
    def state_list(path: str) -> ToolResult:
        try:
            result = TerraformTool._tf(["state", "list"], path)
            resources = [r for r in result.stdout.strip().splitlines() if r]
            return ToolResult(result.returncode == 0,
                              f"✓ {len(resources)} resources in state", resources)
        except Exception as e:
            return ToolResult(False, f"✗ tf state list failed: {e}")

    @staticmethod
    def state_show(path: str, resource: str) -> ToolResult:
        try:
            result = TerraformTool._tf(["state", "show", resource], path)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf state show failed: {e}")

    @staticmethod
    def state_rm(path: str, resource: str) -> ToolResult:
        try:
            result = TerraformTool._tf(["state", "rm", resource], path)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf state rm failed: {e}")

    @staticmethod
    def import_resource(path: str, address: str, id: str) -> ToolResult:
        try:
            result = TerraformTool._tf(
                ["import", "-no-color", address, id], path
            )
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ tf import failed: {e}")

    @staticmethod
    def graph(path: str, output_file: str = "graph.dot") -> ToolResult:
        try:
            result = TerraformTool._tf(["graph"], path)
            if result.returncode != 0:
                return ToolResult(False, result.stderr.strip())
            Path(output_file).write_text(result.stdout)
            return ToolResult(True, f"✓ Graph saved to '{output_file}'",
                              {"dot_file": output_file})
        except Exception as e:
            return ToolResult(False, f"✗ tf graph failed: {e}")

    @staticmethod
    def workspace_list(path: str) -> ToolResult:
        try:
            result = TerraformTool._tf(["workspace", "list"], path)
            workspaces = [w.strip().lstrip("* ") for w in
                          result.stdout.strip().splitlines() if w.strip()]
            current = next((w.strip().lstrip("*").strip() for w in
                            result.stdout.strip().splitlines() if w.startswith("*")), "default")
            return ToolResult(result.returncode == 0,
                              f"✓ {len(workspaces)} workspaces, current: {current}",
                              {"workspaces": workspaces, "current": current})
        except Exception as e:
            return ToolResult(False, f"✗ workspace list failed: {e}")

    @staticmethod
    def workspace_new(path: str, name: str) -> ToolResult:
        try:
            result = TerraformTool._tf(["workspace", "new", name], path)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ workspace new failed: {e}")

    @staticmethod
    def workspace_select(path: str, name: str) -> ToolResult:
        try:
            result = TerraformTool._tf(["workspace", "select", name], path)
            output = result.stdout + result.stderr
            return ToolResult(result.returncode == 0, output.strip())
        except Exception as e:
            return ToolResult(False, f"✗ workspace select failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 10. MonitoringTool
# ══════════════════════════════════════════════════════════════════════════════
class MonitoringTool:
    name = "monitoring"
    description = "System & app monitoring: CPU, memory, disk, network, processes, logs, alerts"
    use = (
        """
Name of Tool:- MonitoringTool,

Purpose of Tool:- 
The MonitoringTool provides comprehensive system and application monitoring capabilities for servers, containers, and applications. 
It includes real-time metrics for CPU, memory, disk, network I/O, running processes, GPU usage, open ports, service health checks, log monitoring and parsing, file change watching, and alert notifications via Slack, Telegram, or custom webhooks. 
Built on top of psutil, GPUtil, watchdog, and requests, this tool enables proactive system observation, troubleshooting, resource tracking, and automated alerting — essential for DevOps, SRE, infrastructure monitoring, and agentic observability workflows.

Methods:-
- get_cpu_usage: Retrieves current CPU usage, core count, and frequency.
- get_memory_info: Returns detailed virtual memory and swap statistics.
- get_disk_usage: Reports disk space usage and I/O statistics for a given path.
- get_network_io: Shows network bytes sent/received, packets, and errors (per interface or total).
- get_process_list: Lists running processes sorted by CPU, memory, etc.
- kill_process: Terminates a process by PID.
- get_gpu_info: Retrieves GPU load, memory, temperature, and driver details.
- watch_file_changes: Sets up real-time file/directory change monitoring.
- get_open_ports: Lists listening network ports and associated processes.
- check_service_health: Performs HTTP health checks on services/endpoints.
- send_alert: Sends notifications via Slack, Telegram, or webhook.
- get_system_info: Returns comprehensive system and hardware information.
- tail_log_file: Tails the end of a log file (with optional follow).
- parse_log_file: Parses log files with pattern matching, time filtering, and error/warning counting.

How to use Tool Methods:-

1. get_cpu_usage:
   - Purpose: Gets current CPU utilization percentage, core counts, and CPU frequency.
   - Arguments:
     a) interval: float (default: 1.0) - Sampling interval in seconds (0 for non-blocking).
     b) percpu: bool (default: False) - Return per-core usage instead of average.
   - Returns: Usage percent, logical/physical CPU count, and current frequency.
   - How to call: MonitoringTool.get_cpu_usage(interval=0.5, percpu=True)

2. get_memory_info:
   - Purpose: Returns detailed RAM and swap memory statistics in GB and percentages.
   - Arguments: None
   - Returns: Total, available, used memory, percentages, and swap info.
   - How to call: MonitoringTool.get_memory_info()

3. get_disk_usage:
   - Purpose: Reports disk space usage and I/O counters for a mount point.
   - Arguments:
     a) path: str (default: "/") - Filesystem path to check.
   - Returns: Total/used/free space in GB, usage percent, and read/write bytes.
   - How to call: MonitoringTool.get_disk_usage(path="/data")

4. get_network_io:
   - Purpose: Monitors network traffic statistics.
   - Arguments:
     a) interface: str (default: "") - Specific network interface (e.g., "eth0"). Empty = aggregate.
   - Returns: Bytes sent/received (MB), packets, errors, and drops.
   - How to call: MonitoringTool.get_network_io(interface="eth0")

5. get_process_list:
   - Purpose: Lists running processes with resource usage.
   - Arguments:
     a) sort_by: str (default: "cpu") - Sort by "cpu", "memory", "pid", or "name".
     b) limit: int (default: 20) - Number of top processes to return.
   - Returns: List of processes with PID, name, CPU%, memory%, etc.
   - How to call: MonitoringTool.get_process_list(sort_by="memory", limit=15)

6. kill_process:
   - Purpose: Terminates a process gracefully or forcefully.
   - Arguments:
     a) pid: int - Process ID.
     b) signal: int (default: 15) - 15 = SIGTERM (graceful), 9 = SIGKILL (force).
   - How to call: MonitoringTool.kill_process(pid=12345, signal=9)

7. get_gpu_info:
   - Purpose: Retrieves information about installed NVIDIA GPUs (requires GPUtil).
   - Arguments: None
   - Returns: List of GPUs with load, memory usage, temperature, etc.
   - How to call: MonitoringTool.get_gpu_info()

8. watch_file_changes:
   - Purpose: Starts a background observer for file/directory changes (create, modify, delete, etc.).
   - Arguments:
     a) path: str - Directory or file to watch.
     b) callback: callable - Function that receives (event_type, src_path).
     c) recursive: bool (default: True) - Watch subdirectories.
   - Returns: Observer object (must be managed/stopped by caller).
   - How to call: MonitoringTool.watch_file_changes(path="/var/log", callback=my_callback_function)

9. get_open_ports:
   - Purpose: Lists all listening TCP/UDP ports and associated processes.
   - Arguments: None
   - Returns: List of open ports with PID and process name.
   - How to call: MonitoringTool.get_open_ports()

10. check_service_health:
    - Purpose: Performs an HTTP health check on a service/URL.
    - Arguments:
      a) url: str - Full URL to check.
      b) timeout: int (default: 10) - Request timeout in seconds.
      c) expected_status: int (default: 200).
    - Returns: Health status, response time, and details.
    - How to call: MonitoringTool.check_service_health(url="https://api.example.com/health", expected_status=200)

11. send_alert:
    - Purpose: Sends monitoring alerts through configured channels.
    - Arguments:
      a) title: str - Alert title.
      b) message: str - Alert body.
      c) channel: str (default: "slack") - "slack", "telegram", or "webhook".
      d) cred_key: str (default: "alerts") - Credential store key.
    - Credential requirements vary by channel (webhook URL, bot token + chat ID, etc.).
    - How to call: MonitoringTool.send_alert(title="High CPU", message="CPU usage exceeded 90%", channel="slack")

12. get_system_info:
    - Purpose: Returns detailed information about the operating system and hardware.
    - Arguments: None
    - Returns: Hostname, OS version, uptime, CPU/RAM/disk totals, etc.
    - How to call: MonitoringTool.get_system_info()

13. tail_log_file:
    - Purpose: Reads the last N lines of a log file, with optional follow mode and pattern filtering.
    - Arguments:
      a) path: str - Path to log file.
      b) lines: int (default: 100)
      c) follow: bool (default: False) - Start background tail.
      d) pattern: str (default: "") - Regex filter.
    - How to call: MonitoringTool.tail_log_file(path="/var/log/app.log", lines=50, pattern="ERROR")

14. parse_log_file:
    - Purpose: Parses a log file with optional regex filtering, time range, and error/warning counting.
    - Arguments:
      a) path: str - Log file path.
      b) pattern: str (default: "") - Regex to match lines.
      c) time_range: tuple (default: None) - (start, end) string timestamps.
    - Returns: Summary with matched lines, error/warning counts, and sample lines.
    - How to call: MonitoringTool.parse_log_file(path="/var/log/app.log", pattern="ERROR|Exception")
""")
    
    @staticmethod
    def get_cpu_usage(interval: float = 1.0,
                      percpu: bool = False) -> ToolResult:
        try:
            import psutil
            usage = psutil.cpu_percent(interval=interval, percpu=percpu)
            freq = psutil.cpu_freq()
            data = {
                "usage_percent": usage,
                "logical_cpus": psutil.cpu_count(logical=True),
                "physical_cpus": psutil.cpu_count(logical=False),
                "frequency_mhz": round(freq.current, 1) if freq else None,
            }
            label = f"{usage}%" if not percpu else f"avg {sum(usage)/len(usage):.1f}%"
            return ToolResult(True, f"✓ CPU usage: {label}", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_cpu_usage failed: {e}")

    @staticmethod
    def get_memory_info() -> ToolResult:
        try:
            import psutil
            vm = psutil.virtual_memory()
            swap = psutil.swap_memory()
            data = {
                "total_gb": round(vm.total / 1e9, 2),
                "available_gb": round(vm.available / 1e9, 2),
                "used_gb": round(vm.used / 1e9, 2),
                "percent": vm.percent,
                "swap_total_gb": round(swap.total / 1e9, 2),
                "swap_used_gb": round(swap.used / 1e9, 2),
                "swap_percent": swap.percent,
            }
            return ToolResult(True,
                              f"✓ Memory: {vm.percent}% used ({data['used_gb']}GB/{data['total_gb']}GB)",
                              data)
        except Exception as e:
            return ToolResult(False, f"✗ get_memory_info failed: {e}")

    @staticmethod
    def get_disk_usage(path: str = "/") -> ToolResult:
        try:
            import psutil
            usage = psutil.disk_usage(path)
            io = psutil.disk_io_counters()
            data = {
                "path": path,
                "total_gb": round(usage.total / 1e9, 2),
                "used_gb": round(usage.used / 1e9, 2),
                "free_gb": round(usage.free / 1e9, 2),
                "percent": usage.percent,
                "read_mb": round(io.read_bytes / 1e6, 1) if io else None,
                "write_mb": round(io.write_bytes / 1e6, 1) if io else None,
            }
            return ToolResult(True,
                              f"✓ Disk '{path}': {usage.percent}% used ({data['used_gb']}GB/{data['total_gb']}GB)",
                              data)
        except Exception as e:
            return ToolResult(False, f"✗ get_disk_usage failed: {e}")

    @staticmethod
    def get_network_io(interface: str = "") -> ToolResult:
        try:
            import psutil
            if interface:
                counters = psutil.net_io_counters(pernic=True)
                if interface not in counters:
                    return ToolResult(False, f"✗ Interface '{interface}' not found")
                io = counters[interface]
            else:
                io = psutil.net_io_counters()
            data = {
                "bytes_sent_mb": round(io.bytes_sent / 1e6, 2),
                "bytes_recv_mb": round(io.bytes_recv / 1e6, 2),
                "packets_sent": io.packets_sent,
                "packets_recv": io.packets_recv,
                "errin": io.errin,
                "errout": io.errout,
                "dropin": io.dropin,
                "dropout": io.dropout,
            }
            return ToolResult(True,
                              f"✓ Network I/O: sent {data['bytes_sent_mb']}MB, recv {data['bytes_recv_mb']}MB",
                              data)
        except Exception as e:
            return ToolResult(False, f"✗ get_network_io failed: {e}")

    @staticmethod
    def get_process_list(sort_by: str = "cpu",
                         limit: int = 20) -> ToolResult:
        try:
            import psutil
            procs = []
            for p in psutil.process_iter(
                    ["pid", "name", "cpu_percent", "memory_percent",
                     "status", "username", "create_time"]):
                try:
                    info = p.info
                    info["cpu_percent"] = p.cpu_percent(interval=0.1)
                    procs.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            key_map = {
                "cpu": "cpu_percent",
                "memory": "memory_percent",
                "pid": "pid",
                "name": "name",
            }
            sort_key = key_map.get(sort_by, "cpu_percent")
            procs.sort(key=lambda x: x.get(sort_key, 0) or 0, reverse=True)
            return ToolResult(True, f"✓ {len(procs)} processes (top {limit} by {sort_by})",
                              procs[:limit])
        except Exception as e:
            return ToolResult(False, f"✗ get_process_list failed: {e}")

    @staticmethod
    def kill_process(pid: int, signal: int = 15) -> ToolResult:
        try:
            import psutil
            p = psutil.Process(pid)
            name = p.name()
            if signal == 9:
                p.kill()
            else:
                p.terminate()
            return ToolResult(True, f"✓ Process {pid} ({name}) killed with signal {signal}")
        except Exception as e:
            return ToolResult(False, f"✗ kill_process failed: {e}")

    @staticmethod
    def get_gpu_info() -> ToolResult:
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if not gpus:
                return ToolResult(True, "✓ No GPUs found", [])
            data = [
                {"id": g.id, "name": g.name,
                 "load_percent": round(g.load * 100, 1),
                 "memory_used_mb": g.memoryUsed,
                 "memory_total_mb": g.memoryTotal,
                 "memory_percent": round(g.memoryUsed / g.memoryTotal * 100, 1) if g.memoryTotal else 0,
                 "temperature_c": g.temperature,
                 "driver": g.driver}
                for g in gpus
            ]
            return ToolResult(True, f"✓ {len(data)} GPU(s) found", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_gpu_info failed: {e}")

    @staticmethod
    def watch_file_changes(path: str, callback,
                           recursive: bool = True) -> ToolResult:
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            class _Handler(FileSystemEventHandler):
                def on_any_event(self, event):
                    if not event.is_directory:
                        try:
                            callback(event.event_type, event.src_path)
                        except Exception:
                            pass

            observer = Observer()
            observer.schedule(_Handler(), path, recursive=recursive)
            observer.start()
            return ToolResult(True, f"✓ Watching '{path}' for changes (recursive={recursive})",
                              {"observer": observer})
        except Exception as e:
            return ToolResult(False, f"✗ watch_file_changes failed: {e}")

    @staticmethod
    def get_open_ports() -> ToolResult:
        try:
            import psutil
            connections = psutil.net_connections(kind="inet")
            ports = []
            for conn in connections:
                if conn.status == "LISTEN":
                    try:
                        proc = psutil.Process(conn.pid) if conn.pid else None
                        proc_name = proc.name() if proc else "unknown"
                    except Exception:
                        proc_name = "unknown"
                    ports.append({
                        "port": conn.laddr.port,
                        "address": conn.laddr.ip,
                        "pid": conn.pid,
                        "process": proc_name,
                        "family": "IPv4" if conn.family == 2 else "IPv6",
                    })
            ports.sort(key=lambda x: x["port"])
            return ToolResult(True, f"✓ {len(ports)} open/listening ports", ports)
        except Exception as e:
            return ToolResult(False, f"✗ get_open_ports failed: {e}")

    @staticmethod
    def check_service_health(url: str, timeout: int = 10,
                              expected_status: int = 200) -> ToolResult:
        try:
            import requests
            start = time.time()
            r = requests.get(url, timeout=timeout, allow_redirects=True)
            elapsed_ms = round((time.time() - start) * 1000, 1)
            healthy = r.status_code == expected_status
            data = {
                "url": url,
                "status_code": r.status_code,
                "expected_status": expected_status,
                "healthy": healthy,
                "response_ms": elapsed_ms,
                "content_type": r.headers.get("content-type", ""),
            }
            return ToolResult(
                healthy,
                f"✓ {url} → {r.status_code} ({elapsed_ms}ms)" if healthy
                else f"✗ {url} → {r.status_code} (expected {expected_status})",
                data
            )
        except Exception as e:
            return ToolResult(False, f"✗ check_service_health failed: {url} → {e}",
                              {"url": url, "healthy": False, "error": str(e)})

    @staticmethod
    def send_alert(title: str, message: str,
                   channel: str = "slack",
                   cred_key: str = "alerts") -> ToolResult:
        try:
            import requests
            c = CredStore.load(cred_key)
            if channel == "slack":
                webhook_url = c.get("slack_webhook", "")
                if not webhook_url:
                    return ToolResult(False, "✗ No slack_webhook in alerts credentials")
                payload = {
                    "text": f"*🚨 {title}*\n{message}",
                    "username": "NPM Agent Monitor",
                }
                r = requests.post(webhook_url, json=payload, timeout=10)
                return ToolResult(r.status_code == 200,
                                  "✓ Slack alert sent" if r.status_code == 200
                                  else f"✗ Slack alert failed: {r.status_code}")
            elif channel == "telegram":
                bot_token = c.get("telegram_bot_token", "")
                chat_id = c.get("telegram_chat_id", "")
                if not bot_token or not chat_id:
                    return ToolResult(False, "✗ telegram_bot_token and telegram_chat_id required")
                r = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": f"🚨 {title}\n\n{message}",
                          "parse_mode": "Markdown"},
                    timeout=10
                )
                return ToolResult(r.ok, "✓ Telegram alert sent" if r.ok else f"✗ {r.text}")
            elif channel == "webhook":
                webhook_url = c.get("webhook_url", "")
                if not webhook_url:
                    return ToolResult(False, "✗ No webhook_url in alerts credentials")
                r = requests.post(webhook_url, json={"title": title, "message": message,
                                                      "timestamp": datetime.now().isoformat()},
                                  timeout=10)
                return ToolResult(r.ok, "✓ Webhook alert sent" if r.ok else f"✗ {r.text}")
            else:
                return ToolResult(False, f"✗ Unknown alert channel: {channel}")
        except Exception as e:
            return ToolResult(False, f"✗ send_alert failed: {e}")

    @staticmethod
    def get_system_info() -> ToolResult:
        try:
            import psutil
            import platform
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime_seconds = (datetime.now() - boot_time).total_seconds()
            data = {
                "hostname": platform.node(),
                "os": platform.system(),
                "os_version": platform.version(),
                "platform": platform.platform(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "boot_time": boot_time.isoformat(),
                "uptime_hours": round(uptime_seconds / 3600, 2),
                "cpu_count_logical": psutil.cpu_count(logical=True),
                "cpu_count_physical": psutil.cpu_count(logical=False),
                "ram_total_gb": round(psutil.virtual_memory().total / 1e9, 2),
                "disk_total_gb": round(psutil.disk_usage("/").total / 1e9, 2),
            }
            return ToolResult(True, f"✓ System info: {data['hostname']} ({data['os']})", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_system_info failed: {e}")

    @staticmethod
    def tail_log_file(path: str, lines: int = 100,
                      follow: bool = False,
                      pattern: str = "") -> ToolResult:
        try:
            log_path = Path(path)
            if not log_path.exists():
                return ToolResult(False, f"✗ Log file not found: {path}")
            # Read last N lines efficiently
            with open(path, "rb") as fh:
                fh.seek(0, 2)
                file_size = fh.tell()
                block_size = min(8192 * 10, file_size)
                fh.seek(max(0, file_size - block_size))
                content = fh.read().decode(errors="replace")
            all_lines = content.splitlines()
            last_lines = all_lines[-lines:]
            # Apply pattern filter if given
            if pattern:
                try:
                    regex = re.compile(pattern, re.IGNORECASE)
                    last_lines = [l for l in last_lines if regex.search(l)]
                except re.error as re_err:
                    return ToolResult(False, f"✗ Invalid pattern: {re_err}")
            if follow:
                # Non-blocking tail follow in background thread, return current content
                def _follow_thread():
                    with open(path, "r", errors="replace") as fh:
                        fh.seek(0, 2)
                        while True:
                            line = fh.readline()
                            if line:
                                print(line.rstrip())
                            else:
                                time.sleep(0.5)
                t = threading.Thread(target=_follow_thread, daemon=True)
                t.start()
            return ToolResult(True,
                              f"✓ Last {len(last_lines)} lines of '{path}'",
                              "\n".join(last_lines))
        except Exception as e:
            return ToolResult(False, f"✗ tail_log_file failed: {e}")

    @staticmethod
    def parse_log_file(path: str, pattern: str = "",
                       time_range: tuple = None) -> ToolResult:
        try:
            log_path = Path(path)
            if not log_path.exists():
                return ToolResult(False, f"✗ Log file not found: {path}")
            with open(path, "r", errors="replace") as fh:
                all_lines = fh.readlines()

            regex = re.compile(pattern, re.IGNORECASE) if pattern else None
            # Common timestamp patterns
            ts_patterns = [
                re.compile(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})"),
                re.compile(r"(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2})"),
            ]
            matched = []
            errors = 0
            warnings = 0
            for line in all_lines:
                line = line.rstrip()
                if not line:
                    continue
                if regex and not regex.search(line):
                    continue
                if time_range:
                    ts = None
                    for tsp in ts_patterns:
                        m = tsp.search(line)
                        if m:
                            ts = m.group(1)
                            break
                    # Simple string comparison for time range filtering
                    if ts and time_range:
                        if not (str(time_range[0]) <= ts <= str(time_range[1])):
                            continue
                matched.append(line)
                lower = line.lower()
                if "error" in lower or "exception" in lower or "critical" in lower:
                    errors += 1
                elif "warn" in lower:
                    warnings += 1

            summary = {
                "total_lines": len(all_lines),
                "matched_lines": len(matched),
                "errors": errors,
                "warnings": warnings,
                "lines": matched[:500],
            }
            return ToolResult(True,
                              f"✓ Parsed '{path}': {len(matched)} matches, {errors} errors, {warnings} warnings",
                              summary)
        except Exception as e:
            return ToolResult(False, f"✗ parse_log_file failed: {e}")


# ── Tool registry ─────────────────────────────────────────────────────────────
CLOUD_DEVOPS_TOOLS = {
    "aws_s3":       AWSS3Tool,
    "aws_lambda":   AWSLambdaTool,
    "aws_ecs":      AWSECSTool,
    "cloudflare":   CloudflareTool,
    "vercel":       VercelTool,
    "netlify":      NetlifyTool,
    "railway":      RailwayTool,
    "kubernetes":   KubernetesTool,
    "terraform":    TerraformTool,
    "monitoring":   MonitoringTool,
}
