from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="openai/gpt-oss-20b",
    local_dir="./gpt-oss-20b",
    force_download=False   # デフォルト。途中から再開される
)

print("ダウンロード先:", local_dir)
