import os
import json
import subprocess
import yt_dlp
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

REPO_RAW_BASE = "https://raw.githubusercontent.com/Norevio/halloween-prank-data/main"
CDN_BASE = "https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main"

PINS = {
    "video_calls": {
        "ghosts": {
            "name": "Ghosts",
            "urls": [
                "https://www.pinterest.com/pin/987555024541801925/",
                "https://www.pinterest.com/pin/798614946463728775/",
                "https://www.pinterest.com/pin/798614946465262043/",
                "https://www.pinterest.com/pin/610026712064317128/"
            ]
        },
        "undead": {
            "name": "Undead",
            "urls": [
                "https://www.pinterest.com/pin/798614946465320218/",
                "https://www.pinterest.com/pin/798614946465340507/",
                "https://www.pinterest.com/pin/798614946465490737/",
                "https://www.pinterest.com/pin/830914200039141192/"
            ]
        },
        "classic": {
            "name": "Classic",
            "urls": [
                "https://www.pinterest.com/pin/922815779898658740/",
                "https://www.pinterest.com/pin/999306604815084767/",
                "https://www.pinterest.com/pin/795237246739896329/",
                "https://www.pinterest.com/pin/953637289856821362/"
            ]
        },
        "alien": {
            "name": "Alien",
            "urls": [
                "https://www.pinterest.com/pin/902408844104674721/",
                "https://www.pinterest.com/pin/353954851985634751/",
                "https://www.pinterest.com/pin/1125899975622693093/",
                "https://www.pinterest.com/pin/663084745154507841/"
            ]
        },
        "temptress": {
            "name": "Temptress",
            "urls": [
                "https://www.pinterest.com/pin/954129871065872723/",
                "https://www.pinterest.com/pin/754001162650408784/",
                "https://www.pinterest.com/pin/435512226489274232/",
                "https://www.pinterest.com/pin/734649758001041595/",
                "https://www.pinterest.com/pin/8092474326985742/",
                "https://www.pinterest.com/pin/954129871065872779/"
            ]
        },
        "jumpscare": {
            "name": "Jumpscare",
            "urls": [
                "https://www.pinterest.com/pin/609534130805285912/",
                "https://www.pinterest.com/pin/883831495628900568/",
                "https://www.pinterest.com/pin/798614946468401625/",
                "https://www.pinterest.com/pin/910641987207153531/"
            ]
        }
    },
    "explore": [
        "https://www.pinterest.com/pin/728035096001886620/",
        "https://www.pinterest.com/pin/742601426087070338/",
        "https://www.pinterest.com/pin/850124867228216905/",
        "https://www.pinterest.com/pin/668643875964605345/",
        "https://www.pinterest.com/pin/836965912039881820/",
        "https://www.pinterest.com/pin/1108800370791640334/",
        "https://www.pinterest.com/pin/1044483338589052188/",
        "https://www.pinterest.com/pin/999447342312082882/",
        "https://www.pinterest.com/pin/1059471881119754729/"
    ]
}

