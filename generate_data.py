"""
Social Media Analytics - Data Generator
========================================
Script untuk generate synthetic social media dataset
yang realistis untuk keperluan portofolio data analyst.

Author: Data Analyst Portfolio Project
Date: 2024
"""

import json
import random
from datetime import datetime, timedelta

# Seed untuk reproducibility
random.seed(42)

# ─────────────────────────────────────────
# KONFIGURASI
# ─────────────────────────────────────────
PLATFORMS = ["Instagram", "TikTok", "Twitter", "YouTube", "LinkedIn"]
CONTENT_TYPES = ["Video", "Image", "Carousel", "Story", "Reel", "Text"]
CATEGORIES = ["Product", "Educational", "Entertainment", "Behind The Scene", "Promotion", "User Generated Content"]
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)
NUM_POSTS = 500

PLATFORM_CONFIG = {
    "Instagram": {
        "avg_followers": 45000,
        "follower_growth_rate": 0.015,
        "base_reach_pct": 0.12,
        "content_types": ["Image", "Carousel", "Reel", "Story"],
        "peak_hours": [8, 12, 18, 21],
        "peak_days": [1, 3, 5],  # Tue, Thu, Sat (0=Mon)
    },
    "TikTok": {
        "avg_followers": 82000,
        "follower_growth_rate": 0.03,
        "base_reach_pct": 0.35,
        "content_types": ["Video", "Story"],
        "peak_hours": [17, 19, 21, 23],
        "peak_days": [1, 2, 3, 4, 5],
    },
    "Twitter": {
        "avg_followers": 18000,
        "follower_growth_rate": 0.008,
        "base_reach_pct": 0.05,
        "content_types": ["Text", "Image"],
        "peak_hours": [7, 9, 12, 17],
        "peak_days": [0, 1, 2, 3, 4],
    },
    "YouTube": {
        "avg_followers": 31000,
        "follower_growth_rate": 0.012,
        "base_reach_pct": 0.08,
        "content_types": ["Video"],
        "peak_hours": [14, 16, 20],
        "peak_days": [5, 6],  # Sat, Sun
    },
    "LinkedIn": {
        "avg_followers": 9500,
        "follower_growth_rate": 0.02,
        "base_reach_pct": 0.07,
        "content_types": ["Text", "Image", "Carousel"],
        "peak_hours": [8, 10, 12],
        "peak_days": [0, 1, 2, 3, 4],
    },
}


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days), hours=random.randint(0, 23))


def engagement_multiplier(post_date, config):
    """Hitung multiplier berdasarkan waktu posting."""
    mult = 1.0
    if post_date.hour in config["peak_hours"]:
        mult *= random.uniform(1.2, 1.6)
    if post_date.weekday() in config["peak_days"]:
        mult *= random.uniform(1.1, 1.4)
    return mult


def generate_post(post_id, platform):
    config = PLATFORM_CONFIG[platform]
    post_date = random_date(START_DATE, END_DATE)

    # Hitung followers di tanggal tersebut
    days_elapsed = (post_date - START_DATE).days
    followers = int(
        config["avg_followers"] * (1 + config["follower_growth_rate"] * days_elapsed / 30)
    )

    content_type = random.choice(config["content_types"])
    category = random.choice(CATEGORIES)

    # Engagement calculation
    mult = engagement_multiplier(post_date, config)
    reach = int(followers * config["base_reach_pct"] * random.uniform(0.6, 2.5) * mult)
    impressions = int(reach * random.uniform(1.1, 2.0))

    like_rate = random.uniform(0.03, 0.15) * mult
    comment_rate = random.uniform(0.005, 0.03) * mult
    share_rate = random.uniform(0.002, 0.015) * mult
    save_rate = random.uniform(0.01, 0.05) * mult

    likes = int(reach * like_rate)
    comments = int(reach * comment_rate)
    shares = int(reach * share_rate)
    saves = int(reach * save_rate)

    total_engagement = likes + comments + shares + saves
    engagement_rate = round((total_engagement / followers) * 100, 2) if followers > 0 else 0

    # Video views
    video_views = int(reach * random.uniform(0.4, 0.85)) if content_type in ["Video", "Reel", "Story"] else 0

    # Link clicks
    link_clicks = int(reach * random.uniform(0.005, 0.03)) if platform in ["Instagram", "LinkedIn"] else 0

    return {
        "post_id": f"POST_{post_id:04d}",
        "platform": platform,
        "content_type": content_type,
        "category": category,
        "post_date": post_date.strftime("%Y-%m-%d"),
        "post_hour": post_date.hour,
        "day_of_week": post_date.strftime("%A"),
        "month": post_date.strftime("%B"),
        "month_num": post_date.month,
        "followers_at_post": followers,
        "reach": reach,
        "impressions": impressions,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "saves": saves,
        "video_views": video_views,
        "link_clicks": link_clicks,
        "total_engagement": total_engagement,
        "engagement_rate": engagement_rate,
    }


def generate_dataset():
    print("📊 Generating Social Media Analytics Dataset...")
    posts = []
    post_id = 1

    # Distribute posts across platforms
    for platform in PLATFORMS:
        num_platform_posts = NUM_POSTS // len(PLATFORMS)
        for _ in range(num_platform_posts):
            posts.append(generate_post(post_id, platform))
            post_id += 1

    # Sort by date
    posts.sort(key=lambda x: x["post_date"])

    print(f"✅ Generated {len(posts)} posts across {len(PLATFORMS)} platforms")

    # Save as JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print("💾 Dataset saved to data.json")

    # Print summary
    print("\n📈 Dataset Summary:")
    for platform in PLATFORMS:
        platform_posts = [p for p in posts if p["platform"] == platform]
        avg_er = sum(p["engagement_rate"] for p in platform_posts) / len(platform_posts)
        print(f"  {platform}: {len(platform_posts)} posts | Avg ER: {avg_er:.2f}%")

    return posts


if __name__ == "__main__":
    generate_dataset()
    print("\n✨ Dataset generation complete! Ready for analysis.")
