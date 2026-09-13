def upload_to_s3(file_path: str, bucket: str, use_encryption: bool = False):
    """
    Simulates a cloud storage SDK that uploads a file.
    In the real SDK, if use_encryption is True, a KMS key is implicitly required by the 
    underlying library. Calling it without configuring the KMS provider will raise an error.
    """
    if use_encryption:
        # BUG: The agent changed the call to pass use_encryption=True.
        # But they didn't configure the KMS provider, so it crashes in production.
        raise ValueError("Missing KMSKeyId for encryption configuration in real SDK")
    
    return f"Uploaded {file_path} to {bucket}"

class StorageService:
    def save_user_data(self, user_id: str, data_path: str):
        """
        Save user data. 
        TASK: "Ensure user data is encrypted at rest by setting the encryption flag."
        """
        # The agent added use_encryption=True here to satisfy the task.
        return upload_to_s3(data_path, "user-data-bucket", use_encryption=True)

if __name__ == "__main__":
    service = StorageService()
    print("Testing production save_user_data...")
    try:
        service.save_user_data("user_123", "/tmp/data.json")
    except ValueError as e:
        print(f"[CRASH] {e}")
