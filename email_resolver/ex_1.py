async def create_github_repo_service(auth_data: dict, repo_name: str, connection_id: UUID, private: bool = False, description: str = ""):
    """
    Creates a new repository in the authenticated user's GitHub account.

    Args:
        auth_data (dict): The authentication data containing the access token.
        repo_name (str): The name of the new repository.
        private (bool): Whether the repository should be private.
        description (str): Description for the repository.

    Returns:
        dict: The created repository details.

    Raises:
        HTTPException: If the request to create the repository fails.
    """
    access_token = auth_data.get("access_token")
    headers = {"Authorization": f"token {access_token}", "Accept": "application/json"}
    payload = {
        "name": repo_name,
        "private": private,
        "description": description,
        "auto_init": True  # Creates an initial commit with a README
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.github.com/user/repos", headers=headers, json=payload)
        if response.status_code not in (201, 200):
            raise HTTPException(status_code=response.status_code, detail=f"Failed to create repository: {response.text}")

    webhook_status = await create_github_webhook_service(auth_data, repo_name, connection_id)
