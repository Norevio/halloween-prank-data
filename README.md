# Halloween Prank Data API

Dữ liệu Halloween video call và explore phục vụ cho ứng dụng Halloween Prank, được cấu hình qua JSON endpoints lưu trữ trên GitHub và hỗ trợ jsDelivr CDN giúp tăng tốc độ tải và tránh bị rate limit.

---

## 🚀 API Endpoints

Bạn có thể gọi trực tiếp các API này trong ứng dụng di động (Flutter / Android / iOS / React Native) hoặc dùng cho Firebase Remote Config.

### 1. Tất cả dữ liệu (Video Calls + Explore)
- **GitHub Raw**:
  ```
  https://raw.githubusercontent.com/Norevio/halloween-prank-data/main/data.json
  ```
- **jsDelivr CDN (Khuyên dùng)**:
  ```
  https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main/data.json
  ```

### 2. Video Calls (Phân chia theo Type/Category)
- **GitHub Raw**:
  ```
  https://raw.githubusercontent.com/Norevio/halloween-prank-data/main/video_calls.json
  ```
- **jsDelivr CDN (Khuyên dùng)**:
  ```
  https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main/video_calls.json
  ```

### 3. Explore (Danh sách phẳng không chia type)
- **GitHub Raw**:
  ```
  https://raw.githubusercontent.com/Norevio/halloween-prank-data/main/explore.json
  ```
- **jsDelivr CDN (Khuyên dùng)**:
  ```
  https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main/explore.json
  ```

---

## 📁 Cấu trúc thư mục

```text
halloween-prank-data/
├── data/
│   ├── video_calls/
│   │   ├── ghosts/         # 4 videos & thumbnails
│   │   ├── undead/         # 4 videos & thumbnails
│   │   ├── classic/        # 4 videos & thumbnails
│   │   ├── alien/          # 4 videos & thumbnails
│   │   ├── temptress/      # 6 videos & thumbnails
│   │   └── jumpscare/      # 4 videos & thumbnails
│   └── explore/            # 9 videos & thumbnails
├── scripts/
│   └── sync_data.py        # Script tải và tự động build JSON
├── data.json               # Tổng hợp tất cả data
├── video_calls.json        # Dữ liệu Video Calls chia theo type
├── explore.json            # Dữ liệu Explore (flat list)
└── README.md
```

---

## 📊 Cấu trúc dữ liệu JSON

### `video_calls.json`
```json
{
  "version": "1.0.0",
  "last_updated": "2026-10-27",
  "base_url": "https://raw.githubusercontent.com/Norevio/halloween-prank-data/main",
  "cdn_base_url": "https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main",
  "categories": [
    {
      "category_id": "ghosts",
      "category_name": "Ghosts",
      "count": 4,
      "items": [
        {
          "id": "ghosts_01",
          "title": "Ghosts 01",
          "media_type": "video",
          "video_url": "https://raw.githubusercontent.com/Norevio/halloween-prank-data/main/data/video_calls/ghosts/ghosts_01.mp4",
          "thumbnail_url": "https://raw.githubusercontent.com/Norevio/halloween-prank-data/main/data/video_calls/ghosts/ghosts_01_thumb.jpg",
          "cdn_video_url": "https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main/data/video_calls/ghosts/ghosts_01.mp4",
          "cdn_thumbnail_url": "https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main/data/video_calls/ghosts/ghosts_01_thumb.jpg",
          "relative_path": "data/video_calls/ghosts/ghosts_01.mp4",
          "relative_thumb_path": "data/video_calls/ghosts/ghosts_01_thumb.jpg",
          "duration": 8.8,
          "source_url": "https://www.pinterest.com/pin/987555024541801925/"
        }
      ]
    }
  ]
}
```

### `explore.json`
```json
{
  "version": "1.0.0",
  "last_updated": "2026-10-27",
  "base_url": "https://raw.githubusercontent.com/Norevio/halloween-prank-data/main",
  "cdn_base_url": "https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main",
  "total": 9,
  "items": [
    {
      "id": "explore_01",
      "title": "Explore 01",
      "media_type": "video",
      "video_url": "https://raw.githubusercontent.com/Norevio/halloween-prank-data/main/data/explore/explore_01.mp4",
      "thumbnail_url": "https://raw.githubusercontent.com/Norevio/halloween-prank-data/main/data/explore/explore_01_thumb.jpg",
      "cdn_video_url": "https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main/data/explore/explore_01.mp4",
      "cdn_thumbnail_url": "https://cdn.jsdelivr.net/gh/Norevio/halloween-prank-data@main/data/explore/explore_01_thumb.jpg",
      "relative_path": "data/explore/explore_01.mp4",
      "relative_thumb_path": "data/explore/explore_01_thumb.jpg",
      "duration": 13.2,
      "source_url": "https://www.pinterest.com/pin/728035096001886620/"
    }
  ]
}
```

---

## 🛠 Thống kê danh mục

| Danh mục | Loại | Số lượng | Thư mục |
| :--- | :--- | :--- | :--- |
| **Ghosts** | Video Call | 4 | `data/video_calls/ghosts/` |
| **Undead** | Video Call | 4 | `data/video_calls/undead/` |
| **Classic** | Video Call | 4 | `data/video_calls/classic/` |
| **Alien** | Video Call | 4 | `data/video_calls/alien/` |
| **Temptress** | Video Call | 6 | `data/video_calls/temptress/` |
| **Jumpscare** | Video Call | 4 | `data/video_calls/jumpscare/` |
| **Explore** | Explore | 9 | `data/explore/` |
| **Tổng cộng** | | **35** | |
