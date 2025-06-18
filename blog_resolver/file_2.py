async def copy_folder_from_github(
    src_owner: str,
    src_repo: str,
    src_folder: str,
    dst_owner: str,
    dst_repo: str,
    dst_branch: str,
    github_token: str
):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    # 1. List files in the source folder
    url = f"https://api.github.com/repos/{src_owner}/{src_repo}/contents/{src_folder}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        files = resp.json()
        for file in files:
            if file["type"] == "file":
                # 2. Download file content (raw)
                file_resp = await client.get(file["download_url"])
                file_resp.raise_for_status()
                content = file_resp.content
                # 3. Create file in destination repo
                dst_path = file["name"]  # or f"{src_folder}/{file['name']}" for subfolders
                create_url = f"https://api.github.com/repos/{dst_owner}/{dst_repo}/contents/{dst_path}"
                payload = {
                    "message": f"Add {dst_path} from template",
                    "content": base64.b64encode(content).decode(),
                    "branch": dst_branch,
                }
                put_resp = await client.put(create_url, headers=headers, json=payload)
                put_resp.raise_for_status()