def generate_thumbnail(video_path, thumb_path):
    cmd = [
        "ffmpeg", "-y", "-ss", "00:00:01", "-i", video_path,
        "-vframes", "1", "-q:v", "2", thumb_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        cmd = [
            "ffmpeg", "-y", "-ss", "00:00:00", "-i", video_path,
            "-vframes", "1", "-q:v", "2", thumb_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_video_info_ffprobe(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return round(float(res.stdout.strip()), 1)
    except:
        return 0.0

def process_item(url, target_dir, file_prefix):
    os.makedirs(target_dir, exist_ok=True)
    video_path = os.path.join(target_dir, f"{file_prefix}.mp4")
    thumb_path = os.path.join(target_dir, f"{file_prefix}_thumb.jpg")
    img_path = os.path.join(target_dir, f"{file_prefix}.jpg")

    # If video already exists, just return info
    if os.path.exists(video_path) and os.path.getsize(video_path) > 1000:
        if not os.path.exists(thumb_path):
            generate_thumbnail(video_path, thumb_path)
        dur = get_video_info_ffprobe(video_path)
        return {
            "type": "video",
            "file_path": video_path,
            "thumb_path": thumb_path,
            "title": file_prefix.replace("_", " ").title(),
            "duration": dur
        }

    # Otherwise, download using yt-dlp with fallback formats
    print(f"Downloading/Fixing {file_prefix} from {url}...")
    ydl_opts = {
        'format': 'best[protocol=https]/bestvideo+bestaudio/best',
        'outtmpl': os.path.join(target_dir, f"{file_prefix}.%(ext)s"),
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"yt-dlp error for {url}: {e}")

    # Check for downloaded video file
    actual_video = None
    for ext in ['mp4', 'mkv', 'webm', 'mov']:
        p = os.path.join(target_dir, f"{file_prefix}.{ext}")
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            actual_video = p
            break

    if actual_video:
        if actual_video != video_path:
            subprocess.run(["ffmpeg", "-y", "-i", actual_video, "-c", "copy", video_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.remove(actual_video)
        # remove leftover jpg if any was placeholder
        if os.path.exists(img_path):
            os.remove(img_path)
        generate_thumbnail(video_path, thumb_path)
        dur = get_video_info_ffprobe(video_path)
        return {
            "type": "video",
            "file_path": video_path,
            "thumb_path": thumb_path,
            "title": file_prefix.replace("_", " ").title(),
            "duration": dur
        }

    # If really only image:
    if os.path.exists(img_path) and os.path.getsize(img_path) > 1000:
        return {
            "type": "image",
            "file_path": img_path,
            "thumb_path": img_path,
            "title": file_prefix.replace("_", " ").title(),
            "duration": 0.0
        }

    # Fetch image from pinterest page
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        og_img = soup.find('meta', property='og:image')
        if og_img and og_img.get('content'):
            img_url = og_img['content']
            with open(img_path, 'wb') as f:
                f.write(requests.get(img_url, headers=headers, timeout=10).content)
            return {
                "type": "image",
                "file_path": img_path,
                "thumb_path": img_path,
                "title": file_prefix.replace("_", " ").title(),
                "duration": 0.0
            }
    except Exception as e:
        print(f"Error fetching image: {e}")

    return None

def main():
    all_data = {
        "version": "1.0.0",
        "last_updated": "2026-10-27",
        "base_url": REPO_RAW_BASE,
        "cdn_base_url": CDN_BASE,
        "video_calls": [],
        "explore": []
    }

    print("--- FIXING & COMPLETING ALL ITEMS ---")
    for cat_id, cat_info in PINS["video_calls"].items():
        cat_name = cat_info["name"]
        cat_dir = os.path.join(DATA_DIR, "video_calls", cat_id)
        cat_items = []
        for idx, url in enumerate(cat_info["urls"], start=1):
            prefix = f"{cat_id}_{idx:02d}"
            res = process_item(url, cat_dir, prefix)
            if res:
                rel_media = os.path.relpath(res["file_path"], BASE_DIR)
                rel_thumb = os.path.relpath(res["thumb_path"], BASE_DIR)
                cat_items.append({
                    "id": prefix,
                    "title": f"{cat_name} {idx:02d}",
                    "media_type": res["type"],
                    "video_url": f"{REPO_RAW_BASE}/{rel_media}",
                    "thumbnail_url": f"{REPO_RAW_BASE}/{rel_thumb}",
                    "cdn_video_url": f"{CDN_BASE}/{rel_media}",
                    "cdn_thumbnail_url": f"{CDN_BASE}/{rel_thumb}",
                    "relative_path": rel_media,
                    "relative_thumb_path": rel_thumb,
                    "duration": res["duration"],
                    "source_url": url
                })
        all_data["video_calls"].append({
            "category_id": cat_id,
            "category_name": cat_name,
            "count": len(cat_items),
            "items": cat_items
        })

    explore_dir = os.path.join(DATA_DIR, "explore")
    explore_items = []
    for idx, url in enumerate(PINS["explore"], start=1):
        prefix = f"explore_{idx:02d}"
        res = process_item(url, explore_dir, prefix)
        if res:
            rel_media = os.path.relpath(res["file_path"], BASE_DIR)
            rel_thumb = os.path.relpath(res["thumb_path"], BASE_DIR)
            explore_items.append({
                "id": prefix,
                "title": f"Explore {idx:02d}",
                "media_type": res["type"],
                "video_url": f"{REPO_RAW_BASE}/{rel_media}",
                "thumbnail_url": f"{REPO_RAW_BASE}/{rel_thumb}",
                "cdn_video_url": f"{CDN_BASE}/{rel_media}",
                "cdn_thumbnail_url": f"{CDN_BASE}/{rel_thumb}",
                "relative_path": rel_media,
                "relative_thumb_path": rel_thumb,
                "duration": res["duration"],
                "source_url": url
            })
    all_data["explore"] = explore_items

    # Write configs
    with open(os.path.join(BASE_DIR, "data.json"), "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    with open(os.path.join(BASE_DIR, "video_calls.json"), "w", encoding="utf-8") as f:
        json.dump({
            "version": all_data["version"],
            "last_updated": all_data["last_updated"],
            "base_url": REPO_RAW_BASE,
            "cdn_base_url": CDN_BASE,
            "categories": all_data["video_calls"]
        }, f, ensure_ascii=False, indent=2)

    with open(os.path.join(BASE_DIR, "explore.json"), "w", encoding="utf-8") as f:
        json.dump({
            "version": all_data["version"],
            "last_updated": all_data["last_updated"],
            "base_url": REPO_RAW_BASE,
            "cdn_base_url": CDN_BASE,
            "total": len(all_data["explore"]),
            "items": all_data["explore"]
        }, f, ensure_ascii=False, indent=2)

    print("\n[ALL FINISHED] data.json, video_calls.json, explore.json updated.")

if __name__ == "__main__":
    main()
